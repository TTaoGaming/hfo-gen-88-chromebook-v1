# Medallion: Bronze | Mutation: 0% | HIVE: V

# P0 ISR Suite Report (Lidless Legion) — 2026-01-23T17_26_10.417982Z

**Suite version:** 2026-01-23T17:15:20Z

## Goals

- Verify P0 is observation-only (read-only operations + allowed report write).

- Verify the 8-shard observation toolchain health via tracer_venom.

## Tracer Venom Results

### Strict mode (exactly-8 invariant)

Exit: 0


```
[HFO HUB] P3 tracer: MCP server inventory
  canonical_expected=8 present=8 missing=0
[HFO HUB] P3 tracer: key presence
  TAVILY_API_KEY=OK
  OPENROUTER_API_KEY=OK
  BRAVE_API_KEY=OK
[HFO HUB] P3 tracer: live probes
  tavily: OK (HTTP 200)
  openrouter: OK (HTTP 200)
  brave-search: OK (HTTP 200)
[HFO HUB] P3 tracer: OK (venom=0.1.0)
```

### Allowed-optional mode (HFO_ALLOW_OPTIONAL_MCP=1)

Exit: 0


```
[HFO HUB] P3 tracer: MCP server inventory
  canonical_expected=8 present=8 missing=0
[HFO HUB] P3 tracer: key presence
  TAVILY_API_KEY=OK
  OPENROUTER_API_KEY=OK
  BRAVE_API_KEY=OK
[HFO HUB] P3 tracer: live probes
  tavily: OK (HTTP 200)
  openrouter: OK (HTTP 200)
  brave-search: OK (HTTP 200)
[HFO HUB] P3 tracer: OK (venom=0.1.0)
```

## Read-Only Invariant Check

This suite only performs reads and network probes, then writes this report file.

### Git status before

```
M .github/agents/hfo-basic-mcp.agent.md
M .gitops/batches.json
M .vscode/tasks.json
M ai-chat-omega-gen6-2026-1-20.md
M contracts/hfo_data_fabric.zod.ts
M hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py
M hfo_hot_obsidian/bronze/3_resources/fixtures/golden/gen6_v12_touch2d_split_top_bottom_commit_crossing_golden.json
M hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/GEN6_V12_TRIPWIRE_THREAD_PLANCK_BABYLON_SPEC_2026_01_21.yaml
M hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v12.html
M hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/architecture/ports/versions/base.py
M hfo_hub.py
M hfo_mcp_gateway_hub.py
M hfo_pointers.json
M package.json
M scripts/hfo_healthcheck.py
M scripts/p5_sentinel_daemon.py
```

### Git status after

```
M .github/agents/hfo-basic-mcp.agent.md
M .gitops/batches.json
M .vscode/tasks.json
M ai-chat-omega-gen6-2026-1-20.md
M contracts/hfo_data_fabric.zod.ts
M hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py
M hfo_hot_obsidian/bronze/3_resources/fixtures/golden/gen6_v12_touch2d_split_top_bottom_commit_crossing_golden.json
M hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/GEN6_V12_TRIPWIRE_THREAD_PLANCK_BABYLON_SPEC_2026_01_21.yaml
M hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v12.html
M hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/architecture/ports/versions/base.py
M hfo_hub.py
M hfo_mcp_gateway_hub.py
M hfo_pointers.json
M package.json
M scripts/hfo_healthcheck.py
M scripts/p5_sentinel_daemon.py
```

### Invariant: OK

No new changes detected outside allowed report paths.
