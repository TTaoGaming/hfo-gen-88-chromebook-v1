#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""SSOT-native status updates for Gen88 v4 (doobidoo sqlite_vec).

Policy:
- The sqlite SSOT is the only blessed write-path for "memory".
- JSONL memory ledgers (e.g. mcp_memory.jsonl) are legacy and must not be appended to.

This is a tiny helper used by scripts to store a structured status update into
SSOT without requiring an MCP server.

Design note:
- This script is intended to be safe-by-default and fail-closed on non-SSOT writes.
- It imports shared guardrails so guidance is consistent across entrypoints.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp_memory_service.models.memory import Memory
from mcp_memory_service.storage.factory import create_storage_instance
from mcp_memory_service.utils.hashing import generate_content_hash

_REPO_ROOT = Path(__file__).resolve().parents[1]

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_pointers(repo_root: Path) -> dict[str, Any]:
    p = repo_root / "hfo_pointers.json"
    if not p.exists():
        return {}
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def resolve_ssot_sqlite_path(*, repo_root: Path | None = None) -> str:
    repo_root = repo_root or _REPO_ROOT

    # Local import so this script stays import-order clean even with sys.path mutation.
    from hfo_memory_guardrails import enforce_ssot_write_target_or_exit

    env_path = os.environ.get("MCP_MEMORY_SQLITE_PATH")
    if env_path:
        candidate = env_path
    else:
        candidate = ""

    pointers = _read_pointers(repo_root)
    paths_obj = pointers.get("paths")
    paths: dict[str, Any] = paths_obj if isinstance(paths_obj, dict) else {}

    rel_obj = paths.get("mcp_memory_ssot_sqlite")
    rel = rel_obj if isinstance(rel_obj, str) else ""

    if not candidate:
        if rel:
            candidate = str((repo_root / rel).resolve())
        else:
            candidate = str(
                (
                    repo_root
                    / "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db"
                ).resolve()
            )

    enforce_ssot_write_target_or_exit(repo_root=repo_root, sqlite_path=str(candidate))
    return str(candidate)


def build_status_update_content(*, topic: str, payload: dict[str, Any]) -> str:
    header = [
        "[type:status_update]",
        f"[topic:{topic}]",
        f"[ts:{_utc_now_iso()}]",
        "",
    ]
    return "\n".join(header) + json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


async def store_status_update(
    *,
    topic: str,
    payload: dict[str, Any],
    tags: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    sqlite_path: str | None = None,
    dry_run: bool = False,
) -> tuple[bool, str]:
    """Store a single SSOT memory entry. Returns (ok, message)."""

    sqlite_path = sqlite_path or resolve_ssot_sqlite_path(repo_root=_REPO_ROOT)

    # Fail-closed even in dry-run so drift is obvious.
    from hfo_memory_guardrails import enforce_ssot_write_target_or_exit

    enforce_ssot_write_target_or_exit(
        repo_root=_REPO_ROOT, sqlite_path=str(sqlite_path)
    )

    content = build_status_update_content(topic=topic, payload=payload)
    content_hash = generate_content_hash(content)

    base_tags = tags or ["gen88_v4", "ssot", "status_update"]
    deduped_tags = list(dict.fromkeys([*base_tags, f"topic:{topic}"]))

    mem = Memory(
        content=content,
        content_hash=content_hash,
        tags=deduped_tags,
        memory_type="status_update",
        metadata={
            "topic": topic,
            "ts": _utc_now_iso(),
            **(metadata or {}),
        },
    )

    if dry_run:
        return True, "dry-run"

    storage = await create_storage_instance(sqlite_path=sqlite_path, server_type="mcp")
    ok, msg = await storage.store(mem)
    return bool(ok), str(msg or "")


def _parse_json(s: str) -> Any:
    try:
        return json.loads(s)
    except Exception as e:
        raise SystemExit(f"Invalid JSON: {e}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="Write a status_update into the doobidoo sqlite SSOT"
    )
    ap.add_argument("--topic", required=True)
    ap.add_argument(
        "--payload-json",
        required=True,
        help="JSON string payload to embed in SSOT content",
    )
    ap.add_argument(
        "--tags",
        default="gen88_v4 ssot status_update",
        help="Space-separated tags",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write; just validate payload and print resolved sqlite path",
    )
    args = ap.parse_args(argv)

    payload = _parse_json(args.payload_json)
    if not isinstance(payload, dict):
        raise SystemExit("--payload-json must be a JSON object")

    sqlite_path = resolve_ssot_sqlite_path(repo_root=_REPO_ROOT)

    ok, msg = asyncio.run(
        store_status_update(
            topic=str(args.topic),
            payload=payload,
            tags=[t for t in (args.tags or "").split() if t.strip()],
            sqlite_path=sqlite_path,
            dry_run=bool(args.dry_run),
            metadata={"source": "scripts/hfo_ssot_status_update.py"},
        )
    )

    print(f"[ssot] sqlite={sqlite_path}")
    print(f"[ssot] ok={ok} msg={msg}")

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
