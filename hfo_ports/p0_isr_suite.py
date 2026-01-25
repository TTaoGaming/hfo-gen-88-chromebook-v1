#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone

P0_ISR_SUITE_VERSION = "2026-01-23T17:15:20Z"


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _run_capture(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return int(proc.returncode), out


def _git_porcelain(cwd: Path) -> list[str]:
    code, out = _run_capture(["git", "status", "--porcelain"], cwd)
    if code != 0:
        return []
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return lines


def _is_allowed_write(path: str) -> bool:
    # P0 may write reports (and only reports) by default.
    # Keep this conservative.
    if path.startswith("hfo_hot_obsidian/") and "/reports/" in path:
        return True
    return False


@dataclass(frozen=True)
class SuiteResult:
    ok: bool
    report_path: str


def run(argv: list[str], repo_root: Path) -> int:
    sub = argv[0].lower() if argv else ""
    if sub not in {"suite", "isr_suite", "report"}:
        print("Usage: python3 hfo_hub.py p0 suite")
        return 2

    # Pre-snapshot repo dirty state (for delta detection).
    before = _git_porcelain(repo_root)

    # Run tracer in both strict and allowed-optional modes.
    strict_code, strict_out = _run_capture(["python3", "hfo_hub.py", "p3", "tracer"], repo_root)
    allow_env = dict(os.environ)
    allow_env["HFO_ALLOW_OPTIONAL_MCP"] = allow_env.get("HFO_ALLOW_OPTIONAL_MCP", "1")
    allow_code, allow_out = subprocess.run(
        ["python3", "hfo_hub.py", "p3", "tracer"],
        cwd=str(repo_root),
        env=allow_env,
        capture_output=True,
        text=True,
    ).returncode, ""
    # Reconstruct allow_out without re-running
    # (capture_output above already captured; fetch from the CompletedProcess by re-running in a safe way)
    proc = subprocess.run(
        ["python3", "hfo_hub.py", "p3", "tracer"],
        cwd=str(repo_root),
        env=allow_env,
        capture_output=True,
        text=True,
    )
    allow_code = int(proc.returncode)
    allow_out = (proc.stdout or "") + (proc.stderr or "")

    # Write a timestamped report (this is the only allowed write).
    ts = _iso_utc_now().replace(":", "_")
    rel_report = f"hfo_hot_obsidian/bronze/3_resources/reports/P0_ISR_SUITE_REPORT_{ts}.md"
    report_path = repo_root / rel_report
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report = []
    report.append("# Medallion: Bronze | Mutation: 0% | HIVE: V\n")
    report.append(f"# P0 ISR Suite Report (Lidless Legion) — {ts}\n")
    report.append(f"**Suite version:** {P0_ISR_SUITE_VERSION}\n")
    report.append("## Goals\n")
    report.append("- Verify P0 is observation-only (read-only operations + allowed report write).\n")
    report.append("- Verify the 8-shard observation toolchain health via tracer_venom.\n")

    report.append("## Tracer Venom Results\n")
    report.append("### Strict mode (exactly-8 invariant)\n")
    report.append(f"Exit: {strict_code}\n\n")
    report.append("```\n" + strict_out.strip() + "\n```\n")

    report.append("### Allowed-optional mode (HFO_ALLOW_OPTIONAL_MCP=1)\n")
    report.append(f"Exit: {allow_code}\n\n")
    report.append("```\n" + allow_out.strip() + "\n```\n")

    report.append("## Read-Only Invariant Check\n")
    report.append("This suite only performs reads and network probes, then writes this report file.\n")

    after = _git_porcelain(repo_root)

    report.append("### Git status before\n")
    report.append("```\n" + "\n".join(before) + ("\n" if before else "") + "```\n")
    report.append("### Git status after\n")
    report.append("```\n" + "\n".join(after) + ("\n" if after else "") + "```\n")

    # Detect newly introduced changes beyond allowed report write.
    new_lines = [ln for ln in after if ln not in before]
    introduced = []
    for ln in new_lines:
        # format: XY path
        path = ln[3:] if len(ln) > 3 else ""
        if path and not _is_allowed_write(path):
            introduced.append(ln)

    if introduced:
        report.append("### Invariant: FAIL\n")
        report.append("New changes detected outside allowed report paths:\n")
        report.append("```\n" + "\n".join(introduced) + "\n```\n")
    else:
        report.append("### Invariant: OK\n")
        report.append("No new changes detected outside allowed report paths.\n")

    report_path.write_text("\n".join(report), encoding="utf-8")

    ok = (allow_code == 0) and (len(introduced) == 0)

    print(f"[HFO HUB] P0 suite report -> {rel_report}")
    print(f"[HFO HUB] P0 suite: {'OK' if ok else 'FAIL'}")
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(run(os.sys.argv[1:], Path(__file__).resolve().parents[1]))
