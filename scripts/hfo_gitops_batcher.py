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
- Uses git hooks by default; pass --no-verify only when you intentionally want to bypass pre-commit.

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


def _commit(message: str, *, no_verify: bool) -> str:
    args = ["commit", "-m", message]
    if no_verify:
        args.append("--no-verify")
    _git(args, check=True)
    return _git(["rev-parse", "HEAD"], check=True)


def _push(remote: str, branch: str) -> None:
    _git(["push", remote, branch], check=True)


def _current_branch() -> str:
    # Empty string in detached HEAD.
    return _git(["symbolic-ref", "--short", "-q", "HEAD"], check=False)


def _resolve_branch(configured_branch: str) -> str:
    """Resolve branch target.

    Priority:
    1) env HFO_GITOPS_BRANCH (if set)
    2) config defaults.branch

    Special values:
    - CURRENT / AUTO: use the currently checked-out branch.
    """

    env_branch = os.environ.get("HFO_GITOPS_BRANCH", "").strip()
    branch = env_branch or (configured_branch or "").strip()

    if branch.upper() in {"CURRENT", "AUTO"}:
        return _current_branch()

    return branch


def _ensure_remote_exists(remote: str) -> None:
    _git(["remote", "get-url", remote], check=True)


def run_once(
    config_path: Path,
    push: bool | None,
    *,
    push_mode: str,
    no_verify: bool,
) -> int:
    if not config_path.exists():
        _log(f"missing config: {config_path}")
        return 2

    defaults, batches = _load_config(config_path)

    show_untracked = bool(defaults.get("showUntracked", False))
    remote = str(defaults.get("remote", "origin"))
    configured_branch = str(defaults.get("branch", "master"))
    branch = _resolve_branch(configured_branch)
    if not branch:
        _log(
            "branch resolution failed (detached HEAD or empty branch); "
            "set defaults.branch or HFO_GITOPS_BRANCH to push"
        )
        if (os.environ.get("HFO_GITOPS_PUSH", "").strip() in {"1", "true", "TRUE", "yes", "YES"}) or (
            push is True
        ):
            return 1

    env_push = os.environ.get("HFO_GITOPS_PUSH", "").strip() in {"1", "true", "TRUE", "yes", "YES"}
    do_push = env_push if push is None else bool(push)

    if do_push:
        try:
            _ensure_remote_exists(remote)
        except subprocess.CalledProcessError as e:
            _log(f"remote '{remote}' not configured; refusing to push\n{e.stdout}")
            return 1

        current = _current_branch()
        if not current:
            _log("detached HEAD; refusing to push")
            return 1
        if current != branch:
            _log(f"current branch '{current}' != configured branch '{branch}'; refusing to push")
            return 1

    _set_show_untracked(show_untracked)

    # Keep status cheap.
    _log(
        f"start push={do_push} remote={remote} branch={branch} "
        f"showUntracked={show_untracked} (defaults.branch={configured_branch!r})"
    )

    any_commits = False

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

            sha = _commit(b.message, no_verify=no_verify)
            _log(f"batch {b.id}: committed {sha[:12]}")

            any_commits = True

            if do_push and push_mode == "each":
                _push(remote, branch)
                _log(f"batch {b.id}: pushed {remote}/{branch}")
        except subprocess.CalledProcessError as e:
            _log(f"batch {b.id}: ERROR\n{e.stdout}")
            return 1

    if do_push and push_mode == "end" and any_commits:
        try:
            _push(remote, branch)
            _log(f"pushed {remote}/{branch}")
        except subprocess.CalledProcessError as e:
            _log(f"push ERROR\n{e.stdout}")
            return 1

    _log("done")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, default=str(DEFAULT_CONFIG))
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument(
        "--no-verify",
        action="store_true",
        help="Bypass git commit hooks (use intentionally; default runs hooks).",
    )
    ap.add_argument(
        "--push-mode",
        type=str,
        choices=["each", "end"],
        default="each",
        help="When pushing is enabled, push after each batch commit (each) or once at the end (end).",
    )
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
        return run_once(
            Path(args.config),
            push,
            push_mode=str(args.push_mode),
            no_verify=bool(args.no_verify),
        )

    interval = max(60, interval)
    while True:
        rc = run_once(
            Path(args.config),
            push,
            push_mode=str(args.push_mode),
            no_verify=bool(args.no_verify),
        )
        # If an error happens, back off but keep looping.
        if rc != 0:
            _log(f"non-zero rc={rc}; sleeping {interval}s")
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
