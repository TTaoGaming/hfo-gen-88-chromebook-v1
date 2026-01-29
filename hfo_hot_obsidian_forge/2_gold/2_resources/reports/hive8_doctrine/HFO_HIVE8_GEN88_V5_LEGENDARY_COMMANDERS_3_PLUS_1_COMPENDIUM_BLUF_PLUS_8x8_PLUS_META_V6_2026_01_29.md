---
schema_id: hfo.hive8.compendium
schema_version: 2
version: v6
status: draft

doc_id: hfo.hive8.gen88.v5.legendary_commanders_3_plus_1_compendium_bluf_8x8_meta

dates:
  created_utc: "2026-01-29"
  updated_utc: "2026-01-29"

medallion:
  layer: bronze
  mutation_score: 0
  hive: V

intent:
  primary:
    - "Single-source DevOps/CDD/BDD/TDD reference for HFO HIVE8 legendary commanders (Gen88)."
    - "Machine-parseable, gate-executable, fail-closed documentation that links behaviors ↔ contracts ↔ tests ↔ ops."
  anti_goals:
    - "Do not mutate SSOT mapping tables except via versioned contracts."
    - "Do not treat Markdown views as truth; contracts are truth."

ssot:
  identity_invariants: contracts/hfo_legendary_commanders_invariants.v1.json
  mapping_contract: contracts/hfo_mtg_port_card_mappings.v5.json

views:
  prior_compendium_v5: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V5_2026_01_29.md
  port_ladders:
    P0: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P0_SENSE_OBSERVE_LIDLESS_LEGION_LADDER_8PART_V1_2026_01_28.md
    P1: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P1_FUSE_BRIDGE_THE_WEB_WEAVER_LADDER_8PART_V1_2026_01_28.md
    P2: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P2_SHAPE_SHAPE_MIRROR_MAGUS_LADDER_8PART_V1_2026_01_28.md
    P3: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P3_DELIVER_INJECT_HARMONIC_HYDRA_LADDER_8PART_V1_2026_01_28.md
    P4: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P4_DISRUPT_DISRUPT_RED_REGNANT_LADDER_8PART_V1_2026_01_28.md
    P5: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P5_DEFEND_IMMUNIZE_PYRE_PRAETORIAN_LADDER_8PART_V1_2026_01_28.md
    P6: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P6_STORE_ASSIMILATE_KRAKEN_KEEPER_LADDER_8PART_V1_2026_01_28.md
    P7: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P7_NAVIGATE_NAVIGATE_SPIDER_SOVEREIGN_LADDER_8PART_V1_2026_01_28.md

gates:
  - id: mapping_table_drift
    command: "node scripts/verify_hive8_mtg_card_mappings.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: contracts_schema
    command: "npm run test:contracts"
    pass_condition: "Exits 0"
  - id: compendium_frontmatter
    command: "node scripts/verify_hive8_compendium_frontmatter.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: mermaid_syntax
    command: "npm run mermaid:lint"
    pass_condition: "Exits 0"
  - id: precommit_gate
    command: "bash scripts/hfo_precommit_gate.sh"
    pass_condition: "Exits 0"

operational_assumptions:
  - "Cross-port payloads validate or they do not cross (fail-closed)."
  - "Memory writes use SSOT write-path only (no JSONL append)."
---

# HFO HIVE8 GEN88 — Legendary Commanders 3+1 Compendium (V6)

This V6 is a *reference layer* that makes the compendium more usable as CDD/BDD/TDD/DevOps documentation:
- CDD: contract inventory + enforcement map + producer/consumer boundaries.
- BDD: explicit behaviors per port + “what counts as done” + failure modes.
- TDD: behaviors mapped to executable gates; missing harnesses are tracked.
- DevOps: runnable commands, pass conditions, and proof artifacts.

## Prime directive
- **SSOT is law**: identities and mappings live in `contracts/`.
- **Views are disposable**: Markdown is a view; regenerate or correct it.
- **Fail-closed by default**: if it crosses a boundary, it validates.

## Canonical identity invariants (binary)
Binary is canonicalized to port index ordering: `P0..P7 == 000..111`.
- P0: 000
- P1: 001
- P2: 010
- P3: 011
- P4: 100
- P5: 101
- P6: 110
- P7: 111

## Executable Gates Index (DevOps/TDD)

| Gate | What it protects | Command | Pass condition |
| ---- | ---------------- | ------- | -------------- |
| Mapping-table drift gate | SSOT-locked 3+1 mapping table across checked Gold docs | `node scripts/verify_hive8_mtg_card_mappings.mjs` | Prints an `OK:` line and exits 0 |
| Contracts schema gate | SSOT contracts parse + invariants stay consistent | `npm run test:contracts` | Exits 0 |
| Compendium header gate | Machine-parseability + required YAML keys | `node scripts/verify_hive8_compendium_frontmatter.mjs` | Prints an `OK:` line and exits 0 |
| Mermaid lint gate | Diagrams don’t silently rot | `npm run mermaid:lint` | Exits 0 |
| Precommit gate | Router lint + repo local guardrails | `bash scripts/hfo_precommit_gate.sh` | Exits 0 |

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

