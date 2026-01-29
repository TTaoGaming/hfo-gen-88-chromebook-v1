# Medallion: Silver | Mutation: 0% | HIVE: V

# P7 “Spider Sovereign” — Analysis Adapter Spec (Hub + SSOT + Stigmergy)

Date: 2026-01-25

## Verbatim Request (Anchor)

> “formalize this kind of analysis with the hfo hub create an adapter for port 7 navigate - Spider Sovereign… use repo, database, stigmergy… report lack of coverage… port 7 should orchestrate the other 7 hfo ports… add in port 3 injector - harmonic hydra tracer_venom variants and have port 0 observer - lidless legion watch it and give a report to port 7 again… JADC2 mosaic team… HIVE/8… obsidian hourglass:HIVE/8… bootstrap… HIVE/8:1010… target 8787+7676+6565+5454+4343+3232+2121+1010… focus on markdowns for now…”

> “please do that, please log my exact wording to the silver documents and mcp memory… note down the important terminology.”

## Executive Summary

This spec formalizes **Port 7 (P7 NAVIGATE)** as **Spider Sovereign**: the orchestrator that produces **evidence-backed analysis** and **coverage-gap reports** by fusing:

- **Repo SSOT** (files + contracts)
- **Database SSOT** (DuckDB)
- **Stigmergy** (append-only JSONL blackboards + MCP memory)

P7 is not a “new monolith.” It is the commander that issues **bounded directives** to other ports and aggregates proof into artifacts (Markdown reports + receipts).

## Grounding: Existing Anchors in the Repo

These already exist and should be treated as “real wires” the spec binds to:

- P7 role definition in hub vision text: [hfo_hub.py](../../../../hfo_hub.py)
  - “P7 NAVIGATE — mission orchestration + parameter hot-swap + intent manifests”
- P0 → P7 handoff/receipt pattern exists in the Alpha gateway hub: [hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py](../../../../hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py)
  - Tool `p0_observe_compile` emits a **Phase-1 H baton** “from P0 to P7” and logs HANDOFF.
- Port 0 “strict baton” concept exists as a CLI facade: [hfo_ports/p0_context_facade_v2.py](../../../../hfo_ports/p0_context_facade_v2.py)
- Port 3 tracer_venom exists and already inventories MCP servers / keys and can alias into P1 DataFabric: [hfo_ports/p3_tracer_venom.py](../../../../hfo_ports/p3_tracer_venom.py)
- Contract boundary is explicit: [contracts/](../../../../contracts)

## Terminology (Canonical)

- **Spider Sovereign** = P7 Navigate (orchestrator / commander / report generator)
- **Lidless Legion** = P0 Observe/Sense (evidence gatherer / recon)
- **Harmonic Hydra** = P3 Deliver/Inject tracer variants (active probes + injection surface)
- **Stigmergy** = append-only JSONL coordination substrate (blackboards + receipts)
- **HIVE/8** = the 8-phase operational workflow (Obsidian Hourglass)
- **JADC2 mosaic team** = composable tiles (ports) orchestrated by P7

## Adapter Boundaries

### Inputs (P7 reads)

- Repo state (files + contracts)
  - Required: [contracts/](../../../../contracts)
  - Optional: `hfo_pointers.json`, `playwright.config.ts`, `scripts/` audit scripts
- DuckDB SSOT (telemetry and indexes)
- Stigmergy logs (append-only)
  - MCP memory: `hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl`
  - Hot blackboard: `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl`

### Outputs (P7 writes)

- **Silver reports** (Markdown) into `hfo_hot_obsidian/silver/3_resources/reports/`
- **Receipts + handoff batons** into the blackboard/memory substrate (append-only)
- **Coverage-gap ledger** as a stable report artifact (month-anchored)

## Coverage (Definition of “Lack of Coverage”)

Coverage is multi-dimensional; P7 should report “lack of coverage” as a vector, not a single number:

1) **Spec coverage**: for each contract/spec file, is there (a) an owning port, (b) tests/harness, (c) a known pointer action?
2) **Telemetry coverage**: do key port actions emit receipts and appear in blackboard/DuckDB?
3) **Regression coverage**: do we have deterministic, fail-closed tests for critical entrypoints?
4) **Interface coverage**: are Alpha↔Omega shared surfaces mapped and enforced by contracts?

## Orchestration Pattern (P7 as Commander)

P7 should operate as a **bounded loop**:

1) Pull evidence (repo + DuckDB + stigmergy)
2) Produce a coverage-gap report (Silver)
3) Emit a minimal directive to one port (P0/P3/P5 are typical)
4) Validate results (proof artifact + receipt)
5) Write back to stigmergy (status_update + blackboard)

This retains **FORK_AND_EVOLVE** posture: reports and proofs are additive artifacts, not rewrites.

## Minimal “Adapter Contract” (Doc-First)

Before introducing new schemas, the adapter contract for P7 can be stabilized as Markdown invariants:

- Every P7 run emits:
  - A report path
  - A list of sources (file paths + log artifacts)
  - A list of next actions (bounded, port-scoped)
- Every next action references:
  - A port owner (P0–P7)
  - A proof expectation (receipt, JSON artifact, or test command)

Future step (not implemented here): formalize this into a Zod schema under `contracts/`.

## Related Specs

- Loop spec: [hfo_hot_obsidian/silver/3_resources/reports/P0_P3_P7_LIDLESS_LEGION_HARMONIC_HYDRA_LOOP_2026_01_25.md](P0_P3_P7_LIDLESS_LEGION_HARMONIC_HYDRA_LOOP_2026_01_25.md)
- HIVE/8 ladder: [hfo_hot_obsidian/silver/3_resources/reports/HIVE8_OBSIDIAN_HOURGLASS_BOOTSTRAP_LADDER_2026_01_25.md](HIVE8_OBSIDIAN_HOURGLASS_BOOTSTRAP_LADDER_2026_01_25.md)
