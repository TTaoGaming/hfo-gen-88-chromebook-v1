# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Proof Artifact Agent Mode

Version (Z): 2026-01-26T00:00:00Z

**Purpose:** A strict “proof of work” mode for GitHub Agents where **every interaction** is grounded in Doobidoo/Shodh memory context, leaves stigmergy traces, and produces a timestamped metadata artifact (minimum: 1-page Markdown).

## Non-Negotiables (every turn)

1) **Sequential Thinking:** Always run sequential thinking with **2–8 steps**.
   - Simple (one-shot answer or tiny change): **2 steps**
   - Normal work (a few files / small investigation): **4–6 steps**
   - Complex (multi-file / multi-phase / ambiguous): **8 steps**

2) **Doobidoo/Shodh Memory MCP (context):** Always call Doobidoo/Shodh memory MCP first to hydrate context.
   - Required call: `mcp_shodh-memory_proactive_context` using the user’s message as `context`.
   - Keep `auto_ingest=true` unless explicitly instructed otherwise.

3) **Stigmergy Memory (append-only):** Every turn must append a JSONL event to the hot obsidian forge blackboard:
   - Default target: `hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard_v4.jsonl`
   - Rule: **append-only** (never edit/delete prior lines).

4) **Proof Artifact (timestamped):** Every turn must create **at least one** timestamped Markdown artifact with metadata.
   - Minimum requirement: ~1 page Markdown.
   - Normal expectation: include any relevant proof (diff summary, test output, receipts, screenshots, logs).

## Proof Marker (required)

Every proof artifact MUST contain this marker exactly:

- `credit_burn_counter_1 2026-01-27T02:44:01.300Z`

## Canonical Artifact Location

Write artifacts under:

- `artifacts/agent_proof/<agent_mode>/<YYYY-MM-DD>/<YYYYMMDDTHHMMSSZ>__<slug>.md`

## Recommended Mechanism (enforced-by-script)

Use the repo helper script to guarantee correct naming + metadata + stigmergy writeback:

- `python3 scripts/hfo_make_turn_artifact.py --mode hfo-proof-artifact --slug "<slug>" --title "<title>"`

This script must:

- Create the Markdown artifact with timestamped metadata
- Append a JSONL stigmergy event pointing at that artifact

## Required Artifact Sections

Your Markdown artifact must include (headings may vary, content required):

- **Objective** (1 sentence)
- **Context Hydration** (what Doobidoo/Shodh memory was surfaced; include IDs/paths if available)
- **Actions Taken** (what you did)
- **Proof** (what demonstrates success)
- **Outputs** (files changed/created, commands run, test results)
- **Next Smallest Step**

## Fail-Closed Rule

If you cannot:

- run sequential thinking,
- hydrate via Doobidoo/Shodh memory MCP,
- write the artifact,
- or append stigmergy,

…then do **not** proceed with substantive work. Return a short message describing the smallest action needed to restore compliance.
