# Medallion: Bronze | Mutation: 0% | HIVE: V

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
   - Example: a folder of `.md` notes, JSON, exported wiki pages, etc.
3) Use the gateway tool `offline_wiki_search`.

## Configuration: `OFFLINE_WIKI_PATH`

- Required env var (fail-closed): `OFFLINE_WIKI_PATH`.
- If missing, the gateway returns an explicit error: `OFFLINE_WIKI_PATH not set in environment.`

**Recommended structure under `OFFLINE_WIKI_PATH`:**

- `*.md` notes and playbooks
- `*.json` manifests
- Exported wiki dumps (text)

## Troubleshooting

### Symptom: offline wiki returns an env-var error

- Confirm `OFFLINE_WIKI_PATH` is set in the environment that runs the gateway.
- Confirm the path exists and is readable.

### Symptom: “ripgrep (rg) not found on PATH.”

- Install ripgrep.

### Symptom: returns empty results

- Confirm your offline corpus contains the search terms.
- Increase limit.

## Operational Pattern (Fallback Ladder)

1) `offline_wiki_search` (local corpus)
2) `wikipedia_search` (online; Wikipedia API)
3) `duck_search` (DuckDB file index)
4) web search (Tavily/Brave)

## Notes / Guardrails

- Keep the offline corpus non-secret unless you explicitly control the machine/storage.
- Prefer adding *your own* curated notes rather than copying large third-party corpora into the repo.

---
*Spider Sovereign | Playbook-OfflineWiki-01*
