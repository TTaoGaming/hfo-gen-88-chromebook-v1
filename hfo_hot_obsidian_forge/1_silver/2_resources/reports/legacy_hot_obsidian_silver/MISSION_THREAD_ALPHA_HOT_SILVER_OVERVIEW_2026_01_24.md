# Medallion: Silver | Mutation: 0% | HIVE: V

## Mission Thread Alpha — Hot/Silver Overview (Infrastructure)

Date: 2026-01-24

## Definition (SSOT)

Alpha is the infrastructure thread.

- Scope rule: **Infrastructure == Alpha. Product/gesture/UI payload == Omega. If ambiguous, treat as Alpha.**
  - Source: `hfo_hot_obsidian/bronze/3_resources/para/mission_thread_alpha_current/specs/hfo_alpha_hub_spec_v2026_01_24.yaml`

Alpha and Omega are one continuous mission timeline; they are separated for safety and clarity, not because they are unrelated.

- Source: `AGENTS.md`

## Primary Entry Surfaces (Blessed)

- Root shim: `hfo_hub.py`
  - Delegates to the current Alpha gateway implementation via `HFO_HUB_TARGET` and `hfo_pointers`.
  - Source: `hfo_hub.py`
- Direct gateway shim: `hfo_mcp_gateway_hub.py`
  - Source: repo root
- Current Alpha gateway implementation:
  - `hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py`
  - Source: `hfo_hub.py` (DEFAULT_TARGET)

## What Alpha Produces

Alpha produces things that make the swarm safer and less fragile:

- Contracts and schema boundaries (`contracts/`)
- Receipts, integrity checks, and fail-close gates
- System-aware wrappers and automation guardrails (pareto/low-RAM governance)
- Audit-grade observability (append-only blackboard events + correlated invoke/result)

Sources:

- `hfo_hot_obsidian/bronze/3_resources/para/mission_thread_alpha_current/specs/hfo_alpha_hub_spec_v2026_01_24.yaml`
- `hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/README.md`

## Invariants (Alpha Contract)

From the Alpha spec:

- **Blessed entry surface**: critical actions flow through hub/gateway (no ad-hoc scripts without receipts)
- **Fail-close boundaries**: missing contracts/receipts must block progress
- **Append-only audit bus**: hot blackboard JSONL is the audit trail
- **Observability by default**: every wrapper invocation emits invoke+result events

Audit bus:

- File: `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl`
- Envelope: CloudEvents-ish with tracing fields

Source: `hfo_hot_obsidian/bronze/3_resources/para/mission_thread_alpha_current/specs/hfo_alpha_hub_spec_v2026_01_24.yaml`

## Interfaces (Ports as the Swarm Safety Boundary)

Alpha encodes the port doctrine as the anti-coupling rule:

- P0 Observe — sensing/search/context retrieval
- P1 Bridge/Fuse — schema/contract bridge + routing
- P5 Immunize/Defend — audits and integrity gates
- P6 Assimilate — storage/rollups
- P7 Navigate — orchestration + sequential reasoning

Port 7 Hot/Silver resources:

- `hfo_hot_obsidian/silver/3_resources/reports/P7_SPIDER_SOVEREIGN_SHARD_FRAMEWORK_V0_1_2026_01_25.md`

Port 6 Hot/Silver resources:

- `hfo_hot_obsidian/silver/3_resources/reports/PORT6_KRAKEN_KEEPER_SCATTER_GATHER_CONTEXT_CAPSULE_V0_1_2026_01_25.md`

Archetype mapping (operational shorthand):

- Port 6 (Kraken Keeper): builds and stores checkable capsules + receipts.
- Port 7 (Lady of the Lake): surfaces the “right” capsule/receipts at the moment of decision.

Source: `hfo_hot_obsidian/bronze/3_resources/para/mission_thread_alpha_current/specs/hfo_alpha_hub_spec_v2026_01_24.yaml`

## What’s Working (Recent Evidence)

Patterns that correlate with stability and forward motion (from recent MCP memory entries):

- Safe runner + proof bundles (pre/post snapshots + enforced low-RAM settings)
- Hub wrappers that emit correlated invoke/result to blackboard
- P1 DataFabric snapshots used as a shared diagnostic substrate

Sources (via MCP memory rollups):

- `scripts/hfo_playwright_safe_run.py`
- `hfo_ports/p1_data_fabric.py`
- `hfo_hub.py`

## Critical Gaps (Alpha)

- A universal lineage envelope is not yet a first-class contract (needed to make FORK_AND_EVOLVE automatic).
- Promotion to Silver is not yet uniformly gated by contract validation + deterministic proof artifact.
- Some "archive vs active" drift still happens without explicit lineage pointers.

## Next Actions (Alpha)

1) Extend `contracts/hfo_data_fabric.zod.ts` with a lineage envelope (artifact_id, parents, intent, compat, promotion).
2) Add a blessed Alpha command to fork-and-register artifacts (writes lineage + updates stable pointers fail-closed).
3) Tie Silver promotion to minimum proof:
   - a contract validation check, and
   - at least one deterministic test/proof artifact or P5 audit PASS.
