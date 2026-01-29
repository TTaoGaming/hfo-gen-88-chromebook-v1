---
medallion_layer: gold
mutation_score: "0%"  # template; narrative
hfo_scope: hive8
template: hive8_port_translation_ladder
version: v2
created: 2026-01-28
provenance:
  identity_ssot: contracts/hfo_legendary_commanders_invariants.v1.json
  mapping_ssot: contracts/hfo_mtg_port_card_mappings.v5.json
  generator: scripts/render_hive8_port_translation_ladder.mjs
---

# Template: HIVE8 Port Translation Ladder (8-part, Galois→Meadows)

Use this template to create one deep-dive per port (P0–P7) that follows the same 8-part structure:

0) **Galois lattice + identity + 3+1 cards (+ relevant data)**
1) **Plain-language analogies + cognitive scaffolding**
2) **JADC2 MOSAIC tiles**
3) **Declarative Gherkin + 2 Mermaid diagrams**
4) **Devil’s advocate / red-team weaknesses**
5) **Invariants list**
6) **Key tags + metadata summaries + 1 Mermaid diagram**
7) **Systems engineering (Donna Meadows vocabulary)**

## Recommended creation workflow
- Generate a skeleton from SSOT:
  - `node scripts/render_hive8_port_translation_ladder.mjs --port P0 --out <path>`
- Fill in the analogies/examples and the Meadows sections.
- Keep identity fields *verbatim* from SSOT.

## Required structure
- Part 0 — Galois lattice + identity + 3+1 cards (SSOT)
- Part 1 — Plain-language analogies + cognitive scaffolding
- Part 2 — JADC2 MOSAIC tiles
- Part 3 — Declarative Gherkin + 2 Mermaid diagrams
- Part 4 — Devil’s advocate / red teaming
- Part 5 — Invariants list
- Part 6 — Key tags + metadata summaries + 1 Mermaid diagram
- Part 7 — Systems engineering (Donna Meadows)

## Guardrail
- Treat `contracts/*` as law.
- Treat Gold docs as views.
- If a card mapping in a narrative doc disagrees with SSOT, fix the doc.
