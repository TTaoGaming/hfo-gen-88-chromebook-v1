# Gen81 QUINE: Technology + Workflow (curated)

This document is the “what we run + how we work” listing for Gen81.

## Core workflow (budgeted, swarm-safe)

- **Start small**: read curated context first; avoid repo-wide ingestion.
- Use **PREY₈** to budget parallel work.
- Treat storage constraints as a first-class part of the execution plan.

## Apex Assimilation Analysis (AoA/DSE planning step)

Before PDCA and implementation, Gen81 runs an **Apex Assimilation Analysis**: a NASA-style **AoA/DSE** trade study with **TRL/maturity**, **mission fit** scoring, and explicit **Pareto frontier** thinking.

This is intentionally probabilistic (distributions, not “one right answer”), and it is framed as multi-time-horizon **H‑POMDP** planning.

Primary note:
- [active/kiro_dev_2025/.kiro/steering/context_payload/07-APEX_ASSIMILATION_ANALYSIS.md](/active/kiro_dev_2025/.kiro/steering/context_payload/07-APEX_ASSIMILATION_ANALYSIS.md)

## System spine

### PREY₈ execution dial

Source: [_archive/archive_dev_2025/HFO_buds/generation_80/GEN_80.3_PREY8_OBSIDIAN.md](/_archive/archive_dev_2025/HFO_buds/generation_80/GEN_80.3_PREY8_OBSIDIAN.md)

- Perceive / React / Execute / Yield
- 8-based parallelism
- Single-writer stores imply cautious E/Y

### OBSIDIAN 8 ports

- 0 Observer (sense)
- 1 Bridger (connect)
- 2 Shaper (transform)
- 3 Injector (deliver)
- 4 Disruptor (chaos)
- 5 Immunizer (validate)
- 6 Assimilator (remember)
- 7 Navigator (navigate)

### Obsidian Matrix (Greek ↔ I‑Ching ↔ JADC2)

If you need the explicit ontology crosswalk (Greek metaphysics, Bagua/I‑Ching, JADC2 verbs, and “tech stack” exemplars), use:

- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md)

## Gen81 datalake + memory

Primary spec: [active/kiro_dev_2025/hfo-gen81-datalake/design.md](/active/kiro_dev_2025/hfo-gen81-datalake/design.md)

- Bronze: `_archive/**` read-only
- Silver: DuckDB with hybrid search
  - VSS (vector similarity)
  - FTS (full-text search)
- Gold: curated exports for new sessions
- Cold: stigmergy markers

### Memory MCP (intended shape)

Gen81’s memory layer is intended to expose **exactly 4 tools**:

- `search_exact`
- `search_semantic`
- `search_hybrid`
- `search_related`

(See the Gen81 spec for details.)

## Gesture control plane (adopt-first)

Primary anchor: [_archive/Spatial_Input_Mobile/ObsidianBlackboard.md](/_archive/Spatial_Input_Mobile/ObsidianBlackboard.md)

- Input options: MediaPipe Tasks GestureRecognizer; optional richer Landmarker; Human.js is also a candidate.
- Core adapter logic: FSM clutch + hysteresis + debouncing + (optional) lookahead.
- Output: stable controller events consumable by multiple runtimes.

## Tool virtualization (factory path)

Gen81 treats “tool virtualization” as a factory outcome of the same architecture:

- Standard surfaces first (e.g., WebXR controller emulation).
- Minimal adapters (VRM retargeting, training overlays) behind flags.
- Guard rails (goldens/smokes) so the factory stays reproducible.

Anchors:

- [_archive/Spatial Input Mobile/tmp/backup_20250921T225726/docs/knowledge/HFO_PURPOSE_Semantic_Knife.md](/_archive/Spatial%20Input%20Mobile/tmp/backup_20250921T225726/docs/knowledge/HFO_PURPOSE_Semantic_Knife.md)
- [_archive/Spatial Input Mobile/tmp/backup_20250921T225726/scaffolds/webway_ww-2025-081_tool_virtualization_xr_adoption.md](/_archive/Spatial%20Input%20Mobile/tmp/backup_20250921T225726/scaffolds/webway_ww-2025-081_tool_virtualization_xr_adoption.md)

## Testing harness + validation posture

- Disruptor + Immunizer are treated as first-class (chaos + guards).
- Prefer:
  - feature flags
  - reversible adapters
  - small smokes
  - golden snapshots (when appropriate)

## Practical tech inventory (high-level)

This is not meant to be exhaustive; it’s the *architecturally relevant* list.

- Storage/search: DuckDB (Silver), JSONL (Hot/ingest), curated Markdown (Gold)
- Orchestration/state: XState (Navigator exemplar)
- Messaging/bus: NATS (Bridger exemplar)
- Validation: Zod (Immunizer exemplar)
- Logging: Pino (Assimilator exemplar)
- Gesture input: MediaPipe Tasks, Human.js
- Runtimes: Phaser/PlayCanvas/Babylon/Unity/Three/VRM

## Current Gen81 constraints (operational)

- Keep Kiro context small by default.
- Treat `_ref/**` and `.history/**` as high-risk for context blowups.
- Prefer generating small Gold exports (like this folder) to onboard new AI sessions.
