#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""HFO Healthcheck (fail-loud, repo-grounded)

Goals
- One command to evaluate system health and stop silent breakage.
- Works offline; never mutates state.
- Can run in two modes:
  - soft: exit 0, but reports problems (for dashboards/quick eval)
  - hard: exit non-zero if any FAIL conditions (for gates/preflight)

Primary signals (grounded in repo patterns)
- JSONL integrity (blackboard + MCP memory)
- signature == 'pending' (integrity not finalized)
- TOOL_TRIPWIRE FAIL entries (dependencies degraded)
- missing env vars (tavily/openrouter)
- DuckDB path existence (from p5_sentinel_daemon.py)
- timestamp ambiguity pattern '+00:00Z'

This does not attempt to "repair" anything.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


RE_OFFSET_Z = re.compile(r"[+-]\d\d:\d\dZ$")


@dataclass
class Counters:
    jsonl_parse_errors: int = 0
    pending_signatures: int = 0
    tripwire_fails: int = 0
    timestamp_ambiguities: int = 0


def iter_jsonl(path: Path) -> Iterable[tuple[int, str]]:
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            s = line.strip("\n")
            if not s.strip():
                continue
            yield idx, s


def scan_jsonl(path: Path, label: str) -> tuple[Counters, Dict[str, Any]]:
    counters = Counters()
    details: Dict[str, Any] = {
        "label": label,
        "path": str(path),
        "pending_signature_lines": [],
        "parse_error_lines": [],
        "tripwire_fail_tools": {},
    }

    if not path.exists():
        counters.jsonl_parse_errors += 1
        details["missing"] = True
        return counters, details

    for line_no, raw in iter_jsonl(path):
        try:
            obj = json.loads(raw)
        except Exception:
            counters.jsonl_parse_errors += 1
            if len(details["parse_error_lines"]) < 10:
                details["parse_error_lines"].append(line_no)
            continue

        ts = obj.get("timestamp") or obj.get("ts")
        if isinstance(ts, str) and RE_OFFSET_Z.search(ts):
            counters.timestamp_ambiguities += 1

        sig = obj.get("signature")
        if sig == "pending":
            counters.pending_signatures += 1
            if len(details["pending_signature_lines"]) < 20:
                details["pending_signature_lines"].append(line_no)

        if obj.get("phase") == "TOOL_TRIPWIRE" and obj.get("status") == "FAIL":
            counters.tripwire_fails += 1
            tool = str(obj.get("tool", "(unknown)"))
            details["tripwire_fail_tools"][tool] = details["tripwire_fail_tools"].get(tool, 0) + 1

    return counters, details


def extract_constant_from_file(path: Path, name: str) -> Optional[str]:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(rf"^{re.escape(name)}\s*=\s*\"([^\"]+)\"", text, flags=re.MULTILINE)
    return m.group(1) if m else None


def build_report(repo_root: Path, blackboard_rel: str, memory_rel: str) -> Dict[str, Any]:
    blackboard_path = (repo_root / blackboard_rel).resolve()
    memory_path = (repo_root / memory_rel).resolve()

    bb_counts, bb_details = scan_jsonl(blackboard_path, "blackboard")
    mem_counts, mem_details = scan_jsonl(memory_path, "mcp_memory")

    env_required = ["TAVILY_API_KEY", "OPENROUTER_API_KEY"]
    env_missing = [k for k in env_required if not os.environ.get(k)]

    sentinel_path = repo_root / "scripts" / "p5_sentinel_daemon.py"
    duckdb_path_str = extract_constant_from_file(sentinel_path, "DUCKDB_PATH")
    duckdb_exists = None
    duckdb_size = None
    if duckdb_path_str:
        p = Path(duckdb_path_str)
        duckdb_exists = p.exists()
        if duckdb_exists:
            try:
                duckdb_size = p.stat().st_size
            except Exception:
                duckdb_size = None

    report = {
        "repo": str(repo_root),
        "signals": {
            "blackboard": {
                "counters": bb_counts.__dict__,
                "details": bb_details,
            },
            "mcp_memory": {
                "counters": mem_counts.__dict__,
                "details": mem_details,
            },
        },
        "deps": {
            "env_required": env_required,
            "env_missing": env_missing,
            "duckdb_path": duckdb_path_str,
            "duckdb_exists": duckdb_exists,
            "duckdb_size": duckdb_size,
        },
    }

    # Derived severities
    fail_reasons = []
    if bb_counts.jsonl_parse_errors or mem_counts.jsonl_parse_errors:
        fail_reasons.append("jsonl_parse_errors")
    if bb_counts.pending_signatures:
        fail_reasons.append("pending_signatures")

    warn_reasons = []
    if bb_counts.tripwire_fails:
        warn_reasons.append("tool_tripwire_fails")
    if bb_counts.timestamp_ambiguities:
        warn_reasons.append("timestamp_ambiguities")
    if env_missing:
        warn_reasons.append("missing_env")
    if duckdb_exists is False:
        warn_reasons.append("duckdb_missing")

    report["summary"] = {
        "fail": bool(fail_reasons),
        "fail_reasons": fail_reasons,
        "warn": bool(warn_reasons),
        "warn_reasons": warn_reasons,
    }

    return report


def print_human(report: Dict[str, Any]) -> None:
    s = report["summary"]
    bb = report["signals"]["blackboard"]["counters"]
    deps = report["deps"]

    print("HFO Healthcheck")
    print(f"Repo: {report['repo']}")
    print(f"FAIL={s['fail']} WARN={s['warn']}")
    if s["fail_reasons"]:
        print(f"Fail reasons: {', '.join(s['fail_reasons'])}")
    if s["warn_reasons"]:
        print(f"Warn reasons: {', '.join(s['warn_reasons'])}")

    print("-")
    print(
        "Blackboard counters: "
        f"parse_errors={bb['jsonl_parse_errors']} "
        f"pending_signatures={bb['pending_signatures']} "
        f"tripwire_fails={bb['tripwire_fails']} "
        f"timestamp_ambiguities={bb['timestamp_ambiguities']}"
    )

    if deps["env_missing"]:
        print(f"Missing env: {', '.join(deps['env_missing'])}")
    if deps["duckdb_exists"] is False:
        print(f"DuckDB missing: {deps['duckdb_path']}")


def main() -> int:
    ap = argparse.ArgumentParser(description="HFO healthcheck (fail-loud)")
    ap.add_argument("--mode", choices=["soft", "hard"], default="soft")
    ap.add_argument("--format", choices=["human", "json"], default="human")
    ap.add_argument("--blackboard", default="hfo_hot_obsidian/hot_obsidian_blackboard.jsonl")
    ap.add_argument("--memory", default="hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    report = build_report(repo_root, args.blackboard, args.memory)

    exit_code = 0
    if args.mode == "hard" and report["summary"]["fail"]:
        exit_code = 2

    try:
        if args.format == "json":
            print(json.dumps(report, sort_keys=True))
        else:
            print_human(report)
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
