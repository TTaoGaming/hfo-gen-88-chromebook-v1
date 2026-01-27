#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Port 7 S3 v2.1 turn driver (single blessed ritual).

Automates the fail-closed S3 ritual:
1) Preflight (via scripts/hfo_flight.sh)
2) Write exactly one S3 v2.1 artifact (PARA)
3) Validate artifact (scripts/s3_v2_1_validate.py)
4) Postflight (via scripts/hfo_flight.sh)

This driver is intentionally deterministic and does not call any LLM.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional


DEFAULT_PARA_DIR = Path("hfo_hot_obsidian/bronze/3_resources/para/areas/sensemaking/s3_protocol_turns")
SPEC_PATH = Path("hfo_hot_obsidian/silver/3_resources/reports/S3_PROTOCOL_V2_1_TTAO_IDE_CARD_2026_01_25.md")
VALIDATOR_PATH = Path("scripts/s3_v2_1_validate.py")


@dataclass
class CmdResult:
    ok: bool
    code: int
    out: str


def utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utc_day() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _sanitize_slug(slug: str) -> str:
    slug = (slug or "").strip().lower()
    slug = re.sub(r"\s+", "_", slug)
    slug = re.sub(r"[^a-z0-9_\-]+", "", slug)
    slug = re.sub(r"_{2,}", "_", slug).strip("_")
    return slug or "turn"


def run_cmd(args: list[str], timeout_sec: int = 120) -> CmdResult:
    try:
        proc = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout_sec,
        )
        out = (proc.stdout or "").strip()
        if len(out) > 50000:
            out = out[:49900] + "\n…[truncated]"
        return CmdResult(ok=proc.returncode == 0, code=proc.returncode, out=out)
    except Exception as e:
        return CmdResult(ok=False, code=1, out=f"{type(e).__name__}: {e}")


def parse_multi_json(text: str) -> List[Any]:
    decoder = json.JSONDecoder()
    idx = 0
    objs: List[Any] = []
    length = len(text)
    while idx < length:
        while idx < length and text[idx].isspace():
            idx += 1
        if idx >= length:
            break
        obj, next_idx = decoder.raw_decode(text, idx)
        objs.append(obj)
        idx = next_idx
    return objs


def extract_receipt_id_from_text(text: str) -> Optional[str]:
    for obj in parse_multi_json(text):
        if isinstance(obj, dict) and isinstance(obj.get("receipt_id"), str):
            return obj["receipt_id"]
    # fallback: raw grep
    m = re.search(r"\"receipt_id\"\s*:\s*\"([0-9a-f]{8,64})\"", text)
    return m.group(1) if m else None


