# Medallion: Bronze | Mutation: 0% | HIVE: V

# TTao Dev Work — Monthly Deep Dive v1: 2026-01

## Provenance
- Generated (UTC): 2026-01-22T02:04:51.692604Z
- DuckDB: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
- Window (modified_at): 2026-01-01T00:00:00 .. 2026-02-01T00:00:00 (start inclusive, end exclusive)

## Scope notes (first pass)
- This report is purely based on `file_system.modified_at` (file index).
- It does not assume older forks are ‘your work’; it only reports what files appear in the index for this month window.

## Summary
- Indexed file records this month: 62528
- Earliest modified_at in month: 2026-01-01 00:21:52
- Latest modified_at in month: 2026-01-15 15:26:38.676408

## Keyword path hits (counts)
- hopeos: 0
- alpha: 1036
- omega: 5172
- tectangle: 0
- drumpad: 0
- tags: 60

## Top eras (by count)
| era | n |
|---|---|
| GEN88_ACTIVE | 34387 |
| UNCATEGORIZED | 20815 |
| COLD_BRONZE_2025 | 5217 |
| TAGS_DRUMPADS | 1959 |
|  | 129 |
| COMPUTER_VISION_EARLY | 21 |

## Top projects (by count)
| project | n |
|---|---|
| active | 34515 |
| _archive_dev_2026_1_14 | 27884 |
|  | 129 |

## Top buckets (by count; coarse path prefix)
| bucket | n |
|---|---|
| home/tommytai3/active/hfo_gen_88_chromebook_v_1 | 33195 |
| home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3 | 26670 |
| home/tommytai3/active/.venv | 1327 |
| home/tommytai3/_archive_dev_2026_1_14/hfo_gen88 | 1218 |
| home/tommytai3/_archive_dev_2026_1_14/archive_mission_thread_omega_gen_4_v24_poc_working_2026_1_14 | 61 |
| home/tommytai3/_archive_dev_2026_1_14/miniconda3 | 24 |
| home/tommytai3/_archive_dev_2026_1_14/ttao-mobile-obsidian-2026-01-09-20260109T214348Z-3-001 | 23 |
| home/tommytai3/_archive_dev_2026_1_14/gen88_bronze | 6 |
| home/tommytai3/_archive_dev_2026_1_14/hfo_gen_87_chrome | 2 |
| home/tommytai3/_archive_dev_2026_1_14/omega_gen4_v25_spec.yaml | 1 |
| home/tommytai3/_archive_dev_2026_1_14/omega_gen4_v24_23.html | 1 |

## Hotspots (path substring counts)
| substring | n |
|---|---|
| .venv | 49782 |
| __pycache__ | 18661 |
| tests/ | 12433 |
| vendor/ | 6792 |
| test-results | 755 |
| scripts/ | 581 |
| build/ | 522 |
| contracts/ | 520 |
| hfo_hot_obsidian/bronze/4_archive | 462 |
| dist/ | 401 |
| coverage/ | 274 |
| hfo_hot_obsidian/bronze/3_resources | 179 |
| hfo_hot_obsidian/bronze/1_projects | 155 |
| hfo_hot_obsidian/silver | 11 |

## Patterns (heuristic)
- High concentration in one bucket (home/tommytai3/active/hfo_gen_88_chromebook_v_1) ≈ 53% of indexed records.
- Both omega and alpha keywords appear this month (cross-thread work visible in path-level signals).

## Anti-patterns / risks (heuristic)
- Concentration can indicate coupling/hotspot risk; consider splitting responsibilities or adding gates.
- Presence of .venv paths suggests environment artifacts are being indexed; consider excluding .venv from change signals.
- Presence of __pycache__ suggests derived Python artifacts; consider excluding from tracked changes.
- test-results appearing in changes can be noisy; consider keeping only curated receipts/reports.
- High .pyc volume suggests derived artifacts are dominating the change signal; consider filtering compiled outputs.

