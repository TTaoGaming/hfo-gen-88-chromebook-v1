# Medallion: Bronze | Mutation: 0% | HIVE: V

# TTao Dev Work — Monthly Deep Dive v1: 2025-12

## Provenance
- Generated (UTC): 2026-01-22T02:04:06.918205Z
- DuckDB: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
- Window (modified_at): 2025-12-01T00:00:00 .. 2026-01-01T00:00:00 (start inclusive, end exclusive)

## Scope notes (first pass)
- This report is purely based on `file_system.modified_at` (file index).
- It does not assume older forks are ‘your work’; it only reports what files appear in the index for this month window.

## Summary
- Indexed file records this month: 26075
- Earliest modified_at in month: 2025-12-01 00:18:54.082167
- Latest modified_at in month: 2025-12-31 23:01:42

## Keyword path hits (counts)
- hopeos: 0
- alpha: 529
- omega: 17
- tectangle: 2
- drumpad: 0
- tags: 14

## Top eras (by count)
| era | n |
|---|---|
| UNCATEGORIZED | 20511 |
| COLD_BRONZE_2025 | 5418 |
|  | 82 |
| TAGS_DRUMPADS | 28 |
| COMPUTER_VISION_EARLY | 20 |
| HFO_BOOTSTRAP | 14 |
| TECTANGLE_ERA | 2 |

## Top projects (by count)
| project | n |
|---|---|
| _archive_dev_2026_1_14 | 25993 |
|  | 82 |

## Top buckets (by count; coarse path prefix)
| bucket | n |
|---|---|
| home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome | 18974 |
| home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3 | 3160 |
| home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY | 1709 |
| home/tommytai3/_archive_dev_2026_1_14/miniconda3 | 1042 |
| home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11 | 777 |
| home/tommytai3/_archive_dev_2026_1_14/active_hfn_gen_85_to_gen_87_x3 | 371 |
| home/tommytai3/_archive_dev_2026_1_14/_HFO_ARCHIVE | 22 |
| home/tommytai3/_archive_dev_2026_1_14/hfo_gen88 | 8 |
| home/tommytai3/_archive_dev_2026_1_14/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52 | 7 |
| home/tommytai3/_archive_dev_2026_1_14/ARCHIVE_MANIFEST_2025_12_28.md | 1 |
| home/tommytai3/_archive_dev_2026_1_14/verify_cqrs_architecture.py | 1 |
| home/tommytai3/_archive_dev_2026_1_14/SANDBOX_OPTIONS.md | 1 |

## Hotspots (path substring counts)
| substring | n |
|---|---|
| .venv | 17254 |
| __pycache__ | 3698 |
| tests/ | 1392 |
| vendor/ | 894 |
| build/ | 648 |
| dist/ | 394 |
| test-results | 182 |
| scripts/ | 100 |
| coverage/ | 87 |
| contracts/ | 11 |

## Patterns (heuristic)
- High concentration in one bucket (home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome) ≈ 73% of indexed records.
- Both omega and alpha keywords appear this month (cross-thread work visible in path-level signals).

## Anti-patterns / risks (heuristic)
- Concentration can indicate coupling/hotspot risk; consider splitting responsibilities or adding gates.
- Presence of __pycache__ suggests derived Python artifacts; consider excluding from tracked changes.
- test-results appearing in changes can be noisy; consider keeping only curated receipts/reports.

## Top extensions (by count)
| ext | n |
|---|---|
| py | 12666 |
| pyc | 3698 |
| md | 2549 |
|  | 2460 |
| png | 577 |
| pyi | 500 |
| json | 448 |
| map | 389 |
| manifest | 329 |
| txn | 329 |
| lance | 328 |
| txt | 279 |

## Keyword samples (newest paths)
### hopeos
(none)

### alpha
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/active_hfn_gen_85_to_gen_87_x3/hfo_gen87_x3/hfo_daily_specs/HARD_GATED_SWARM_SCATTER_GATHER_20251230.md
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/hot_bronze/specs/HARD_GATED_SWARM_SCATTER_GATHER_20251230.md
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/hot_bronze/src/crewai_agents/run_swarm.py
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/hot_bronze/src/mcp/lidless-legion/package.json
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/hot_bronze/src/mcp/lidless-legion/README.md
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/hot_bronze/src/mcp/lidless-legion/tsconfig.json
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-9qLthi/cold/bronze/archive_2025-12-31/hot_bronze/specs/HARD_GATED_SWARM_SCATTER_GATHER_20251230.md
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-9qLthi/cold/bronze/archive_2025-12-31/hot_bronze/src/crewai_agents/run_swarm.py
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-9qLthi/cold/bronze/archive_2025-12-31/hot_bronze/src/mcp/lidless-legion/package.json
- 2025-12-31 00:31:04 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-9qLthi/cold/bronze/archive_2025-12-31/hot_bronze/src/mcp/lidless-legion/README.md

