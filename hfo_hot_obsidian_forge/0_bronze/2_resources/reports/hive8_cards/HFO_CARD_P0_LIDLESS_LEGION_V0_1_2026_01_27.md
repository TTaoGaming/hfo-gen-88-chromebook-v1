<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: bronze
mutation_score_target: 0.88
hfo_scope: hive8
port: P0
powerword: OBSERVE
jadc2_domain: ISR
card_id: p0_lidless_legion
version: v0_1
created_utc: 2026-01-27
---

# HFO Card — P0: The Lidless Legion (V0.1)

## Objective

Capture the operator dictation for “Port 0: The Lidless Legion” and identify ambiguity before stabilization.

## Raw Dictation (Source)

- “when enter battlefield create a */* lidless legion army artifact token that is type hfo with power = to number of hfo permanents I control, and all sliver gain tap to look at 1 random opponent card in deck and do not shuffle and scry 1. all slivers have vigilance”

## Parsed Intent (Draft)

- ETB trigger creates an **HFO** artifact “army” token whose power scales with the number of HFO permanents you control.
- Global Sliver buffs:
  - All Slivers gain vigilance.
  - All Slivers gain an activated “tap to look at a random card in an opponent’s deck” plus “scry 1”.

## Open Questions (Must Decide in Silver)

1. Scope: do the Sliver-granted abilities apply to **all Slivers** or only **Slivers you control**?
2. Token typing: is “HFO” a **subtype**, a **supertype**, or a project-level tag? (We can model as a subtype for consistency.)
3. Token P/T: dynamic (CDAs: always equals count) vs snapshot at ETB.
4. “Random opponent card in deck” semantics: which zone (library), whether revealed, and whether it moves.
5. “Do not shuffle”: if no searching occurs, this clause may be redundant; keep only if required.

## Grimoire Hooks

- Canonical alias cluster for search/tagging:
  - hyper fractal obsidian grimoire
  - galois lattice
  - declarative gherkin
  - heartbeat mantra
  - quine
  - gem gene seed
  - hydra buds

## Related Doctrine

- hfo_hot_obsidian_forge/1_silver/2_resources/reports/hive8_doctrine/HFO_GRIMOIRE_POWERWORDS_ALIAS_EQUIVALENCE_V1_2026_01_27.md
- hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_OBSIDIAN_POWERWORDS_JADC2_DOMAIN_MAP_V1_2026_01_26.md