def write_s3_artifact(
    *,
    out_path: Path,
    para_location: str,
    risk_level: str,
    prompt_summary: str,
    attachments: list[str],
    assumptions: list[str],
    aliases_pref: str,
    aliases_alt: list[str],
    aliases_hidden: list[str],
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    attachments_json = ", ".join([f"{a}" for a in attachments])
    alt_json = ", ".join(aliases_alt)
    hidden_json = ", ".join(aliases_hidden)

    # Minimal-but-valid content; operator can iterate by editing the artifact.
    content = "\n".join(
        [
            "---",
            "protocol: S3",
            "card_version: v2.1",
            f"timestamp_utc: {utc_iso()}",
            "owner: TTao",
            f"para_location: {para_location}",
            f"risk_level: {risk_level}",
            "inputs:",
            f"  prompt_summary: {prompt_summary}",
            "  attachments_or_links:",
            *[f"    - {a}" for a in (attachments or [])],
            "assumptions_used:",
            *[f"  - {a}" for a in (assumptions or ["Operator will refine details after first pass"])],
            "aliases:  # EXEMPLAR: SKOS",
            f"  prefLabel: {aliases_pref}",
            f"  altLabel: [{alt_json}]" if aliases_alt else "  altLabel: []",
            f"  hiddenLabel: [{hidden_json}]" if aliases_hidden else "  hiddenLabel: []",
            "---",
            "",
            "# P0 — OBSERVE — Observations (current question + current state)",
            f"- Prompt summary: {prompt_summary}",
            "- Observable vs inferred: This artifact is a first-pass scaffold; content is partially inferred.",
            "- Constraints: fail-closed S3 ritual; one artifact; validate structure.",
            "- Top 3 immediate risks: (1) drift from v2.1 template, (2) missing Mermaid blocks, (3) missing proof bundle when high-risk.",
            "- What changed since last iteration (if known): Introduced a dedicated P7 S3 driver + validator behind a single entryway.",
            "",
            "# P1 — BRIDGE — Current understanding + shared data fabrics",
            "Plain language:",
            "- We are standardizing Port-7 sensemaking so every turn is auditable: preflight→artifact→postflight.",
            "- The artifact is the primary review surface; receipts prove tool use.",
            "Where truth lives right now (shared data fabric):",
            f"- Canonical S3 spec: {SPEC_PATH}",
            f"- Artifact: {out_path}",
            "",
            "```mermaid",
            "flowchart TD",
            "  A[Preflight receipt] --> B[Write 1 S3 artifact]",
            "  B --> C[Validate artifact]",
            "  C --> D[Postflight receipt]",
            "  D --> E[Short preview]",
            "```",
            "",
            "# P2 — SHAPE — Possible next actions (MAP-Elites trade study + exemplars)",
            "## P2.1 Exemplar Registry (named exemplars used in THIS run)",
            "- Exemplar name: PARA",
            "  5W1H: Who=TTao; What=organize notes; Where=Obsidian vault; When=every turn; Why=reviewable provenance; How=Projects/Areas/Resources/Archives.",
            "  Formal definition: A knowledge organization method dividing work into Projects, Areas, Resources, Archives.",
            "  Source link: https://fortelabs.com/blog/para/",
            "  How applied here: Artifact is filed under Areas/Sensemaking by default.",
            "- Exemplar name: Mermaid",
            "  5W1H: Who=developer; What=diagrams-as-text; Where=Markdown; When=each artifact; Why=portable visuals; How=flowchart/stateDiagram.",
            "  Formal definition: Text-based diagramming syntax rendered into visuals.",
            "  Source link: https://mermaid.js.org/",
            "  How applied here: Included flowchart + state diagram blocks.",
            "- Exemplar name: MAP-Elites (Quality-Diversity)",
            "  5W1H: Who=designer; What=archive of diverse options; Where=P2 matrix; When=planning; Why=avoid single-path lock-in; How=binning options.",
            "  Formal definition: Quality-Diversity algorithm that maintains an archive of high-performing diverse solutions across behavioral dimensions.",
            "  Source link: https://en.wikipedia.org/wiki/MAP-Elites",
            "  How applied here: Provide a small option matrix instead of one plan.",
            "- Exemplar name: SKOS aliasing",
            "  5W1H: Who=knowledge builder; What=preferred + alternate labels; Where=YAML front matter; When=each artifact; Why=searchability; How=prefLabel/altLabel/hiddenLabel.",
            "  Formal definition: Simple Knowledge Organization System for concept labeling and relations.",
            "  Source link: https://www.w3.org/TR/skos-reference/",
            "  How applied here: aliases block in front matter.",
            "",
            "## P2.2 Trade Study Matrix (4–8 options; exemplar-composed; MAP-Elites archive)",
            "| Option | Exemplars (names) | What changes | Pros | Cons | Risks | Proof needed | Score |",
            "|---|---|---|---|---|---|---|---|",
            "| A: Keep using bash flight manually | S3, PARA | No new code | Already works | Manual steps | Human error | Receipt files | 6 |",
            "| B: Dedicated P7 driver + validator | S3, PARA, Mermaid | Automate ritual + validate | Repeatable, auditable | New surface area | Drift if spec changes | Smoke turn + validator run | 9 |",
            "| C: Add CI gate for new S3 artifacts | S3, Mutation testing | Enforce in CI | Prevents drift | CI complexity | False negatives | CI logs | 8 |",
            "| D: Extend MCP hub tool for P7 turn | S3, MCP | Run ritual via MCP tool | Single surface | Harder integration | Tooling coupling | MCP receipt chain | 7 |",
            "",
            "# P3 — INJECT — Implementation options + injection capabilities",
            "- Injection points: scripts/ (driver+validator) + hfo_hub.py shim (dispatch).",
            "- Minimal reversible move: add commands; revert by removing dispatch + scripts.",
            "",
            "```mermaid",
            "stateDiagram-v2",
            "  [*] --> PREFLIGHT",
            "  PREFLIGHT --> WRITE_ARTIFACT: receipt_id",
            "  WRITE_ARTIFACT --> VALIDATE",
            "  VALIDATE --> POSTFLIGHT: ok",
            "  VALIDATE --> POSTFLIGHT: error",
            "  POSTFLIGHT --> [*]",
            "```",
            "",
            "# P4 — DETECT — Tests, regressions, green-lie vs red-truth checks",
            "- Current tests: structural validator run; flight receipts produced on disk.",
            "- Green lie risks: artifact looks right but misses required diagrams/sections.",
            "- Anti-green-lie upgrades: keep validator strict and optionally add CI checks.",
            "- Replay/Golden recipe: rerun p7_s3_turn with same slug and compare artifacts.",
            *(
                [
                    "- Proof Bundle: (required because risk_level=high)",
                    "  - citations/links: included in Exemplar Registry",
                    "  - tests evidence: validator output must be OK",
                    "  - replay steps: re-run the driver with the same args",
                ]
                if risk_level == "high"
                else []
            ),
            "",
            "# P5 — IMMUNIZE — Guards and risk protection",
            "- Tripwire: validator must pass or the run is outcome=error.",
            "- Rollback: delete the new artifact and rerun; receipts remain append-only.",
            "- Fail-closed defaults: do not claim success without receipts + validator OK.",
            "",
            "# P6 — ARCHIVE — Memory notes and handoff",
            "- New scripts: p7_s3_turn.py + s3_v2_1_validate.py",
            "- Root entryway: hfo_hub.py will dispatch P7 commands without breaking MCP forwarding.",
            "- Receipt parsing: handle multi-JSON outputs from flight wrapper.",
            "- PARA filing: default Areas/Sensemaking for S3 turns.",
            "",
            "# P7 — NAVIGATE — Clarifying questions for next iteration (Strange Loop N+1)",
            "- Should the P7 driver always include the preflight receipt_id in the slug? (P2)",
            "- Do you want validator strictness to fail on missing exemplar source links? (P4)",
            "- Should we add a CI gate that validates any new S3 artifact in the turns folder? (P5)",
            "- Do you want a separate MissionThread Alpha ledger entry per P7 turn, or batch them? (P6)",
            "",
        ]
    )

    out_path.write_text(content + "\n", encoding="utf-8")


def validate_artifact(path: Path) -> CmdResult:
    return run_cmd([sys.executable, str(VALIDATOR_PATH), str(path), "--json"], timeout_sec=60)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="P7 S3 v2.1 turn driver (preflight → artifact → validate → postflight)")
    ap.add_argument("--slug", required=True, help="Short slug for the turn (used in filename)")
    ap.add_argument("--objective", default="S3 P7 sensemaking turn", help="1-line objective / note for receipts")
    ap.add_argument("--para-dir", default=str(DEFAULT_PARA_DIR), help="Output PARA directory for the artifact")
    ap.add_argument(
        "--para-location",
        default="Areas/Sensemaking",
        help="PARA location string stored in YAML front matter",
    )
    ap.add_argument("--risk-level", default="low", choices=["low", "medium", "high"])
    ap.add_argument("--prompt-summary", default="", help="1–3 line prompt summary (stored in YAML)")
    ap.add_argument("--attachment", action="append", default=[], help="Attachment/link (repeatable)")
    ap.add_argument("--assumption", action="append", default=[], help="Assumption used (repeatable)")
    ap.add_argument("--aliases-pref", default="Spider Sovereign Sensemaking Protocol (S3)")
    ap.add_argument("--aliases-alt", action="append", default=["S3 protocol", "TTao IDE Card"])
    ap.add_argument("--aliases-hidden", action="append", default=["s3", "sensemaking protocol", "spider sovereign protocol"])
    ap.add_argument("--write-memory", default="true", choices=["true", "false"], help="Pass through to flight wrapper")
    ap.add_argument("--print-preview", action="store_true", help="Print short in-chat preview format")
    args = ap.parse_args(argv)

    slug = _sanitize_slug(args.slug)
    day = utc_day()

    preflight_out = Path("artifacts/flight") / f"preflight_P7_s3_{slug}_{day}.json"
    postflight_out = Path("artifacts/flight") / f"postflight_P7_s3_{slug}_{day}.json"

    preflight_cmd = [
        "bash",
        "scripts/hfo_flight.sh",
        "preflight",
        "--scope",
        "P7",
        "--note",
        args.objective,
        "--write-memory",
        args.write_memory,
        "--out",
        str(preflight_out),
    ]

    pre = run_cmd(preflight_cmd, timeout_sec=180)
    if not pre.ok:
        print(pre.out)
        return 2

    pre_text = preflight_out.read_text(encoding="utf-8") if preflight_out.exists() else pre.out
    preflight_receipt_id = extract_receipt_id_from_text(pre_text)
    if not preflight_receipt_id:
        print("Error: could not extract preflight receipt_id")
        print(pre_text[:2000])
        return 2

    para_dir = Path(args.para_dir)
    artifact_name = f"{day}__s3__{slug}_{preflight_receipt_id}__v2.1.md"
    artifact_path = para_dir / artifact_name

    prompt_summary = (args.prompt_summary or "").strip() or args.objective

    write_s3_artifact(
        out_path=artifact_path,
        para_location=args.para_location,
        risk_level=args.risk_level,
        prompt_summary=prompt_summary,
        attachments=list(args.attachment or []),
        assumptions=list(args.assumption or []),
        aliases_pref=args.aliases_pref,
        aliases_alt=list(args.aliases_alt or []),
        aliases_hidden=list(args.aliases_hidden or []),
    )

    v = validate_artifact(artifact_path)
    valid_ok = False
    try:
        payload = json.loads(v.out)
        valid_ok = bool(payload.get("ok"))
    except Exception:
        valid_ok = False

    outcome = "ok" if valid_ok else "error"
    summary = (
        f"P7 S3 turn complete: wrote 1 artifact and validator OK (preflight={preflight_receipt_id})."
        if valid_ok
        else f"P7 S3 turn failed validation; wrote artifact but validator reported errors (preflight={preflight_receipt_id})."
    )

    postflight_cmd = [
        "bash",
        "scripts/hfo_flight.sh",
        "postflight",
        "--scope",
        "P7",
        "--preflight-receipt-id",
        preflight_receipt_id,
        "--summary",
        summary,
        "--outcome",
        outcome,
        "--sources",
        ",".join(
            [
                str(SPEC_PATH),
                str(VALIDATOR_PATH),
                str(artifact_path),
                str(preflight_out),
            ]
        ),
        "--changes",
        ",".join(["scripts/p7_s3_turn.py", "scripts/s3_v2_1_validate.py", "hfo_hub.py (if used)"]),
        "--write-memory",
        args.write_memory,
        "--out",
        str(postflight_out),
    ]

    post = run_cmd(postflight_cmd, timeout_sec=180)
    if not post.ok:
        print(post.out)
        return 2

    if args.print_preview:
        # Required in-chat response format (short)
        questions = [
            "Do you want the P7 driver to auto-fill more of P2/P4 content, or keep it scaffold-only?",
            "Should we enforce strict validation of exemplar 'Source link' lines (warnings→errors)?",
            "Should the 'one blessed entryway' be `hfo_hub.py` only, or also expose a dedicated script alias?",
        ]
        assumptions = list(args.assumption or [])[:5]
        if not assumptions:
            assumptions = ["Proceeding with a scaffold-first artifact that the operator can refine."]

        print("0) Clarifying questions (2–4, plain language)")
        for q in questions[:4]:
            print(f"- {q}")
        print("1) P0–P7 preview (1 line each)")
        print("P0: Standardize auditable P7 turn ritual.")
        print("P1: Truth lives in receipts + single artifact.")
        print("P2: Options: manual flight vs driver+validator vs CI gate.")
        print("P3: Injection via scripts + hub shim dispatch.")
        print("P4: Validator prevents green lies; proof bundle gated for high risk.")
        print("P5: Fail closed if validator fails.")
        print("P6: Archive: keep grep-friendly notes + file paths.")
        print("P7: Next questions are in artifact P7.")
        print("2) Artifact path (PARA path + filename)")
        print(str(artifact_path))
        print("3) Assumptions used (2–5 bullets)")
        for a in assumptions[:5]:
            print(f"- {a}")

    # Print validator JSON output for evidence
    print(v.out)

    return 0 if valid_ok else 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
