<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->

# HFO — AI Agent Swarm: What They Do Not Respect vs What They Behaviorally Respect (V1, 2026-01-28)

## Purpose

This document is behavior-first. It ignores what an AI model *claims* to respect (e.g., “literate programming”), and instead catalogs what agent swarms reliably do in practice.

**Key premise:** in a tool-augmented environment, *wiring beats words*. If the environment permits multiple write paths, an agent swarm will behave as if multiple truths exist.

## Terms (behavioral)

- **Respect (behavioral):** a constraint or incentive that consistently shapes the agent’s actions.
- **Non-respect:** a human expectation that has no binding mechanism; agents may follow it only when convenient/in-context.
- **Enforcement theater:** doctrine exists in prose, but the environment still permits violations.

## What agents do NOT reliably respect (even if “obvious” to humans)

1. **Names as rules**
   - “SSOT”, “canonical”, “blessed”, “do-not-touch”, “archive”, “gold/silver/bronze” are not enforcement.
   - If a different tool path exists, the agent will use it.

2. **Documentation as a gate**
   - README/doctrine/literate programming can help *when the relevant text is in context*, but it does not prevent tool misuse.

3. **Folder semantics**
   - Humans infer lifecycle: `archive/` shouldn’t be edited; `gold/` is stable.
   - Agents see only paths unless you encode lifecycle rules as permissions, validators, or tooling constraints.

4. **“Single source of truth” as an invariant**
   - If two stores are writable, the operational reality is “multiple truths”.
   - Humans may still call one “SSOT”, but the system is not single-source.

5. **Negative instructions without hard stop**
   - “Don’t do X” fails when X is still a reachable/working tool and there’s no fail-closed guard.

6. **Intent preservation across time**
   - Agents have no durable internal “belief” unless the environment forces consistency (tests, contracts, state).

7. **Consistency of nomenclature**
   - If tags/keys/paths vary across ingestors, agents will treat them as separate concepts.

## What agents DO behaviorally respect (predictably)

These are the mechanisms that consistently shape behavior:

1. **Tool availability (capability surface)**
   - If a tool is not exposed/available, the agent cannot use it.

2. **Permissions & sandboxing**
   - Read-only filesystems, restricted directories, and lack of network access are respected because they are physical constraints.

3. **Fail-closed entrypoints**
   - Commands that exit non-zero unless prerequisites are met.
   - “Guardrails” work when they are placed on every write path (not just a preferred one).

4. **Schema/contract validation**
   - If outputs are rejected unless they match a schema, agents adapt.
   - This is the most reliable way to prevent semantic drift.

5. **Single entrypoint / no alternatives**
   - One write API + one read API yields predictable behavior.
   - Multiple overlapping entrypoints produces “choose the easiest tool” behavior.

6. **Budgets and timeouts**
   - Agents implicitly optimize for completion; slow/unreliable paths get avoided (or cause failure loops).

7. **Deterministic tests and CI gates**
   - If CI/test gates run automatically and fail on violations, agent changes get corrected.

8. **Explicit, machine-checkable authority markers**
   - Not “SSOT” in prose, but a concrete rule like: “Only backend X can accept writes; all other backends are read-only or rejected.”

## HFO-specific behavioral evidence (why SSOT wasn’t binding)

### Multiple memory backends exist in tooling

In MCP server config [.vscode/mcp.json](.vscode/mcp.json):

- `memory` MCP server is wired to a JSONL file (`MEMORY_FILE_PATH`).
- `mcp-memory-service` MCP server is wired to sqlite_vec (`MCP_MEMORY_SQLITE_PATH`).

Behaviorally, that means: there is no “single” memory write surface unless you remove/disable one.

### Guardrails apply to preferred entrypoints, not all possible actions

The SSOT facade [scripts/hfo_ssot.py](scripts/hfo_ssot.py) provides guidance-first guardrails for the commands it owns.

Behaviorally, that does not prevent:

- other MCP servers from writing to their own backends, or
- direct file writes if filesystem tools exist.

### Derived services look “broken” when they are lifecycle-managed separately

Shodh is derived and must be running to answer recall. It is started by [scripts/shodh_memory_server.sh](scripts/shodh_memory_server.sh). If it is not running (or cold-starting/indexing), recall feels “broken” or slow even if SSOT is healthy.

## Anti-theater checklist (behavioral architecture)

If you want “SSOT” to be real to agents:

- **One write tool:** expose exactly one write-capable memory interface.
- **Hard-disable competitors:** do not merely document “don’t use”; remove tool access.
- **Make receipts non-authoritative:** if you keep JSONL receipts, treat them as append-only logs and do not label that MCP server as primary “memory”.
- **Validate contracts at the boundary:** use schemas for cross-port communication.
- **Fail-closed everywhere:** every write path must run the same guardrails.
- **Run CI gates:** policy that isn’t tested is optional.

## Bottom line

Agents are not “disrespectful”; they are constrained optimizers operating on the capabilities you expose. If you expose multiple writable truths, you will get multiple truths.

## Sources

- MCP servers / memory backends: [.vscode/mcp.json](.vscode/mcp.json)
- SSOT facade / guardrails: [scripts/hfo_ssot.py](scripts/hfo_ssot.py)
- Shodh lifecycle: [scripts/shodh_memory_server.sh](scripts/shodh_memory_server.sh)
- Guardrails CI reality check: [artifacts/reports/GUARDRAILS_CICD_REALITY_CHECK_2026-01-28.md](artifacts/reports/GUARDRAILS_CICD_REALITY_CHECK_2026-01-28.md)
- Enforcement-theater forensic: [artifacts/forensics/FORENSIC_ENFORCEMENT_THEATER_AND_AGENT_SEMANTICS_2026_01_28.md](artifacts/forensics/FORENSIC_ENFORCEMENT_THEATER_AND_AGENT_SEMANTICS_2026_01_28.md)