## Contract Inventory (CDD)

| Contract | Scope | Producer(s) | Consumer(s) | Fail behavior |
| -------- | ----- | ----------- | ----------- | ------------- |
| contracts/hfo_legendary_commanders_invariants.v1.json | Identity + trigram + binary | Operator / doctrine | All ports | Hard fail on parse/uniqueness |
| contracts/hfo_mtg_port_card_mappings.v5.json | 3+1 mapping table SSOT | Operator / doctrine | Gold docs + verifiers | Hard fail on drift |
| contracts/hfo_blackboard_cloudevent.zod.ts | Cross-port stigmergy event | Any port | Any port | Reject invalid cloudevent |
| contracts/hfo_tripwire_events.zod.ts | Safety/guardrail triggers | P4/P5 | P7/P6 | Reject invalid event shape |
| contracts/hfo_phase_receipt.zod.ts | Phase receipts | Tooling | Tooling | Reject missing objective_pointer |
| contracts/hfo_flight_receipt.zod.ts | Flight receipts | Tooling | Tooling | Reject missing run_id |
| contracts/hfo_exemplar_event.zod.ts | Exemplars | P6 | P0/P7/P2 | Reject invalid sha256 |

## Enforcement Map (CDD → DevOps)

This table answers: “where is the contract enforced, and what breaks if it isn’t?”

| Boundary | Contract enforced | Enforced by | Proof you ran it |
| -------- | ----------------- | ----------- | ---------------- |
| Gold docs ↔ SSOT mappings | contracts/hfo_mtg_port_card_mappings.v5.json | scripts/verify_hive8_mtg_card_mappings.mjs | 4-beat payload includes verifier output |
| Contracts ↔ runtime parsing | all Zod schemas + invariants JSON | npm run test:contracts | test output in proof payload |
| Doc YAML ↔ automation | this file front matter | scripts/verify_hive8_compendium_frontmatter.mjs | verifier output |

## BDD → Gate Traceability (BDD/TDD)

| Port | Behavior (BDD invariant) | Gate(s) that enforce it today | Gap (what to add in V6+) |
| ---- | ------------------------- | ----------------------------- | ------------------------ |
| P0 | evidence must be schema-valid + provenance-tagged | contracts_schema + proof receipts | add `p0_evidence_packet` contract + unit tests |
| P1 | bridge payloads fail-closed if schema mismatch | contracts_schema + proof receipts | add adapter test harness + fuzzing |
| P2 | shape payloads normalized before injection | contracts_schema + proof receipts | add golden fixtures for pointer/touch2d |
| P3 | inject only validated effects | contracts_schema + proof receipts | add injection harness tests |
| P4 | disruption is auditable and reversible | contracts_schema + proof receipts | add “no silent damage” tripwire tests |
| P5 | defenses are fail-closed; drift is caught | mapping_table_drift + contracts_schema | add quarantine/resurrection playbook tests |
| P6 | SSOT is the only write-path | SSOT status update (operational), proof receipts | add enforcement script to detect JSONL writes |
| P7 | navigation decisions are traceable to evidence | contracts_schema + proof receipts | add nav decision record schema + replay tests |

## Port quicklinks (human layer)
These are the canonical “deep doctrine” pages; V6 stays thin and executable.
- P0 ladder: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P0_SENSE_OBSERVE_LIDLESS_LEGION_LADDER_8PART_V1_2026_01_28.md
- P1 ladder: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P1_FUSE_BRIDGE_THE_WEB_WEAVER_LADDER_8PART_V1_2026_01_28.md
- P2 ladder: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P2_SHAPE_SHAPE_MIRROR_MAGUS_LADDER_8PART_V1_2026_01_28.md
- P3 ladder: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P3_DELIVER_INJECT_HARMONIC_HYDRA_LADDER_8PART_V1_2026_01_28.md
- P4 ladder: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P4_DISRUPT_DISRUPT_RED_REGNANT_LADDER_8PART_V1_2026_01_28.md
- P5 ladder: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P5_DEFEND_IMMUNIZE_PYRE_PRAETORIAN_LADDER_8PART_V1_2026_01_28.md
- P6 ladder: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P6_STORE_ASSIMILATE_KRAKEN_KEEPER_LADDER_8PART_V1_2026_01_28.md
- P7 ladder: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P7_NAVIGATE_NAVIGATE_SPIDER_SOVEREIGN_LADDER_8PART_V1_2026_01_28.md

## V6 upgrade backlog (Pareto)
1) Add a small “port harness” test per port that asserts at least one real boundary contract.
2) Add a CI job that runs: mapping drift + contracts + compendium YAML + mermaid lint.
3) Add a replayable “decision record” schema for P7 and a minimal replay test.
