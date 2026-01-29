---
medallion_layer: silver
mutation_score: 0
hive: V
---

# HFO Gen88 v5 — Blessed GitOps Workflow (v1)

## Goal
Commit and push safely in **small batches**, without brittle gates blocking doc/migration work.

## Canonical entrypoints

- GitOps driver: [scripts/hfo_gitops_auto.sh](../../../../../scripts/hfo_gitops_auto.sh)
- Pre-commit gate: [scripts/hfo_precommit_gate.sh](../../../../../scripts/hfo_precommit_gate.sh)

## Batch discipline

- Prefer the batcher/auto script over manual `git add -A`.
- If a gate needs a runtime asset, gate should be **applicable-only** (skip when asset absent; fail-closed when present).

## Pointer alignment

- When GitOps needs paths (blackboard, runtime pages, SSOT DB), resolve them through `hfo_pointers.py` rather than hardcoding.
