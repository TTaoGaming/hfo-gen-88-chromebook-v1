#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Derived FTS5 index for Doobidoo SSOT (rebuildable).

Design
- Keep the Doobidoo sqlite_vec SSOT schema stable.
- Build a separate, derived SQLite DB containing an FTS5 virtual table.
- Treat this index as disposable: delete and rebuild from SSOT.

Why this exists
- Agents get confused when there are many ways to search.
- This provides a deterministic lexical search surface (FTS) while keeping the
  SSOT as the only canonical write target.

Usage (via SSOT front door)
- Build:  hfo_hub.py ssot build-fts --limit 0 --rebuild
- Query:  hfo_hub.py ssot search-fts --query "hive8" --limit 8
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

_REPO_ROOT = Path(__file__).resolve().parents[1]

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from hfo_memory_guardrails import (  # noqa: E402
    enforce_ssot_write_target_or_exit,
    get_blessed_entryways,
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_ssot_sqlite_path() -> Path:
    entryways = get_blessed_entryways(repo_root=_REPO_ROOT, environ=os.environ)
    p = (
        entryways.get("paths", {}).get("ssot_sqlite")
        if isinstance(entryways, dict)
        else None
    )
    if isinstance(p, str) and p:
        ssot = Path(p)
    else:
        ssot = (
            _REPO_ROOT
            / "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"
        )

    # Validate against pointer-blessed SSOT (fail-closed).
    enforce_ssot_write_target_or_exit(repo_root=_REPO_ROOT, sqlite_path=str(ssot))
    return ssot


def _default_out_path() -> Path:
    return (
        _REPO_ROOT
        / "artifacts/mcp_memory_service/gen88_v4/derived_indexes/ssot_fts_v1.sqlite"
    )


def _ensure_parent_dir(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def _connect(path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(path))
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA synchronous=NORMAL;")
    return con


def _create_schema(con: sqlite3.Connection, *, tokenize: str) -> None:
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );
        """
    )

    # FTS5 table. Keep most fields indexed except explicitly UNINDEXED fields.
    # We use rowid == ssot_id for stable mapping back to SSOT.
    con.execute(
        f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts
        USING fts5(
          content,
          tags,
          memory_type,
          content_hash UNINDEXED,
          source_path UNINDEXED,
          tokenize='{tokenize}'
        );
        """
    )


def _iter_ssot_rows(
    ssot_con: sqlite3.Connection, *, limit: int
) -> Iterable[sqlite3.Row]:
    ssot_con.row_factory = sqlite3.Row
    cur = ssot_con.cursor()

    lim = "" if int(limit) <= 0 else f"LIMIT {int(limit)}"
    q = f"""
    SELECT id, content, tags, memory_type, content_hash, metadata
    FROM memories
    WHERE deleted_at IS NULL
    ORDER BY id ASC
    {lim}
    """
    for row in cur.execute(q):
        yield row


def _extract_source_path(metadata_text: str | None) -> str | None:
    if not metadata_text:
        return None
    try:
        obj = json.loads(metadata_text)
        if isinstance(obj, dict):
            v = obj.get("source_path")
            return str(v) if isinstance(v, str) and v else None
    except Exception:
        return None
    return None


