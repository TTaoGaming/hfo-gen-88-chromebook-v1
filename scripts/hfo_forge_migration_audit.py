#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Audit legacy-root references.

Goal:
- Make it obvious what still needs to be moved from legacy roots into the forges.

What it does:
- Scans workspace text files for references to legacy roots (defaults:
  `hfo_hot_obsidian/` and `hfo_cold_obsidian/`).
- Produces a markdown report with counts and a prioritized "top offenders" list.

Notes:
- This is intentionally conservative and read-only.
- It ignores common large/output directories (artifacts, node_modules, etc.).
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_PATTERNS = ("hfo_hot_obsidian/", "hfo_cold_obsidian/")
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "artifacts",
    "test-results",
    "Obsidian2025",
    "hfo_gen_88_cb_v2",
}
DEFAULT_EXTS = {
    ".md",
    ".py",
    ".sh",
    ".ts",
    ".js",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".mjs",
    ".cjs",
}


@dataclass(frozen=True)
class Hit:
    path: Path
    count: int


def _is_excluded_dir(path: Path, exclude_dirs: set[str]) -> bool:
    for part in path.parts:
        if part in exclude_dirs:
            return True
    return False


def _count_matches(text: str, patterns: tuple[str, ...]) -> int:
    return sum(text.count(p) for p in patterns)


def scan_repo(
    repo_root: Path,
    *,
    patterns: tuple[str, ...],
    exts: set[str],
    exclude_dirs: set[str],
) -> list[Hit]:
    hits: list[Hit] = []

    for root, dirs, files in os.walk(repo_root):
        root_path = Path(root)
        if _is_excluded_dir(root_path.relative_to(repo_root), exclude_dirs):
            dirs[:] = []
            continue

        # prune excluded dirs early
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for name in files:
            p = root_path / name
            if p.suffix not in exts:
                continue

            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue

            c = _count_matches(content, patterns)
            if c:
                hits.append(Hit(path=p.relative_to(repo_root), count=c))

    hits.sort(key=lambda h: (-h.count, str(h.path)))
    return hits


def render_markdown(
    *,
    repo_root: Path,
    patterns: tuple[str, ...],
    hits: list[Hit],
    top: int,
) -> str:
    total_hits = sum(h.count for h in hits)
    total_files = len(hits)

    lines: list[str] = []
    lines.append("---")
    lines.append("medallion_layer: bronze")
    lines.append("mutation_score: 0")
    lines.append("hive: V")
    lines.append("---")
    lines.append("")
    lines.append("# Forge Migration Audit (Legacy Roots → Forges)")
    lines.append("")
    lines.append("## Objective")
    lines.append(
        "Make it obvious which files still reference legacy roots so we can consolidate around the two forges (hot + cold)."
    )
    lines.append("")
    lines.append("## Patterns")
    for p in patterns:
        lines.append(f"- `{p}`")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- repo_root: `{repo_root}`")
    lines.append(f"- files_with_hits: `{total_files}`")
    lines.append(f"- total_hits: `{total_hits}`")
    lines.append("")

    if not hits:
        lines.append("No legacy-root references found. ✅")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"## Top {min(top, len(hits))} offenders")
    for h in hits[:top]:
        lines.append(f"- `{h.count}`: `{h.path.as_posix()}`")
    lines.append("")

    lines.append("## Full list")
    for h in hits:
        lines.append(f"- `{h.count}`: `{h.path.as_posix()}`")
    lines.append("")

    lines.append("## Interpretation")
    lines.append("- Prefer moving content into `hfo_hot_obsidian_forge/` or `hfo_cold_obsidian_forge/`.")
    lines.append("- For load-bearing legacy paths, convert call-sites to resolve via `hfo_pointers.py`.")
    lines.append("- Keep `hfo_hot_obsidian/` and `hfo_cold_obsidian/` as compatibility-only drains until cutover is complete.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Repo root to scan (default: workspace root)",
    )
    parser.add_argument(
        "--patterns",
        default=",".join(DEFAULT_PATTERNS),
        help="Comma-separated patterns to count",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=50,
        help="How many top offenders to list",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output markdown file path (relative to repo root or absolute)",
    )

    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    patterns = tuple(p.strip() for p in args.patterns.split(",") if p.strip())

    out_path = Path(args.out).expanduser()
    if not out_path.is_absolute():
        out_path = repo_root / out_path

    hits = scan_repo(
        repo_root,
        patterns=patterns,
        exts=DEFAULT_EXTS,
        exclude_dirs=DEFAULT_EXCLUDE_DIRS,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        render_markdown(repo_root=repo_root, patterns=patterns, hits=hits, top=args.top),
        encoding="utf-8",
    )
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