## Top extensions (by count)
| ext | n |
|---|---|
| py | 19212 |
| pyc | 18661 |
|  | 4276 |
| ts | 3953 |
| pyi | 2655 |
| md | 2091 |
| h | 1470 |
| html | 1249 |
| json | 1226 |
| js | 1218 |
| png | 551 |
| f90 | 540 |

## Keyword samples (newest paths)
### hopeos
(none)

### alpha
- 2026-01-15 12:09:38.262168 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_duckdb_mcp.py
- 2026-01-14 10:40:47.190765 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.playwright-mcp/omega_v23_1_navigator.png
- 2026-01-14 10:10:42.164672 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.playwright-mcp/gen4_v23_1_visual_fix_audit.png
- 2026-01-14 10:08:48.658667 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/hfo_refactor_mission_thread_alpha_20260114/README.md
- 2026-01-14 10:04:49.983655 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.playwright-mcp/gen4_v23_1_rebirth.png
- 2026-01-14 10:04:33.207654 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.playwright-mcp/gen4_v21_1_legendary.png
- 2026-01-13 19:20:16.010755 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_alpha/HFO_ARCHETYPE_ANALYSIS_V1.md.receipt.json
- 2026-01-13 19:15:56.756742 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_alpha/HFO_ARCHETYPE_ANALYSIS_V1.md
- 2026-01-13 17:28:43.856922 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/hfo_mission_thread_alpha.md
- 2026-01-13 10:52:47.282018 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_alpha/p0_observe/mutants/.pytest_cache/v/cache/lastfailed.receipt.json

### omega
- 2026-01-15 15:26:38.676408 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v26_1.html
- 2026-01-15 15:05:52.720345 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/OMEGA_GEN4_CONCORDANCE.md
- 2026-01-15 15:05:44.444344 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/OMEGA_GEN4_MANIFEST.yaml
- 2026-01-15 15:05:35.908344 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/OMEGA_GEN4_CONSOLIDATED_ROADMAP.md
- 2026-01-15 14:53:29.776307 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/ai-chat-error-2026-1-15.md
- 2026-01-15 12:12:20.453176 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v26.html
- 2026-01-15 12:01:38.786143 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/reports/POSTMORTEM_OMEGA_V25_FAILURE.md
- 2026-01-15 11:48:16.653102 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/reports/POST_MORTEM_OMEGA_GEN_4_V25_FAILURE.md
- 2026-01-15 11:21:37.556102 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v25_2.html
- 2026-01-15 11:04:55.138051 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v25_spec.yaml

### tectangle
(none)

### drumpad
(none)

### tags
- 2026-01-12 19:11:22.457694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/setuptools/_vendor/packaging/tags.py
- 2026-01-12 19:11:22.457694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/setuptools/_vendor/packaging/__pycache__/tags.cpython-311.pyc
- 2026-01-12 19:11:22.216694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/tags.py
- 2026-01-12 19:11:22.215694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/pkg_resources/_vendor/packaging/__pycache__/tags.cpython-311.pyc
- 2026-01-12 19:11:22.181694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/pip/_vendor/packaging/tags.py
- 2026-01-12 19:11:22.178694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/pip/_vendor/packaging/__pycache__/tags.cpython-311.pyc
- 2026-01-12 19:11:22.151694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/pip/_internal/utils/compatibility_tags.py
- 2026-01-12 19:11:22.147694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/pip/_internal/utils/__pycache__/compatibility_tags.cpython-311.pyc
- 2026-01-12 19:11:21.690694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/packaging/tags.py
- 2026-01-12 19:11:21.689694 | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.stryker-tmp/sandbox-s5piJz/.venv/lib/python3.11/site-packages/packaging/__pycache__/tags.cpython-311.pyc

