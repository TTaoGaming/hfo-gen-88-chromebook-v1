# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Agent Context (Short)

## Mission Continuity (Alias Truth)
Alpha (MCP Gateway Hub) and Omega (Gen4 Pointer Stack) are a single continuous mission across 2025–present, evolving under different aliases.

## Strict Interfaces + Decoupling (Swarm Safety)
- All ports and hubs must expose strict interfaces and fail-closed boundaries.
- No hidden cross-port coupling. All cross-port data must pass explicit schemas/contracts.
- Anti-fragile posture: any single agent failure must not crash the system.

## Root Hub Shim (Stable Entry)
- Root hub entrypoint: hfo_mcp_gateway_hub.py delegates to the current Alpha project implementation.
- This keeps alias/version changes isolated behind a stable root interface.

## Rollup Reference
Full historical context is archived at:
- hfo_cold_obsidian/bronze/3_resources/reports/AGENTS_ROLLUP_2026_01_18.md
