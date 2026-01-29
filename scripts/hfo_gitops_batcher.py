#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""HFO GitOps Batcher (low-load, async-friendly).

Why
- Git can spike CPU/RAM/disk when enumerating huge untracked trees.
- This tool avoids repo-wide scans by:
    - never relying on repo-wide untracked enumeration
    - committing tracked-only changes first (git add -u)
    - adding untracked files only via explicit allowlisted paths

Safety defaults
- Does NOT push by default (set --push or env HFO_GITOPS_PUSH=1).
- Uses explicit batch paths from .gitops/batches.json.
- Uses git hooks by default; pass --no-verify only when you intentionally want to bypass pre-commit.
- Writes an append-only proof bundle under artifacts/proofs/ (receipt + logs).

Usage
- One-shot run (no push):
    python3 scripts/hfo_gitops_batcher.py
- Run and push:
    HFO_GITOPS_PUSH=1 python3 scripts/hfo_gitops_batcher.py
- Plan-only (no mutations):
    python3 scripts/hfo_gitops_batcher.py --plan
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
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
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


@dataclass
class BatchReceipt:
    id: str
    type: str
    message: str
    paths: list[str]
    planned_tracked_changes: int = 0
    planned_untracked_files: int = 0
    staged_files_count: int = 0
    staged_files_sample: list[str] | None = None
    commit_sha: str | None = None
    outcome: str = "skipped"  # skipped | planned | committed | error
    error: str | None = None


@dataclass
class RunReceipt:
    version: int
    run_id: str
    ts_utc_start: str
    ts_utc_end: str | None
    repo_root: str
    config_path: str
    branch: str
    remote: str
    push_enabled: bool
    push_mode: str
    plan_only: bool
    no_verify: bool
    git_status_show_untracked_prev: str | None
    dirty_tracked_before: list[str]
    dirty_tracked_after: list[str]
    batches: list[BatchReceipt]
    commits: list[str]
    exit_code: int | None


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


