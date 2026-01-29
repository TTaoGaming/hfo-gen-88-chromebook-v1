#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Memory overview (make it easy-mode).

Purpose
- One command answers: what is SSOT, what is derived, what is legacy.
- Output includes actionable guidance and the blessed entryways.

Usage
- Human output:
    bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py memory:overview

- JSON output:
    bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py memory:overview --json

Notes
- Grounded on `artifacts/memory_manifest/latest.(json|yaml)`.
- SSOT row counts are read from sqlite (read-only).
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from hfo_memory_guardrails import (  # noqa: E402
    format_entryways_text,
    get_blessed_entryways,
)


@dataclass(frozen=True)
class Overview:
    generated_at_iso: str
    manifest_path: str
    blessed_write_path: str | None
    ssot: dict[str, Any]
    derived: list[dict[str, Any]]
    legacy: list[dict[str, Any]]
    unknown: list[dict[str, Any]]
    guidance: dict[str, Any]


def _now_iso_local() -> str:
    # Local ISO for operator logs.
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _safe_read_text(path: Path, *, max_bytes: int = 5_000_000) -> str:
    data = path.read_bytes()
    if len(data) > max_bytes:
        raise ValueError(f"manifest too large ({len(data)} bytes)")
    return data.decode("utf-8")


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(str(path))

    if path.suffix.lower() == ".json":
        return json.loads(_safe_read_text(path))

    # YAML is optional; prefer the adjacent latest.json when possible.
    if path.suffix.lower() in {".yaml", ".yml"}:
        candidate_json = path.with_suffix(".json")
        if candidate_json.exists():
            return json.loads(_safe_read_text(candidate_json))
        try:
            import yaml  # type: ignore

            return yaml.safe_load(_safe_read_text(path))
        except Exception as e:
            raise RuntimeError(
                "manifest is YAML but PyYAML is unavailable; generate latest.json via: "
                "bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot manifest"
            ) from e

    raise ValueError(f"unsupported manifest extension: {path.suffix}")


def _sqlite_probe_counts(sqlite_path: Path, *, timeout_sec: float) -> dict[str, Any]:
    detail: dict[str, Any] = {
        "sqlite_path": str(sqlite_path),
        "exists": sqlite_path.exists(),
    }
    if not sqlite_path.exists():
        return detail

    started = time.time()

    def _connect_ro(p: Path) -> sqlite3.Connection:
        try:
            return sqlite3.connect(
                f"file:{p.as_posix()}?mode=ro",
                uri=True,
                timeout=max(0.0, float(timeout_sec)),
            )
        except Exception:
            return sqlite3.connect(str(p), timeout=max(0.0, float(timeout_sec)))

    try:
        con = _connect_ro(sqlite_path)
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        tables = [
            r[0]
            for r in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name ASC"
            ).fetchall()
        ]
        detail["tables_count"] = len(tables)
        detail["has_memories_table"] = "memories" in set(tables)

        if "memories" in set(tables):
            cols = [r[1] for r in cur.execute("PRAGMA table_info(memories)").fetchall()]
            cols_set = set(cols)
            detail["memories_columns"] = sorted(cols)

            total = cur.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            detail["rows_total"] = int(total)

            if "deleted_at" in cols_set:
                alive = cur.execute(
                    "SELECT COUNT(*) FROM memories WHERE deleted_at IS NULL"
                ).fetchone()[0]
                detail["rows_alive"] = int(alive)

            if "created_at_iso" in cols_set:
                detail["max_created_at_iso"] = cur.execute(
                    "SELECT MAX(created_at_iso) FROM memories"
                ).fetchone()[0]
            if "updated_at_iso" in cols_set:
                detail["max_updated_at_iso"] = cur.execute(
                    "SELECT MAX(updated_at_iso) FROM memories"
                ).fetchone()[0]

        con.close()
        detail["elapsed_ms"] = int((time.time() - started) * 1000)
        return detail

    except Exception as e:
        detail["error"] = "sqlite_probe_failed"
        detail["exception"] = f"{type(e).__name__}: {e}"
        detail["elapsed_ms"] = int((time.time() - started) * 1000)
        return detail


def _classify_stores(
    manifest: Mapping[str, Any],
) -> tuple[
    dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]
]:
    stores = manifest.get("stores", []) if isinstance(manifest, dict) else []
    if not isinstance(stores, list):
        stores = []

    ssot: dict[str, Any] = {}
    derived: list[dict[str, Any]] = []
    legacy: list[dict[str, Any]] = []
    unknown: list[dict[str, Any]] = []

    for s in stores:
        if not isinstance(s, dict):
            continue
        store_id = s.get("id")
        write_policy = s.get("write_policy")
        kind = s.get("kind")

        if store_id == "doobidoo_sqlite_vec_ssot" or (
            isinstance(s.get("authoritative"), bool) and s.get("authoritative") is True
        ):
            ssot = s
            continue

        if write_policy in {"derived_rebuildable"} or kind in {
            "derived_index",
            "derived_index_state",
            "analytics_snapshot",
        }:
            derived.append(s)
            continue

        if write_policy in {"deprecated", "deprecated_no_write"} or (
            isinstance(store_id, str) and store_id.startswith("legacy_")
        ):
            legacy.append(s)
            continue

        unknown.append(s)

    return ssot, derived, legacy, unknown


