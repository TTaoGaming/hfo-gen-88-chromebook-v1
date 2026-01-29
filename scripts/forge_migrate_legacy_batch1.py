#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Batch-1 legacy → forge migration (copy-first, idempotent).

Why this exists:
- `rsync` is not guaranteed to be installed in all environments.
- GitOps provenance gate requires a Medallion header for HOT `.md`/`.html`.

What it does:
- Copies a small, low-risk set of legacy docs into forge Bronze/Silver PARA buckets.
- Skips existing destination files by default (safe re-runs).
- Optionally injects a Medallion provenance header into copied `.md`/`.html`.

This script is intentionally dependency-free.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]


EXCLUDED_SUFFIXES = (
    ".jsonl",
    ".duckdb",
    ".parquet",
    ".sqlite",
    ".sqlite3",
    ".db",
)


@dataclass(frozen=True)
class Mapping:
    src_root: Path
    dst_root: Path
    medallion: str  # e.g. "Bronze", "Silver"


DEFAULT_MAPPINGS: list[Mapping] = [
    Mapping(
        src_root=REPO_ROOT / "hfo_hot_obsidian/bronze/3_resources/reports",
        dst_root=REPO_ROOT
        / "hfo_hot_obsidian_forge/0_bronze/2_resources/reports/legacy_hot_obsidian_bronze",
        medallion="Bronze",
    ),
    Mapping(
        src_root=REPO_ROOT / "hfo_hot_obsidian/silver/3_resources/reports",
        dst_root=REPO_ROOT
        / "hfo_hot_obsidian_forge/1_silver/2_resources/reports/legacy_hot_obsidian_silver",
        medallion="Silver",
    ),
    Mapping(
        src_root=REPO_ROOT / "hfo_cold_obsidian/bronze/3_resources/reports",
        dst_root=REPO_ROOT
        / "hfo_cold_obsidian_forge/0_bronze/2_resources/reports/legacy_cold_obsidian_bronze",
        medallion="Bronze",
    ),
    Mapping(
        src_root=REPO_ROOT / "hfo_cold_obsidian/bronze/3_resources/playbooks",
        dst_root=REPO_ROOT
        / "hfo_cold_obsidian_forge/0_bronze/2_resources/playbooks/legacy_cold_obsidian_bronze",
        medallion="Bronze",
    ),
]


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        name = path.name
        if name.startswith("."):
            continue
        if name == "__pycache__":
            continue
        if any(name.endswith(suf) for suf in EXCLUDED_SUFFIXES):
            continue
        yield path


def _has_medallion_header(head: str) -> bool:
    lines = head.splitlines()
    first_nonempty_idx = None
    first_nonempty = ""
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s:
            continue
        first_nonempty_idx = i
        first_nonempty = s
        break

    if first_nonempty_idx is None:
        return False

    if first_nonempty.startswith("# Medallion:") or first_nonempty.startswith(
        "<!-- Medallion:"
    ):
        return True

    # YAML front matter provenance
    if first_nonempty == "---":
        fm_lines: list[str] = []
        for ln in lines[first_nonempty_idx + 1 :]:
            if ln.strip() == "---":
                break
            fm_lines.append(ln)
        fm = "\n".join(fm_lines)
        if "medallion_layer:" in fm or "\nmedallion:" in ("\n" + fm):
            return True

    return False


def ensure_provenance_header(path: Path, *, medallion: str) -> bool:
    """Ensure a Medallion header exists. Returns True if modified."""

    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False

    head = raw[:8192]
    if _has_medallion_header(head):
        return False

    header = f"<!-- Medallion: {medallion} | Mutation: 0% | HIVE: V -->\n"
    path.write_text(header + raw, encoding="utf-8")
    return True


def run(
    *, mode: str, overwrite: bool, add_provenance: bool, log_path: Path | None
) -> int:
    if mode not in {"dry-run", "write"}:
        raise ValueError("mode must be 'dry-run' or 'write'")

    def log(obj: dict) -> None:
        line = json.dumps(obj, sort_keys=True)
        if log_path is not None:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        else:
            print(line)

    copied = 0
    skipped_exists = 0
    missing_sources: list[str] = []

    for m in DEFAULT_MAPPINGS:
        if not m.src_root.exists():
            missing_sources.append(str(m.src_root))
            continue

        m.dst_root.mkdir(parents=True, exist_ok=True)

        for src in iter_files(m.src_root):
            rel = src.relative_to(m.src_root)
            dst = m.dst_root / rel
            if dst.exists() and not overwrite:
                skipped_exists += 1
                log(
                    {
                        "action": "skip_exists",
                        "src": str(src.relative_to(REPO_ROOT)),
                        "dst": str(dst.relative_to(REPO_ROOT)),
                    }
                )
                continue

            log(
                {
                    "action": "copy" if mode == "write" else "plan_copy",
                    "src": str(src.relative_to(REPO_ROOT)),
                    "dst": str(dst.relative_to(REPO_ROOT)),
                }
            )

            if mode == "write":
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1

    provenance_touched = 0
    if add_provenance:
        for m in DEFAULT_MAPPINGS:
            if not m.dst_root.exists():
                continue
            for p in m.dst_root.rglob("*"):
                if not p.is_file():
                    continue
                if p.suffix.lower() not in {".md", ".html"}:
                    continue
                if mode == "write":
                    if ensure_provenance_header(p, medallion=m.medallion):
                        provenance_touched += 1
                else:
                    # Dry-run heuristic: count files that appear to miss header.
                    try:
                        head = p.read_text(encoding="utf-8", errors="replace")[:8192]
                    except OSError:
                        continue
                    if not _has_medallion_header(head):
                        provenance_touched += 1

    summary = {
        "mode": mode,
        "copied": copied,
        "skipped_exists": skipped_exists,
        "provenance_touched": provenance_touched,
        "missing_sources": missing_sources,
    }
    log({"action": "summary", **summary})

    if missing_sources:
        print("Missing source dirs:", file=sys.stderr)
        for s in missing_sources:
            print(f"- {s}", file=sys.stderr)

    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["dry-run", "write"], default="dry-run")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--no-provenance", action="store_true")
    ap.add_argument("--log", type=str, default="")
    args = ap.parse_args()

    log_path = Path(args.log) if args.log else None
    if log_path is not None and not log_path.is_absolute():
        log_path = REPO_ROOT / log_path

    return run(
        mode=args.mode,
        overwrite=bool(args.overwrite),
        add_provenance=not bool(args.no_provenance),
        log_path=log_path,
    )


if __name__ == "__main__":
    raise SystemExit(main())
