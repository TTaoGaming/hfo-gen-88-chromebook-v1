#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""HFO Forensics Stress Checker (defensive)

Purpose:
- Mechanically surface brittle points that can "kill" the system:
  - broken append-only logs (JSONL corruption)
  - unsigned / pending signatures
  - missing external dependencies (keys, DuckDB)
  - timestamp format inconsistencies that corrupt causality

This tool is intentionally non-destructive: it never edits state.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


RE_OFFSET_Z = re.compile(r"[+-]\d\d:\d\dZ$")


@dataclass
class Finding:
    severity: str  # INFO | WARN | FAIL
    code: str
    message: str
    source: str | None = None


def iter_jsonl(path: Path) -> Iterable[tuple[int, str]]:
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            s = line.strip("\n")
            if not s.strip():
                continue
            yield idx, s


def parse_jsonl(path: Path, label: str) -> tuple[list[Finding], int, int]:
    findings: list[Finding] = []
    ok = 0
    bad = 0

    if not path.exists():
        return [Finding("FAIL", "MISSING_FILE", f"Missing {label}: {path}", str(path))], 0, 0

    for line_no, raw in iter_jsonl(path):
        try:
            obj = json.loads(raw)
            ok += 1
        except Exception as e:
            bad += 1
            preview = raw[:160].replace("\t", " ")
            findings.append(
                Finding(
                    "FAIL",
                    "JSONL_PARSE",
                    f"Invalid JSON at {label} line {line_no}: {e} | preview={preview!r}",
                    str(path),
                )
            )
            continue

        # Generic timestamp sanity checks
        ts = obj.get("timestamp") or obj.get("ts")
        if isinstance(ts, str) and RE_OFFSET_Z.search(ts):
            findings.append(
                Finding(
                    "WARN",
                    "TS_OFFSET_Z",
                    f"Timestamp has offset plus trailing 'Z' (ambiguous): {ts}",
                    str(path),
                )
            )

        sig = obj.get("signature")
        if sig == "pending":
            findings.append(
                Finding(
                    "FAIL",
                    "SIGNATURE_PENDING",
                    f"Found signature='pending' at {label} line {line_no}",
                    str(path),
                )
            )

        # Blackboard-specific tripwire scan
        phase = obj.get("phase")
        if phase == "TOOL_TRIPWIRE" and obj.get("status") == "FAIL":
            tool = obj.get("tool", "(unknown)")
            details = obj.get("details", "")
            findings.append(
                Finding(
                    "WARN",
                    "TRIPWIRE_FAIL",
                    f"TOOL_TRIPWIRE FAIL: tool={tool} details={details}",
                    str(path),
                )
            )

    if bad == 0:
        findings.append(Finding("INFO", "JSONL_OK", f"{label} JSONL parse OK ({ok} entries)", str(path)))

    return findings, ok, bad


def extract_constant_from_file(path: Path, name: str) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(rf"^{re.escape(name)}\s*=\s*\"([^\"]+)\"", text, flags=re.MULTILINE)
    return m.group(1) if m else None


def check_env_keys() -> list[Finding]:
    findings: list[Finding] = []
    for key in ("TAVILY_API_KEY", "OPENROUTER_API_KEY"):
        if os.environ.get(key):
            findings.append(Finding("INFO", "ENV_OK", f"Env var present: {key}"))
        else:
            findings.append(Finding("WARN", "ENV_MISSING", f"Env var missing: {key}"))
    return findings


def check_duckdb_path(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    sentinel = repo_root / "scripts" / "p5_sentinel_daemon.py"
    duckdb_path = extract_constant_from_file(sentinel, "DUCKDB_PATH")

    if not duckdb_path:
        return [Finding("WARN", "DUCKDB_PATH_UNKNOWN", "Could not extract DUCKDB_PATH from p5_sentinel_daemon.py", str(sentinel))]

    p = Path(duckdb_path)
    if not p.exists():
        findings.append(Finding("WARN", "DUCKDB_MISSING", f"DuckDB file missing at DUCKDB_PATH: {p}", str(sentinel)))
        return findings

    try:
        sz = p.stat().st_size
        if sz <= 0:
            findings.append(Finding("WARN", "DUCKDB_EMPTY", f"DuckDB file exists but size is 0: {p}", str(sentinel)))
        else:
            findings.append(Finding("INFO", "DUCKDB_OK", f"DuckDB file exists: {p} ({sz} bytes)", str(sentinel)))
    except Exception as e:
        findings.append(Finding("WARN", "DUCKDB_STAT_FAIL", f"DuckDB stat failed: {e}", str(sentinel)))

    return findings


def check_zod_governance(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []

    cold_start = repo_root / "COLD_START.md"
    pkg = repo_root / "package.json"

    if cold_start.exists():
        text = cold_start.read_text(encoding="utf-8", errors="replace")
        if "Zod 6.0" in text or "Zod 6" in text:
            findings.append(Finding("INFO", "DOCTRINE_ZOD6", "Doctrine references Zod 6.0", str(cold_start)))

    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            zod_ver = (data.get("dependencies") or {}).get("zod")
            if zod_ver:
                findings.append(Finding("INFO", "PKG_ZOD", f"package.json declares zod={zod_ver}", str(pkg)))
                if "6" in str(zod_ver):
                    findings.append(Finding("INFO", "ZOD_MATCH", "Zod major version appears aligned with doctrine", str(pkg)))
                else:
                    findings.append(Finding("WARN", "ZOD_MISMATCH", "Doctrine references Zod 6.0 but package.json declares a different Zod version", str(pkg)))
        except Exception as e:
            findings.append(Finding("WARN", "PKG_PARSE_FAIL", f"Failed to parse package.json: {e}", str(pkg)))

    return findings


def summarize(findings: list[Finding]) -> tuple[int, int, int]:
    info = sum(1 for f in findings if f.severity == "INFO")
    warn = sum(1 for f in findings if f.severity == "WARN")
    fail = sum(1 for f in findings if f.severity == "FAIL")
    return info, warn, fail


def main() -> int:
    ap = argparse.ArgumentParser(description="HFO defensive forensics stress checker")
    ap.add_argument("--blackboard", default="hfo_hot_obsidian/hot_obsidian_blackboard.jsonl")
    ap.add_argument("--memory", default="hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    findings: list[Finding] = []

    bb_path = (repo_root / args.blackboard).resolve()
    mem_path = (repo_root / args.memory).resolve()

    bb_findings, _, _ = parse_jsonl(bb_path, "blackboard")
    mem_findings, _, _ = parse_jsonl(mem_path, "mcp_memory")

    findings.extend(bb_findings)
    findings.extend(mem_findings)
    findings.extend(check_env_keys())
    findings.extend(check_duckdb_path(repo_root))
    findings.extend(check_zod_governance(repo_root))

    # Print
    info, warn, fail = summarize(findings)
    exit_code = 1 if fail > 0 else 0

    try:
        print("HFO Forensics Stress Check")
        print(f"Repo: {repo_root}")
        print(f"Blackboard: {bb_path}")
        print(f"MCP memory: {mem_path}")
        print(f"Findings: INFO={info} WARN={warn} FAIL={fail}")
        print("-")

        # Show FAIL then WARN
        for sev in ("FAIL", "WARN"):
            for f in findings:
                if f.severity != sev:
                    continue
                src = f" src={f.source}" if f.source else ""
                print(f"[{f.severity}] {f.code}: {f.message}{src}")
    except BrokenPipeError:
        # Allow piping to `head`/`tail` without stack traces.
        try:
            sys.stdout.close()
        except Exception:
            pass
        return exit_code

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
