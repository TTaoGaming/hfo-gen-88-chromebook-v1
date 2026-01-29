#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Port 6 (Kraken Keeper) — Bronze progressive rollup (non-destructive).

Goal
- Produce a *bounded*, high-signal daily rollup from Hot Bronze ledgers:
  - hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
  - hfo_hot_obsidian/hot_obsidian_blackboard.jsonl

Non-destructive invariants
- Never mutates source ledgers.
- Writes rollup output into Hot Silver.
- Optionally appends a small status_update to MCP memory to record the proof.

This script is intentionally streaming/bounded to avoid OOM on small machines.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def _now_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


@dataclass(frozen=True)
class ScanLimits:
    max_status_updates: int
    max_blackboard_events: int


def _iter_jsonl(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except Exception:
                continue
            if isinstance(obj, dict):
                yield idx, obj


def _path_stat(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False}
    try:
        st = path.stat()
        return {
            "path": str(path),
            "exists": True,
            "size_bytes": int(st.st_size),
            "modified_utc": datetime.fromtimestamp(st.st_mtime, timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        }
    except Exception as e:
        return {"path": str(path), "exists": True, "error": f"{type(e).__name__}: {e}"}


def _ts_matches_day(ts: Any, iso_day: str) -> bool:
    return isinstance(ts, str) and ts.startswith(iso_day)


def _classify_blackboard_event(ev: dict[str, Any]) -> str | None:
    phase = str(ev.get("phase") or "")
    status = str(ev.get("status") or "")

    # High-signal: explicit failures/breaches.
    if status in {"FAIL", "BREACH"}:
        return "high"

    # High-signal phases we care about at Bronze level.
    if phase in {"TOOL_TRIPWIRE", "WATCH_SENTINEL"}:
        return "high"

    return None


def build_bronze_rollup(
    *,
    iso_day: str,
    repo_root: Path,
    memory_path: Path,
    blackboard_path: Path,
    limits: ScanLimits,
) -> dict[str, Any]:
    mem_stat = _path_stat(memory_path)
    bb_stat = _path_stat(blackboard_path)

    memory_total = 0
    memory_day = 0
    memory_status_updates = 0
    status_updates: list[dict[str, Any]] = []

    for _line_no, obj in _iter_jsonl(memory_path):
        memory_total += 1
        ts = obj.get("timestamp") or obj.get("ts")
        if not _ts_matches_day(ts, iso_day):
            continue
        memory_day += 1
        if obj.get("type") == "status_update":
            memory_status_updates += 1
            if len(status_updates) < limits.max_status_updates:
                status_updates.append(obj)

    bb_total = 0
    bb_day = 0
    bb_high = 0
    blackboard_events: list[dict[str, Any]] = []
    blackboard_phase_counts: dict[str, int] = {}

    for _line_no, ev in _iter_jsonl(blackboard_path):
        bb_total += 1
        ts = ev.get("timestamp") or ev.get("ts")
        if not _ts_matches_day(ts, iso_day):
            continue
        bb_day += 1
        phase = str(ev.get("phase") or "")
        if phase:
            blackboard_phase_counts[phase] = blackboard_phase_counts.get(phase, 0) + 1

        cls = _classify_blackboard_event(ev)
        if cls == "high":
            bb_high += 1
            if len(blackboard_events) < limits.max_blackboard_events:
                blackboard_events.append(ev)

    return {
        "type": "p6_bronze_rollup",
        "ts": _now_z(),
        "day": iso_day,
        "repo_root": str(repo_root),
        "inputs": {
            "mcp_memory": mem_stat,
            "blackboard": bb_stat,
        },
        "lossy_policy": {
            "notes": [
                "Source ledgers are append-only; this rollup is a bounded summary.",
                "High signal includes status_update entries (working memory) and blackboard failures/breaches/tripwires.",
                "Lists are capped to keep output small and stable.",
            ],
            "limits": {
                "max_status_updates": limits.max_status_updates,
                "max_blackboard_events": limits.max_blackboard_events,
            },
        },
        "scan": {
            "mcp_memory": {
                "total_entries": memory_total,
                "day_entries": memory_day,
                "day_status_updates": memory_status_updates,
            },
            "blackboard": {
                "total_entries": bb_total,
                "day_entries": bb_day,
                "day_high_signal": bb_high,
                "phase_counts": blackboard_phase_counts,
            },
        },
        "high_signal": {
            "status_updates": status_updates,
            "blackboard_events": blackboard_events,
        },
    }


def render_markdown(rollup: dict[str, Any]) -> str:
    day = rollup.get("day")
    ts = rollup.get("ts")
    inputs = rollup.get("inputs") or {}
    scan = rollup.get("scan") or {}
    lossy = rollup.get("lossy_policy") or {}
    hs = rollup.get("high_signal") or {}

    lines: list[str] = []
    lines.append("# Medallion: Silver | Mutation: 0% | HIVE: V")
    lines.append("")
    lines.append(f"# P6 Bronze Progressive Rollup (Daily): {day}")
    lines.append("")
    lines.append("## Provenance")
    lines.append(f"- Generated (Z): {ts}")
    lines.append("- Authority: Port 6 (Kraken Keeper)")
    lines.append("- Script: scripts/p6_bronze_progressive_rollup.py")
    lines.append("")

    lines.append("## Inputs (non-destructive)")
    mem = inputs.get("mcp_memory") or {}
    bb = inputs.get("blackboard") or {}
    lines.append(
        f"- MCP memory: {mem.get('path')} (exists={mem.get('exists')}, size={mem.get('size_bytes')})"
    )
    lines.append(
        f"- Blackboard: {bb.get('path')} (exists={bb.get('exists')}, size={bb.get('size_bytes')})"
    )
    lines.append("")

    lines.append("## Lossy Compression Policy (managed)")
    for note in lossy.get("notes") or []:
        lines.append(f"- {note}")
    lim = lossy.get("limits") or {}
    lines.append(
        f"- Limits: status_updates≤{lim.get('max_status_updates')} blackboard_events≤{lim.get('max_blackboard_events')}"
    )
    lines.append("")

    lines.append("## Scan Stats")
    ms = scan.get("mcp_memory") or {}
    bs = scan.get("blackboard") or {}
    lines.append(
        "- MCP memory: total_entries={total_entries} day_entries={day_entries} day_status_updates={day_status_updates}".format(
            **{
                k: ms.get(k)
                for k in ("total_entries", "day_entries", "day_status_updates")
            }
        )
    )
    lines.append(
        "- Blackboard: total_entries={total_entries} day_entries={day_entries} day_high_signal={day_high_signal}".format(
            **{
                k: bs.get(k)
                for k in ("total_entries", "day_entries", "day_high_signal")
            }
        )
    )
    phase_counts = bs.get("phase_counts") or {}
    if isinstance(phase_counts, dict) and phase_counts:
        top = sorted(phase_counts.items(), key=lambda kv: kv[1], reverse=True)[:12]
        lines.append("- Blackboard phase_counts (top):")
        for k, v in top:
            lines.append(f"  - {k}: {v}")
    lines.append("")

    lines.append("## High Signal — Working Memory (status_update)")
    sus = hs.get("status_updates") or []
    if not sus:
        lines.append("- None captured (either none for this day, or capped to 0).")
    else:
        for su in sus:
            ts2 = su.get("timestamp") or su.get("ts")
            topic = su.get("topic") or su.get("summary") or "(no topic)"
            lines.append(f"- {ts2} | {topic}")
    lines.append("")

    lines.append("## High Signal — Blackboard (failures/breaches/tripwires)")
    evs = hs.get("blackboard_events") or []
    if not evs:
        lines.append("- None captured.")
    else:
        for ev in evs:
            ts2 = ev.get("timestamp") or ev.get("ts")
            phase = ev.get("phase")
            status = ev.get("status")
            msg = ev.get("msg") or ev.get("details") or ev.get("tool") or ""
            msg = str(msg)
            if len(msg) > 200:
                msg = msg[:200] + "…"
            lines.append(f"- {ts2} | {phase} | {status} | {msg}")
    lines.append("")

    lines.append("## Next step (Bronze → Cold Bronze → Hot Silver)")
    lines.append(
        "- Freeze *inputs* (or their daily snapshots) into Cold Bronze with hash receipts."
    )
    lines.append(
        "- Use this rollup as the curated bridge: Cold Bronze is tamper-evident storage; Hot Silver is reusable narrative."
    )
    lines.append("")

    return "\n".join(lines)


def _append_status_update(
    memory_path: Path, *, topic: str, summary: dict[str, Any], sources: list[str]
) -> None:
    raise RuntimeError(
        "JSONL MCP memory writes are banned. Store status updates into the SSOT sqlite instead."
    )


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="P6 Bronze progressive rollup (bounded, non-destructive)"
    )
    ap.add_argument("--day", default="", help="YYYY-MM-DD (UTC). Default: today (UTC).")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument(
        "--memory",
        default="hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl",
    )
    ap.add_argument(
        "--blackboard", default="hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
    )
    ap.add_argument(
        "--out-dir",
        default="hfo_hot_obsidian/silver/3_resources/reports/rollups/daily",
        help="Hot Silver output directory.",
    )
    ap.add_argument("--max-status-updates", type=int, default=40)
    ap.add_argument("--max-blackboard-events", type=int, default=40)
    ap.add_argument(
        "--write-memory",
        action="store_true",
        help="DEPRECATED: writes to JSONL are banned; this now writes the proof entry into SSOT sqlite.",
    )
    args = ap.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()

    iso_day = (args.day or "").strip()
    if not iso_day:
        iso_day = datetime.now(timezone.utc).date().isoformat()

    memory_path = (repo_root / args.memory).resolve()
    blackboard_path = (repo_root / args.blackboard).resolve()

    limits = ScanLimits(
        max_status_updates=max(0, args.max_status_updates),
        max_blackboard_events=max(0, args.max_blackboard_events),
    )

    rollup = build_bronze_rollup(
        iso_day=iso_day,
        repo_root=repo_root,
        memory_path=memory_path,
        blackboard_path=blackboard_path,
        limits=limits,
    )

    md = render_markdown(rollup)
    out_dir = (repo_root / args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    out_name = f"BRONZE_ROLLUP_{iso_day.replace('-', '_')}.md"
    out_path = out_dir / out_name
    out_path.write_text(md, encoding="utf-8")

    artifact_dir = repo_root / "artifacts" / "rollups" / "bronze_daily"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_json = (
        artifact_dir
        / f"bronze_rollup_{iso_day.replace('-', '')}_{_sha256_text(md)[:12]}.json"
    )
    artifact_json.write_text(
        json.dumps(rollup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(str(out_path))
    print(str(artifact_json))

    if args.write_memory:
        # SSOT proof write (replaces legacy JSONL append).
        import asyncio

        from hfo_ssot_status_update import store_status_update

        payload = {
            "type": "status_update",
            "ts": _now_z(),
            "topic": f"p6_bronze_progressive_rollup_{iso_day}",
            "summary": {
                "rollup_markdown": str(out_path.relative_to(repo_root)),
                "rollup_artifact": str(artifact_json.relative_to(repo_root)),
                "day": iso_day,
            },
            "sources": [
                "scripts/p6_bronze_progressive_rollup.py",
                str(out_path.relative_to(repo_root)),
                str(artifact_json.relative_to(repo_root)),
                "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl",
            ],
        }

        ok, msg = asyncio.run(
            store_status_update(
                topic=payload["topic"],
                payload=payload,
                tags=["gen88_v4", "ssot", "status_update", "p6"],
                metadata={"source": "scripts/p6_bronze_progressive_rollup.py"},
                dry_run=False,
            )
        )
        if not ok:
            print(f"[rollup] warn: SSOT status_update write failed: {msg}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
