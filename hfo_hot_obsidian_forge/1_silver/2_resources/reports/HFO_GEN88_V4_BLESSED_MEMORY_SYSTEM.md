# Medallion: Silver | Mutation: 0% | HIVE: V

# Gen88 v4: Blessed Memory System (SSOT)

## What Is “Blessed”

**Single write-path SSOT:** doobidoo MCP server `mcp-memory-service` backed by `sqlite_vec`.

- Writes: **ONLY** via `mcp-memory-service` → `store_memory`
- Reads: via `mcp-memory-service` → `retrieve_memory` (and related query/tag tools)
- Derived views (optional): Shodh is a rebuildable index fed from SSOT (never SSOT)

This keeps memory portable, auditable, and rebuildable.

## Consolidation Policy (Gen88 v4)

- SSOT (durable write-path): doobidoo sqlite_vec only.
- JSONL: allowed for **raw telemetry / stigmergy / receipts** (blackboards), not SSOT.
- Everything else: treated as **derived views** that can be rebuilt from sqlite (e.g. Shodh index, DuckDB exports/analytics, legacy JSONL caches).

## Canonical Locations (Pointer-Backed)

The canonical SSOT paths are pointer-resolved:

- `paths.mcp_memory_ssot_base_dir`
- `paths.mcp_memory_ssot_sqlite`

See the pointer file:

- [hfo_pointers.json](hfo_pointers.json)

## MCP Server Wiring

Workspace MCP config already wires the SSOT DB:

- [.vscode/mcp.json](.vscode/mcp.json) (`mcp-memory-service` env: `MCP_MEMORY_SQLITE_PATH`)

Recommended policy for new agents:

- Enable: `HFO_MCP_ENABLE_MCP_MEMORY_SERVICE=1`
- Disable legacy write paths:
  - `HFO_MCP_ENABLE_MEMORY=0` (JSONL memory)
  - `HFO_MCP_ENABLE_SHODH_MEMORY=0` (unless explicitly used as derived view)

## How To Use (New Agent Quickstart)

1) Ensure MCP memory service is enabled (env flag).
2) Store a memory:
   - tool: `mcp-memory-service.store_memory`
   - fields: `content` + `metadata.tags` (tags are critical for retrieval)
3) Retrieve:
   - tool: `mcp-memory-service.retrieve_memory` (use `n_results=5..20`)

Tag conventions (suggested):

- `gen88_v4`
- `ssot`
- `source:file:<workspace-relative-path>`
- `topic:<area>` (e.g. `topic:s3`, `topic:pointers`)

## Ingesting Files Into SSOT (Batch)

For bulk ingestion (markdown-first), use:

Example:
 Dry-run (default):

- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_ingest_markdown_dir.py --dir hfo_hot_obsidian/bronze/3_resources/para/areas/sensemaking/s3_protocol_turns --max-files 25 --tags gen88_v4 ssot topic:s3`
 Write to SSOT (explicit):
- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_ingest_markdown_dir.py --dir hfo_hot_obsidian/bronze/3_resources/para/areas/sensemaking/s3_protocol_turns --max-files 25 --tags gen88_v4 ssot topic:s3 --write`

Notes:

- `--max-files <= 0` means “no limit”.
- Large files are chunked (see `--chunk-chars`).
- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_memory_ingest_markdown_dir.py --dir hfo_hot_obsidian/bronze/3_resources/para/areas/sensemaking/s3_protocol_turns --tags gen88_v4 ssot topic:s3`

## Derived View: Shodh (Optional)

Shodh is treated as **derived, rebuildable**. The canonical sync script:

- [scripts/shodh_sync_from_doobidoo_ssot.py](scripts/shodh_sync_from_doobidoo_ssot.py)

Reference setup report:

- [hfo_hot_obsidian_forge/1_silver/2_resources/reports/HFO_GEN88_V4_DOOBIDOO_SSOT_SETUP.md](hfo_hot_obsidian_forge/1_silver/2_resources/reports/HFO_GEN88_V4_DOOBIDOO_SSOT_SETUP.md)

Pointer (derived view state):

- `paths.shodh_sync_state_gen88_v4`

## One-click Sync (VS Code)

Tasks (see [.vscode/tasks.json](.vscode/tasks.json)):

- `Memory: Sync SSOT → Shodh (Dry Run)`
- `Memory: Sync SSOT → Shodh`

## Operational Rules

- Commit code/docs and pointer updates frequently.
- Do **not** commit the SSOT sqlite DB (it lives under `artifacts/`). Back it up separately.
- Treat any other memory sinks as caches/exports unless explicitly promoted.
