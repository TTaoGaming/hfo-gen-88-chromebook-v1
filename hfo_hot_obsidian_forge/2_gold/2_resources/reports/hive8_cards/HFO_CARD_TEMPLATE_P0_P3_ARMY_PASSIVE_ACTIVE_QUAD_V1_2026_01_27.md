<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
protocol: card_template_p0_p3
version: v1
created_utc: 2026-01-27
---

# HFO Card Template — P0–P3 (Army + Passive + Active + Quad Lens) (V1)

## Required Sections (Gold)

### Card Identity

Declare the commander as the controlled Sliver-like HFO (usually the legendary creature itself).

### Gen88v4 Ability Slots

- **Ability 0 — Passive Keyword Sharing** (keywords shared across HFO)
- **Ability 1 — Passive Effect** (static or triggered effect)
- **Ability 2 — Activated Effect** (must reference a **d8** roll)
- **Ability 3 — ETB Effect** (often the token construct for P0–P3)

Ability 3 invariant for P0–P3 (scatter):

- Create **HFO-SCATTER-ARMY** (see canonical invariants):
	- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_LEGENDARY_COMMANDER_CARD_INVARIANTS_GEN88V4_V1_2026_01_27.md

### Quad Card

Link the per-card to the quad-lens scaffold:

- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_QUAD_CARD_LENS_TEMPLATE_GALOIS_GHERKIN_JADC2_MERMAID_V1_2026_01_27.md

## Minimal Fill-In Form

## Card Box

- Name: `…`
- Type line: `Legendary Creature — HFO`

## 0) Controlled HFO (HFO under control)

- Controlled HFO: `…`

## Ability 0 — Passive Keyword Sharing

- … have …

## Ability 1 — Passive Effect

- …

## Ability 2 — Activated Effect

- … have “{T}: Roll a d8. …”

## Ability 3 — ETB Effect

- When … enters the battlefield, create **HFO-SCATTER-ARMY**, a colorless **Artifact Creature — Army HFO** token with base **0/0**. It enters with a **+1/+1 counter** on it for each **HFO permanent** you control.

## Quad Card

- Galois lattice identity: …
- Declarative gherkin: …
- JADC2 / mosaic: …
- Mermaid proof: …
