#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""SSOT front door facade (single blessed entryway).

Purpose
- Provide ONE command surface for memory operations so agents stop "free-styling".
- Enforce guidance-first guardrails: Doobidoo sqlite_vec is the only write SSOT.
- Treat Shodh as derived/on-demand; SSOT remains usable if Shodh is down.

Primary entrypoint
- Preferred: `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot ...`

This facade intentionally shells into existing, already-audited scripts using
`runpy.run_path` to avoid duplicating logic.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import runpy
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from hfo_memory_guardrails import (  # noqa: E402
    check_guardrails,
    format_entryways_text,
    format_guardrails_human,
    get_blessed_entryways,
)


def _run_script(rel_path: str, argv: list[str]) -> int:
    """Run an existing script as __main__ with argv, returning an exit code."""
    script_path = _REPO_ROOT / rel_path
    if not script_path.exists():
        print(f"[ssot] ERROR: missing script: {rel_path}")
        return 2

    old_argv = sys.argv
    try:
        sys.argv = [str(script_path)] + list(argv)
        runpy.run_path(str(script_path), run_name="__main__")
        return 0
    except SystemExit as e:
        code = e.code
        return int(code) if isinstance(code, int) else 0
    finally:
        sys.argv = old_argv


def _probe_shodh_health(
    *,
    shodh_url: str,
    timeout_sec: float,
    retries: int = 2,
    retry_backoff_sec: float = 1.0,
) -> tuple[bool, str]:
    try:
        import time

        import requests

        probe_timeout = float(timeout_sec)
        probe_timeout = max(5.0, min(30.0, probe_timeout))

        last_exc: Exception | None = None
        for attempt in range(max(0, int(retries)) + 1):
            try:
                resp = requests.get(
                    f"{shodh_url.rstrip('/')}/health",
                    timeout=probe_timeout,
                )
                if resp.status_code != 200:
                    return False, f"HTTP {resp.status_code}"
                data = None
                try:
                    data = json.loads(resp.text)
                except Exception:
                    data = None
                if isinstance(data, dict) and data.get("status") == "healthy":
                    return True, "healthy"
                return False, "unhealthy_or_unexpected_response"
            except Exception as e:
                last_exc = e
                if attempt >= int(retries):
                    break
                time.sleep(max(0.0, float(retry_backoff_sec)))

        return (
            False,
            f"{type(last_exc).__name__}: {last_exc}" if last_exc else "unknown",
        )
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def _ssot_stats() -> dict[str, Any]:
    sqlite_path = _ssot_sqlite_path()
    conn = sqlite3.connect(str(sqlite_path))
    row = conn.execute(
        "SELECT COUNT(*) as n, MAX(updated_at_iso) as max_u, MAX(created_at_iso) as max_c "
        "FROM memories WHERE deleted_at IS NULL"
    ).fetchone()
    return {
        "sqlite": str(sqlite_path),
        "rows_alive": int(row[0] or 0),
        "max_updated_at_iso": str(row[1]) if row[1] is not None else None,
        "max_created_at_iso": str(row[2]) if row[2] is not None else None,
    }


def _resolve_shodh_sync_state_path() -> Path:
    try:
        from hfo_pointers import resolve_path

        p = resolve_path("paths.shodh_sync_state_gen88_v4", default="")
        if p:
            return Path(p)
    except Exception:
        pass
    return _REPO_ROOT / "artifacts/shodh_memory/sync_state_doobidoo_gen88_v4.json"