### omega
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-9qLthi/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-BeeZUy/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-D8wHjh/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-fY6fnl/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-ikPEvO/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-IojNW6/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-j2F8fZ/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-LIuUOM/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md
- 2025-12-31 17:32:12 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-SArQAt/cold/bronze/archive_2025-12-31/cold_bronze_content/legacy-demos/sandbox-demos/hfo-golden-mediapipe/README.md

### tectangle
- 2025-12-03 15:01:41.185719 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_64/archive/dream_slop/archive/analyze_tectangle.py
- 2025-12-03 15:01:41.185719 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_64/archive/dream_slop/archive/grimoire_cards/tectangle_core.md

### drumpad
(none)

### tags
- 2025-12-29 15:10:35.690698 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/.venv/lib/python3.11/site-packages/prefect/server/database/_migrations/versions/sqlite/__pycache__/2025_06_12_144500_add_automation_tags_bb2345678901.cpython-311.pyc
- 2025-12-29 15:10:02.740697 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/.venv/lib/python3.11/site-packages/prefect/server/database/_migrations/versions/sqlite/2025_06_12_144500_add_automation_tags_bb2345678901.py
- 2025-12-29 15:10:02.689696 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/.venv/lib/python3.11/site-packages/prefect/server/database/_migrations/versions/postgresql/2025_06_12_144500_add_automation_tags_aa1234567890.py
- 2025-12-29 14:48:23.364630 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/.venv/lib/python3.11/site-packages/packaging/__pycache__/tags.cpython-311.pyc
- 2025-12-29 14:48:07.174629 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/.venv/lib/python3.11/site-packages/packaging/tags.py
- 2025-12-29 00:55:44.536842 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/portable_hfo_memory_pre_hfo_to_gen84/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52/venv/lib/python3.11/site-packages/pip/_vendor/packaging/__pycache__/tags.cpython-311.pyc
- 2025-12-29 00:55:44.212842 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/portable_hfo_memory_pre_hfo_to_gen84/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52/venv/lib/python3.11/site-packages/pip/_internal/utils/__pycache__/compatibility_tags.cpython-311.pyc
- 2025-12-29 00:55:43.854842 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/portable_hfo_memory_pre_hfo_to_gen84/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52/venv/lib/python3.11/site-packages/pip/_vendor/packaging/tags.py
- 2025-12-29 00:55:43.823842 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/portable_hfo_memory_pre_hfo_to_gen84/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52/venv/lib/python3.11/site-packages/pip/_internal/utils/compatibility_tags.py
- 2025-12-29 00:55:43.605842 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/portable_hfo_memory_pre_hfo_to_gen84/portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52/venv/lib/python3.11/site-packages/setuptools/_vendor/packaging/__pycache__/tags.cpython-311.pyc

## Newest paths (top 25)
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-9qLthi/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-BeeZUy/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-D8wHjh/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-fY6fnl/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-ikPEvO/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-IojNW6/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-j2F8fZ/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-LIuUOM/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-SArQAt/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 23:01:42 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-ZWz5hN/cold/bronze/archive_2025-12-31/hot_bronze/W3C_GESTURE_CONTROL_PLANE_AUDIT_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-9qLthi/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-BeeZUy/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-D8wHjh/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-fY6fnl/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-ikPEvO/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-IojNW6/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-j2F8fZ/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-LIuUOM/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-SArQAt/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:59:58 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-ZWz5hN/cold/bronze/archive_2025-12-31/hot_silver/INTERLOCK_W3C_GESTURE_COMPLETE_20251231.md
- 2025-12-31 22:46:18 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-6N23Ug/cold/bronze/archive_2025-12-31/root_sprawl/reports/mutation/mutation-report.json
- 2025-12-31 22:46:18 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-9qLthi/cold/bronze/archive_2025-12-31/root_sprawl/reports/mutation/mutation-report.json
- 2025-12-31 22:46:18 | score=0 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/.stryker-tmp/sandbox-BeeZUy/cold/bronze/archive_2025-12-31/root_sprawl/reports/mutation/mutation-report.json

