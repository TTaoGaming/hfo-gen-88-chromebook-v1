---
medallion_layer: silver
mutation_score_target: 0.88
hfo_scope: hive8
protocol: scatter_gather_double_diamond_pdca
version: v1
created_utc: 2026-01-26
---

# HFO HIVE8 — Scatter/Gather Double Diamond + PDCA Strange Loop (V1)

## Intent

Formalize HIVE8 as a fractal **scatter/gather** system (diverge/converge) that:

- Uses powers of two (1, 2, 4, 8, …)
- Implements a **double diamond** rhythm (scatter → gather → scatter → gather)
- Maps to **PDCA** as an iterative strange loop

This protocol exists to keep the envelope mathematically consistent for Mosaic Warfare / lattice reasoning.

## Port Partition (Scatter vs Gather)

- **Scatter ports (0–3):** P0, P1, P2, P3
- **Gather ports (4–7):** P4, P5, P6, P7

Operational meaning:

- **Scatter (0–3):** generate option mass / hypothesis mass / candidate surfaces.
- **Gather (4–7):** compress / validate / bind / navigate into commitments and handoffs.

## HIVE8 as a Double Diamond (Fractal)

HIVE8 is a “double diamond” at multiple scales:

- Micro: each port’s work diverges then converges.
- Meso: the lattice pairing order yields repeated scatter+gather adjacency.
- Macro: each full turn produces a divergent set (8 artifacts) and a convergent meta synthesis.

Recommended reading order (existing lattice order):

- (P0+P7) → (P1+P6) → (P2+P5) → (P3+P4)

## PDCA Mapping (Strange Loop)

Interpretation (practical):

- **Plan:** Scatter ports (0–3) generate candidate plans/frames.
- **Do:** Execute/bridge within the lattice (pairing cadence).
- **Check:** Gather ports (4–7) validate, audit, memory-bind.
- **Act:** Meta synthesis and next-step commitments reshape the next turn (loop closure).

This is intentionally *iterative* and *self-correcting*.

## Enforced Cardinality Contract

All ports MUST satisfy:

- **Artifact items:** $8^1 = 8$ (each port publishes exactly 8 items into its artifact)
- **Meta-promoted items:**
  - Scatter ports (0–3): $2^1 = 2$ items promoted into meta
  - Gather ports (4–7): $8^0 = 1$ item promoted into meta

These rules are enforced via explicit markers in the per-port templates and checked during finalization.

## Proof / Compliance

- Templates MUST contain marker regions for:
  - `HIVE8_CARD_8_ITEMS_START/END`
  - `HIVE8_META_PROMOTED_START/END`
- Finalizer MUST:
  - validate bullet counts (8 and 2-or-1)
  - inject explicit scatter/gather labels into meta synthesis

## Notes

- If you want stricter semantics, we can additionally enforce “powers-of-two only” inside each bullet label or ID (e.g. require item IDs `1,2,4,8` in the first four, etc.).
