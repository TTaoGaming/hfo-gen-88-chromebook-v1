<!-- Medallion: Silver | Mutation: N/A | HIVE: V -->

# HFO SSOT: Archive Ingest Coverage (Final V1, 2026-01-28T22:46:34Z)

## Credit burn (user-provided)
- `credit_burn_counter: 9`

## What “coverage %” means (this report)
Coverage is computed from two hard sources:
- **Denominator**: markdown files present on disk under the dropped-in archive directories.
- **Numerator**: those markdown files that have **at least one SSOT row** referencing the file path via:
  - a `source:file:<path>` tag match, OR
  - a `metadata` substring match containing the workspace-relative path.

This is **provenanced ingestion coverage**: it measures whether SSOT can point back to each specific archive file.

## SSOT target (blessed)
- `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`

## Archive scope (“dropped in archive”)
- Monthly deep dives (Gen72): `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/monthly_deep_dive_gen_72/`
- GEM (Gen1–50): `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/`

## Results (coverage %)
### Monthly deep dives (Gen72)
- Markdown files on disk: `10`
- Files with SSOT provenance: `10`
- Coverage: **100.00%**

### GEM corpus (Gen1–50)
- Markdown files on disk: `207`
- Files with SSOT provenance: `200`
- Coverage: **96.62%**

### Combined (Monthly + GEM)
- Markdown files on disk: `217`
- Files with SSOT provenance: `210`
- Coverage: **96.77%**

## What is not yet provenanced (missing list)
These files exist on disk but did not have a `source:file:` / `metadata` provenance hit at the time of this report:
- `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_8/deep_dive.md`
- `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_8/original_gem.md`
- `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_8/summary.md`
- `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_9/deep_dive.md`
- `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_9/original_gem.md`
- `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/gen_9/summary.md`
- `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/hfo_gem_gen_1_to_gen_50/handcrafted.md`

## SSOT auxiliary counts (context)
- Total SSOT rows: `7154`
- Tag count `source:monthly_deep_dive_gen72`: `11`
- Tag count `source:gem_gen1_50`: `392`

## How to reach 100% GEM provenance
Run additional bounded GEM batches until those missing files show provenance hits:
- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot ingest-md --dir hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50 --max-files 200 --tags gen88_v4 source:gem_gen1_50 epoch:gen1_50 topic:gem --memory-type note --write`

Then re-run the coverage script (or ask and I’ll rerun it) to verify 100%.

## Proof blob (machine summary)
```json
{
  "db": "artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db",
  "credit_burn_counter_user_provided": 9,
  "corpora": {
    "monthly_deep_dive_gen72": {
      "md_files_total": 10,
      "md_files_with_ssot_provenance": 10,
      "coverage_percent": 100.0
    },
    "gem_gen1_50": {
      "md_files_total": 207,
      "md_files_with_ssot_provenance": 200,
      "coverage_percent": 96.62
    }
  },
  "overall": {
    "md_files_total": 217,
    "md_files_with_ssot_provenance": 210,
    "coverage_percent": 96.77
  },
  "ssot_aux_counts": {
    "rows_total": 7154,
    "source:monthly_deep_dive_gen72": 11,
    "source:gem_gen1_50": 392
  }
}
```
