# HFO Dimensional Matrix (Gen81)

This is the compact “coordinate system” for reasoning about HFO.

## Why a matrix

HFO spans multiple orthogonal dimensions:

- **What phase** of work is happening (PREY)
- **Which port/role** is responsible (OBSIDIAN)
- **Which data layer** is being read/written (Medallion)
- **Which domain** is being served (Infra vs Gesture)

Using the matrix avoids mixing concerns and helps keep changes reversible.

## Dimension A: PREY (execution phase)

- **P**erceive: gather observations (read-only, probe)
- **R**eact: route/connect/plan
- **E**xecute: do work (often constrained)
- **Y**ield: commit results (often constrained)

Dial: PREY₈ (parallelism per phase). Gen80 defines the notation.

## Dimension A2: Decision model (H‑POMDP framing)

Use “H‑POMDP” as the mental model for **hierarchical decision-making under uncertainty**:

- Belief/state estimation lives in **Observer + Assimilator**.
- Policy selection and decomposition lives in **Navigator**.
- Actions are executed through **Shaper + Injector** (adapters).
- Robustness is enforced through **Disruptor + Immunizer** (chaos + guards).

This keeps planning compatible with partial observability (no single agent has full truth).

## Dimension B: OBSIDIAN (8 ports / responsibilities)

- **0 Observer**: sensing, observability, telemetry
- **1 Bridger**: messaging/bus/connection
- **2 Shaper**: transforms, shaping, compilation
- **3 Injector**: delivery, side effects, integration
- **4 Disruptor**: chaos, adversarial testing
- **5 Immunizer**: validation, schema, guards
- **6 Assimilator**: logging, memory persistence
- **7 Navigator**: orchestration, planning

Note: a closely related crosswalk exists in the Obsidian Matrix (Greek ↔ Bagua/I‑Ching ↔ JADC2 verbs):

- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_matrix.md)

## Dimension C: Medallion layer (data + memory)

- **Bronze**: `_archive/**` immutable history (read-only)
- **Silver**: DuckDB searchable memory (VSS+FTS), single-writer safety matters
- **Gold**: curated exports for consumption (AI context packs, docs)
- **Cold**: durable markers / stigmergy

## Dimension D: Domain plane (what we’re building)

- **Infra plane (HFO)**: orchestration, testing harness, memory MCP, stigmergy
- **Control plane (Gesture/W3C)**: camera → recognizer → controller events → runtimes

## Dimension E: Mission engineering / “mosaic tiles”

Treat each adapter, tool, and test harness module as a **tile** that can be recomposed for a mission.

- OBSIDIAN gives a stable role vocabulary.
- Hexagonal adapters keep tiles swappable.
- Medallion layers keep memory/query stable across generations.

## The working matrix (practical)

Use this table as a mental routing rule for tasks.

| If you are doing… | PREY phase | OBSIDIAN port(s) | Medallion layer | Domain plane |
|---|---|---|---|---|
| “Find precedent / understand history” | P | 0 + 6 | Bronze | Infra + Gesture |
| “Plan a change / choose adapters” | R | 1 + 7 | Bronze + Silver | Infra + Gesture |
| “Implement a small adapter” | E | 2 + 3 | Silver + Gold | Gesture or Infra |
| “Add a guard/test or validate” | Y | 4 + 5 → 6 → 7 | Silver + Gold | Infra |

## Default safety constraints

- Writes belong in `active/kiro_dev_2025/**`.
- Treat `_archive/**` as non-writable bronze.
- Avoid repo-wide scans; do surgical reads via linked sources.
