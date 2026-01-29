#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Export doobidoo sqlite SSOT memories to JSONL.

Purpose:
- Make SSOT portable between machines without trying to merge sqlite files.
- Provide a simple bridge for bulk copying from "desktop SSOT" -> "Chromebook SSOT".

Each line is a JSON object with fields needed to re-import.

Example:
  bash scripts/mcp_env_wrap.sh ./.venv/bin/python \
    scripts/hfo_memory_export_doobidoo_ssot.py \
      --out artifacts/exports/doobidoo_export.jsonl \
      --limit 1000

Then copy the JSONL to another machine and import.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from hfo_pointers import resolve_path


def _resolve_sqlite_path(repo_root: Path) -> str:
    sqlite_path = os.environ.get("MCP_MEMORY_SQLITE_PATH")
    if sqlite_path:
        return sqlite_path
    return resolve_path(
        dotted_key="paths.mcp_memory_ssot_sqlite",
        env_var="MCP_MEMORY_SQLITE_PATH",
        default=str(repo_root / "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Export doobidoo sqlite SSOT memories to JSONL.")
    parser.add_argument(
        "--out",
        required=True,
        help="Output JSONL path",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max rows to export (0 means no limit)",
    )

    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    sqlite_path = _resolve_sqlite_path(repo_root)

    out_path = (repo_root / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(sqlite_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    sql = "SELECT id, content_hash, content, tags, memory_type, metadata, created_at, created_at_iso FROM memories WHERE deleted_at IS NULL ORDER BY id ASC"
    if int(args.limit) > 0:
        sql += " LIMIT ?"
        cur.execute(sql, (int(args.limit),))
    else:
        cur.execute(sql)

    n = 0
    with out_path.open("w", encoding="utf-8") as f:
        for row in cur:
            obj = dict(row)
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            n += 1

    print(f"[export] sqlite={sqlite_path}")
    print(f"[export] out={out_path}")
    print(f"[export] rows={n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
