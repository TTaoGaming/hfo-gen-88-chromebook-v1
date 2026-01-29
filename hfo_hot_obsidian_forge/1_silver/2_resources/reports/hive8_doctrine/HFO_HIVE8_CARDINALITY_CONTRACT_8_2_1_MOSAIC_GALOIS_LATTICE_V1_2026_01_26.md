---
medallion_layer: silver
mutation_score_target: 0.88
hfo_scope: hive8
protocol: cardinality_contract_8_2_1
version: v1
created_utc: 2026-01-26
---

# HFO HIVE8 — Cardinality Contract (8 / 2 / 1) for Mosaic Warfare Galois Lattice (V1)

## Why This Exists

We enforce a strict per-port cardinality so the system’s outputs remain composable under lattice-style reasoning.

This is treated as **mathematically important** for the Mosaic Warfare Galois lattice: predictable arity enables reliable joins/meets across ports.

## Contract

For every port artifact:

- **Artifact cardinality:** $8^1 = 8$
  - Each port artifact MUST contain exactly 8 bullet items inside the `HIVE8_CARD_8_ITEMS` marker region.

- **Meta-promoted cardinality (depends on port class):**
  - **Scatter ports (0–3):** $2^1 = 2$ promoted items
  - **Gather ports (4–7):** $8^0 = 1$ promoted item

## Marker Interface (Required)

Each port artifact MUST contain these regions:

- `<!-- HIVE8_CARD_8_ITEMS_START -->` … `<!-- HIVE8_CARD_8_ITEMS_END -->`
  - exactly 8 non-empty `-` bullet lines

- `<!-- HIVE8_META_PROMOTED_START -->` … `<!-- HIVE8_META_PROMOTED_END -->`
  - exactly 2 (scatter) or 1 (gather) non-empty `-` bullet lines

## Enforcement

- Generator: injects per-port mode and expected counts into the artifact templates.
- Finalizer: counts bullets and emits PASS/FAIL in meta synthesis.

## Escalation Rule

- If any port fails cardinality validation, treat the turn as **non-final** until corrected.

## Notes

- This document intentionally does not over-specify semantics (content meaning). It only specifies arity + extraction mechanics.