def _print_human(ov: Overview) -> None:
    print("[memory:overview] easy-mode")
    print(f"[memory:overview] generated_at={ov.generated_at_iso}")
    print(f"[memory:overview] manifest={ov.manifest_path}")

    if ov.blessed_write_path:
        print(f"[memory:overview] blessed_write_path={ov.blessed_write_path}")

    ssot_path = ov.ssot.get("path") if isinstance(ov.ssot, dict) else None
    ssot_status = ov.ssot.get("status") if isinstance(ov.ssot, dict) else None
    ssot_abs = None
    if isinstance(ssot_path, str) and ssot_path:
        ssot_abs = str((_REPO_ROOT / ssot_path).resolve())

    print("[memory:overview] SSOT (write-path)")
    if ssot_abs:
        print(f"  - path={ssot_abs}")
    if isinstance(ssot_status, dict):
        if "size_bytes" in ssot_status:
            print(f"  - size_bytes={ssot_status.get('size_bytes')}")
        if "mtime_utc" in ssot_status:
            print(f"  - mtime_utc={ssot_status.get('mtime_utc')}")

    probe = ov.ssot.get("probe") if isinstance(ov.ssot, dict) else None
    if isinstance(probe, dict) and probe.get("rows_total") is not None:
        print(
            f"  - rows_total={probe.get('rows_total')} rows_alive={probe.get('rows_alive')}"
        )

    print("[memory:overview] Derived / rebuildable")
    if not ov.derived:
        print("  - (none)")
    for s in ov.derived:
        print(f"  - {s.get('id')} → {s.get('path')}")

    print("[memory:overview] Legacy / no-write")
    if not ov.legacy:
        print("  - (none)")
    for s in ov.legacy:
        print(f"  - {s.get('id')} → {s.get('path')}")

    if ov.unknown:
        print("[memory:overview] Unknown/unclassified")
        for s in ov.unknown[:20]:
            print(
                f"  - {s.get('id')} → {s.get('path')} (write_policy={s.get('write_policy')})"
            )

    print("[memory:overview] Next steps")
    print(
        "  - overview: bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py memory:overview --json"
    )
    print("  - ingest (dry): use VS Code task ‘Memory: Ingest Text Dir (Dry Run)’")
    print("  - ingest (write): use VS Code task ‘Memory: Ingest Text Dir (Write)’")
    print("  - rebuild search: use VS Code task ‘Memory: Sync SSOT → Shodh’")
    print("")
    print(format_entryways_text(ov.guidance))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Memory overview (SSOT vs derived vs legacy)"
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON payload (stable for automation)",
    )
    ap.add_argument(
        "--manifest",
        default="",
        help="Override manifest path (defaults to pointers/env/latest)",
    )
    ap.add_argument(
        "--sqlite-timeout-sec",
        default="1.0",
        help="sqlite read timeout for probes",
    )
    args = ap.parse_args()

    guidance = get_blessed_entryways(repo_root=_REPO_ROOT, environ=os.environ)

    manifest_path_raw = str(args.manifest).strip()
    if manifest_path_raw:
        manifest_path = Path(manifest_path_raw)
        if not manifest_path.is_absolute():
            manifest_path = (_REPO_ROOT / manifest_path).resolve()
    else:
        # Use pointer-resolved path from guidance.
        p = guidance.get("paths", {}).get("manifest_latest")
        manifest_path = (
            Path(p)
            if isinstance(p, str) and p
            else (_REPO_ROOT / "artifacts/memory_manifest/latest.json")
        )

    try:
        manifest = _load_manifest(manifest_path)
    except Exception as e:
        payload = {
            "ok": False,
            "error": "manifest_load_failed",
            "exception": f"{type(e).__name__}: {e}",
            "manifest_path": str(manifest_path),
            "guidance": guidance,
        }
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=False))
        else:
            print("[memory:overview] ERROR: could not load storage manifest")
            print(f"[memory:overview] manifest={manifest_path}")
            print(f"[memory:overview] {payload['exception']}")
            print("[memory:overview] Fix: regenerate manifest via:")
            print(
                "  bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot manifest"
            )
            print("")
            print(format_entryways_text(guidance))
        return 2

    blessed_write_path = None
    policy = manifest.get("policy") if isinstance(manifest, dict) else None
    if isinstance(policy, dict):
        blessed_write_path = policy.get("blessed_write_path")

    ssot, derived, legacy, unknown = _classify_stores(manifest)

    # Attach SSOT probe (row counts) when possible.
    if isinstance(ssot, dict):
        rel = ssot.get("path")
        if isinstance(rel, str) and rel:
            sqlite_path = (_REPO_ROOT / rel).resolve()
            ssot["probe"] = _sqlite_probe_counts(
                sqlite_path, timeout_sec=float(args.sqlite_timeout_sec)
            )

    ov = Overview(
        generated_at_iso=_now_iso_local(),
        manifest_path=str(manifest_path),
        blessed_write_path=str(blessed_write_path) if blessed_write_path else None,
        ssot=ssot,
        derived=derived,
        legacy=legacy,
        unknown=unknown,
        guidance=guidance,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "ok": True,
                    "generated_at": ov.generated_at_iso,
                    "manifest": ov.manifest_path,
                    "blessed_write_path": ov.blessed_write_path,
                    "ssot": ov.ssot,
                    "derived": ov.derived,
                    "legacy": ov.legacy,
                    "unknown": ov.unknown,
                    "guidance": ov.guidance,
                },
                indent=2,
                sort_keys=False,
            )
        )
        return 0

    _print_human(ov)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
