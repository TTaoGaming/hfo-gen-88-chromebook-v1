# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Warn-only structural validator for the HFO 2×4×4 forge layout.

Goal
- One command that reports drift vs the SSOT YAML spec.
- No file moves; no modifications; warnings by default.

Primary inputs
- HFO folder-structure spec YAML (SSOT)
- hfo_pointers.json (pointer registry)

This validator is intentionally structural, not semantic.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml

# Ensure repo root is importable when running from scripts/.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from hfo_blackboard_events import emit_cloudevent_to_blackboard

try:
    from hfo_pointers import resolve_path
except Exception:  # pragma: no cover
    resolve_path = None


@dataclass(frozen=True)
class Finding:
    severity: str  # INFO | WARN | ERROR
    check_id: str
    message: str
    path: Optional[str] = None


def _as_posix(path: Path) -> str:
    return path.as_posix()


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Spec is not a mapping: {path}")
    return data


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"JSON is not a mapping: {path}")
    return data


def _get_nested(obj: Dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    cur: Any = obj
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def _collect_expected_leaf_dirs(
    forges: List[str], layers: List[str], paras: List[str]
) -> List[str]:
    expected: List[str] = []
    for forge in forges:
        for layer in layers:
            for para in paras:
                expected.append(f"{forge}/{layer}/{para}")
    return expected


def check_forge_skeleton(
    repo_root: Path, forges: List[str], layers: List[str], paras: List[str]
) -> List[Finding]:
    findings: List[Finding] = []

    for forge in forges:
        forge_path = repo_root / forge
        if not forge_path.exists():
            findings.append(
                Finding(
                    severity="WARN",
                    check_id="skeleton_exists",
                    message=f"Missing forge root: {forge}",
                    path=_as_posix(forge_path),
                )
            )
            continue
        if not forge_path.is_dir():
            findings.append(
                Finding(
                    severity="WARN",
                    check_id="skeleton_exists",
                    message=f"Forge root is not a directory: {forge}",
                    path=_as_posix(forge_path),
                )
            )
            continue

        # Expected layers
        for layer in layers:
            layer_path = forge_path / layer
            if not layer_path.is_dir():
                findings.append(
                    Finding(
                        severity="WARN",
                        check_id="skeleton_exists",
                        message=f"Missing layer dir: {forge}/{layer}",
                        path=_as_posix(layer_path),
                    )
                )
                continue

            # Expected PARA under each layer
            for para in paras:
                para_path = layer_path / para
                if not para_path.is_dir():
                    findings.append(
                        Finding(
                            severity="WARN",
                            check_id="skeleton_exists",
                            message=f"Missing PARA dir: {forge}/{layer}/{para}",
                            path=_as_posix(para_path),
                        )
                    )

        # Unexpected layer entries
        expected_layers = set(layers)
        for child in forge_path.iterdir():
            if child.is_dir() and child.name not in expected_layers:
                findings.append(
                    Finding(
                        severity="WARN",
                        check_id="skeleton_unexpected",
                        message=f"Unexpected directory under forge root: {forge}/{child.name}",
                        path=_as_posix(child),
                    )
                )

    return findings


def check_pointer_targets(
    repo_root: Path,
    pointers_path: Path,
    phase: str,
    allowed_prefixes_by_phase: Dict[str, List[str]],
) -> List[Finding]:
    findings: List[Finding] = []
    ptr = _load_json(pointers_path)

    allowed_prefixes = allowed_prefixes_by_phase.get(phase)
    if allowed_prefixes is None:
        findings.append(
            Finding(
                severity="WARN",
                check_id="pointers_phase_unknown",
                message=f"Unknown phase '{phase}'; falling back to P0 prefix rules",
            )
        )
        allowed_prefixes = allowed_prefixes_by_phase.get("P0", [])

    def _check_target(pointer_id: str, target: str) -> None:
        target_path = repo_root / target
        if not target_path.exists():
            findings.append(
                Finding(
                    severity="WARN",
                    check_id="pointers_resolve",
                    message=f"Pointer target missing: {pointer_id} -> {target}",
                    path=_as_posix(target_path),
                )
            )

        if allowed_prefixes:
            if not any(target.startswith(prefix) for prefix in allowed_prefixes):
                findings.append(
                    Finding(
                        severity="WARN",
                        check_id="pointers_prefix",
                        message=(
                            f"Pointer target not in allowed prefixes for {phase}: {pointer_id} -> {target}"
                        ),
                        path=target,
                    )
                )

    targets = ptr.get("targets", {})
    paths = ptr.get("paths", {})

    if isinstance(targets, dict):
        for pointer_id, target in targets.items():
            if isinstance(target, str):
                _check_target(pointer_id, target)

    if isinstance(paths, dict):
        for pointer_id, target in paths.items():
            if isinstance(target, str):
                _check_target(pointer_id, target)

    return findings


def check_root_inventory(
    repo_root: Path,
    spec: Dict[str, Any],
    *,
    include_files: bool,
    ignore_root_names: set[str],
    max_items: int,
    clutter_threshold: int,
) -> List[Finding]:
    findings: List[Finding] = []

    allowed_root_items = set(
        _get_nested(spec, ["root_shim", "allowed_root_items"], default=[]) or []
    )

    forges = set(_get_nested(spec, ["canonical_layout", "forges"], default=[]) or [])

    # Paths explicitly acknowledged by path_mapping (avoid noise in warn-only stage).
    mapping_entries = _get_nested(spec, ["path_mapping", "entries"], default=[]) or []
    mapped_roots: set[str] = set()
    if isinstance(mapping_entries, list):
        for entry in mapping_entries:
            if isinstance(entry, dict):
                cur = entry.get("current_path")
                if isinstance(cur, str) and cur.endswith("/"):
                    mapped_roots.add(cur[:-1])

    # Always ignore common dotfiles.
    ignored_prefixes = (".",)

    unknown_dirs: List[Path] = []
    unknown_files: List[Path] = []

    for child in repo_root.iterdir():
        name = child.name
        if name.startswith(ignored_prefixes):
            continue

        if name in ignore_root_names:
            continue

        if name in forges:
            continue

        if name in allowed_root_items:
            continue

        if name in mapped_roots:
            # acknowledged legacy/kept root
            continue

        if child.is_dir():
            unknown_dirs.append(child)
        elif include_files:
            unknown_files.append(child)

    unknown_dirs.sort(key=lambda p: p.name)
    unknown_files.sort(key=lambda p: p.name)

    total_unknown = len(unknown_dirs) + len(unknown_files)
    if total_unknown >= clutter_threshold:
        findings.append(
            Finding(
                severity="WARN",
                check_id="root_clutter_count",
                message=(
                    f"Root clutter detected: {total_unknown} unaccounted items "
                    f"(dirs={len(unknown_dirs)}, files={len(unknown_files)}). "
                    "Add to root_shim.allowed_root_items or path_mapping.entries if intentional."
                ),
                path=_as_posix(repo_root),
            )
        )

    # Emit per-item warnings (capped)
    remaining = max_items
    for d in unknown_dirs:
        if remaining <= 0:
            break
        findings.append(
            Finding(
                severity="WARN",
                check_id="root_unknown_dir",
                message=f"Root directory not accounted for by spec/root_shim/path_mapping: {d.name}",
                path=_as_posix(d),
            )
        )
        remaining -= 1

    for f in unknown_files:
        if remaining <= 0:
            break
        suffix = f.suffix.lower()
        category = (
            "doc"
            if suffix in {".md", ".txt"}
            else "spec"
            if suffix in {".yaml", ".yml", ".json"}
            else "code"
            if suffix in {".py", ".ts", ".js"}
            else "asset"
            if suffix in {".html", ".png", ".svg"}
            else "file"
        )
        findings.append(
            Finding(
                severity="WARN",
                check_id="root_unknown_file",
                message=f"Root {category} file not accounted for by spec/root_shim/path_mapping: {f.name}",
                path=_as_posix(f),
            )
        )
        remaining -= 1

    if total_unknown > max_items:
        findings.append(
            Finding(
                severity="WARN",
                check_id="root_unknown_truncated",
                message=f"Root slop output truncated: showed {max_items} of {total_unknown} unknown items",
                path=_as_posix(repo_root),
            )
        )

    return findings


def check_alias_table(spec: Dict[str, Any]) -> List[Finding]:
    findings: List[Finding] = []
    alias_rows = _get_nested(spec, ["aliases_and_compat", "alias_table"], default=[]) or []
    if not isinstance(alias_rows, list):
        return findings

    for row in alias_rows:
        if not isinstance(row, dict):
            continue
        enabled = bool(row.get("enabled", False))
        if not enabled:
            continue
        alias_id = row.get("id", "(missing id)")
        sunset = row.get("sunset_utc")
        if not sunset:
            findings.append(
                Finding(
                    severity="WARN",
                    check_id="alias_missing_sunset",
                    message=f"Enabled alias missing sunset_utc: {alias_id}",
                )
            )

    return findings


def build_report(
    repo_root: Path,
    spec_path: Path,
    pointers_path: Path,
    phase: str,
    *,
    include_files: bool,
    ignore_root_names: set[str],
    max_items: int,
    clutter_threshold: int,
) -> Tuple[List[Finding], Dict[str, Any]]:
    spec = _load_yaml(spec_path)

    forges = _get_nested(spec, ["canonical_layout", "forges"], default=[]) or []
    layers = _get_nested(spec, ["canonical_layout", "medallion_layers"], default=[]) or []
    paras = _get_nested(spec, ["canonical_layout", "para_folders"], default=[]) or []

    allowed_prefixes_by_phase = (
        _get_nested(spec, ["pointers", "schema", "allowed_target_prefixes_by_phase"], default={})
        or {}
    )

    findings: List[Finding] = []
    findings.extend(check_forge_skeleton(repo_root, list(forges), list(layers), list(paras)))
    findings.extend(check_pointer_targets(repo_root, pointers_path, phase, allowed_prefixes_by_phase))
    findings.extend(
        check_root_inventory(
            repo_root,
            spec,
            include_files=include_files,
            ignore_root_names=ignore_root_names,
            max_items=max_items,
            clutter_threshold=clutter_threshold,
        )
    )
    findings.extend(check_alias_table(spec))

    meta = {
        "repo_root": _as_posix(repo_root),
        "spec_path": _as_posix(spec_path),
        "pointers_path": _as_posix(pointers_path),
        "phase": phase,
        "expected_leaf_dirs": _collect_expected_leaf_dirs(list(forges), list(layers), list(paras)),
    }

    return findings, meta


def _print_human(findings: List[Finding], meta: Dict[str, Any]) -> None:
    warn = [f for f in findings if f.severity == "WARN"]
    err = [f for f in findings if f.severity == "ERROR"]
    info = [f for f in findings if f.severity == "INFO"]

    print("HFO Structure Validator (warn-only)")
    print(f"- repo_root: {meta['repo_root']}")
    print(f"- spec: {meta['spec_path']}")
    print(f"- pointers: {meta['pointers_path']}")
    print(f"- phase: {meta['phase']}")
    print(f"- findings: WARN={len(warn)} ERROR={len(err)} INFO={len(info)}")

    def _dump(label: str, items: List[Finding]) -> None:
        if not items:
            return
        print(f"\n{label}:")
        for f in items:
            suffix = f" ({f.path})" if f.path else ""
            print(f"- [{f.check_id}] {f.message}{suffix}")

    _dump("WARN", warn)
    _dump("ERROR", err)


def _utc_now_compact() -> str:
    # Filesystem-safe timestamp
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _write_artifact_json(path: Path, payload: Dict[str, Any]) -> None:
    _ensure_parent(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_blackboard_event(
    *,
    blackboard_path: Path,
    artifact_path: str,
    phase: str,
    findings: List[Finding],
) -> None:
    warn_count = sum(1 for f in findings if f.severity == "WARN")
    error_count = sum(1 for f in findings if f.severity == "ERROR")

    top = [
        {"check_id": f.check_id, "message": f.message, "path": f.path, "severity": f.severity}
        for f in findings[:10]
    ]

    emit_cloudevent_to_blackboard(
        event_type="hfo.structure_validator.report",
        source="hfo://scripts/hfo_structure_validator",
        subject="hfo_structure_validator",
        data={
            "phase": phase,
            "artifact_path": artifact_path,
            "counts": {"warn": warn_count, "error": error_count, "total": len(findings)},
            "top_findings": top,
        },
        extensions={
            "dataschema": "contracts/hfo_blackboard_cloudevent.zod.ts",
        },
        blackboard_path=blackboard_path,
    )


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Warn-only validator for HFO 2x4x4 forge layout")

    default_spec = "HFO_ALPHA_FOLDER_STRUCTURE_V1_SPEC_2026_01_26.yaml"
    if resolve_path:
        default_spec = resolve_path(
            dotted_key="targets.alpha_folder_structure_spec_v1",
            default=default_spec,
        )

    ap.add_argument(
        "--spec",
        default=default_spec,
        help="Path to SSOT YAML spec",
    )
    ap.add_argument(
        "--pointers",
        default="hfo_pointers.json",
        help="Path to pointer registry JSON",
    )
    ap.add_argument("--repo-root", default=".", help="Repo root directory")
    ap.add_argument(
        "--phase",
        default="P0",
        choices=["P0", "P1", "P2", "P3"],
        help="Migration phase (controls pointer prefix warnings)",
    )
    ap.add_argument(
        "--artifact-out",
        default=None,
        help="Write JSON report artifact to this path (default: artifacts/forensics/hfo_structure_validator_<ts>.json)",
    )
    ap.add_argument(
        "--blackboard-out",
        default=None,
        help=(
            "Append a signed CloudEvent JSONL line to this blackboard. "
            "Default resolves from hfo_pointers.json (paths.blackboard_hot_forge or paths.blackboard)."
        ),
    )
    ap.add_argument(
        "--no-blackboard",
        action="store_true",
        help="Do not append to blackboard (artifact/stdout only)",
    )
    ap.add_argument(
        "--directories-only",
        action="store_true",
        help="Only warn on root directories (suppress root file slop warnings)",
    )
    ap.add_argument(
        "--ignore-root",
        action="append",
        default=["node_modules", "__pycache__", "Obsidian2025"],
        help="Root entry name to ignore (repeatable). Defaults ignore common generated/externals.",
    )
    ap.add_argument(
        "--max-items",
        type=int,
        default=75,
        help="Max number of per-item root slop warnings to print (prevents overwhelming output)",
    )
    ap.add_argument(
        "--clutter-threshold",
        type=int,
        default=10,
        help="Emit a root_clutter_count warning if unknown root items >= this number",
    )
    ap.add_argument("--json", action="store_true", help="Emit JSON report to stdout")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any WARN/ERROR findings exist",
    )

    args = ap.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    spec_path = (repo_root / args.spec).resolve() if not Path(args.spec).is_absolute() else Path(args.spec)
    pointers_path = (
        (repo_root / args.pointers).resolve()
        if not Path(args.pointers).is_absolute()
        else Path(args.pointers)
    )

    findings, meta = build_report(
        repo_root,
        spec_path,
        pointers_path,
        args.phase,
        include_files=not bool(args.directories_only),
        ignore_root_names=set(args.ignore_root or []),
        max_items=int(args.max_items),
        clutter_threshold=int(args.clutter_threshold),
    )

    artifact_default = Path("artifacts/forensics") / f"hfo_structure_validator_{_utc_now_compact()}.json"
    artifact_path = Path(args.artifact_out) if args.artifact_out else artifact_default
    artifact_path = (repo_root / artifact_path).resolve() if not artifact_path.is_absolute() else artifact_path

    artifact_payload = {
        "meta": meta,
        "findings": [
            {
                "severity": f.severity,
                "check_id": f.check_id,
                "message": f.message,
                "path": f.path,
            }
            for f in findings
        ],
    }
    _write_artifact_json(artifact_path, artifact_payload)

    if not args.no_blackboard:
        bb_out = args.blackboard_out
        if not bb_out:
            try:
                from hfo_pointers import resolve_path

                bb_out = resolve_path(
                    "paths.blackboard_hot_forge",
                    default=resolve_path(
                        "paths.blackboard",
                        default="hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard.jsonl",
                    ),
                )
            except Exception:
                bb_out = "hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard.jsonl"

        bb_path = Path(bb_out)
        bb_path = (repo_root / bb_path).resolve() if not bb_path.is_absolute() else bb_path
        _append_blackboard_event(
            blackboard_path=bb_path,
            artifact_path=str(artifact_path.relative_to(repo_root))
            if str(artifact_path).startswith(str(repo_root))
            else str(artifact_path),
            phase=args.phase,
            findings=findings,
        )

    if args.json:
        print(json.dumps(artifact_payload, indent=2, sort_keys=True))
    else:
        _print_human(findings, meta)
        print(f"\nartifact: {artifact_path}")

    if args.strict and findings:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
