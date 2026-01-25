#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""HFO System Budget helper (Pareto stability).

Purpose
- Provide a single, cheap way to detect low-memory pressure and a user-toggleable
  "pareto mode" that asks background daemons to back off.

Notes
- Reads only /proc/meminfo and a small JSON state file under .hfo_runtime.
- Designed to be safe to import from long-running daemons.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PARETO_STATE_PATH = REPO_ROOT / ".hfo_runtime" / "pareto_mode.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_meminfo_kb() -> dict[str, int]:
    out: dict[str, int] = {}
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if ":" not in line:
                continue
            k, rest = line.split(":", 1)
            rest = rest.strip()
            parts = rest.split()
            if not parts:
                continue
            try:
                out[k] = int(parts[0])
            except ValueError:
                continue
    except Exception:
        pass
    return out


def mem_available_kb() -> int:
    return int(read_meminfo_kb().get("MemAvailable", 0) or 0)


def mem_total_kb() -> int:
    return int(read_meminfo_kb().get("MemTotal", 0) or 0)


def _env_float(key: str, default: float) -> float:
    raw = os.environ.get(key)
    if not raw:
        return float(default)
    try:
        return float(raw)
    except Exception:
        return float(default)


def low_ram_threshold_kb() -> int:
    # Default: if MemAvailable < 1.25 GiB, ask daemons to back off.
    gib = _env_float("HFO_LOW_RAM_AVAILABLE_GIB", 1.25)
    return int(max(0.25, gib) * 1024 * 1024)


def is_low_ram() -> bool:
    avail = mem_available_kb()
    if avail <= 0:
        return False
    return avail < low_ram_threshold_kb()


def set_pareto_mode(enabled: bool, *, note: str = "") -> dict:
    state = {
        "type": "hfo_pareto_mode",
        "enabled": bool(enabled),
        "updated_utc": _now_iso(),
        "note": str(note or ""),
    }
    PARETO_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PARETO_STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    return state


