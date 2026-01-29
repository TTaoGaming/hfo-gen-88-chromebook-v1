---
medallion_layer: silver
mutation_score: 0
hive: V
---

# HFO Gen88 v5 — Blessed Systems Index (v1)

Goal: reduce “multi-touch surface” edits by routing operational paths and workflows through a small set of **blessed roots**, primarily via the **blessed pointer registry**.

## Pointer registries (root)

- Working pointers (editable): [hfo_pointers.json](../../../../../hfo_pointers.json)
- Blessed pointers (stable / preferred by resolver): [hfo_pointers_blessed.json](../../../../../hfo_pointers_blessed.json)

Policy:
- Change locations by updating pointers first.
- Scripts/entrypoints should resolve paths via `hfo_pointers.py` rather than hardcoding deep paths.

Related:
- Pointer policy: [hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_POINTER_POLICY_V1_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_POINTER_POLICY_V1_2026_01_29.md)

## Forge consolidation (first-class)

Canonical roots:

- Hot forge: [hfo_hot_obsidian_forge/](../../../../../hfo_hot_obsidian_forge/)
- Cold forge: [hfo_cold_obsidian_forge/](../../../../../hfo_cold_obsidian_forge/)

Legacy roots are compatibility-only drains:

- `hfo_hot_obsidian/`
- `hfo_cold_obsidian/`

Operational visibility:

- Migration audit (what still references legacy roots): [hfo_hot_obsidian_forge/0_bronze/2_resources/reports/migration/HFO_FORGE_MIGRATION_AUDIT_V1_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/0_bronze/2_resources/reports/migration/HFO_FORGE_MIGRATION_AUDIT_V1_2026_01_29.md)

## Blessed operator entrypoints

- Root agent context (anchors-only): [AGENTS.md](../../../../../AGENTS.md)
- Copilot governance: [.github/copilot-instructions.md](../../../../../.github/copilot-instructions.md)
- P4 basic agent mode: [.github/agents/hfo-basic-p4.agent.md](../../../../../.github/agents/hfo-basic-p4.agent.md)

## Blessed hub roots

- Hub shim entrypoint: [hfo_mcp_gateway_hub.py](../../../../../hfo_mcp_gateway_hub.py)
- Hub CLI: [hfo_hub.py](../../../../../hfo_hub.py)

## Blessed blackboards (pointer-resolved)

- Hot forge blackboard (canonical): [hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard_v5.jsonl](../../../../../hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard_v5.jsonl)
- Cold forge blackboard (canonical): [hfo_cold_obsidian_forge/0_bronze/2_resources/blackboards/cold_obsidian_blackboard_v1.jsonl](../../../../../hfo_cold_obsidian_forge/0_bronze/2_resources/blackboards/cold_obsidian_blackboard_v1.jsonl)

## Blessed GitOps workflow

- GitOps auto entrypoint: [scripts/hfo_gitops_auto.sh](../../../../../scripts/hfo_gitops_auto.sh)
- GitOps pre-commit gate (fail-closed): [scripts/hfo_precommit_gate.sh](../../../../../scripts/hfo_precommit_gate.sh)

Related:
- GitOps workflow: [hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_GITOPS_WORKFLOW_V1_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_GITOPS_WORKFLOW_V1_2026_01_29.md)

## Blessed DevOps workflow (local)

- P4 4-beat wrapper: [scripts/hfo_p4_basic_4beat.sh](../../../../../scripts/hfo_p4_basic_4beat.sh)
- Flight tools (preflight/postflight): [scripts/hfo_flight_preflight.sh](../../../../../scripts/hfo_flight_preflight.sh)

Related:
- DevOps workflow: [hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_DEVOPS_WORKFLOW_V1_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_DEVOPS_WORKFLOW_V1_2026_01_29.md)

## Blessed engineering workflows

- Contract-driven development (CDD): Zod contracts under [contracts/](../../../../../contracts/)
- Test-driven development (TDD): tests under [tests/](../../../../../tests/)
- Behavior-driven development (BDD): reserve for feature-level workflows (when introduced)

Related:
- Testing workflows: [hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_TESTING_WORKFLOWS_CDD_TDD_BDD_V1_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_TESTING_WORKFLOWS_CDD_TDD_BDD_V1_2026_01_29.md)

## Blessed doctrine anchors

- Hive8 Compendium v8.6: [hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_6_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_6_2026_01_29.md)
- Hive8 Compendium v8.7: [hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_7_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_7_2026_01_29.md)

Related:
- Compendium pointers: [hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_COMPENDIUM_POINTERS_V1_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_COMPENDIUM_POINTERS_V1_2026_01_29.md)

## Blessed grimoire (placeholder)

- Consolidate verified “how-to” operational recipes under this folder (Silver) over time.

Related:
- Blessed grimoire: [hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_GRIMOIRE_V1_2026_01_29.md](../../../../../hfo_hot_obsidian_forge/1_silver/2_resources/reports/blessed/HFO_GEN88_V5_BLESSED_GRIMOIRE_V1_2026_01_29.md)
