# HFO Architecture Overview (Gen81)

## North star

Build a **swarm-driven engineering platform** (HFO) that can reliably ship and evolve a **gesture-driven control plane** (W3C pointer/gesture) using a **polymorphic, hexagonal, adapter-first** architecture.

In practice: “adopt-first, add minimal glue, leave stigmergy.”

## Mission engineering framing (JADC2 / Mosaic)

Within HFO, “mission engineering” means:

- Describe an outcome (“mission”), constraints, and safety boundaries.
- Compose capabilities as **small swappable adapters** (“mosaic tiles”).
- Run a closed loop of **sense → connect → act → pulse → test → defend → store → decide** (OBSIDIAN/JADC2-aligned verbs).

This is intentionally compatible with “mosaic” thinking: composable modules, fast reconfiguration, and reversibility.

Primary ontology/matrix anchors:

- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md)
- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/metaphysics_of_obsidian.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/metaphysics_of_obsidian.md)

## The Gen80 formalism: PREY₈ + OBSIDIAN

Source: [_archive/archive_dev_2025/HFO_buds/generation_80/GEN_80.3_PREY8_OBSIDIAN.md](/_archive/archive_dev_2025/HFO_buds/generation_80/GEN_80.3_PREY8_OBSIDIAN.md)

### PREY₈

PREY₈ is the swarm execution dial: **Perceive → React → Execute → Yield**, each with an 8-based parallelism exponent.

Important constraint: **Execute (E) and Yield (Y) are effectively constrained** when the system depends on a single-writer store (e.g., DuckDB). This keeps ingestion safe.

### OBSIDIAN (8 ports)

OBSIDIAN is the 8-port architecture and role vocabulary:

- 0 Observer: sense / observability
- 1 Bridger: connect / bus
- 2 Shaper: transform / shaping
- 3 Injector: deliver / injection
- 4 Disruptor: chaos / adversarial testing
- 5 Immunizer: validate / integrity checks
- 6 Assimilator: remember / logging + memory
- 7 Navigator: plan / orchestration

The PREY×OBSIDIAN matrix describes how phases map to ports (e.g., P uses Observer+Assimilator; R uses Bridger+Navigator).

## OBSIDIAN as an octet fractal octree

OBSIDIAN is not only “8 roles”; it is intended as an **octet fractal octree**:

- Each node in the architecture is categorized by the 8 roles (OBSIDIAN).
- Any node can recurse into 8 sub-nodes (an “octree” split), each with the same 8-role vocabulary.
- This supports scale across levels: repo → system → subsystem → module → component → function, without inventing new role names.

For the deeper framing (semantic manifold + hourglass webs + octet spawning), see:

- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/metaphysics_of_obsidian.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/metaphysics_of_obsidian.md)

## The Gen81 backbone: medallion datalake + air gap

Primary spec: [active/kiro_dev_2025/hfo-gen81-datalake/design.md](/active/kiro_dev_2025/hfo-gen81-datalake/design.md)

Gen81 introduces a **medallion datalake** with strict isolation:

- **Bronze**: `_archive/**` read-only. It is the “whole history” layer.
- **Silver**: DuckDB (hybrid search: VSS + FTS). This is the queryable memory/knowledge layer.
- **Gold**: curated exports (markdown/JSONL/parquet) suitable for feeding new AI sessions.
- **Cold**: long-lived stigmergy markers.

The hard constraint is the **air gap**:

- No writes to `_archive/**`.
- Prefer all new work under `active/kiro_dev_2025/**`.
- Avoid scanning massive mirrored folders.

## Stigmergy: leaving traces

A recurring pattern is “stigmergy as coordination.” Examples:

- “Hot” event streams (JSONL blackboards)
- “Cold” headers/markers in source
- Bronze/Silver/Gold medallion movement

## Gesture control plane (W3C pointer + adapter-first)

Key anchor: [_archive/Spatial_Input_Mobile/ObsidianBlackboard.md](/_archive/Spatial_Input_Mobile/ObsidianBlackboard.md)

The gesture system is explicitly **adopt-first**:

- Input: MediaPipe Tasks (GestureRecognizer) or Human.js
- Minimal custom logic: **FSM clutch + hysteresis + debouncing + lookahead**, behind feature flags
- Output: stable controller-like events (pinch_down/up, open, fist, etc.) suitable for game engines and UIs
- Runtimes: Phaser/PlayCanvas/Babylon/Unity/Three/VRM etc

The architectural intent is a **polymorphic hexagonal adapter** setup:

- Domain core speaks in **events + contracts**.
- Adapters translate to/from specific engines, camera pipelines, UIs, and test harnesses.
- Everything is designed to be swappable without rewriting the core.

## Tool virtualization (factory goal)

One explicit long-horizon goal is **total tool virtualization**: delivering interfaces and training overlays that let constrained environments access powerful capabilities via standards + adapters.

Two strong historical anchors:

- Purpose framing (“Semantic Knife”): [_archive/Spatial Input Mobile/tmp/backup_20250921T225726/docs/knowledge/HFO_PURPOSE_Semantic_Knife.md](/_archive/Spatial%20Input%20Mobile/tmp/backup_20250921T225726/docs/knowledge/HFO_PURPOSE_Semantic_Knife.md)
- Adopt-first tool virtualization slice (WebXR + VRM adapters, flag-gated): [_archive/Spatial Input Mobile/tmp/backup_20250921T225726/scaffolds/webway_ww-2025-081_tool_virtualization_xr_adoption.md](/_archive/Spatial%20Input%20Mobile/tmp/backup_20250921T225726/scaffolds/webway_ww-2025-081_tool_virtualization_xr_adoption.md)

## What matters most for a new AI session

- HFO uses **a consistent 8-role/8-port language** (OBSIDIAN).
- Execution is controlled by **PREY₈**, and storage constraints are first-class.
- Gen81’s medallion + air gap exists to prevent “repo ingestion explosions.”
- Gesture work is treated as a control plane with minimal glue and maximal leverage from existing precedents.

## H‑POMDP note (planning model)

When you see “H‑POMDP” in this project, interpret it as the intended **hierarchical planning under partial observability** framing:

- The system maintains beliefs under uncertainty (Observer/Assimilator).
- It selects policies and decomposes goals across levels (Navigator).
- It executes via adapters and validates aggressively (Shaper/Injector + Disruptor/Immunizer).

This is a conceptual alignment for how the swarm should behave; the concrete implementation is expressed through PREY₈ + OBSIDIAN + medallion layers.
