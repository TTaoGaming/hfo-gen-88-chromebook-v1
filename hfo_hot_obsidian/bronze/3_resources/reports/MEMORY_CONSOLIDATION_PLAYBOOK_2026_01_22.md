# Medallion: Bronze | Mutation: 0% | HIVE: V

# Memory Consolidation Playbook (Gen88)

## What you actually have (grounded)

### Long-term SSOT candidate (DuckDB)

- `hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb` (~7.1GB)
- This DB is primarily a **file index + content batches + FTS**:
  - `main.file_system(path, hash, score, modified_at, era, project)`
  - `main.fts_unified_docs(batch, path, content)`
  - `main.file_content*` batch tables
  - `main.mission_journal` exists but is lightly populated (not your year of work)

### Working memory (structured summaries)

- `hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl` (~171KB)
- Contains many `type=status_update` entries with `timestamp`, `topic/summary`, and `sources/related_files`.

### Stigmergy blackboards (raw operational events)

- Live: `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl` (~1.8MB)
- Cold: `hfo_cold_obsidian/cold_obsidian_blackboard.jsonl` (~2.6KB)
- Anchors (high-volume snapshots): `hfo_hot_obsidian/4_archive/stigmergy_anchors/anchor_*/hot_obsidian_blackboard.jsonl` (~45MB each)

## Consolidation strategy (Bronze → Silver → Gold)

### Bronze (raw, append-only)

- Keep JSONLs append-only; never rewrite history.
- Anchors are the “checkpointed blackboard history”. Treat them as immutable.

### Silver (integration, queryable)

- Use the merged DuckDB as the *indexable view* of reality:
  - “What changed on a day?” → `file_system.modified_at`
  - “Where is the content?” → `fts_unified_docs.content`
- Keep working-memory summaries as a separate stream (JSONL), then reference them in Silver rollups.

### Gold (hardened, human-readable)

- Gold artifacts are curated rollups (Markdown) that link to evidence.
- Principle: **Gold is edited** (human curation) but always traceable to Silver/Bronze sources.

## Daily rollups (repeatable)

Use the generator:

- Daily:
  - `python3 scripts/hfo_rollup_generate.py daily --day 2026-01-21`
  - Output: `hfo_hot_obsidian/silver/3_resources/reports/rollups/daily/ROLLUP_2026_01_21.md`

What the daily rollup includes:

- `status_update` entries from `mcp_memory.jsonl` on that day
- blackboard events from `hot_obsidian_blackboard.jsonl` on that day
- top changed files from DuckDB `file_system` in the repo-root window
- files whose *names* contain date tokens (`YYYY-MM-DD` or `YYYY_MM_DD`)

## Monthly rollups (Gold)

- Monthly:
  - `python3 scripts/hfo_rollup_generate.py monthly --month 2026-01`
  - Output: `hfo_hot_obsidian/gold/3_resources/reports/rollups/monthly/ROLLUP_2026_01.md`

Then:

- Generate daily rollups for the busiest days.
- Edit the monthly rollup to link the most important daily rollups and promote key reports/specs.

## Next hardening steps (if you want)

1) Expand DuckDB event journaling

- Write `status_update` entries into `main.mission_journal` as well as JSONL.
- Benefit: single-query daily summaries without scanning JSONL.

1) Add “promotion receipts”

- When promoting a Bronze report/spec to Silver/Gold, write a small receipt that records:
  - source path + hash
  - promoted path
  - date + rationale

1) Add a daily cron/daemon hook

- Run daily rollup at end-of-day and commit the markdown into Git for cheap SSOT.