## Newest paths (top 25)
- 2026-01-15 15:26:38.676408 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v26_1.html
- 2026-01-15 15:22:34.141396 | score=35 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl
- 2026-01-15 15:12:32.976365 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_152233/hot_obsidian_blackboard.jsonl
- 2026-01-15 15:09:19.064355 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_151231/hot_obsidian_blackboard.jsonl
- 2026-01-15 15:06:30.715347 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/check_blackboard.txt
- 2026-01-15 15:05:52.720345 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/OMEGA_GEN4_CONCORDANCE.md
- 2026-01-15 15:05:44.444344 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/OMEGA_GEN4_MANIFEST.yaml
- 2026-01-15 15:05:35.908344 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/OMEGA_GEN4_CONSOLIDATED_ROADMAP.md
- 2026-01-15 15:01:21.716331 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/hfo_mtg_commanders/KRAKEN_KEEPER_ASSIMILATION_PROTOCOL.md
- 2026-01-15 14:59:34.825326 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_150037/hot_obsidian_blackboard.jsonl
- 2026-01-15 14:59:23.348325 | score=10 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/.gitignore
- 2026-01-15 14:53:29.776307 | score=15 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/ai-chat-error-2026-1-15.md
- 2026-01-15 14:53:19.510306 | score=25 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/ttao-notes-2025-1-14.md
- 2026-01-15 14:50:36.159298 | score=10 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/ROOT_GOVERNANCE.md
- 2026-01-15 14:43:02.574275 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/p0_vitality.log
- 2026-01-15 14:41:09.499269 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/p1.log
- 2026-01-15 14:36:09.632254 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/p7.log
- 2026-01-15 14:36:09.588254 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/p5.log
- 2026-01-15 14:36:09.552254 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/p4.log
- 2026-01-15 14:36:09.539254 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/p3.log
- 2026-01-15 14:36:09.523254 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/p2.log
- 2026-01-15 14:14:11.674186 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/MISSION_CONTROL/P0_LIDLESS_LEGION_PROTOCOL.md
- 2026-01-15 14:14:11.665186 | score=10 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/MISSION_CONTROL/EXECUTIVE_SUMMARY.md
- 2026-01-15 14:14:11.665186 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/MISSION_CONTROL/PORT_PROTOCOL_TEMPLATE.md
- 2026-01-15 14:14:11.663186 | score=0 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/MISSION_CONTROL/INGEST_STATUS_REPORT.md

## Highest-score paths (top 25)
- score=45 | 2026-01-15 13:03:49.989970 | / | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_ingest_master.py
- score=45 | 2026-01-15 12:12:40.833177 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/DUCKDB_ROLLUP_PLAN.md
- score=45 | 2026-01-13 13:21:52.232628 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/hfo_mtg_commanders/MASTER_HFO_COMMANDER_VAULT.md
- score=36 | 2026-01-02 11:57:00 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/cold/bronze/archive_2025-12-31/cold_bronze_content/archive/session_logs/ttao_notes_compilation.json
- score=36 | 2026-01-02 11:57:00 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/hfo_gen87_x3/cold/bronze/archive_2025-12-31/cold_bronze_content/archive/session_logs/TTAO_NOTES_COMPILATION.md
- score=35 | 2026-01-15 15:22:34.141396 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 12:53:05.968249 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/MISSION_CONTROL/HIVE_DASHBOARD.html
- score=35 | 2026-01-15 12:53:03.328249 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_html_dashboard.py
- score=35 | 2026-01-15 12:45:05.134224 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_124927/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 12:29:30.989176 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_123925/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 12:24:53.108162 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_122923/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 12:19:12.126145 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_121914/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 12:18:42.651143 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_121902/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 12:13:21.924179 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_121831/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 12:05:15.272154 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_120609/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:55:55.363126 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_115559/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:54:59.517123 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_115549/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:52:27.996115 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_115240/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:42:04.607083 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_114232/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:40:05.129159 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_114153/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:38:48.609155 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_113849/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:38:34.654154 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_113836/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:36:20.244147 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_113706/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:33:55.646140 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_113355/hot_obsidian_blackboard.jsonl
- score=35 | 2026-01-15 11:33:27.291138 | GEN88_ACTIVE/active | /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_20260115_113349/hot_obsidian_blackboard.jsonl
