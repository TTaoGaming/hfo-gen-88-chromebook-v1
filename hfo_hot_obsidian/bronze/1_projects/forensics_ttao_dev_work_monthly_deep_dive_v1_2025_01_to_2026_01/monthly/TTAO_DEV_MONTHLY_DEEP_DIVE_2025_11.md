# Medallion: Bronze | Mutation: 0% | HIVE: V

# TTao Dev Work — Monthly Deep Dive v1: 2025-11

## Provenance
- Generated (UTC): 2026-01-22T02:04:06.548497Z
- DuckDB: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
- Window (modified_at): 2025-11-01T00:00:00 .. 2025-12-01T00:00:00 (start inclusive, end exclusive)

## Scope notes (first pass)
- This report is purely based on `file_system.modified_at` (file index).
- It does not assume older forks are ‘your work’; it only reports what files appear in the index for this month window.

## Summary
- Indexed file records this month: 79318
- Earliest modified_at in month: 2025-11-04 08:18:52.968806
- Latest modified_at in month: 2025-11-30 22:21:57.904808

## Keyword path hits (counts)
- hopeos: 0
- alpha: 1368
- omega: 5
- tectangle: 3
- drumpad: 0
- tags: 36

## Top eras (by count)
| era | n |
|---|---|
| UNCATEGORIZED | 73134 |
| COLD_BRONZE_2025 | 5450 |
|  | 506 |
| COMPUTER_VISION_EARLY | 152 |
| HFO_BOOTSTRAP | 36 |
| TAGS_DRUMPADS | 36 |
| TECTANGLE_ERA | 3 |
| GEN88_ACTIVE | 1 |

## Top projects (by count)
| project | n |
|---|---|
| _archive_dev_2026_1_14 | 78811 |
|  | 506 |
| active | 1 |

## Top buckets (by count; coarse path prefix)
| bucket | n |
|---|---|
| home/tommytai3/_archive_dev_2026_1_14/miniconda3 | 39920 |
| home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY | 31513 |
| home/tommytai3/_archive_dev_2026_1_14/go | 6149 |
| home/tommytai3/_archive_dev_2026_1_14/hive_fleet_obsidian_2025_11 | 1488 |
| home/tommytai3/_archive_dev_2026_1_14/_HFO_ARCHIVE | 247 |
| home/tommytai3/active/hfo_gen_88_chromebook_v_1 | 1 |

## Hotspots (path substring counts)
| substring | n |
|---|---|
| tests/ | 5241 |
| scripts/ | 100 |
| build/ | 90 |
| __pycache__ | 33 |
| vendor/ | 8 |

## Patterns (heuristic)
- High concentration in one bucket (home/tommytai3/_archive_dev_2026_1_14/miniconda3) ≈ 50% of indexed records.
- Both omega and alpha keywords appear this month (cross-thread work visible in path-level signals).

## Anti-patterns / risks (heuristic)
- Concentration can indicate coupling/hotspot risk; consider splitting responsibilities or adding gates.
- Presence of __pycache__ suggests derived Python artifacts; consider excluding from tracked changes.

## Top extensions (by count)
| ext | n |
|---|---|
| py | 21534 |
| h | 10378 |
| manifest | 8587 |
| txn | 8587 |
| lance | 8582 |
| md | 5592 |
| go | 4602 |
| json | 1710 |
|  | 1700 |
| zip | 1218 |
| pyi | 919 |
| so | 456 |

## Keyword samples (newest paths)
### hopeos
(none)

### alpha
- 2025-11-30 00:18:07.582036 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_61/brain/intent_swarm_philosophy.feature
- 2025-11-29 17:33:56.834404 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_60/nerves/swarm_heartbeat.py
- 2025-11-29 12:06:14.783399 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_60/brain/lore_swarmlord_persona.md
- 2025-11-29 12:06:14.783399 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_60/brain/design_swarmlord_perspectives.md
- 2025-11-29 11:10:09.853227 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_60/brain/Swarmlord_of_Webs_Digest_Gen60_Architecture.md
- 2025-11-29 11:10:09.853227 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_60/brain/design_swarmlord_variations.md
- 2025-11-28 22:50:30.596240 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_60/brain/prey_swarm.py
- 2025-11-28 21:15:50.200949 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_59/hydra/hydra_swarm.py
- 2025-11-28 21:15:50.191949 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_59/brain/prey_swarm.py
- 2025-11-28 20:53:31.468881 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_59/hydra/__pycache__/hydra_swarm.cpython-313.pyc

