#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Generate first-pass monthly forensic deep dives for TTao dev work.

Non-destructive:
- Reads DuckDB (read-only)
- Writes new markdown reports under hot bronze projects

Grounding:
- Uses DuckDB `main.file_system.modified_at` as the month bucket
- This is a *file index* view of what changed, not a narrative truth

Default range: 2025-01 .. 2026-01 (inclusive)
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict
from typing import Any

import duckdb


REPO_ROOT = Path("/home/tommytai3/active/hfo_gen_88_chromebook_v_1")
DB_DEFAULT = REPO_ROOT / (
    "hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/"
    "root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb"
)
OUT_DIR_DEFAULT = REPO_ROOT / (
    "hfo_hot_obsidian/bronze/1_projects/"
    "forensics_ttao_dev_work_monthly_deep_dive_v1_2025_01_to_2026_01"
)

KEYWORDS = {
    # Alpha/HopeOS-ish
    "hopeos": ["hopeos", "hopeos_era", "hope ai", "hopeai"],
    "alpha": ["alpha", "mcp", "gateway", "swarm"],
    # Omega/CV-ish
    "omega": ["omega", "mediapipe", "opencv"],
    # Legacy project labels
    "tectangle": ["tectangle"],
    "drumpad": ["drumpad", "drum", "pads", "drumpads"],
    "tags": ["tags", "tags_drumpads"],
}


@dataclass(frozen=True)
class MonthWindow:
    year: int
    month: int
    start_naive: datetime
    end_naive: datetime


def _month_window(year: int, month: int) -> MonthWindow:
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    return MonthWindow(year=year, month=month, start_naive=start, end_naive=end)


def _month_iter(start_year: int, start_month: int, end_year: int, end_month: int):
    y, m = start_year, start_month
    while (y < end_year) or (y == end_year and m <= end_month):
        yield y, m
        if m == 12:
            y += 1
            m = 1
        else:
            m += 1


def _q(con: duckdb.DuckDBPyConnection, sql: str, params: list[Any]):
    return con.execute(sql, params).fetchall()


def _month_rows(con: duckdb.DuckDBPyConnection, start: datetime, end: datetime) -> list[tuple[str, Any, str, str, Any]]:
    """Load all rows for a month window in one query.

    Returns: (path, modified_at, era, project, score)
    """

    return _q(
        con,
        """
        select
          path,
          modified_at,
          coalesce(era, '') as era,
          coalesce(project, '') as project,
          coalesce(score, 0) as score
        from file_system
        where modified_at >= ? and modified_at < ?
        """,
        [start, end],
    )


def _ext_from_path(path: str) -> str:
    # Keep this intentionally simple; report is heuristic.
    leaf = path.rsplit("/", 1)[-1]
    if "." not in leaf:
        return ""
    ext = leaf.rsplit(".", 1)[-1].lower()
    return ext


def _bucket_from_path(path: str) -> str:
    # Coarse prefix bucket: first 4 segments.
    parts = [p for p in path.split("/") if p]
    return "/".join(parts[:4])


def _top_counter(counter: Counter[str], limit: int = 12) -> list[tuple[str, int]]:
    return counter.most_common(limit)


def _count_hotspots(paths_lower: list[str]) -> list[tuple[str, int]]:
    hotspots = [
        "node_modules",
        "dist/",
        "build/",
        "coverage/",
        "__pycache__",
        ".venv",
        "vendor/",
        "test-results",
        "hfo_hot_obsidian/bronze/4_archive",
        "hfo_hot_obsidian/bronze/1_projects",
        "hfo_hot_obsidian/bronze/3_resources",
        "hfo_hot_obsidian/silver",
        "hfo_hot_obsidian/gold",
        "contracts/",
        "scripts/",
        "tests/",
    ]

    out: list[tuple[str, int]] = []
    for h in hotspots:
        n = sum(1 for p in paths_lower if h in p)
        if n:
            out.append((h, n))
    out.sort(key=lambda x: x[1], reverse=True)
    return out


def _render_section_table(rows: list[tuple[Any, ...]], headers: list[str], max_rows: int = 12) -> list[str]:
    lines: list[str] = []
    if not rows:
        return ["(none)"]
    # header
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows[:max_rows]:
        lines.append("| " + " | ".join(str(x) for x in r) + " |")
    if len(rows) > max_rows:
        lines.append(f"(truncated; {len(rows)} rows total)")
    return lines


