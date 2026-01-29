# Medallion: Bronze | Mutation: 0% | HIVE: V

# S3 Turn Artifact (v2.1) — Best MCP Servers (2026)

Date (UTC): 2026-01-27

Proof marker: credit_burn_counter_1 2026-01-27T02:44:01.300Z

## Objective

Identify a minimal, high-leverage MCP server set for 2026 HFO work, grounded in this repo’s existing agent modes.

## Facts (proven in repo)

- HFO already defines an “Always-Use MCP Servers” baseline list in `.github/agents/hfo-basic-mcp.agent.md`.
- Port 7 mode requires filesystem/memory/sequential-thinking/time and writes one S3 artifact per user question in `hfo_hot_obsidian/bronze/3_resources/para/areas/sensemaking/s3_protocol_turns/`.
- Port 6 mode is designed for deterministic, auditable assimilation and emphasizes bounded memory hydration and receipts.

## Hypotheses (unproven / contextual)

- “Best” depends on whether the operator is doing repo-first engineering vs web research vs UI parity testing.
- Adding more MCP servers increases capability but also increases failure surface; keep a small default set.

## Recommended MCP server set (HFO practical)

Core (always):

- filesystem
- memory
- sequential-thinking
- time

Research (when needed):

- tavily
- brave-search

UI parity (when needed):

- playwright

## Sources

- `.github/agents/hfo-basic-mcp.agent.md`
- `.github/agents/hfo-port7-spider-sovereign.agent.md`
- `.github/agents/hfo-port6-kraken-keeper.agent.md`

## Next smallest step

Decide the default profile:

- “Core only” (repo-first coding), or
- “Core + Research” (facts gathering), or
- “Core + UI parity” (Omega testing)
