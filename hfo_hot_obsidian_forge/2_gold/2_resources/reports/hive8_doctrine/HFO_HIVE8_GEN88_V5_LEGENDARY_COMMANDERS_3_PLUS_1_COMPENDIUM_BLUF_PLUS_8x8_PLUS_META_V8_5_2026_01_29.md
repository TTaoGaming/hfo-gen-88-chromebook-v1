---
schema_id: hfo.hive8.compendium
schema_version: 4
version: v8.5
status: canonical

doc_id: hfo.hive8.gen88.v5.legendary_commanders_3_plus_1_compendium_bluf_8x8_meta

dates:
  created_utc: "2026-01-29"
  updated_utc: "2026-01-29"

medallion:
  layer: gold
  mutation_score: 0
  hive: V

promotion:
  target_layer: hyper_fractal_obsidian
  doctrine: "Gold is verified; Hyper Fractal Obsidian is anti-fragile across recursion (8^N) with enforced provenance, replay, and bounded blast radius."
  mutation_score_target_zone: "80-99"

consistency:
  manifest: contracts/hfo_hive8_compendium_manifest.v1.json
  family_id: hfo.hive8.gen88.v5.legendary_commanders_3_plus_1_compendium_bluf_8x8_meta
  supersedes: v8.4
  policy: "Canonical is manifest-resolved; superseded docs are informational and not gate-enforced by default."

portability:
  goal: "single-file markdown (portable)"
  rule: "No http(s) URLs anywhere; no Markdown links in the portable body; any local links live only in 'Extra References (non-portable)'."

intent:
  primary:
    - "Portable, self-contained reference for HFO HIVE8 legendary commanders and ports (Gen88)."
    - "A single file you can export/share without breaking meaning or losing the core system."
    - "Keeps the portable kernel lean; deep dives are preserved as annex links under Extra References (non-portable)."
  operational:
    - "Still provides executable gate commands (for repo environments) but does not require them to understand the doctrine."

ssot_snapshot:
  identity_invariants:
    schema: "hfo.legendary_commanders.invariants.v1"
    binary_rule: "port_index == binary (P0..P7 == 000..111)"
  mapping_contract:
    schema: "hfo.mtg.port_card_mappings.v5"
    p7_trigger_note: "Regal Sliver"

ssot:
  identity_invariants: contracts/hfo_legendary_commanders_invariants.v1.json
  mapping_contract: contracts/hfo_mtg_port_card_mappings.v5.json

gates:
  - id: compendium_manifest
    command: "node scripts/verify_hive8_compendium_manifest.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: compendium_frontmatter
    command: "node scripts/verify_hive8_compendium_frontmatter.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: compendium_portable_links
    command: "node scripts/verify_hive8_compendium_portable_links.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: identity_invariants_table_drift
    command: "node scripts/verify_hive8_identity_invariants_table_drift.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: event_envelope_table_drift
    command: "node scripts/verify_hive8_event_envelope_table_drift.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: p3_blast_radius_policy_drift
    command: "node scripts/verify_hive8_p3_blast_radius_policy_drift.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: contracts_schema
    command: "npm run test:contracts"
    pass_condition: "Exits 0"
  - id: mapping_table_drift
    command: "node scripts/verify_hive8_mtg_card_mappings.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: mermaid_syntax
    command: "npm run mermaid:lint"
    pass_condition: "Exits 0"

operational_assumptions:
  - "Cross-port payloads validate or they do not cross (fail-closed)."
  - "Memory writes use the SSOT write-path only."
---

# HFO HIVE8 GEN88 — Legendary Commanders 3+1 Compendium (V8.5, Portable, Full)

This document is intentionally self-contained.

It is designed to be a better CDD/BDD/TDD/DevOps reference by being:
- CDD: contracts are enumerated as concepts and enforcement boundaries.
- BDD: each port has explicit behaviors and failure modes.
- TDD: behaviors are mapped to executable checks (gates) and known gaps.
- DevOps: a runnable gate index exists, but doctrine is understandable without running anything.

## Prime directives
- SSOT is law (identities/mappings are authoritative).
- Views are disposable (this document is a view and can be regenerated).
- Fail-closed by default (if it crosses a boundary, it validates).
- Single write-path for memory writes (SSOT only).

## Bootstrap (portable, repo-optional)
This file is designed to bootstrap HFO in two modes:

Mode A (doc-only, anywhere):
- Use the mapping table + commander pages as the doctrine lens.
- Apply the confidence tiers to every decision: LOW/MED/HIGH/BFT constrains action.
- Enforce two non-negotiables in your environment: (1) fail-closed boundaries, (2) one blessed memory write-path.

Mode B (repo-backed, promotion-grade verification):
- Run the compendium gates: `npm run verify:hive8:compendium`
- Run contract tests: `npm run test:contracts`
- Run mermaid lint (if you change diagrams): `npm run mermaid:lint`

Promotion-ready operational invariant:
- If a change cannot produce receipts (gates + tests + artifacts), it is not promoted.

## Hyper Fractal Obsidian promotion bar (V8.5)
This section defines what “above gold” means for this compendium.

Gold (today):
- Canonical selection is machine-driven (manifest-resolved).
- Portability is enforced (no http(s); no markdown links in body).
- SSOT drift is detectable (mapping + identity invariants).

Hyper Fractal Obsidian (promotion target):
- Recursion-ready: doctrine explicitly supports 8^N scaling without skipping levels (8^N → 8^(N-1)).
- Provenance is enforced across recursion: every derived claim carries receipts, and every receipt can be replayed.
- Bounded cascade is enforceable: budgets, blast radius, and rollback are machine-gated.
- Adversarial realism is mandatory: 100% certainty is treated as a failure signal (green lie).

Minimum bar to promote this doc to hyper_fractal_obsidian:
- `npm run verify:hive8:compendium` passes.
- `npm run test:contracts` passes.
- Evidence of at least one adversarial probe loop exists (P4 receipts) and is assimilated (P6), with replayable artifacts.

## Confidence + BFT doctrine (V8.5)
This section formalizes how HFO behaves when some inputs may be spoofed.

Core invariants:
- Confidence is never 100% in a healthy system.
- The system assumes at least one hidden adversary exists (Port 4 pressure) to prevent “green lies.”
- The Goldilocks zone for promotion-grade confirmation is 80–99%.
- <80% means iterate (gather more evidence, reduce scope, tighten gates).
- 100% is treated as a failure signal: the red team was not detected and defenses likely failed.

Definitions:
- **Confirmation %** is a bounded operational score in the range 0–99.
- **Confidence tier** maps confirmation into an allowed action class.
- **BFT tier** requires PBFT-style multi-party corroboration and explicit adversarial challenge.

### Confidence tiers → allowed action classes

| Tier | Confirmation band | Meaning | Allowed action class | Required checks |
| ---- | ----------------- | ------- | -------------------- | --------------- |
| LOW | 0–49% | Untrusted / spoof-risk high | Observe-only; collect evidence; no writes | P0 provenance; P1 envelope; no P3 inject |
| MED | 50–79% | Partially trusted | Limited probes in sandbox; bounded writes only | Tight blast radius; receipts; explicit P4 review |
| HIGH | 80–94% | Promotion-candidate | Bounded injection + controlled rollout | Gates pass; rollback ready; P4 adversarial test evidence |
| BFT | 95–99% | Adversarially confirmed | Production-impact allowed (still gated) | PBFT-style quorum; explicit P4 challenge; P5 enforcement |

### PBFT-style verification (conceptual mapping to the 8 ports)
We treat the octet as a quorum engine:
- **Propose (pre-prepare):** P7 proposes intent + allowed action class + budget.
- **Prepare:** P0 supplies evidence + freshness; P1 packages envelope/trace; P2 supplies candidate set; P6 supplies priors/exemplars.
- **Adversarial challenge:** P4 attempts to falsify the proposal (must produce reproducible break recipe + receipts).
- **Commit:** P5 enforces gates (no bypass paths), confirms rollback/resurrection, and blesses execution.
- **Execute:** P3 performs injection under the agreed blast radius.
- **Reply / assimilate:** P6 records results, strengthens tests/contracts, and updates replayability.

Operational rule:
- If the system computes 100% confirmation, clamp to 99% and open a “green lie” incident for investigation.

## Consistency + drift control (V8.5)
This repo intentionally contains multiple historical compendium versions. To prevent “which file is real?” drift:

- Canonical selection is machine-driven via `contracts/hfo_hive8_compendium_manifest.v1.json`.
- Gate scripts default to the canonical entry from that manifest (no more hardcoded `..._V8_...` paths).
- Superseded compendia are informational snapshots; they are not relied upon by default verifiers.

