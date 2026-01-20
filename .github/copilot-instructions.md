# Medallion: Bronze | Mutation: 0% | HIVE: V
# 🧭 HFO Gen 88: AI Agent Steering & Governance

## 🏗️ Core Architecture: The Medallion Flow

All development must follow the **Medallion Refinement Flow**. Do not bypass layers.

1. **Bronze (Incubation)**: Experimental code, raw logic. Always start here.
2. **Silver (Integration)**: Verified code. Requires passing property tests and contract validation.
3. **Gold (Hardened)**: Automated mission engineering ready. Pareto optimal.

## 📏 Testing & The HFO Goldilocks Zone

We prioritize **Mutation Scoring** (Stryker) over simple line coverage. HFO operates best within the Pareto Goldilocks range.

- **Pareto Optimal**: 88% (matches 7/8 cognitive shards / 87.5%).
- **Target Zone**: 80% - 99% mutation score.
- **Reject**: < 80% (Under-tested/Needs evolution).
- **Warning**: 100% (Possible "AI Theater" or trivial tests/over-fitted).

## 🛡️ Coding Patterns

- **Zod 6.0 Contracts**: Use Zod for all cross-port (P0-P7) communication. Define schemas in `contracts/` directories.
- **Stigmergy Signals**: Use `.jsonl` blackboards for indirect coordination between ports.
- **Immutable Provenance**: Every file should have a provenance header including its Medallion layer and mutation score.

## 🧠 Memory MCP Protocol (Required)

Make Memory MCP a first-class workflow step for every task:

1) **Start of task**: read the last MCP memory tail and confirm alignment with current work.
2) **End of task**: append a short `status_update` entry with:
 - Summary of changes
 - Tests run
 - Short/long-term goals
 - Source links (workspace-relative)

This is mandatory for cognitive persistence and to prevent repeated regressions.

## 🔗 File Linking & Context

- Always use workspace-relative markdown links for file references.
- Reference **AGENTS.md** for high-level mission context.
- Consult [.github/agents/HFO-Hive8.agent.md](.github/agents/HFO-Hive8.agent.md) for mandatory agent workflows.
- Consult **hfo_cold_obsidian** for hardened code samples and verified schemas.

## 🤖 Commander Port Mapping

- **P0 SENSE**: MediaPipe/Python source logic.
- **P1 FUSE**: Schema bridge/TypeScript stabilization.
- **P2 SHAPE**: Physics/Rapier Wasm integration.
- **P3 DELIVER**: W3C Event dispatch/FSM.
- **P4 DISRUPT**: Feedback loops/Suppression.
- **P5 DEFEND**: Integrity checks/Resurrection.
- **P6 STORE**: DuckDB telemetry.
- **P7 NAVIGATE**: Orchestration/Knowledge management.

---
*Spider Sovereign (Port 7) | Gen 88 Guidance*
