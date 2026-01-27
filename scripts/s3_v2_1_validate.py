#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""S3 Protocol v2.1 artifact validator.

Fail-closed intent:
- Return non-zero exit code if the artifact violates non-negotiables.
- Keep checks deterministic and dependency-free.

This validator is intentionally structural (format + required blocks), not semantic.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FILENAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}__s3__.+__v2\.1\.md$")

REQUIRED_FRONT_MATTER_KEYS = [
    "protocol:",
    "card_version:",
    "timestamp_utc:",
    "owner:",
    "para_location:",
    "risk_level:",
    "inputs:",
    "assumptions_used:",
    "aliases:",
]

REQUIRED_SECTION_PREFIXES = [
    "# P0 — OBSERVE —",
    "# P1 — BRIDGE —",
    "# P2 — SHAPE —",
    "# P3 — INJECT —",
    "# P4 — DETECT —",
    "# P5 — IMMUNIZE —",
    "# P6 — ARCHIVE —",
    "# P7 — NAVIGATE —",
]


@dataclass
class Finding:
    level: str  # error|warning
    code: str
    message: str


def _extract_front_matter(text: str) -> str | None:
    text = text.lstrip("\ufeff")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return text[4:end + 1]


def _get_yaml_scalar(front_matter: str, key: str) -> str | None:
    # Very small YAML subset: key: value (single-line scalars only)
    m = re.search(rf"(?m)^{re.escape(key)}\s*([^\n#]+)?$", front_matter)
    if not m:
        return None
    value = (m.group(1) or "").strip()
    return value or None


def _count_mermaid_blocks(text: str) -> dict[str, int]:
    blocks = re.findall(r"```mermaid\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    out = {"flowchart": 0, "stateDiagram-v2": 0, "total": len(blocks)}
    for b in blocks:
        if re.search(r"\bflowchart\b", b):
            out["flowchart"] += 1
        if re.search(r"\bstateDiagram-v2\b", b):
            out["stateDiagram-v2"] += 1
    return out


def validate_artifact(path: Path, strict: bool) -> list[Finding]:
    findings: list[Finding] = []

    if not path.exists():
        return [Finding("error", "missing_file", f"File does not exist: {path}")]

    text = path.read_text(encoding="utf-8")

    if not FILENAME_RE.match(path.name):
        findings.append(
            Finding(
                "error",
                "bad_filename",
                "Filename must match YYYY-MM-DD__s3__<slug>__v2.1.md",
            )
        )

    fm = _extract_front_matter(text)
    if fm is None:
        findings.append(Finding("error", "missing_front_matter", "Missing YAML front matter (--- ... ---)."))
    else:
        for key in REQUIRED_FRONT_MATTER_KEYS:
            if re.search(rf"(?m)^{re.escape(key)}", fm) is None:
                findings.append(Finding("error", "missing_front_matter_key", f"Missing front matter key: {key}"))

        proto = _get_yaml_scalar(fm, "protocol:")
        if proto and proto != "S3":
            findings.append(Finding("error", "bad_protocol", f"protocol must be S3 (got {proto!r})."))

        card = _get_yaml_scalar(fm, "card_version:")
        if card and card != "v2.1":
            findings.append(Finding("error", "bad_card_version", f"card_version must be v2.1 (got {card!r})."))

        risk = _get_yaml_scalar(fm, "risk_level:")
        if risk and risk not in {"low", "medium", "high"}:
            findings.append(Finding("error", "bad_risk_level", f"risk_level must be low|medium|high (got {risk!r})."))

        if risk == "high":
            if re.search(r"(?i)Proof Bundle", text) is None:
                findings.append(
                    Finding(
                        "error",
                        "missing_proof_bundle",
                        "risk_level=high requires a Proof Bundle in P4 (include 'Proof Bundle' section/bullets).",
                    )
                )

    for prefix in REQUIRED_SECTION_PREFIXES:
        if prefix not in text:
            findings.append(Finding("error", "missing_section", f"Missing required section heading: {prefix}"))

    # Template-required subheadings
    if "## P2.1 Exemplar Registry" not in text:
        findings.append(Finding("error", "missing_exemplar_registry", "Missing '## P2.1 Exemplar Registry' section."))
    if "## P2.2 Trade Study Matrix" not in text:
        findings.append(Finding("error", "missing_trade_study", "Missing '## P2.2 Trade Study Matrix' section."))

    mermaid = _count_mermaid_blocks(text)
    if mermaid["flowchart"] < 1:
        findings.append(Finding("error", "missing_mermaid_flowchart", "Must include at least one Mermaid flowchart."))
    if mermaid["stateDiagram-v2"] < 1:
        findings.append(
            Finding("error", "missing_mermaid_state", "Must include at least one Mermaid stateDiagram-v2."))

    if mermaid["total"] < 2 and strict:
        findings.append(
            Finding(
                "warning",
                "few_mermaid_blocks",
                "Expected at least 2 Mermaid blocks (1 flowchart + 1 stateDiagram-v2).",
            )
        )

    # Non-strict warnings
    if "Source link:" not in text:
        findings.append(
            Finding(
                "warning",
                "missing_exemplar_sources",
                "Exemplar Registry entries should include 'Source link:'.",
            )
        )

    if strict:
        findings = [f for f in findings if f.level != "warning"]

    return findings


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Validate an S3 v2.1 Markdown artifact")
    ap.add_argument("path", help="Path to a single S3 v2.1 Markdown artifact")
    ap.add_argument("--json", action="store_true", help="Print machine-readable JSON output")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors (structural strictness)")
    args = ap.parse_args(argv)

    path = Path(args.path)
    findings = validate_artifact(path, strict=args.strict)
    ok = all(f.level != "error" for f in findings)

    if args.json:
        payload: dict[str, Any] = {
            "ok": ok,
            "path": str(path),
            "findings": [f.__dict__ for f in findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if ok:
            print(f"OK: {path}")
        else:
            print(f"INVALID: {path}")
        for f in findings:
            print(f"- {f.level.upper()} [{f.code}]: {f.message}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