Consistency gates you can run:
- `node scripts/verify_hive8_compendium_manifest.mjs`
- `node scripts/verify_hive8_compendium_frontmatter.mjs`
- `node scripts/verify_hive8_compendium_portable_links.mjs`
- `node scripts/verify_hive8_mtg_card_mappings.mjs`

## Canonical identity invariants (binary)
Binary is canonicalized to port index ordering: P0..P7 == 000..111.

| Port | Powerword | Commander | Trigram | Binary |
| ---- | --------- | --------- | ------- | ------ |
| P0 | OBSERVE | THE LIDLESS LEGION | Kun (☷) Earth | 000 |
| P1 | BRIDGE | THE WEB WEAVER | Gen (☶) Mountain | 001 |
| P2 | SHAPE | THE MIRROR MAGUS | Kan (☵) Water | 010 |
| P3 | INJECT | HARMONIC HYDRA | Xun (☴) Wind | 011 |
| P4 | DISRUPT | RED REGNANT | Zhen (☳) Thunder | 100 |
| P5 | IMMUNIZE | PYRE PRAETORIAN | Li (☲) Fire | 101 |
| P6 | ASSIMILATE | KRAKEN KEEPER | Dui (☱) Lake | 110 |
| P7 | NAVIGATE | SPIDER SOVEREIGN | Qian (☰) Heaven | 111 |

## Mapping Table (SSOT-locked)

| Port | Commander        | Mosaic Domain                                 | Sliver (Static)      | Sliver (Trigger)   | Sliver (Activated) | Equipment (Non-creature)  |
| ---- | ---------------- | --------------------------------------------- | -------------------- | ------------------ | ------------------ | ------------------------- |
| P0   | Lidless Legion   | ISR / sensing under contest                   | Cloudshredder Sliver | Synapse Sliver     | Telekinetic Sliver | Infiltration Lens         |
| P1   | Web Weaver       | Shared data fabric / interoperability         | Quick Sliver         | Diffusion Sliver   | Gemhide Sliver     | Goldvein Pick             |
| P2   | Mirror Magus     | Creation / digital twin / spike factory       | Mirror Entity        | Hatchery Sliver    | Sliver Queen       | Illusionist's Bracers     |
| P3   | Harmonic Hydra   | Delivery / payload injection / recomposition  | The First Sliver     | Harmonic Sliver    | Hibernation Sliver | Blade of Selves           |
| P4   | Red Regnant      | Red team / contestation / destructive probing | Venom Sliver         | Thorncaster Sliver | Necrotic Sliver    | Blade of the Bloodchief   |
| P5   | Pyre Praetorian  | Blue team / defense-in-depth / recovery       | Sliver Hivelord      | Pulmonic Sliver    | Basal Sliver       | Sword of Light and Shadow |
| P6   | Kraken Keeper    | AAR / learning / assimilation                 | Dregscape Sliver     | Lazotep Sliver     | Homing Sliver      | Sword of Fire and Ice     |
| P7   | Spider Sovereign | C2 / navigate / hunt heuristics               | Sliver Legion        | Regal Sliver       | Sliver Overlord    | Lightning Greaves         |

## Canonical event envelope (P1↔P6 spine)
This section makes the P1↔P6 spine enforceable: trace continuity and provenance are not optional.

SSOT contract:
- `contracts/hfo_event_envelope.v1.json`

Portable envelope field set (must match SSOT):

| Field | Required | Meaning |
| ----- | -------- | ------- |
| event_id | yes | Stable unique id for dedupe + replay |
| event_type | yes | Semantic type name for routing + policy |
| created_utc | yes | Timestamp for freshness bounds |
| producer | yes | Producer identity + scope (port, agent_id, run_id) |
| trace | yes | Trace context (traceparent/trace_id/span_id/parent_span_id) |
| provenance | yes | Integrity (payload_sha256) + inputs summary |
| budget | yes | Explicit unit + limit so cost/blast radius is enforceable |
| payload | yes | Typed payload at the boundary |
| receipts | no | Optional receipt ids / replay ids (no URLs) |

## P3 bounded cascade policy (blast radius, enforceable)
This section makes “bounded cascade” enforceable: P3 is prohibited from injecting unless these controls are present.

SSOT contract:
- `contracts/hfo_p3_blast_radius_policy.v1.json`

Portable control set (must match SSOT):