def generate_month_report(con: duckdb.DuckDBPyConnection, window: MonthWindow, db_path: Path) -> dict[str, Any]:
    start = window.start_naive
    end = window.end_naive

    rows = _month_rows(con, start, end)
    total = len(rows)
    if total:
        modified_ats = [r[1] for r in rows]
        min_ts = min(modified_ats)
        max_ts = max(modified_ats)
    else:
        min_ts = None
        max_ts = None

    era_counts: Counter[str] = Counter()
    project_counts: Counter[str] = Counter()
    ext_counts: Counter[str] = Counter()
    bucket_counts: Counter[str] = Counter()

    # Preserve sortability even if modified_at is not a python datetime.
    newest_rows = sorted(rows, key=lambda r: r[1], reverse=True)[:25]
    top_score_rows = sorted(rows, key=lambda r: (r[4], r[1]), reverse=True)[:25]

    paths_lower = [r[0].lower() for r in rows]
    for (path, _modified_at, era, project, _score) in rows:
        era_counts[str(era)] += 1
        project_counts[str(project)] += 1
        ext_counts[_ext_from_path(path)] += 1
        bucket_counts[_bucket_from_path(path)] += 1

    keyword_counts: dict[str, int] = {}
    keyword_samples: dict[str, list[tuple[str, str]]] = {}

    by_label: dict[str, list[tuple[str, Any]]] = defaultdict(list)
    for (path, modified_at, _era, _project, _score) in rows:
        p = path.lower()
        for label, patterns in KEYWORDS.items():
            if any(pt.lower() in p for pt in patterns):
                by_label[label].append((path, modified_at))

    for label in KEYWORDS.keys():
        hits = by_label.get(label, [])
        keyword_counts[label] = len(hits)
        hits_sorted = sorted(hits, key=lambda x: x[1], reverse=True)[:10]
        keyword_samples[label] = [(p, str(ts)) for (p, ts) in hits_sorted]

    hotspots = _count_hotspots(paths_lower)

    # Heuristic signals (grounded in the above counts).
    patterns: list[str] = []
    antipatterns: list[str] = []
    if total:
        top_bucket, top_bucket_n = bucket_counts.most_common(1)[0]
        top_bucket_share = top_bucket_n / total
        if top_bucket_share >= 0.35:
            patterns.append(f"High concentration in one bucket ({top_bucket}) ≈ {top_bucket_share:.0%} of indexed records.")
            antipatterns.append("Concentration can indicate coupling/hotspot risk; consider splitting responsibilities or adding gates.")

        hm = {h: n for (h, n) in hotspots}
        if hm.get("node_modules", 0) > 0:
            antipatterns.append("Presence of node_modules paths suggests vendored/generated artifacts; consider excluding from SSOT indexing.")
        if hm.get(".venv", 0) > 0:
            antipatterns.append("Presence of .venv paths suggests environment artifacts are being indexed; consider excluding .venv from change signals.")
        if hm.get("__pycache__", 0) > 0:
            antipatterns.append("Presence of __pycache__ suggests derived Python artifacts; consider excluding from tracked changes.")
        if hm.get("test-results", 0) > 0:
            antipatterns.append("test-results appearing in changes can be noisy; consider keeping only curated receipts/reports.")

        pyc_n = ext_counts.get("pyc", 0)
        if total and (pyc_n / total) >= 0.15:
            antipatterns.append("High .pyc volume suggests derived artifacts are dominating the change signal; consider filtering compiled outputs.")

        if keyword_counts.get("omega", 0) and keyword_counts.get("alpha", 0):
            patterns.append("Both omega and alpha keywords appear this month (cross-thread work visible in path-level signals).")

    newest = [(p, str(ts), era, proj, score) for (p, ts, era, proj, score) in newest_rows]
    top_score = [(p, str(ts), era, proj, score) for (p, ts, era, proj, score) in top_score_rows]

    return {
        "total": int(total),
        "min_ts": str(min_ts) if min_ts is not None else None,
        "max_ts": str(max_ts) if max_ts is not None else None,
        "top_eras": _top_counter(era_counts, limit=12),
        "top_projects": _top_counter(project_counts, limit=12),
        "top_ext": _top_counter(ext_counts, limit=12),
        "top_bucket": _top_counter(bucket_counts, limit=12),
        "keyword_counts": keyword_counts,
        "keyword_samples": keyword_samples,
        "hotspots": hotspots,
        "patterns": patterns,
        "antipatterns": antipatterns,
        "newest": newest,
        "top_score": top_score,
        "db_path": str(db_path),
        "window": {"start": start.isoformat(), "end": end.isoformat()},
    }


