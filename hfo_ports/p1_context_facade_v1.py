#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sys

P1_CONTEXT_FACADE_VERSION = "2026-01-23T00:00:00Z"


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _emit(obj: dict) -> None:
    # Strict: prints exactly one JSON object (the baton) and nothing else.
    print(json.dumps(obj, ensure_ascii=False))


def _deadline_from_budget_ms(budget_ms: int) -> float:
    return time.perf_counter() + max(0, budget_ms) / 1000.0


def _check_deadline(deadline: float) -> bool:
    return time.perf_counter() <= deadline


@dataclass(frozen=True)
class ToolResult:
    tool: str
    ok: bool
    duration_ms: int
    items: list
    note: str | None = None


def _tool_result_dict(tr: ToolResult) -> dict:
    out = {
        "tool": tr.tool,
        "ok": tr.ok,
        "duration_ms": tr.duration_ms,
        "items": tr.items,
    }
    if tr.note:
        out["note"] = tr.note
    return out


def _search_contracts(contracts_dir: Path, query: str, *, max_hits: int, deadline: float) -> ToolResult:
    t0 = time.perf_counter()
    hits: list[dict] = []

    if not contracts_dir.exists() or not contracts_dir.is_dir():
        dt = int((time.perf_counter() - t0) * 1000)
        return ToolResult("contracts", False, dt, [], note=f"missing dir: {contracts_dir}")

    q = (query or "").strip().lower()
    for path in sorted(contracts_dir.glob("**/*.ts")):
        if not _check_deadline(deadline):
            break
        try:
            rel = str(path.relative_to(contracts_dir.parent))
        except Exception:
            rel = str(path)

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        if not q:
            continue

        # very lightweight match: scan lines
        for i, line in enumerate(text.splitlines(), start=1):
            if not _check_deadline(deadline):
                break
            if q in line.lower():
                hits.append(
                    {
                        "file": rel,
                        "line": i,
                        "snippet": line.strip()[:240],
                    }
                )
                if len(hits) >= max_hits:
                    break
        if len(hits) >= max_hits:
            break

    dt = int((time.perf_counter() - t0) * 1000)
    return ToolResult("contracts", True, dt, hits)


def run(argv: list[str], repo_root: Path) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("cmd")
    parser.add_argument("--query", required=True)
    parser.add_argument("--time-budget-ms", type=int, default=2500)
    parser.add_argument("--max-hits", type=int, default=12)

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        baton = {
            "schema": "hfo.baton.v1",
            "port": "p1",
            "action": "fuse",
            "status": "FAIL",
            "exit_code": 2,
            "started_utc": _iso_utc_now(),
            "duration_ms": 0,
            "time_budget_ms": None,
            "request": None,
            "tool_results": [],
            "failures": [
                {
                    "tool": "p1-context-facade",
                    "error": "Usage: python3 hfo_hub.py p1 fuse --query <text> [--time-budget-ms N]",
                }
            ],
            "version": P1_CONTEXT_FACADE_VERSION,
        }
        _emit(baton)
        return 2

    started_utc = _iso_utc_now()
    deadline = _deadline_from_budget_ms(int(args.time_budget_ms))
    t0 = time.perf_counter()

    tool_results: list[ToolResult] = []
    failures: list[dict] = []

    contracts_dir = repo_root / "contracts"

    try:
        tr = _search_contracts(contracts_dir, str(args.query), max_hits=int(args.max_hits), deadline=deadline)
        tool_results.append(tr)
        if not tr.ok:
            failures.append({"tool": tr.tool, "error": tr.note or "failed"})
    except Exception as e:
        failures.append({"tool": "contracts", "error": f"exception: {type(e).__name__}: {e}"})

    duration_ms = int((time.perf_counter() - t0) * 1000)

    ok = len(failures) == 0
    baton = {
        "schema": "hfo.baton.v1",
        "port": "p1",
        "action": "fuse",
        "status": "OK" if ok else "FAIL",
        "exit_code": 0 if ok else 3,
        "started_utc": started_utc,
        "duration_ms": duration_ms,
        "time_budget_ms": int(args.time_budget_ms),
        "request": {
            "query": str(args.query),
            "max_hits": int(args.max_hits),
        },
        "tool_results": [_tool_result_dict(tr) for tr in tool_results],
        "failures": failures,
        "version": P1_CONTEXT_FACADE_VERSION,
    }

    _emit(baton)
    return 0 if ok else 3


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    raise SystemExit(run(argv=sys.argv[1:], repo_root=repo_root))
