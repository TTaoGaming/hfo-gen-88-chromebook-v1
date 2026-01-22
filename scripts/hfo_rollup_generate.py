#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Generate daily/monthly rollups from HFO memory artifacts.

Primary inputs (read-only):
- DuckDB SSOT (file index + content batches): hfo_unified_v88_merged.duckdb
- Working memory: hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
- Stigmergy blackboard: hfo_hot_obsidian/hot_obsidian_blackboard.jsonl

Outputs:
- Daily rollups -> hfo_hot_obsidian/silver/3_resources/reports/rollups/daily/
- Monthly rollups -> hfo_hot_obsidian/gold/3_resources/reports/rollups/monthly/

This stays intentionally simple: deterministic, grep-like filtering by date prefix,
plus DuckDB queries over file_system for changed artifacts.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import duckdb


REPO_ROOT_DEFAULT = Path("/home/tommytai3/active/hfo_gen_88_chromebook_v_1")
DB_DEFAULT = REPO_ROOT_DEFAULT / (
    "hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/"
    "root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb"
)
MCP_MEMORY_DEFAULT = REPO_ROOT_DEFAULT / "hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl"
HOT_BLACKBOARD_DEFAULT = REPO_ROOT_DEFAULT / "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

DAILY_OUT_DEFAULT = REPO_ROOT_DEFAULT / "hfo_hot_obsidian/silver/3_resources/reports/rollups/daily"
MONTHLY_OUT_DEFAULT = REPO_ROOT_DEFAULT / "hfo_hot_obsidian/gold/3_resources/reports/rollups/monthly"


@dataclass(frozen=True)
class RollupWindow:
    start_utc: datetime
    end_utc: datetime


def _parse_day(day_str: str) -> date:
    return date.fromisoformat(day_str)


def _day_window_utc(day: date) -> RollupWindow:
    start = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    return RollupWindow(start_utc=start, end_utc=end)


