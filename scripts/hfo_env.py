#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Repo-local environment loader.

Why this exists
- VS Code tasks, background daemons, and some agent-run processes do not reliably
  inherit your interactive shell environment.
- This loader makes runtime behavior consistent by loading repo-root secret files
  into the process environment *without* printing secrets.

Files (in order)
- .env
- .env.local (optional)
- .hfo_secret (optional)

Rules
- Never overrides already-set environment variables unless override=True.
- No external dependencies (does not require python-dotenv).

Opt-out
- Set HFO_ENV_DISABLE=1 to skip loading.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Iterable, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILES: Tuple[str, ...] = (".env", ".env.local", ".hfo_secret")


def _strip_quotes(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        return v[1:-1]
    return v


def _parse_env_file(path: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return out
    except Exception:
        return out

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = _strip_quotes(value.strip())

        if not key:
            continue
        out[key] = value

    return out


def load_repo_env(*, override: bool = False, env_files: Iterable[str] = DEFAULT_ENV_FILES) -> Dict[str, str]:
    """Load repo-root env files into os.environ.

    Returns a dict of keys that were set/updated in os.environ.
    """

    if os.environ.get("HFO_ENV_DISABLE", "").strip() in {"1", "true", "TRUE", "yes", "YES"}:
        return {}

    # Avoid repeated parsing in long-running processes.
    if os.environ.get("HFO_ENV_LOADED") == "1":
        return {}

    changed: Dict[str, str] = {}

    for filename in env_files:
        path = REPO_ROOT / filename
        for key, value in _parse_env_file(path).items():
            if override or not os.environ.get(key):
                os.environ[key] = value
                changed[key] = "***"

    os.environ["HFO_ENV_LOADED"] = "1"
    return changed
