#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Import JSONL memories into the doobidoo sqlite SSOT.

This complements scripts/hfo_memory_export_doobidoo_ssot.py.

Notes:
- Import is idempotent due to `memories.content_hash` UNIQUE constraint.
- Tags/metadata are stored as TEXT in sqlite; the mcp_memory_service backend
  accepts Python types and will serialize.

Example:
  bash scripts/mcp_env_wrap.sh ./.venv/bin/python \
    scripts/hfo_memory_import_jsonl_to_doobidoo.py \
      --in artifacts/exports/doobidoo_export.jsonl

Dry-run (default) only counts what would be imported:
  ... --dry-run

Actually write:
  ... --write
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from mcp_memory_service.models.memory import Memory
from mcp_memory_service.storage.factory import create_storage_instance

from hfo_memory_guardrails import enforce_ssot_or_exit
from hfo_pointers import resolve_path


def _resolve_sqlite_path(repo_root: Path) -> str:
    sqlite_path = os.environ.get("MCP_MEMORY_SQLITE_PATH")
    if sqlite_path:
        return sqlite_path
    return resolve_path(
        dotted_key="paths.mcp_memory_ssot_sqlite",
        env_var="MCP_MEMORY_SQLITE_PATH",
        default=str(
            repo_root
            / "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"
        ),
    )


def _coerce_tags(tags_field) -> list[str]:
    if tags_field is None:
        return []
    if isinstance(tags_field, list):
        return [str(x) for x in tags_field]
    if isinstance(tags_field, str):
        s = tags_field.strip()
        if not s:
            return []
        # Try JSON first.
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return [str(x) for x in parsed]
        except Exception:
            pass
        # Fallback: comma-separated
        return [t.strip() for t in s.split(",") if t.strip()]
    return [str(tags_field)]


def _coerce_metadata(meta_field) -> dict:
    if meta_field is None:
        return {}
    if isinstance(meta_field, dict):
        return meta_field
    if isinstance(meta_field, str):
        s = meta_field.strip()
        if not s:
            return {}
        try:
            parsed = json.loads(s)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return {"raw": s}
    return {"raw": str(meta_field)}


async def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import JSONL memories into doobidoo sqlite SSOT."
    )
    parser.add_argument("--in", dest="in_path", required=True, help="Input JSONL path")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Dry-run (default): do not write, only report counts",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Actually write into SSOT (disables dry-run)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max lines to read (0 means no limit)",
    )

    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    if args.write:
        enforce_ssot_or_exit(repo_root=repo_root)
    sqlite_path = _resolve_sqlite_path(repo_root)

    in_path = (
        (repo_root / args.in_path).resolve()
        if not Path(args.in_path).is_absolute()
        else Path(args.in_path).resolve()
    )
    if not in_path.exists():
        raise SystemExit(f"--in does not exist: {in_path}")

    dry_run = bool(args.dry_run and not args.write)

    storage = await create_storage_instance(sqlite_path=sqlite_path, server_type="mcp")

    read_n = 0
    stored_n = 0
    skipped_n = 0

    with in_path.open("r", encoding="utf-8") as f:
        for line in f:
            if int(args.limit) > 0 and read_n >= int(args.limit):
                break

            line = line.strip()
            if not line:
                continue

            read_n += 1
            obj = json.loads(line)

            mem = Memory(
                content=str(obj.get("content") or ""),
                content_hash=str(obj.get("content_hash") or ""),
                tags=_coerce_tags(obj.get("tags")),
                memory_type=str(obj.get("memory_type") or "file"),
                metadata=_coerce_metadata(obj.get("metadata")),
            )

            if not mem.content or not mem.content_hash:
                skipped_n += 1
                continue

            if dry_run:
                skipped_n += 1
                continue

            ok, _msg = await storage.store(mem)
            if ok:
                stored_n += 1
            else:
                skipped_n += 1

    mode = "DRY_RUN" if dry_run else "WRITE"
    print(
        f"[import] mode={mode} in={in_path} read={read_n} stored={stored_n} skipped={skipped_n}"
    )
    print(f"[import] sqlite={sqlite_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
