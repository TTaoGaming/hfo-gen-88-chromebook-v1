---
medallion_layer: silver
mutation_score_target: 0.88
hfo_scope: hive8
protocol: commander_invariants_octree
version: v1
created_utc: 2026-01-27
---

# HFO HIVE8 — Legendary Commander Invariants (Octree / Binary / Trigrams) (V1)

## Why This Exists

This is a **single invariants anchor** for HFO Alpha + Omega architecture.

If the Legendary Commanders mapping is stable, the port holonarchy is stable.

## Locked Invariants (Operator)

These are treated as **locked** (do not drift without an explicit operator correction):

- Port index: P0–P7
- Binary (3-bit octree address)
- Trigram + element
- Commander name
- Powerword (OBSIDIAN verb)
- JADC2 domain + Mosaic tile

## Holonarchy Model

- HFO uses a **fractal octree holonarchy**.
- Depth-1 has exactly 8 ports (P0–P7) addressed by 3-bit binary `000`…`111`.
- Higher-order subshards recurse the same 0–7 port scheme (octree all the way down).

## P2 SHAPE Boundary (Touch2D + W3C)

Architecture boundary statement (important):

- **Touch2D cursor frames** and **W3C PointerEvent-shaped payloads** are treated as **SHAPE-domain formats**.
- P2 owns the normalization/validation of these shapes before downstream injection.

## Canonical Machine-Readable SSOT

The canonical, test-validated mapping lives in:

- contracts/hfo_legendary_commanders_invariants.v1.json

Primary source for the **operator-corrected** port→binary→trigram order:

- hfo_hot_obsidian/silver/3_resources/reports/HFO_GRIMOIRE_8_COMMANDERS_TRIPLE_SIDED_HYPER_SLIVER_ARISTOCRATS_2026_01_22.md

Drift note:

- Some older Bronze doctrine files contain a permuted P1/P3/P4/P6 binary assignment; the JSON SSOT now uses canonical port_index→binary ordering (P0..P7 == 000..111).