| Control | Required | Meaning |
| ------- | -------- | ------- |
| targets_allowlist | yes | Which subjects are eligible for injection |
| max_concurrency | yes | Upper bound on parallel injections |
| budget | yes | Explicit unit + limit for effect budget |
| rollback_required | yes | Rollback must exist for any non-trivial injection |
| receipts_required | yes | No ship without receipts (replayable artifacts) |

## Gen88 “3+1” Synergy Summary (portable, V8.5)

Purpose: keep the operator-facing insights while keeping the portable kernel lean. Full narrative is preserved in Extra References.

High-signal axioms:
- P7 sets mission window + allowed action class + budgets.
- P0 produces calibrated evidence (uncertainty + provenance), or fails closed.
- P1 enforces the event envelope + metering; no schema/trace, no crossing.
- P3 ships only under bounded cascade (targets, concurrency, rollback, receipts).
- P5 is the non-bypassable gatekeeper; enforcement beats aspiration.
- P6 assimilates only source-grounded, replay-referenced truths into SSOT.

Key dyads (why the octet composes):
- 0+7: evidence → decisions (confidence governs allowed actions).
- 1+6: envelopes → learning (trace continuity is mandatory).
- 2+5: generation → safety (no ‘innovation theater’).
- 3+4: ship ↔ break (receipts bind the loop).

## Executable Gates Index (DevOps/TDD)
These commands are optional. The doctrine remains valid without running them.

| Gate | What it protects | Command | Pass condition |
| ---- | ---------------- | ------- | -------------- |
| Compendium manifest gate | Canonical selection + file existence | node scripts/verify_hive8_compendium_manifest.mjs | Prints OK: and exits 0 |
| Compendium header gate | Machine-parseability + required YAML keys | node scripts/verify_hive8_compendium_frontmatter.mjs | Prints OK: and exits 0 |
| Portability gate | No external links in body | node scripts/verify_hive8_compendium_portable_links.mjs | Prints OK: and exits 0 |
| Identity invariants drift gate | Identity table matches SSOT invariants contract | node scripts/verify_hive8_identity_invariants_table_drift.mjs | Prints OK: and exits 0 |
| Event envelope drift gate | P1↔P6 envelope table matches SSOT contract | node scripts/verify_hive8_event_envelope_table_drift.mjs | Prints OK: and exits 0 |
| P3 blast radius drift gate | Bounded cascade policy matches SSOT contract | node scripts/verify_hive8_p3_blast_radius_policy_drift.mjs | Prints OK: and exits 0 |
| Contracts schema gate | Contracts parse + invariants stay consistent | npm run test:contracts | Exits 0 |
| Mapping-table drift gate | Mapping table matches SSOT across checked docs | node scripts/verify_hive8_mtg_card_mappings.mjs | Prints OK: and exits 0 |
| Mermaid lint gate | Diagrams don’t silently rot | npm run mermaid:lint | Exits 0 |

## Contract inventory (CDD, conceptual)
This is a portable inventory: it describes what must exist and what it means.

| Contract concept | Purpose | Producer(s) | Consumer(s) | Fail behavior |
| ---------------- | ------- | ----------- | ----------- | ------------- |
| Identity invariants | Canonical names, domains, trigram, binary | Operator / doctrine | All ports + docs | Hard fail on uniqueness/bit mismatch |
| 3+1 mapping contract | Commander-to-cards mapping SSOT | Operator / doctrine | Gold docs + verifier | Hard fail on drift |
| Event envelope | Canonical cross-port envelope (id/trace/provenance/budget) | P1 | P0/P2/P3/P4/P5/P6/P7 | Reject missing envelope fields |
| P3 blast radius policy | Bounded cascade controls (targets/concurrency/budget/rollback/receipts) | P5/P7 policy | P3 | Hard fail if controls missing |
| Blackboard cloudevent | Cross-port stigmergy events | Any port | Any port | Reject invalid event shape |
| Tripwire events | Safety/guardrail triggers | P4/P5 | P7/P6 | Reject invalid event shape |
| Flight/phase receipts | Proof-of-work & continuity | Tooling | Tooling | Reject missing required fields |
| Exemplar event | Reusable exemplars for learning | P6 | P0/P7/P2 | Reject invalid sha256 |

## Enforcement map (CDD → DevOps)

