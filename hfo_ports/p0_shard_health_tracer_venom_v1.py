#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

P0_SHARD_HEALTH_TRACER_VENOM_VERSION = "2026-01-23T00:00:00Z"


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _emit(obj: dict) -> None:
    # Strict: exactly one JSON object printed.
    print(json.dumps(obj, ensure_ascii=False))


@dataclass(frozen=True)
class ShardResult:
    shard: str
    ok: bool
    duration_ms: int
    evidence: list[str]
    note: str | None = None


def _sr_dict(sr: ShardResult) -> dict:
    d = {
        "tool": sr.shard,
        "ok": sr.ok,
        "duration_ms": sr.duration_ms,
        "evidence": sr.evidence,
    }
    if sr.note:
        d["note"] = sr.note
    return d


def _read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _check_env_key(name: str) -> ShardResult:
    t0 = time.perf_counter()
    ok = bool(os.environ.get(name))
    dt = int((time.perf_counter() - t0) * 1000)
    return ShardResult(f"env:{name}", ok, dt, [f"present:{name}" if ok else f"missing:{name}"], note="presence-only")


def _check_file_exists(label: str, path: Path) -> ShardResult:
    t0 = time.perf_counter()
    ok = path.exists()
    dt = int((time.perf_counter() - t0) * 1000)
    return ShardResult(label, ok, dt, [str(path)], note="exists" if ok else "missing")


def _check_mcp_inventory(repo_root: Path) -> tuple[ShardResult, list[dict]]:
    t0 = time.perf_counter()
    failures: list[dict] = []

    mcp_path = repo_root / ".vscode" / "mcp.json"
    if not mcp_path.exists():
        dt = int((time.perf_counter() - t0) * 1000)
        failures.append({"tool": "mcp_inventory", "error": "missing .vscode/mcp.json"})
        return ShardResult("mcp_inventory", False, dt, [str(mcp_path)], note="missing"), failures

    obj = _read_json(mcp_path)
    servers = {}
    if isinstance(obj, dict):
        servers = obj.get("servers", {})
    if not isinstance(servers, dict):
        servers = {}

    canonical_8 = [
        "filesystem",
        "memory",
        "sequential-thinking",
        "time",
        "tavily",
        "brave-search",
        "playwright",
        "hfo_mcp_gateway_hub",
    ]
    optional = {"context7", "omnisearch"}

    present = set(str(k) for k in servers.keys())
    missing = [x for x in canonical_8 if x not in present]
    extra = sorted([x for x in present if x not in set(canonical_8) and x not in optional])

    allow_optional = os.environ.get("HFO_ALLOW_OPTIONAL_MCP", "0") in {"1", "true", "TRUE"}
    ok = (len(missing) == 0) and (allow_optional or len(extra) == 0)

    evidence = [str(mcp_path)]
    evidence.append("present:" + ",".join(sorted(present)))
    if missing:
        failures.append({"tool": "mcp_inventory", "error": f"missing_canonical:{','.join(missing)}"})
    if extra and not allow_optional:
        failures.append({"tool": "mcp_inventory", "error": f"extra_noncanonical:{','.join(extra)}"})

    dt = int((time.perf_counter() - t0) * 1000)
    note = f"missing={len(missing)} extra={len(extra)} allow_optional={allow_optional}"
    return ShardResult("mcp_inventory", ok, dt, evidence, note=note), failures


