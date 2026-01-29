<!-- Medallion: Silver | Mutation: N/A | HIVE: V -->

# HFO Memory: Ingest Status + Cognitive Persistence — Exec Summary (V1, 2026-01-28)

## What I am doing (plain language)
- Reducing “repo root clutter” by moving large historical corpora into a single **ingest_sources** area.
- Updating the few places in code/docs that referenced the old root paths.
- Proving (with SSOT queries) what is already in the Doobidoo SSOT vs what still needs ingest.
- Reducing freezes/crashes by stopping VS Code from indexing/searching the huge corpora directory by default.

## What is done (proof)
### 1) Root corpora moved out of repo root
The following now live under:
- `hfo_hot_obsidian/bronze/3_resources/ingest_sources/`

Directory proof (shell): the folder exists and contains:
- `hfo_gem_gen_1_to_gen_50`
- `monthly_deep_dive_gen_72`
- `portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52`

### 2) Key internal references updated
- `scripts/hfo_memory_export_portable_duckdb_to_jsonl.py` (example `--db` path updated)
- `scripts/hfo_memory_fragments_manifest.py` (scan root updated)
- `hfo_hot_obsidian/bronze/3_resources/reports/HFO_PAIN_POINTS_GEN1_40_EXTRACT_V1_2026_01_28.md` (references updated)

### 3) Crash mitigation applied
- `.vscode/settings.json`: excluded `**/hfo_hot_obsidian/bronze/3_resources/ingest_sources/**` from VS Code watchers + search.
  - Goal: prevent VS Code/ripgrep/language servers from trying to index huge corpora and spiking memory.

## Why things “kept crashing”
- Some failures were not “mystery crashes” — they were hard errors:
  - A derived index builder hit `OSError: [Errno 36] File name too long` because it encoded full paths into filenames. Fix was to switch to short hashed filenames.
  - A query attempted to read a `source_path` column that does not exist in SSOT (SSOT stores `source_path` inside `metadata`).
- The “502” is typically an upstream/service-side failure (VS Code extension host / network / provider), not your code. The consistent pattern is: large-repo operations + memory spikes increase the likelihood of these failures.

## Are we already ingested into SSOT or not? (proof-backed)
SSOT file:
- `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`

Evidence from direct SSOT queries:
- **SSOT total rows:** `6750`

### Portable DuckDB corpus (pre-HFO → Gen84)
- **Already ingested:** YES.
- Proof:
  - `tags LIKE '%source:portable%'` count = `6423`
  - `metadata LIKE '%portable_hfo_memory_pre_hfo_to_gen84_2025-12-27T21-46-52%'` count = `6423`
  - This means the portable corpus is already present inside SSOT as `portable_artifact`-style records.
- Note: metadata still contains the *old absolute source_path* pointing to the original location; that is provenance, not a live dependency.

### GEM corpus (Gen 1–50 folder)
- **Partially ingested:** YES (but not complete).
- Proof:
  - `metadata LIKE '%hfo_gem_gen_1_to_gen_50%'` count = `209`
- Interpretation:
  - Some GEM content made it into SSOT (likely via portable artifacts and/or prior ingest), but this count is far smaller than “entire corpus ingested.”

### Monthly deep dive Gen72 folder
- **Not ingested (as a direct SSOT source path):** NO.
- Proof:
  - `metadata LIKE '%monthly_deep_dive_gen_72%'` count = `0`
- Interpretation:
  - The folder exists in the repo now, but SSOT does not show evidence that its files were ingested with provenance.

## Cognitive persistence Jan 2025 → now: do we have broad strokes?
- **Yes, on the filesystem**: you have a month-by-month deep dive archive under Hot Obsidian projects (2025-01 through 2026-01), which supports “broad strokes then drill down.”
- **Yes, partially in SSOT**:
  - SSOT already contains a very large portable corpus (6423 rows) spanning pre-HFO → Gen84.
  - SSOT can store additional summaries/doctrine/rollups for long-horizon continuity.
- **But the key gap** is: not everything you want is ingested into SSOT with consistent provenance/tags yet (notably the moved `monthly_deep_dive_gen_72`).

## What you should ingest next (carefully)
### Priority 1 — Monthly deep dive Gen72 folder
- Ingest it as text/markdown with clear tags:
  - `tags`: `gen88_v4`, `source:monthly_deep_dive_gen72`, `epoch:2025_to_2026`, plus any project tags.
  - `memory_type`: `monthly_deep_dive`
- Run dry-run first, then bounded write (small batches) to avoid freezes.

### Priority 2 — GEM corpus (only if you need it as first-class SSOT content)
- Since it’s partially ingested already (209 matches), do a careful ingest to avoid duplicates.
- Use strong tags like `source:gem`, `epoch:gen1_50` and keep memory_type consistent.

## After ingest: “sorted/prioritized with Shodh Hebbian learning”
- Treat **Doobidoo SSOT** as the canonical store.
- Treat **Shodh** as a derived, rebuildable index that can apply ranking / Hebbian-style reinforcement over time.
- Operationally:
  1) Ingest into SSOT (bounded, tagged).
  2) Rebuild/update derived indexes (Shodh; optionally SSOT-derived FTS).
  3) Run high-level rollups first (broad strokes) and store those rollups back into SSOT as `status_update`/`note` so future retrieval is cheap.

## Immediate next action (low risk)
- Ingest `monthly_deep_dive_gen_72` with a dry-run first, then a small write batch (e.g., max files / limit), and only then scale up.
