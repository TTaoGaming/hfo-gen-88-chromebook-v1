# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO MCP Stack Standardization — 2026-01-18

## Purpose

Standardize the MCP stack for HFO (Mission Thread Alpha/Omega) and identify exemplar servers to adopt. This artifact is intended for **Hot Bronze** stabilization and to reduce tool drift.

---

## Current Verified Stack (from workspace config)

Source: [.vscode/mcp.json](../../../.vscode/mcp.json)

- filesystem
- memory
- sequential-thinking
- time
- tavily
- brave-search

**Note:** Additional MCP servers may be enabled via the Copilot UI (not visible from repo state). Those must be reviewed manually in the UI to align with this standard.

---

## Standardized HFO Stack (Minimal + Evidence)

### Core (must‑have)

- filesystem
- memory
- sequential-thinking
- time

### Evidence & Search (recommended)

- tavily
- brave-search

### Optional (Omega testing)

- microsoft/playwright-mcp

---

## Exemplar Adopts (Curated)

Source: <https://github.com/wong2/awesome-mcp-servers>

**Adopt for standardization (high signal, low bloat):**

1) **Git MCP** — <https://github.com/modelcontextprotocol/servers/tree/main/src/git>
   - Adds commit/diff anchors for monthly rollups.
2) **Fetch MCP** — <https://github.com/modelcontextprotocol/servers/tree/main/src/fetch>
   - Deterministic web content ingestion for evidence.
3) **1mcpserver** — <https://github.com/particlefuture/1mcpserver>
   - Standard registry/discovery; helps eliminate hidden tool drift.
4) **AgentQL MCP** — <https://github.com/tinyfish-io/agentql-mcp>
   - Structured web extraction for Alpha evidence and Omega assets.

**Optional upgrades (only if needed):**

- **Apify Actors MCP** — <https://github.com/apify/actors-mcp-server> (industrial web extraction)
- **Atla MCP** — <https://github.com/atla-ai/atla-mcp-server> (rollup evaluation/QA)

---

## Recommendation: Stop Suboptimal Tooling

- **Freeze** to the Standardized HFO Stack above.
- **Disable** UI‑enabled MCP tools not in this list until reviewed.
- **Pin** versions after adoption to prevent drift.

---

## Next Actions

1) Confirm Copilot UI MCP list and disable non‑standard tools.
2) Add Git/Fetch/1mcpserver/AgentQL MCPs if you want a hardened standard.
3) Pin versions in `.vscode/mcp.json` after adoption.

*HFO Hot Bronze — Port 6 Kraken Keeper / Stack Standardization*
