---
medallion_layer: bronze
mutation_score: 0
hive: V
ts_utc: 2026_01_29T232549Z
---

# Hot Obsidian → Hot Obsidian Forge Migration Health (Projected)

This report includes two proofs:
- Index baseline (what git currently considers tracked in the index)
- Projected tracked set after applying rename/delete deltas from git status

## Hot Obsidian (overall) — Index Baseline

- Legacy hot obsidian tracked files (index): **1776**
- Forge hot obsidian tracked files (index): **355**
- Forge share (index): **16.66%**

## Hot Obsidian (overall) — Projected (worktree-renames applied)

- Legacy hot obsidian tracked files (projected): **1565**
- Forge hot obsidian tracked files (projected): **353**
- Forge share (projected): **18.40%**

## Hot Bronze — Index Baseline

- Legacy hot bronze tracked files (index): **1760**
- Forge hot bronze tracked files (index): **145**
- Forge share (index): **7.61%**

## Hot Bronze — Projected (worktree-renames applied)

- Legacy hot bronze tracked files (projected): **1549**
- Forge hot bronze tracked files (projected): **145**
- Forge share (projected): **8.56%**

## Remaining Legacy Hot Obsidian Buckets (top 20, projected)

- 1126: hfo_hot_obsidian/bronze/4_archive
- 332: hfo_hot_obsidian/bronze/3_resources
- 91: hfo_hot_obsidian/bronze/1_projects
- 5: hfo_hot_obsidian/silver/3_resources
- 5: hfo_hot_obsidian/silver/2_areas
- 3: hfo_hot_obsidian/gold/3_resources
- 1: hfo_hot_obsidian/hot_obsidian_blackboard.jsonl.receipt.json
- 1: hfo_hot_obsidian/blackboard_manifest.json
- 1: hfo_hot_obsidian/silver/1_projects

## Remaining Legacy Hot Bronze Buckets (top 20, projected)

- 602: hfo_hot_obsidian/bronze/4_archive/hot_obsidian_root_4_archive
- 512: hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18
- 114: hfo_hot_obsidian/bronze/3_resources/reports
- 96: hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18
- 85: hfo_hot_obsidian/bronze/3_resources/para
- 43: hfo_hot_obsidian/bronze/1_projects/omega_gen5_current
- 17: hfo_hot_obsidian/bronze/3_resources/logs
- 14: hfo_hot_obsidian/bronze/1_projects/forensics_ttao_tooling_forensics_v1_2025_01_to_2026_01
- 14: hfo_hot_obsidian/bronze/1_projects/forensics_ttao_dev_work_monthly_deep_dive_v1_2025_01_to_2026_01
- 6: hfo_hot_obsidian/bronze/4_archive/serena_memories
- 6: hfo_hot_obsidian/bronze/3_resources/.serena
- 4: hfo_hot_obsidian/bronze/1_projects/_inbox
- 4: hfo_hot_obsidian/bronze/1_projects/hfo_omega_assimillation_touchscreen_targets
- 4: hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub
- 4: hfo_hot_obsidian/bronze/3_resources/fixtures
- 3: hfo_hot_obsidian/bronze/3_resources/receipts
- 3: hfo_hot_obsidian/bronze/1_projects/alpha_gen1_current
- 2: hfo_hot_obsidian/bronze/1_projects/omega_gen4_current
- 2: hfo_hot_obsidian/bronze/1_projects/forensics
- 2: hfo_hot_obsidian/bronze/3_resources/.serena_managed

## Notes

- All counts are from git tracked paths only (git ls-files + status deltas).
- Untracked files are excluded intentionally.
