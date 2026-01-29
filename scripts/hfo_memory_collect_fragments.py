#!/usr/bin/env python3
"""Medallion: Silver | Mutation: N/A | HIVE: V

Create a consolidated view of memory fragments under Hot Obsidian Forge (Bronze resources).

This script does NOT move data. It creates a stable, obvious directory that contains:
  - symlinks (or fallback pointer text files) to all known memory fragments
  - an index YAML describing what was linked

Source of truth is the latest fragments manifest produced by:
  scripts/hfo_memory_fragments_manifest.py
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


_SAFE_CHARS_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _short_safe_name(rel: str) -> str:
    """Return a filesystem-safe filename for a fragment.

    Avoids Linux filename limits by not embedding full paths.
    """

    p = Path(rel)
    base = p.name or "fragment"

    # Preserve extension when possible.
    suffix = "".join(p.suffixes)
    stem = base[: -len(suffix)] if suffix and base.endswith(suffix) else base

    stem = _SAFE_CHARS_RE.sub("_", stem).strip("._-") or "fragment"
    suffix = _SAFE_CHARS_RE.sub("_", suffix)

    digest = hashlib.sha1(rel.encode("utf-8"), usedforsecurity=False).hexdigest()[:12]
    stem = stem[:80]
    suffix = suffix[:20]

    return f"{stem}__{digest}{suffix}"


def _find_latest_manifest(manifest_dir: Path) -> Path | None:
    candidates = sorted(manifest_dir.glob("hfo_memory_fragments_gen88_v4_*.yaml"))
    if not candidates:
        return None
    return candidates[-1]


def _safe_load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _symlink_or_pointer(src: Path, dst: Path) -> dict[str, Any]:
    # Return an action record.
    action: dict[str, Any] = {
        "src": str(src),
        "dst": str(dst),
        "method": None,
        "ok": False,
        "error": None,
    }

    if dst.exists() or dst.is_symlink():
        try:
            if dst.is_symlink() or dst.is_file():
                dst.unlink()
            elif dst.is_dir():
                # Don’t delete dirs; caller should use a clean collection root.
                action["error"] = "dst_is_dir"
                return action
        except Exception as e:
            action["error"] = f"unlink_failed:{type(e).__name__}:{e}"
            return action

    try:
        dst.symlink_to(src)
        action["method"] = "symlink"
        action["ok"] = True
        return action
    except Exception as e:
        # Fallback to pointer file (some environments restrict symlinks).
        try:
            dst.write_text(f"pointer:\n  src: {src}\n", encoding="utf-8")
            action["method"] = "pointer_file"
            action["ok"] = True
            action["error"] = f"symlink_failed:{type(e).__name__}:{e}"
            return action
        except Exception as e2:
            action["error"] = f"symlink_and_pointer_failed:{type(e2).__name__}:{e2}"
            return action


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Create a consolidated memory fragments collection directory."
    )
    ap.add_argument(
        "--manifest",
        default="",
        help="Path to a fragments manifest YAML. If omitted, uses the latest in artifacts/memory_manifest/.",
    )
    ap.add_argument(
        "--out-root",
        default="hfo_hot_obsidian_forge/0_bronze/2_resources/memory_fragments_collection",
        help="Output collection root (repo-relative).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not create links; just produce the index.",
    )
    args = ap.parse_args()

    manifest_dir = REPO_ROOT / "artifacts/memory_manifest"
    manifest_path = (
        Path(args.manifest) if args.manifest else _find_latest_manifest(manifest_dir)
    )
    if manifest_path is None:
        raise SystemExit(
            "No fragments manifest found. Run scripts/hfo_memory_fragments_manifest.py first."
        )
    if not manifest_path.is_absolute():
        manifest_path = (REPO_ROOT / manifest_path).resolve()

    doc = _safe_load_yaml(manifest_path)
    fragments = doc.get("fragments", [])
    if not isinstance(fragments, list):
        raise SystemExit("Invalid manifest: fragments is not a list")

    out_root = (REPO_ROOT / args.out_root).resolve()
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y_%m_%dT%H%M%SZ")
    run_dir = out_root / f"run_{ts}"

    actions: list[dict[str, Any]] = []
    by_class: dict[str, int] = {}

    if not args.dry_run:
        _ensure_dir(run_dir)

    for frag in fragments:
        if not isinstance(frag, dict):
            continue
        rel = frag.get("path")
        if not isinstance(rel, str) or not rel:
            continue

        classification = frag.get("classification")
        if not isinstance(classification, str) or not classification:
            classification = "unclassified"

        by_class[classification] = by_class.get(classification, 0) + 1

        src = (REPO_ROOT / rel).resolve()
        # Avoid name collisions and filename-too-long issues.
        safe_name = _short_safe_name(rel)
        dst_dir = run_dir / classification
        dst = dst_dir / safe_name

        if args.dry_run:
            actions.append(
                {
                    "src": str(src),
                    "dst": str(dst),
                    "method": "dry_run",
                    "ok": True,
                    "error": None,
                }
            )
            continue

        _ensure_dir(dst_dir)
        actions.append(_symlink_or_pointer(src, dst))

    index = {
        "collection_version": "hfo.memory_fragments_collection.v1",
        "generated_at_utc": dt.datetime.now(dt.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "manifest_source": str(manifest_path),
        "out_root": str(out_root),
        "run_dir": str(run_dir),
        "counts_by_classification": by_class,
        "actions": actions,
        "note": "This is a *view* (symlinks/pointers). SSOT remains the Doobidoo sqlite_vec DB; Shodh/DuckDB/JSONL are derived or legacy.",
    }

    if not args.dry_run:
        (run_dir / "index.yaml").write_text(
            yaml.safe_dump(index, sort_keys=False, width=110), encoding="utf-8"
        )
    else:
        # Emit index to stdout in dry-run.
        print(yaml.safe_dump(index, sort_keys=False, width=110))
        return 0

    print(str(run_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
