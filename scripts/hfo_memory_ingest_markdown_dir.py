#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Ingest markdown files into the Gen88 v4 blessed memory SSOT.

This is an *offline ingestion helper* that writes directly to the sqlite_vec SSOT
(using mcp_memory_service's storage backend) so agents can bulk-load key docs.

Safety:
- Default is dry-run.
- Uses pointer-resolved SSOT path (or env MCP_MEMORY_SQLITE_PATH override).
- Never touches legacy JSONL memory sinks.

Example:
  bash scripts/mcp_env_wrap.sh ./.venv/bin/python \
    scripts/hfo_memory_ingest_markdown_dir.py \
      --dir hfo_hot_obsidian/bronze/3_resources/para/areas/sensemaking/s3_protocol_turns \
      --tags gen88_v4 ssot topic:s3
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Iterable

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from mcp_memory_service.models.memory import Memory
from mcp_memory_service.storage.factory import create_storage_instance
from mcp_memory_service.utils.hashing import generate_content_hash

from hfo_memory_guardrails import enforce_ssot_or_exit
from hfo_pointers import resolve_path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _iter_markdown_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.md")):
        if path.is_file():
            yield path


def _chunk_text(text: str, chunk_chars: int) -> list[str]:
    if chunk_chars <= 0:
        return [text]
    if len(text) <= chunk_chars:
        return [text]
    return [text[i : i + chunk_chars] for i in range(0, len(text), chunk_chars)]


async def _ingest_one_file(
    storage,
    *,
    file_path: Path,
    repo_root: Path,
    base_tags: list[str],
    memory_type: str,
    dry_run: bool,
    chunk_chars: int,
) -> tuple[int, int]:
    rel = str(file_path.resolve().relative_to(repo_root))
    raw = file_path.read_text(encoding="utf-8", errors="replace")

    # Include provenance for retrieval context without rewriting the source file.
    header = f"[source:file:{rel}]\n"
    content = header + raw

    chunks = _chunk_text(content, chunk_chars)

    stored = 0
    skipped = 0

    if len(chunks) == 1:
        content_hash = generate_content_hash(content)
        tags = list(dict.fromkeys([*base_tags, f"source:file:{rel}"]))
        mem = Memory(
            content=content,
            content_hash=content_hash,
            tags=tags,
            memory_type=memory_type,
            metadata={
                "source_type": "file",
                "source_path": rel,
                "chunked": False,
            },
        )

        if dry_run:
            return (0, 1)

        ok, msg = await storage.store(mem)
        if not ok and msg:
            print(f"[ingest] skipped file={rel} reason={msg}")
        return (1, 0) if ok else (0, 1)

    # Chunked
    parent_hash = generate_content_hash(content)
    for idx, chunk in enumerate(chunks):
        chunk_hash = generate_content_hash(chunk)
        tags = list(
            dict.fromkeys(
                [
                    *base_tags,
                    f"source:file:{rel}",
                    f"chunk_of:{parent_hash}",
                    "chunked",
                ]
            )
        )
        mem = Memory(
            content=chunk,
            content_hash=chunk_hash,
            tags=tags,
            memory_type=memory_type,
            metadata={
                "source_type": "file",
                "source_path": rel,
                "chunked": True,
                "chunk_parent": parent_hash,
                "chunk_index": idx,
                "chunk_count": len(chunks),
            },
        )

        if dry_run:
            skipped += 1
            continue

        ok, msg = await storage.store(mem)
        if ok:
            stored += 1
        else:
            skipped += 1
            if msg:
                print(f"[ingest] skipped chunk file={rel} idx={idx} reason={msg}")

    return stored, skipped


async def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ingest markdown files into Gen88 v4 SSOT."
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--dir", help="Directory to scan recursively for .md files")
    src.add_argument(
        "--path",
        action="append",
        default=[],
        help="Specific markdown file to ingest (repeatable).",
    )
    parser.add_argument(
        "--tags",
        nargs="*",
        default=["gen88_v4", "ssot"],
        help="Base tags to apply to every stored memory",
    )
    parser.add_argument(
        "--memory-type",
        default="file",
        help="Memory type label stored alongside the memory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Dry-run (default): do not write, only report what would be stored",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Actually write memories into the SSOT (disables dry-run)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=200,
        help="Maximum number of markdown files to ingest",
    )
    parser.add_argument(
        "--chunk-chars",
        type=int,
        default=12000,
        help="Chunk size in characters when content is large (0 disables chunking)",
    )

    args = parser.parse_args()

    repo_root = _repo_root()

    selected_files: list[Path] = []
    if args.path:
        for raw in args.path:
            p = (
                (repo_root / raw).resolve()
                if not Path(raw).is_absolute()
                else Path(raw).resolve()
            )
            if not p.exists() or not p.is_file():
                raise SystemExit(f"--path does not exist or is not a file: {p}")
            if p.suffix.lower() != ".md":
                raise SystemExit(f"--path is not a .md file: {p}")
            selected_files.append(p)
    else:
        scan_dir = (
            (repo_root / args.dir).resolve()
            if not Path(args.dir).is_absolute()
            else Path(args.dir).resolve()
        )
        if not scan_dir.exists() or not scan_dir.is_dir():
            raise SystemExit(f"--dir does not exist or is not a directory: {scan_dir}")

        selected_files = list(_iter_markdown_files(scan_dir))

    dry_run = bool(args.dry_run and not args.write)

    if not dry_run:
        enforce_ssot_or_exit(repo_root=repo_root)

    sqlite_path = os.environ.get("MCP_MEMORY_SQLITE_PATH")
    if not sqlite_path:
        sqlite_path = resolve_path(
            dotted_key="paths.mcp_memory_ssot_sqlite",
            env_var="MCP_MEMORY_SQLITE_PATH",
            default=str(
                repo_root
                / "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"
            ),
        )

    storage = await create_storage_instance(sqlite_path=sqlite_path, server_type="mcp")

    stored_total = 0
    skipped_total = 0

    max_files = int(args.max_files)
    files = selected_files if max_files <= 0 else selected_files[:max_files]

    for fp in files:
        stored, skipped = await _ingest_one_file(
            storage,
            file_path=fp,
            repo_root=repo_root,
            base_tags=list(args.tags),
            memory_type=str(args.memory_type),
            dry_run=dry_run,
            chunk_chars=int(args.chunk_chars),
        )
        stored_total += stored
        skipped_total += skipped

    mode = "DRY_RUN" if dry_run else "WRITE"
    if args.dir:
        source_desc = f"dir={scan_dir}"
    else:
        source_desc = f"paths={len(args.path)}"
    print(
        f"[ingest] mode={mode} {source_desc} files={len(files)} stored={stored_total} skipped={skipped_total}"
    )
    print(f"[ingest] sqlite={sqlite_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