def _mirror_status_payload() -> dict[str, Any]:
    ssot = _ssot_stats()
    sync_state_path = _resolve_shodh_sync_state_path()
    state = _load_json_file(sync_state_path)
    cursor = state.get("max_updated_at_iso") if isinstance(state, dict) else None
    full = (
        bool(cursor)
        and bool(ssot.get("max_updated_at_iso"))
        and str(cursor) == str(ssot.get("max_updated_at_iso"))
    )
    return {
        "ssot": ssot,
        "shodh": {
            "url": "http://127.0.0.1:3030",
            "health_ok": _probe_shodh_health(
                shodh_url="http://127.0.0.1:3030",
                timeout_sec=20,
                retries=1,
                retry_backoff_sec=1.0,
            )[0],
        },
        "sync_state": {
            "path": str(sync_state_path),
            "max_updated_at_iso": cursor,
            "last_run_at": state.get("last_run_at")
            if isinstance(state, dict)
            else None,
        },
        "mirror": {"fully_caught_up": full},
    }


def _shodh_recall_raw(
    *,
    query: str,
    limit: int,
    mode: str,
    user_id: str,
    timeout_sec: float,
) -> dict[str, Any]:
    import requests

    def _dotenv_get(key: str) -> str:
        p = _REPO_ROOT / ".env"
        if not p.exists():
            return ""
        try:
            for raw in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == key:
                    return v.strip().strip('"').strip("'")
        except Exception:
            return ""
        return ""

    api_key = (
        os.getenv("SHODH_API_KEY", "").strip()
        or os.getenv("SHODH_DEV_API_KEY", "").strip()
        or _dotenv_get("SHODH_API_KEY").strip()
        or _dotenv_get("SHODH_DEV_API_KEY").strip()
    )
    headers = {"X-API-Key": api_key} if api_key else {}

    resp = requests.post(
        "http://127.0.0.1:3030/api/recall",
        headers=headers,
        json={
            "user_id": user_id,
            "query": query,
            "limit": int(limit),
            "mode": mode,
        },
        timeout=max(1.0, float(timeout_sec)),
    )

    if resp.status_code in (401, 403) and not api_key:
        raise RuntimeError(
            "Shodh rejected the request (401/403). This Shodh server appears to require an API key; set SHODH_API_KEY (or SHODH_DEV_API_KEY) or reconfigure Shodh to allow unauthenticated local access."
        )
    resp.raise_for_status()
    obj = resp.json()
    return obj if isinstance(obj, dict) else {"raw": obj}


def _load_json_file(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _ssot_sqlite_path() -> Path:
    entryways = get_blessed_entryways(repo_root=_REPO_ROOT, environ=os.environ)
    p = (
        entryways.get("paths", {}).get("ssot_sqlite")
        if isinstance(entryways, dict)
        else None
    )
    if isinstance(p, str) and p:
        return Path(p)
    # Fallback to repo-relative default.
    return (
        _REPO_ROOT
        / "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"
    )


def _format_snippet(s: str, max_chars: int = 220) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:max_chars]


