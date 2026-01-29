<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# HFO Pain Points (Gen 1–40) — Evidence-Backed Extract (V1, 2026-01-28)

## What is present locally (repo evidence)

- Local “gene seed” corpus exists for generations 1–40 under:
  - `hfo_hot_obsidian/bronze/3_resources/ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_1/` … `gen_40/`
- The “buds/…” directory structure is referenced in some deep-dive pointers, but those specific external paths are not present as a local folder in this workspace.

## Canonical pain encyclopedia (Gen 18)

Source of record for a complete “Pain #1–21” list with definitions is Gen18’s appendix:
- `hfo_hot_obsidian/bronze/3_resources/ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_18/original_gem.md` — “Appendix D: Detailed Pain Point Encyclopedia (Generations 1-17)”

Titles (Pain #1–21):

1. **Pain #1**: Spaghetti Death Spiral (Downstream-Upstream Fighting)
2. **Pain #2**: Late Adoption (Integration Hell)
3. **Pain #3**: Premature Optimization
4. **Pain #4**: Resource Waste (Gold Plating)
5. **Pain #5**: Data Loss (Transient State)
6. **Pain #6**: Governance Gaps (Unchecked Agents)
7. **Pain #7**: Context Corridor (Narrow Vision)
8. **Pain #8**: Reinforcement Loop Spirals
9. **Pain #9**: Context Loss (Lossy Compression)
10. **Pain #10**: Role Bloat (36 Forbidden Terms)
11. **Pain #11**: False Baselines (44% L1 Lie)
12. **Pain #12**: Optimistic Override
13. **Pain #13**: Lossy Compression Death Spiral (ROOT CAUSE)
14. **Pain #14**: Manual Verification Bottleneck
15. **Pain #15**: Health Minimums Violations
16. **Pain #16**: AI Optimism Bias (Reward Hacking)
17. **Pain #17**: Tool Amnesia (Post-Summary Forgetting)
18. **Pain #18**: Upstream Cascade Failures
19. **Pain #19**: Unauthorized Singletons
20. **Pain #20**: Meta-QD (Quality Diversity on HFO Itself)
21. **Pain #21**: SOTA Research Gap

## Additional pains referenced inside Gen 1–40 corpus

### Gen 16: “Trust Crisis Learnings” (pains #22–24)

Source:
- `hfo_hot_obsidian/bronze/3_resources/ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_16/original_gem.md` — “Identified Pains #22–24”

- **Pain #22: AI Reward Hacking**
- **Pain #23: Theater Mode**
- **Pain #24: Priority Inversion**

Note: these are explicitly labeled as “Identified Pains #22–24” in Gen16.

### Gen 29: SSOT autogeneration “Pain Points” (engineering pain list)

Source:
- `hfo_hot_obsidian/bronze/3_resources/ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_29/deep_dive.md` — “SSOT Autogeneration Vision → Current State (Gen 29)”

- 760 lines of boilerplate code
- System prompts buried in Python strings
- Temperature tuning through trial-and-error
- No standardized pattern for new swarm types

## Portable / quine corpus availability (SSOT evidence)

SSOT contains many `portable_artifact` entries sourced from:
- `hfo_hot_obsidian/bronze/3_resources/ingest_sources/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52/hfo_memory.duckdb`

Example SSOT hits include “GEM GENE SEED 21” and “HFO BACKUP QUINE: GEN 72 …”, indicating the quine/gene-seed content exists in SSOT even if the portable DuckDB is not directly readable with the current tooling.

## Notes / drift to watch

- **Pain numbering can collide across documents.** For example, Gen19 uses “Pain #22” and “Pain #23” for different additions (neurobiology misalignment / exemplar drift). Treat pain IDs as *document-scoped* unless you decide on a canonical cross-gen enumeration.
