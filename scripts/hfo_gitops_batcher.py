#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""HFO GitOps Batcher (low-load, async-friendly).

Why
- Git can spike CPU/RAM/disk when enumerating huge untracked trees.
- This tool avoids repo-wide scans by:
  - optionally disabling untracked listing
  - committing tracked-only changes first (git add -u)
  - adding untracked files only via explicit allowlisted paths

Safety defaults
- Does NOT push by default (set --push or env HFO_GITOPS_PUSH=1).
- Uses explicit batch paths from .gitops/batches.json.

Usage
- One-shot run (no push):
    python3 scripts/hfo_gitops_batcher.py
- Run and push:
    HFO_GITOPS_PUSH=1 python3 scripts/hfo_gitops_batcher.py
- Daemon mode:
    python3 scripts/hfo_gitops_batcher.py --interval-sec 600

Notes
- If git authentication prompts, run interactively (not as daemon).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = REPO_ROOT / ".gitops" / "batches.json"


@dataclass(frozen=True)
class Batch:
    id: str
    type: str  # tracked | untracked
    message: str
    paths: list[str]


def _run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )


def _log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] [gitops] {msg}")
    sys.stdout.flush()


def _git(args: list[str], *, check: bool = True) -> str:
    cp = _run(["git", *args], check=check)
    return (cp.stdout or "").strip()


def _load_config(path: Path) -> tuple[dict, list[Batch]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    defaults = raw.get("defaults", {})
    batches = []
    for b in raw.get("batches", []):
        batches.append(
            Batch(
                id=b["id"],
                type=b["type"],
                message=b["message"],
                paths=list(b.get("paths", [])),
            )
        )
    return defaults, batches


def _set_show_untracked(enabled: bool) -> None:
    val = "normal" if enabled else "no"
    _git(["config", "--local", "status.showUntrackedFiles", val], check=False)


def _has_any_changes() -> bool:
    # Avoid -uall scans; rely on diff/index only.
    return bool(_git(["status", "--porcelain=v1"], check=True))


def _stage_tracked(paths: Iterable[str]) -> None:
    # Stage modifications/deletions of tracked files only.
    _git(["add", "-u", "--", *paths], check=True)


def _stage_untracked(paths: Iterable[str]) -> None:
    # Stage only explicitly provided paths.
    _git(["add", "--", *paths], check=True)


def _has_staged() -> bool:
    return bool(_git(["diff", "--cached", "--name-only"], check=True))


def _commit(message: str) -> str:
    _git(["commit", "-m", message], check=True)
    return _git(["rev-parse", "HEAD"], check=True)


def _push(remote: str, branch: str) -> None:
    _git(["push", remote, branch], check=True)


def run_once(config_path: Path, push: bool | None) -> int:
    if not config_path.exists():
        _log(f"missing config: {config_path}")
        return 2

    defaults, batches = _load_config(config_path)

    show_untracked = bool(defaults.get("showUntracked", False))
    remote = str(defaults.get("remote", "origin"))
    branch = str(defaults.get("branch", "master"))

    env_push = os.environ.get("HFO_GITOPS_PUSH", "").strip() in {"1", "true", "TRUE", "yes", "YES"}
    do_push = env_push if push is None else bool(push)

    _set_show_untracked(show_untracked)

    # Keep status cheap.
    _log(f"start push={do_push} remote={remote} branch={branch} showUntracked={show_untracked}")

    for b in batches:
        try:
            # Clear index staging from prior partial run.
            _git(["reset"], check=True)

            if b.type == "tracked":
                _log(f"batch {b.id}: stage tracked {b.paths}")
                _stage_tracked(b.paths)
            elif b.type == "untracked":
                _log(f"batch {b.id}: stage explicit {b.paths}")
                _stage_untracked(b.paths)
            else:
                _log(f"skip unknown batch type: {b.type} ({b.id})")
                continue

            if not _has_staged():
                _log(f"batch {b.id}: no staged changes; skip")
                continue

            sha = _commit(b.message)
            _log(f"batch {b.id}: committed {sha[:12]}")

            if do_push:
                _push(remote, branch)
                _log(f"batch {b.id}: pushed {remote}/{branch}")
        except subprocess.CalledProcessError as e:
            _log(f"batch {b.id}: ERROR\n{e.stdout}")
            return 1

    _log("done")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default=str(DEFAULT_CONFIG))
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--interval-sec", type=int, default=0)
    args = ap.parse_args()

    push: bool | None
    if args.push:
        push = True
    elif args.no_push:
        push = False
    else:
        push = None

    interval = int(args.interval_sec)
    if interval <= 0:
        return run_once(Path(args.config), push)

    interval = max(60, interval)
    while True:
        rc = run_once(Path(args.config), push)
        # If an error happens, back off but keep looping.
        if rc != 0:
            _log(f"non-zero rc={rc}; sleeping {interval}s")
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