def _month_window_utc(year: int, month: int) -> RollupWindow:
    start = datetime(year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(year, month + 1, 1, tzinfo=timezone.utc)
    return RollupWindow(start_utc=start, end_utc=end)


def _iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if isinstance(obj, dict):
                yield obj


def _date_prefixes(day: date) -> tuple[str, str]:
    # Common timestamp encodings we see in this repo.
    return (day.isoformat(), f"{day.year:04d}_{day.month:02d}_{day.day:02d}")


def _filter_jsonl_by_day(records: Iterable[dict[str, Any]], day: date) -> list[dict[str, Any]]:
    iso, _ = _date_prefixes(day)
    keep: list[dict[str, Any]] = []
    for r in records:
        ts = r.get("timestamp") or r.get("ts")
        if isinstance(ts, str) and ts.startswith(iso):
            keep.append(r)
    return keep


def _filter_mcp_status_updates_by_day(path: Path, day: date) -> list[dict[str, Any]]:
    iso, _ = _date_prefixes(day)
    out: list[dict[str, Any]] = []
    for r in _iter_jsonl(path):
        if r.get("type") != "status_update":
            continue
        ts = r.get("timestamp") or r.get("ts")
        if isinstance(ts, str) and ts.startswith(iso):
            out.append(r)
    return out


def _duckdb_changed_files(con: duckdb.DuckDBPyConnection, repo_root: Path, window: RollupWindow) -> list[tuple[str, datetime, str, str, int]]:
    root_prefix = str(repo_root) + "/%"
    # Note: file_system.modified_at is naive TIMESTAMP; treat it as UTC for windowing.
    # We intentionally keep this simple and deterministic.
    q = """
    select
      path,
      modified_at,
      coalesce(era, '') as era,
      coalesce(project, '') as project,
      coalesce(score, 0) as score
    from file_system
    where path like ?
      and modified_at >= ?
      and modified_at < ?
    order by modified_at desc
    limit 200
    """
    rows = con.execute(q, [root_prefix, window.start_utc.replace(tzinfo=None), window.end_utc.replace(tzinfo=None)]).fetchall()
    return [(p, m, era, proj, int(score)) for (p, m, era, proj, score) in rows]


def _duckdb_files_with_date_in_name(con: duckdb.DuckDBPyConnection, repo_root: Path, day: date) -> list[str]:
    iso, underscored = _date_prefixes(day)
    root_prefix = str(repo_root) + "/%"
    q = """
    select path
    from file_system
    where path like ?
      and (path like ? or path like ?)
    order by modified_at desc
    limit 200
    """
    like_iso = f"%{iso}%"
    like_us = f"%{underscored}%"
    return [r[0] for r in con.execute(q, [root_prefix, like_iso, like_us]).fetchall()]


def _render_daily_md(
    day: date,
    repo_root: Path,
    db_path: Path,
    changed_files: list[tuple[str, datetime, str, str, int]],
    named_files: list[str],
    status_updates: list[dict[str, Any]],
    blackboard_events: list[dict[str, Any]],
) -> str:
    iso, underscored = _date_prefixes(day)
    lines: list[str] = []
    lines.append("# Medallion: Silver | Mutation: 0% | HIVE: V")
    lines.append("")
    lines.append(f"# Daily Rollup: {iso}")
    lines.append("")
    lines.append("## Provenance")
    lines.append(f"- Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"- DuckDB SSOT: {db_path}")
    lines.append(f"- Repo root: {repo_root}")
    lines.append("")

    lines.append("## Working Memory (status_update)")
    if not status_updates:
        lines.append("- None found for this day in mcp_memory.jsonl")
    else:
        for su in status_updates:
            topic = su.get("topic") or su.get("summary")
            ts = su.get("timestamp") or su.get("ts")
            lines.append(f"- {ts} | {topic}")
            evidence = su.get("evidence") or {}
            related = evidence.get("related_files") if isinstance(evidence, dict) else None
            if isinstance(related, list) and related:
                for rf in related[:12]:
                    if isinstance(rf, str):
                        lines.append(f"  - {rf}")
    lines.append("")

    lines.append("## Stigmergy Blackboard (events)")
    if not blackboard_events:
        lines.append("- None found for this day in hot_obsidian_blackboard.jsonl")
    else:
        for ev in blackboard_events[:50]:
            ts = ev.get("timestamp") or ev.get("ts")
            phase = ev.get("phase")
            status = ev.get("status")
            msg = ev.get("msg") or ev.get("details") or ev.get("tool")
            lines.append(f"- {ts} | {phase} | {status} | {msg}")
    lines.append("")

    lines.append("## Files Changed (repo-root; from DuckDB file_system)")
    lines.append(f"- Total returned (top 200 newest): {len(changed_files)}")
    if changed_files:
        for (p, m, era, proj, score) in changed_files[:80]:
            lines.append(f"- {m.isoformat()} | score={score} | {era}/{proj} | {p}")
    lines.append("")

    lines.append("## Files With Date In Name")
    lines.append(f"- Date tokens: {iso}, {underscored}")
    if not named_files:
        lines.append("- None found")
    else:
        for p in named_files[:120]:
            lines.append(f"- {p}")

    lines.append("")
    lines.append("## Notes")
    lines.append("- This rollup is generated from *observed artifacts* (DuckDB index + JSONL logs).")
    lines.append("- If you want a richer narrative, promote this to Gold by editing + linking the key files listed above.")
    lines.append("")
    return "\n".join(lines)


def generate_daily(args: argparse.Namespace) -> Path:
    day = _parse_day(args.day)
    window = _day_window_utc(day)

    repo_root = Path(args.repo_root)
    db_path = Path(args.db)
    mcp_memory = Path(args.mcp_memory)
    blackboard = Path(args.blackboard)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        changed = _duckdb_changed_files(con, repo_root, window)
        named = _duckdb_files_with_date_in_name(con, repo_root, day)
    finally:
        con.close()

    status_updates = _filter_mcp_status_updates_by_day(mcp_memory, day)
    blackboard_events = _filter_jsonl_by_day(_iter_jsonl(blackboard), day)

    md = _render_daily_md(day, repo_root, db_path, changed, named, status_updates, blackboard_events)
    out_path = out_dir / f"ROLLUP_{day.year:04d}_{day.month:02d}_{day.day:02d}.md"
    out_path.write_text(md, encoding="utf-8")
    return out_path


def generate_monthly(args: argparse.Namespace) -> Path:
    year, month = [int(x) for x in args.month.split("-")]
    window = _month_window_utc(year, month)

    repo_root = Path(args.repo_root)
    db_path = Path(args.db)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        root_prefix = str(repo_root) + "/%"
        q = """
        select
          date_trunc('day', modified_at) as day,
          count(*) as n
        from file_system
        where path like ?
          and modified_at >= ?
          and modified_at < ?
        group by day
        order by day
        """
        rows = con.execute(q, [root_prefix, window.start_utc.replace(tzinfo=None), window.end_utc.replace(tzinfo=None)]).fetchall()
    finally:
        con.close()

    lines: list[str] = []
    lines.append("# Medallion: Gold | Mutation: 0% | HIVE: V")
    lines.append("")
    lines.append(f"# Monthly Rollup: {year:04d}-{month:02d}")
    lines.append("")
    lines.append("## Provenance")
    lines.append(f"- Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"- DuckDB SSOT: {db_path}")
    lines.append(f"- Repo root: {repo_root}")
    lines.append("")
    lines.append("## Change Volume (file_system)")
    if not rows:
        lines.append("- No changes found in this month window")
    else:
        total = sum(int(n) for (_d, n) in rows)
        lines.append(f"- Total changed file records: {total}")
        for (d, n) in rows:
            day_iso = d.isoformat() if hasattr(d, "isoformat") else str(d)
            lines.append(f"- {day_iso} | {int(n)}")
    lines.append("")
    lines.append("## Next")
    lines.append("- Generate daily rollups for the busiest days and summarize them here with links.")
    lines.append("")

    out_path = out_dir / f"ROLLUP_{year:04d}_{month:02d}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    p_day = sub.add_parser("daily")
    p_day.add_argument("--day", required=True, help="YYYY-MM-DD")
    p_day.add_argument("--repo-root", default=str(REPO_ROOT_DEFAULT))
    p_day.add_argument("--db", default=str(DB_DEFAULT))
    p_day.add_argument("--mcp-memory", default=str(MCP_MEMORY_DEFAULT))
    p_day.add_argument("--blackboard", default=str(HOT_BLACKBOARD_DEFAULT))
    p_day.add_argument("--out-dir", default=str(DAILY_OUT_DEFAULT))

    p_month = sub.add_parser("monthly")
    p_month.add_argument("--month", required=True, help="YYYY-MM")
    p_month.add_argument("--repo-root", default=str(REPO_ROOT_DEFAULT))
    p_month.add_argument("--db", default=str(DB_DEFAULT))
    p_month.add_argument("--out-dir", default=str(MONTHLY_OUT_DEFAULT))

    args = p.parse_args()
    if args.cmd == "daily":
        out = generate_daily(args)
        print(out)
        return 0
    if args.cmd == "monthly":
        out = generate_monthly(args)
        print(out)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
