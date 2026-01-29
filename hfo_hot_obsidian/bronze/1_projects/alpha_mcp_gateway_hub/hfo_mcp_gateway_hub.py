#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""
HFO MCP Gateway Hub (Single Entry Path)
- Enforces receipt chain: think_receipt -> p5_audit_receipt -> commit_receipt
- Logs to blackboard and DuckDB mission journal
"""

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET

import duckdb
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

try:
    from pathlib import Path

    _here = Path(__file__).resolve()
    for _parent in [_here.parent] + list(_here.parents):
        if (_parent / "hfo_pointers.py").exists() and (_parent / "hfo_pointers.json").exists():
            if str(_parent) not in sys.path:
                sys.path.insert(0, str(_parent))
            break
except Exception:
    _BOOTSTRAP_PATH_RESOLUTION_ERROR = True

BASE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
BLACKBOARD_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl")
try:
    from hfo_pointers import resolve_path

    DUCKDB_PATH = resolve_path(
        env_var="HFO_DUCKDB_UNIFIED_PATH",
        dotted_key="paths.duckdb_unified",
    )
    FILE_INDEX_DB_PATH = resolve_path(
        env_var="HFO_DUCKDB_FILE_INDEX_PATH",
        dotted_key="paths.duckdb_file_index",
    )
except Exception:
    DUCKDB_PATH = os.environ.get(
        "HFO_DUCKDB_UNIFIED_PATH",
        "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb",
    )
    BASE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
    FILE_INDEX_DB_PATH = os.path.join(
        BASE_PATH, os.environ.get("HFO_DUCKDB_FILE_INDEX_PATH", "hfo_unified_v88_merged.duckdb")
    )
RECEIPTS_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/3_resources/receipts/hfo_mcp_gateway_receipts.jsonl")
BATON_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/3_resources/receipts/hfo_mcp_gateway_baton.jsonl")
MCP_MEMORY_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl")
SERENA_MEMORY_DIR = os.path.join(BASE_PATH, ".serena/memories")

SILVER_REPORTS_DIR = os.path.join(BASE_PATH, "hfo_hot_obsidian/silver/3_resources/reports")

server = Server("hfo-mcp-gateway-hub")


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _append_receipt(receipt_type: str, payload: dict) -> str:
    receipt_id = hashlib.sha256(f"{receipt_type}{_now_iso()}".encode()).hexdigest()[:12]
    entry = {
        "type": receipt_type,
        "receipt_id": receipt_id,
        "timestamp": _now_iso(),
        "payload": payload,
    }
    os.makedirs(os.path.dirname(RECEIPTS_PATH), exist_ok=True)
    with open(RECEIPTS_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return receipt_id


def _last_receipt_type() -> str | None:
    if not os.path.exists(RECEIPTS_PATH):
        return None
    try:
        tail = _read_jsonl_tail(RECEIPTS_PATH, limit=1)
        if not tail:
            return None
        last = tail[-1]
        if isinstance(last, dict):
            t = last.get("type")
            return str(t) if t is not None else None
        return None
    except Exception:
        return None


def _log_blackboard(entry: dict) -> None:
    try:
        entry.setdefault("timestamp", _now_iso())
        try:
            from pathlib import Path

            from hfo_blackboard_events import append_signed_entry

            append_signed_entry(dict(entry), blackboard_path=Path(BLACKBOARD_PATH))
            return
        except Exception:
            with open(BLACKBOARD_PATH, "a") as f:
                f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Error logging to blackboard: {e}", file=sys.stderr)


def _file_info(path: str) -> dict:
    exists = os.path.exists(path)
    info = {"path": path, "exists": exists}
    if not exists:
        return info
    try:
        stat = os.stat(path)
        info.update(
            {
                "size_bytes": stat.st_size,
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime, datetime.timezone.utc).isoformat(),
            }
        )
    except Exception as e:
        info["error"] = str(e)
    return info


def _read_jsonl_tail(path: str, limit: int) -> list[dict]:
    """Read the last N JSONL records without loading the entire file.

    This is intentionally bounded to prevent OOM when JSONL logs grow large
    (e.g. MCP working memory). We read from the end of the file in chunks.
    """
    if not os.path.exists(path):
        return []

    limit = max(1, min(int(limit or 0), 2000))

    max_bytes_env = os.environ.get("HFO_JSONL_TAIL_MAX_BYTES", "")
    try:
        max_bytes = int(max_bytes_env) if max_bytes_env.strip() else 4 * 1024 * 1024
    except Exception:
        max_bytes = 4 * 1024 * 1024
    max_bytes = max(64 * 1024, min(max_bytes, 64 * 1024 * 1024))

    block_size = 64 * 1024
    data = b""
    bytes_read = 0
    file_size = 0
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            file_size = f.tell()

            while bytes_read < file_size and bytes_read < max_bytes:
                read_size = min(block_size, file_size - bytes_read, max_bytes - bytes_read)
                if read_size <= 0:
                    break
                bytes_read += read_size
                f.seek(file_size - bytes_read)
                chunk = f.read(read_size)
                if not chunk:
                    break
                data = chunk + data

                # If we have enough newlines for the requested tail, stop early.
                if data.count(b"\n") >= (limit + 1):
                    break
    except Exception:
        if os.environ.get("HFO_DEBUG_JSONL_TAIL") == "1":
            raise
        return []

    # Split into lines; drop the first line if it may be a partial line.
    lines = [ln for ln in data.splitlines() if ln.strip()]
    # If we didn't read the full file, the first line may be partial. Drop it only
    # if we still have enough lines to satisfy the requested tail; otherwise keep
    # it (and it may parse as a parse_error record).
    if bytes_read < file_size and len(lines) > limit:
        lines = lines[1:]

    tail = lines[-limit:]
    parsed: list[dict] = []
    for raw in tail:
        try:
            text = raw.decode("utf-8", errors="replace")
            parsed.append(json.loads(text))
        except Exception:
            try:
                parsed.append({"parse_error": True, "raw": raw.decode("utf-8", errors="replace")})
            except Exception:
                parsed.append({"parse_error": True, "raw": "(un-decodable)"})
    return parsed


def _append_jsonl(path: str, entry: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def _read_pointers_subset() -> dict:
    path = os.path.join(BASE_PATH, "hfo_pointers.json")
    if not os.path.exists(path):
        return {"path": path, "exists": False}
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return {
            "path": path,
            "exists": True,
            "targets": data.get("targets", {}),
            "paths": data.get("paths", {}),
        }
    except Exception as e:
        return {"path": path, "exists": True, "error": str(e)}


def _list_recent_silver_reports(limit: int) -> list[dict]:
    limit = max(0, min(int(limit or 0), 50))
    if limit == 0:
        return []
    if not os.path.isdir(SILVER_REPORTS_DIR):
        return [{"path": SILVER_REPORTS_DIR, "exists": False}]
    items: list[dict] = []
    for name in os.listdir(SILVER_REPORTS_DIR):
        if not name.endswith(".md"):
            continue
        path = os.path.join(SILVER_REPORTS_DIR, name)
        if not os.path.isfile(path):
            continue
        items.append(_file_info(path))
    items.sort(key=lambda x: x.get("modified", ""), reverse=True)
    return items[:limit]


def _enforce_resource_limits(snapshot: dict, arguments: dict) -> str | None:
    try:
        min_mem_kb = arguments.get("min_mem_available_kb")
        max_load_1m = arguments.get("max_load_1m")
        if min_mem_kb is not None:
            min_mem_kb = int(min_mem_kb)
            avail = int(snapshot.get("memory_kb", {}).get("available", 0))
            if avail < min_mem_kb:
                return f"Resource gate: MemAvailable {avail}KB < {min_mem_kb}KB"
        if max_load_1m is not None:
            max_load_1m = float(max_load_1m)
            load_1m = float(snapshot.get("load_avg", {}).get("1m", 0.0))
            if load_1m > max_load_1m:
                return f"Resource gate: load_1m {load_1m} > {max_load_1m}"
    except Exception as e:
        return f"Resource gate: invalid thresholds ({e})"
    return None


def _build_context_capsule(port: str, role: str, system_health: dict, arguments: dict) -> dict:
    blackboard_tail = int(arguments.get("blackboard_tail", 10))
    mcp_memory_tail = int(arguments.get("mcp_memory_tail", 20))
    recent_reports = int(arguments.get("recent_reports", 10))
    scope = arguments.get("scope")
    subshard_path = arguments.get("subshard_path")
    capsule = {
        "timestamp": _now_iso(),
        "scope": scope or port,
        "subshard_path": subshard_path,
        "port": port,
        "role": role,
        "note": arguments.get("note", ""),
        "system_health": system_health,
        "pointers": _read_pointers_subset(),
        "short_term_blackboard": {
            "info": _file_info(BLACKBOARD_PATH),
            "tail": _read_jsonl_tail(BLACKBOARD_PATH, blackboard_tail),
        },
        "working_memory_mcp": {
            "info": _file_info(MCP_MEMORY_PATH),
            "tail": _read_jsonl_tail(MCP_MEMORY_PATH, mcp_memory_tail),
        },
        "silver_reports_recent": _list_recent_silver_reports(recent_reports),
    }
    return capsule


def _list_serena_memories() -> list[str]:
    if not os.path.isdir(SERENA_MEMORY_DIR):
        return []
    return sorted([name for name in os.listdir(SERENA_MEMORY_DIR) if name.endswith(".md")])


def _read_serena_memory(name: str) -> str | None:
    if not name.endswith(".md"):
        name = f"{name}.md"
    path = os.path.join(SERENA_MEMORY_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return f.read()


def _write_serena_memory(name: str, content: str, overwrite: bool) -> str:
    if not name.endswith(".md"):
        name = f"{name}.md"
    os.makedirs(SERENA_MEMORY_DIR, exist_ok=True)
    path = os.path.join(SERENA_MEMORY_DIR, name)
    if os.path.exists(path) and not overwrite:
        return "exists"
    with open(path, "w") as f:
        f.write(content)
    return "written"


def _last_baton_signature() -> str:
    if not os.path.exists(BATON_PATH):
        return "0" * 64
    try:
        with open(BATON_PATH, "r") as f:
            lines = [line for line in f.read().splitlines() if line.strip()]
        if not lines:
            return "0" * 64
        last = json.loads(lines[-1])
        return last.get("signature", "0" * 64)
    except Exception:
        return "0" * 64


def _log_baton(phase_from: str, phase_to: str, receipt_id: str, payload: dict) -> None:
    try:
        phase_names = {
            "PHASE_1": "Hindsight - Hunting Hyperheuristics",
            "PHASE_2": "Insight - Interlocking Interfaces",
            "PHASE_3": "Validated Foresight - Validation Vanguards",
            "PHASE_4": "Evolve - Evolving Engines",
        }
        entry = {
            "timestamp": _now_iso(),
            "phase": "BATON",
            "from": phase_from,
            "to": phase_to,
            "from_name": phase_names.get(phase_from),
            "to_name": phase_names.get(phase_to),
            "receipt_id": receipt_id,
            "payload": payload,
        }
        prev_sig = _last_baton_signature()
        content = json.dumps(entry, sort_keys=True)
        sig = hashlib.sha256(f"{prev_sig}{content}".encode()).hexdigest()
        entry["prev_signature"] = prev_sig
        entry["signature"] = sig
        os.makedirs(os.path.dirname(BATON_PATH), exist_ok=True)
        with open(BATON_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Error logging baton: {e}", file=sys.stderr)


def _log_handoff_baton(role_from: str, role_to: str, receipt_id: str, payload: dict) -> None:
    try:
        entry = {
            "timestamp": _now_iso(),
            "phase": "HANDOFF",
            "from": role_from,
            "to": role_to,
            "receipt_id": receipt_id,
            "payload": payload,
        }
        prev_sig = _last_baton_signature()
        content = json.dumps(entry, sort_keys=True)
        sig = hashlib.sha256(f"{prev_sig}{content}".encode()).hexdigest()
        entry["prev_signature"] = prev_sig
        entry["signature"] = sig
        os.makedirs(os.path.dirname(BATON_PATH), exist_ok=True)
        with open(BATON_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"Error logging handoff baton: {e}", file=sys.stderr)


def _log_duckdb(event_type: str, payload: dict) -> None:
    try:
        conn = duckdb.connect(DUCKDB_PATH)
        # Existing DuckDB files may already have a mission_journal schema.
        # Fail-open on schema differences (never break tool execution).
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mission_journal (
                event_id VARCHAR PRIMARY KEY,
                actor_id VARCHAR,
                event_type VARCHAR,
                payload VARCHAR,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        columns = set()
        try:
            rows = conn.execute("PRAGMA table_info('mission_journal')").fetchall()
            # rows: (cid, name, type, notnull, dflt_value, pk)
            columns = {r[1] for r in rows}
        except Exception:
            columns = set()

        if "event_id" in columns:
            conn.execute(
                "INSERT INTO mission_journal (event_id, actor_id, event_type, payload) VALUES (?, ?, ?, ?)",
                (uuid.uuid4().hex, "HFO_MCP_GATEWAY", event_type, json.dumps(payload)),
            )
        elif "id" in columns:
            conn.execute("CREATE SEQUENCE IF NOT EXISTS mission_journal_id_seq")
            conn.execute(
                "INSERT INTO mission_journal (id, actor_id, event_type, payload) VALUES (nextval('mission_journal_id_seq'), ?, ?, ?)",
                ("HFO_MCP_GATEWAY", event_type, json.dumps(payload)),
            )
        else:
            conn.execute(
                "INSERT INTO mission_journal (actor_id, event_type, payload) VALUES (?, ?, ?)",
                ("HFO_MCP_GATEWAY", event_type, json.dumps(payload)),
            )
        conn.close()
    except Exception as e:
        print(f"Error logging to DuckDB: {e}", file=sys.stderr)


def _tavily_search(query: str, max_results: int) -> dict:
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return {"error": "TAVILY_API_KEY not found in environment."}
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
    }
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"Tavily HTTPError: {e.code}", "detail": e.read().decode("utf-8")}
    except Exception as e:
        return {"error": f"Tavily request failed: {e}"}


def _duckduckgo_search(query: str, max_results: int) -> dict:
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "no_redirect": 1,
        "skip_disambig": 1,
    }
    url = "https://api.duckduckgo.com/?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "HFO-MCP-Gateway"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        topics = data.get("RelatedTopics", [])
        results = []
        for item in topics:
            if "Text" in item and "FirstURL" in item:
                results.append({"text": item.get("Text"), "url": item.get("FirstURL")})
            elif "Topics" in item:
                for sub in item.get("Topics", []):
                    if "Text" in sub and "FirstURL" in sub:
                        results.append({"text": sub.get("Text"), "url": sub.get("FirstURL")})
        return {"results": results[: max_results]}
    except Exception as e:
        return {"error": f"DuckDuckGo request failed: {e}"}


def _wikipedia_search(query: str, max_results: int) -> dict:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": max_results,
    }
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "HFO-MCP-Gateway"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": f"Wikipedia request failed: {e}"}


def _arxiv_search(query: str, max_results: int) -> dict:
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "HFO-MCP-Gateway"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml_data = resp.read().decode("utf-8")
        root = ET.fromstring(xml_data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = []
        for entry in root.findall("atom:entry", ns):
            entries.append({
                "id": entry.findtext("atom:id", default="", namespaces=ns),
                "title": entry.findtext("atom:title", default="", namespaces=ns).strip(),
                "summary": entry.findtext("atom:summary", default="", namespaces=ns).strip(),
                "published": entry.findtext("atom:published", default="", namespaces=ns),
            })
        return {"results": entries}
    except Exception as e:
        return {"error": f"arXiv request failed: {e}"}


def _rg_search(query: str, limit: int, path: str) -> dict:
    if not shutil.which("rg"):
        return {"error": "ripgrep (rg) not found on PATH."}
    if not os.path.exists(path):
        return {"error": f"search path not found: {path}"}
    cmd = ["rg", "--no-heading", "--line-number", "--max-count", str(limit), query, path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 1:
            return {"results": []}
        if result.returncode != 0:
            return {"error": result.stderr.strip()}
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        return {"results": lines}
    except Exception as e:
        return {"error": f"ripgrep failed: {e}"}


def _offline_wiki_search(query: str, limit: int) -> dict:
    wiki_path = os.environ.get("OFFLINE_WIKI_PATH")
    if not wiki_path:
        return {"error": "OFFLINE_WIKI_PATH not set in environment."}
    return _rg_search(query, limit, wiki_path)


def _context7_search(query: str, max_results: int) -> dict:
    api_key = os.environ.get("CONTEXT7_API_KEY")
    if not api_key:
        return {"error": "CONTEXT7_API_KEY not found in environment."}
    return {
        "status": "pending",
        "msg": "Context7 MCP integration not wired in gateway hub yet.",
        "query": query,
        "max_results": max_results,
    }


def _duck_search(query: str, limit: int) -> dict:
    terms = [t for t in re.split(r"\s+", query.strip()) if t]
    if not terms:
        return {"error": "No search terms provided."}
    clause = " OR ".join(["path ILIKE ?" for _ in terms])
    sql = f"""
        SELECT path, score, modified_at
        FROM file_system
        WHERE {clause}
        ORDER BY modified_at DESC
        LIMIT ?
    """
    params = [f"%{t}%" for t in terms] + [limit]
    try:
        conn = duckdb.connect(FILE_INDEX_DB_PATH)
        rows = conn.execute(sql, params).fetchall()
        cols = [desc[0] for desc in conn.description]
        return {"results": [dict(zip(cols, row)) for row in rows]}
    except Exception as e:
        return {"error": f"DuckDB query failed: {e}"}
    finally:
        try:
            conn.close()
        except Exception:
            ...


def _openrouter_chat(model: str, messages: list[dict]) -> dict:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "OPENROUTER_API_KEY not found in environment."}
    body = {
        "model": model,
        "messages": messages,
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/hfo-gen-88",
            "X-Title": "HFO-MCP-Gateway-Hub",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"OpenRouter HTTPError: {e.code}", "detail": e.read().decode("utf-8")}
    except Exception as e:
        return {"error": f"OpenRouter request failed: {e}"}


def _tool_health_quick() -> dict:
    health = {
        "tavily_key": bool(os.environ.get("TAVILY_API_KEY")),
        "openrouter_key": bool(os.environ.get("OPENROUTER_API_KEY")),
        "context7_key": bool(os.environ.get("CONTEXT7_API_KEY")),
        "offline_wiki_path": bool(os.environ.get("OFFLINE_WIKI_PATH")),
        "rg_available": bool(shutil.which("rg")),
        "duckdb_exists": os.path.exists(DUCKDB_PATH),
        "file_index_db_exists": os.path.exists(FILE_INDEX_DB_PATH),
        "gateway_receipts_exists": os.path.exists(RECEIPTS_PATH),
    }
    health["ok"] = all(health.values())
    return health


def _read_meminfo() -> dict:
    meminfo = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":", 1)
                if len(parts) != 2:
                    continue
                key = parts[0].strip()
                value = parts[1].strip().split()[0]
                meminfo[key] = int(value)
    except Exception as e:
        meminfo["error"] = str(e)
    return meminfo


def _system_health_snapshot() -> dict:
    meminfo = _read_meminfo()
    total_kb = meminfo.get("MemTotal", 0)
    avail_kb = meminfo.get("MemAvailable", 0)
    used_kb = max(0, total_kb - avail_kb)
    disk = shutil.disk_usage(BASE_PATH)
    load = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)
    return {
        "timestamp": _now_iso(),
        "cpu_count": os.cpu_count(),
        "load_avg": {"1m": load[0], "5m": load[1], "15m": load[2]},
        "memory_kb": {
            "total": total_kb,
            "available": avail_kb,
            "used": used_kb,
        },
        "disk_bytes": {
            "path": BASE_PATH,
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
        },
    }


def _health_notice_text(snapshot: dict) -> str:
    return json.dumps({"system_health": snapshot}, indent=2)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="local_code_search",
            description="Local code search using ripgrep across the workspace.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 50},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="duckdb_index_search",
            description="Local DuckDB file_system index search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 20},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="offline_wiki_search",
            description="Offline wiki search via ripgrep (uses OFFLINE_WIKI_PATH).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 20},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="wikipedia_search",
            description="Wikipedia API search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="arxiv_search",
            description="arXiv API search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="duckduckgo_search",
            description="DuckDuckGo Instant Answer API search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="tavily_search",
            description="Tavily web search.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="context7_search",
            description="Context7 docs search (requires MCP wiring/API key).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="memory_status",
            description="Return status for short-term, working, and long-term memory stores.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="read_blackboard_tail",
            description="Read last N entries from hot_obsidian_blackboard.jsonl (short-term memory).",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 20},
                },
            },
        ),
        types.Tool(
            name="list_mcp_memory",
            description="Read last N entries from MCP memory JSONL (working memory).",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 50},
                },
            },
        ),
        types.Tool(
            name="append_mcp_memory",
            description="Append a JSONL entry to MCP memory (working memory).",
            inputSchema={
                "type": "object",
                "properties": {
                    "entry": {"type": "object"},
                },
                "required": ["entry"],
            },
        ),
        types.Tool(
            name="list_serena_memories",
            description="List Serena memory files (integration layer).",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="read_serena_memory",
            description="Read a Serena memory file by name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
                "required": ["name"],
            },
        ),
        types.Tool(
            name="write_serena_memory",
            description="Write a Serena memory file by name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                    "overwrite": {"type": "boolean", "default": False},
                },
                "required": ["name", "content"],
            },
        ),
        types.Tool(
            name="port6_assimilate",
            description=(
                "Port 6 Assimilate (Kraken Keeper). Consolidate subshard memory systems: "
                "short-term blackboard, working MCP memory graph, Serena memories, long-term DuckDB store."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "blackboard_tail": {"type": "integer", "default": 10},
                    "mcp_memory_tail": {"type": "integer", "default": 20},
                    "include_serena_list": {"type": "boolean", "default": True},
                },
            },
        ),
        types.Tool(
            name="port6_preflight",
            description=(
                "Port 6 preflight: compile a bounded context capsule (SSOT inputs + resource snapshot). "
                "Designed to be called at the start of every agent run."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {"type": "string", "default": "agent"},
                    "note": {"type": "string"},
                    "blackboard_tail": {"type": "integer", "default": 10},
                    "mcp_memory_tail": {"type": "integer", "default": 20},
                    "recent_reports": {"type": "integer", "default": 10},
                    "min_mem_available_kb": {"type": "integer"},
                    "max_load_1m": {"type": "number"},
                    "write_memory": {"type": "boolean", "default": True},
                },
            },
        ),
        types.Tool(
            name="port6_postflight",
            description=(
                "Port 6 postflight: write an append-only receipt + (optional) memory entry summarizing outcomes and proof. "
                "Designed to be called at the end of every agent run."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "preflight_receipt_id": {"type": "string"},
                    "outcome": {"type": "string", "enum": ["ok", "partial", "error"], "default": "ok"},
                    "summary": {"type": "string"},
                    "changes": {"type": "array", "items": {"type": "string"}, "default": []},
                    "sources": {"type": "array", "items": {"type": "string"}, "default": []},
                    "write_memory": {"type": "boolean", "default": True},
                },
                "required": ["summary"],
            },
        ),
        types.Tool(
            name="hfo_preflight",
            description=(
                "HFO unified preflight: compile the canonical context capsule (hub-level SSOT) with resource snapshot. "
                "Use this when a run spans multiple ports or needs a single consolidated start-state."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {"type": "string", "default": "hub"},
                    "note": {"type": "string"},
                    "blackboard_tail": {"type": "integer", "default": 10},
                    "mcp_memory_tail": {"type": "integer", "default": 20},
                    "recent_reports": {"type": "integer", "default": 10},
                    "min_mem_available_kb": {"type": "integer"},
                    "max_load_1m": {"type": "number"},
                    "write_memory": {"type": "boolean", "default": True},
                },
            },
        ),
        types.Tool(
            name="hfo_postflight",
            description=(
                "HFO unified postflight: write an append-only hub-level receipt + (optional) memory entry summarizing outcomes and proof."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "preflight_receipt_id": {"type": "string"},
                    "outcome": {"type": "string", "enum": ["ok", "partial", "error"], "default": "ok"},
                    "summary": {"type": "string"},
                    "changes": {"type": "array", "items": {"type": "string"}, "default": []},
                    "sources": {"type": "array", "items": {"type": "string"}, "default": []},
                    "write_memory": {"type": "boolean", "default": True},
                },
                "required": ["summary"],
            },
        ),
        types.Tool(
            name="port_preflight",
            description=(
                "Port preflight (P0..P7): compile a bounded context capsule for a specific port and optional subshard scope. "
                "Use scope like 'P0' or 'P0.3.5.7.1' to align with the fractal octree holonarchy."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "port": {"type": "integer", "minimum": 0, "maximum": 7},
                    "scope": {"type": "string"},
                    "subshard_path": {"type": ["array", "string"], "items": {"type": "integer"}},
                    "role": {"type": "string", "default": "agent"},
                    "note": {"type": "string"},
                    "blackboard_tail": {"type": "integer", "default": 10},
                    "mcp_memory_tail": {"type": "integer", "default": 20},
                    "recent_reports": {"type": "integer", "default": 10},
                    "min_mem_available_kb": {"type": "integer"},
                    "max_load_1m": {"type": "number"},
                    "write_memory": {"type": "boolean", "default": True}
                },
                "required": ["port"],
            },
        ),
        types.Tool(
            name="port_postflight",
            description=(
                "Port postflight (P0..P7): write an append-only receipt + (optional) memory entry summarizing outcomes and proof for a port/subshard run."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "port": {"type": "integer", "minimum": 0, "maximum": 7},
                    "scope": {"type": "string"},
                    "subshard_path": {"type": ["array", "string"], "items": {"type": "integer"}},
                    "preflight_receipt_id": {"type": "string"},
                    "outcome": {"type": "string", "enum": ["ok", "partial", "error"], "default": "ok"},
                    "summary": {"type": "string"},
                    "changes": {"type": "array", "items": {"type": "string"}, "default": []},
                    "sources": {"type": "array", "items": {"type": "string"}, "default": []},
                    "write_memory": {"type": "boolean", "default": True}
                },
                "required": ["port", "summary"],
            },
        ),
        types.Tool(
            name="p0_observe_compile",
            description=(
                "P0 Observe → Tavily + DuckDB search → LLM synthesis. Returns Phase-1 H handoff baton for P7."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "model": {"type": "string", "default": "google/gemma-7b-it:free"},
                    "tavily_limit": {"type": "integer", "default": 5},
                    "duck_limit": {"type": "integer", "default": 8},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="tool_health",
            description="Quick tool health check (keys + critical files).",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="system_health",
            description="System health snapshot (CPU load, memory, disk).",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="observe_navigate",
            description="Phase 1: Observe + Navigate (creates phase1_receipt).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="bridge_assimilate",
            description="Phase 2: Bridge + Assimilate (creates phase2_receipt).",
            inputSchema={
                "type": "object",
                "properties": {
                    "note": {"type": "string"},
                },
            },
        ),
        types.Tool(
            name="shape_immunize",
            description="Phase 3: Shape + Immunize (creates phase3_receipt).",
            inputSchema={
                "type": "object",
                "properties": {
                    "note": {"type": "string"},
                    "mode": {"type": "string", "enum": ["preflight", "full"], "default": "preflight"}
                },
            },
        ),
        types.Tool(
            name="deliver_disrupt",
            description="Phase 4: Deliver + Disrupt (creates phase4_receipt).",
            inputSchema={
                "type": "object",
                "properties": {
                    "note": {"type": "string"},
                },
            },
        ),
        types.Tool(
            name="query_journal",
            description="Query DuckDB mission journal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                },
                "required": ["sql"],
            },
        ),
        types.Tool(
            name="commit",
            description="Generate a commit_receipt (no git commit executed).",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
                "required": ["message"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    arguments = arguments or {}

    health = _tool_health_quick()
    system_health = _system_health_snapshot()

    def _respond(contents: list[types.TextContent]) -> list[types.TextContent]:
        if os.environ.get("HFO_HEALTH_NOTIFY", "1") != "1":
            return contents
        notice = types.TextContent(type="text", text=_health_notice_text(system_health))
        return [notice] + contents

    if os.environ.get("HFO_HEALTH_LOG", "1") == "1":
        _log_blackboard({"type": "system_health", "snapshot": system_health})

    if name == "observe_navigate":
        receipt_id = _append_receipt("phase1_receipt", {"query": arguments.get("query", "")})
        _log_blackboard({"phase": "H", "action": "observe_navigate", "receipt_id": receipt_id, "input": arguments})
        _log_blackboard({"phase": "HANDOFF", "from": "PHASE_1", "to": "PHASE_2", "receipt_id": receipt_id})
        _log_baton("PHASE_1", "PHASE_2", receipt_id, {"input": arguments})
        _log_duckdb("observe_navigate", arguments)
        cmd = [sys.executable, os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/2_areas/architecture/ports/hfo_orchestration_hub.py"), "think", arguments.get("query", "")]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return _respond([types.TextContent(type="text", text=result.stdout + result.stderr)])

    if name == "memory_status":
        payload = {
            "short_term_blackboard": _file_info(BLACKBOARD_PATH),
            "working_memory_mcp": _file_info(MCP_MEMORY_PATH),
            "serena_memory_dir": _file_info(SERENA_MEMORY_DIR),
            "long_term_duckdb": _file_info(DUCKDB_PATH),
        }
        return _respond([types.TextContent(type="text", text=json.dumps(payload, indent=2))])

    if name == "read_blackboard_tail":
        limit = int(arguments.get("limit", 20))
        entries = _read_jsonl_tail(BLACKBOARD_PATH, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(entries, indent=2))])

    if name == "list_mcp_memory":
        limit = int(arguments.get("limit", 50))
        entries = _read_jsonl_tail(MCP_MEMORY_PATH, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(entries, indent=2))])

    if name == "append_mcp_memory":
        entry = arguments.get("entry")
        if not isinstance(entry, dict):
            return _respond([types.TextContent(type="text", text="Error: entry must be an object.")])
        if "type" not in entry:
            return _respond([types.TextContent(type="text", text="Error: entry.type is required.")])
        _append_jsonl(MCP_MEMORY_PATH, entry)
        return _respond([types.TextContent(type="text", text="mcp_memory_append: ok")])

    if name == "list_serena_memories":
        names = _list_serena_memories()
        return _respond([types.TextContent(type="text", text=json.dumps(names, indent=2))])

    if name == "read_serena_memory":
        name_arg = arguments.get("name", "")
        if not name_arg:
            return _respond([types.TextContent(type="text", text="Error: name is required.")])
        content = _read_serena_memory(name_arg)
        if content is None:
            return _respond([types.TextContent(type="text", text="Error: memory not found.")])
        return _respond([types.TextContent(type="text", text=content)])

    if name == "write_serena_memory":
        name_arg = arguments.get("name", "")
        content = arguments.get("content", "")
        overwrite = bool(arguments.get("overwrite", False))
        if not name_arg:
            return _respond([types.TextContent(type="text", text="Error: name is required.")])
        result = _write_serena_memory(name_arg, content, overwrite)
        if result == "exists":
            return _respond([types.TextContent(type="text", text="Error: memory exists (set overwrite=true to replace).")])
        return _respond([types.TextContent(type="text", text="serena_memory_write: ok")])

    if name == "port6_assimilate":
        blackboard_tail = int(arguments.get("blackboard_tail", 10))
        mcp_memory_tail = int(arguments.get("mcp_memory_tail", 20))
        include_serena_list = bool(arguments.get("include_serena_list", True))
        payload = {
            "kraken_keeper": {
                "port": "P6",
                "role": "Assimilate",
                "theme": "Lady in the Lake; Kraken of the Depths",
                "authority": "Consolidated memory subshards",
            },
            "short_term_blackboard": {
                "info": _file_info(BLACKBOARD_PATH),
                "tail": _read_jsonl_tail(BLACKBOARD_PATH, blackboard_tail),
            },
            "working_memory_mcp": {
                "info": _file_info(MCP_MEMORY_PATH),
                "tail": _read_jsonl_tail(MCP_MEMORY_PATH, mcp_memory_tail),
            },
            "serena_memory": {
                "info": _file_info(SERENA_MEMORY_DIR),
                "list": _list_serena_memories() if include_serena_list else [],
            },
            "long_term_duckdb": _file_info(DUCKDB_PATH),
        }
        _log_blackboard({"phase": "P6", "action": "port6_assimilate", "input": arguments})
        _log_duckdb("port6_assimilate", {"input": arguments})
        return _respond([types.TextContent(type="text", text=json.dumps(payload, indent=2))])

    if name == "port_preflight":
        port_num = arguments.get("port")
        try:
            port_num = int(port_num)
        except Exception:
            return _respond([types.TextContent(type="text", text="Error: port must be an integer 0..7")])
        if port_num < 0 or port_num > 7:
            return _respond([types.TextContent(type="text", text="Error: port must be in range 0..7")])

        port = f"P{port_num}"
        role = str(arguments.get("role", "agent"))
        gate_err = _enforce_resource_limits(system_health, arguments)
        if gate_err:
            return _respond([types.TextContent(type="text", text=f"Error: {gate_err}")])

        capsule = _build_context_capsule(port, role, system_health, arguments)
        receipt_type = f"{port.lower()}_preflight_receipt"
        receipt_id = _append_receipt(receipt_type, {"port": port, "role": role, "scope": arguments.get("scope")})
        _log_blackboard({"phase": port, "action": "preflight", "receipt_id": receipt_id, "input": arguments})
        _log_duckdb(f"{port.lower()}_preflight", {"receipt_id": receipt_id, "input": arguments})

        if bool(arguments.get("write_memory", True)):
            _append_jsonl(
                MCP_MEMORY_PATH,
                {
                    "type": "flight_pre",
                    "timestamp": _now_iso(),
                    "port": port,
                    "role": role,
                    "scope": arguments.get("scope"),
                    "subshard_path": arguments.get("subshard_path"),
                    "receipt_id": receipt_id,
                    "capsule": capsule,
                },
            )

        return _respond([types.TextContent(type="text", text=json.dumps({"receipt_id": receipt_id, "capsule": capsule}, indent=2))])

    if name == "port_postflight":
        port_num = arguments.get("port")
        try:
            port_num = int(port_num)
        except Exception:
            return _respond([types.TextContent(type="text", text="Error: port must be an integer 0..7")])
        if port_num < 0 or port_num > 7:
            return _respond([types.TextContent(type="text", text="Error: port must be in range 0..7")])

        port = f"P{port_num}"
        outcome = str(arguments.get("outcome", "ok"))
        preflight_receipt_id = str(arguments.get("preflight_receipt_id", ""))
        summary = str(arguments.get("summary", ""))
        changes = arguments.get("changes", [])
        sources = arguments.get("sources", [])
        if not isinstance(changes, list):
            changes = [str(changes)]
        if not isinstance(sources, list):
            sources = [str(sources)]

        receipt_type = f"{port.lower()}_postflight_receipt"
        receipt_id = _append_receipt(
            receipt_type,
            {
                "port": port,
                "scope": arguments.get("scope"),
                "subshard_path": arguments.get("subshard_path"),
                "outcome": outcome,
                "preflight_receipt_id": preflight_receipt_id,
                "summary": summary,
            },
        )
        _log_blackboard(
            {
                "phase": port,
                "action": "postflight",
                "receipt_id": receipt_id,
                "preflight_receipt_id": preflight_receipt_id,
                "outcome": outcome,
                "scope": arguments.get("scope"),
            }
        )
        _log_duckdb(f"{port.lower()}_postflight", {"receipt_id": receipt_id, "outcome": outcome})

        if bool(arguments.get("write_memory", True)):
            _append_jsonl(
                MCP_MEMORY_PATH,
                {
                    "type": "flight_post",
                    "timestamp": _now_iso(),
                    "port": port,
                    "scope": arguments.get("scope"),
                    "subshard_path": arguments.get("subshard_path"),
                    "receipt_id": receipt_id,
                    "preflight_receipt_id": preflight_receipt_id,
                    "outcome": outcome,
                    "summary": summary,
                    "changes": [str(x) for x in changes],
                    "sources": [str(x) for x in sources],
                },
            )

        return _respond([types.TextContent(type="text", text=json.dumps({"receipt_id": receipt_id}, indent=2))])

    if name in {"port6_preflight", "hfo_preflight"}:
        port = "P6" if name == "port6_preflight" else "HFO"
        role = str(arguments.get("role", "agent" if port == "P6" else "hub"))
        gate_err = _enforce_resource_limits(system_health, arguments)
        if gate_err:
            return _respond([types.TextContent(type="text", text=f"Error: {gate_err}")])
        capsule = _build_context_capsule(port, role, system_health, arguments)
        receipt_type = "p6_preflight_receipt" if port == "P6" else "hfo_preflight_receipt"
        receipt_id = _append_receipt(receipt_type, {"port": port, "role": role})
        _log_blackboard({"phase": port, "action": "preflight", "receipt_id": receipt_id, "input": arguments})
        _log_duckdb(f"{port.lower()}_preflight", {"receipt_id": receipt_id, "input": arguments})

        if bool(arguments.get("write_memory", True)):
            _append_jsonl(
                MCP_MEMORY_PATH,
                {
                    "type": "flight_pre",
                    "timestamp": _now_iso(),
                    "port": port,
                    "role": role,
                    "receipt_id": receipt_id,
                    "capsule": capsule,
                },
            )

        return _respond([types.TextContent(type="text", text=json.dumps({"receipt_id": receipt_id, "capsule": capsule}, indent=2))])

    if name in {"port6_postflight", "hfo_postflight"}:
        port = "P6" if name == "port6_postflight" else "HFO"
        outcome = str(arguments.get("outcome", "ok"))
        preflight_receipt_id = str(arguments.get("preflight_receipt_id", ""))
        summary = str(arguments.get("summary", ""))
        changes = arguments.get("changes", [])
        sources = arguments.get("sources", [])
        if not isinstance(changes, list):
            changes = [str(changes)]
        if not isinstance(sources, list):
            sources = [str(sources)]

        receipt_type = "p6_postflight_receipt" if port == "P6" else "hfo_postflight_receipt"
        receipt_id = _append_receipt(
            receipt_type,
            {
                "port": port,
                "outcome": outcome,
                "preflight_receipt_id": preflight_receipt_id,
                "summary": summary,
            },
        )
        _log_blackboard(
            {
                "phase": port,
                "action": "postflight",
                "receipt_id": receipt_id,
                "preflight_receipt_id": preflight_receipt_id,
                "outcome": outcome,
            }
        )
        _log_duckdb(f"{port.lower()}_postflight", {"receipt_id": receipt_id, "outcome": outcome})

        if bool(arguments.get("write_memory", True)):
            _append_jsonl(
                MCP_MEMORY_PATH,
                {
                    "type": "flight_post",
                    "timestamp": _now_iso(),
                    "port": port,
                    "receipt_id": receipt_id,
                    "preflight_receipt_id": preflight_receipt_id,
                    "outcome": outcome,
                    "summary": summary,
                    "changes": [str(x) for x in changes],
                    "sources": [str(x) for x in sources],
                },
            )

        return _respond([types.TextContent(type="text", text=json.dumps({"receipt_id": receipt_id}, indent=2))])

    if name == "local_code_search":
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        limit = int(arguments.get("limit", 50))
        result = _rg_search(query, limit, BASE_PATH)
        return _respond([types.TextContent(type="text", text=json.dumps(result, indent=2))])

    if name == "duckdb_index_search":
        if not health.get("file_index_db_exists"):
            return _respond([types.TextContent(type="text", text="Error: file index DuckDB not found.")])
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        limit = int(arguments.get("limit", 20))
        result = _duck_search(query, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(result, indent=2))])

    if name == "offline_wiki_search":
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        limit = int(arguments.get("limit", 20))
        result = _offline_wiki_search(query, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(result, indent=2))])

    if name == "wikipedia_search":
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        limit = int(arguments.get("limit", 10))
        result = _wikipedia_search(query, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(result, indent=2))])

    if name == "arxiv_search":
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        limit = int(arguments.get("limit", 10))
        result = _arxiv_search(query, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(result, indent=2))])

    if name == "duckduckgo_search":
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        limit = int(arguments.get("limit", 10))
        result = _duckduckgo_search(query, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(result, indent=2))])

    if name == "tavily_search":
        if not health.get("tavily_key"):
            return _respond([types.TextContent(type="text", text="Error: TAVILY_API_KEY not found.")])
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        limit = int(arguments.get("limit", 5))
        result = _tavily_search(query, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(result, indent=2))])

    if name == "context7_search":
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        limit = int(arguments.get("limit", 5))
        result = _context7_search(query, limit)
        return _respond([types.TextContent(type="text", text=json.dumps(result, indent=2))])

    if name == "p0_observe_compile":
        if not health.get("tavily_key"):
            return _respond([types.TextContent(type="text", text="Error: TAVILY_API_KEY not found.")])
        if not health.get("openrouter_key"):
            return _respond([types.TextContent(type="text", text="Error: OPENROUTER_API_KEY not found.")])
        if not health.get("file_index_db_exists"):
            return _respond([types.TextContent(type="text", text="Error: file index DuckDB not found.")])
        query = arguments.get("query", "").strip()
        if not query:
            return _respond([types.TextContent(type="text", text="Error: query is required.")])
        model = arguments.get("model", "google/gemma-7b-it:free")
        tavily_limit = int(arguments.get("tavily_limit", 5))
        duck_limit = int(arguments.get("duck_limit", 8))

        tavily = _tavily_search(query, tavily_limit)
        duck = _duck_search(query, duck_limit)

        prompt = (
            "You are Port 0 (Observe). Compile evidence into a Phase-1 H handoff baton for Port 7. "
            "Format as JSON with keys: summary, evidence, risks, next_actions, baton_to. "
            "Use evidence from Tavily and DuckDB only; if missing, state missing."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps({"query": query, "tavily": tavily, "duck": duck})},
        ]

        llm = _openrouter_chat(model, messages)
        content = None
        try:
            content = llm.get("choices", [])[0].get("message", {}).get("content")
        except Exception:
            content = None

        receipt_id = _append_receipt("p0_handoff_receipt", {"query": query, "model": model})
        _log_blackboard({
            "phase": "H",
            "actor": "P0",
            "action": "p0_observe_compile",
            "receipt_id": receipt_id,
            "input": arguments,
        })
        _log_blackboard({
            "phase": "HANDOFF",
            "from": "P0",
            "to": "P7",
            "receipt_id": receipt_id,
        })
        _log_handoff_baton("P0", "P7", receipt_id, {"query": query, "model": model})
        _log_duckdb("p0_observe_compile", {"query": query, "model": model})

        output = {
            "receipt_id": receipt_id,
            "model": model,
            "tavily": tavily,
            "duck": duck,
            "llm": llm,
            "handoff": content,
        }
        return _respond([types.TextContent(type="text", text=json.dumps(output, indent=2))])

    if name == "tool_health":
        return _respond([types.TextContent(type="text", text=json.dumps(health, indent=2))])

    if name == "system_health":
        return _respond([types.TextContent(type="text", text=json.dumps(system_health, indent=2))])

    if name == "bridge_assimilate":
        if _last_receipt_type() != "phase1_receipt":
            return _respond([types.TextContent(type="text", text="Error: phase1_receipt required before Phase 2.")])
        receipt_id = _append_receipt("phase2_receipt", {"note": arguments.get("note", "")})
        _log_blackboard({"phase": "I", "action": "bridge_assimilate", "receipt_id": receipt_id, "input": arguments})
        _log_blackboard({"phase": "HANDOFF", "from": "PHASE_2", "to": "PHASE_3", "receipt_id": receipt_id})
        _log_baton("PHASE_2", "PHASE_3", receipt_id, {"input": arguments})
        _log_duckdb("bridge_assimilate", arguments)
        return _respond([types.TextContent(type="text", text=f"phase2_receipt: {receipt_id}")])

    if name == "shape_immunize":
        if _last_receipt_type() != "phase2_receipt":
            return _respond([types.TextContent(type="text", text="Error: phase2_receipt required before Phase 3.")])
        receipt_id = _append_receipt("phase3_receipt", {"note": arguments.get("note", "")})
        _log_blackboard({"phase": "V", "action": "shape_immunize", "receipt_id": receipt_id, "input": arguments})
        _log_blackboard({"phase": "HANDOFF", "from": "PHASE_3", "to": "PHASE_4", "receipt_id": receipt_id})
        _log_baton("PHASE_3", "PHASE_4", receipt_id, {"input": arguments})
        _log_duckdb("shape_immunize", arguments)
        mode = arguments.get("mode", "preflight")
        if mode == "preflight":
            cmd = [sys.executable, os.path.join(BASE_PATH, "scripts/p5_preflight_audit.py")]
        else:
            cmd = [sys.executable, os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/2_areas/architecture/ports/hfo_orchestration_hub.py"), "p5"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return _respond([types.TextContent(type="text", text=result.stdout + result.stderr)])

    if name == "deliver_disrupt":
        if _last_receipt_type() != "phase3_receipt":
            return _respond([types.TextContent(type="text", text="Error: phase3_receipt required before Phase 4.")])
        receipt_id = _append_receipt("phase4_receipt", {"note": arguments.get("note", "")})
        _log_blackboard({"phase": "E", "action": "deliver_disrupt", "receipt_id": receipt_id, "input": arguments})
        _log_blackboard({"phase": "HANDOFF", "from": "PHASE_4", "to": "COMPLETE", "receipt_id": receipt_id})
        _log_baton("PHASE_4", "COMPLETE", receipt_id, {"input": arguments})
        _log_duckdb("deliver_disrupt", arguments)
        return _respond([types.TextContent(type="text", text=f"phase4_receipt: {receipt_id}")])

    if name == "query_journal":
        sql = arguments.get("sql", "")
        conn = duckdb.connect(DUCKDB_PATH)
        try:
            res = conn.execute(sql).fetchall()
            cols = [desc[0] for desc in conn.description]
            formatted = [dict(zip(cols, row)) for row in res]
            return _respond([types.TextContent(type="text", text=json.dumps(formatted, indent=2, default=str))])
        finally:
            conn.close()

    if name == "commit":
        if _last_receipt_type() != "phase4_receipt":
            return _respond([types.TextContent(type="text", text="Error: phase4_receipt required before commit.")])
        receipt_id = _append_receipt("commit_receipt", {"message": arguments.get("message", "")})
        _log_blackboard({"phase": "C", "action": "commit", "receipt_id": receipt_id, "input": arguments})
        _log_duckdb("commit", arguments)
        return _respond([types.TextContent(type="text", text=f"commit_receipt: {receipt_id}")])

    return _respond([types.TextContent(type="text", text=f"Unknown tool: {name}")])


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hfo-mcp-gateway-hub",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