### omega
- 2025-11-30 00:18:07.568036 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_61/brain/verse_0_omega_variants.md
- 2025-11-30 00:18:07.568036 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_61/brain/verse_0_omega_variants_v2.md
- 2025-11-30 00:18:07.568036 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_61/brain/verse_0_omega_variants_v3.md
- 2025-11-20 23:53:43.419339 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/scipy/special/tests/test_wrightomega.py
- 2025-11-20 23:53:43.411339 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/scipy/special/_precompute/wrightomega.py

### tectangle
- 2025-11-22 02:18:44.939742 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Cleanup_Logs/Audit_History/audit_trail/logs/swarm_tectangle_100.log
- 2025-11-22 02:08:31.262711 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Cleanup_Logs/Audit_History/audit_trail/logs/swarm_tectangle_retry.log
- 2025-11-22 02:05:41.683702 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Cleanup_Logs/Audit_History/audit_trail/logs/swarm_tectangle.log

### drumpad
(none)

### tags
- 2025-11-28 08:45:27.154648 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_ARCHIVE/Legacy_Snapshots/hfo-archives-2025-12-03/hfo_gem_gen_1_to_gen_50/gen_24/models/tags.yml
- 2025-11-25 21:08:00.878486 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/torchgen/packaged/ATen/native/tags.yaml
- 2025-11-25 20:37:16.505391 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/lance_namespace_urllib3_client/models/list_table_tags_response.py
- 2025-11-24 07:29:11.350036 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Legacy_Code/legacy/gen_63_root/memory/procedural/gen_1_50_codebase/HFO_2025_11_19/hfo_gem/gen_24/models/tags.yml
- 2025-11-21 17:31:06.505691 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/jsonpickle/tags_pd.py
- 2025-11-21 17:31:06.504691 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/jsonpickle/tags.py
- 2025-11-21 03:02:17.468917 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/ray/autoscaler/tags.py
- 2025-11-20 23:53:48.880340 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/sklearn/utils/tests/test_tags.py
- 2025-11-20 23:53:48.859339 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/sklearn/utils/_tags.py
- 2025-11-19 19:57:32.000946 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/fontTools/unicodedata/OTTags.py

## Newest paths (top 25)
- 2025-11-30 22:21:57.904808 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/189.manifest
- 2025-11-30 22:21:57.897808 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_transactions/188-fcb5e326-b7eb-4c0d-81e9-d10319e02efc.txn
- 2025-11-30 22:21:57.884808 | score=6 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/0110111111001011111010107e88174c319db19e04bd56748b.lance
- 2025-11-30 21:30:27.829651 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/188.manifest
- 2025-11-30 21:30:27.822651 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_transactions/187-fd7a44da-683e-474d-b510-9bc08397f3c8.txn
- 2025-11-30 21:30:27.810650 | score=26 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/100000101011100110111001cc81024e9095b6af051450b36e.lance
- 2025-11-30 21:07:21.600580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/187.manifest
- 2025-11-30 21:07:21.599580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_transactions/186-64f45231-7eb4-4a05-8482-ac342b949346.txn
- 2025-11-30 21:07:21.596580 | score=6 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/1011101101110010101001008f07ae44758ca097e57239eaf2.lance
- 2025-11-30 21:07:20.315580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_transactions/185-aa845f0b-a310-4f3e-83bd-8a4cef432af5.txn
- 2025-11-30 21:07:20.315580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/186.manifest
- 2025-11-30 21:07:20.311580 | score=6 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/001100101011100011011110f178ce45589d61a4c448b8f2ee.lance
- 2025-11-30 21:07:19.135580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/185.manifest
- 2025-11-30 21:07:19.134580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_transactions/184-29e8f4b1-2f04-4b99-a1f3-00494e99958b.txn
- 2025-11-30 21:07:19.130580 | score=6 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/110011000001010101101011b9cbf9479b84129ccc7c74e837.lance
- 2025-11-30 21:07:18.061580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_transactions/183-1ce693d8-8451-473d-971d-a3d64b3a9f9a.txn
- 2025-11-30 21:07:18.061580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/184.manifest
- 2025-11-30 21:07:18.057580 | score=6 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/00011100111100011000011025e74546f58ed35b7ce0be9cda.lance
- 2025-11-30 21:07:17.622580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/183.manifest
- 2025-11-30 21:07:17.621580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_transactions/182-60620faa-6880-45f0-a31b-08d453b087cf.txn
- 2025-11-30 21:07:17.618580 | score=6 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/100000010010010011010111fcb9b8429bb17bf8d1cd4e6b1d.lance
- 2025-11-30 21:07:17.028580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/182.manifest
- 2025-11-30 21:07:17.027580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_transactions/181-93df1b81-34fc-473a-8615-4bf92b7d1ed3.txn
- 2025-11-30 21:07:17.023580 | score=6 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/0001010000001110101000111b770f4b37821359c152b3c8d8.lance
- 2025-11-30 21:07:16.512580 | score=1 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/_versions/181.manifest