def write_month_md(out_path: Path, window: MonthWindow, report: dict[str, Any]) -> None:
    y, m = window.year, window.month
    month_str = f"{y:04d}-{m:02d}"

    lines: list[str] = []
    lines.append("# Medallion: Bronze | Mutation: 0% | HIVE: V")
    lines.append("")
    lines.append(f"# TTao Dev Work — Monthly Deep Dive v1: {month_str}")
    lines.append("")
    lines.append("## Provenance")
    lines.append(f"- Generated (UTC): {datetime.now(timezone.utc).isoformat().replace('+00:00','Z')}")
    lines.append(f"- DuckDB: {report['db_path']}")
    lines.append(f"- Window (modified_at): {report['window']['start']} .. {report['window']['end']} (start inclusive, end exclusive)")
    lines.append("")
    lines.append("## Scope notes (first pass)")
    lines.append("- This report is purely based on `file_system.modified_at` (file index).")
    lines.append("- It does not assume older forks are ‘your work’; it only reports what files appear in the index for this month window.")
    lines.append("")

    lines.append("## Summary")
    lines.append(f"- Indexed file records this month: {report['total']}")
    lines.append(f"- Earliest modified_at in month: {report['min_ts']}")
    lines.append(f"- Latest modified_at in month: {report['max_ts']}")
    lines.append("")

    lines.append("## Keyword path hits (counts)")
    for k, v in report["keyword_counts"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("## Top eras (by count)")
    lines.extend(_render_section_table(report["top_eras"], ["era", "n"], max_rows=12))
    lines.append("")

    lines.append("## Top projects (by count)")
    lines.extend(_render_section_table(report["top_projects"], ["project", "n"], max_rows=12))
    lines.append("")

    lines.append("## Top buckets (by count; coarse path prefix)")
    lines.extend(_render_section_table(report["top_bucket"], ["bucket", "n"], max_rows=12))
    lines.append("")

    lines.append("## Hotspots (path substring counts)")
    if report.get("hotspots"):
        lines.extend(_render_section_table(report["hotspots"], ["substring", "n"], max_rows=20))
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("## Patterns (heuristic)")
    if report.get("patterns"):
        for p in report["patterns"]:
            lines.append(f"- {p}")
    else:
        lines.append("(none detected)")
    lines.append("")

    lines.append("## Anti-patterns / risks (heuristic)")
    if report.get("antipatterns"):
        for a in report["antipatterns"]:
            lines.append(f"- {a}")
    else:
        lines.append("(none detected)")
    lines.append("")

    lines.append("## Top extensions (by count)")
    lines.extend(_render_section_table(report["top_ext"], ["ext", "n"], max_rows=12))
    lines.append("")

    lines.append("## Keyword samples (newest paths)")
    for label, samples in report["keyword_samples"].items():
        lines.append(f"### {label}")
        if not samples:
            lines.append("(none)")
        else:
            for p, ts in samples:
                lines.append(f"- {ts} | {p}")
        lines.append("")

    lines.append("## Newest paths (top 25)")
    for (p, ts, era, proj, score) in report["newest"]:
        lines.append(f"- {ts} | score={score} | {era}/{proj} | {p}")
    lines.append("")

    lines.append("## Highest-score paths (top 25)")
    for (p, ts, era, proj, score) in report["top_score"]:
        lines.append(f"- score={score} | {ts} | {era}/{proj} | {p}")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DB_DEFAULT))
    ap.add_argument("--out", default=str(OUT_DIR_DEFAULT))
    ap.add_argument("--start", default="2025-01", help="YYYY-MM")
    ap.add_argument("--end", default="2026-01", help="YYYY-MM (inclusive)")
    ap.add_argument("--progress", action="store_true", default=True)
    args = ap.parse_args()

    start_year, start_month = [int(x) for x in args.start.split("-")]
    end_year, end_month = [int(x) for x in args.end.split("-")]

    out_root = Path(args.out)
    out_monthly = out_root / "monthly"
    out_monthly.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(args.db), read_only=True)
    try:
        index_rows: list[tuple[str, int, str, str]] = []
        for (y, m) in _month_iter(start_year, start_month, end_year, end_month):
            window = _month_window(y, m)
            if args.progress:
                print(f"[month {y:04d}-{m:02d}] scanning...", flush=True)
            rep = generate_month_report(con, window, Path(args.db))
            out_path = out_monthly / f"TTAO_DEV_MONTHLY_DEEP_DIVE_{y:04d}_{m:02d}.md"
            write_month_md(out_path, window, rep)
            if args.progress:
                print(f"[month {y:04d}-{m:02d}] wrote {out_path} (n={rep['total']})", flush=True)

            top_era = rep["top_eras"][0][0] if rep["top_eras"] else ""
            top_proj = rep["top_projects"][0][0] if rep["top_projects"] else ""
            index_rows.append((f"{y:04d}-{m:02d}", rep["total"], str(top_era), str(top_proj)))

        # Write index
        idx = []
        idx.append("# Medallion: Bronze | Mutation: 0% | HIVE: V")
        idx.append("")
        idx.append("# TTao Dev Work — Monthly Deep Dives v1 (Index)")
        idx.append("")
        idx.append("## Provenance")
        idx.append(f"- Generated (UTC): {datetime.now(timezone.utc).isoformat().replace('+00:00','Z')}")
        idx.append(f"- DuckDB: {args.db}")
        idx.append(f"- Range: {args.start} .. {args.end} (inclusive)")
        idx.append("")
        idx.append("## Months")
        idx.append("| month | indexed_records | top_era | top_project | report |");
        idx.append("|---|---:|---|---|---|")
        for (month, n, era, proj) in index_rows:
            y, m = month.split("-")
            rel = f"monthly/TTAO_DEV_MONTHLY_DEEP_DIVE_{y}_{m}.md"
            idx.append(f"| {month} | {n} | {era} | {proj} | [{rel}]({rel}) |")
        (out_root / "INDEX.md").write_text("\n".join(idx), encoding="utf-8")

    finally:
        con.close()

    print(out_root / "INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
