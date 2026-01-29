<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
protocol: hive8_commanders_3_plus_1_front_door
version: v1
created_utc: 2026-01-29
---

# HFO HIVE8 — 8 Legendary Commanders (3 Slivers + 1 Equipment) × JADC2 Mosaic Map (Front Door) (V1)

## Purpose
This is the **single entrypoint** for the HFO “8 Legendary Commanders” framing as a **3+1 bundle**:
- **3 Slivers** (Static / Trigger / Activated) = compact mnemonics for tile posture
- **1 Equipment** (non-creature) = portability / coupling-reduction primitive

It ties the mnemonic MTG mapping to the **JADC2 domain + mosaic-tile** vocabulary used by HFO ports.

## Canonical SSOT Sources (Gold)
- Card set + 3+1 mapping table: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_SET_HIVE8_LEGENDARY_COMMANDERS_V1_2026_01_27.md`
- 3+1 schema + tile narratives: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_HIVE8_3_PLUS_1_CARD_SCHEMA_AND_TILE_NARRATIVES_V1_2026_01_27.md`
- OBSIDIAN↔JADC2 vocabulary: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_OBSIDIAN_POWERWORDS_JADC2_DOMAIN_MAP_V1_2026_01_26.md`

## Canonical JSON Mappings (SSOT)
- Port→commander invariants: `contracts/hfo_legendary_commanders_invariants.v1.json`
- Port→(3 slivers + 1 equipment) mapping:
  - `contracts/hfo_mtg_port_card_mappings.v5.json`
  - `contracts/hfo_mtg_port_card_mappings.v2.json`
  - `contracts/hfo_mtg_port_card_mappings.v1.json`

## Mapping Table (Per Port)

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

## JADC2 Vocabulary (OBSIDIAN)

| Port | Powerword  | JADC2 Domain |
|---|---|---|
| P0 | OBSERVE   | ISR |
| P1 | BRIDGE    | Data Fabric |
| P2 | SHAPE     | Shaping |
| P3 | INJECT    | Delivery |
| P4 | DISRUPT   | Red Team |
| P5 | IMMUNIZE  | Blue Team |
| P6 | ASSIMILATE| AAR/Store |
| P7 | NAVIGATE  | Navigate |

## Acceptance Criteria (Gold)
- The 3+1 mapping table above exactly matches `contracts/hfo_mtg_port_card_mappings.v5.json`.
- The port→commander naming exactly matches `contracts/hfo_legendary_commanders_invariants.v1.json`.
- The JADC2 domain labels align with the OBSIDIAN vocabulary map:
  `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_OBSIDIAN_POWERWORDS_JADC2_DOMAIN_MAP_V1_2026_01_26.md`.
- This doc remains **link-only** and acts as a stable “front door”; detailed narratives live in the schema+narratives doc.
