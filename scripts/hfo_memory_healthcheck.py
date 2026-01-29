#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Antifragile memory health check (Doobidoo SSOT + Shodh).

Goals
- Fast, bounded, and non-destructive (read-only).
- Clear exit codes for automation.
- JSON output option for logs/CI.

Checks
- Doobidoo sqlite SSOT: file exists, can open read-only, `memories` table present,
  expected columns present, row counts.
- Shodh server: GET /health reachable with timeout.

Usage
- Human output:
    bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_healthcheck.py

- JSON output:
    bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_healthcheck.py --json

- Override endpoints:
    ... scripts/hfo_memory_healthcheck.py --sqlite-path /abs/path.db --shodh-url http://127.0.0.1:3030

Exit codes
- 0: all required checks OK
- 2: one or more checks failed
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


@dataclass(frozen=True)
class CheckResult:
    ok: bool
    name: str
    detail: dict[str, Any]


def _now_ms() -> int:
    return int(time.time() * 1000)


def _default_sqlite_path() -> str:
    env = os.getenv("MCP_MEMORY_SQLITE_PATH", "").strip()
    if env:
        return env
    try:
        from hfo_pointers import resolve_path

        return resolve_path(
            dotted_key="paths.mcp_memory_ssot_sqlite",
            env_var="MCP_MEMORY_SQLITE_PATH",
            default=str(
                _REPO_ROOT
                / "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"
            ),
        )
    except Exception:
        return str(
            _REPO_ROOT
            / "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"
        )


def _default_shodh_url() -> str:
    host = os.getenv("SHODH_HOST", "127.0.0.1")
    port = os.getenv("SHODH_PORT", "3030")
    return f"http://{host}:{port}"


def _safe_json_loads(s: str) -> Any:
    try:
        return json.loads(s)
    except Exception:
        return None


def _sqlite_connect_readonly(
    sqlite_path: Path, *, timeout_sec: float
) -> sqlite3.Connection:
    # Prefer read-only URI mode to avoid accidental writes/locks.
    try:
        return sqlite3.connect(
            f"file:{sqlite_path.as_posix()}?mode=ro",
            uri=True,
            timeout=max(0.0, float(timeout_sec)),
        )
    except Exception:
        return sqlite3.connect(str(sqlite_path), timeout=max(0.0, float(timeout_sec)))


def _check_doobidoo_sqlite(
    *,
    sqlite_path: Path,
    sqlite_timeout_sec: float,
    deep_sqlite: bool = False,
) -> CheckResult:
    started = _now_ms()
    detail: dict[str, Any] = {
        "sqlite_path": str(sqlite_path),
        "exists": sqlite_path.exists(),
    }

    if not sqlite_path.exists():
        detail["error"] = "sqlite_path_missing"
        detail["elapsed_ms"] = _now_ms() - started
        return CheckResult(ok=False, name="doobidoo_sqlite", detail=detail)

    try:
        con = _sqlite_connect_readonly(sqlite_path, timeout_sec=sqlite_timeout_sec)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        if deep_sqlite:
            deep_started = _now_ms()
            rows = cur.execute("PRAGMA quick_check").fetchall()
            # Usually a single row: 'ok'. If not, include a small sample.
            detail["sqlite_quick_check"] = [r[0] for r in rows[:5]]
            detail["sqlite_quick_check_elapsed_ms"] = _now_ms() - deep_started

        tables = [
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name ASC"
            ).fetchall()
        ]
        detail["tables_count"] = len(tables)
        detail["has_memories_table"] = "memories" in set(tables)

        if "memories" not in set(tables):
            detail["error"] = "missing_memories_table"
            detail["elapsed_ms"] = _now_ms() - started
            return CheckResult(ok=False, name="doobidoo_sqlite", detail=detail)

        cols = [r[1] for r in cur.execute("PRAGMA table_info(memories)").fetchall()]
        required_cols = {
            "id",
            "content_hash",
            "content",
            "tags",
            "memory_type",
            "metadata",
            "deleted_at",
        }
        cols_set = set(cols)
        detail["memories_columns_present"] = sorted(list(cols_set & required_cols))
        detail["memories_columns_missing"] = sorted(list(required_cols - cols_set))

        # Counts are read-only. Keep it simple; do not scan content.
        total = cur.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        alive = cur.execute(
            "SELECT COUNT(*) FROM memories WHERE deleted_at IS NULL"
        ).fetchone()[0]
        detail["rows_total"] = int(total)
        detail["rows_alive"] = int(alive)

        max_id = cur.execute("SELECT MAX(id) FROM memories").fetchone()[0]
        detail["max_id"] = int(max_id) if max_id is not None else None

        # Best-effort timestamp columns (may not exist in older schemas).
        if "updated_at_iso" in cols_set:
            detail["max_updated_at_iso"] = cur.execute(
                "SELECT MAX(updated_at_iso) FROM memories"
            ).fetchone()[0]
        if "created_at_iso" in cols_set:
            detail["max_created_at_iso"] = cur.execute(
                "SELECT MAX(created_at_iso) FROM memories"
            ).fetchone()[0]

        con.close()

        ok = len(required_cols - cols_set) == 0
        detail["elapsed_ms"] = _now_ms() - started
        if not ok:
            detail["error"] = "schema_missing_required_columns"
        return CheckResult(ok=ok, name="doobidoo_sqlite", detail=detail)

    except Exception as e:
        detail["error"] = "sqlite_open_or_query_failed"
        detail["exception"] = f"{type(e).__name__}: {e}"
        detail["elapsed_ms"] = _now_ms() - started
        return CheckResult(ok=False, name="doobidoo_sqlite", detail=detail)


