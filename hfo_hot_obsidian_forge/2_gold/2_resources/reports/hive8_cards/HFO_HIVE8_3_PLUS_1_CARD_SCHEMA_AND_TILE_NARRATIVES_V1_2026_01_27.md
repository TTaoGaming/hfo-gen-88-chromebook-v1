<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
protocol: hive8_3_plus_1_card_schema
version: v1
created_utc: 2026-01-27
---

# HFO HIVE8 — 3+1 Card Schema + Tile Narratives (V1)

## Definition (3+1)
For each port (P0–P7):
- **3 Slivers** (narrative anchors) mapped to slots:
  - Static
  - Trigger
  - Activated
- **1 Equipment** (4th-slot constraint): **non-creature**

This is a **narrative mapping**: MTG card names are used as compact mnemonic labels for each tile’s behavioral posture.

## Canonical Mappings (SSOT)
- contracts/hfo_mtg_port_card_mappings.v2.json
- contracts/hfo_mtg_port_card_mappings.v5.json

## Mapping Table (Per Port)

| Port | Commander | Mosaic Domain | Sliver (Static) | Sliver (Trigger) | Sliver (Activated) | Equipment (Non-creature) |
|---|---|---|---|---|---|---|
| P0 | Lidless Legion | ISR / sensing under contest | Cloudshredder Sliver | Synapse Sliver | Telekinetic Sliver | Infiltration Lens |
| P1 | Web Weaver | Shared data fabric / interoperability | Quick Sliver | Diffusion Sliver | Gemhide Sliver | Goldvein Pick |
| P2 | Mirror Magus | Creation / digital twin / spike factory | Mirror Entity | Hatchery Sliver | Sliver Queen | Illusionist's Bracers |
| P3 | Harmonic Hydra | Delivery / payload injection / recomposition | The First Sliver | Harmonic Sliver | Hibernation Sliver | Blade of Selves |
| P4 | Red Regnant | Red team / contestation / destructive probing | Venom Sliver | Thorncaster Sliver | Necrotic Sliver | Blade of the Bloodchief |
| P5 | Pyre Praetorian | Blue team / defense-in-depth / recovery | Sliver Hivelord | Pulmonic Sliver | Basal Sliver | Sword of Light and Shadow |
| P6 | Kraken Keeper | AAR / learning / assimilation | Dregscape Sliver | Lazotep Sliver | Homing Sliver | Sword of Fire and Ice |
| P7 | Spider Sovereign | C2 / navigate / hunt heuristics | Sliver Legion | Regal Sliver | Sliver Overlord | Lightning Greaves |

## Equipment Oracle References (4th-Slot Constraint)
Infiltration Lens; Goldvein Pick; Illusionist’s Bracers; Blade of Selves; Blade of the Bloodchief; Sword of Light and Shadow; Sword of Fire and Ice; Lightning Greaves.

## Tile Narratives (Mosaic / JADC2-first)

### P0 — Lidless Legion (ISR Tile)
A denied-environment sensing tile: it seeks contact fast, expects obstruction, and treats being blocked as a primary learning channel. It converts friction into information (lens-on-block), then applies local control to stabilize the picture long enough for downstream tiles to act. Net behavior: “probe → harvest signal from resistance → constrain the local scene → hand off validated observations.”

### P1 — Web Weaver (Shared Data Fabric Tile)
An interoperability tile: it exists to reduce coupling cost and keep cross-tile coordination fluid. It makes critical actions available at interface speed (flash posture), taxes hostile interference (diffusion), and supplies universal “bus power” (gemhide) while the equipment minting portable budget (Treasure) turns coordination into measurable throughput. Net behavior: “attach/detach quickly → keep links alive under disruption → fund the fabric.”

### P2 — Mirror Magus (Creation / Spike Factory Tile)
An option-generation tile: it creates many candidate instances and rapidly amplifies the actuators that produce variants. Bracers are the validated-foresight accelerant here: they increase how many “tries” you can run per unit time (copying key activations), while the slivers supply the ability to spawn and reshape the swarm into many faces. Net behavior: “manufacture variants → amplify generation knobs → feed the evaluation layer.”

### P3 — Harmonic Hydra (Delivery / Payload Injection Tile)
An effects-delivery tile: it’s built for fan-out, on-arrival payload, and re-deploy semantics. Cascade posture pushes payloads broadly, harmonic provides the “payload on entry,” hibernation provides backoff/retry (bounce/recast), and Blade of Selves adds burst replication during delivery waves. Net behavior: “deliver broadly → apply payload on contact → retry until state change sticks.”

### P4 — Red Regnant (Red-Team Contention Tile)
A stress and degradation tile: it forces expensive engagements, converts pressure into measurable adversarial outcomes, and uses sacrifice as a deliberate destructive probe. Deathtouch and ping pressure shape the fight; necrotic turns self-loss into targeted deletion; the Bloodchief blade records every casualty as escalating threat. Net behavior: “contest constantly → destroy selectively → turn churn into compounding pressure.”

### P5 — Pyre Praetorian (Blue-Team Recovery Tile)
A defense-in-depth tile: it keeps the force package inside a survivability envelope while enabling controlled recovery. Indestructible posture reduces catastrophic loss, pulmonic biases toward continuity after death events, basal converts sacrifice into emergency fuel, and Sword of Light and Shadow couples sustained operation (life) with recoverability (return key pieces). Net behavior: “absorb shocks → recover capability → keep the system online.”

### P6 — Kraken Keeper (AAR / Learning Tile)
A learning and assimilation tile: it converts operational experience into retained advantage and re-deployable patterns. Unearth posture makes the past usable, death-to-mass (amass) turns losses into reusable substrate, homing fetches missing components, and Sword of Fire and Ice explicitly couples “do work” with “log a lesson” on each successful engagement. Net behavior: “ingest outcomes → compress into reusable patterns → replay with improved odds.”

### P7 — Spider Sovereign (C2 / Navigation Tile)
A command-and-control tile: it composes the force package, accelerates tasking, and keeps the command node protected and online. Legion provides global posture, brood compounds momentum from contact, overlord performs assembly/tasking, and Lightning Greaves ensures immediate readiness with protection so the first command cycle happens before disruption. Net behavior: “assemble → task → scale → retask under pressure.”

## Links to Gold Cards
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_P0_LIDLESS_LEGION_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_P1_WEB_WEAVER_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_P2_MIRROR_MAGUS_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_P3_HARMONIC_HYDRA_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_P4_RED_REGNANT_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_P5_PYRE_PRAETORIAN_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_P6_KRAKEN_KEEPER_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_P7_SPIDER_SOVEREIGN_V1_2026_01_27.md

## Sources
- ttao-notes-2026-1-27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_SET_HIVE8_LEGENDARY_COMMANDERS_V1_2026_01_27.md
- contracts/hfo_mtg_port_card_mappings.v2.json
