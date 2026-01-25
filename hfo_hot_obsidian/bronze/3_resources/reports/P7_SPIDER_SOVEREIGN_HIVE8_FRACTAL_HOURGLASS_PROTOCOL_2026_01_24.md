# Medallion: Bronze | Mutation: 0% | HIVE: V

# P7 Spider Sovereign — HIVE-8 Fractal Hourglass Protocol (Draft)

Date anchor: 2026-01-24

## Purpose

Define a workable, fractal meta-process for Port 7 (Navigate) a.k.a. “Spider Sovereign”:

- Run the same loop at multiple zoom levels (life → area → project → task → next action).
- Reduce “fractal detail overwhelm” by enforcing zoom discipline.
- Keep the system auditable: decisions become append-only breadcrumbs.

This is explicitly a **draft**: highest-level abstractions are not fully formalized yet.

## Name

Recommended canonical name:

- **HIVE-8 Fractal Hourglass Protocol (FHP)**

Aliases that may appear in notes:

- Spider Sovereign Octa-Loop
- Obsidian Hourglass Navigator
- Octree Compass / Fractal Indexing

## The 8 Shards (Navigator Cognitive Primitives)

1) **Sequential Thinking**
   - Convert fuzzy intent into a bounded chain of steps.

2) **Reflexion**
   - Self-checks: detect drift, missing evidence, bad assumptions.

3) **Apex Assimilation (Exemplar Composition; No Invention)**
   - Synthesize from trusted artifacts only (repo, contracts, receipts, telemetry).

4) **Cynefin Mode Selection**
   - Decide the operating regime (clear/complicated/complex/chaotic) to choose the right action style.

5) **Fork/Evolve (Destructive Mutation When Needed)**
   - Controlled exploration: probe variants, learn quickly, prune aggressively.

6) **Stigmergy Coordination**
   - Externalize state for asynchronous alignment (blackboards, manifests, append-only logs).

7) **Boundary / Contracts (Fail-Closed Interfaces)** (placeholder name)
   - Ensure cross-port coupling is explicit and gated (schemas/contracts/pointers).

8) **Fractal Indexing & Retrieval (Octree Compass)** (likely)
   - The navigation substrate: stable addressing across zoom levels to prevent getting lost.

## Hourglass Move (Zoom Discipline)

Use an explicit expand→compress cycle:

- **Expand** (explore): gather evidence, list options, decide Cynefin mode.
- **Compress** (commit): pick the smallest safe next action and write a breadcrumb.

Rule of thumb:

- If you feel “lost”: you are likely mixing zoom levels.
- Fix: write the current zoom level explicitly, then do one compress step.

## “Hub vs Ideal” Audit Loop (Non-blocking)

Because the ideal is not fully formalized, this loop focuses on logging deltas safely.

### Ideal State (Draft Targets)

- P7 orchestration is **evidence-first** and **fail-closed**.
- Cross-port communication uses explicit schemas/contracts.
- Every action emits append-only breadcrumbs (memory + blackboard), including sources.
- There is a stable way to jump zoom levels (octree addressing taxonomy).

### Current State (What to log, not judge)

When auditing the current hub implementation, collect:

- Which entrypoints exist (e.g., hub/gateway scripts) and what they claim to do.
- Which contracts exist and which ports use them.
- Which telemetry/blackboard events are emitted and correlated.
- What pointers/stable aliases exist and what they target.

### Delta Log Template (for MCP memory JSONL)

Use a consistent JSON shape:

- `type`: `status_update` or `framework_note`
- `topic`: stable + date-anchored
- `summary`: short natural language summary
- `observed`: facts about the current hub (file paths, commands, outputs)
- `ideal_targets`: a short list of desired properties
- `gaps`: concrete mismatches or unknowns
- `next_actions`: smallest next steps (bounded)
- `sources`: workspace-relative paths

## Open Questions

- What is the canonical definition of shard #7: “Boundary/Contracts”, “Integrity Gates”, or another term?
- What is the canonical octree taxonomy (levels) used to index decisions and artifacts?
- Where should the canonical “ideal state spec” live (Bronze now, promoted to Silver when stable)?

## Next Steps

- Create a lightweight snapshot script that logs hub surface area into MCP memory.
- Define a first-pass octree taxonomy (8 levels) and adopt it consistently in topics/tags.
- Promote this report to Silver once terminology stabilizes.