def _ssot_search(
    *,
    query: str,
    tag_like: str | None,
    memory_type: str | None,
    limit: int,
) -> dict[str, Any]:
    sqlite_path = _ssot_sqlite_path()
    con = sqlite3.connect(sqlite_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    where = ["deleted_at IS NULL", "content LIKE ?"]
    args: list[Any] = [f"%{query}%"]
    if tag_like:
        where.append("tags LIKE ?")
        args.append(f"%{tag_like}%")
    if memory_type:
        where.append("memory_type = ?")
        args.append(memory_type)

    q = f"""
    SELECT id, created_at_iso, memory_type, tags, metadata, substr(content,1,800) AS snippet
    FROM memories
    WHERE {" AND ".join(where)}
    ORDER BY id DESC
    LIMIT {int(max(1, limit))}
    """
    rows = cur.execute(q, args).fetchall()

    results: list[dict[str, Any]] = []
    for r in rows:
        src = None
        try:
            src = (
                json.loads(r["metadata"]).get("source_path") if r["metadata"] else None
            )
        except Exception:
            src = None
        results.append(
            {
                "id": r["id"],
                "created_at_iso": r["created_at_iso"],
                "memory_type": r["memory_type"],
                "source_path": src,
                "tags": r["tags"],
                "snippet": _format_snippet(r["snippet"] or ""),
            }
        )

    total = cur.execute(
        f"SELECT COUNT(*) FROM memories WHERE {' AND '.join(where)}",
        args,
    ).fetchone()[0]

    con.close()

    return {
        "sqlite": str(sqlite_path),
        "query": query,
        "tag_like": tag_like,
        "memory_type": memory_type,
        "total_matches": int(total),
        "returned": len(results),
        "results": results,
    }


def _guardrails_or_exit(*, allow_shodh_mcp: bool, json_out: bool) -> None:
    payload = check_guardrails(
        repo_root=_REPO_ROOT,
        allow_shodh_mcp=allow_shodh_mcp,
        environ=os.environ,
    )
    if payload.get("ok"):
        return

    # Guidance-first failure.
    if json_out:
        import json

        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(format_guardrails_human(payload))
    raise SystemExit(2)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="ssot",
        description="SSOT front door (Doobidoo sqlite_vec). Shodh is derived/on-demand.",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_entry = sub.add_parser("entryways", help="Print blessed entryways and exit")
    p_entry.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON"
    )

    p_guard = sub.add_parser(
        "guard", help="Fail-closed memory guardrails (non-destructive)"
    )
    p_guard.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON"
    )
    p_guard.add_argument(
        "--allow-shodh-mcp",
        action="store_true",
        help="Allow Shodh MCP adapter (normally blocked to reduce confusion)",
    )

    p_health = sub.add_parser(
        "health", help="Antifragile health check (SSOT + optional Shodh)"
    )
    p_health.add_argument("--json", action="store_true")
    p_health.add_argument("--ssot-only", action="store_true")
    p_health.add_argument("--deep-sqlite", action="store_true")

    sub.add_parser(
        "manifest", help="Generate memory storage manifest (snapshot + latest)"
    )

    p_ingest_md = sub.add_parser("ingest-md", help="Ingest markdown dir/path into SSOT")
    p_ingest_md.add_argument("--dir", help="Directory to scan recursively for .md")
    p_ingest_md.add_argument(
        "--path",
        action="append",
        help="Specific markdown file to ingest (repeatable)",
    )
    p_ingest_md.add_argument("--tags", nargs="*", default=[], help="Tags to apply")
    p_ingest_md.add_argument("--memory-type", default="doctrine")
    p_ingest_md.add_argument("--max-files", type=int, default=200)
    p_ingest_md.add_argument("--chunk-chars", type=int, default=12000)
    p_ingest_md.add_argument("--write", action="store_true")

    p_ingest_text = sub.add_parser(
        "ingest-text", help="Ingest a text dir into SSOT (bounded)"
    )
    p_ingest_text.add_argument("--dir", required=True)
    p_ingest_text.add_argument("--tags", nargs="*", default=[])
    p_ingest_text.add_argument("--memory-type", default="note")
    p_ingest_text.add_argument("--max-files", type=int, default=200)
    p_ingest_text.add_argument("--max-bytes", type=int, default=2_000_000)
    p_ingest_text.add_argument("--write", action="store_true")

    p_export = sub.add_parser("export", help="Export SSOT memories to JSONL")
    p_export.add_argument("--out", required=True)
    p_export.add_argument("--limit", type=int, default=0)

    p_import = sub.add_parser("import", help="Import JSONL into SSOT")
    p_import.add_argument("--in", dest="in_path", required=True)
    p_import.add_argument("--write", action="store_true")

    p_sync = sub.add_parser("sync-shodh", help="Sync SSOT -> Shodh derived view")
    p_sync.add_argument("--dry-run", action="store_true")
    p_sync.add_argument("--limit", type=int, default=0)
    p_sync.add_argument("--timeout-sec", type=int, default=30)
    p_sync.add_argument("--require-tag", action="append", default=[])
    p_sync.add_argument("--retries", type=int, default=1)
    p_sync.add_argument("--retry-backoff-sec", type=float, default=1.0)
    p_sync.add_argument("--sleep-ms", type=int, default=25)
    p_sync.add_argument("--max-content-chars", type=int, default=2000)

    p_recall = sub.add_parser("recall-shodh", help="Query Shodh derived view")
    p_recall.add_argument("--query", required=True)
    p_recall.add_argument("--limit", type=int, default=8)

    p_recall_auto = sub.add_parser(
        "recall",
        help="Unified recall API: auto-uses Shodh when healthy, otherwise falls back to SSOT search",
    )
    p_recall_auto.add_argument("--query", required=True)
    p_recall_auto.add_argument("--limit", type=int, default=8)
    p_recall_auto.add_argument(
        "--mode",
        default="auto",
        choices=["auto", "shodh", "fts", "like"],
        help="Recall backend: auto (default), shodh, fts, like",
    )

    p_mirror_status = sub.add_parser(
        "mirror-status",
        help="Report derived Shodh mirror cursor vs SSOT max_updated_at_iso",
    )
    p_mirror_status.add_argument("--json", action="store_true")

    p_mirror_catchup = sub.add_parser(
        "mirror-catchup",
        help="Catch up Shodh derived mirror from SSOT (time-bounded; resumable)",
    )
    p_mirror_catchup.add_argument("--timeout-sec", type=int, default=20)
    p_mirror_catchup.add_argument("--retries", type=int, default=1)
    p_mirror_catchup.add_argument("--retry-backoff-sec", type=float, default=1.0)
    p_mirror_catchup.add_argument("--sleep-ms", type=int, default=25)
    p_mirror_catchup.add_argument("--max-content-chars", type=int, default=2000)
    p_mirror_catchup.add_argument(
        "--max-runtime-sec",
        type=int,
        default=900,
        help="Max seconds to spend inside the sync run (default: 900)",
    )
    p_mirror_catchup.add_argument(
        "--proof-dir",
        default="",
        help="Optional proof directory (default: artifacts/proofs/shodh_mirror_catchup_<UTC>/)",
    )

    p_feedback = sub.add_parser(
        "feedback-from-shodh",
        help="Export Shodh recall ranking/score signals and (optionally) import into SSOT",
    )
    p_feedback.add_argument("--query", required=True)
    p_feedback.add_argument("--limit", type=int, default=20)
    p_feedback.add_argument(
        "--mode",
        default="hybrid",
        choices=["semantic", "associative", "hybrid"],
    )
    p_feedback.add_argument(
        "--user-id",
        default=os.getenv("SHODH_USER_ID", "hfo_gen88_v4"),
    )
    p_feedback.add_argument("--timeout-sec", type=float, default=60.0)
    p_feedback.add_argument(
        "--out",
        default="",
        help="Output JSONL path (default: artifacts/exports/shodh_feedback_<UTC>.jsonl)",
    )
    p_feedback.add_argument(
        "--write",
        action="store_true",
        help="Import the exported JSONL into SSOT (SSOT-only write path)",
    )

    p_search = sub.add_parser(
        "search",
        help="Search SSOT sqlite directly (works even if Shodh is down)",
    )
    p_search.add_argument("--query", required=True, help="Substring query (SQL LIKE)")
    p_search.add_argument(
        "--tag-like",
        default=None,
        help="Optional substring filter on tags (e.g. 'hive8' or 'medallion:silver')",
    )
    p_search.add_argument(
        "--memory-type",
        default=None,
        help="Optional exact memory_type filter",
    )
    p_search.add_argument("--limit", type=int, default=8)
    p_search.add_argument("--json", action="store_true")

    p_build_fts = sub.add_parser(
        "build-fts",
        help="Build a rebuildable FTS5 index over SSOT into a derived sqlite DB",
    )
    p_build_fts.add_argument(
        "--out",
        default=str(
            _REPO_ROOT
            / "artifacts/mcp_memory_service/gen88_v4/derived_indexes/ssot_fts_v1.sqlite"
        ),
        help="Output sqlite path for the derived FTS index",
    )
    p_build_fts.add_argument(
        "--limit",
        type=int,
        default=0,
        help="0 means no limit; otherwise index only first N SSOT rows",
    )
    p_build_fts.add_argument(
        "--rebuild",
        action="store_true",
        help="Delete and rebuild the derived FTS DB",
    )
    p_build_fts.add_argument(
        "--tokenize",
        default="unicode61",
        help="FTS5 tokenizer (default: unicode61)",
    )
    p_build_fts.add_argument("--json", action="store_true")

    p_search_fts = sub.add_parser(
        "search-fts",
        help="Search the derived FTS5 index (lexical; deterministic)",
    )
    p_search_fts.add_argument(
        "--db",
        default=str(
            _REPO_ROOT
            / "artifacts/mcp_memory_service/gen88_v4/derived_indexes/ssot_fts_v1.sqlite"
        ),
        help="Derived FTS sqlite path",
    )
    p_search_fts.add_argument("--query", required=True)
    p_search_fts.add_argument("--limit", type=int, default=8)
    p_search_fts.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)

    if args.cmd == "entryways":
        entryways = get_blessed_entryways(repo_root=_REPO_ROOT, environ=os.environ)
        if args.json:
            print(json.dumps(entryways, indent=2, ensure_ascii=False))
        else:
            print(format_entryways_text(entryways))
        return 0

    if args.cmd == "guard":
        payload = check_guardrails(
            repo_root=_REPO_ROOT,
            allow_shodh_mcp=bool(getattr(args, "allow_shodh_mcp", False)),
            environ=os.environ,
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(format_guardrails_human(payload))
        return 0 if payload.get("ok") else 2

    if args.cmd == "health":
        script_argv: list[str] = []
        if args.json:
            script_argv.append("--json")
        if args.ssot_only:
            script_argv.append("--ssot-only")
        if args.deep_sqlite:
            script_argv.append("--deep-sqlite")
        return _run_script("scripts/hfo_memory_healthcheck.py", script_argv)

    if args.cmd == "manifest":
        # Non-destructive snapshot.
        return _run_script("scripts/hfo_memory_storage_manifest.py", [])

    if args.cmd == "ingest-md":
        write = bool(args.write)
        if write:
            _guardrails_or_exit(allow_shodh_mcp=False, json_out=False)
        script_argv: list[str] = []
        if args.dir:
            script_argv += ["--dir", args.dir]
        if args.path:
            for p in args.path:
                script_argv += ["--path", p]
        script_argv += ["--max-files", str(int(args.max_files))]
        script_argv += ["--chunk-chars", str(int(args.chunk_chars))]
        if args.tags:
            script_argv += ["--tags"] + list(args.tags)
        if args.memory_type:
            script_argv += ["--memory-type", str(args.memory_type)]
        if write:
            script_argv.append("--write")
        else:
            script_argv.append("--dry-run")
        return _run_script("scripts/hfo_memory_ingest_markdown_dir.py", script_argv)

    if args.cmd == "ingest-text":
        write = bool(args.write)
        if write:
            _guardrails_or_exit(allow_shodh_mcp=False, json_out=False)
        script_argv: list[str] = [
            "--dir",
            args.dir,
            "--max-files",
            str(int(args.max_files)),
            "--max-bytes",
            str(int(args.max_bytes)),
        ]
        if args.tags:
            script_argv += ["--tags"] + list(args.tags)
        if args.memory_type:
            script_argv += ["--memory-type", str(args.memory_type)]
        if write:
            script_argv.append("--write")
        return _run_script("scripts/hfo_memory_ingest_text_dir.py", script_argv)

    if args.cmd == "export":
        # Read-only, but still benefits from guardrails alignment.
        _guardrails_or_exit(allow_shodh_mcp=False, json_out=False)
        return _run_script(
            "scripts/hfo_memory_export_doobidoo_ssot.py",
            ["--out", args.out, "--limit", str(int(args.limit))],
        )

    if args.cmd == "import":
        write = bool(args.write)
        if write:
            _guardrails_or_exit(allow_shodh_mcp=False, json_out=False)
        script_argv = ["--in", args.in_path]
        if write:
            script_argv.append("--write")
        return _run_script(
            "scripts/hfo_memory_import_jsonl_to_doobidoo.py", script_argv
        )

    if args.cmd == "sync-shodh":
        # Shodh is optional; do not hard-fail guardrails here.
        ok, detail = _probe_shodh_health(
            shodh_url="http://127.0.0.1:3030",
            timeout_sec=args.timeout_sec,
            retries=2,
            retry_backoff_sec=1.0,
        )
        if not ok:
            print(
                "ERROR: Shodh is not reachable. Start the 'Shodh Memory: Server (3030)' task (or check SHODH_HOST/SHODH_PORT) and retry."
            )
            print(f"ERROR: /health probe failed: {detail}")
            return 2
        script_argv: list[str] = [
            "--timeout-sec",
            str(int(args.timeout_sec)),
            "--retries",
            str(int(args.retries)),
            "--retry-backoff-sec",
            str(float(args.retry_backoff_sec)),
            "--sleep-ms",
            str(int(args.sleep_ms)),
            "--max-content-chars",
            str(int(args.max_content_chars)),
        ]
        if args.dry_run:
            script_argv.append("--dry-run")
        if args.limit:
            script_argv += ["--limit", str(int(args.limit))]
        for t in args.require_tag or []:
            script_argv += ["--require-tag", t]
        return _run_script("scripts/shodh_sync_from_doobidoo_ssot.py", script_argv)

    if args.cmd == "recall-shodh":
        ok, detail = _probe_shodh_health(
            shodh_url="http://127.0.0.1:3030",
            timeout_sec=20,
            retries=2,
            retry_backoff_sec=1.0,
        )
        if not ok:
            print(
                "ERROR: Shodh is not reachable. Start the 'Shodh Memory: Server (3030)' task and (optionally) run `hfo_hub.py ssot sync-shodh` first."
            )
            print(f"ERROR: /health probe failed: {detail}")
            return 2
        return _run_script(
            "scripts/hfo_shodh_recall.py",
            ["--query", args.query, "--limit", str(int(args.limit))],
        )

    if args.cmd == "recall":
        query = str(args.query)
        limit = int(args.limit)
        mode = str(args.mode)

        if mode in ("auto", "shodh"):
            ok, _detail = _probe_shodh_health(
                shodh_url="http://127.0.0.1:3030",
                timeout_sec=20,
                retries=2,
                retry_backoff_sec=1.0,
            )
            if ok:
                return _run_script(
                    "scripts/hfo_shodh_recall.py",
                    ["--query", query, "--limit", str(limit)],
                )
            if mode == "shodh":
                print(
                    "ERROR: Shodh recall requested but Shodh is not healthy/reachable. Try `hfo_hub.py ssot mirror-status` and/or start Shodh, then re-sync."
                )
                return 2

        # Derived lexical fallback (if present)
        if mode in ("auto", "fts"):
            fts_db = (
                _REPO_ROOT
                / "artifacts/mcp_memory_service/gen88_v4/derived_indexes/ssot_fts_v1.sqlite"
            )
            if fts_db.exists():
                return _run_script(
                    "scripts/hfo_ssot_fts.py",
                    [
                        "search",
                        "--db",
                        str(fts_db),
                        "--query",
                        query,
                        "--limit",
                        str(limit),
                    ],
                )
            if mode == "fts":
                print(
                    "ERROR: FTS recall requested but derived FTS DB is missing. Build it with `hfo_hub.py ssot build-fts --rebuild`."
                )
                return 2

        # SSOT LIKE fallback (always available)
        payload = _ssot_search(
            query=query, tag_like=None, memory_type=None, limit=limit
        )
        print(f"sqlite={payload['sqlite']}")
        print(
            f"total_matches={payload['total_matches']} returned={payload['returned']}"
        )
        for r in payload["results"]:
            print(
                f"- id={r['id']} type={r['memory_type']} created={r['created_at_iso']}"
            )
            if r.get("source_path"):
                print(f"  source_path={r['source_path']}")
            if r.get("tags"):
                print(f"  tags={str(r['tags'])[:220]}")
            print(f"  snippet={r['snippet']}")
        return 0

    if args.cmd == "mirror-status":
        payload = _mirror_status_payload()

        if bool(args.json):
            print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
            return 0

        print(f"ssot.sqlite={payload['ssot']['sqlite']}")
        print(f"ssot.rows_alive={payload['ssot']['rows_alive']}")
        print(f"ssot.max_updated_at_iso={payload['ssot']['max_updated_at_iso']}")
        print(f"shodh.health_ok={payload['shodh']['health_ok']}")
        print(f"sync_state.path={payload['sync_state']['path']}")
        print(
            f"sync_state.max_updated_at_iso={payload['sync_state']['max_updated_at_iso']}"
        )
        print(f"mirror.fully_caught_up={payload['mirror']['fully_caught_up']}")
        if not payload["mirror"]["fully_caught_up"]:
            print(
                "NOTE: Shodh is a derived mirror. To catch up, run a larger SSOT→Shodh sync (e.g. phoenix regen with --limit 0) and monitor for timeouts."
            )
        return 0

    if args.cmd == "mirror-catchup":
        ok, detail = _probe_shodh_health(
            shodh_url="http://127.0.0.1:3030",
            timeout_sec=args.timeout_sec,
            retries=2,
            retry_backoff_sec=1.0,
        )
        if not ok:
            print(
                "ERROR: Shodh is not reachable. Start the 'Shodh Memory: Server (3030)' task and retry."
            )
            print(f"ERROR: /health probe failed: {detail}")
            return 2

        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        proof_dir = (
            Path(args.proof_dir)
            if str(args.proof_dir).strip()
            else (_REPO_ROOT / f"artifacts/proofs/shodh_mirror_catchup_{ts}")
        )
        proof_dir.mkdir(parents=True, exist_ok=True)

        pre = _mirror_status_payload()
        (proof_dir / "mirror_status_before.json").write_text(
            json.dumps(pre, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        script_argv: list[str] = [
            "--timeout-sec",
            str(int(args.timeout_sec)),
            "--retries",
            str(int(args.retries)),
            "--retry-backoff-sec",
            str(float(args.retry_backoff_sec)),
            "--sleep-ms",
            str(int(args.sleep_ms)),
            "--max-content-chars",
            str(int(args.max_content_chars)),
            "--max-runtime-sec",
            str(int(args.max_runtime_sec)),
            "--limit",
            "0",
        ]
        rc = _run_script("scripts/shodh_sync_from_doobidoo_ssot.py", script_argv)

        post = _mirror_status_payload()
        (proof_dir / "mirror_status_after.json").write_text(
            json.dumps(post, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        print(f"proof_dir={proof_dir}")
        print(f"sync_exit_code={rc}")
        print(f"mirror.fully_caught_up={post['mirror']['fully_caught_up']}")
        print(
            f"sync_state.max_updated_at_iso={post['sync_state']['max_updated_at_iso']}"
        )
        print(f"ssot.max_updated_at_iso={post['ssot']['max_updated_at_iso']}")
        return 0 if rc == 0 else rc

    if args.cmd == "feedback-from-shodh":
        ok, detail = _probe_shodh_health(
            shodh_url="http://127.0.0.1:3030",
            timeout_sec=20,
            retries=2,
            retry_backoff_sec=1.0,
        )
        if not ok:
            print(
                "ERROR: Shodh is not reachable. Start the 'Shodh Memory: Server (3030)' task and retry."
            )
            print(f"ERROR: /health probe failed: {detail}")
            return 2

        ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        out_path = (
            Path(args.out)
            if str(args.out).strip()
            else (_REPO_ROOT / f"artifacts/exports/shodh_feedback_{ts}.jsonl")
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)

        raw = _shodh_recall_raw(
            query=str(args.query),
            limit=int(args.limit),
            mode=str(args.mode),
            user_id=str(args.user_id),
            timeout_sec=float(args.timeout_sec),
        )

        memories = raw.get("memories", []) if isinstance(raw, dict) else []
        written = 0
        with out_path.open("w", encoding="utf-8") as f:
            for rank, mem in enumerate(memories, start=1):
                exp = mem.get("experience") if isinstance(mem, dict) else None
                content = (exp.get("content") if isinstance(exp, dict) else None) or ""

                # Attempt to recover doobidoo content_hash from the derived header.
                content_hash = None
                try:
                    lines = str(content).splitlines()
                    if len(lines) >= 2 and lines[0].strip() == "[HFO_DERIVED_VIEW]":
                        header = json.loads(lines[1])
                        if isinstance(header, dict):
                            content_hash = header.get("content_hash")
                except Exception:
                    content_hash = None

                score = mem.get("score") if isinstance(mem, dict) else None
                external_id = mem.get("external_id") if isinstance(mem, dict) else None
                feedback_obj = {
                    "content": json.dumps(
                        {
                            "type": "shodh_feedback_signal_v1",
                            "query": str(args.query),
                            "mode": str(args.mode),
                            "rank": rank,
                            "score": score,
                            "external_id": external_id,
                            "content_hash": content_hash,
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    "content_hash": f"shodh_feedback:{ts}:{rank}:{content_hash or external_id or 'unknown'}",
                    "tags": ["ssot", "feedback", "derived_shodh", "gen88_v4"],
                    "memory_type": "shodh_feedback",
                    "metadata": {
                        "source": "shodh",
                        "shodh_url": "http://127.0.0.1:3030",
                        "query": str(args.query),
                        "rank": rank,
                    },
                }
                f.write(json.dumps(feedback_obj, ensure_ascii=False) + "\n")
                written += 1

        print(f"exported={written} out={out_path}")

        if bool(args.write):
            _guardrails_or_exit(allow_shodh_mcp=False, json_out=False)
            return _run_script(
                "scripts/hfo_memory_import_jsonl_to_doobidoo.py",
                ["--in", str(out_path), "--write"],
            )

        return 0

    if args.cmd == "search":
        import json as json_mod

        payload = _ssot_search(
            query=str(args.query),
            tag_like=str(args.tag_like) if args.tag_like else None,
            memory_type=str(args.memory_type) if args.memory_type else None,
            limit=int(args.limit),
        )
        if args.json:
            print(json_mod.dumps(payload, indent=2, ensure_ascii=False))
            return 0
        print(f"sqlite={payload['sqlite']}")
        print(
            f"total_matches={payload['total_matches']} returned={payload['returned']}"
        )
        for r in payload["results"]:
            print(
                f"- id={r['id']} type={r['memory_type']} created={r['created_at_iso']}"
            )
            if r.get("source_path"):
                print(f"  source_path={r['source_path']}")
            if r.get("tags"):
                print(f"  tags={str(r['tags'])[:220]}")
            print(f"  snippet={r['snippet']}")
        return 0

    if args.cmd == "build-fts":
        # Derived write is allowed; still enforce guardrails alignment.
        _guardrails_or_exit(allow_shodh_mcp=False, json_out=False)
        script_argv: list[str] = [
            "build",
            "--out",
            str(args.out),
            "--limit",
            str(int(args.limit)),
            "--tokenize",
            str(args.tokenize),
        ]
        if args.rebuild:
            script_argv.append("--rebuild")
        if args.json:
            script_argv.append("--json")
        return _run_script("scripts/hfo_ssot_fts.py", script_argv)

    if args.cmd == "search-fts":
        script_argv = [
            "search",
            "--db",
            str(args.db),
            "--query",
            str(args.query),
            "--limit",
            str(int(args.limit)),
        ]
        if args.json:
            script_argv.append("--json")
        return _run_script("scripts/hfo_ssot_fts.py", script_argv)

    print(f"[ssot] ERROR: unknown cmd: {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
