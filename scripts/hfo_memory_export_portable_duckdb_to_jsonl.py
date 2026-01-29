#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Export a portable HFO DuckDB memory bank into JSONL for SSOT import.

This is intended to bridge a portable DuckDB corpus (e.g. pre-HFO → Gen84)
into the Gen88 v4 blessed SSOT write-path (doobidoo sqlite_vec).

Pipeline:
  1) Export DuckDB `artifacts` table → JSONL (this script)
  2) Import JSONL → SSOT sqlite_vec:
       scripts/hfo_memory_import_jsonl_to_doobidoo.py
  3) Rebuild derived Shodh view:
       scripts/shodh_sync_from_doobidoo_ssot.py

Safety:
- Default is dry-run (no output file written).
- Output JSONL format matches scripts/hfo_memory_import_jsonl_to_doobidoo.py:
    {content, content_hash, tags, memory_type, metadata}

Example (sample):
  bash scripts/mcp_env_wrap.sh ./.venv/bin/python \
    scripts/hfo_memory_export_portable_duckdb_to_jsonl.py \
            --db hfo_hot_obsidian/bronze/3_resources/ingest_sources/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52/hfo_memory.duckdb \
      --out artifacts/exports/portable_pre_hfo_to_gen84_sample.jsonl \
      --limit 50 \
      --tags gen88_v4 ssot source:portable epoch:pre_hfo_to_gen84 \
      --write

Then import the sample:
  bash scripts/mcp_env_wrap.sh ./.venv/bin/python \
    scripts/hfo_memory_import_jsonl_to_doobidoo.py \
      --in artifacts/exports/portable_pre_hfo_to_gen84_sample.jsonl \
      --write
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import duckdb

_REPO_ROOT = Path(__file__).resolve().parents[1]


def _repo_root() -> Path:
    return _REPO_ROOT


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _tags_for_row(
    *, base_tags: list[str], era: str | None, generation: int | None
) -> list[str]:
    tags = list(base_tags)
    if era:
        tags.append(f"era:{era}")
    if generation is not None:
        tags.append(f"gen:{generation}")
    # de-dupe while preserving order
    return list(dict.fromkeys([t for t in tags if str(t).strip()]))


def main() -> int:
    p = argparse.ArgumentParser(
        description="Export portable DuckDB artifacts → JSONL for SSOT import"
    )
    p.add_argument(
        "--db",
        required=True,
        help="Path to portable DuckDB (must contain table `artifacts`)",
    )
    p.add_argument(
        "--out",
        default="",
        help="Output JSONL path (required with --write)",
    )
    p.add_argument(
        "--tags",
        nargs="*",
        default=["gen88_v4", "ssot", "source:portable"],
        help="Base tags applied to every exported memory",
    )
    p.add_argument(
        "--memory-type",
        default="portable_artifact",
        help="Memory type label stored alongside the memory",
    )
    p.add_argument(
        "--where",
        default="",
        help="Optional SQL WHERE clause (without the 'WHERE' keyword)",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max rows to export (0 means no limit)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Dry-run (default): do not write, only report counts",
    )
    p.add_argument(
        "--write",
        action="store_true",
        help="Actually write the JSONL output file (disables dry-run)",
    )

    args = p.parse_args()

    repo_root = _repo_root()

    db_path = (
        (repo_root / args.db).resolve()
        if not Path(args.db).is_absolute()
        else Path(args.db).resolve()
    )
    if not db_path.exists():
        raise SystemExit(f"--db does not exist: {db_path}")

    dry_run = bool(args.dry_run and not args.write)

    out_path: Path | None = None
    if not dry_run:
        if not args.out:
            raise SystemExit("--out is required when using --write")
        out_path = (
            (repo_root / args.out).resolve()
            if not Path(args.out).is_absolute()
            else Path(args.out).resolve()
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(db_path), read_only=True)

    where_clause = f"WHERE {args.where}" if str(args.where).strip() else ""
    limit_clause = f"LIMIT {int(args.limit)}" if int(args.limit) > 0 else ""

    # Explicit column list (stable ordering) to match README schema.
    query = f"""
        SELECT id, era, generation, filename, path, content, content_hash, modified, char_count, created_at
        FROM artifacts
        {where_clause}
        ORDER BY created_at
        {limit_clause}
    """.strip()

    cur = con.execute(query)

    total = 0
    total_chars = 0

    f = None
    if out_path is not None:
        f = out_path.open("w", encoding="utf-8")

    try:
        while True:
            rows = cur.fetchmany(250)
            if not rows:
                break

            for (
                artifact_id,
                era,
                generation,
                filename,
                path,
                content,
                content_hash,
                modified,
                char_count,
                created_at,
            ) in rows:
                total += 1
                total_chars += int(char_count or 0)

                if dry_run:
                    continue

                obj = {
                    "content": _coerce_str(content),
                    "content_hash": _coerce_str(content_hash)
                    or _coerce_str(artifact_id),
                    "tags": _tags_for_row(
                        base_tags=list(args.tags),
                        era=_coerce_str(era) or None,
                        generation=int(generation) if generation is not None else None,
                    ),
                    "memory_type": _coerce_str(args.memory_type) or "portable_artifact",
                    "metadata": {
                        "source_type": "portable_duckdb",
                        "source_path": str(db_path),
                        "artifact_id": _coerce_str(artifact_id),
                        "era": _coerce_str(era) or None,
                        "generation": int(generation)
                        if generation is not None
                        else None,
                        "filename": _coerce_str(filename) or None,
                        "path": _coerce_str(path) or None,
                        "modified": _coerce_str(modified) or None,
                        "char_count": int(char_count)
                        if char_count is not None
                        else None,
                        "created_at": _coerce_str(created_at) or None,
                    },
                }

                assert f is not None
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    finally:
        if f is not None:
            f.close()
        con.close()

    mode = "DRY_RUN" if dry_run else "WRITE"
    approx_mb = total_chars / 1024 / 1024
    print(
        f"[portable_export] mode={mode} db={db_path} rows={total} approx_content_mb={approx_mb:.1f}"
    )
    if out_path is not None:
        try:
            size_mb = out_path.stat().st_size / 1024 / 1024
            print(f"[portable_export] out={out_path} size_mb={size_mb:.1f}")
        except OSError:
            print(f"[portable_export] out={out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
