#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""HFO pointer resolver.

Goal:
- Keep a *stable root shim* while allowing the active implementation + SSOT paths
  to be swapped by changing a single artifact (hfo_pointers.json).

Rules:
- Backward compatible: if the pointer file is missing or malformed, return defaults.
- Env overrides win (lets CI/agents override without edits).

This module is intentionally tiny and dependency-free.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

POINTERS_FILENAME = "hfo_pointers.json"


def _find_repo_root(start: Path | None = None) -> Path:
    cur = (start or Path(__file__)).resolve()
    if cur.is_file():
        cur = cur.parent

    for _ in range(12):
        if (cur / "AGENTS.md").exists() and (cur / "hfo_hot_obsidian").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent

    # Fallback: assume this file lives at repo root.
    return Path(__file__).resolve().parent


def _load_pointers(repo_root: Path) -> dict[str, Any]:
    p = repo_root / POINTERS_FILENAME
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _dig(d: dict[str, Any], dotted: str) -> Any:
    cur: Any = d
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def get_pointer(dotted_key: str, default: Any = None) -> Any:
    """Get a pointer value from hfo_pointers.json using a dotted key."""

    repo_root = _find_repo_root()
    pointers = _load_pointers(repo_root)
    val = _dig(pointers, dotted_key)
    return default if val is None else val


def resolve_path(
    dotted_key: str,
    *,
    env_var: str | None = None,
    default: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> str:
    """Resolve a path pointer to an absolute path.

    - If env_var is set and present, uses that.
    - Else reads dotted_key from pointer file.
    - Else uses default.

    If the resulting path is relative, it is resolved relative to repo root.
    """

    repo_root = _find_repo_root()

    env = environ or os.environ

    if env_var:
        env_val = env.get(env_var)
        if env_val:
            return str(Path(env_val).expanduser())

    raw = get_pointer(dotted_key, default)
    if not raw:
        return str(Path(default).expanduser()) if default else ""

    p = Path(str(raw)).expanduser()
    return str(p if p.is_absolute() else (repo_root / p))


def resolve_target(*, env_var: str, dotted_key: str, default: str) -> str:
    """Resolve a python 'runpy target' script path."""

    return resolve_path(dotted_key, env_var=env_var, default=default)