def _utc_now_iso_z() -> str:
    return (
        datetime.now(tz=timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _utc_run_id() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _git_config_get(key: str) -> str | None:
    val = _git(["config", "--local", "--get", key], check=False).strip()
    return val or None


def _git_config_set(key: str, value: str) -> None:
    _git(["config", "--local", key, value], check=False)


def _ensure_status_shows_untracked(*, enforce: bool) -> str | None:
    prev = _git_config_get("status.showUntrackedFiles")
    if enforce:
        # Prevent "it looks clean" confusion for humans and agents.
        _git_config_set("status.showUntrackedFiles", "all")
    return prev


def _dirty_tracked_paths(paths: Iterable[str] | None = None) -> list[str]:
    # -uno: avoid enumerating untracked files.
    args = ["status", "--porcelain=v1", "-uno"]
    if paths:
        args.extend(["--", *paths])
    out = _git(args, check=True)
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    # Porcelain lines are like " M path" or "D  path"; keep the trailing path.
    parsed: list[str] = []
    for ln in lines:
        # Split once; porcelain can have rename syntax, but keep line as-is for debugging.
        parts = ln.split(maxsplit=2)
        if len(parts) >= 2:
            parsed.append(parts[-1])
        else:
            parsed.append(ln)
    return parsed


def _planned_tracked_change_count(paths: Iterable[str]) -> int:
    # Restrict to allowlisted paths and avoid untracked scans.
    return len(_dirty_tracked_paths(paths))


def _planned_untracked_files(paths: Iterable[str], *, max_files: int) -> list[str]:
    args = ["ls-files", "-o", "--exclude-standard", "--", *paths]
    out = _git(args, check=True)
    files = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if max_files > 0:
        return files[:max_files]
    return files


def _stage_tracked(paths: Iterable[str]) -> None:
    # Stage modifications/deletions of tracked files only.
    _git(["add", "-u", "--", *paths], check=True)


def _stage_untracked(paths: Iterable[str]) -> None:
    # Stage only explicitly provided paths.
    _git(["add", "--", *paths], check=True)


def _has_staged() -> bool:
    return bool(_git(["diff", "--cached", "--name-only"], check=True))


def _staged_files(*, max_files: int) -> list[str]:
    out = _git(["diff", "--cached", "--name-only"], check=True)
    files = [ln.strip() for ln in out.splitlines() if ln.strip()]
    if max_files > 0:
        return files[:max_files]
    return files


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


def _write_json(path: Path, obj: object) -> None:
    if isinstance(obj, (RunReceipt, BatchReceipt)):
        obj = asdict(obj)
    path.write_text(
        json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _has_staged_paths() -> bool:
    return bool(_git(["diff", "--cached", "--name-only"], check=True).strip())


def run_once(
    config_path: Path,
    push: bool | None,
    *,
    push_mode: str,
    no_verify: bool,
    plan_only: bool,
    proof_dir: Path | None,
    enforce_status_untracked: bool,
    plan_max_files: int,
    staged_max_files: int,
    fail_on_dirty: bool,
    allow_dirty_index: bool,
) -> int:
    if not config_path.exists():
        _log(f"missing config: {config_path}")
        return 2

    defaults, batches = _load_config(config_path)

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

    # Proof bundle
    run_id = _utc_run_id()
    if proof_dir is None:
        proof_root = Path(
            str(defaults.get("proofRoot", REPO_ROOT / "artifacts" / "proofs"))
        )
        proof_dir = proof_root / f"gitops_{run_id}__{branch or 'detached'}"
    proof_dir.mkdir(parents=True, exist_ok=True)

    git_status_show_untracked_prev = _ensure_status_shows_untracked(
        enforce=enforce_status_untracked
    )

    dirty_before = _dirty_tracked_paths()
    if dirty_before and do_push and fail_on_dirty:
        _log("dirty tracked files present before push; refusing to proceed")
        (proof_dir / "dirty_tracked_before.txt").write_text(
            "\n".join(dirty_before) + "\n", encoding="utf-8"
        )
        return 1

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

    receipt = RunReceipt(
        version=1,
        run_id=run_id,
        ts_utc_start=_utc_now_iso_z(),
        ts_utc_end=None,
        repo_root=str(REPO_ROOT),
        config_path=str(config_path),
        branch=branch,
        remote=remote,
        push_enabled=do_push,
        push_mode=push_mode,
        plan_only=plan_only,
        no_verify=no_verify,
        git_status_show_untracked_prev=git_status_show_untracked_prev,
        dirty_tracked_before=dirty_before,
        dirty_tracked_after=[],
        batches=[],
        commits=[],
        exit_code=None,
    )

    _log(
        f"start push={do_push} remote={remote} branch={branch} "
        f"planOnly={plan_only} (defaults.branch={configured_branch!r}) proofDir={proof_dir}"
    )

    if _has_staged_paths() and not allow_dirty_index:
        # The batcher uses `git reset` to clear the index between batches. If we ran with
        # a non-empty index, we'd silently discard the operator's staging.
        _log("index has staged changes; refusing to run (pass --allow-dirty-index to override)")
        receipt.ts_utc_end = _utc_now_iso_z()
        receipt.exit_code = 1
        _write_json(proof_dir / "gitops_receipt.json", receipt)
        return 1

    any_commits = False

    for b in batches:
        batch_receipt = BatchReceipt(
            id=b.id, type=b.type, message=b.message, paths=b.paths
        )
        try:
            # Clear index staging from prior partial run.
            # (Safe because we refused to run if the operator had staged changes.)
            _git(["reset"], check=True)

            if plan_only:
                if b.type == "tracked":
                    batch_receipt.planned_tracked_changes = (
                        _planned_tracked_change_count(b.paths)
                    )
                    batch_receipt.outcome = (
                        "planned"
                        if batch_receipt.planned_tracked_changes
                        else "skipped"
                    )
                elif b.type == "untracked":
                    planned = _planned_untracked_files(
                        b.paths, max_files=plan_max_files
                    )
                    batch_receipt.planned_untracked_files = len(planned)
                    batch_receipt.staged_files_sample = planned if planned else None
                    batch_receipt.outcome = "planned" if planned else "skipped"
                else:
                    batch_receipt.outcome = "skipped"

                receipt.batches.append(batch_receipt)
                continue

            if b.type == "tracked":
                _log(f"batch {b.id}: stage tracked {b.paths}")
                _stage_tracked(b.paths)
            elif b.type == "untracked":
                _log(f"batch {b.id}: stage explicit {b.paths}")
                _stage_untracked(b.paths)
            else:
                _log(f"skip unknown batch type: {b.type} ({b.id})")
                receipt.batches.append(batch_receipt)
                continue

            if not _has_staged():
                _log(f"batch {b.id}: no staged changes; skip")
                batch_receipt.outcome = "skipped"
                receipt.batches.append(batch_receipt)
                continue

            staged = _staged_files(max_files=staged_max_files)
            batch_receipt.staged_files_count = len(
                _git(["diff", "--cached", "--name-only"], check=True).splitlines()
            )
            batch_receipt.staged_files_sample = staged if staged else None

            sha = _commit(b.message, no_verify=no_verify)
            _log(f"batch {b.id}: committed {sha[:12]}")

            batch_receipt.commit_sha = sha
            batch_receipt.outcome = "committed"
            receipt.commits.append(sha)
            receipt.batches.append(batch_receipt)

            any_commits = True

            if do_push and push_mode == "each":
                _push(remote, branch)
                _log(f"batch {b.id}: pushed {remote}/{branch}")
        except subprocess.CalledProcessError as e:
            _log(f"batch {b.id}: ERROR\n{e.stdout}")
            batch_receipt.outcome = "error"
            batch_receipt.error = (e.stdout or "").strip() or str(e)
            receipt.batches.append(batch_receipt)
            receipt.ts_utc_end = _utc_now_iso_z()
            receipt.exit_code = 1
            _write_json(proof_dir / "gitops_receipt.json", receipt)
            return 1

    if do_push and push_mode == "end" and any_commits:
        try:
            _push(remote, branch)
            _log(f"pushed {remote}/{branch}")
        except subprocess.CalledProcessError as e:
            _log(f"push ERROR\n{e.stdout}")
            receipt.ts_utc_end = _utc_now_iso_z()
            receipt.exit_code = 1
            _write_json(proof_dir / "gitops_receipt.json", receipt)
            return 1

    dirty_after = _dirty_tracked_paths()
    receipt.dirty_tracked_after = dirty_after
    if dirty_after:
        (proof_dir / "dirty_tracked_after.txt").write_text(
            "\n".join(dirty_after) + "\n", encoding="utf-8"
        )
        if fail_on_dirty:
            _log("dirty tracked files detected after run")
            receipt.ts_utc_end = _utc_now_iso_z()
            receipt.exit_code = 1
            _write_json(proof_dir / "gitops_receipt.json", receipt)
            return 1

    (proof_dir / "run_id.txt").write_text(f"{run_id}\n", encoding="utf-8")
    (proof_dir / "proof_dir.txt").write_text(f"{proof_dir}\n", encoding="utf-8")

    receipt.ts_utc_end = _utc_now_iso_z()
    receipt.exit_code = 0
    _write_json(proof_dir / "gitops_receipt.json", receipt)

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
    ap.add_argument(
        "--plan",
        action="store_true",
        help="Plan-only mode: do not stage/commit/push; only compute planned changes per batch and write a receipt.",
    )
    ap.add_argument(
        "--proof-dir",
        type=str,
        default="",
        help="Explicit proof directory (default: artifacts/proofs/gitops_<run_id>__<branch>/).",
    )
    ap.add_argument(
        "--enforce-status-untracked",
        action="store_true",
        help="Force git config status.showUntrackedFiles=all to avoid hidden-untracked confusion.",
    )
    ap.add_argument(
        "--no-enforce-status-untracked",
        action="store_true",
        help="Disable enforcing status.showUntrackedFiles=all.",
    )
    ap.add_argument(
        "--plan-max-files",
        type=int,
        default=50,
        help="In --plan mode, cap the untracked file sample stored in the receipt.",
    )
    ap.add_argument(
        "--staged-max-files",
        type=int,
        default=50,
        help="When committing, cap the staged file sample stored in the receipt.",
    )
    ap.add_argument(
        "--fail-on-dirty",
        action="store_true",
        help="Fail the run if tracked files are dirty before/after (recommended for swarm automation).",
    )
    ap.add_argument(
        "--allow-dirty-index",
        action="store_true",
        help="Allow a non-empty staged index (DANGEROUS: batcher clears index between batches).",
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

    enforce_status_untracked = True
    if bool(args.no_enforce_status_untracked):
        enforce_status_untracked = False
    elif bool(args.enforce_status_untracked):
        enforce_status_untracked = True

    proof_dir = Path(args.proof_dir) if str(args.proof_dir).strip() else None
    fail_on_dirty = bool(args.fail_on_dirty) or bool(push)
    if interval <= 0:
        return run_once(
            Path(args.config),
            push,
            push_mode=str(args.push_mode),
            no_verify=bool(args.no_verify),
            plan_only=bool(args.plan),
            proof_dir=proof_dir,
            enforce_status_untracked=enforce_status_untracked,
            plan_max_files=int(args.plan_max_files),
            staged_max_files=int(args.staged_max_files),
            fail_on_dirty=fail_on_dirty,
            allow_dirty_index=bool(args.allow_dirty_index),
        )

    interval = max(60, interval)
    while True:
        rc = run_once(
            Path(args.config),
            push,
            push_mode=str(args.push_mode),
            no_verify=bool(args.no_verify),
            plan_only=bool(args.plan),
            proof_dir=proof_dir,
            enforce_status_untracked=enforce_status_untracked,
            plan_max_files=int(args.plan_max_files),
            staged_max_files=int(args.staged_max_files),
            fail_on_dirty=fail_on_dirty,
            allow_dirty_index=bool(args.allow_dirty_index),
        )
        # If an error happens, back off but keep looping.
        if rc != 0:
            _log(f"non-zero rc={rc}; sleeping {interval}s")
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
