#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""P7 Hive-8 alignment snapshot (lightweight).

Purpose:
- Capture a small, repeatable snapshot of the current hub surface area.
- Append that snapshot to MCP memory JSONL for diffing over time.

This is intentionally non-blocking: it logs observations and unknowns without
requiring the "ideal" to be fully formalized.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MEMORY_PATH = (
    REPO_ROOT / "hfo_hot_obsidian" / "bronze" / "3_resources" / "memory" / "mcp_memory.jsonl"
)


@dataclass(frozen=True)
class SnapshotConfig:
    topic: str
    memory_path: Path


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=REPO_ROOT, text=True).strip()
    except Exception:
        return ""


def _safe_rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(REPO_ROOT))
    except Exception:
        return str(p)


def _read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _file_meta(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": _safe_rel(path), "exists": False}
    st = path.stat()
    return {
        "path": _safe_rel(path),
        "exists": True,
        "size_bytes": st.st_size,
        "mtime_utc": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
    }


def build_snapshot(config: SnapshotConfig) -> dict[str, Any]:
    hub_files = [
        REPO_ROOT / "hfo_hub.py",
        REPO_ROOT / "hfo_mcp_gateway_hub.py",
        REPO_ROOT / "hfo_blackboard_events.py",
    ]
    pointers_path = REPO_ROOT / "hfo_pointers.json"
    vscode_tasks_path = REPO_ROOT / ".vscode" / "tasks.json"
    agents_path = REPO_ROOT / "AGENTS.md"
    root_governance_path = REPO_ROOT / "ROOT_GOVERNANCE.md"
    contracts_dir = REPO_ROOT / "contracts"
    ports_dir = REPO_ROOT / "hfo_ports"

    pointers = _read_json(pointers_path) if pointers_path.exists() else None
    tasks_obj = _read_json(vscode_tasks_path) if vscode_tasks_path.exists() else None

    tasks = []
    if isinstance(tasks_obj, dict) and isinstance(tasks_obj.get("tasks"), list):
        tasks = tasks_obj["tasks"]

    task_summaries: list[dict[str, Any]] = []
    for t in tasks:
        if not isinstance(t, dict):
            continue
        task_summaries.append(
            {
                "label": t.get("label"),
                "command": t.get("command"),
                "isBackground": t.get("isBackground"),
                "group": t.get("group"),
                "runOn": (t.get("runOptions") or {}).get("runOn") if isinstance(t.get("runOptions"), dict) else None,
            }
        )

    pointer_paths = {}
    if isinstance(pointers, dict) and isinstance(pointers.get("paths"), dict):
        pointer_paths = pointers["paths"]

    blackboard_rel = pointer_paths.get("blackboard") if isinstance(pointer_paths.get("blackboard"), str) else None
    mcp_memory_rel = pointer_paths.get("mcp_memory") if isinstance(pointer_paths.get("mcp_memory"), str) else None
    duckdb_unified_rel = pointer_paths.get("duckdb_unified") if isinstance(pointer_paths.get("duckdb_unified"), str) else None

    observed: dict[str, Any] = {
        "repo": {
            "branch": _run(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
            "head": _run(["git", "rev-parse", "HEAD"]),
            "status_porcelain": _run(["git", "status", "--porcelain"]),
        },
        "hub_files": [
            _file_meta(p)
            for p in hub_files
        ],
        "governance": [
            _file_meta(agents_path),
            _file_meta(root_governance_path),
        ],
        "contracts": {
            "dir": _safe_rel(contracts_dir),
            "zod_files": sorted(
                _safe_rel(p)
                for p in contracts_dir.glob("*.zod.ts")
                if p.is_file()
            ),
        },
        "ports_python": {
            "dir": _safe_rel(ports_dir),
            "files": sorted(_safe_rel(p) for p in ports_dir.glob("*.py") if p.is_file()) if ports_dir.exists() else [],
        },
        "pointers": {
            "path": _safe_rel(pointers_path),
            "targets": pointers.get("targets") if isinstance(pointers, dict) else None,
            "paths": pointers.get("paths") if isinstance(pointers, dict) else None,
        },
        "vscode_tasks": {
            "path": _safe_rel(vscode_tasks_path),
            "count": len(task_summaries),
            "tasks": task_summaries,
        },
        "key_artifacts": {
            "blackboard": _file_meta(REPO_ROOT / blackboard_rel) if blackboard_rel else None,
            "mcp_memory": _file_meta(REPO_ROOT / mcp_memory_rel) if mcp_memory_rel else None,
            "duckdb_unified": _file_meta(REPO_ROOT / duckdb_unified_rel) if duckdb_unified_rel else None,
        },
    }

    entry: dict[str, Any] = {
        "type": "status_update",
        "ts": _utc_now_iso(),
        "topic": config.topic,
        "summary": {
            "changes": [
                "Recorded a P7 Hive-8 alignment snapshot (hub surface area + contracts + pointers + tasks + key artifacts)."
            ],
            "tests": {"note": "Snapshot only; no tests executed."},
        },
        "observed": observed,
        "ideal_targets": [
            "P7 orchestration is evidence-first and fail-closed",
            "Cross-port coupling is explicit via contracts",
            "Hub actions emit append-only breadcrumbs (memory + blackboard) with sources",
            "Fractal zoom-level addressing is explicit (octree taxonomy)",
        ],
        "gaps": [
            "Ideal state taxonomy not fully formalized yet (expected).",
            "No automated diffing yet; use repeated snapshots + human review.",
        ],
        "sources": [
            "hfo_hub.py",
            "hfo_mcp_gateway_hub.py",
            "hfo_pointers.json",
            ".vscode/tasks.json",
            "AGENTS.md",
            "ROOT_GOVERNANCE.md",
            "contracts/",
            "hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl",
        ],
    }

    return entry


def append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main() -> int:
    topic = os.environ.get("HFO_TOPIC") or "p7_hive8_alignment_snapshot"
    memory_path = Path(os.environ.get("HFO_MCP_MEMORY", str(DEFAULT_MEMORY_PATH)))

    entry = build_snapshot(SnapshotConfig(topic=topic, memory_path=memory_path))
    append_jsonl(memory_path, entry)
    print(f"Appended snapshot to {memory_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
