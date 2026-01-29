---
medallion_layer: silver
mutation_score: 0
hive: V
---

# HFO Gen88 v5 — Blessed DevOps Workflow (v1)

## Goal
Make local operations reproducible: preflight/postflight, blackboard signals, SSOT writes.

## Canonical tools

- P4 4-beat wrapper: [scripts/hfo_p4_basic_4beat.sh](../../../../../scripts/hfo_p4_basic_4beat.sh)
- Hub CLI: [hfo_hub.py](../../../../../hfo_hub.py)
- SSOT status updates: [hfo_ssot_status_update.py](../../../../../hfo_ssot_status_update.py)

## Memory + SSOT

- Write memory only through the SSOT tooling.
- Keep legacy JSONL ledgers read-only.
