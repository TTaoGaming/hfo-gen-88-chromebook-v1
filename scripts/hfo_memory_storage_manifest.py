# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Generate a timestamped manifest of all memory/datastore surfaces in this repo.

Goal:
- Provide a machine-enforceable inventory for deprecation/consolidation.
- Make the blessed write-path explicit: doobidoo sqlite_vec SSOT.
- Treat Shodh as derived/on-demand (mirror index), never SSOT.

Outputs:
- YAML + JSON written under artifacts/memory_manifest/
- latest.yaml + latest.json updated as copies of the newest snapshot

Design notes:
- Prefer explicit pointer-resolved paths (hfo_pointers.json) for SSOT + core stores.
- Add a limited discovery pass for additional DB artifacts.
- Avoid enumerating every JSONL in the repo; summarize counts + sample paths.

"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _safe_rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except Exception:
        return str(path)


def _file_stat(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"exists": False}

    st = path.stat()
    mtime = datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).replace(microsecond=0)
    return {
        "exists": True,
        "size_bytes": int(st.st_size) if path.is_file() else None,
        "mtime_utc": mtime.isoformat().replace("+00:00", "Z"),
        "is_dir": path.is_dir(),
    }


def _load_pointers() -> Dict[str, Any]:
    pointers_path = REPO_ROOT / "hfo_pointers.json"
    with pointers_path.open("r", encoding="utf-8") as f:
        return json.load(f)


@dataclass(frozen=True)
class StoreSpec:
    store_id: str
    kind: str
    engine: str
    path: Optional[str] = None
    authoritative: bool = False
    write_policy: str = "read_only"
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


def _make_store(spec: StoreSpec) -> Dict[str, Any]:
    store: Dict[str, Any] = {
        "id": spec.store_id,
        "kind": spec.kind,
        "engine": spec.engine,
        "authoritative": bool(spec.authoritative),
        "write_policy": spec.write_policy,
    }
    if spec.path is not None:
        store["path"] = spec.path
        store["status"] = _file_stat(REPO_ROOT / spec.path)
    else:
        store["status"] = {"exists": False}
    if spec.tags:
        store["tags"] = list(spec.tags)
    if spec.notes:
        store["notes"] = spec.notes
    return store


