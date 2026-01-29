# Medallion: Silver | Mutation: 0% | HIVE: V

# Doobidoo (Doobidoo sqlite_vec SSOT) — Best Practices (V1, 2026-01-28)

## What Doobidoo is for (SSOT)

- **Doobidoo sqlite_vec is the SSOT**: canonical content + tags + metadata live here.
- **Writes go here only**. Everything else is either:
  - **Derived** (rebuildable): Shodh index, DuckDB analytics.
  - **Legacy/telemetry** (no-write): JSON/JSONL ledgers, old sqlite files.

Ground truth check (current SSOT): `hfo_hub.py health:ssot --json` reports **6745 alive rows** in:
- `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`

## The safe operator workflow (always)

- Guardrails first:
  - `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot guard`
- Confirm SSOT health:
  - `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py health:ssot --json`
- Ingest (dry-run mindset; then write):
  - `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot ingest-md --dir <DIR> --tags gen88_v4 ssot --max-files 200 --write`
  - `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot ingest-text --dir <DIR> --tags gen88_v4 ssot --max-files 200 --max-bytes 2000000 --write`
- Search (works even if Shodh is down):
  - `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot search --query "..." --limit 10`

## FTS (deterministic lexical search)

- Build/rebuild derived FTS index (rebuildable; does NOT mutate SSOT):
  - `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot build-fts --rebuild --limit 0`
- Query FTS:
  - `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot search-fts --query "hive8" --limit 8`

## Standardization rules (to prevent drift)

- **Deduping**: rely on `content_hash` (idempotent ingest). Expect duplicates across exports; SSOT ingest should skip duplicates.
- **Provenance** (metadata): always keep at least:
  - `source` (script/entrypoint), `source_path` (original file), `ingest_ts`.
- **Tags**: use a small stable base set and extend with `topic:*` tags.
  - Example base: `gen88_v4 ssot` + `memory_type`-appropriate tags.
- **memory_type**: keep a small taxonomy (examples): `note`, `doctrine`, `status_update`, `incident`.

## “Everything into SQLite with semantic + FTS” — how hard is it?

It’s feasible, and at your current scale it’s not too large.

### Practical sizing intuition (rule-of-thumb)

- You’re currently at ~6.7k rows; the SSOT sqlite is small enough to stay ergonomic.
- Embeddings storage cost depends on vector dimensionality and indexing:
  - Example: 384-dim float32 vector is ~1.5 KiB/row (plus overhead).
  - 100k rows → on the order of hundreds of MiB for vectors; 1M rows → multiple GiB.
- FTS indexes grow roughly with text volume and tokenization; expect a meaningful multiplier for large corpora.

### Best architecture (still “all SQLite”, but safer)

- **Recommended**: keep **SSOT sqlite** as canonical truth, and build **derived SQLite indexes**:
  - `ssot.db` (authoritative): canonical content + metadata + tags + content_hash.
  - `ssot_index.db` (derived/rebuildable): FTS5 tables + optional vector index for fast retrieval.

Why this is best:
- No risky schema/migration changes inside the SSOT file.
- Rebuild drills are easy: delete `ssot_index.db` and regenerate from `ssot.db`.
- You still get deterministic lexical search (FTS5) even when embeddings/rankers aren’t installed.

### Single-file alternative (harder)

- You *can* add an FTS5 virtual table into the SSOT sqlite itself, but it’s higher risk:
  - You must manage schema migrations alongside `mcp-memory-service`.
  - You must keep triggers in sync for inserts/updates.

## Duplicate handling (best practice)

- Treat duplicates as normal; ingestion should be idempotent.
- Prefer:
  - normalized content (consistent newlines/whitespace)
  - stable provenance (`source_path`)
  - `content_hash`-based dedupe

## What not to do

- Don’t write memory to JSONL (telemetry/legacy only).
- Don’t treat DuckDB or Shodh as authoritative. They are caches/views.

## Related docs

- `HFO_SSOT_FRONT_DOOR_QUICKSTART_V1_2026_01_28.md`
- `HFO_GEN88_V4_DOOBIDOO_SSOT_SETUP.md`
