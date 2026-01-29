# Medallion: Silver | Mutation: 0% | HIVE: V

# P0↔P3↔P7 Feedback Loop — Lidless Legion × Harmonic Hydra × Spider Sovereign

Date: 2026-01-25

## Verbatim Request (Anchor)

> “add in port 3 injector - harmonic hydra tracer_venom variants and have port 0 observer - lidless legion watch it and give a report to port 7 again…”

## Goal

Define an **operational loop** where:

- **P3** runs controlled injection/tracer variants (active probe)
- **P0** observes outcomes and compiles evidence (recon)
- **P7** aggregates evidence and emits coverage-gap + next directives (commander)

This creates a repeatable “mosaic tile” pattern: probe → observe → report → steer.

## Grounded Primitives (What Exists Today)

### P0 (Observe) — Evidence Baton

- P0 strict baton facade emits a single JSON object (“baton”): [hfo_ports/p0_context_facade_v2.py](../../../../hfo_ports/p0_context_facade_v2.py)
- Alpha gateway hub can compile evidence and explicitly log P0→P7 handoff: [hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py](../../../../hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py)
  - Tool: `p0_observe_compile`

### P3 (Deliver/Inject) — tracer_venom + MCP integrity probe

- P3 tracer_venom inventories MCP servers/keys, and can alias IDE snapshot to P1 DataFabric: [hfo_ports/p3_tracer_venom.py](../../../../hfo_ports/p3_tracer_venom.py)

### P7 (Navigate) — Orchestrator role

- P7 is defined as orchestration + parameter hot-swap + intent manifests: [hfo_hub.py](../../../../hfo_hub.py)

## “Harmonic Hydra” Variants (Doc-First Interface)

Treat Harmonic Hydra as a family of P3 variants. Doc-first (no new code required yet):

- **Variant A: MCP Integrity Probe** (already present)
  - Runs P3 tracer inventory and key probes.
  - Output: pass/fail + drift list.
- **Variant B: Injection Harness Probe** (Omega-facing)
  - Drives a controlled input injection into Omega (Playwright-safe-run or W3C pointer injection), expecting an ack.
  - Output: proof artifact(s) + FAIL/CLOSE if not acked.
- **Variant C: Telemetry/Receipt Probe**
  - Confirms that the injection run emits receipts into blackboard + shows up in DuckDB.

## Loop Protocol (P0→P7)

### Step 1: P3 executes a variant

P3 emits:

- A proof artifact (e.g., JSON summary, Playwright safe run proof dir)
- A receipt/log trace (blackboard entry)

### Step 2: P0 observes and compiles

P0 emits a baton that includes:

- Summary (what happened)
- Evidence (URLs / file paths / proof artifacts)
- Risks (missing keys, drift, gaps)
- Next actions (bounded)
- `baton_to: P7`

Concrete anchor: the Alpha gateway tool `p0_observe_compile` explicitly formats a “Phase-1 H handoff baton for Port 7” and logs HANDOFF in blackboard: [hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py](../../../../hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py)

### Step 3: P7 writes the commander report

P7 writes a Silver report that answers:

- What was attempted (variant)
- What proof exists (links)
- What failed-closed (if any)
- What coverage gap was discovered
- What directive to issue next (single-port or dual-port)

## Coverage-Gap Output Format (Suggested)

P7 should publish the loop result in a stable table:

- Probe name / variant
- Target surface (Omega entrypoint, MCP server, contract)
- Expected ack / invariants
- Proof link(s)
- Status: PASS / FAIL / UNKNOWN
- Remediation owner port (P0–P7)

## Failure Handling (Fail-Closed)

If any probe cannot produce proof or receipt correlation, classify as **UNKNOWN** and treat as “coverage gap,” not as success.

## Related Specs

- P7 adapter spec: [hfo_hot_obsidian/silver/3_resources/reports/P7_SPIDER_SOVEREIGN_ANALYSIS_ADAPTER_SPEC_2026_01_25.md](P7_SPIDER_SOVEREIGN_ANALYSIS_ADAPTER_SPEC_2026_01_25.md)
- HIVE/8 ladder: [hfo_hot_obsidian/silver/3_resources/reports/HIVE8_OBSIDIAN_HOURGLASS_BOOTSTRAP_LADDER_2026_01_25.md](HIVE8_OBSIDIAN_HOURGLASS_BOOTSTRAP_LADDER_2026_01_25.md)
