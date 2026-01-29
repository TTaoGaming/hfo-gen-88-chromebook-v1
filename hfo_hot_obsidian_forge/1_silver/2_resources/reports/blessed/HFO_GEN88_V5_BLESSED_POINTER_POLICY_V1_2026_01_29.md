---
medallion_layer: silver
mutation_score: 0
hive: V
---

# HFO Gen88 v5 — Blessed Pointer Policy (v1)

## Objective
Make large refactors a **single-touch operation**: change pointers, not code paths.

## Two registries (both at repo root)

- Working: [hfo_pointers.json](../../../../../hfo_pointers.json)
- Blessed: [hfo_pointers_blessed.json](../../../../../hfo_pointers_blessed.json)

## Resolver behavior

- `hfo_pointers.py` prefers `hfo_pointers_blessed.json` when present.
- Override selection with `HFO_POINTERS_FILE`.

## Rules of engagement

- When moving a root (e.g. Omega Gen7, blackboards, SSOT DB): update pointers first.
- Any script that needs a deep path should call `hfo_pointers.py` (Python) or shell out to it.
- Treat the blessed registry as stable; only bless changes after they’ve survived GitOps + normal ops.