## Highest-score paths (top 25)
- score=31 | 2025-11-09 20:18:14.286898 | / | /home/tommytai3/_archive_dev_2026_1_14/go/bin/temporal-mcp
- score=31 | 2025-11-08 19:32:11.491830 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/bin/python
- score=31 | 2025-11-08 19:32:11.491830 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/bin/python3
- score=31 | 2025-11-08 19:32:11.491830 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/bin/python3.1
- score=31 | 2025-11-08 19:32:11.491830 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/bin/python3.13
- score=26 | 2025-11-30 21:30:27.810650 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/memories.lance/data/100000101011100110111001cc81024e9095b6af051450b36e.lance
- score=26 | 2025-11-19 01:41:04 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_ARCHIVE/Legacy_Snapshots/hfo-archives-2025-12-03/hfo_gem_gen_1_to_gen_50/gen_43/adapters/tensorboard/metadata.tsv
- score=26 | 2025-11-19 01:41:04 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Legacy_Code/legacy/gen_63_root/memory/procedural/gen_1_50_codebase/HFO_2025_11_19/hfo_gem/gen_43/adapters/tensorboard/metadata.tsv
- score=26 | 2025-11-19 01:33:27 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Legacy_Code/legacy/gen_63_root/memory/procedural/gen_1_50_codebase/HFO_2025_11_19/hfo_gem/gen_43/hfo_memory_dashboard.html
- score=26 | 2025-11-19 01:16:32 | COLD_BRONZE_2025/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Legacy_Code/legacy/gen_63_root/memory/procedural/gen_1_50_codebase/HFO_2025_11_19/hfo_gem/gen_43/hfo_memory_viz.html
- score=26 | 2025-11-08 20:32:31.588015 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/share/jupyter/lab/staging/yarn.js
- score=21 | 2025-11-30 21:05:25.711574 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_63/06_assimilator_memory/lancedb/hfo_gen_61_lancedb/hfo_vectors.lance/data/11111001000001101100101081c02e4363b4a383c48347f307.lance
- score=21 | 2025-11-30 15:49:22.119892 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Databases/Historical_Buds/hfo_gem_gen_61/memory/hfo_gen_61_lancedb/hfo_vectors.lance/data/11111001000001101100101081c02e4363b4a383c48347f307.lance
- score=21 | 2025-11-19 19:30:32.729864 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/pkgs/cache/47929eba.solv
- score=21 | 2025-11-11 14:01:00.064876 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/python3.13/site-packages/psycopg2_binary.libs/libcrypto-2e26a48f.so.3
- score=21 | 2025-11-08 21:01:19.304103 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/pkgs/cache/09cdf8bf.solv
- score=21 | 2025-11-08 19:48:31.285880 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/libglib-2.0.so.0
- score=21 | 2025-11-08 19:48:31.285880 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/libglib-2.0.so.0.8400.4
- score=21 | 2025-11-08 19:48:15.353880 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/pkgs/jupyter-sysml-kernel-0.53.0-pyhd8ed1ab_0.conda
- score=21 | 2025-11-08 19:32:12.365830 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/libpython3.13.so.1.0
- score=21 | 2025-11-08 19:32:10.825830 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/libcrypto.so.3
- score=21 | 2025-11-08 19:32:10.725830 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/miniconda3/lib/libcrypto.a
- score=21 | 2025-11-08 16:16:44.264047 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Legacy_Code/legacy/gen_63_root/memory/episodic/raw_audit_logs/hfo_gems_raw/HiveFleetObsidian_hfo_gem/gen_9/deep_dive.md
- score=21 | 2025-11-08 16:16:44.264047 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Legacy_Code/legacy/gen_63_root/memory/procedural/gen_1_50_codebase/HiveFleetObsidian_hfo_gem/gen_9/deep_dive.md
- score=21 | 2025-11-08 16:16:44.263047 | UNCATEGORIZED/_archive_dev_2026_1_14 | /home/tommytai3/_archive_dev_2026_1_14/_HFO_LIBRARY/Legacy_Code/legacy/gen_63_root/memory/episodic/raw_audit_logs/hfo_gems_raw/HiveFleetObsidian_hfo_gem/gen_5/original_gem.md
