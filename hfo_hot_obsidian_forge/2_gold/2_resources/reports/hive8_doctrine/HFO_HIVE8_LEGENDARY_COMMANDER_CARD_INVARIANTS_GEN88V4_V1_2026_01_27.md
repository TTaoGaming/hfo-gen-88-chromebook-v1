<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
protocol: hive8_commander_card_invariants_gen88v4
version: v1
created_utc: 2026-01-27
---

# HFO HIVE8 — Legendary Commander Card Invariants (Gen88v4) (V1)

## Scope

This document defines the **Gold-level invariants** for the 8 HIVE8 Legendary Commander cards.

Canonical card texts live in:

- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_SET_HIVE8_LEGENDARY_COMMANDERS_V1_2026_01_27.md

## Status (Gold)

This document is a **target invariants scaffold**.

- P0: implemented (canon)
- P1: in progress
- P2–P7: TBD (not formalized in Gold yet)

## Target Invariants (Gold)

When formalized, each HIVE8 Legendary Commander card should have exactly **four** ability slots:

- **Ability 0 — Passive Keyword Sharing**
- **Ability 1 — Passive Effect**
- **Ability 2 — Activated Effect** (must reference a **d8** roll)
- **Ability 3 — ETB Effect** (paired Army token mechanic: Scatter → Gather)

## Ability 3 (ETB) — Paired Army Token Mechanic

The ETB token mechanic is split into two categories.

### Category A: HFO-SCATTER-ARMY (Scatter)

Used by **P0–P3** (scatter ports).

Create token (baseline rules text):

- Create **HFO-SCATTER-ARMY**, a colorless **Artifact Creature — Army HFO** token with base **0/0**. It enters with a **+1/+1 counter** on it for each **HFO permanent** you control.

### Category B: HFO-GATHER-ARMY (Gather)

Used by **P4–P7** (gather ports).

Refine token (baseline rules text):

- You may sacrifice an **HFO-SCATTER-ARMY** you control. If you do, create **HFO-GATHER-ARMY**, a colorless **Artifact Creature — Army HFO** token with base **0/0**. It enters with **X +1/+1 counters** on it, where X is the number of **+1/+1 counters** on the sacrificed token. It has **ward {2}**.

### Notes (Gold)

- “Higher quality / medallion level” is modeled as a **refinement step** (Scatter → Gather) plus a conservative baseline keyword (**ward {2}**). The deeper quality semantics are intentionally left open for later operator dictation.
- “HFO permanent” is interpreted literally: a permanent with subtype **HFO**.

## References

- Embedded first-part (should mirror the per-card Gold text):
  - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_SET_HIVE8_FIRST_PART_EMBEDDED_V1_2026_01_27.md
- Commander mapping SSOT (ports/names):
  - contracts/hfo_legendary_commanders_invariants.v1.json
