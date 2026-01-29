<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
---
medallion_layer: silver
mutation_score_target: 0.88
hfo_scope: hive8
protocol: hfo_s4_protocol_gen88_v1_5
version: v1
created_utc: 2026-01-27
---

# HFO S4 Protocol — Gen88 v1.5 (Silver Spec)

## Objective
Harden S4 outputs against “schema-valid nonsense” by forcing explicit grounding (assumptions + falsifiers + evidence/receipts + premortem) while preserving the diverge→converge heartbeat (Double Diamond) and social cue-based sensemaking framing.

## Standards
- JSON Schema dialect: Draft 2020-12 (`$schema: https://json-schema.org/draft/2020-12/schema`)
- Validator recommendation: `ajv` / `ajv-cli` with `--spec=draft2020`
- Default posture: `additionalProperties: false` everywhere (fail-closed)

## Render Contract (Markdown)
**Primary render:** Markdown

**Top-level headings:** Exactly these sections in order, with roman numerals:
- `I) BLUF`
- `II) H — Hindsight (P0 + P7)`
- `III) I — Insight (P1 + P6)`
- `IV) V — Validated Foresight (P2 + P5)`
- `V) E — Evolution (P3 + P4)`
- `VI) Meta Synthesis (scatter→gather)`

**Hard fails**
- Missing any required section heading
- Required sections out of order
- Any extra top-level section beyond `I–VI`

## Heartbeat Rules (Scatter → Gather)
**Smallest pulse:** `2 → 1 → 2 → 1`

- Scatter roles: P0–P3
  - Each emits **Alpha** + **Beta**
  - Each subsection has **exactly 2 options**
  - Option labels are **exactly**: `Option A:` and `Option B:`
  - Each option is **one paragraph** (no blank lines)
- Gather roles: P4–P7
  - Each emits **exactly 1 Omega**
  - Omega is grounded via required fields (below)

## Role Cards (Identity)
- P0: Lidless Legion — `OBSERVE`
- P1: Web Weaver — `BRIDGE`
- P2: Mirror Magus — `SHAPE`
- P3: Harmonic Hydra — `INJECT`
- P4: Red Regnant — `DISRUPT`
- P5: Pyre Praetorian — `IMMUNIZE`
- P6: Kraken Keeper — `ASSIMILATE`
- P7: Spider Sovereign — `NAVIGATE`

## Grounding Hooks (Fail-Closed)
If required info is unknown, emit the literal token `MISSING:<field>` and default to the safest reversible next action.

### Omega Required Fields (Gather)
Each gather role’s Omega contains:
- `Nonnegotiables:`
- `Top risks:`
- `Recommended next action:`
- `Assumptions:` (min 1)
- `Falsifiers:` (min 1)
- `Evidence refs:` (0–12)
- `Premortem:`

**Formatting constraint:** each field is a single paragraph.

## Evidence References (Allowed Patterns)
Evidence refs may point at URL, file path, hash, ticket id, trace id, or dataset key.

Allowed prefix patterns:
- `url:<...>`
- `file:<...>`
- `sha256:<64-hex>`
- `ticket:<...>`
- `trace:<...>`
- `ds:<...>`

## Meta Synthesis Rules (Mini Pulse)
Meta Synthesis is itself a mini scatter→gather:
- Scatter options: exactly **2**
- Gather recommendation: exactly **1**

Required artifacts (conceptual):
- Branch portfolio (2–8 branches): `branch_id, intent, descriptor, fitness_hypothesis, gate_status, next_probe, evidence_refs`
- Trade study (2–4 options): `option, what_it_is, pros, cons, when_to_use, evidence_refs`
- Meta analysis: `agreement_zones, tensions, missing_signals, failure_modes, key_assumptions, falsifiers`
- Decision: `selected_branch_or_portfolio, why, reversibility_plan, premortem`
- Evidence register (optional; max 30): `evidence_id, ref, summary`

## Enforcement Pipeline (IR → Markdown)
1. Agent emits structured S4 IR (JSON/YAML) and validates against `S4ReportSchema_2020_12`.
2. Validator rejects on schema failure (missing fields, wrong option counts, extra fields).
3. Renderer converts IR → markdown with fixed headings + subsection headings.
4. Markdown linter applies presentation conformance checks (regex + subsection presence).

Recommended CLI:
- `ajv validate --spec=draft2020 -s s4_report_schema.json -d report.json`

## Presentation Checks (Markdown Lint)
- Subsection headings must appear exactly once each (e.g., `P0 Lidless Legion — Alpha`, `P0 Lidless Legion — Beta`, …)
- Scatter option line regex: `^Option\s+(A|B):\s+.+`
- Omega field labels required (exact): `Nonnegotiables:`, `Top risks:`, `Recommended next action:`, `Assumptions:`, `Falsifiers:`, `Evidence refs:`, `Premortem:`

## Sources
- ttao-notes-2026-1-27.md
