<!-- Medallion: Silver | Mutation: N/A | HIVE: V -->

# HFO SSOT SQLite: Ingest Coverage Proof Report (V1, 2026-01-28T22:27:14Z)

## Scope
You asked: “what is in sqlite memory and what is not anymore / how much is ingested already?”

This report is **evidence-backed** from the blessed Doobidoo SSOT SQLite DB.

## SSOT target (blessed)
- SSOT file: `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`

## Proof: direct SQLite query results (snapshot)
The following JSON was produced by querying the `memories` table directly:

```json
{
  "db": "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db",
  "schema_columns": [
    "id",
    "content_hash",
    "content",
    "tags",
    "memory_type",
    "metadata",
    "created_at",
    "updated_at",
    "created_at_iso",
    "updated_at_iso",
    "deleted_at"
  ],
  "rows_total": 6751,
  "max_id": 6751,
  "tag_source_portable": 6423,
  "tag_source_report": 1,
  "meta_portable_path": 6423,
  "meta_gem_path": 209,
  "meta_monthly_gen72_path": 0,
  "content_exec_summary_title": 1,
  "latest_5": [
    {
      "id": 6751,
      "updated_at": "1769638921.93268",
      "tags_prefix": "gen88_v4,exec_summary,source:report,topic:ssot,topic:ingest_status,epoch:2026_01"
    },
    {
      "id": 6750,
      "updated_at": "1769638425.65446",
      "tags_prefix": "gen88_v4,ssot,status_update,topic:memory_ingest_exec_summary_v1_2026_01_28"
    },
    {
      "id": 6749,
      "updated_at": "1769636970.71037",
      "tags_prefix": "gen88_v4,status_update,ingest_sources,repo_hygiene,topic:repo_root_corpora_moved"
    },
    {
      "id": 6748,
      "updated_at": "1769634792.94452",
      "tags_prefix": "gen88_v4,ssot,status_update,topic:pain_points_gen1_40_extract_2026_01_28"
    },
    {
      "id": 6747,
      "updated_at": "1769634516.32242",
      "tags_prefix": "gen88_v4,ssot,status_update,topic:doobidoo_fts_setup_2026_01_28"
    }
  ]
}
```

## Proof: SSOT-native retrieval (read path works)
A SSOT-native search for the exec summary title returned exactly one match:
- memory id: `6751`
- source_path points at the markdown report file

(Operator output showed: `total_matches=1 returned=1`.)

## What is ingested (high confidence)
### Overall
- **Total SSOT memories:** `6751`

### Portable corpus (pre-HFO → Gen84)
- **In SSOT:** YES
- Evidence:
  - `tags LIKE '%source:portable%'` → `6423`
  - `metadata LIKE '%portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52%'` → `6423`

### GEM corpus (Gen 1–50)
- **In SSOT:** PARTIAL
- Evidence:
  - `metadata LIKE '%hfo_gem_gen_1_to_gen_50%'` → `209`

### Exec summary report (this session)
- **In SSOT:** YES
- Evidence:
  - `tags LIKE '%source:report%'` → `1`
  - `content LIKE '%HFO Memory: Ingest Status + Cognitive Persistence%'` → `1`

## What is NOT evidenced as ingested (by provenance)
### Monthly deep dive Gen72 folder
- **Not evidenced as ingested:** YES (meaning: SSOT has no provenance match for that folder yet)
- Evidence:
  - `metadata LIKE '%monthly_deep_dive_gen_72%'` → `0`

## Interpretation (tight)
- You currently have **6751** memories inside the SSOT SQLite.
- The “portable pre-HFO→Gen84” material accounts for **6423** SSOT rows.
- The Gen72 monthly deep dive folder appears **not yet ingested** into SSOT (no provenance hits).

## Next SSOT-safe steps (low credit burn)
1) Dry-run ingest `hfo_hot_obsidian/bronze/3_resources/ingest_sources/monthly_deep_dive_gen_72` with `--max-files`.
2) If dry-run looks right, ingest in small write batches (e.g. 50–200 files per run) to avoid instability.
3) Re-run SSOT health checks after each batch.

## Sources
- SSOT DB: `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`
- Exec summary ingested: `hfo_hot_obsidian_forge/1_silver/2_resources/reports/HFO_MEMORY_INGEST_STATUS_AND_COGNITIVE_PERSISTENCE_EXEC_SUMMARY_V1_2026_01_28.md`
