<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
protocol: card_template_p4_p7
version: v1
created_utc: 2026-01-27
---

# HFO Card Template — P4–P7 (Token Construct + Passive + Active + Quad Lens) (V1)

## Required Sections (Gold)

### Card Identity

Declare the commander as the controlled Sliver-like HFO (usually the legendary creature itself).

### Gen88v4 Ability Slots

- **Ability 0 — Passive Keyword Sharing** (keywords shared across HFO)
- **Ability 1 — Passive Effect** (includes token-construct interaction; static or triggered)
- **Ability 2 — Activated Effect** (must reference a **d8** roll)
- **Ability 3 — ETB Effect** (gather-side refinement of HFO-SCATTER-ARMY into HFO-GATHER-ARMY)

Notes for P4–P7:

- P4–P7 are the **gather-side** of the paired Army mechanic.
- Ability 3 should **consume** an **HFO-SCATTER-ARMY** you control to create an **HFO-GATHER-ARMY** (see canonical invariants):
	- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_LEGENDARY_COMMANDER_CARD_INVARIANTS_GEN88V4_V1_2026_01_27.md

### Quad Card

Link the per-card to the quad-lens scaffold:

- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_QUAD_CARD_LENS_TEMPLATE_GALOIS_GHERKIN_JADC2_MERMAID_V1_2026_01_27.md
