# Medallion: Bronze | Mutation: 0% | HIVE: V

# Port 0 (ISR) — HFO Hub Canonical 8 Tools (v2026.1.23)

## Goal

Make Port 0 ISR mostly-free, non-brittle, and fail-closed. The main failure mode we are eliminating is **silent regression** (keys not loaded, optional tools drifting in/out, flaky offline sources).

This version pins the workspace to **exactly 8 MCP servers** and treats everything else as optional/offline data sources, not part of the canonical toolchain.

## Canonical MCP Servers (8)

These are the only servers that should be enabled in `.vscode/mcp.json` for the default workflow.

These 8 MCP servers are the **Port 0 tool shards** (capabilities) the agent may invoke.

1) `filesystem` — read repo + artifacts deterministically
2) `memory` — append/read MCP working-memory JSONL
3) `sequential-thinking` — required reasoning protocol
4) `time` — stable timestamps for receipts/reports
5) `tavily` — paid web search (high-recall external ISR)
6) `brave-search` — free web search (baseline external ISR)
7) `playwright` — UI parity + Omega probes (when needed)
8) `hfo_mcp_gateway_hub` — gateway tool shard: Port 6 memory consolidation + stigmergy tail access

## Entryway (Not a Tool Shard)

The **entryway** is the pointer SSOT + hub routing layer:

- `hfo_pointers.json` — stable SSOT for targets/versions/paths
- `hfo_hub.py` — stable entrypoint that routes to the pinned implementations

Removed from canonical set:

- `omnisearch` (optional)
- `context7` (optional)

## ISR Battery (Port 0)

### Free-first ISR

- **Local evidence (free):** use `filesystem` + `hfo_mcp_gateway_hub` to read:
  - stigmergy blackboard tail
  - MCP memory tail
  - DuckDB SSOT pointers (when available)
- **External evidence (free):** use `brave-search` probes for quick confirmation.

### Paid ISR escalation

- Use `tavily` when free search is insufficient or low-confidence (e.g., precise citations, broader recall).

### Offline wiki (optional data source)

Offline wiki can remain part of ISR as a *data source* (not a tool/server), ideally accessed via gateway hub tooling when configured.
If `offline_wiki_path` is missing, ISR still functions; it just degrades gracefully to local artifacts + Brave/Tavily.

## Anti-Regression Controls

- **Tracer venom (P3) strict drift check**: fails if MCP server inventory drifts from the 8 tool shards.
  - Run: `python3 hfo_hub.py p3 tracer`
- **P0 ISR suite (read-only invariant)**: generates a report and asserts no repo changes outside the report path.
  - Run: `python3 hfo_hub.py p0 suite`
- **Pointer SSOT**: `hfo_pointers.json` is the hub’s canonical gate for versions/targets/paths.

## Operational Notes

- The MCP servers for Tavily/Brave must inherit `.env` reliably; the workspace uses `scripts/mcp_env_wrap.sh` for that purpose.
- If you need optional tools (Context7/Omnisearch), enable them explicitly as a separate “optional profile” rather than diluting the default 8-tool baseline.