def _discover_files(
    roots: Iterable[Path],
    suffixes: Tuple[str, ...],
    max_results: int,
    ignore_dirs: Tuple[str, ...],
) -> List[Path]:
    results: List[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            for name in filenames:
                p = Path(dirpath) / name
                if p.suffix.lower() in suffixes:
                    results.append(p)
                    if len(results) >= max_results:
                        return results
    return results


def _count_files(
    roots: Iterable[Path],
    suffixes: Tuple[str, ...],
    ignore_dirs: Tuple[str, ...],
    max_sample: int,
) -> Dict[str, Any]:
    count = 0
    sample: List[str] = []
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            for name in filenames:
                p = Path(dirpath) / name
                if p.suffix.lower() in suffixes:
                    count += 1
                    if len(sample) < max_sample:
                        sample.append(_safe_rel(p))
    return {"count": count, "sample_paths": sample}


def build_manifest() -> Dict[str, Any]:
    pointers = _load_pointers()
    paths = pointers.get("paths", {})
    services = pointers.get("services", {})

    stores: List[Dict[str, Any]] = []

    # Canonical SSOT + primary stores (pointer-resolved)
    stores.extend(
        [
            _make_store(
                StoreSpec(
                    store_id="doobidoo_sqlite_vec_ssot",
                    kind="memory_ssot",
                    engine="sqlite_vec",
                    path=paths.get("mcp_memory_ssot_sqlite"),
                    authoritative=True,
                    write_policy="blessed_write_path",
                    tags=["ssot", "blessed"],
                    notes="Single blessed write path. All other memory views are derived or legacy.",
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="duckdb_unified",
                    kind="analytics_snapshot",
                    engine="duckdb",
                    path=paths.get("duckdb_unified"),
                    authoritative=False,
                    write_policy="read_only",
                    tags=["duckdb"],
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="duckdb_file_index_merged",
                    kind="analytics_snapshot",
                    engine="duckdb",
                    path=paths.get("duckdb_file_index"),
                    authoritative=False,
                    write_policy="read_only",
                    tags=["duckdb", "file_index"],
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="shodh_derived_index_dir",
                    kind="derived_index",
                    engine="shodh",
                    path="artifacts/shodh_memory",
                    authoritative=False,
                    write_policy="derived_rebuildable",
                    tags=["derived", "on_demand"],
                    notes="Derived mirror index; safe to delete/rebuild from SSOT.",
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="shodh_sync_state_gen88_v4",
                    kind="derived_index_state",
                    engine="json",
                    path=paths.get("shodh_sync_state_gen88_v4"),
                    authoritative=False,
                    write_policy="derived_rebuildable",
                    tags=["derived", "sync_state"],
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="blackboard_hot_legacy",
                    kind="stigmergy_blackboard",
                    engine="jsonl",
                    path=paths.get("blackboard_legacy"),
                    authoritative=False,
                    write_policy="append_only_telemetry",
                    tags=["stigmergy", "telemetry"],
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="blackboard_hot_forge_v4",
                    kind="stigmergy_blackboard",
                    engine="jsonl",
                    path=paths.get("blackboard_hot_forge"),
                    authoritative=False,
                    write_policy="append_only_telemetry",
                    tags=["stigmergy", "telemetry"],
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="blackboard_hot_forge_legacy",
                    kind="stigmergy_blackboard",
                    engine="jsonl",
                    path=paths.get("blackboard_hot_forge_legacy"),
                    authoritative=False,
                    write_policy="deprecated",
                    tags=["stigmergy", "legacy"],
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="blackboard_cold_forge",
                    kind="stigmergy_blackboard",
                    engine="jsonl",
                    path=paths.get("blackboard_cold_forge"),
                    authoritative=False,
                    write_policy="append_only_telemetry",
                    tags=["stigmergy", "telemetry"],
                )
            ),
            _make_store(
                StoreSpec(
                    store_id="legacy_mcp_memory_jsonl",
                    kind="legacy_memory_ledger",
                    engine="jsonl",
                    path=paths.get("mcp_memory"),
                    authoritative=False,
                    write_policy="deprecated_no_write",
                    tags=["legacy"],
                    notes="Legacy MCP memory ledger. Do not append; use doobidoo SSOT instead.",
                )
            ),
        ]
    )

    # Known legacy sqlite file (pre-gen88_v4)
    stores.append(
        _make_store(
            StoreSpec(
                store_id="doobidoo_sqlite_vec_legacy_db",
                kind="legacy_memory_store",
                engine="sqlite_vec",
                path="artifacts/mcp_memory_service/sqlite_vec.db",
                authoritative=False,
                write_policy="deprecated",
                tags=["legacy"],
            )
        )
    )

    # Discovery pass: additional DB files that exist in-repo.
    ignore_dirs = (
        ".git",
        "node_modules",
        "__pycache__",
        "test-results",
        "Obsidian2025",
    )

    discovered_duckdb = _discover_files(
        roots=[REPO_ROOT],
        suffixes=(".duckdb",),
        max_results=50,
        ignore_dirs=ignore_dirs,
    )
    discovered_sqlite = _discover_files(
        roots=[REPO_ROOT / "artifacts"],
        suffixes=(".db", ".sqlite", ".sqlite3"),
        max_results=100,
        ignore_dirs=ignore_dirs,
    )

    def _already_listed(rel_path: str) -> bool:
        for s in stores:
            if s.get("path") == rel_path:
                return True
        return False

    for p in discovered_duckdb:
        rel = _safe_rel(p)
        if _already_listed(rel):
            continue
        stores.append(
            _make_store(
                StoreSpec(
                    store_id=f"duckdb_discovered:{rel}",
                    kind="analytics_snapshot",
                    engine="duckdb",
                    path=rel,
                    authoritative=False,
                    write_policy="read_only",
                    tags=["discovered"],
                )
            )
        )

    for p in discovered_sqlite:
        rel = _safe_rel(p)
        if _already_listed(rel):
            continue
        stores.append(
            _make_store(
                StoreSpec(
                    store_id=f"sqlite_discovered:{rel}",
                    kind="unknown_sqlite",
                    engine="sqlite",
                    path=rel,
                    authoritative=False,
                    write_policy="unknown",
                    tags=["discovered"],
                )
            )
        )

    # Summaries (avoid enumerating massive JSONL sets)
    jsonl_summary = _count_files(
        roots=[
            REPO_ROOT / "hfo_hot_obsidian",
            REPO_ROOT / "hfo_cold_obsidian",
            REPO_ROOT / "hfo_hot_obsidian_forge",
            REPO_ROOT / "hfo_cold_obsidian_forge",
            REPO_ROOT / "artifacts",
        ],
        suffixes=(".jsonl",),
        ignore_dirs=ignore_dirs,
        max_sample=20,
    )

    manifest: Dict[str, Any] = {
        "manifest_version": "hfo.memory_storage_manifest.v1",
        "generated_at_utc": _utc_now_iso(),
        "repo_root": str(REPO_ROOT),
        "policy": {
            "blessed_write_path": "doobidoo_sqlite_vec_ssot",
            "shodh_mirror": {
                "mode": "on_demand",
                "derived_from": "doobidoo_sqlite_vec_ssot",
                "service": services.get("shodh", {}),
            },
            "deprecated_write_paths": [
                "legacy_mcp_memory_jsonl",
                "doobidoo_sqlite_vec_legacy_db",
                "blackboard_hot_forge_legacy",
            ],
        },
        "stores": stores,
        "discovery": {
            "jsonl": jsonl_summary,
            "notes": "Discovery is summarized to avoid huge manifests; use targeted queries if you need full path enumeration.",
        },
    }

    return manifest


def write_manifest(out_dir: Path, write_latest: bool) -> Tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    yaml_path = out_dir / f"hfo_memory_storage_manifest_{ts}.yaml"
    json_path = out_dir / f"hfo_memory_storage_manifest_{ts}.json"

    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(manifest, f, sort_keys=False)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=False)
        f.write("\n")

    if write_latest:
        latest_yaml = out_dir / "latest.yaml"
        latest_json = out_dir / "latest.json"
        latest_yaml.write_text(yaml_path.read_text(encoding="utf-8"), encoding="utf-8")
        latest_json.write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")

    return yaml_path, json_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out-dir",
        default=str(REPO_ROOT / "artifacts" / "memory_manifest"),
        help="Output directory for manifest snapshots",
    )
    ap.add_argument(
        "--no-latest",
        action="store_true",
        help="Do not update artifacts/memory_manifest/latest.(yaml|json)",
    )
    args = ap.parse_args()

    yaml_path, json_path = write_manifest(
        Path(args.out_dir), write_latest=(not args.no_latest)
    )
    print(
        json.dumps(
            {"yaml": _safe_rel(yaml_path), "json": _safe_rel(json_path)}, indent=2
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
