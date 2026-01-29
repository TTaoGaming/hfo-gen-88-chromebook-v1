# Medallion: Silver | Mutation: 0% | HIVE: V

# Gen88 v4: Doobidoo SQLite SSOT Setup

## Goal

Make doobidoo (MCP `mcp-memory-service`) backed by `sqlite_vec` the **single write-path SSOT**. All other memory systems are disabled for writes (and treated as legacy/read-only snapshots).

## Canonical SSOT Location

- SQLite file: `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`
- Base dir: `artifacts/mcp_memory_service/gen88_v4/`

These are wired in:

- `.vscode/mcp.json` (`mcp-memory-service` env)
- `.env` (mirrors the same values)

## Current Quality Mode (Pareto)

- Enabled: **ONNX embeddings** (PyTorch-free) via `MCP_MEMORY_USE_ONNX=1`.
- Not enabled (optional): local ONNX ranker (requires `transformers` + `torch`, heavy).

## Safety Policy

- SSOT writes: only via doobidoo MCP tool `store_memory`.
- Legacy memory MCP servers are disabled via `.env`:
  - `HFO_MCP_ENABLE_MEMORY=0`
  - `HFO_MCP_ENABLE_SHODH_MEMORY=0`

## Derived View: Shodh (Hebbian Index)

Shodh runs as a **derived, rebuildable view** on top of the sqlite SSOT. It should not be treated as the write-path truth.

- Backend: start separately via `scripts/shodh_memory_server.sh` (Docker).
- Sync SSOT → Shodh (idempotent): `scripts/shodh_sync_from_doobidoo_ssot.py` uses Shodh `/api/upsert` with `external_id = doobidoo:<content_hash>`.

### Runbook

- Dry-run:
  - `./.venv/bin/python scripts/shodh_sync_from_doobidoo_ssot.py --dry-run`
- Real sync:
  - `./.venv/bin/python scripts/shodh_sync_from_doobidoo_ssot.py`

Required env:

- `MCP_MEMORY_SQLITE_PATH` (doobidoo SSOT sqlite file)
- `SHODH_API_KEY` (used as HTTP header `X-API-Key`)
- `SHODH_HOST` / `SHODH_PORT` (defaults: `127.0.0.1:3030`)

Optional env:

- `SHODH_USER_ID` (defaults: `hfo_gen88_v4`)
- `HFO_SHODH_SYNC_STATE` (defaults: `artifacts/shodh_memory/sync_state_doobidoo_gen88_v4.json`)

## Backup Checklist

- Stop the MCP server (or ensure no writes in-flight), then copy the sqlite file.
- Keep timestamped copies under `artifacts/mcp_memory_service/gen88_v4/backups/` (recommended).

## Next Improvements (Suggested)

1. Add an exporter: sqlite → JSONL receipts and sqlite → DuckDB tables.
2. Add a scheduled backup task.
3. (Optional) Install the heavy ranker dependencies if you want better ordering:
   - `pip install transformers torch`