def _check_shodh_health(*, shodh_url: str, timeout_sec: float) -> CheckResult:
    started = _now_ms()
    detail: dict[str, Any] = {"shodh_url": shodh_url}

    try:
        resp = requests.get(
            f"{shodh_url.rstrip('/')}/health",
            timeout=max(0.5, float(timeout_sec)),
        )
        detail["http_status"] = int(resp.status_code)
        resp.raise_for_status()
        data = _safe_json_loads(resp.text)
        detail["body"] = data if isinstance(data, dict) else resp.text[:500]
        detail["elapsed_ms"] = _now_ms() - started

        ok = isinstance(data, dict) and data.get("status") == "healthy"
        if not ok:
            detail["error"] = "unhealthy_or_unexpected_response"
        return CheckResult(ok=ok, name="shodh_health", detail=detail)

    except Exception as e:
        detail["error"] = "shodh_unreachable"
        detail["exception"] = f"{type(e).__name__}: {e}"
        detail["elapsed_ms"] = _now_ms() - started
        return CheckResult(ok=False, name="shodh_health", detail=detail)


def _format_human(results: list[CheckResult]) -> str:
    lines: list[str] = []
    overall_ok = all(r.ok for r in results)
    lines.append(f"overall_ok={str(overall_ok).lower()}")

    for r in results:
        status = "OK" if r.ok else "FAIL"
        lines.append(f"[{status}] {r.name}")
        # Keep human output small and readable.
        for k in (
            "sqlite_path",
            "rows_alive",
            "rows_total",
            "max_id",
            "max_updated_at_iso",
            "shodh_url",
            "http_status",
        ):
            if k in r.detail:
                lines.append(f"  - {k}: {r.detail[k]}")
        if not r.ok and "error" in r.detail:
            lines.append(f"  - error: {r.detail.get('error')}")
            if "exception" in r.detail:
                lines.append(f"  - exception: {r.detail.get('exception')}")

    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Antifragile memory health check (Doobidoo + Shodh)"
    )
    ap.add_argument("--sqlite-path", default=_default_sqlite_path())
    ap.add_argument("--shodh-url", default=_default_shodh_url())
    ap.add_argument(
        "--timeout-sec", type=float, default=3.0, help="HTTP timeout seconds"
    )
    ap.add_argument(
        "--sqlite-timeout-sec",
        type=float,
        default=0.2,
        help="SQLite connect/query timeout seconds",
    )
    ap.add_argument(
        "--ssot-only",
        action="store_true",
        help="Only require Doobidoo sqlite SSOT to be healthy (Shodh treated as optional/derived)",
    )
    ap.add_argument(
        "--deep-sqlite",
        action="store_true",
        help="Run PRAGMA quick_check on the sqlite SSOT (slower but read-only)",
    )
    ap.add_argument("--json", action="store_true", help="Emit JSON only")

    args = ap.parse_args(argv)

    results: list[CheckResult] = []
    results.append(
        _check_doobidoo_sqlite(
            sqlite_path=Path(args.sqlite_path),
            sqlite_timeout_sec=float(args.sqlite_timeout_sec),
            deep_sqlite=bool(args.deep_sqlite),
        )
    )
    if not args.ssot_only:
        results.append(
            _check_shodh_health(
                shodh_url=str(args.shodh_url),
                timeout_sec=float(args.timeout_sec),
            )
        )

    overall_ok = all(r.ok for r in results)
    payload = {
        "overall_ok": overall_ok,
        "checks": [asdict(r) for r in results],
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(_format_human(results), end="")

    return 0 if overall_ok else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