def get_pareto_state() -> dict:
    try:
        if not PARETO_STATE_PATH.exists():
            return {"enabled": False}
        data = json.loads(PARETO_STATE_PATH.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
        return {"enabled": False}
    except Exception:
        return {"enabled": False}


def is_pareto_enabled() -> bool:
    if os.environ.get("HFO_PARETO", "0") in {"1", "true", "TRUE"}:
        return True
    st = get_pareto_state()
    return bool(st.get("enabled"))


@dataclass(frozen=True)
class BudgetSnapshot:
    ts_utc: str
    mem_total_kb: int
    mem_available_kb: int
    low_ram: bool
    low_ram_threshold_kb: int
    pareto_enabled: bool
    reason: str


@dataclass(frozen=True)
class ThrottleProfile:
    ts_utc: str
    cpu_count: int
    load1: float | None
    load5: float | None
    load15: float | None
    mem_total_kb: int
    mem_available_kb: int
    pareto_enabled: bool
    low_ram_threshold_kb: int
    # ok: no throttling; soft: rate-limit heavy work; hard: skip heavy work
    level: str
    # 1.0 = normal cadence; >1 increases sleeps/backoff windows.
    sleep_multiplier: float
    reason: str


_CACHE: BudgetSnapshot | None = None
_CACHE_UNTIL: float = 0.0


def get_budget_snapshot(ttl_sec: float = 2.0) -> BudgetSnapshot:
    global _CACHE, _CACHE_UNTIL
    now = time.time()
    if _CACHE is not None and now < _CACHE_UNTIL:
        return _CACHE

    total = mem_total_kb()
    avail = mem_available_kb()
    thr = low_ram_threshold_kb()
    low = (avail > 0 and avail < thr)
    pareto = is_pareto_enabled()
    reason = "pareto_mode" if pareto else ("low_ram" if low else "ok")
    snap = BudgetSnapshot(
        ts_utc=_now_iso(),
        mem_total_kb=total,
        mem_available_kb=avail,
        low_ram=bool(low),
        low_ram_threshold_kb=int(thr),
        pareto_enabled=bool(pareto),
        reason=reason,
    )
    _CACHE = snap
    _CACHE_UNTIL = now + max(0.1, float(ttl_sec))
    return snap


def should_backoff() -> bool:
    s = get_budget_snapshot()
    return bool(s.pareto_enabled or s.low_ram)


def _env_float_default(key: str, default: float) -> float:
    raw = os.environ.get(key)
    if not raw:
        return float(default)
    try:
        return float(raw)
    except Exception:
        return float(default)


def _get_loadavg() -> tuple[float, float, float] | None:
    try:
        return os.getloadavg()
    except Exception:
        return None


def _cpu_count() -> int:
    try:
        n = os.cpu_count() or 0
        return int(n) if n > 0 else 1
    except Exception:
        return 1


def _kb_from_gib(gib: float) -> int:
    return int(max(0.0, float(gib)) * 1024 * 1024)


def pareto_sweet_spot_available_gib() -> tuple[float, float]:
    """Return (soft_floor_gib, hard_floor_gib) for MemAvailable.

    - hard: below hard_floor_gib, skip heavy work.
    - soft: below soft_floor_gib, rate-limit heavy work.

    Defaults tuned for 6–8GiB VM environments.
    """

    soft = _env_float_default("HFO_PARETO_SOFT_AVAIL_GIB", 2.0)
    hard = _env_float_default("HFO_PARETO_HARD_AVAIL_GIB", 1.25)
    if hard > soft:
        hard = soft
    return float(soft), float(hard)


def get_throttle_profile(ttl_sec: float = 2.0) -> ThrottleProfile:
    snap = get_budget_snapshot(ttl_sec=ttl_sec)
    cpu = _cpu_count()
    la = _get_loadavg()
    load1, load5, load15 = (la if la else (None, None, None))

    soft_gib, hard_gib = pareto_sweet_spot_available_gib()
    soft_kb = _kb_from_gib(soft_gib)
    hard_kb = _kb_from_gib(hard_gib)

    level = "ok"
    reason = "ok"

    avail = int(snap.mem_available_kb)
    if avail > 0 and avail < hard_kb:
        level = "hard"
        reason = "low_mem_hard"
    elif avail > 0 and avail < soft_kb:
        level = "soft"
        reason = "low_mem_soft"

    # Load-based damping: if already CPU-saturated, gently increase throttling.
    load_ratio = None
    if load1 is not None and cpu > 0:
        load_ratio = float(load1) / float(cpu)
        if load_ratio >= _env_float_default("HFO_PARETO_LOAD_HARD_RATIO", 1.1):
            level = "hard" if level != "hard" else level
            reason = "cpu_saturated"
        elif load_ratio >= _env_float_default("HFO_PARETO_LOAD_SOFT_RATIO", 0.9) and level == "ok":
            level = "soft"
            reason = "cpu_busy"

    # Pareto mode means: always use adaptive cadence (but don't slow down if ok).
    if snap.pareto_enabled and level == "ok":
        reason = "pareto_ok"

    # Sweet spot cadence: ok=1.0, soft ramps 1.5–3.0, hard ramps 3.0–6.0.
    if level == "ok":
        mult = 1.0
    elif level == "soft":
        # The closer to hard_kb, the higher the multiplier.
        if avail <= 0 or soft_kb <= hard_kb:
            mult = 2.0
        else:
            t = (soft_kb - max(avail, hard_kb)) / float(max(1, soft_kb - hard_kb))
            mult = 1.5 + 1.5 * max(0.0, min(1.0, t))
    else:
        if avail <= 0:
            mult = 4.0
        else:
            t = (hard_kb - max(avail, 0)) / float(max(1, hard_kb))
            mult = 3.0 + 3.0 * max(0.0, min(1.0, t))

    return ThrottleProfile(
        ts_utc=snap.ts_utc,
        cpu_count=cpu,
        load1=load1,
        load5=load5,
        load15=load15,
        mem_total_kb=snap.mem_total_kb,
        mem_available_kb=snap.mem_available_kb,
        pareto_enabled=snap.pareto_enabled,
        low_ram_threshold_kb=snap.low_ram_threshold_kb,
        level=level,
        sleep_multiplier=float(mult),
        reason=reason,
    )


def should_skip_heavy_work() -> bool:
    p = get_throttle_profile(ttl_sec=2.0)
    return p.level == "hard"


def recommended_sleep_seconds(base_seconds: float, *, kind: str = "medium") -> float:
    """Return a scaled sleep duration based on throttle profile.

    kind: light|medium|heavy applies extra multiplier in soft/hard states.
    """

    base = max(0.0, float(base_seconds))
    p = get_throttle_profile(ttl_sec=2.0)
    if p.level == "ok":
        return base

    kind = (kind or "medium").lower()
    extra = 1.0
    if kind == "heavy":
        extra = 1.5 if p.level == "soft" else 2.0
    elif kind == "light":
        extra = 1.1 if p.level == "soft" else 1.25

    return base * p.sleep_multiplier * extra


def should_force_low_ram_for_playwright() -> bool:
    """Playwright is bursty; be conservative under pareto or soft/hard states."""

    p = get_throttle_profile(ttl_sec=2.0)
    return bool(p.pareto_enabled or p.level in {"soft", "hard"})


def main() -> int:
    ap = argparse.ArgumentParser(description="HFO system budget / pareto mode helper")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("status", help="Print current budget snapshot as JSON")
    p_on = sub.add_parser("on", help="Enable pareto mode")
    p_on.add_argument("--note", default="")
    p_off = sub.add_parser("off", help="Disable pareto mode")
    p_off.add_argument("--note", default="")

    args = ap.parse_args()
    cmd = (args.cmd or "status").lower()

    if cmd == "on":
        st = set_pareto_mode(True, note=getattr(args, "note", ""))
        print(json.dumps(st, indent=2, sort_keys=True))
        return 0
    if cmd == "off":
        st = set_pareto_mode(False, note=getattr(args, "note", ""))
        print(json.dumps(st, indent=2, sort_keys=True))
        return 0

    p = get_throttle_profile(ttl_sec=0.0)
    print(
        json.dumps(
            {
                "ts_utc": p.ts_utc,
                "cpu_count": p.cpu_count,
                "loadavg": [p.load1, p.load5, p.load15],
                "mem_total_kb": p.mem_total_kb,
                "mem_available_kb": p.mem_available_kb,
                "low_ram_threshold_kb": p.low_ram_threshold_kb,
                "pareto_enabled": p.pareto_enabled,
                "throttle_level": p.level,
                "sleep_multiplier": p.sleep_multiplier,
                "reason": p.reason,
                "pareto_state_path": str(PARETO_STATE_PATH),
                "platform": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "machine": platform.machine(),
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
