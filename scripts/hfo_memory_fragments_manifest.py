#!/usr/bin/env python3
"""Medallion: Silver | Mutation: N/A | HIVE: V

Gen88 memory fragments manifest.

Purpose
  - Inventory all memory-related storage artifacts in the repo (SSOT / derived / legacy).
  - Produce a timestamped YAML manifest with sizes and metadata.
  - Optionally lock JSONL fragments read-only (chmod a-w).

Ground truth inputs
  - artifacts/memory_manifest/latest.json (policy + known stores)
  - hfo_pointers.json (blessed paths)

Notes
  - The blessed write SSOT is the Doobidoo sqlite_vec DB from pointers/manifest.
  - Shodh is a derived index; JSONL ledgers/blackboards are legacy/telemetry and can be locked read-only.
"""

from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclasses.dataclass(frozen=True)
class Fragment:
    path: str
    kind: str
    engine: str
    authoritative: bool
    write_policy: str
    classification: str
    size_bytes: int | None
    mtime_utc: str | None
    is_dir: bool
    mode_octal: str | None
    sha256: str | None
    notes: str | None


def _utc_iso_from_mtime(mtime: float) -> str:
    # Avoid importing datetime in hot path; ISO-8601 Z formatting.
    import datetime as _dt

    return (
        _dt.datetime.fromtimestamp(mtime, tz=_dt.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _safe_rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except Exception:
        return str(path)


def _stat_fragment(
    path: Path, compute_sha256_max_bytes: int
) -> tuple[int | None, str | None, bool, str | None, str | None]:
    try:
        st = path.stat()
    except FileNotFoundError:
        return None, None, False, None, None

    is_dir = path.is_dir()

    size_bytes: int | None
    if is_dir:
        size_bytes = _dir_size_bytes(path)
    else:
        size_bytes = st.st_size

    mtime_utc = _utc_iso_from_mtime(st.st_mtime)
    mode_octal = oct(st.st_mode & 0o777)

    sha256: str | None = None
    if not is_dir and size_bytes is not None and size_bytes <= compute_sha256_max_bytes:
        sha256 = _sha256_file(path)

    return size_bytes, mtime_utc, is_dir, mode_octal, sha256


def _dir_size_bytes(path: Path) -> int:
    total = 0
    # No symlink following.
    for root, dirs, files in os.walk(path, followlinks=False):
        root_p = Path(root)
        for name in files:
            try:
                fp = root_p / name
                if fp.is_symlink():
                    continue
                total += fp.stat().st_size
            except FileNotFoundError:
                continue
    return total


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _classify_path(
    rel_path: str, blessed_ssot: str | None, shodh_dir: str | None
) -> str:
    if blessed_ssot and rel_path == blessed_ssot:
        return "blessed_ssot"
    if shodh_dir and (
        rel_path == shodh_dir or rel_path.startswith(shodh_dir.rstrip("/") + "/")
    ):
        return "derived_shodh"
    if rel_path.endswith(".duckdb"):
        return "derived_analytics"
    if rel_path.endswith(".jsonl"):
        return "legacy_or_telemetry_jsonl"
    if rel_path.endswith("sqlite_vec.db"):
        return "legacy_sqlite_vec"
    return "other_fragment"


def _discover_by_globs(roots: list[Path], patterns: list[str]) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_dir():
                continue
            # Avoid treating derived symlink views (collections) as storage fragments.
            if p.is_symlink():
                continue
            rel = _safe_rel(p)
            if any(fnmatch.fnmatch(rel, pat) for pat in patterns):
                if p not in seen:
                    seen.add(p)
                    found.append(p)
    return found


def _chmod_remove_write(path: Path, dry_run: bool) -> dict[str, Any]:
    result: dict[str, Any] = {"path": _safe_rel(path), "changed": False}
    try:
        st = path.stat()
    except FileNotFoundError:
        result["error"] = "missing"
        return result

    mode = st.st_mode & 0o777
    new_mode = mode & ~0o222
    if new_mode == mode:
        result["changed"] = False
        result["mode_before"] = oct(mode)
        result["mode_after"] = oct(mode)
        return result

    result["mode_before"] = oct(mode)
    result["mode_after"] = oct(new_mode)
    if not dry_run:
        os.chmod(path, new_mode)
    result["changed"] = True
    return result


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Generate a timestamped YAML manifest of Gen88 memory fragments."
    )
    ap.add_argument(
        "--out-dir",
        default="artifacts/memory_manifest",
        help="Output directory (repo-relative).",
    )
    ap.add_argument(
        "--compute-sha256-max-bytes",
        type=int,
        default=5 * 1024 * 1024,
        help="Compute sha256 for files up to this size.",
    )
    ap.add_argument(
        "--lock-jsonl",
        action="store_true",
        help="Remove write bits from memory-related JSONL files (chmod a-w).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not modify filesystem; still generate manifest.",
    )
    args = ap.parse_args()

    manifest_latest = _load_json(REPO_ROOT / "artifacts/memory_manifest/latest.json")
    pointers = _load_json(REPO_ROOT / "hfo_pointers.json")

    blessed_ssot: str | None = None
    shodh_dir: str | None = None
    if pointers:
        blessed_ssot = pointers.get("paths", {}).get("mcp_memory_ssot_sqlite")
        shodh_dir = "artifacts/shodh_memory"

    if manifest_latest:
        # Prefer the manifest if present.
        for store in manifest_latest.get("stores", []):
            if store.get("id") == "doobidoo_sqlite_vec_ssot":
                blessed_ssot = store.get("path") or blessed_ssot
            if store.get("id") == "shodh_derived_index_dir":
                shodh_dir = store.get("path") or shodh_dir

    scan_roots = [
        REPO_ROOT / "artifacts",
        REPO_ROOT / "hfo_hot_obsidian",
        REPO_ROOT / "hfo_hot_obsidian_forge",
        REPO_ROOT / "hfo_cold_obsidian",
        REPO_ROOT / "hfo_cold_obsidian_forge",
        REPO_ROOT / "hfo_gen_88_cb_v2",
        REPO_ROOT
        / "hfo_hot_obsidian/bronze/3_resources/ingest_sources/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52",
    ]

    patterns = [
        "**/*.db",
        "**/*.sqlite",
        "**/*.sqlite3",
        "**/*.duckdb",
        "**/*.jsonl",
        "**/*.ndjson",
        "**/*.parquet",
        "**/*.csv",
        "**/sync_state_*.json",
    ]

    discovered_files = _discover_by_globs(scan_roots, patterns)

    # Also include directory fragments we care about (like shodh index dir).
    discovered_dirs: list[Path] = []
    if shodh_dir:
        p = REPO_ROOT / shodh_dir
        if p.exists() and p.is_dir():
            discovered_dirs.append(p)

    fragments: list[Fragment] = []

    # Seed from latest.json stores so known ground truth gets stable IDs.
    seeded_paths: set[str] = set()
    if manifest_latest:
        for store in manifest_latest.get("stores", []):
            rel = store.get("path")
            if not isinstance(rel, str):
                continue
            p = REPO_ROOT / rel
            # Don’t treat symlink views as storage fragments.
            if p.is_symlink():
                continue
            size_bytes, mtime_utc, is_dir, mode_octal, sha256 = _stat_fragment(
                p,
                compute_sha256_max_bytes=args.compute_sha256_max_bytes,
            )
            fragments.append(
                Fragment(
                    path=rel,
                    kind=str(store.get("kind") or "unknown"),
                    engine=str(store.get("engine") or "unknown"),
                    authoritative=bool(store.get("authoritative")),
                    write_policy=str(store.get("write_policy") or "unknown"),
                    classification=_classify_path(rel, blessed_ssot, shodh_dir),
                    size_bytes=size_bytes,
                    mtime_utc=mtime_utc,
                    is_dir=bool(is_dir),
                    mode_octal=mode_octal,
                    sha256=sha256,
                    notes=store.get("notes"),
                )
            )
            seeded_paths.add(rel)

    for p in discovered_files:
        rel = _safe_rel(p)
        if rel in seeded_paths:
            continue
        size_bytes, mtime_utc, is_dir, mode_octal, sha256 = _stat_fragment(
            p,
            compute_sha256_max_bytes=args.compute_sha256_max_bytes,
        )
        fragments.append(
            Fragment(
                path=rel,
                kind="discovered",
                engine=(p.suffix.lstrip(".") or "unknown"),
                authoritative=False,
                write_policy="unknown",
                classification=_classify_path(rel, blessed_ssot, shodh_dir),
                size_bytes=size_bytes,
                mtime_utc=mtime_utc,
                is_dir=bool(is_dir),
                mode_octal=mode_octal,
                sha256=sha256,
                notes=None,
            )
        )

    for d in discovered_dirs:
        rel = _safe_rel(d)
        if rel in seeded_paths:
            continue
        size_bytes, mtime_utc, is_dir, mode_octal, sha256 = _stat_fragment(
            d,
            compute_sha256_max_bytes=args.compute_sha256_max_bytes,
        )
        fragments.append(
            Fragment(
                path=rel,
                kind="discovered_dir",
                engine="dir",
                authoritative=False,
                write_policy="derived_rebuildable"
                if shodh_dir and rel.startswith(shodh_dir)
                else "unknown",
                classification=_classify_path(rel, blessed_ssot, shodh_dir),
                size_bytes=size_bytes,
                mtime_utc=mtime_utc,
                is_dir=True,
                mode_octal=mode_octal,
                sha256=sha256,
                notes=None,
            )
        )

    # Build lock list (memory JSONL only).
    lock_targets: list[str] = []
    for frag in fragments:
        if frag.path.endswith(".jsonl"):
            lock_targets.append(frag.path)

    lock_actions: list[dict[str, Any]] = []
    if args.lock_jsonl:
        for rel in sorted(set(lock_targets)):
            lock_actions.append(
                _chmod_remove_write(REPO_ROOT / rel, dry_run=args.dry_run)
            )

    # Emit YAML.
    import datetime as dt

    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y_%m_%dT%H%M%SZ")
    out_dir = REPO_ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"hfo_memory_fragments_gen88_v4_{ts}.yaml"

    doc: dict[str, Any] = {
        "manifest_version": "hfo.memory_fragments_manifest.v1",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "repo_root": str(REPO_ROOT),
        "inputs": {
            "storage_manifest_latest_json": "artifacts/memory_manifest/latest.json"
            if manifest_latest
            else None,
            "pointers": "hfo_pointers.json" if pointers else None,
        },
        "policy": (manifest_latest or {}).get("policy"),
        "blessed": {
            "doobidoo_sqlite_vec_ssot": blessed_ssot,
            "shodh_dir": shodh_dir,
        },
        "fragments": [
            dataclasses.asdict(f) for f in sorted(fragments, key=lambda x: x.path)
        ],
        "jsonl_lock": {
            "requested": bool(args.lock_jsonl),
            "dry_run": bool(args.dry_run),
            "targets": sorted(set(lock_targets)),
            "actions": lock_actions,
            "note": "JSONL is legacy/telemetry; with lock enabled this makes JSONL effectively read-only at the filesystem level.",
        },
    }

    out_path.write_text(
        yaml.safe_dump(doc, sort_keys=False, width=110), encoding="utf-8"
    )
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
