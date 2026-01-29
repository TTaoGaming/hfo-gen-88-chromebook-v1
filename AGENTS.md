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

## Memory Stack (Port 6: Kraken Keeper)

Gen88 v4 consolidates around a **single write-path SSOT**:

1) doobidoo (`mcp-memory-service`) sqlite_vec SSOT (blessed write path)
2) Obsidian blackboards (stigmergy/telemetry JSONL; coordination + receipts)
3) Derived views (rebuildable from SSOT): Shodh index, DuckDB exports/analytics, legacy JSONL caches

Use `port6_assimilate` in the gateway hub to consolidate the operational tails (telemetry + any enabled legacy caches) in one call.

## Rollup Reference

Full historical context is archived at:

- hfo_cold_obsidian/bronze/3_resources/reports/AGENTS_ROLLUP_2026_01_18.md

## GitHub Agent Modes

See the agent mode index at `.github/agents/README.md`.

- Recommended proof-first mode: `.github/agents/hfo-proof-artifact.agent.md` (always emits a timestamped proof artifact + stigmergy)

## HFO LifeOS Vault (8 Areas + PARA)

Consolidation target: a lean Obsidian vault for an 8-part HFO LifeOS energy/task system.

Structure:

- 00-inbox, 01-projects, 02-areas (8 areas), 03-resources (templates), 04-archive (short stubs only)

Area mapping (snake_case):

- p0_health, p1_work, p2_learning, p3_admin, p4_money, p5_home, p6_people, p7_play_meaning

Templates live in:

- /mnt/chromeos/GoogleDrive/MyDrive/Obsidian2025/03-resources

Vault location (authoritative):

- /mnt/chromeos/GoogleDrive/MyDrive/Obsidian2025

Symlink note:

- A workspace symlink named Obsidian2025 exists at repo root for local use, but some agents cannot follow symlinks. When interacting with the vault, prefer the absolute Drive path above.
