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


def _probe_shodh_health(*, shodh_url: str, timeout_sec: float) -> tuple[bool, str]:
    try:
        import requests

        resp = requests.get(
            f"{shodh_url.rstrip('/')}/health",
            timeout=max(0.5, float(timeout_sec)),
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
        return False, f"{type(e).__name__}: {e}"


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

    p_recall = sub.add_parser("recall-shodh", help="Query Shodh derived view")
    p_recall.add_argument("--query", required=True)
    p_recall.add_argument("--limit", type=int, default=8)

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
            import json

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
            import json

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
            shodh_url="http://127.0.0.1:3030", timeout_sec=args.timeout_sec
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
            shodh_url="http://127.0.0.1:3030", timeout_sec=10
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