def _check_pointers(repo_root: Path) -> tuple[ShardResult, list[dict]]:
    t0 = time.perf_counter()
    failures: list[dict] = []

    pointers = repo_root / "hfo_pointers.json"
    obj = _read_json(pointers)
    if not isinstance(obj, dict):
        dt = int((time.perf_counter() - t0) * 1000)
        failures.append({"tool": "pointers", "error": "missing_or_invalid_json"})
        return ShardResult("pointers", False, dt, [str(pointers)], note="invalid"), failures

    targets = obj.get("targets", {})
    paths = obj.get("paths", {})

    required_target_keys = [
        "mcp_gateway_impl",
        "p0_context_facade_impl",
        "p1_context_facade_impl",
    ]
    missing_targets = [k for k in required_target_keys if not (isinstance(targets, dict) and targets.get(k))]

    required_path_keys = ["blackboard", "mcp_memory"]
    missing_paths = [k for k in required_path_keys if not (isinstance(paths, dict) and paths.get(k))]

    evidence = [str(pointers)]
    ok = (len(missing_targets) == 0) and (len(missing_paths) == 0)
    if missing_targets:
        failures.append({"tool": "pointers", "error": f"missing_targets:{','.join(missing_targets)}"})
    if missing_paths:
        failures.append({"tool": "pointers", "error": f"missing_paths:{','.join(missing_paths)}"})

    # existence checks for the resolved paths (best-effort)
    if isinstance(paths, dict):
        for k in required_path_keys:
            v = paths.get(k)
            if isinstance(v, str) and v:
                p = repo_root / v
                if not p.exists():
                    ok = False
                    failures.append({"tool": "pointers", "error": f"path_not_found:{k}:{v}"})
                    evidence.append(f"missing:{v}")

    dt = int((time.perf_counter() - t0) * 1000)
    note = f"missing_targets={len(missing_targets)} missing_paths={len(missing_paths)}"
    return ShardResult("pointers", ok, dt, evidence, note=note), failures


def run(argv: list[str], repo_root: Path) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("cmd")
    parser.add_argument("--query", required=True)
    parser.add_argument("--time-budget-ms", type=int, default=1500)
    parser.add_argument("--strict", action="store_true")

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        baton = {
            "schema": "hfo.baton.v1",
            "port": "p0",
            "action": "tracer",
            "status": "FAIL",
            "exit_code": 2,
            "started_utc": _iso_utc_now(),
            "duration_ms": 0,
            "time_budget_ms": None,
            "request": None,
            "tool_results": [],
            "failures": [
                {
                    "tool": "p0-shard-health",
                    "error": "Usage: python3 hfo_hub.py p0 tracer --query <text> [--time-budget-ms N]",
                }
            ],
            "version": P0_SHARD_HEALTH_TRACER_VENOM_VERSION,
        }
        _emit(baton)
        return 2

    started_utc = _iso_utc_now()
    t0 = time.perf_counter()

    shard_results: list[ShardResult] = []
    failures: list[dict] = []

    # Deterministic inventory checks (local only)
    mcp_sr, mcp_fail = _check_mcp_inventory(repo_root)
    shard_results.append(mcp_sr)
    failures.extend(mcp_fail)

    ptr_sr, ptr_fail = _check_pointers(repo_root)
    shard_results.append(ptr_sr)
    failures.extend(ptr_fail)

    # Presence-only key checks (do not attempt network probes)
    shard_results.append(_check_env_key("BRAVE_API_KEY"))
    shard_results.append(_check_env_key("TAVILY_API_KEY"))
    shard_results.append(_check_env_key("OPENROUTER_API_KEY"))

    for sr in shard_results[-3:]:
        if not sr.ok:
            failures.append({"tool": sr.shard, "error": "missing"})

    # Existence checks for key local files
    shard_results.append(_check_file_exists("file:hfo_hub.py", repo_root / "hfo_hub.py"))
    shard_results.append(_check_file_exists("file:contracts_dir", repo_root / "contracts"))

    for sr in shard_results[-2:]:
        if not sr.ok:
            failures.append({"tool": sr.shard, "error": sr.note or "missing"})

    duration_ms = int((time.perf_counter() - t0) * 1000)

    ok = len(failures) == 0
    status = "OK" if ok else "FAIL"

    baton = {
        "schema": "hfo.baton.v1",
        "port": "p0",
        "action": "tracer",
        "status": status,
        "exit_code": 0 if ok else 3,
        "started_utc": started_utc,
        "duration_ms": duration_ms,
        "time_budget_ms": int(args.time_budget_ms),
        "request": {
            "query": str(args.query),
            "mode": "shard-health",
            "strict": bool(args.strict),
        },
        "tool_results": [_sr_dict(sr) for sr in shard_results],
        "failures": failures,
        "version": P0_SHARD_HEALTH_TRACER_VENOM_VERSION,
    }

    _emit(baton)
    return 0 if ok else 3


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    raise SystemExit(run(argv=os.sys.argv[1:], repo_root=repo_root))
