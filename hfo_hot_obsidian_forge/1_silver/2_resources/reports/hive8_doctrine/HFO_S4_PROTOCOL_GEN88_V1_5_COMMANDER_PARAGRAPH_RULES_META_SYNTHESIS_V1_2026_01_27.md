<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
---
medallion_layer: silver
mutation_score_target: 0.88
hfo_scope: hive8
protocol: hfo_s4_protocol_gen88_v1_5_commander_paragraph_rules
version: v1
created_utc: 2026-01-27
---

# HFO S4 Protocol — Commander Paragraph Rules + Meta Synthesis (Silver)

## Commander Global Rules
- Each commander writes **exactly 1 paragraph**.
- Distinct voice/behavior per port; do not merge voices.
- Assume tokens are plentiful but finite; avoid minutiae.
- P7 keeps **2–8** concurrent plan branches alive (never 1).
- P6 chooses exactly one objective mode per cycle: `ALPHA` or `OMEGA`.
- P4 is always-on; peacetime more aggressive, crisis more cooperative.
- “Ambushes” are treated as a P0 weakness; P4 drills them continuously.

## Per-Port Paragraph Focus (Single Paragraph Each)
- P0 (Hindsight): facts, contradictions, blind spots, reacquisition plan
- P7 (Hindsight): fork set (2–8), descriptors, selection pressure (fitness TBD)
- P1 (Insight): shared fabric/contract state, coordination friction, routing
- P6 (Insight): assimilation objective (ALPHA/OMEGA), assets harvested, reuse plan
- P2 (Validated Foresight): shape posture/composition, runnable representations, probes
- P5 (Validated Foresight): tripwires, invalid-if constraints, fail-closed actions
- P3 (Evolution): payload mutations, reversible deltas, capability injection
- P4 (Evolution): adversarial critique, exploit catalog, training drills

## Meta Synthesis (Required Fields)
- `branch_table`: `{branch_id, intent, fitness_hypothesis, gate_status, next_probe}`
- `trade_study_matrix`: 2–4 options with pros/cons and when-to-use
- `meta_analysis`: agreement_zones, tensions, missing_signals, failure_modes
- `final_recommendation`: chosen_branch_or_portfolio + why

## Governance
- P5 can veto any branch failing tripwires.
- P7 selects via exemplar composition; keep diversity unless gated out.
- If missing signals: emit `MISSING:<field>` and default to safest reversible action.

## Sources
- ttao-notes-2026-1-27.md
