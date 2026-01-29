<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: silver
mutation_score_target: 0.88
hfo_scope: hive8
port: P0
powerword: OBSERVE
jadc2_domain: ISR
card_id: p0_lidless_legion
version: v1
created_utc: 2026-01-27
---

# HFO Card — P0: The Lidless Legion (V1)

## Stabilized Rules Text (Oracle-Style)

### The Lidless Legion

**Type line (project formalization):** Legendary Creature — Sliver HFO

**Rules text:**

- When The Lidless Legion enters the battlefield, create a token named **Lidless Legion Army** that’s a colorless **Artifact Creature — Army HFO** with “This creature’s power and toughness are each equal to the number of HFO permanents you control.”
- Slivers have vigilance.
- Slivers have “{T}: Look at a random card in target opponent’s library. Scry 1.”

## Token Definition

### Lidless Legion Army

- Name: Lidless Legion Army
- Types: Artifact Creature — Army HFO
- Color: Colorless
- P/T: */* where both are equal to the number of HFO permanents you control (dynamic)

## Interpretation Notes (From Dictation)

- “artifact token that is type hfo” is modeled as the token having subtype/tag **HFO**.
- “power = to number of hfo permanents I control” is implemented as a dynamic P/T definition.
- “do not shuffle” is not encoded as an explicit clause because the formalized effect does not perform a search or shuffle.

## Grimoire Hooks (Search/Recall)

Use these as stable keywords in turn artifacts and SSOT memory chunks:

- hyper fractal obsidian
- grimoire
- galois_lattice
- declarative_gherkin
- heartbeat_mantra
- quine
- gem_gene_seed
- hydra_buds

## Related Doctrine

- hfo_hot_obsidian_forge/0_bronze/2_resources/reports/hive8_cards/HFO_CARD_P0_LIDLESS_LEGION_V0_1_2026_01_27.md
- hfo_hot_obsidian_forge/1_silver/2_resources/reports/hive8_doctrine/HFO_GRIMOIRE_POWERWORDS_ALIAS_EQUIVALENCE_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_OBSIDIAN_POWERWORDS_JADC2_DOMAIN_MAP_V1_2026_01_26.md
