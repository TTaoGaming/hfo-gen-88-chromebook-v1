# Fractal Architecture / QUINE (HFO)

This is the “deep structure” vocabulary behind the 8-pillar system.

Primary sources (deep structure):

- [_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_64/dreaming/evaporated/HFO_FRACTAL_QUINE_MATRIX_v5_2025_12_03_1400.md](/_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_64/dreaming/evaporated/HFO_FRACTAL_QUINE_MATRIX_v5_2025_12_03_1400.md)
- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md)
- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/metaphysics_of_obsidian.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/metaphysics_of_obsidian.md)

## The 8 pillars (OBSIDIAN roles)

OBSIDIAN roles are mapped to multiple interpretive frames (Greek, Bagua, stigmergy, JADC2-like verbs, and a “tech stack” category). The key is that the same 8 roles are reused consistently across:

- swarm orchestration
- testing harness / guards
- memory / logging
- gesture control plane adapters

## Crosswalk: Greek ↔ I‑Ching trigram ↔ binary triplet ↔ JADC2 verb

This table is the **fastest rehydration** of the “OBSIDIAN = multi-ontology mapping” idea.

Source of this specific mapping: [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md)

Important: I‑Ching trigram ↔ 3-bit mappings have multiple conventions (Earlier Heaven vs Later Heaven). The binary triplets below use a common convention:

- Qian ☰ = 111
- Dui ☱ = 110
- Li ☲ = 101
- Zhen ☳ = 100
- Xun ☴ = 011
- Kan ☵ = 010
- Gen ☶ = 001
- Kun ☷ = 000

| OBSIDIAN role | Greek aspect | Bagua trigram | Binary triplet | JADC2 function |
|---|---|---|---|---|
| Observer | ONTOS (Being) | ☰ Qian (Heaven) | 111 | SENSE |
| Bridger | LOGOS (Reason) | ☴ Xun (Wind) | 011 | CONNECT |
| Shaper | TECHNE (Craft) | ☲ Li (Fire) | 101 | ACT |
| Injector | CHRONOS (Time) | ☳ Zhen (Thunder) | 100 | PULSE |
| Disruptor | PATHOS (Affect) | ☱ Dui (Lake) | 110 | TEST |
| Immunizer | ETHOS (Ethics) | ☶ Gen (Mountain) | 001 | DEFEND |
| Assimilator | TOPOS (Place/Memory) | ☵ Kan (Water) | 010 | STORE |
| Navigator | TELOS (Purpose) | ☷ Kun (Earth) | 000 | DECIDE |

If Gen81 wants a different Bagua↔role mapping (there are historical variants), treat the table as configurable but keep the *idea* stable: **8 roles ↔ 8 symbols ↔ 3-bit vocabulary ↔ mission verbs**.

## Structural grouping

The fractal quine groups the 8 pillars into three functional clusters:

- **Engine Quad (Execution)**: Observer → Bridger → Shaper → Injector
- **Body Triad (Regulation)**: Disruptor → Immunizer → Assimilator
- **Apex (Intent)**: Navigator

This matches how systems often behave:

- “Hot loop” produces effects.
- “Cold loop” tests/guards/stores.
- “Apex” decides what the system is trying to do.

## Octet fractal octree (recursion rule)

The “fractal” aspect means the same 8-role vocabulary applies at every scale.

- A “system” node can be split into 8 sub-nodes (octree), each assigned an OBSIDIAN role.
- This is a way to keep architecture legible as it grows: you don’t invent new taxonomies; you recurse.

For the semantic manifold / hourglass framing (past/present/future webs), see:

- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/metaphysics_of_obsidian.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/metaphysics_of_obsidian.md)

## The 64-card expansion

The quine expands the 8 pillars into an 8×8 matrix (64 “cards/holons”):

- Rows: pillar (role)
- Columns: layer/aspect

This yields a reusable way to talk about capabilities like:

- Observer×Validate (schema checks)
- Bridger×Retry (routing policy)
- Assimilator×QueryPlan (memory retrieval)
- Navigator×ContextRAG (planning with curated context)

## Why this matters in Gen81

Gen81’s medallion datalake + air gap is the operationalization of the quine:

- “Remember” has a dedicated **Silver** store.
- “Validate” becomes explicit guards and tests.
- “Navigate” becomes explicit orchestration (PREY₈ + plans).

## Minimal practical takeaway

When unclear where something belongs, ask:

1. Which pillar owns it (OBSIDIAN port)?
2. Is it hot-loop execution or cold-loop regulation?
3. Which medallion layer should hold the artifact?
4. Can it be implemented as a small adapter instead of core rewrite?
