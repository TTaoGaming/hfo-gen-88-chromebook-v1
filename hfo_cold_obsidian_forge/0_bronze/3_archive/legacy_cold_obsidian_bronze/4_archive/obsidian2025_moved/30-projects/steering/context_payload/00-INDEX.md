# Gen81 Curated Context Payload (HFO)

This directory is a **bounded context pack** for new AI sessions.

## How to use

- **Do not ingest the whole repo.** Start with this folder only.
- If more context is needed, follow the links in each section and pull **only the referenced source**.
- Treat `_archive/**` as **read-only bronze**. Gen81 work happens under `active/kiro_dev_2025/**`.

## Read order (recommended)

1. [Architecture Overview](01-ARCHITECTURE.md)
2. [Dimensional Matrix](02-DIMENSIONAL_MATRIX.md)
3. [Fractal / Quine Architecture](03-FRACTAL_QUINE.md)
4. [Gen81 Tech + Workflow QUINE](04-GEN81_TECH_WORKFLOW_QUINE.md)
5. [Swarm Factory Protocols](06-SWARM_FACTORY_PROTOCOLS.md)
6. [Apex Assimilation Analysis](07-APEX_ASSIMILATION_ANALYSIS.md)
7. [Monthly Deep Dives Index](05-MONTHLY_DEEP_DIVES.md)

## Two main projects (same spine)

1. **Hive Fleet Obsidian (HFO)**: swarm orchestration platform + testing harness + stigmergy/memory system.
2. **W3C Pointer / Gesture Control Plane**: web-first gesture input pipeline (MediaPipe / Human.js) feeding a polymorphic, hexagonal adapter architecture so runtimes can be swapped (Phaser/PlayCanvas/Babylon/Unity/etc).

## Key “don’t break Kiro” constraints

- The failure mode is **context limit exceeded** caused by scanning massive folders (`_archive/**`, mirrored `_ref/**`, `.history/**`).
- This pack is intentionally small. Prefer links + surgical reads.

## Primary source anchors (do not bulk-ingest)

- Gen81 scope rule: [active/kiro_dev_2025/.kiro/steering/00-gen81-scope.md](00-gen81-scope.md)
- Gen80 formalism (PREY₈ + OBSIDIAN): [_archive/archive_dev_2025/HFO_buds/generation_80/GEN_80.3_PREY8_OBSIDIAN.md](/_archive/archive_dev_2025/HFO_buds/generation_80/GEN_80.3_PREY8_OBSIDIAN.md)
- Gen81 medallion datalake spec: [active/kiro_dev_2025/hfo-gen81-datalake/design.md](/active/kiro_dev_2025/hfo-gen81-datalake/design.md)
- Gesture control-plane blackboard (historical but key): [_archive/Spatial_Input_Mobile/ObsidianBlackboard.md](/_archive/Spatial_Input_Mobile/ObsidianBlackboard.md)
- Fractal quine matrix v5 (deep structure): [_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_64/dreaming/evaporated/HFO_FRACTAL_QUINE_MATRIX_v5_2025_12_03_1400.md](/_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_64/dreaming/evaporated/HFO_FRACTAL_QUINE_MATRIX_v5_2025_12_03_1400.md)
