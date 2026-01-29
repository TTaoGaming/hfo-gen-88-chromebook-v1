<!-- Medallion: Silver | Mutation: N/A | HIVE: V -->

# HFO SSOT: Monthly Deep Dives + GEM Ingest Proof (V1, 2026-01-28T22:42:10Z)

## Credit burn (user-provided)
- `credit_burn_counter: 9`

## Final coverage report
- See: `hfo_hot_obsidian_forge/1_silver/2_resources/reports/HFO_SSOT_ARCHIVE_INGEST_COVERAGE_FINAL_V1_2026_01_28T224634Z.md`

## SSOT target (blessed)
- `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`

## Source corpora locations
The real corpora live here:
- Monthly deep dives (Gen72): `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/monthly_deep_dive_gen_72/`
- GEM (Gen1–50): `hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50/`

Note: `hfo_hot_obsidian/bronze/3_resources/ingest_sources/` contains symlinks for convenience. `find` does not traverse symlinked directories unless you pass `-L`, so earlier `find ... ingest_sources/... -name '*.md'` returned `0` even though the real source dirs contain markdown.

## Proof A — Monthly deep dive content is in SSOT
### Files exist on disk
- `*.md` files in monthly deep dive dir: `10`

### SSOT search proof
Query used:
- `hfo_hub.py ssot search --query "HFO_2025_01_JANUARY_DEEP_DIVE" --limit 3`

Result (SSOT-native output excerpt):
- `total_matches=1 returned=1`
- returned memory:
  - `id=6752`
  - `type=monthly_deep_dive`
  - `source_path=.../monthly_deep_dive_gen_72/HFO_2025_01_JANUARY_DEEP_DIVE.md`
  - tags include: `source:monthly_deep_dive_gen72`

### Tag count proof
- `source:monthly_deep_dive_gen72` tag count in SSOT: `11`

## Proof B — GEM content is in SSOT
### Files exist on disk
- `*.md` files in GEM dir: `207`

### SSOT search proof
Query used:
- `hfo_hub.py ssot search --query "original_gem" --limit 3`

Result (SSOT-native output excerpt):
- `total_matches=156 returned=3`
- returned memories include:
  - `id=7152` (and `7151`, `7150`)
  - `type=note`
  - `source_path=.../hfo_gem_gen_1_to_gen_50/.../original_gem.md` (example: `gen_7/original_gem.md`)
  - tags include: `source:gem_gen1_50`

### Tag count proof
- `source:gem_gen1_50` tag count in SSOT: `392`

## SSOT rowcount (current)
- `rows_total`: `7154`

## Operational takeaway (tight)
- Monthly Gen72 deep dives are now present and queryable in SSOT (at least one file stored, and tag count is non-zero).
- GEM corpus is present and queryable in SSOT (multiple matches returned; tag count is non-zero).

## Next step (if you want full GEM coverage)
Continue ingest in bounded batches (example):
- `hfo_hub.py ssot ingest-md --dir hfo_hot_obsidian/bronze/3_resources/memory_ingest_sources/hfo_gem_gen_1_to_gen_50 --max-files 200 --tags gen88_v4 source:gem_gen1_50 epoch:gen1_50 topic:gem --memory-type note --write`

If you want, I can run additional batches until `stored` reaches ~0 consistently (indicating dedupe saturation) and then emit a final coverage proof.
