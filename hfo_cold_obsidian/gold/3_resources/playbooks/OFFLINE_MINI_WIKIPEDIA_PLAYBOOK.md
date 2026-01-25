# Medallion: Gold | Mutation: 0% | HIVE: V

# 📚 Playbook: Offline Mini Wikipedia (Local Knowledge)

**Intent:** Provide a repeatable, offline-first “mini Wikipedia” capability for HFO ops: fast local lookup, searchable notes, and a predictable interface for agents.

---

## What This Playbook Covers

- How offline wiki search is implemented in this repo (gateway tool + `ripgrep`).
- How to configure `OFFLINE_WIKI_PATH` so the tool actually works.
- Operational patterns: fallback paths, logging, and troubleshooting.

## Repo Evidence (Grounded)

- Offline wiki tool implementation: `hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py` (`_offline_wiki_search`, `_rg_search`, `_tool_health_quick`).
- Blackboard evidence that “Local Wikipedia content retrieved” exists conceptually: `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl` (entries with `source: "RAG-Lite + ZIM"`, `zim_ready: true`).

## Quick Start

1) Ensure `ripgrep` is installed and on `PATH` (`rg`).
2) Set `OFFLINE_WIKI_PATH` to a directory of text/markdown/wiki artifacts you want indexed.
3) Use the gateway tool `offline_wiki_search`.

## Configuration: `OFFLINE_WIKI_PATH`

- Required env var (fail-closed): `OFFLINE_WIKI_PATH`.
- If missing, the gateway returns: `OFFLINE_WIKI_PATH not set in environment.`

## Troubleshooting

- `rg` missing → install ripgrep.
- Path missing/unreadable → fix permissions/path.
- Empty results → adjust query/limit; verify corpus contains terms.

## Operational Fallback Ladder

1) `offline_wiki_search` (local corpus)
2) `wikipedia_search` (online; Wikipedia API)
3) `duck_search` (DuckDB file index)
4) web search (Tavily/Brave)

---
*Spider Sovereign | Playbook-OfflineWiki-01*
