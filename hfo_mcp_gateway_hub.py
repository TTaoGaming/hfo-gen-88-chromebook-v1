#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""
HFO MCP Gateway Hub (Single Entry Path)
- Enforces receipt chain: think_receipt -> p5_audit_receipt -> commit_receipt
- Logs to blackboard and DuckDB mission journal
"""

import os
import sys
import json
import datetime
import hashlib
import subprocess
import re
import urllib.request
import urllib.error
import urllib.parse
import shutil
import xml.etree.ElementTree as ET
import duckdb
import mcp.server.stdio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.types as types

BASE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
BLACKBOARD_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl")
DUCKDB_PATH = os.path.join(BASE_PATH, "hfo_gen_88_cb_v2/hfo_unified_v88.duckdb")
FILE_INDEX_DB_PATH = os.path.join(BASE_PATH, "hfo_unified_v88_merged.duckdb")
RECEIPTS_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/3_resources/receipts/hfo_mcp_gateway_receipts.jsonl")
BATON_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/3_resources/receipts/hfo_mcp_gateway_baton.jsonl")
MCP_MEMORY_PATH = os.path.join(BASE_PATH, "hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl")
SERENA_MEMORY_DIR = os.path.join(BASE_PATH, ".serena/memories")

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
    with open(RECEIPTS_PATH, "r") as f:
        lines = [line for line in f.read().splitlines() if line.strip()]
    if not lines:
        return None
    try:
        return json.loads(lines[-1]).get("type")
    except json.JSONDecodeError:
        return None


def _log_blackboard(entry: dict) -> None:
    try:
        entry.setdefault("timestamp", _now_iso())
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
    if not os.path.exists(path):
        return []
    limit = max(1, min(limit, 2000))
    with open(path, "r") as f:
        lines = [line for line in f.read().splitlines() if line.strip()]
    tail = lines[-limit:]
    parsed = []
    for line in tail:
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            parsed.append({"parse_error": True, "raw": line})
    return parsed


def _append_jsonl(path: str, entry: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(entry) + "\n")


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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mission_journal (
                id INTEGER PRIMARY KEY,
                actor_id VARCHAR,
                event_type VARCHAR,
                payload VARCHAR,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE SEQUENCE IF NOT EXISTS mission_journal_id_seq")
        conn.execute(
            "INSERT INTO mission_journal (id, actor_id, event_type, payload) VALUES (nextval('mission_journal_id_seq'), ?, ?, ?)",
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
            pass


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
