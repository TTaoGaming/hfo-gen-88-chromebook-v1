#!/usr/bin/env python3
"""Medallion: Bronze | Mutation: 0% | HIVE: V

Finalize a HIVE8 turn envelope by auto-composing the Meta Synthesis from the 8 port artifacts.

Why this exists (anti-theater):
- The envelope generator creates deterministic files + paths.
- A *finalizer* should turn 8 individual port writeups into a readable, 2-page meta synthesis.
- Optionally, emit *one* stigmergy JSONL line only after meta is assembled.

No external dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

DEFAULT_BLACKBOARD = Path(
    "hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard_v4.jsonl"
)

PORT_ORDER = ["P0", "P7", "P1", "P6", "P2", "P5", "P3", "P4"]

AUTO_PORT_BRIEFINGS_START = "<!-- AUTO:PORT_BRIEFINGS_START -->"
AUTO_PORT_BRIEFINGS_END = "<!-- AUTO:PORT_BRIEFINGS_END -->"
AUTO_OPEN_LOOPS_START = "<!-- AUTO:OPEN_LOOPS_START -->"
AUTO_OPEN_LOOPS_END = "<!-- AUTO:OPEN_LOOPS_END -->"
AUTO_FEATURED_DIAGRAMS_START = "<!-- AUTO:FEATURED_DIAGRAMS_START -->"
AUTO_FEATURED_DIAGRAMS_END = "<!-- AUTO:FEATURED_DIAGRAMS_END -->"
AUTO_FEATURED_COLORS_START = "<!-- AUTO:FEATURED_COLORS_START -->"
AUTO_FEATURED_COLORS_END = "<!-- AUTO:FEATURED_COLORS_END -->"
AUTO_VALIDATION_RESULTS_START = "<!-- AUTO:VALIDATION_RESULTS_START -->"
AUTO_VALIDATION_RESULTS_END = "<!-- AUTO:VALIDATION_RESULTS_END -->"
AUTO_SCATTER_GATHER_LABELS_START = "<!-- AUTO:SCATTER_GATHER_LABELS_START -->"
AUTO_SCATTER_GATHER_LABELS_END = "<!-- AUTO:SCATTER_GATHER_LABELS_END -->"
AUTO_CARDINALITY_VALIDATION_START = "<!-- AUTO:CARDINALITY_VALIDATION_START -->"
AUTO_CARDINALITY_VALIDATION_END = "<!-- AUTO:CARDINALITY_VALIDATION_END -->"
AUTO_META_PROMOTED_DELIVERABLES_START = "<!-- AUTO:META_PROMOTED_DELIVERABLES_START -->"
AUTO_META_PROMOTED_DELIVERABLES_END = "<!-- AUTO:META_PROMOTED_DELIVERABLES_END -->"
AUTO_OBSIDIAN_POWERWORDS_START = "<!-- AUTO:OBSIDIAN_POWERWORDS_START -->"
AUTO_OBSIDIAN_POWERWORDS_END = "<!-- AUTO:OBSIDIAN_POWERWORDS_END -->"
AUTO_COMMANDER_MAPPINGS_START = "<!-- AUTO:COMMANDER_MAPPINGS_START -->"
AUTO_COMMANDER_MAPPINGS_END = "<!-- AUTO:COMMANDER_MAPPINGS_END -->"
AUTO_STAGE_FLOW_START = "<!-- AUTO:STAGE_FLOW_START -->"
AUTO_STAGE_FLOW_END = "<!-- AUTO:STAGE_FLOW_END -->"
AUTO_FINAL_DEBATE_START = "<!-- AUTO:FINAL_DEBATE_START -->"
AUTO_FINAL_DEBATE_END = "<!-- AUTO:FINAL_DEBATE_END -->"


def _scryfall_exact_name_url(card_name: str) -> str:
    q = f'!"{card_name.strip()}"'
    return "https://scryfall.com/search?q=" + quote(q, safe="")


def _load_port_mtg_card_map(repo_root: Path) -> dict[str, dict[str, str]]:
    mapping_paths = [
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
class PortExtract:
    port: str
    commander_name: str
    commander_port_role: str
    summary_bullets: list[str]
    handoff_target: str
    open_loops: list[str]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append_jsonl(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# Allow an optional leading provenance comment and whitespace before YAML frontmatter.
_FRONTMATTER_RE = re.compile(r"\A(?:\s|<!--.*?-->\s*)*---\n(.*?)\n---\n", re.DOTALL)


def _parse_frontmatter(md: str) -> dict[str, object]:
    """Very small YAML-ish parser for simple key: value pairs.

    Supports:
    - key: "string"
    - key: string
    - key: []

    We intentionally avoid external YAML deps.
    """

    m = _FRONTMATTER_RE.search(md)
    if not m:
        return {}

    out: dict[str, object] = {}
    for raw_line in m.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue

        if value == "[]":
            out[key] = []
            continue

        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            out[key] = value[1:-1]
        else:
            out[key] = value

    return out


def _extract_section_bullets(md: str, heading: str) -> list[str]:
    """Extract bullet lines under a given '## ' heading until the next '## ' heading."""

    idx = md.find(heading)
    if idx < 0:
        return []

    rest = md[idx + len(heading) :]
    # stop at next H2
    next_h2 = rest.find("\n## ")
    if next_h2 >= 0:
        rest = rest[:next_h2]

    bullets: list[str] = []
    for line in rest.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullet = stripped[2:].strip()
            if bullet:
                bullets.append(bullet)

    # Drop placeholders
    bullets = [
        b
        for b in bullets
        if b
        not in {
            "(2–4 bullets; write for a busy human)",
            "(2-4 bullets; write for a busy human)",
        }
    ]
    return bullets


def _extract_output_fields(md: str) -> tuple[str, list[str]]:
    """Extract handoff target and open loops from the Output / Handoff section."""

    handoff_target = ""
    open_loops: list[str] = []

    idx = md.find("## Output / Handoff")
    if idx < 0:
        return handoff_target, open_loops

    rest = md[idx:]
    next_h2 = rest.find("\n## ", 1)
    if next_h2 >= 0:
        rest = rest[:next_h2]

    for line in rest.splitlines():
        s = line.strip()
        if s.startswith("- Handoff target:"):
            handoff_target = s.split(":", 1)[1].strip()
        elif s.startswith("- Open loops:"):
            tail = s.split(":", 1)[1].strip()
            if tail:
                open_loops.append(tail)
        elif s.startswith("- "):
            # allow additional bullets under Output/Handoff as open loops if they look like tasks
            val = s[2:].strip()
            if (
                val
                and not val.lower().startswith("handoff target")
                and not val.lower().startswith("open loops")
            ):
                open_loops.append(val)

    open_loops = [
        x for x in open_loops if x and x != "-" and x != "(none)" and x != "TODO"
    ]
    return handoff_target, open_loops


def _extract_port(md_path: Path, port: str) -> PortExtract:
    md = _read_text(md_path)
    fm = _parse_frontmatter(md)

    commander_name = str(fm.get("commander_name") or "UNKNOWN")
    commander_port_role = str(fm.get("commander_port_role") or "UNKNOWN")

    summary_bullets = _extract_section_bullets(
        md, "## Port Summary (for Meta Synthesis)"
    )
    handoff_target, open_loops = _extract_output_fields(md)

    return PortExtract(
        port=port,
        commander_name=commander_name,
        commander_port_role=commander_port_role,
        summary_bullets=summary_bullets,
        handoff_target=handoff_target,
        open_loops=open_loops,
    )


def _replace_between(text: str, start: str, end: str, replacement: str) -> str:
    s = text.find(start)
    e = text.find(end)
    if s < 0 or e < 0 or e <= s:
        raise ValueError(f"Missing/invalid markers: {start} … {end}")

    before = text[: s + len(start)]
    after = text[e:]
    return before + "\n\n" + replacement.rstrip() + "\n\n" + after


def _extract_between(md: str, start: str, end: str) -> str:
    s = md.find(start)
    e = md.find(end)
    if s < 0 or e < 0 or e <= s:
        return ""
    return md[s + len(start) : e]


def _extract_bullets_between(md: str, start: str, end: str) -> list[str]:
    region = _extract_between(md, start, end)
    if not region:
        return []
    bullets: list[str] = []
    for line in region.splitlines():
        s = line.strip()
        if s.startswith("- "):
            val = s[2:].strip()
            if val:
                bullets.append(val)
    return bullets


_LEADING_INT_RE = re.compile(
    r"^\s*(?:\[(?P<bracket>\d+)\]|(?P<plain>\d+))\s*(?:[:\-—]\s*)?"
)


def _leading_int(value: str) -> int | None:
    m = _LEADING_INT_RE.match(value or "")
    if not m:
        return None
    raw = m.group("bracket") or m.group("plain")
    try:
        return int(raw)
    except Exception:
        return None


def _is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


_P1_COLOR_LANE_RE = re.compile(r"^###\s+(?P<idx>[0-7])\s+", re.MULTILINE)


def _p1_validate_color_weave(p1_md: str) -> tuple[dict[str, bool], list[str]]:
    """Validate P1 color-weave shape.

    Rules (minimal + deterministic):
    - Exactly 2 top colors listed (as bullets) in the Top Colors marker region
    - All 8 lanes 0..7 exist as H3 headings ("### <idx> <name>")
    - Shadow lane mentions black + red
    """

    results: dict[str, bool] = {}
    notes: list[str] = []

    top_region = _extract_between(
        p1_md, "<!-- P1_TOP_COLORS_START -->", "<!-- P1_TOP_COLORS_END -->"
    )
    top_lines = [ln.strip() for ln in (top_region or "").splitlines()]
    top_bullets = [
        ln[2:].strip() for ln in top_lines if ln.startswith("- ") and ln[2:].strip()
    ]
    results["p1_top_colors_exactly_2"] = len(top_bullets) == 2
    if not results["p1_top_colors_exactly_2"]:
        notes.append(f"Top Colors bullets found={len(top_bullets)}")

    lane_idxs = [int(m.group("idx")) for m in _P1_COLOR_LANE_RE.finditer(p1_md)]
    lane_set = set(lane_idxs)
    results["p1_has_all_8_lanes_0_7"] = lane_set == set(range(8))
    if not results["p1_has_all_8_lanes_0_7"]:
        missing = [str(i) for i in range(8) if i not in lane_set]
        extra = [str(i) for i in sorted(lane_set) if i not in set(range(8))]
        if missing:
            notes.append(f"Missing lanes: {', '.join(missing)}")
        if extra:
            notes.append(f"Unexpected lanes: {', '.join(extra)}")

    shadow_ok = False
    shadow_heading = "### 7"
    idx = p1_md.find(shadow_heading)
    if idx >= 0:
        tail = p1_md[idx:]
        # Clip to next lane heading (or next H2)
        cut = tail.find("\n### ", 1)
        if cut >= 0:
            tail = tail[:cut]
        shadow_lower = tail.lower()
        shadow_ok = ("black" in shadow_lower) and ("red" in shadow_lower)
    results["p1_shadow_mentions_black_and_red"] = shadow_ok
    if not shadow_ok:
        notes.append("Shadow lane missing black/red mentions")

    return results, notes


_MERMAID_BLOCK_RE = re.compile(r"```mermaid\n.*?\n```", re.DOTALL)


def _extract_mermaid_blocks(md: str) -> list[str]:
    return [m.group(0).strip() for m in _MERMAID_BLOCK_RE.finditer(md)]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Finalize a HIVE8 turn by composing meta synthesis from port artifacts."
    )
    ap.add_argument("--manifest", required=True, help="Path to turn_manifest.json")
    ap.add_argument(
        "--blackboard",
        default=str(DEFAULT_BLACKBOARD),
        help="Blackboard JSONL (stigmergy sink)",
    )
    ap.add_argument(
        "--no-stigmergy", action="store_true", help="Do not append stigmergy"
    )
    ap.add_argument(
        "--non-strict",
        action="store_true",
        help="Do not fail-closed when cardinality validators FAIL (still writes meta + manifest).",
    )
    ap.add_argument(
        "--finalized-utc",
        default="",
        help="Optional: override finalized_utc ISO timestamp (use for deterministic tests). Example: 2026-01-27T00:01:00Z",
    )

    args = ap.parse_args()
    strict = not args.non_strict
    finalized_utc = (args.finalized_utc or "").strip() or _utc_now_iso()

    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Fail-closed on input contract drift.
    # NOTE: user_prompt may be empty in non-strict mode.
    required_fields = [
        "turn_id",
        "created_utc",
        "mission_thread",
        "user_prompt",
        "artifacts",
    ]
    missing = []
    for k in required_fields:
        if k not in manifest:
            missing.append(k)
            continue
        if k == "user_prompt":
            continue
        if not manifest.get(k):
            missing.append(k)
    if missing:
        print(
            f"HIVE8 finalize failed: manifest missing required fields: {missing}",
            file=sys.stderr,
        )
        return 2

    mission_thread = str(manifest.get("mission_thread") or "").strip().lower()
    user_prompt = str(manifest.get("user_prompt") or "").strip()
    if strict and mission_thread not in {"alpha", "omega"}:
        print(
            "HIVE8 finalize failed strict input: mission_thread must be alpha|omega",
            file=sys.stderr,
        )
        return 2
    if strict and not user_prompt:
        print(
            "HIVE8 finalize failed strict input: user_prompt must be non-empty",
            file=sys.stderr,
        )
        return 2

    envelope_dir = Path(manifest.get("envelope_dir") or manifest_path.parent)
    meta_path = Path(
        manifest.get("meta_synthesis_path")
        or (envelope_dir / "HIVE8__meta_synthesis.md")
    )
    artifacts: dict[str, str] = manifest.get("artifacts") or {}
    manifest_commanders: dict[str, dict[str, str]] = manifest.get("commanders") or {}

    if strict:
        expected_ports = {f"P{i}" for i in range(8)}
        got_ports = set(artifacts.keys())
        if got_ports != expected_ports:
            print(
                f"HIVE8 finalize failed strict input: artifacts must have exactly {sorted(expected_ports)}; got {sorted(got_ports)}",
                file=sys.stderr,
            )
            return 2

    # Read all port artifacts once (we need multiple extracts)
    port_md: dict[str, str] = {}
    for port in PORT_ORDER:
        p = artifacts.get(port)
        if not p:
            raise SystemExit(f"Manifest missing artifact path for {port}")
        port_md[port] = _read_text(Path(p))

    # Extract per-port summaries
    extracts: list[PortExtract] = []
    for port in PORT_ORDER:
        extracts.append(_extract_port(Path(artifacts[port]), port))

    # Extract featured Mermaid diagrams for P3 and P6 (if present)
    p3_md = port_md["P3"]
    p6_md = port_md["P6"]
    p1_md = port_md["P1"]

    p3_top_region = _extract_between(
        p3_md, "<!-- P3_TOP_MERMAIDS_START -->", "<!-- P3_TOP_MERMAIDS_END -->"
    )
    p6_pearl_region = _extract_between(
        p6_md, "<!-- P6_IRIDESCENT_PEARL_START -->", "<!-- P6_IRIDESCENT_PEARL_END -->"
    )

    p3_mermaids = _extract_mermaid_blocks(p3_top_region)[:2]
    p6_mermaids = _extract_mermaid_blocks(p6_pearl_region)[:1]

    featured_lines: list[str] = []
    featured_lines.append("### P3 — Harmonic Hydra: Top Picks (2)")
    featured_lines.append("")
    if p3_mermaids:
        featured_lines.extend(p3_mermaids)
    else:
        featured_lines.append("- (no P3 top-pick Mermaid blocks found)")

    featured_lines.append("")
    featured_lines.append("### P6 — Kraken Keeper: Iridescent Pearl (1)")
    featured_lines.append("")
    if p6_mermaids:
        featured_lines.extend(p6_mermaids)
    else:
        featured_lines.append("- (no P6 pearl Mermaid block found)")

    featured_md = "\n".join(featured_lines).rstrip() + "\n"

    # Extract P1 featured colors (top 2)
    p1_top_region = _extract_between(
        p1_md, "<!-- P1_TOP_COLORS_START -->", "<!-- P1_TOP_COLORS_END -->"
    )
    p1_top_bullets = [
        ln.strip()
        for ln in (p1_top_region or "").splitlines()
        if ln.strip().startswith("- ")
    ]
    if p1_top_bullets:
        featured_colors_md = (
            "\n".join(
                ["### P1 — Web Weaver: Top 2 Colors", "", *p1_top_bullets]
            ).rstrip()
            + "\n"
        )
    else:
        featured_colors_md = (
            "\n".join(
                ["### P1 — Web Weaver: Top 2 Colors", "", "- (no top colors found)"]
            ).rstrip()
            + "\n"
        )

    # Validate P1 color weave
    p1_results, p1_notes = _p1_validate_color_weave(p1_md)
    validation_lines: list[str] = []
    validation_lines.append("### P1 Color-Weave Validators")
    validation_lines.append("")
    for key in [
        "p1_top_colors_exactly_2",
        "p1_has_all_8_lanes_0_7",
        "p1_shadow_mentions_black_and_red",
    ]:
        ok = bool(p1_results.get(key))
        validation_lines.append(f"- {'PASS' if ok else 'FAIL'}: {key}")
    if p1_notes:
        validation_lines.append("")
        validation_lines.append("Notes:")
        for n in p1_notes[:10]:
            validation_lines.append(f"- {n}")

    validation_md = "\n".join(validation_lines).rstrip() + "\n"

    # Scatter/Gather + Cardinality contract extraction/validation
    scatter_ports = {"P0", "P1", "P2", "P3"}
    ordered_ports_0_to_7 = [f"P{i}" for i in range(8)]
    expected_8_ids = [1, 2, 4, 8, 16, 32, 64, 128]

    cardinality_errors: list[dict[str, object]] = []
    ports_cardinality_summary: dict[str, dict[str, object]] = {}

    cardinality_lines: list[str] = []
    cardinality_lines.append("### Cardinality Contract Validators")
    cardinality_lines.append("")

    scatter_gather_lines: list[str] = []
    scatter_gather_lines.append("### Scatter/Gather Map (Double Diamond / PDCA)")
    scatter_gather_lines.append("")
    scatter_gather_lines.append(
        "- Ports 0–3 are **SCATTER** (diverge): publish 8^1 items and promote 2^1 items into meta."
    )
    scatter_gather_lines.append(
        "- Ports 4–7 are **GATHER** (converge): publish 8^1 items and promote 8^0 items into meta."
    )
    scatter_gather_lines.append("")
    scatter_gather_lines.append("| Port | Mode | Artifact | Meta | Promoted Items |")
    scatter_gather_lines.append("|---|---|---|---|---|")

    for port in ordered_ports_0_to_7:
        md = port_md.get(port, "")
        is_scatter = port in scatter_ports
        mode = "SCATTER" if is_scatter else "GATHER"
        artifact_label = "8^1"
        meta_label = "2^1" if is_scatter else "8^0"
        meta_expected = 2 if is_scatter else 1

        items8 = _extract_bullets_between(
            md, "<!-- HIVE8_CARD_8_ITEMS_START -->", "<!-- HIVE8_CARD_8_ITEMS_END -->"
        )
        promoted = _extract_bullets_between(
            md, "<!-- HIVE8_META_PROMOTED_START -->", "<!-- HIVE8_META_PROMOTED_END -->"
        )

        ok_items8 = len(items8) == 8
        ok_promoted = len(promoted) == meta_expected

        # Power-of-two validation: require leading IDs for artifact items and promoted items.
        item_ids = [_leading_int(x) for x in items8]
        promoted_ids = [_leading_int(x) for x in promoted]

        ok_item_ids = (item_ids == expected_8_ids) if ok_items8 else False
        ok_promoted_ids = False
        if ok_promoted:
            # Scatter expects [1,2], Gather expects [1]
            exp = [1, 2] if is_scatter else [1]
            promoted_ids_int = [pid for pid in promoted_ids if pid is not None]
            ok_promoted_ids = (len(promoted_ids_int) == len(promoted_ids)) and (
                promoted_ids_int == exp
            )

        # Also ensure IDs are powers of two if present.
        ok_all_item_ids_pow2 = (
            all((i is not None and _is_power_of_two(i)) for i in item_ids)
            if ok_items8
            else False
        )
        ok_all_promoted_ids_pow2 = (
            all((i is not None and _is_power_of_two(i)) for i in promoted_ids)
            if ok_promoted
            else False
        )

        exp_promoted_ids = [1, 2] if is_scatter else [1]
        ports_cardinality_summary[port] = {
            "mode": mode,
            "artifact_items": items8,
            "meta_promoted_items": promoted,
            "artifact_item_ids": item_ids,
            "meta_promoted_ids": promoted_ids,
            "expected_artifact_items_count": 8,
            "expected_meta_promoted_count": meta_expected,
            "expected_artifact_item_ids": expected_8_ids,
            "expected_meta_promoted_ids": exp_promoted_ids,
        }

        if not ok_items8:
            cardinality_errors.append(
                {
                    "port": port,
                    "check": "artifact_items_count",
                    "expected": 8,
                    "got": len(items8),
                    "marker_start": "<!-- HIVE8_CARD_8_ITEMS_START -->",
                    "marker_end": "<!-- HIVE8_CARD_8_ITEMS_END -->",
                    "artifact_path": artifacts.get(port, ""),
                }
            )
        if not ok_promoted:
            cardinality_errors.append(
                {
                    "port": port,
                    "check": "meta_promoted_count",
                    "expected": meta_expected,
                    "got": len(promoted),
                    "marker_start": "<!-- HIVE8_META_PROMOTED_START -->",
                    "marker_end": "<!-- HIVE8_META_PROMOTED_END -->",
                    "artifact_path": artifacts.get(port, ""),
                }
            )
        if ok_items8 and not (ok_item_ids and ok_all_item_ids_pow2):
            cardinality_errors.append(
                {
                    "port": port,
                    "check": "artifact_item_ids_pow2",
                    "expected": expected_8_ids,
                    "got": item_ids,
                    "artifact_path": artifacts.get(port, ""),
                }
            )
        if ok_promoted and not (ok_promoted_ids and ok_all_promoted_ids_pow2):
            cardinality_errors.append(
                {
                    "port": port,
                    "check": "meta_promoted_ids_pow2",
                    "expected": exp_promoted_ids,
                    "got": promoted_ids,
                    "artifact_path": artifacts.get(port, ""),
                }
            )

        cardinality_lines.append(
            f"- {port}: {'PASS' if ok_items8 else 'FAIL'} artifact_items_count (expected 8, got {len(items8)})"
        )
        cardinality_lines.append(
            f"- {port}: {'PASS' if ok_promoted else 'FAIL'} meta_promoted_count (expected {meta_expected}, got {len(promoted)})"
        )
        cardinality_lines.append(
            f"- {port}: {'PASS' if (ok_item_ids and ok_all_item_ids_pow2) else 'FAIL'} artifact_item_ids_pow2 (expected {expected_8_ids})"
        )
        cardinality_lines.append(
            f"- {port}: {'PASS' if (ok_promoted_ids and ok_all_promoted_ids_pow2) else 'FAIL'} meta_promoted_ids_pow2 (expected {[1, 2] if is_scatter else [1]})"
        )

        promoted_cell = "<br>".join(promoted) if promoted else "(not filled)"
        scatter_gather_lines.append(
            f"| {port} | {mode} | {artifact_label} | {meta_label} | {promoted_cell} |"
        )

    scatter_gather_md = "\n".join(scatter_gather_lines).rstrip() + "\n"
    cardinality_md = "\n".join(cardinality_lines).rstrip() + "\n"

    cardinality_passed = len(cardinality_errors) == 0

    # Stage flow (4 stages × 2 ports) derived from generator SSOT in manifest.pair_order.
    stage_flow_lines: list[str] = []
    stage_flow_lines.append("### HIVE/8 Stage Flow (4 stages × 2 ports)")
    stage_flow_lines.append("")
    pair_order = manifest.get("pair_order")
    if isinstance(pair_order, list) and pair_order:
        stage_flow_lines.append("| Stage | Phase | Pair |")
        stage_flow_lines.append("|---|---|---|")
        for idx, row in enumerate(pair_order[:4]):
            a = (row or {}).get("a") if isinstance(row, dict) else ""
            b = (row or {}).get("b") if isinstance(row, dict) else ""
            ph = (row or {}).get("phase") if isinstance(row, dict) else ""
            stage_flow_lines.append(
                f"| {idx} | {ph or '(missing)'} | {a or '(missing)'} + {b or '(missing)'} |"
            )
    else:
        stage_flow_lines.append("- (pair_order missing in manifest)")
    stage_flow_md = "\n".join(stage_flow_lines).rstrip() + "\n"

    # Final Debate + Map-Elites matrix seed: show promoted shards per port in one convergence table.
    debate_lines: list[str] = []
    debate_lines.append("### Debate Inputs (promoted shards)")
    debate_lines.append("")
    debate_lines.append("| Port | Mode | Persona | Promoted Shards |")
    debate_lines.append("|---|---|---|---|")
    for i in range(8):
        port = f"P{i}"
        port_info = ports_cardinality_summary.get(port) or {}
        mode = str(port_info.get("mode") or "")
        persona = (manifest_commanders.get(port) or {}).get("name") or port
        promoted_items = port_info.get("meta_promoted_items")
        cell = (
            "<br>".join([str(x) for x in promoted_items])
            if isinstance(promoted_items, list) and promoted_items
            else "(not filled)"
        )
        debate_lines.append(f"| {port} | {mode} | {persona} | {cell} |")
    debate_lines.append("")
    debate_lines.append("### Convergence Prompt (Map-Elites)")
    debate_lines.append("")
    debate_lines.append(
        "- Rows: ports (P0–P7). Columns: candidate strategies derived from promoted shards."
    )
    debate_lines.append(
        "- SCATTER (P0–P3) contributes 2 candidates; GATHER (P4–P7) contributes 1 champion."
    )
    debate_lines.append(
        "- Decide: best exploit path, best explore path, and the highest-risk unknowns."
    )
    final_debate_md = "\n".join(debate_lines).rstrip() + "\n"

    # Explicit meta-promoted deliverables (P0..P7 ordering)
    promoted_lines: list[str] = []
    promoted_lines.append("### Meta-Promoted Deliverables (P0 → P7)")
    promoted_lines.append("")

    def _promoted_block(port: str, label: str, expected: int) -> list[str]:
        items = _extract_bullets_between(
            port_md.get(port, ""),
            "<!-- HIVE8_META_PROMOTED_START -->",
            "<!-- HIVE8_META_PROMOTED_END -->",
        )
        header = f"#### {port} — {label} ({expected})"
        out = [header, ""]
        if items:
            out.extend([f"- {x}" for x in items[: max(expected, 1)]])
        else:
            out.append("- (not filled)")
        out.append("")
        return out

    promoted_lines.extend(_promoted_block("P0", "Two Observations", 2))
    promoted_lines.extend(_promoted_block("P7", "One Alignment (S3 Handoff)", 1))
    promoted_lines.extend(_promoted_block("P1", "Two Top Colors (8-color weave)", 2))

    # P6: promoted deliverable is the Iridescent Pearl Mermaid (UML-flavored).
    promoted_lines.append("#### P6 — One Iridescent Pearl (UML Mermaid) (1)")
    promoted_lines.append("")
    p6_pearl = _extract_mermaid_blocks(
        _extract_between(
            p6_md,
            "<!-- P6_IRIDESCENT_PEARL_START -->",
            "<!-- P6_IRIDESCENT_PEARL_END -->",
        )
    )
    if p6_pearl:
        promoted_lines.extend(p6_pearl[:1])
    else:
        promoted_lines.append("- (no P6 pearl Mermaid block found)")
    promoted_lines.append("")

    promoted_lines.extend(_promoted_block("P2", "Two Reflections", 2))
    promoted_lines.extend(_promoted_block("P5", "One Firewall", 1))
    promoted_lines.extend(_promoted_block("P3", "Two Injections (Batteries)", 2))
    promoted_lines.extend(_promoted_block("P4", "One Song", 1))

    meta_promoted_md = "\n".join(promoted_lines).rstrip() + "\n"

    # OBSIDIAN powerwords mapping (ports ↔ verbs ↔ JADC2 domains)
    obsidian_rows = [
        ("O", "P0", "OBSERVE", "ISR"),
        ("B", "P1", "BRIDGE", "Data Fabric"),
        ("S", "P2", "SHAPE", "Shaping"),
        ("I", "P3", "INJECT", "Delivery"),
        ("D", "P4", "DISRUPT", "Red Team"),
        ("I", "P5", "IMMUNIZE", "Blue Team"),
        ("A", "P6", "ASSIMILATE", "AAR/Store"),
        ("N", "P7", "NAVIGATE", "Navigate"),
    ]
    obsidian_lines: list[str] = []
    obsidian_lines.append("### OBSIDIAN Powerwords (Ports ↔ JADC2 Domains)")
    obsidian_lines.append("")
    obsidian_lines.append("| Letter | Port | Powerword | JADC2 Domain |")
    obsidian_lines.append("|---|---|---|---|")
    for letter, port, word, domain in obsidian_rows:
        obsidian_lines.append(f"| {letter} | {port} | {word} | {domain} |")
    obsidian_md = "\n".join(obsidian_lines).rstrip() + "\n"

    # Commander mappings (test surface): 3 Slivers + 1 Equipment (Gen88 v2)
    commander_lines: list[str] = []
    commander_lines.append("### 3×Sliver + 1×Equipment Mapping (per Port)")
    commander_lines.append("")
    commander_lines.append(
        "| Port | Persona | Mosaic Domain | Sliver (Static) | Sliver (Trigger) | Sliver (Activated) | Equipment |"
    )
    commander_lines.append("|---|---|---|---|---|---|---|")

    repo_root = Path.cwd()
    mtg_port_cards = _load_port_mtg_card_map(repo_root)
    if not mtg_port_cards:
        mtg_port_cards = (
            (manifest.get("mtg_port_cards") or {})
            if isinstance(manifest.get("mtg_port_cards"), dict)
            else {}
        )

    for i in range(8):
        port = f"P{i}"
        persona = (manifest_commanders.get(port) or {}).get("name") or port
        mapping = mtg_port_cards.get(port) or {}

        mosaic_domain = (mapping.get("mosaic_domain") or "").strip()
        slivers = (
            mapping.get("slivers") if isinstance(mapping.get("slivers"), list) else []
        )
        slot_to_card: dict[str, str] = {}
        for s in slivers:
            if not isinstance(s, dict):
                continue
            slot = str(s.get("slot") or "").strip().lower()
            card = str(s.get("card") or "").strip()
            if slot and card:
                slot_to_card[slot] = card

        sliver_static = slot_to_card.get("static", "")
        sliver_trigger = slot_to_card.get("trigger", "")
        sliver_activated = slot_to_card.get("activated", "")

        equipment = (
            mapping.get("equipment")
            if isinstance(mapping.get("equipment"), dict)
            else {}
        )
        equipment_card = str(equipment.get("card") or "").strip()

        mosaic_cell = mosaic_domain or "(missing)"
        static_cell = (
            f"[{sliver_static}]({_scryfall_exact_name_url(sliver_static)})"
            if sliver_static
            else "(missing)"
        )
        trigger_cell = (
            f"[{sliver_trigger}]({_scryfall_exact_name_url(sliver_trigger)})"
            if sliver_trigger
            else "(missing)"
        )
        activated_cell = (
            f"[{sliver_activated}]({_scryfall_exact_name_url(sliver_activated)})"
            if sliver_activated
            else "(missing)"
        )
        equip_cell = (
            f"[{equipment_card}]({_scryfall_exact_name_url(equipment_card)})"
            if equipment_card
            else "(missing)"
        )

        commander_lines.append(
            f"| {port} | {persona} | {mosaic_cell} | {static_cell} | {trigger_cell} | {activated_cell} | {equip_cell} |"
        )

    commander_mappings_md = "\n".join(commander_lines).rstrip() + "\n"

    # Compose briefings markdown
    briefing_lines: list[str] = []
    for ex in extracts:
        heading = f"### {ex.port} — {ex.commander_name} ({ex.commander_port_role})"
        briefing_lines.append(heading)
        briefing_lines.append("")

        if ex.summary_bullets:
            briefing_lines.append("- Summary:")
            for b in ex.summary_bullets[:6]:
                briefing_lines.append(f"  - {b}")
        else:
            briefing_lines.append("- Summary: (not written yet)")

        briefing_lines.append(f"- Handoff: {ex.handoff_target or '(not set)'}")

        if ex.open_loops:
            briefing_lines.append("- Open loops:")
            for ol in ex.open_loops[:8]:
                briefing_lines.append(f"  - {ol}")
        else:
            briefing_lines.append("- Open loops: (none listed)")

        briefing_lines.append("")

    briefings_md = "\n".join(briefing_lines).rstrip() + "\n"

    # Compose open loops union
    union: list[str] = []
    seen = set()
    for ex in extracts:
        for ol in ex.open_loops:
            key = ol.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            union.append(ol)

    if union:
        open_loops_md = "\n".join([f"- {x}" for x in union[:24]]) + "\n"
    else:
        open_loops_md = "- (none listed)\n"

    # Update meta file
    meta_text = _read_text(meta_path)
    meta_text = _replace_between(
        meta_text, AUTO_PORT_BRIEFINGS_START, AUTO_PORT_BRIEFINGS_END, briefings_md
    )
    meta_text = _replace_between(
        meta_text, AUTO_OPEN_LOOPS_START, AUTO_OPEN_LOOPS_END, open_loops_md
    )
    if (
        AUTO_FEATURED_DIAGRAMS_START in meta_text
        and AUTO_FEATURED_DIAGRAMS_END in meta_text
    ):
        meta_text = _replace_between(
            meta_text,
            AUTO_FEATURED_DIAGRAMS_START,
            AUTO_FEATURED_DIAGRAMS_END,
            featured_md,
        )

    if (
        AUTO_FEATURED_COLORS_START in meta_text
        and AUTO_FEATURED_COLORS_END in meta_text
    ):
        meta_text = _replace_between(
            meta_text,
            AUTO_FEATURED_COLORS_START,
            AUTO_FEATURED_COLORS_END,
            featured_colors_md,
        )

    if (
        AUTO_VALIDATION_RESULTS_START in meta_text
        and AUTO_VALIDATION_RESULTS_END in meta_text
    ):
        meta_text = _replace_between(
            meta_text,
            AUTO_VALIDATION_RESULTS_START,
            AUTO_VALIDATION_RESULTS_END,
            validation_md,
        )

    if (
        AUTO_SCATTER_GATHER_LABELS_START in meta_text
        and AUTO_SCATTER_GATHER_LABELS_END in meta_text
    ):
        meta_text = _replace_between(
            meta_text,
            AUTO_SCATTER_GATHER_LABELS_START,
            AUTO_SCATTER_GATHER_LABELS_END,
            scatter_gather_md,
        )

    if AUTO_STAGE_FLOW_START in meta_text and AUTO_STAGE_FLOW_END in meta_text:
        meta_text = _replace_between(
            meta_text, AUTO_STAGE_FLOW_START, AUTO_STAGE_FLOW_END, stage_flow_md
        )

    if (
        AUTO_CARDINALITY_VALIDATION_START in meta_text
        and AUTO_CARDINALITY_VALIDATION_END in meta_text
    ):
        meta_text = _replace_between(
            meta_text,
            AUTO_CARDINALITY_VALIDATION_START,
            AUTO_CARDINALITY_VALIDATION_END,
            cardinality_md,
        )

    if (
        AUTO_META_PROMOTED_DELIVERABLES_START in meta_text
        and AUTO_META_PROMOTED_DELIVERABLES_END in meta_text
    ):
        meta_text = _replace_between(
            meta_text,
            AUTO_META_PROMOTED_DELIVERABLES_START,
            AUTO_META_PROMOTED_DELIVERABLES_END,
            meta_promoted_md,
        )

    if (
        AUTO_OBSIDIAN_POWERWORDS_START in meta_text
        and AUTO_OBSIDIAN_POWERWORDS_END in meta_text
    ):
        meta_text = _replace_between(
            meta_text,
            AUTO_OBSIDIAN_POWERWORDS_START,
            AUTO_OBSIDIAN_POWERWORDS_END,
            obsidian_md,
        )

    if (
        AUTO_COMMANDER_MAPPINGS_START in meta_text
        and AUTO_COMMANDER_MAPPINGS_END in meta_text
    ):
        meta_text = _replace_between(
            meta_text,
            AUTO_COMMANDER_MAPPINGS_START,
            AUTO_COMMANDER_MAPPINGS_END,
            commander_mappings_md,
        )

    if AUTO_FINAL_DEBATE_START in meta_text and AUTO_FINAL_DEBATE_END in meta_text:
        meta_text = _replace_between(
            meta_text, AUTO_FINAL_DEBATE_START, AUTO_FINAL_DEBATE_END, final_debate_md
        )

    meta_path.write_text(meta_text, encoding="utf-8")

    # Persist machine-readable finalize results into the manifest (SSOT-ish turn record).
    manifest["meta_synthesis_path"] = str(meta_path.as_posix())
    manifest["finalize"] = {
        "finalized_utc": finalized_utc,
        "strict": strict,
        "cardinality_validation_passed": cardinality_passed,
        "cardinality_errors": cardinality_errors,
        "ports": ports_cardinality_summary,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if strict and not cardinality_passed:
        print(
            f"HIVE8 finalize failed strict cardinality validation: {len(cardinality_errors)} error(s).\n"
            f"See manifest.finalize.cardinality_errors in {manifest_path.as_posix()}.",
            file=sys.stderr,
        )
        return 2

    # Optionally append stigmergy once meta is assembled and validations pass
    if (not args.no_stigmergy) and cardinality_passed:
        event = {
            "ts_utc": finalized_utc,
            "kind": "hive8_turn_envelope",
            "finalized": True,
            "agent_mode": manifest.get("agent_mode") or "hfo_hive_8_agent_gen_88_v_4",
            "turn_id": manifest.get("turn_id"),
            "mission_thread": manifest.get("mission_thread"),
            "envelope_dir": str(envelope_dir.as_posix()),
            "manifest_path": str(manifest_path.as_posix()),
            "canonical_s3_path": manifest.get("canonical_s3_path") or "",
            "artifacts": artifacts,
            "meta_synthesis_path": str(meta_path.as_posix()),
        }
        _append_jsonl(Path(args.blackboard), event)

    print(str(meta_path.as_posix()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
