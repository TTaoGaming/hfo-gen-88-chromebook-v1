# Medallion: Bronze | Mutation: 0% | HIVE: V

# Port 6 (Kraken Keeper) — Memory System Interface

## Purpose

Provide a single, stable interface for the three memory shards used by HFO. Port 6 must consolidate and return evidence across all shards without cross-port coupling.

## Memory Shards (3)

1) MCP memory graph (working memory JSONL)
2) Obsidian blackboards (stigmergy JSONL)
3) DuckDB unified Gen88 (long-term SSOT)

## Gateway Hub Tools

- `memory_status`: health/paths for the three shards
- `read_blackboard_tail`: short-term blackboard tail
- `list_mcp_memory` / `append_mcp_memory`: working memory graph
- `query_journal`: DuckDB mission journal (long-term)
- `port6_assimilate`: consolidated payload across all shards

## Recommended Call

Use `port6_assimilate` as the default Port 6 entrypoint.

### Inputs

- `blackboard_tail` (int, default 10)
- `mcp_memory_tail` (int, default 20)
- `include_serena_list` (bool, default true)

### Output

A consolidated JSON payload containing:

- `short_term_blackboard`: tail + file info
- `working_memory_mcp`: tail + file info
- `serena_memory`: directory info + list (if requested)
- `long_term_duckdb`: file info

## Decoupling Rules

- No direct read/write across ports without explicit tool boundaries.
- Memory systems are read-only unless the tool explicitly permits write (e.g., `append_mcp_memory`).
- Every Port 6 output must be safe to consume by any agent without leaking implementation detail.
