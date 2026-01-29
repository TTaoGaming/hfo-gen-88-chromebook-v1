---
medallion_layer: bronze
mutation_score: 0
hive: V
---

# Hot Bronze Consolidation Index (Gen88 v5)

Hot Bronze is for *active disruption + operational steering*. Keep the “hot surface area” small.

## The small set of canonical anchors

1) Agent entrypoint + governance
- Root context: [AGENTS.md](../../../../../AGENTS.md)
- Copilot governance: [.github/copilot-instructions.md](../../../../../.github/copilot-instructions.md)
- P4 agent mode: [.github/agents/hfo-basic-p4.agent.md](../../../../../.github/agents/hfo-basic-p4.agent.md)

2) Pointers (path truth)
- Pointer registry (working): [hfo_pointers.json](../../../../../hfo_pointers.json)
- Pointer registry (blessed): [hfo_pointers_blessed.json](../../../../../hfo_pointers_blessed.json)
- Pointer helper: [hfo_pointers.py](../../../../../hfo_pointers.py)

3) Hub roots
- MCP gateway hub shim (stable): [hfo_mcp_gateway_hub.py](../../../../../hfo_mcp_gateway_hub.py)
- Hub CLI: [hfo_hub.py](../../../../../hfo_hub.py)

4) Omega Gen7 (current execution project)
- Omega project root: [hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified](hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified)
- Omega spec (microkernel): [hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/specs/omega_gen7_v1_1_spec.yaml](hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/specs/omega_gen7_v1_1_spec.yaml)

5) Compendium (doctrine anchors)
- v8.6 compendium: [hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_6_2026_01_29.md](hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_6_2026_01_29.md)
- v8.7 compendium: [hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_7_2026_01_29.md](hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_7_2026_01_29.md)

## Archiving rule (simple)

- If a file is not one of the anchors above, it should live in forge under Bronze/Silver PARA.
- Prefer moving legacy material to:
  - `hfo_hot_obsidian_forge/0_bronze/2_resources/reports/legacy_hot_obsidian_bronze/`
  - `hfo_hot_obsidian_forge/1_silver/2_resources/reports/legacy_hot_obsidian_silver/`
- Put stale root docs and one-off guides under:
  - `hfo_hot_obsidian_forge/0_bronze/3_archive/root_docs/`

## Operational habit

- Use the P4 wrapper for any real work: `bash scripts/hfo_p4_basic_4beat.sh ...`
- Finish turns with an SSOT status update: `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_ssot_status_update.py --topic ...`