| Boundary | Enforced by | Evidence |
| -------- | ----------- | -------- |
| Gold docs ↔ mapping SSOT | mapping-table drift gate | Verifier OK output + receipts |
| Identity table ↔ invariants SSOT | identity invariants drift gate | Verifier OK output |
| Envelope doctrine ↔ envelope SSOT | event envelope drift gate | Verifier OK output |
| P3 policy doctrine ↔ policy SSOT | P3 blast radius drift gate | Verifier OK output |
| Contracts ↔ parsing/uniqueness | contracts schema gate | Test output |
| Document portability | portability gate | Verifier OK output |

## BDD → Gate traceability (BDD/TDD)

| Port | Core behavior invariant (BDD) | Gate(s) that enforce it today | Gap (what to add next) |
| ---- | ----------------------------- | ----------------------------- | ---------------------- |
| P0 | No cross-port evidence without schema + provenance | contracts schema gate + receipts | Add explicit evidence packet schema + tests |
| P1 | No cross-port bridge without strict schema validation | contracts schema gate + event envelope drift gate + receipts | Add adapter harness tests + fuzzing |
| P2 | Shape payloads normalized before injection | contracts schema gate + receipts | Add golden fixtures for pointer/touch2d |
| P3 | Inject only validated, provenance-tagged effects | contracts schema gate + P3 blast radius drift gate + receipts | Add injection harness tests |
| P4 | Disruption is auditable and reversible | contracts schema gate + receipts | Add tripwire test suite (no silent damage) |
| P5 | Defenses are fail-closed; drift is detected before promotion | mapping drift gate + contracts schema gate | Add quarantine/resurrection playbook tests |
| P6 | Memory writes use the single blessed SSOT path | operational status update + event envelope drift gate + receipts | Add a detector gate for JSONL append attempts |
| P7 | Navigation decisions are traceable to evidence + contracts | contracts schema gate + receipts | Add decision record schema + replay gate |

## Port Cards (portable summary)

These are the minimum operator-facing deltas for each port. Full commander deep dives are preserved in Extra References.

| Port | Role | Primary inputs | Primary outputs | Hard-fail rule | Proof artifact |
| ---- | ---- | -------------- | --------------- | -------------- | -------------- |
| P0 | SENSE | raw signals | evidence packets | reject missing uncertainty/provenance | evidence receipts |
| P1 | BRIDGE | domain events | envelope-wrapped typed stream | reject schema/trace mismatch | envelope receipts |
| P2 | SHAPE | blessed evidence | normalized twin + candidates | reject frame/identity drift | shaping receipts |
| P3 | INJECT | validated payloads | bounded effects | reject missing rollback/receipts/budget | injection receipts |
| P4 | DISRUPT | hypotheses + targets | break recipes + tripwires | reject un-auditable probes | repro + tripwire receipts |
| P5 | IMMUNIZE | policies + proofs | gates + quarantine/resurrection | reject bypass paths | gate receipts |
| P6 | ASSIMILATE | receipts + outcomes | SSOT writes + exemplars | reject non-SSOT writes | SSOT status_update |
| P7 | NAVIGATE | evidence + constraints | bounded intent + dispatch | reject non-traceable decisions | decision receipts |

## Synergy meta synthesis (portable summary)

- The octet is a closed loop: Observe→Bridge→Shape→Inject→Disrupt→Immunize→Assimilate→Navigate.
- Safety is enforced by gates, not prose.
- Scaling is adjacent recursion: 8^N → 8^(N-1), never collapsing levels.
- Every crossing is blessed only when validated, provenance-tagged, replayable, and budget-bounded.

## Extra References (non-portable)

- Full synergy narrative (extracted from V8.5 for slim kernel): [hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/annex/HFO_HIVE8_GEN88_V5_SYNERGY_FULL_V8_5_ANNEX_2026_01_29.md](hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/annex/HFO_HIVE8_GEN88_V5_SYNERGY_FULL_V8_5_ANNEX_2026_01_29.md)
- Full commander pages deep dives (extracted from V8.5 for slim kernel): [hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/annex/HFO_HIVE8_GEN88_V5_COMMANDER_PAGES_FULL_V8_5_ANNEX_2026_01_29.md](hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/annex/HFO_HIVE8_GEN88_V5_COMMANDER_PAGES_FULL_V8_5_ANNEX_2026_01_29.md)
- V5 full compendium (source of removed embedded Appendix A): [hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V5_2026_01_29.md](hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V5_2026_01_29.md)
