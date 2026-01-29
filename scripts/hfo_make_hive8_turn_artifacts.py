#!/usr/bin/env python3
"""Medallion: Bronze | Mutation: 0% | HIVE: V

Generate the Gen88 v4 HIVE-8 "8 artifacts per turn" envelope.

This is intentionally simple:
- Creates 8 Markdown files (P0,P7,P1,P6,P2,P5,P3,P4) from a template
- Writes a small manifest JSON
- Appends a single stigmergy JSONL event pointing to the envelope

No external deps.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def _parse_utc_iso(value: str) -> datetime:
    """Parse a UTC ISO-8601 timestamp.

    Accepts a trailing 'Z' and normalizes to timezone-aware UTC.
    """

    raw = (value or "").strip()
    if not raw:
        raise ValueError("empty created_utc")

    # datetime.fromisoformat does not accept 'Z'
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    dt = datetime.fromisoformat(raw)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


DEFAULT_TEMPLATE_PATH = Path("templates/hive8_turn_port_artifact_template.md")
DEFAULT_P1_TEMPLATE_PATH = Path(
    "templates/hive8_turn_port_artifact_template_P1_webweaver.md"
)
DEFAULT_P3_TEMPLATE_PATH = Path(
    "templates/hive8_turn_port_artifact_template_P3_harmonic_hydra.md"
)
DEFAULT_P6_TEMPLATE_PATH = Path(
    "templates/hive8_turn_port_artifact_template_P6_kraken_keeper.md"
)
DEFAULT_META_TEMPLATE_PATH = Path("templates/hive8_turn_meta_synthesis_template.md")
DEFAULT_OUT_ROOT = Path("artifacts/hive8/turns")
DEFAULT_BLACKBOARD = Path(
    "hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard_v4.jsonl"
)


PAIR_ORDER = [
    ("P0", "P7", "phase_0_hindsight"),
    ("P1", "P6", "phase_1_insight"),
    ("P2", "P5", "phase_2_validated_foresight"),
    ("P3", "P4", "phase_3_evolution"),
]


PORT_TITLES = {
    "P0": "P0 — Hindsight Sensor Fusion",
    "P7": "P7 — Spider Sovereign Alignment + S3 Handoff",
    "P1": "P1 — Insight: Interlocking Interfaces",
    "P6": "P6 — Deep Recall: Exemplars + Receipts",
    "P2": "P2 — Validated-Foresight Readiness",
    "P5": "P5 — Validation Vanguards: Forensic Gate",
    "P3": "P3 — Evolutionary Engines: Delivery",
    "P4": "P4 — Evolutionary Engines: Feedback/Suppression",
}


# Canonical commander names/verbs are sourced from:
# hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/hfo_mtg_commanders/LEGENDARY_HFO_COMMANDERS_V7_HYDRA_ASCENDANT.md
PORT_COMMANDERS: dict[str, dict[str, str]] = {
    "P0": {
        "name": "THE LIDLESS LEGION",
        "alias": "",
        "verb": "OBSERVE",
        "port_role": "SENSE",
    },
    "P1": {
        "name": "THE WEB WEAVER",
        "alias": "SWARM LORD OF WEBS",
        "verb": "BRIDGE",
        "port_role": "FUSE",
    },
    "P2": {
        "name": "THE MIRROR MAGUS",
        "alias": "",
        "verb": "SHAPE",
        "port_role": "SHAPE",
    },
    "P3": {
        "name": "HARMONIC HYDRA",
        "alias": "",
        "verb": "INJECT",
        "port_role": "DELIVER",
    },
    "P4": {
        "name": "RED REGNANT",
        "alias": "",
        "verb": "DISRUPT",
        "port_role": "DISRUPT",
    },
    "P5": {
        "name": "PYRE PRAETORIAN",
        "alias": "",
        "verb": "IMMUNIZE",
        "port_role": "DEFEND",
    },
    "P6": {
        "name": "KRAKEN KEEPER",
        "alias": "",
        "verb": "ASSIMILATE",
        "port_role": "STORE",
    },
    "P7": {
        "name": "SPIDER SOVEREIGN",
        "alias": "",
        "verb": "NAVIGATE",
        "port_role": "NAVIGATE",
    },
}


PORT_META_PROMOTED_LABELS: dict[str, list[str]] = {
    # SCATTER (2 items)
    "P0": ["Observation", "Observation"],
    "P1": ["Top Color", "Top Color"],
    "P2": ["Reflection", "Reflection"],
    "P3": ["Injection (Battery)", "Injection (Battery)"],
    # GATHER (1 item)
    "P4": ["Song"],
    "P5": ["Firewall"],
    "P6": ["Iridescent Pearl (UML Mermaid)"],
    "P7": ["Alignment (S3 Handoff)"],
}


def _load_port_mtg_card_map(repo_root: Path) -> dict[str, dict[str, str]]:
    mapping_paths = [
        repo_root / "contracts" / "hfo_mtg_port_card_mappings.v5.json",
        repo_root / "contracts" / "hfo_mtg_port_card_mappings.v2.json",
        repo_root / "contracts" / "hfo_mtg_port_card_mappings.v1.json",
    ]
    for mapping_path in mapping_paths:
        if not mapping_path.exists():
            continue
        raw = json.loads(mapping_path.read_text(encoding="utf-8"))
        ports = raw.get("ports")
        if isinstance(ports, dict):
            return ports
    return {}


@dataclass(frozen=True)
class TurnPaths:
    envelope_dir: Path
    manifest_path: Path
    meta_path: Path
    artifacts: dict[str, Path]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_stamp(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


def _date_dir(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def _safe_slug(value: str) -> str:
    value = (value or "").strip().lower()
    if not value:
        return "turn"

    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-_")
    cleaned = []
    prev_sep = False

    for ch in value:
        if ch in allowed:
            cleaned.append(ch)
            prev_sep = False
        elif ch.isspace() or ch in {"/", "\\", ".", ":"}:
            if not prev_sep:
                cleaned.append("-")
                prev_sep = True
        else:
            continue

    slug = "".join(cleaned).strip("-")
    return slug or "turn"


def _load_template(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def _render(template: str, *, replacements: dict[str, str]) -> str:
    out = template
    for key, value in replacements.items():
        out = out.replace(f"${{{key}}}", value)
    return out


def _append_jsonl(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def _compute_paths(*, out_root: Path, created: datetime, slug: str) -> TurnPaths:
    stamp = _utc_stamp(created)
    day = _date_dir(created)
    envelope_dir = out_root / day / f"{stamp}__{slug}"
    artifacts: dict[str, Path] = {
        "P0": envelope_dir / "P0__hindsight_sensor_fusion.md",
        "P7": envelope_dir / "P7__spider_sovereign_handoff.md",
        "P1": envelope_dir / "P1__interlocking_interfaces.md",
        "P6": envelope_dir / "P6__deep_recall_exemplars.md",
        "P2": envelope_dir / "P2__validated_foresight_readiness.md",
        "P5": envelope_dir / "P5__forensic_audit_gate.md",
        "P3": envelope_dir / "P3__delivery_pipeline.md",
        "P4": envelope_dir / "P4__feedback_suppression.md",
    }
    meta_path = envelope_dir / "HIVE8__meta_synthesis.md"
    manifest_path = envelope_dir / "turn_manifest.json"
    return TurnPaths(
        envelope_dir=envelope_dir,
        manifest_path=manifest_path,
        meta_path=meta_path,
        artifacts=artifacts,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create HIVE-8 Gen88 v4 8-artifact turn envelope."
    )
    parser.add_argument("--slug", required=True, help="Short slug used in folder name.")
    parser.add_argument(
        "--turn-id",
        default="",
        help="Optional: override computed turn_id (use for deterministic tests).",
    )
    parser.add_argument(
        "--created-utc",
        default="",
        help="Optional: override created_utc ISO timestamp (use for deterministic tests). Example: 2026-01-27T00:00:00Z",
    )
    parser.add_argument(
        "--prompt",
        default="",
        help="Optional: user question/prompt for this turn (rendered into artifacts via ${USER_PROMPT}).",
    )
    parser.add_argument(
        "--mission-thread", default="unknown", help="alpha|omega|unknown"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail-closed input contract: require non-empty --prompt and mission-thread in {alpha,omega}.",
    )
    parser.add_argument(
        "--template", default=str(DEFAULT_TEMPLATE_PATH), help="Template path"
    )
    parser.add_argument(
        "--p1-template",
        default=str(DEFAULT_P1_TEMPLATE_PATH),
        help="Optional override template for P1 (Web Weaver / Swarm Lord of Webs).",
    )
    parser.add_argument(
        "--p3-template",
        default=str(DEFAULT_P3_TEMPLATE_PATH),
        help="Optional override template for P3 (Harmonic Hydra).",
    )
    parser.add_argument(
        "--p6-template",
        default=str(DEFAULT_P6_TEMPLATE_PATH),
        help="Optional override template for P6 (Kraken Keeper).",
    )
    parser.add_argument(
        "--meta-template",
        default=str(DEFAULT_META_TEMPLATE_PATH),
        help="Template path for the 1-page meta synthesis artifact",
    )
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT), help="Output root")
    parser.add_argument(
        "--blackboard", default=str(DEFAULT_BLACKBOARD), help="Stigmergy JSONL path"
    )
    parser.add_argument(
        "--canonical-s3-path",
        default="",
        help="Optional: path to the canonical P7 S3 artifact (hot obsidian PARA).",
    )
    parser.add_argument(
        "--no-stigmergy", action="store_true", help="Do not append JSONL stigmergy"
    )

    args = parser.parse_args()

    if args.created_utc:
        created = _parse_utc_iso(args.created_utc)
    else:
        created = _utc_now()
    stamp = _utc_stamp(created)
    created_utc = created.isoformat().replace("+00:00", "Z")

    slug = _safe_slug(args.slug)
    user_prompt = (args.prompt or "").strip()
    mission_thread = (args.mission_thread or "unknown").strip().lower()
    if mission_thread not in {"alpha", "omega", "unknown"}:
        mission_thread = "unknown"

    if args.strict:
        if not user_prompt:
            raise SystemExit("HIVE8 strict mode requires a non-empty --prompt")
        if mission_thread not in {"alpha", "omega"}:
            raise SystemExit("HIVE8 strict mode requires --mission-thread alpha|omega")

    template = _load_template(Path(args.template))
    p1_template = (
        _load_template(Path(args.p1_template)) if args.p1_template else template
    )
    p3_template = (
        _load_template(Path(args.p3_template)) if args.p3_template else template
    )
    p6_template = (
        _load_template(Path(args.p6_template)) if args.p6_template else template
    )
    meta_template = _load_template(Path(args.meta_template))
    paths = _compute_paths(out_root=Path(args.out_root), created=created, slug=slug)

    blackboard_path = Path(args.blackboard)

    paths.envelope_dir.mkdir(parents=True, exist_ok=True)

    # Create the eight port artifacts.
    for left, right, phase in PAIR_ORDER:
        for port, paired in ((left, right), (right, left)):
            scatter_ports = {"P0", "P1", "P2", "P3"}
            is_scatter = port in scatter_ports
            scatter_gather_mode = "SCATTER" if is_scatter else "GATHER"

            artifact_cardinality_label = "8^1"
            artifact_cardinality_count = 8
            meta_cardinality_label = "2^1" if is_scatter else "8^0"
            meta_cardinality_count = 2 if is_scatter else 1
            # Power-of-two placeholders for the meta-promoted lane.
            labels = PORT_META_PROMOTED_LABELS.get(port, ["Promoted", "Promoted"])
            if meta_cardinality_count == 2:
                meta_promoted_placeholders = "\n".join(
                    [
                        f"- 1 {labels[0]}: ",
                        f"- 2 {labels[1] if len(labels) > 1 else labels[0]}: ",
                    ]
                )
            else:
                meta_promoted_placeholders = f"- 1 {labels[0]}: "

            title = PORT_TITLES.get(port, port)
            commander = PORT_COMMANDERS.get(port, {})

            chosen_template = template
            if port == "P1":
                chosen_template = p1_template
            elif port == "P3":
                chosen_template = p3_template
            elif port == "P6":
                chosen_template = p6_template

            turn_id = (args.turn_id or "").strip() or f"{stamp}__{slug}"
            rendered = _render(
                chosen_template,
                replacements={
                    "TURN_ID": turn_id,
                    "CREATED_UTC": created_utc,
                    "PHASE": phase,
                    "PORT": port,
                    "PAIRED_WITH": paired,
                    "COMMANDER_NAME": commander.get("name", "UNKNOWN"),
                    "COMMANDER_ALIAS": commander.get("alias", ""),
                    "COMMANDER_VERB": commander.get("verb", "UNKNOWN"),
                    "COMMANDER_PORT_ROLE": commander.get("port_role", "UNKNOWN"),
                    "SCATTER_GATHER_MODE": scatter_gather_mode,
                    "ARTIFACT_CARDINALITY_LABEL": artifact_cardinality_label,
                    "ARTIFACT_CARDINALITY_COUNT": str(artifact_cardinality_count),
                    "META_CARDINALITY_LABEL": meta_cardinality_label,
                    "META_CARDINALITY_COUNT": str(meta_cardinality_count),
                    "META_PROMOTED_PLACEHOLDERS": meta_promoted_placeholders,
                    "MISSION_THREAD": mission_thread,
                    "SLUG": slug,
                    "TITLE": title,
                    "USER_PROMPT": user_prompt,
                },
            )
            paths.artifacts[port].write_text(rendered, encoding="utf-8")

    # Create the meta synthesis artifact (1 page).
    meta_rendered = _render(
        meta_template,
        replacements={
            "TURN_ID": (args.turn_id or "").strip() or f"{stamp}__{slug}",
            "CREATED_UTC": created_utc,
            "MISSION_THREAD": mission_thread,
            "SLUG": slug,
            "USER_PROMPT": user_prompt,
            "MANIFEST_PATH": str(paths.manifest_path.as_posix()),
            "BLACKBOARD_PATH": str(blackboard_path.as_posix()),
            "CANONICAL_S3_PATH": args.canonical_s3_path or "",
            "P0_ARTIFACT_PATH": str(paths.artifacts["P0"].as_posix()),
            "P7_ARTIFACT_PATH": str(paths.artifacts["P7"].as_posix()),
            "P1_ARTIFACT_PATH": str(paths.artifacts["P1"].as_posix()),
            "P6_ARTIFACT_PATH": str(paths.artifacts["P6"].as_posix()),
            "P2_ARTIFACT_PATH": str(paths.artifacts["P2"].as_posix()),
            "P5_ARTIFACT_PATH": str(paths.artifacts["P5"].as_posix()),
            "P3_ARTIFACT_PATH": str(paths.artifacts["P3"].as_posix()),
            "P4_ARTIFACT_PATH": str(paths.artifacts["P4"].as_posix()),
            "P0_COMMANDER_NAME": PORT_COMMANDERS["P0"]["name"],
            "P7_COMMANDER_NAME": PORT_COMMANDERS["P7"]["name"],
            "P1_COMMANDER_NAME": PORT_COMMANDERS["P1"]["name"],
            "P6_COMMANDER_NAME": PORT_COMMANDERS["P6"]["name"],
            "P2_COMMANDER_NAME": PORT_COMMANDERS["P2"]["name"],
            "P5_COMMANDER_NAME": PORT_COMMANDERS["P5"]["name"],
            "P3_COMMANDER_NAME": PORT_COMMANDERS["P3"]["name"],
            "P4_COMMANDER_NAME": PORT_COMMANDERS["P4"]["name"],
        },
    )
    paths.meta_path.write_text(meta_rendered, encoding="utf-8")

    repo_root = Path.cwd()
    mtg_port_cards = _load_port_mtg_card_map(repo_root)

    turn_id = (args.turn_id or "").strip() or f"{stamp}__{slug}"
    manifest = {
        "schema": "hive8_turn_manifest.v1",
        "strict": bool(args.strict),
        "turn_id": turn_id,
        "created_utc": created_utc,
        "mission_thread": mission_thread,
        "slug": slug,
        "user_prompt": user_prompt,
        "envelope_dir": str(paths.envelope_dir.as_posix()),
        "artifacts": {k: str(v.as_posix()) for k, v in paths.artifacts.items()},
        "meta_synthesis_path": str(paths.meta_path.as_posix()),
        "meta": str(paths.meta_path.as_posix()),
        "commanders": PORT_COMMANDERS,
        "mtg_port_cards": mtg_port_cards,
        "pair_order": [{"a": a, "b": b, "phase": ph} for a, b, ph in PAIR_ORDER],
        "canonical_s3_path": args.canonical_s3_path or "",
    }
    paths.manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if not args.no_stigmergy:
        event = {
            "ts_utc": created_utc,
            "kind": "hive8_turn_envelope",
            "agent_mode": "hfo_hive_8_agent_gen_88_v_4",
            "turn_id": manifest["turn_id"],
            "mission_thread": mission_thread,
            "envelope_dir": manifest["envelope_dir"],
            "manifest_path": str(paths.manifest_path.as_posix()),
            "canonical_s3_path": manifest["canonical_s3_path"],
            "artifacts": manifest["artifacts"],
            "meta_synthesis_path": manifest["meta_synthesis_path"],
        }
        _append_jsonl(blackboard_path, event)

    print(paths.envelope_dir.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
