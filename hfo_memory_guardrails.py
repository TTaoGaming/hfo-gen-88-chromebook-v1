#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Shared memory guardrails + entryways helpers for Gen88.

This module is intentionally dependency-free so it can be imported by:
- CLI scripts in `scripts/`
- ad-hoc operator helpers

Principle:
- Guide, don't punish: failures should be actionable and point to the blessed
  SSOT entryways (Doobidoo sqlite_vec) and the correct commands/tasks.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

from hfo_pointers import get_pointer, resolve_path

_DEFAULT_SSOT_REL = (
    "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"
)
_DEFAULT_MANIFEST_LATEST_REL = "artifacts/memory_manifest/latest.yaml"


def _normalize_path(repo_root: Path, raw: str) -> str:
    if not raw:
        return ""
    p = Path(str(raw)).expanduser()
    return str(p.resolve() if p.is_absolute() else (repo_root / p).resolve())


def _as_bool_env(v: str | None) -> bool:
    if v is None:
        return False
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


def get_blessed_entryways(
    *,
    repo_root: Path,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Return a small, structured "how to do it right" block."""

    env = environ or os.environ

    ssot_sqlite = resolve_path(
        "paths.mcp_memory_ssot_sqlite",
        env_var="MCP_MEMORY_SQLITE_PATH",
        default=str(repo_root / _DEFAULT_SSOT_REL),
        environ=env,
    )

    ssot_sqlite = _normalize_path(repo_root, ssot_sqlite)

    manifest_latest = resolve_path(
        "paths.memory_storage_manifest_latest",
        default=str(repo_root / _DEFAULT_MANIFEST_LATEST_REL),
        environ=env,
    )

    manifest_latest = _normalize_path(repo_root, manifest_latest)

    # Prefer pointers for display, but don't fail if missing.
    pointer_ssot_rel = get_pointer("paths.mcp_memory_ssot_sqlite", None)
    pointer_ssot_display = (
        str((repo_root / pointer_ssot_rel).resolve())
        if isinstance(pointer_ssot_rel, str) and pointer_ssot_rel
        else None
    )

    return {
        "paths": {
            "repo_root": str(repo_root),
            "ssot_sqlite": ssot_sqlite or None,
            "ssot_sqlite_pointer": pointer_ssot_display,
            "manifest_latest": manifest_latest or None,
        },
        "env": {
            "required": {
                "MCP_MEMORY_SQLITE_PATH": ssot_sqlite or "",
                "HFO_MCP_ENABLE_MCP_MEMORY_SERVICE": "1",
                "HFO_MCP_ENABLE_MEMORY": "0",
                "HFO_MCP_ENABLE_SHODH_MEMORY": "0",
            }
        },
        "commands": {
            "guardrails_check": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_guardrails.py",
            "manifest_snapshot": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_storage_manifest.py",
            "ingest_markdown_dir_dry": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_ingest_markdown_dir.py --dir <DIR> --tags gen88_v4 ssot",
            "ingest_markdown_dir_write": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_ingest_markdown_dir.py --dir <DIR> --tags gen88_v4 ssot --write",
            "ingest_text_dir_dry": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_ingest_text_dir.py --dir <DIR> --max-files 200 --max-bytes 2000000 --tags gen88_v4 ssot",
            "ingest_text_dir_write": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_ingest_text_dir.py --dir <DIR> --max-files 200 --max-bytes 2000000 --tags gen88_v4 ssot --write",
            "export_ssot": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_export_doobidoo_ssot.py --out <OUT.jsonl>",
            "import_jsonl_dry": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_import_jsonl_to_doobidoo.py --in <IN.jsonl>",
            "import_jsonl_write": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_import_jsonl_to_doobidoo.py --in <IN.jsonl> --write",
            "shodh_sync_from_ssot": "bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/shodh_sync_from_doobidoo_ssot.py",
        },
        "vscode_tasks": [
            "Memory: Ingest Text Dir (Dry Run)",
            "Memory: Ingest Text Dir (Write)",
            "Memory: Export Doobidoo SSOT → JSONL",
            "Memory: Import JSONL → Doobidoo SSOT (Dry Run)",
            "Memory: Import JSONL → Doobidoo SSOT (Write)",
            "Memory: Sync SSOT → Shodh (Dry Run)",
            "Memory: Sync SSOT → Shodh",
        ],
    }


def format_entryways_text(entryways: Mapping[str, Any]) -> str:
    paths = entryways.get("paths", {}) if isinstance(entryways, dict) else {}
    env = entryways.get("env", {}) if isinstance(entryways, dict) else {}
    required_env = env.get("required", {}) if isinstance(env, dict) else {}
    cmds = entryways.get("commands", {}) if isinstance(entryways, dict) else {}

    lines: list[str] = []
    lines.append("[memory] blessed entryways (SSOT-only)")
    if paths.get("ssot_sqlite"):
        lines.append(f"[memory] ssot_sqlite={paths['ssot_sqlite']}")
    if paths.get("manifest_latest"):
        lines.append(f"[memory] manifest_latest={paths['manifest_latest']}")

    lines.append("[memory] required env (minimal):")
    for k in [
        "MCP_MEMORY_SQLITE_PATH",
        "HFO_MCP_ENABLE_MCP_MEMORY_SERVICE",
        "HFO_MCP_ENABLE_MEMORY",
        "HFO_MCP_ENABLE_SHODH_MEMORY",
    ]:
        v = required_env.get(k, "")
        if k == "MCP_MEMORY_SQLITE_PATH" and v:
            lines.append(f"  export {k}='{v}'")
        else:
            lines.append(f"  export {k}='{v}'")

    lines.append("[memory] quick commands:")
    for key in [
        "guardrails_check",
        "manifest_snapshot",
        "ingest_markdown_dir_dry",
        "ingest_text_dir_dry",
        "export_ssot",
        "import_jsonl_dry",
        "shodh_sync_from_ssot",
    ]:
        cmd = cmds.get(key)
        if cmd:
            lines.append(f"  - {cmd}")

    return "\n".join(lines)


def check_guardrails(
    *,
    repo_root: Path,
    allow_shodh_mcp: bool = False,
    environ: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    env = environ or os.environ

    errors: list[str] = []
    warnings: list[str] = []

    # 1) Backends: enforce single write-path MCP memory service.
    if _as_bool_env(env.get("HFO_MCP_ENABLE_MEMORY")):
        errors.append(
            "HFO_MCP_ENABLE_MEMORY must be 0 (legacy JSONL MCP memory server disabled)"
        )

    if not _as_bool_env(env.get("HFO_MCP_ENABLE_MCP_MEMORY_SERVICE")):
        errors.append(
            "HFO_MCP_ENABLE_MCP_MEMORY_SERVICE must be 1 (Doobidoo SSOT write-path enabled)"
        )

    if _as_bool_env(env.get("HFO_MCP_ENABLE_SHODH_MEMORY")) and not allow_shodh_mcp:
        errors.append(
            "HFO_MCP_ENABLE_SHODH_MEMORY must be 0 by default (Shodh MCP adapter disabled; use HTTP recall + sync scripts)."
        )

    # 2) SSOT path: env must align with pointers.
    blessed = get_blessed_entryways(repo_root=repo_root, environ=env)
    blessed_ssot = (
        blessed.get("paths", {}).get("ssot_sqlite")
        if isinstance(blessed, dict)
        else None
    )

    pointer_ssot = (
        blessed.get("paths", {}).get("ssot_sqlite_pointer")
        if isinstance(blessed, dict)
        else None
    )
    env_ssot_raw = env.get("MCP_MEMORY_SQLITE_PATH")

    if not pointer_ssot:
        errors.append(
            "Missing pointers.paths.mcp_memory_ssot_sqlite in hfo_pointers.json"
        )

    if not env_ssot_raw:
        errors.append("Missing MCP_MEMORY_SQLITE_PATH env var")

    # If both are present, ensure they resolve to the same absolute path.
    if pointer_ssot and env_ssot_raw:
        env_ssot_abs = (
            str((repo_root / env_ssot_raw).resolve())
            if not Path(env_ssot_raw).is_absolute()
            else str(Path(env_ssot_raw).resolve())
        )
        if env_ssot_abs != str(Path(pointer_ssot).resolve()):
            errors.append(
                "MCP_MEMORY_SQLITE_PATH must match hfo_pointers.json paths.mcp_memory_ssot_sqlite: "
                f"env={env_ssot_abs} pointer={pointer_ssot}"
            )

    # 3) SSOT file existence.
    ssot_path = blessed_ssot
    if ssot_path and not Path(ssot_path).exists():
        errors.append(f"SSOT sqlite file does not exist: {ssot_path}")

    # 4) Optional: warn if legacy JSONL path is configured.
    legacy_mem_path = env.get("MEMORY_FILE_PATH")
    if legacy_mem_path:
        warnings.append(
            f"MEMORY_FILE_PATH is set (ok if server disabled): {legacy_mem_path}"
        )

    ok = len(errors) == 0

    return {
        "ok": ok,
        "errors": errors,
        "warnings": warnings,
        "repo_root": str(repo_root),
        "ssot": {
            "env": env.get("MCP_MEMORY_SQLITE_PATH"),
            "pointer": pointer_ssot,
            "blessed": blessed_ssot,
        },
        "flags": {
            "HFO_MCP_ENABLE_MEMORY": env.get("HFO_MCP_ENABLE_MEMORY"),
            "HFO_MCP_ENABLE_MCP_MEMORY_SERVICE": env.get(
                "HFO_MCP_ENABLE_MCP_MEMORY_SERVICE"
            ),
            "HFO_MCP_ENABLE_SHODH_MEMORY": env.get("HFO_MCP_ENABLE_SHODH_MEMORY"),
        },
        "guidance": blessed,
    }


def format_guardrails_human(payload: Mapping[str, Any]) -> str:
    ok = bool(payload.get("ok"))
    errors_obj = payload.get("errors")
    errors = errors_obj if isinstance(errors_obj, list) else []

    warnings_obj = payload.get("warnings")
    warnings = warnings_obj if isinstance(warnings_obj, list) else []

    lines: list[str] = []
    lines.append(f"[guardrails] ok={ok}")

    ssot_obj = payload.get("ssot")
    ssot = ssot_obj if isinstance(ssot_obj, dict) else {}
    blessed = ssot.get("blessed")
    if isinstance(blessed, str) and blessed:
        lines.append(f"[guardrails] ssot={blessed}")

    for e in errors:
        lines.append(f"[guardrails] ERROR: {e}")
    for w in warnings:
        lines.append(f"[guardrails] WARN: {w}")

    if not ok:
        entryways = payload.get("guidance")
        if isinstance(entryways, dict):
            lines.append("[guardrails] next steps (blessed entryways):")
            lines.append(format_entryways_text(entryways))

    return "\n".join(lines)


def enforce_ssot_or_exit(
    *,
    repo_root: Path,
    allow_shodh_mcp: bool = False,
    environ: Mapping[str, str] | None = None,
) -> None:
    """Fail-closed with actionable guidance when guardrails are violated."""

    payload = check_guardrails(
        repo_root=repo_root, allow_shodh_mcp=allow_shodh_mcp, environ=environ
    )
    if not payload.get("ok"):
        print(format_guardrails_human(payload))
        raise SystemExit(2)


def enforce_ssot_write_target_or_exit(
    *,
    repo_root: Path,
    sqlite_path: str,
    environ: Mapping[str, str] | None = None,
) -> None:
    """Fail-closed if a write target is not the pointer-blessed SSOT sqlite.

    This is stricter than "best-effort" resolution: if MCP_MEMORY_SQLITE_PATH is
    pointed at a legacy/alternate DB, we fail even in dry-run so drift is visible.
    """

    env = environ or os.environ

    expected = resolve_path(
        "paths.mcp_memory_ssot_sqlite",
        default=str(repo_root / _DEFAULT_SSOT_REL),
        environ=env,
    )

    expected_abs = _normalize_path(repo_root, expected)
    target_abs = _normalize_path(repo_root, sqlite_path)

    env_raw = env.get("MCP_MEMORY_SQLITE_PATH")
    env_abs = _normalize_path(repo_root, env_raw) if env_raw else ""

    errors: list[str] = []
    if not expected_abs:
        errors.append(
            "Unable to resolve pointer-blessed SSOT path (check hfo_pointers.json paths.mcp_memory_ssot_sqlite)"
        )
    if not target_abs:
        errors.append("Missing/empty sqlite_path for SSOT write")

    if expected_abs and env_abs and env_abs != expected_abs:
        errors.append(
            "MCP_MEMORY_SQLITE_PATH is not pointer-blessed SSOT: "
            f"env={env_abs} expected={expected_abs}"
        )

    if expected_abs and target_abs and target_abs != expected_abs:
        errors.append(
            "Attempted write target is not pointer-blessed SSOT: "
            f"target={target_abs} expected={expected_abs}"
        )

    if errors:
        print("[guardrails] ok=False")
        for e in errors:
            print(f"[guardrails] ERROR: {e}")

        guidance_env = dict(env)
        guidance_env["MCP_MEMORY_SQLITE_PATH"] = expected_abs
        entryways = get_blessed_entryways(repo_root=repo_root, environ=guidance_env)
        print("[guardrails] next steps (blessed entryways):")
        print(format_entryways_text(entryways))
        raise SystemExit(2)
