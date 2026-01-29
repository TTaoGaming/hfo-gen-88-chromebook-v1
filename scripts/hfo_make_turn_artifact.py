#!/usr/bin/env python3
"""Medallion: Bronze | Mutation: 0% | HIVE: V

Creates a timestamped Markdown proof artifact and appends a stigmergy JSONL event.

Designed to enforce the GitHub Agents mode requirement:
- Every turn produces an artifact (>= 1 page markdown target)
- Every turn leaves an append-only stigmergy trace

No external dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_TEMPLATE_PATH = Path("templates/agent_turn_artifact_template.md")
DEFAULT_OUT_ROOT = Path("artifacts/agent_proof")
DEFAULT_BLACKBOARD = Path(
    "hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard_v4.jsonl"
)


@dataclass(frozen=True)
class ArtifactPaths:
    artifact_path: Path
    blackboard_path: Path


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_slug(value: str) -> str:
    value = (value or "").strip().lower()
    if not value:
        return "turn"

    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-_")
    cleaned = []
    prev_was_sep = False

    for ch in value:
        if ch in allowed:
            cleaned.append(ch)
            prev_was_sep = False
        elif ch.isspace() or ch in {"/", "\\", ".", ":"}:
            if not prev_was_sep:
                cleaned.append("-")
                prev_was_sep = True
        else:
            # drop other punctuation
            continue

    slug = "".join(cleaned).strip("-")
    return slug or "turn"


def _load_template(template_path: Path) -> str:
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def _render_template(template: str, *, agent_mode: str, title: str, slug: str, created: datetime) -> str:
    created_utc = created.isoformat().replace("+00:00", "Z")
    local_date = created_utc[:10]

    return (
        template.replace("${AGENT_MODE}", agent_mode)
        .replace("${CREATED_UTC}", created_utc)
        .replace("${LOCAL_DATE}", local_date)
        .replace("${TITLE}", title)
        .replace("${SLUG}", slug)
    )


def _compute_paths(
    *, out_root: Path, agent_mode: str, slug: str, created: datetime, blackboard_path: Path
) -> ArtifactPaths:
    date_dir = created.strftime("%Y-%m-%d")
    stamp = created.strftime("%Y%m%dT%H%M%SZ")

    artifact_dir = out_root / agent_mode / date_dir
    artifact_name = f"{stamp}__{slug}.md"

    return ArtifactPaths(artifact_path=artifact_dir / artifact_name, blackboard_path=blackboard_path)


def _append_stigmergy_event(*, blackboard_path: Path, event: dict) -> None:
    blackboard_path.parent.mkdir(parents=True, exist_ok=True)

    # Append-only JSONL.
    with blackboard_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a timestamped agent proof artifact (+ stigmergy JSONL).")
    parser.add_argument("--mode", required=True, help="Agent mode name (folder segment).")
    parser.add_argument("--slug", required=True, help="Short slug used in filename.")
    parser.add_argument("--title", required=True, help="Human title (H1) for the artifact.")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE_PATH), help="Path to Markdown template.")
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT), help="Output root directory.")
    parser.add_argument(
        "--blackboard",
        default=str(DEFAULT_BLACKBOARD),
        help="Append-only JSONL blackboard path for stigmergy events.",
    )
    parser.add_argument(
        "--no-stigmergy",
        action="store_true",
        help="Create artifact but do not append stigmergy JSONL (not recommended).",
    )

    args = parser.parse_args()

    created = _utc_now()
    agent_mode = args.mode.strip() or "agent"
    slug = _safe_slug(args.slug)
    title = args.title.strip() or slug

    template_path = Path(args.template)
    out_root = Path(args.out_root)
    blackboard_path = Path(args.blackboard)

    template = _load_template(template_path)
    rendered = _render_template(template, agent_mode=agent_mode, title=title, slug=slug, created=created)

    paths = _compute_paths(
        out_root=out_root, agent_mode=agent_mode, slug=slug, created=created, blackboard_path=blackboard_path
    )

    paths.artifact_path.parent.mkdir(parents=True, exist_ok=True)
    paths.artifact_path.write_text(rendered, encoding="utf-8")

    if not args.no_stigmergy:
        event = {
            "ts_utc": created.isoformat().replace("+00:00", "Z"),
            "kind": "agent_turn_artifact",
            "agent_mode": agent_mode,
            "artifact_path": str(paths.artifact_path.as_posix()),
            "slug": slug,
            "title": title,
        }
        _append_stigmergy_event(blackboard_path=paths.blackboard_path, event=event)

    # Print the artifact path as the primary "receipt" for chaining.
    print(paths.artifact_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
