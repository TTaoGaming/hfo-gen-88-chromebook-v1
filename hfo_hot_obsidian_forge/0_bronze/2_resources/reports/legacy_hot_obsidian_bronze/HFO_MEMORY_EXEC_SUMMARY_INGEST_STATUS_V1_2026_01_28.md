# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Memory Executive Summary — Ingest Status (Jan 2025 → Now)
Generated: 2026-01-28

## TL;DR
- **SSOT is healthy and populated**: 6,749 total rows in Doobidoo SSOT.
- **Portable corpus is effectively ingested**: 6,423 / 6,749 rows are tagged `source:portable`.
- **GEM + Monthly Deep Dive appear present, but provenance is not conclusively tied to the moved corpora directories**: term hits exist in SSOT `metadata`/`content`, but these may include embedded mentions (reports/status updates), not necessarily raw-file ingestion.

## What is “ingested” (grounded)
### Canonical SSOT (Doobidoo)
- SSOT DB (blessed write path) resolves to:
  - `hfo_hot_obsidian/bronze/3_resources/memory_fragments_storehouse/blessed_ssot/artifacts__mcp_memory_service__gen88_v4__hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`
- Evidence (queried via sqlite):
  - `rows_total = 6749`
  - `portable_tagged = 6423` (tags `LIKE '%source:portable%'`)

### Evidence of GEM / Monthly Deep Dive content (weaker than tags)
- GEM indicator hit (SSOT `metadata LIKE '%original_gem.md%'`): `41`
- Monthly Deep Dive indicator hit (SSOT `content LIKE '%MONTHLY DEEP DIVE%'`): `60`
- Monthly Deep Dive namespace hit (SSOT `metadata LIKE '%TTAO_DEV_MONTHLY_DEEP_DIVE%'`): `29`

Interpretation:
- These show **presence of terms** in SSOT, not necessarily “raw corpus ingested with file provenance”.
- SSOT schema note: there is **no `source_path` column**; provenance is carried in `metadata` (JSON text). This limits how strongly we can prove “this exact directory was ingested” without a dedicated provenance query/contract.

## Repo hygiene / large-corpora handling (done)
- Large corpora were moved out of repo root into `hfo_hot_obsidian/bronze/3_resources/ingest_sources/` (see prior SSOT status update and pointer updates).
- VS Code crash mitigation: `ingest_sources/**` excluded from watcher + search in `.vscode/settings.json`.

## Derived artifacts status (done)
### Storage manifest
- Regenerated the storage manifest snapshot (and refreshed `latest.json`):
  - `artifacts/memory_manifest/hfo_memory_storage_manifest_20260128T220633Z.json`
  - `artifacts/memory_manifest/latest.json`

### Fragments manifest + collection view
- Fixed `scripts/hfo_memory_fragments_manifest.py` to **exclude symlink views** from discovery/seeding.
  - This prevents stale symlink targets from leaking old paths into new manifests/collections.
- Regenerated:
  - fragments manifest: `artifacts/memory_manifest/hfo_memory_fragments_gen88_v4_2026_01_28T221042Z.yaml`
  - collection run directory: `hfo_hot_obsidian_forge/0_bronze/2_resources/memory_fragments_collection/run_2026_01_28T221045Z/`

## What remains uncertain (and why)
- The moved corpora directories:
  - `hfo_gem_gen_1_to_gen_50/`
  - `monthly_deep_dive_gen_72/`
  - `portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52/`
  are now “available as ingest sources”, but **SSOT does not currently expose a single definitive provenance field** to prove “this exact directory was ingested”.

- Additionally, if ingestion is **content-hash deduped**, re-ingesting already-present text may:
  - skip inserts (good), but
  - **not update provenance** (so it won’t improve proof that a *specific moved directory* was a source).

## Recommended next steps (grounded)
1) **Decide what ‘ingested’ means operationally**
   - If “cognitive persistence” means “the text is present in SSOT for recall/synthesis”, then Portable is already a strong yes.
   - If “ingested” means “file-level provenance to these moved corpora paths is recorded”, then we need a provenance strategy (schema/contract + ingestion behavior).

2) **If you want stronger provenance without schema changes**
   - Add a dedicated SSOT status/update memory that records:
     - corpus root path
     - corpus hash (directory hash or manifest hash)
     - ingestion run timestamp
     - tool/version
   This gives auditability without rewriting old memories.

3) **If you want true per-memory provenance updates (schema + behavior)**
   - Extend ingestion to “merge provenance metadata on duplicate content_hash” rather than skipping.
   - This is a Silver/Gold change and should be contract-driven (Zod in `contracts/`).

4) **After ingestion/provenance stabilization: prioritize with Shodh/Hebbian learning**
   - Treat Shodh as derived ranking:
     - strengthen edges by co-occurrence (tags/time windows) and by repeated recall outcomes
     - keep SSOT immutable as the source of truth; store ranking edges in derived stores (DuckDB/Shodh)

## Sources (repo)
- SSOT pointer: `hfo_pointers.json`
- Storage manifest: `artifacts/memory_manifest/latest.json`
- Fragments manifest: `artifacts/memory_manifest/hfo_memory_fragments_gen88_v4_2026_01_28T221042Z.yaml`
- Collection index: `hfo_hot_obsidian_forge/0_bronze/2_resources/memory_fragments_collection/run_2026_01_28T221045Z/index.yaml`
- Manifest/collection tools: `scripts/hfo_memory_fragments_manifest.py`, `scripts/hfo_memory_collect_fragments.py`