## Highest-score paths (top 25)
- score=26 | 2025-12-29 16:49:46 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/active_hfn_gen_85_to_gen_87_x3/GEN87_X1_GOLD_BATON_QUINE.md
- score=26 | 2025-12-29 16:49:46 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/active_hfn_gen_85_to_gen_87_x3/hfo_gen87_experimental_x1/context_payload/GEN87_X1_GOLD_BATON_QUINE.md
- score=26 | 2025-12-29 16:49:46 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/active_hfn_gen_85_to_gen_87_x3/hfo_gen87_experimental_x1_stem/context_payload/GEN87_X1_GOLD_BATON_QUINE.md
- score=26 | 2025-12-29 16:49:46 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/active_hfn_gen_85_to_gen_87_x3/hfo_gen87_experimental_x2_vscode/context_payload/GEN87_X1_GOLD_BATON_QUINE.md
- score=26 | 2025-12-29 16:22:44 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/active_hfn_gen_85_to_gen_87_x3/FORENSIC_ANALYSIS_AI_FAILURES_2025.md
- score=26 | 2025-12-28 23:28:03.108573 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/gen_82_grimoire/fractal_obsidian_grimoire_gen_82/legendary_quine_manifests.md
- score=26 | 2025-12-28 23:28:02.163573 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/gen_84/gen_84_2025_12_25/GEN84.3_ENRICHED_GOLD_BATON_QUINE.md
- score=26 | 2025-12-28 23:28:02.127573 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/gen_84/gen_84_2025_12_25/GEN84.4_ENRICHED_GOLD_BATON_QUINE.md
- score=26 | 2025-12-28 23:28:02.104573 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/gen_84/gen_84_2025_12_25/GEN84.2_ENRICHED_GOLD_BATON_QUINE.md
- score=26 | 2025-12-28 23:28:02.067573 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/gen_83_baton/hfo_gen_83_baton/GEN83_ENRICHED_GOLD_BATON_QUINE.md
- score=26 | 2025-12-28 23:28:02.050573 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome/archives/gen_83_baton/hfo_gen_83_baton/GEN83.2_ENRICHED_GOLD_BATON_QUINE.md
- score=26 | 2025-12-08 14:23:43.757124 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/buds/hfo_gem_gen_71/brain/HFO_GRIMOIRE_MANIFEST.md
- score=26 | 2025-12-08 14:23:43.756124 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/buds/hfo_gem_gen_71/brain/card_00_obsidian_matrix_quine.md
- score=26 | 2025-12-06 15:49:52.873751 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/buds/hfo_gem_gen_70/brain/grimoire/HFO_GRIMOIRE_MANIFEST.md
- score=26 | 2025-12-06 15:49:52.872751 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/buds/hfo_gem_gen_70/brain/grimoire/card_00_obsidian_matrix_quine.md
- score=26 | 2025-12-06 15:21:54.252666 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/buds/hfo_gem_gen_69/brain/grimoire/card_00_obsidian_matrix_quine.md
- score=26 | 2025-12-05 23:23:30.055277 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/buds/hfo_gem_gen_69/brain/grimoire/HFO_GRIMOIRE_MANIFEST.md
- score=26 | 2025-12-05 22:22:28.320090 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/buds/hfo_gem_gen_68/brain/grimoire/HFO_GRIMOIRE_MANIFEST.md
- score=26 | 2025-12-05 21:25:24.550915 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/buds/hfo_gem_gen_68/brain/grimoire/card_00_obsidian_matrix_quine.md
- score=26 | 2025-12-04 18:18:24.647593 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11/hfo_lancedb/hindsight_memory.lance/data/000101101110100010101110334dc14f6588e62f228d1400a6.lance
- score=26 | 2025-12-03 14:49:57.308684 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_64/archive/dream_slop/archive/EVOLUTION_STIGMERGY.md
- score=26 | 2025-12-03 14:49:33.007682 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_64/archive/dream_slop/archive/EVOLUTION_SWARMLORD.md
- score=26 | 2025-12-03 10:26:27.808875 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63_1/grimoire/cards/navigator_swarmlord_of_webs.md
- score=26 | 2025-12-03 03:33:19 | / | /home/tommytai3/_archive_dev_2026_1_14/_HFO_ARCHIVE/Legacy_Snapshots/hfo-archives-2025-12-03/hfo_gem_gen_63_1/grimoire/cards/navigator_swarmlord_of_webs.md
- score=26 | 2025-12-03 01:19:02.587196 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/07_navigator_brain/ai-chat-hfo-archetecture-rpg-2025-12-02.md
