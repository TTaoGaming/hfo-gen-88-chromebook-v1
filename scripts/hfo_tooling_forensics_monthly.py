#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Generate month-by-month tooling/dependency/worked-vs-failed forensics.

Non-destructive:
- Reads DuckDB (read-only)
- Reads hot blackboard + MCP memory JSONL (read-only)
- Writes new markdown reports under hot bronze projects

Grounding:
- Primary month windowing comes from DuckDB `file_system.modified_at` (naive TIMESTAMP).
  Treat it as UTC and use start-inclusive/end-exclusive windows.
- Tool success/failure signals are heuristic: parsed from MCP memory `tests` fields and
  blackboard TOOL_TRIPWIRE events.

Default range: 2025-01 .. 2026-01 (inclusive)
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import duckdb


REPO_ROOT = Path("/home/tommytai3/active/hfo_gen_88_chromebook_v_1")
DB_DEFAULT = REPO_ROOT / (
    "hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/"
    "root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb"
)
MCP_MEMORY_DEFAULT = REPO_ROOT / "hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl"
BLACKBOARD_DEFAULT = REPO_ROOT / "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
OUT_DIR_DEFAULT = REPO_ROOT / (
    "hfo_hot_obsidian/bronze/1_projects/"
    "forensics_ttao_tooling_forensics_v1_2025_01_to_2026_01"
)


DERIVED_SUBSTRINGS_DEFAULT = [
    "node_modules/",
    "__pycache__/",
    ".venv/",
    "dist/",
    "build/",
    "coverage/",
    "test-results/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".next/",
    ".turbo/",
]


MANIFEST_RULES: dict[str, list[str]] = {
    "node/package.json": ["/package.json"],
    "node/package-lock": ["/package-lock.json"],
    "node/yarn.lock": ["/yarn.lock"],
    "node/pnpm-lock": ["/pnpm-lock.yaml"],
    "node/tsconfig": ["/tsconfig.json"],
    "node/eslint": ["/eslint.config.", "/.eslintrc"],
    "node/playwright": ["/playwright.config.", "playwright."],
    "node/vite": ["/vite.config."],
    "node/next": ["/next.config."],
    "node/jest": ["/jest.config."],
    "node/vitest": ["/vitest.config."],
    "node/webpack": ["/webpack.config."],
    "node/rollup": ["/rollup.config."],
    "python/pyproject": ["/pyproject.toml"],
    "python/poetry.lock": ["/poetry.lock"],
    "python/requirements": ["/requirements.txt", "/requirements-dev.txt", "/requirements-dev.in"],
    "python/pipfile": ["/pipfile", "/pipfile.lock"],
    "python/setup.py": ["/setup.py"],
    "python/conda": ["/environment.yml", "/env.yml"],
    "rust/cargo.toml": ["/cargo.toml"],
    "rust/cargo.lock": ["/cargo.lock"],
    "go/go.mod": ["/go.mod"],
    "go/go.sum": ["/go.sum"],
    "java/maven": ["/pom.xml"],
    "java/gradle": ["/build.gradle", "/build.gradle.kts", "/gradle.properties"],
    "docker/dockerfile": ["/dockerfile"],
    "docker/compose": ["/docker-compose.yml", "/docker-compose.yaml"],
    "ci/github-actions": ["/.github/workflows/"],
    "build/make": ["/makefile"],
    "build/just": ["/justfile"],
    "build/taskfile": ["/taskfile.yml", "/taskfile.yaml"],
}


TEST_TOOL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("playwright", re.compile(r"\bplaywright\b|npx\s+playwright", re.I)),
    ("eslint", re.compile(r"\beslint\b", re.I)),
    ("vitest", re.compile(r"\bvitest\b", re.I)),
    ("jest", re.compile(r"\bjest\b", re.I)),
    ("pytest", re.compile(r"\bpytest\b", re.I)),
    ("ruff", re.compile(r"\bruff\b", re.I)),
    ("mypy", re.compile(r"\bmypy\b", re.I)),
    ("tsc", re.compile(r"\btsc\b|typescript", re.I)),
    ("npm", re.compile(r"\bnpm\b", re.I)),
    ("pnpm", re.compile(r"\bpnpm\b", re.I)),
    ("yarn", re.compile(r"\byarn\b", re.I)),
    ("python", re.compile(r"\bpython\d?\b", re.I)),
]


