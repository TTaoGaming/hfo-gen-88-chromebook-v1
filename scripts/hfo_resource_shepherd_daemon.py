#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""HFO Resource Shepherd (timer-based cleanup daemon).

Goal
- Reduce chances of git / browser / test runs crashing the box by periodically
  pruning *known safe* derived artifacts.

Safety
- Only deletes paths that are typically generated and already gitignored.
- Never touches:
  - tracked source files
  - Obsidian vault data
  - JSONL logs (blackboards/memory)
  - DuckDB files

Usage
- Run continuously:
    python3 scripts/hfo_resource_shepherd_daemon.py --interval-sec 300
- One-shot:
    python3 scripts/hfo_resource_shepherd_daemon.py --once
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SweepResult:
    removed_paths: int
    removed_bytes_est: int
    errors: int


def _now() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _disk_snapshot(path: Path) -> str:
    try:
        usage = shutil.disk_usage(path)
        gib = 1024 ** 3
        return (
            f"disk free={usage.free / gib:.2f}GiB "
            f"used={usage.used / gib:.2f}GiB total={usage.total / gib:.2f}GiB"
        )
    except Exception as e:
        return f"disk snapshot failed: {e}"


def _safe_unlink(path: Path) -> int:
    try:
        sz = path.stat().st_size if path.exists() and path.is_file() else 0
        path.unlink(missing_ok=True)
        return int(sz)
    except Exception:
        return 0


def _safe_rmtree(path: Path) -> int:
    """Best-effort remove directory, returning estimated bytes freed."""

    removed_bytes = 0
    try:
        if not path.exists():
            return 0
        for root, _dirs, files in os.walk(path):
            for f in files:
                fp = Path(root) / f
                try:
                    removed_bytes += int(fp.stat().st_size)
                except Exception:
                    pass
        shutil.rmtree(path, ignore_errors=True)
    except Exception:
        return removed_bytes
    return removed_bytes


def _iter_candidates(repo_root: Path, aggressive: bool) -> list[Path]:
    """Return conservative cleanup targets (relative to repo root)."""

    base = [
        # Playwright outputs
        repo_root / "test-results",
        repo_root / "playwright-report",

        # Python caches
        repo_root / ".pytest_cache",
        repo_root / ".mypy_cache",
        repo_root / ".ruff_cache",
        repo_root / ".cache",

        # JS caches
        repo_root / ".turbo",
        repo_root / ".parcel-cache",
        repo_root / ".npm",
        repo_root / ".pnpm-store",
    ]

    if aggressive:
        # Optional extra cleanup that can be re-generated quickly.
        base.extend(
            [
                repo_root / "dist",
                repo_root / "build",
                repo_root / "coverage",
            ]
        )

    return base


def sweep(repo_root: Path, aggressive: bool) -> SweepResult:
    removed_paths = 0
    removed_bytes = 0
    errors = 0

    # 1) Fixed top-level candidates.
    for p in _iter_candidates(repo_root, aggressive=aggressive):
        try:
            if p.is_dir():
                removed_bytes += _safe_rmtree(p)
                removed_paths += 1
            elif p.is_file():
                removed_bytes += _safe_unlink(p)
                removed_paths += 1
        except Exception:
            errors += 1

    # 2) Recursive python bytecode caches (bounded walk).
    # Avoid scanning huge vendor trees by ignoring common hotspots.
    ignore_substrings = {
        str(repo_root / "node_modules"),
        str(repo_root / ".venv"),
        str(repo_root / "hfo_cold_obsidian"),
        str(repo_root / "Obsidian2025"),
    }

    try:
        for root, dirs, files in os.walk(repo_root):
            root_path = Path(root)
            root_s = str(root_path)

            if any(s in root_s for s in ignore_substrings):
                dirs[:] = []
                continue

            # Prune __pycache__ directories.
            if root_path.name == "__pycache__":
                removed_bytes += _safe_rmtree(root_path)
                removed_paths += 1
                dirs[:] = []
                continue

            for f in files:
                if f.endswith(".pyc"):
                    removed_bytes += _safe_unlink(root_path / f)
    except Exception:
        errors += 1

    return SweepResult(removed_paths=removed_paths, removed_bytes_est=removed_bytes, errors=errors)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval-sec", type=int, default=300)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--aggressive", action="store_true")
    args = ap.parse_args()

    interval = max(30, int(args.interval_sec))

    print(f"[{_now()}] [shepherd] start repo={REPO_ROOT} interval={interval}s aggressive={bool(args.aggressive)}")
    print(f"[{_now()}] [shepherd] {_disk_snapshot(REPO_ROOT)}")

    def run_once() -> None:
        nonlocal interval
        before = _disk_snapshot(REPO_ROOT)
        res = sweep(REPO_ROOT, aggressive=bool(args.aggressive))
        after = _disk_snapshot(REPO_ROOT)
        mib = 1024 ** 2
        freed = res.removed_bytes_est / mib
        print(
            f"[{_now()}] [shepherd] sweep removed_paths={res.removed_paths} "
            f"freed_est={freed:.1f}MiB errors={res.errors}"
        )
        print(f"[{_now()}] [shepherd] before {before}")
        print(f"[{_now()}] [shepherd] after  {after}")
        sys.stdout.flush()

    if args.once:
        run_once()
        return 0

    while True:
        run_once()
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