def build_fts(
    *, out_path: Path, limit: int, rebuild: bool, tokenize: str
) -> dict[str, Any]:
    ssot_path = _resolve_ssot_sqlite_path()

    if rebuild and out_path.exists():
        out_path.unlink()

    _ensure_parent_dir(out_path)

    ssot_con = sqlite3.connect(str(ssot_path))
    out_con = _connect(out_path)

    try:
        _create_schema(out_con, tokenize=tokenize)

        # Fail fast if FTS5 isn't available.
        try:
            out_con.execute("SELECT count(*) FROM memories_fts")
        except sqlite3.OperationalError as e:
            raise SystemExit(
                "FTS5 is not available in this Python/SQLite build. "
                "On many Linux distros it is available by default. "
                f"Underlying error: {e}"
            )

        out_con.execute("BEGIN")

        inserted = 0
        for r in _iter_ssot_rows(ssot_con, limit=limit):
            ssot_id = int(r["id"])
            content = r["content"] or ""
            tags = r["tags"] or ""
            memory_type = r["memory_type"] or ""
            content_hash = r["content_hash"] or ""
            source_path = _extract_source_path(r["metadata"]) or ""

            out_con.execute(
                """
                INSERT OR REPLACE INTO memories_fts(
                  rowid, content, tags, memory_type, content_hash, source_path
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (ssot_id, content, tags, memory_type, content_hash, source_path),
            )
            inserted += 1

        out_con.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
            ("built_at", _utc_now_iso()),
        )
        out_con.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
            ("ssot_sqlite", str(ssot_path)),
        )
        out_con.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
            ("rows_indexed", str(int(inserted))),
        )
        out_con.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES(?, ?)",
            ("tokenize", str(tokenize)),
        )

        out_con.execute("COMMIT")

        return {
            "ok": True,
            "ssot_sqlite": str(ssot_path),
            "fts_sqlite": str(out_path),
            "rows_indexed": int(inserted),
            "built_at": _utc_now_iso(),
        }
    finally:
        try:
            ssot_con.close()
        except Exception:
            pass
        try:
            out_con.close()
        except Exception:
            pass


def search_fts(*, db_path: Path, query: str, limit: int) -> dict[str, Any]:
    if not db_path.exists():
        raise SystemExit(
            f"FTS DB not found: {db_path}. Run `hfo_hub.py ssot build-fts --rebuild` first."
        )

    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row

    try:
        cur = con.cursor()

        rows = cur.execute(
            """
            SELECT
              rowid AS ssot_id,
              memory_type,
              tags,
              content_hash,
              source_path,
              snippet(memories_fts, 0, '[', ']', '…', 12) AS snippet,
              bm25(memories_fts) AS score
            FROM memories_fts
            WHERE memories_fts MATCH ?
            ORDER BY score
            LIMIT ?
            """,
            (query, int(max(1, limit))),
        ).fetchall()

        results: list[dict[str, Any]] = []
        for r in rows:
            results.append(
                {
                    "ssot_id": int(r["ssot_id"]),
                    "score": float(r["score"]) if r["score"] is not None else None,
                    "memory_type": r["memory_type"],
                    "tags": r["tags"],
                    "content_hash": r["content_hash"],
                    "source_path": r["source_path"],
                    "snippet": r["snippet"],
                }
            )

        return {
            "ok": True,
            "fts_sqlite": str(db_path),
            "query": query,
            "returned": len(results),
            "results": results,
        }
    finally:
        con.close()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Derived FTS5 index for Doobidoo SSOT")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="Build/rebuild derived FTS5 DB from SSOT")
    p_build.add_argument("--out", default=str(_default_out_path()))
    p_build.add_argument(
        "--limit",
        type=int,
        default=0,
        help="0 means no limit; otherwise index only first N SSOT rows",
    )
    p_build.add_argument("--rebuild", action="store_true")
    p_build.add_argument(
        "--tokenize",
        default="unicode61",
        help="FTS5 tokenizer (default: unicode61)",
    )
    p_build.add_argument("--json", action="store_true")

    p_search = sub.add_parser("search", help="Query the derived FTS5 DB")
    p_search.add_argument("--db", default=str(_default_out_path()))
    p_search.add_argument("--query", required=True)
    p_search.add_argument("--limit", type=int, default=8)
    p_search.add_argument("--json", action="store_true")

    args = ap.parse_args(argv)

    if args.cmd == "build":
        payload = build_fts(
            out_path=Path(args.out),
            limit=int(args.limit),
            rebuild=bool(args.rebuild),
            tokenize=str(args.tokenize),
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"ok={payload['ok']}")
            print(f"ssot={payload['ssot_sqlite']}")
            print(f"fts_db={payload['fts_sqlite']}")
            print(f"rows_indexed={payload['rows_indexed']}")
        return 0

    if args.cmd == "search":
        payload = search_fts(
            db_path=Path(args.db),
            query=str(args.query),
            limit=int(args.limit),
        )
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 0
        print(f"fts_db={payload['fts_sqlite']}")
        print(f"returned={payload['returned']}")
        for r in payload["results"]:
            print(
                f"- ssot_id={r['ssot_id']} score={r['score']} type={r['memory_type']}"
            )
            if r.get("source_path"):
                print(f"  source_path={r['source_path']}")
            if r.get("tags"):
                print(f"  tags={str(r['tags'])[:220]}")
            print(f"  snippet={r['snippet']}")
        return 0

    print(f"ERROR: unknown cmd: {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