@dataclass(frozen=True)
class MonthWindow:
    year: int
    month: int
    start_naive: datetime
    end_naive: datetime
    start_utc: datetime
    end_utc: datetime


def _month_window(year: int, month: int) -> MonthWindow:
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    start_utc = start.replace(tzinfo=timezone.utc)
    end_utc = end.replace(tzinfo=timezone.utc)
    return MonthWindow(year=year, month=month, start_naive=start, end_naive=end, start_utc=start_utc, end_utc=end_utc)


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


def _month_paths(con: duckdb.DuckDBPyConnection, start: datetime, end: datetime) -> list[str]:
    rows = _q(
        con,
        """
        select path
        from file_system
        where modified_at >= ? and modified_at < ?
        """,
        [start, end],
    )
    return [r[0] for r in rows]


def _ext_from_path(path: str) -> str:
    leaf = path.rsplit("/", 1)[-1]
    if "." not in leaf:
        return ""
    return leaf.rsplit(".", 1)[-1].lower()


def _parse_ts(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        # not expected
        return None
    if not isinstance(value, str):
        return None

    s = value.strip()
    if not s:
        return None

    # Normalize Z:
    # - "...Z"            -> "...+00:00"
    # - "...+00:00Z"      -> "...+00:00"
    # - "...-07:00Z"      -> "...-07:00"
    if s.endswith("Z"):
        s = s[:-1]
        if not re.search(r"[+-]\d{2}:\d{2}$", s):
            s = s + "+00:00"

    # datetime.fromisoformat doesn't accept trailing 'Z' but does accept offsets.
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


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
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                yield obj


def _mcp_entries_for_month(mcp_path: Path, window: MonthWindow) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for obj in _iter_jsonl(mcp_path):
        dt = _parse_ts(obj.get("timestamp") or obj.get("ts"))
        if dt is None:
            continue
        if window.start_utc <= dt < window.end_utc:
            out.append(obj)
    return out


def _blackboard_entries_for_month(bb_path: Path, window: MonthWindow) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for obj in _iter_jsonl(bb_path):
        dt = _parse_ts(obj.get("timestamp"))
        if dt is None:
            continue
        if window.start_utc <= dt < window.end_utc:
            out.append(obj)
    return out


def _detect_manifests(paths_lower: list[str]) -> Counter[str]:
    c: Counter[str] = Counter()
    for p in paths_lower:
        for label, needles in MANIFEST_RULES.items():
            if any(n in p for n in needles):
                c[label] += 1
    return c


def _filter_high_signal(paths: list[str], derived_substrings: list[str]) -> list[str]:
    if not paths:
        return []
    out: list[str] = []
    needles = [d.lower() for d in derived_substrings]
    for p in paths:
        pl = p.lower()
        if any(n in pl for n in needles):
            continue
        out.append(p)
    return out


def _infer_stacks(manifests: Counter[str], ext_counts: Counter[str], tests_counter: Counter[str]) -> list[str]:
    stacks: list[str] = []

    nodeish = sum(manifests.get(k, 0) for k in ["node/package.json", "node/yarn.lock", "node/pnpm-lock", "node/package-lock"]) > 0
    pyish = sum(manifests.get(k, 0) for k in ["python/pyproject", "python/requirements", "python/pipfile", "python/conda"]) > 0
    dockerish = sum(manifests.get(k, 0) for k in ["docker/dockerfile", "docker/compose"]) > 0

    if nodeish:
        stacks.append("node")
    if pyish:
        stacks.append("python")
    if dockerish:
        stacks.append("docker")

    # Tooling anchored by tests even if config files aren't present this month.
    if tests_counter.get("playwright", 0) > 0 or manifests.get("node/playwright", 0) > 0:
        stacks.append("playwright")
    if tests_counter.get("eslint", 0) > 0 or manifests.get("node/eslint", 0) > 0:
        stacks.append("eslint")

    # Language hints by extension volume.
    if ext_counts.get("ts", 0) + ext_counts.get("tsx", 0) >= 50:
        stacks.append("typescript")
    if ext_counts.get("py", 0) >= 50:
        stacks.append("python-code")

    # Keep unique, stable order.
    seen: set[str] = set()
    out: list[str] = []
    for s in stacks:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def _extract_test_runs(entries: list[dict[str, Any]]) -> tuple[Counter[str], Counter[str], list[str]]:
    """Returns (tool_counts, status_counts, sample_lines)."""

    tool_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    samples: list[str] = []

    def classify_tool(seg: str) -> str:
        for name, pat in TEST_TOOL_PATTERNS:
            if pat.search(seg):
                return name
        return "unknown"

    def classify_status(seg: str) -> str:
        s = seg.upper()
        if "FAIL" in s or "EXIT 1" in s or "NONZERO" in s:
            return "FAIL"
        if "PASS" in s or "EXIT 0" in s:
            return "PASS"
        return "UNKNOWN"

    for e in entries:
        tests = e.get("tests")
        if not isinstance(tests, str) or not tests.strip():
            continue
        # Split on common delimiters but keep chunks big enough to parse.
        for seg in re.split(r"[\n;]+", tests):
            seg = seg.strip()
            if not seg:
                continue
            tool = classify_tool(seg)
            status = classify_status(seg)
            tool_counts[tool] += 1
            status_counts[status] += 1
            if len(samples) < 15:
                samples.append(seg)

    return tool_counts, status_counts, samples


def _extract_tripwires(entries: list[dict[str, Any]]) -> tuple[Counter[str], list[str]]:
    by_tool: Counter[str] = Counter()
    samples: list[str] = []

    for e in entries:
        if e.get("phase") != "TOOL_TRIPWIRE":
            continue
        status = str(e.get("status") or "").upper()
        tool = str(e.get("tool") or "unknown")
        if status == "FAIL":
            by_tool[tool] += 1
            if len(samples) < 10:
                details = str(e.get("details") or "").strip()
                samples.append(f"{tool}: {details}" if details else f"{tool}: FAIL")

    return by_tool, samples


def _render_table(rows: list[tuple[Any, ...]], headers: list[str], max_rows: int = 12) -> list[str]:
    if not rows:
        return ["(none)"]
    lines: list[str] = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows[:max_rows]:
        lines.append("| " + " | ".join(str(x) for x in r) + " |")
    if len(rows) > max_rows:
        lines.append(f"(truncated; {len(rows)} rows total)")
    return lines


def generate_month_report(
    con: duckdb.DuckDBPyConnection,
    window: MonthWindow,
    db_path: Path,
    mcp_path: Path,
    bb_path: Path,
    high_signal: bool,
    derived_substrings: list[str],
) -> dict[str, Any]:
    # DuckDB: file-path evidence
    paths = _month_paths(con, window.start_naive, window.end_naive)
    paths_for_signal = _filter_high_signal(paths, derived_substrings) if high_signal else paths
    paths_lower = [p.lower() for p in paths_for_signal]

    ext_counts: Counter[str] = Counter(_ext_from_path(p) for p in paths_for_signal)
    manifests = _detect_manifests(paths_lower)

    # Memory: worked/failed signals (heuristic)
    mcp_entries = _mcp_entries_for_month(mcp_path, window)
    bb_entries = _blackboard_entries_for_month(bb_path, window)

    test_tool_counts, test_status_counts, test_samples = _extract_test_runs(mcp_entries)
    tripwire_by_tool, tripwire_samples = _extract_tripwires(bb_entries)

    stacks = _infer_stacks(manifests, ext_counts, test_tool_counts)

    patterns: list[str] = []
    antipatterns: list[str] = []

    if high_signal:
        patterns.append("High-signal mode enabled (derived artifact substrings filtered).")
    else:
        antipatterns.append("High-signal mode is OFF; derived artifacts may dominate counts.")

    if tripwire_by_tool:
        antipatterns.append("Tool tripwires (missing keys/config) occurred this month; see Tripwires section.")

    if test_status_counts.get("FAIL", 0) > 0:
        antipatterns.append("At least one recorded test/tool command indicates FAIL/nonzero exit.")

    if manifests.get("python/conda", 0) and manifests.get("python/pyproject", 0):
        antipatterns.append("Mixed Python env styles (conda + pyproject) detected; pin one baseline to reduce friction.")

    if manifests.get("node/yarn.lock", 0) and manifests.get("node/pnpm-lock", 0):
        antipatterns.append("Multiple Node lockfile ecosystems detected; pick one to reduce agent slop.")

    # Actionable fixes suggested
    fixes: list[str] = []
    for tool, n in tripwire_by_tool.most_common():
        if n:
            fixes.append(f"Set {tool} credentials/env vars (tripwire FAIL x{n}).")

    if manifests.get("node/package.json", 0) and not (manifests.get("node/package-lock", 0) or manifests.get("node/yarn.lock", 0) or manifests.get("node/pnpm-lock", 0)):
        fixes.append("Node project touched without a lockfile change; consider ensuring lockfile is committed to stabilize installs.")

    return {
        "month": f"{window.year:04d}-{window.month:02d}",
        "provenance": {
            "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "db": str(db_path),
            "mcp_memory": str(mcp_path),
            "blackboard": str(bb_path),
            "window_modified_at": {"start": window.start_naive.isoformat(), "end": window.end_naive.isoformat()},
            "window_utc": {"start": window.start_utc.isoformat().replace("+00:00", "Z"), "end": window.end_utc.isoformat().replace("+00:00", "Z")},
            "high_signal": bool(high_signal),
        },
        "counts": {
            "duckdb_paths_total": len(paths),
            "duckdb_paths_used": len(paths_for_signal),
            "mcp_entries": len(mcp_entries),
            "blackboard_entries": len(bb_entries),
        },
        "stacks": stacks,
        "manifests_top": manifests.most_common(20),
        "ext_top": ext_counts.most_common(20),
        "tests": {
            "tools": test_tool_counts.most_common(20),
            "status": dict(test_status_counts),
            "samples": test_samples,
        },
        "tripwires": {
            "fail_by_tool": tripwire_by_tool.most_common(20),
            "samples": tripwire_samples,
        },
        "patterns": patterns,
        "antipatterns": antipatterns,
        "suggested_fixes": fixes,
    }


def write_month_md(out_path: Path, report: dict[str, Any]) -> None:
    month = report["month"]

    lines: list[str] = []
    lines.append("# Medallion: Bronze | Mutation: 0% | HIVE: V")
    lines.append("")
    lines.append(f"# TTao Tooling Forensics v1: {month}")
    lines.append("")

    prov = report["provenance"]
    lines.append("## Provenance")
    lines.append(f"- Generated (UTC): {prov['generated_utc']}")
    lines.append(f"- DuckDB: {prov['db']}")
    lines.append(f"- MCP memory: {prov['mcp_memory']}")
    lines.append(f"- Hot blackboard: {prov['blackboard']}")
    lines.append(f"- Window (DuckDB modified_at): {prov['window_modified_at']['start']} .. {prov['window_modified_at']['end']} (start inclusive, end exclusive)")
    lines.append(f"- Window (UTC): {prov['window_utc']['start']} .. {prov['window_utc']['end']} (start inclusive, end exclusive)")
    lines.append(f"- High-signal mode: {prov['high_signal']}")
    lines.append("")

    lines.append("## Summary")
    c = report["counts"]
    lines.append(f"- DuckDB path records: total={c['duckdb_paths_total']} used={c['duckdb_paths_used']}")
    lines.append(f"- MCP memory entries in month: {c['mcp_entries']}")
    lines.append(f"- Blackboard entries in month: {c['blackboard_entries']}")
    stacks = report.get("stacks") or []
    lines.append(f"- Inferred stacks: {', '.join(stacks) if stacks else '(none)'}")
    lines.append("")

    lines.append("## Manifests/configs (top)")
    lines.extend(_render_table(report.get("manifests_top") or [], ["signal", "n"], max_rows=20))
    lines.append("")

    lines.append("## Extensions (top; post-filter)")
    lines.extend(_render_table(report.get("ext_top") or [], ["ext", "n"], max_rows=20))
    lines.append("")

    lines.append("## Tests/commands (from MCP memory; heuristic)")
    tests = report.get("tests") or {}
    lines.append("### Tool counts")
    lines.extend(_render_table(tests.get("tools") or [], ["tool", "n"], max_rows=20))
    lines.append("")
    lines.append("### Status counts")
    status = tests.get("status") or {}
    status_rows = sorted([(k, v) for k, v in status.items()], key=lambda x: x[1], reverse=True)
    lines.extend(_render_table(status_rows, ["status", "n"], max_rows=10))
    lines.append("")
    lines.append("### Samples")
    samples = tests.get("samples") or []
    if samples:
        for s in samples:
            lines.append(f"- {s}")
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("## Tripwires (from hot blackboard; TOOL_TRIPWIRE FAIL)")
    trip = report.get("tripwires") or {}
    lines.append("### Fails by tool")
    lines.extend(_render_table(trip.get("fail_by_tool") or [], ["tool", "fail_count"], max_rows=20))
    lines.append("")
    lines.append("### Samples")
    trip_samples = trip.get("samples") or []
    if trip_samples:
        for s in trip_samples:
            lines.append(f"- {s}")
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("## Patterns (heuristic)")
    pats = report.get("patterns") or []
    if pats:
        for p in pats:
            lines.append(f"- {p}")
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("## Anti-patterns / risks (heuristic)")
    aps = report.get("antipatterns") or []
    if aps:
        for a in aps:
            lines.append(f"- {a}")
    else:
        lines.append("(none)")
    lines.append("")

    lines.append("## Suggested friction fixes (actionable)")
    fixes = report.get("suggested_fixes") or []
    if fixes:
        for f in fixes:
            lines.append(f"- {f}")
    else:
        lines.append("(none)")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DB_DEFAULT))
    ap.add_argument("--mcp", default=str(MCP_MEMORY_DEFAULT))
    ap.add_argument("--blackboard", default=str(BLACKBOARD_DEFAULT))
    ap.add_argument("--out", default=str(OUT_DIR_DEFAULT))
    ap.add_argument("--start", default="2025-01", help="YYYY-MM")
    ap.add_argument("--end", default="2026-01", help="YYYY-MM (inclusive)")
    ap.add_argument("--progress", action="store_true", default=True)
    ap.add_argument("--high-signal", action="store_true", default=True)
    ap.add_argument(
        "--derived-substring",
        action="append",
        default=[],
        help="Substring to filter when --high-signal is enabled (repeatable).",
    )
    args = ap.parse_args()

    start_year, start_month = [int(x) for x in args.start.split("-")]
    end_year, end_month = [int(x) for x in args.end.split("-")]

    derived = DERIVED_SUBSTRINGS_DEFAULT + [s for s in args.derived_substring if s]

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
            rep = generate_month_report(
                con=con,
                window=window,
                db_path=Path(args.db),
                mcp_path=Path(args.mcp),
                bb_path=Path(args.blackboard),
                high_signal=bool(args.high_signal),
                derived_substrings=derived,
            )
            out_path = out_monthly / f"TTAO_TOOLING_FORENSICS_{y:04d}_{m:02d}.md"
            write_month_md(out_path, rep)
            if args.progress:
                print(f"[month {y:04d}-{m:02d}] wrote {out_path} (duckdb_used={rep['counts']['duckdb_paths_used']})", flush=True)

            stacks = ",".join(rep.get("stacks") or [])
            fail_n = 0
            try:
                fail_n = int((rep.get("tests") or {}).get("status", {}).get("FAIL", 0))
            except Exception:
                fail_n = 0
            trip_n = sum(n for (_t, n) in (rep.get("tripwires") or {}).get("fail_by_tool", []))
            index_rows.append((f"{y:04d}-{m:02d}", rep["counts"]["duckdb_paths_used"], stacks, f"tests_fail={fail_n} tripwire_fail={trip_n}"))

        idx: list[str] = []
        idx.append("# Medallion: Bronze | Mutation: 0% | HIVE: V")
        idx.append("")
        idx.append("# TTao Tooling Forensics v1 (Index)")
        idx.append("")
        idx.append("## Provenance")
        idx.append(f"- Generated (UTC): {datetime.now(timezone.utc).isoformat().replace('+00:00','Z')}")
        idx.append(f"- DuckDB: {args.db}")
        idx.append(f"- MCP memory: {args.mcp}")
        idx.append(f"- Hot blackboard: {args.blackboard}")
        idx.append(f"- Range: {args.start} .. {args.end} (inclusive)")
        idx.append(f"- High-signal mode: {bool(args.high_signal)}")
        idx.append("")
        idx.append("## Months")
        idx.append("| month | duckdb_paths_used | inferred_stacks | fails | report |")
        idx.append("|---|---:|---|---|---|")
        for (month, used, stacks, fails) in index_rows:
            y, m = month.split("-")
            rel = f"monthly/TTAO_TOOLING_FORENSICS_{y}_{m}.md"
            idx.append(f"| {month} | {used} | {stacks or ''} | {fails} | [{rel}]({rel}) |")

        (out_root / "INDEX.md").write_text("\n".join(idx), encoding="utf-8")

    finally:
        con.close()

    print(out_root / "INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
