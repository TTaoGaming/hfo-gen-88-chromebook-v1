#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Ingest text-like files into the Gen88 v4 blessed memory SSOT (doobidoo sqlite_vec).

This is a scalable companion to scripts/hfo_memory_ingest_markdown_dir.py.
It targets *text-like* files (code, markdown, config, logs) and intentionally
skips binaries.

Safety:
- Default is dry-run.
- Uses pointer-resolved SSOT sqlite path (or env MCP_MEMORY_SQLITE_PATH override).
- Relies on SSOT unique constraint on content_hash to dedupe.

Typical usage (start small):
  bash scripts/mcp_env_wrap.sh ./.venv/bin/python \
    scripts/hfo_memory_ingest_text_dir.py \
      --dir /path/to/big_corpus \
      --max-files 200 \
      --max-bytes 2000000 \
      --tags gen88_v4 ssot topic:corpus

Then actually write:
  ... same args ... --write

Multi-machine strategy:
- Export from a remote sqlite SSOT to JSONL, copy it, then import into the
  canonical SSOT on this machine.
  See: scripts/hfo_memory_export_doobidoo_ssot.py and scripts/hfo_memory_import_jsonl_to_doobidoo.py
"""

from __future__ import annotations

import argparse
import asyncio
import fnmatch
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

_DEFAULT_EXTS = [
    ".md",
    ".mdx",
    ".txt",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".sh",
    ".bash",
    ".zsh",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".log",
    ".html",
    ".css",
]

_DEFAULT_EXCLUDE_GLOBS = [
    "**/.git/**",
    "**/.venv/**",
    "**/venv/**",
    "**/__pycache__/**",
    "**/node_modules/**",
    "**/dist/**",
    "**/build/**",
    "**/.next/**",
    "**/.cache/**",
]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _should_exclude(rel_path: str, exclude_globs: list[str]) -> bool:
    # Normalize to forward slashes for glob matching.
    rel = rel_path.replace("\\", "/")
    return any(fnmatch.fnmatch(rel, pat) for pat in exclude_globs)


def _iter_candidate_files(
    root: Path,
    *,
    exts: set[str],
    exclude_globs: list[str],
    max_bytes: int,
) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        try:
            size = path.stat().st_size
        except OSError:
            continue

        if max_bytes > 0 and size > max_bytes:
            continue

        if path.suffix.lower() not in exts:
            continue

        rel = str(path)
        if _should_exclude(rel, exclude_globs):
            continue

        yield path


def _chunk_text(text: str, chunk_chars: int) -> list[str]:
    if chunk_chars <= 0:
        return [text]
    if len(text) <= chunk_chars:
        return [text]
    return [text[i : i + chunk_chars] for i in range(0, len(text), chunk_chars)]


def _read_optional_text_file(path: str | None) -> str:
    if not path:
        return ""
    p = Path(path)
    if not p.is_absolute():
        p = _repo_root() / p
    p = p.resolve()
    if not p.exists() or not p.is_file():
        raise SystemExit(
            f"--evolutionary-notes-file does not exist or is not a file: {p}"
        )
    return p.read_text(encoding="utf-8", errors="replace")


def _load_paths_file(paths_file: str, *, repo_root: Path) -> list[Path]:
    p = Path(paths_file)
    if not p.is_absolute():
        p = repo_root / p
    p = p.resolve()
    if not p.exists() or not p.is_file():
        raise SystemExit(f"--paths-file does not exist or is not a file: {p}")

    out: list[Path] = []
    for raw_line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        candidate = Path(line)
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        candidate = candidate.resolve()
        if candidate.exists() and candidate.is_file():
            out.append(candidate)
        else:
            print(f"[ingest] warn: paths-file entry missing/invalid: {line}")

    # Dedupe while preserving order
    seen: set[str] = set()
    deduped: list[Path] = []
    for fp in out:
        key = str(fp)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(fp)
    return deduped


async def _ingest_one_file(
    storage,
    *,
    file_path: Path,
    repo_root: Path,
    base_tags: list[str],
    memory_type: str,
    dry_run: bool,
    chunk_chars: int,
    evolutionary_notes: str,
) -> tuple[int, int]:
    try:
        rel = str(file_path.resolve().relative_to(repo_root))
    except ValueError:
        rel = str(file_path.resolve())

    raw = file_path.read_text(encoding="utf-8", errors="replace")

    # Include provenance for retrieval context without rewriting the source file.
    header = f"[source:file:{rel}]\n"

    evo = (evolutionary_notes or "").strip()
    evo_block = ""
    if evo:
        evo_block = "[evolutionary_notes]\n" + evo + "\n[/evolutionary_notes]\n\n"

    content = header + evo_block + raw

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
        description="Ingest text-like files into Gen88 v4 SSOT."
    )
    parser.add_argument(
        "--dir",
        required=False,
        help="Directory to scan recursively (ignored when --paths-file is provided)",
    )
    parser.add_argument(
        "--paths-file",
        required=False,
        help="Newline-separated list of file paths to ingest (repo-relative or absolute). Lines starting with # are ignored.",
    )
    parser.add_argument(
        "--include-ext",
        nargs="*",
        default=_DEFAULT_EXTS,
        help="File extensions to ingest (e.g. .md .txt .py)",
    )
    parser.add_argument(
        "--exclude-glob",
        nargs="*",
        default=_DEFAULT_EXCLUDE_GLOBS,
        help="Glob patterns to exclude (matched against full path)",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=2_000_000,
        help="Skip files larger than this many bytes (0 disables)",
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
        default=500,
        help="Maximum number of files to ingest (<=0 means no limit)",
    )
    parser.add_argument(
        "--chunk-chars",
        type=int,
        default=12000,
        help="Chunk size in characters when content is large (0 disables chunking)",
    )
    parser.add_argument(
        "--evolutionary-notes",
        default="",
        help="Optional text prepended to every ingested memory inside an [evolutionary_notes] block",
    )
    parser.add_argument(
        "--evolutionary-notes-file",
        default="",
        help="Optional file whose contents are prepended to every ingested memory inside an [evolutionary_notes] block",
    )

    args = parser.parse_args()

    repo_root = _repo_root()

    scan_dir: Path | None = None
    if not args.paths_file:
        if not args.dir:
            raise SystemExit("Must provide --dir or --paths-file")
        scan_dir = (
            (repo_root / args.dir).resolve()
            if not Path(args.dir).is_absolute()
            else Path(args.dir).resolve()
        )
        assert scan_dir is not None
        if not scan_dir.exists() or not scan_dir.is_dir():
            raise SystemExit(f"--dir does not exist or is not a directory: {scan_dir}")

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

    exts = {
        e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.include_ext
    }

    evolutionary_notes = (str(args.evolutionary_notes) or "").strip()
    if args.evolutionary_notes_file:
        file_notes = _read_optional_text_file(str(args.evolutionary_notes_file))
        file_notes = (file_notes or "").strip()
        if file_notes:
            evolutionary_notes = (
                (evolutionary_notes + "\n" + file_notes).strip()
                if evolutionary_notes
                else file_notes
            )

    stored_total = 0
    skipped_total = 0

    max_files = int(args.max_files)

    if args.paths_file:
        candidates = _load_paths_file(str(args.paths_file), repo_root=repo_root)
        # Apply the same lightweight filters for consistency
        filtered: list[Path] = []
        for fp in candidates:
            try:
                size = fp.stat().st_size
            except OSError:
                continue
            if int(args.max_bytes) > 0 and size > int(args.max_bytes):
                continue
            if fp.suffix.lower() not in exts:
                continue
            rel = str(fp)
            if _should_exclude(rel, list(args.exclude_glob)):
                continue
            filtered.append(fp)
        files = filtered if max_files <= 0 else filtered[:max_files]
    else:
        assert scan_dir is not None
        candidates = list(
            _iter_candidate_files(
                scan_dir,
                exts=exts,
                exclude_globs=list(args.exclude_glob),
                max_bytes=int(args.max_bytes),
            )
        )
        files = candidates if max_files <= 0 else candidates[:max_files]

    for fp in files:
        stored, skipped = await _ingest_one_file(
            storage,
            file_path=fp,
            repo_root=repo_root,
            base_tags=list(args.tags),
            memory_type=str(args.memory_type),
            dry_run=dry_run,
            chunk_chars=int(args.chunk_chars),
            evolutionary_notes=evolutionary_notes,
        )
        stored_total += stored
        skipped_total += skipped

    mode = "DRY_RUN" if dry_run else "WRITE"
    print(
        f"[ingest] mode={mode} source={'paths-file' if args.paths_file else 'dir'} files={len(files)} stored={stored_total} skipped={skipped_total} "
        f"max_bytes={int(args.max_bytes)} exts={sorted(exts)}"
    )
    print(f"[ingest] sqlite={sqlite_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
