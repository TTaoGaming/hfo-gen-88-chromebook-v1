# Medallion: Silver | Mutation: 0% | HIVE: V

## Purpose

Make a reliable, repeatable way to generate a **context capsule**: a short, timestamped snapshot that helps agents (and you) stay aligned on:

- What we’re doing right now
- What changed recently
- What evidence/proof exists
- What decisions are locked vs still open

This capsule must also keep the swarm aligned on **phases** and the **non-negotiable workflow** so you don’t have to repeat yourself:

- Spec YAML first
- Contract (Zod) second
- RED tests third (TDD + BDD + CDD)
- Only then implementation
- Always emit append-only receipts with sources

Phase anchors (current)

- Phase 0: Infrastructure bootstrap (contracts + red tests + specs)
- Phase 1: Alpha generations/versioning bootstrap (mirror Omega discipline)
- Phase 2: Deterministic capsule compiler (role-scoped hydration)
- Phase 3: Drift firewall invariants (fail-closed)
- Phase 4: Memory delegation (curator daemon/agent)

Canonical Phase 0 spec: hfo_hot_obsidian/bronze/1_projects/alpha_gen1_current/specs/HFO_PHASE0_INFRA_BOOTSTRAP_V0_1_2026_01_25.yaml

Universal invariant (consolidation target)

- Every run has **Preflight** and **Postflight**
- This scales fractally: unified hub → port → subshard → tool
- Receipts are append-only with sources

Canonical policy spec: hfo_hot_obsidian/bronze/1_projects/alpha_gen1_current/specs/HFO_PREFLIGHT_POSTFLIGHT_POLICY_V0_1_2026_01_25.yaml

This is a **Port 6 (Kraken Keeper)** workflow: it’s about memory + truth-seeking + proof.

## The Simple “8¹ → 8⁰” Scatter/Gather Loop

This is a simpler variant of your HIVE/8 thinking:

- **Scatter (8¹):** 8 agents run in parallel.
- **Gather (8⁰):** 1 high-reasoning judge model consolidates and does a quorum-style analysis.

### Scatter step (8¹)

Run **8 agents** with deliberate diversity:

- Use different model families (and ideally 2 per family when possible).
- Each agent is allowed tools.
- Each agent is asked to **seek truth** with **proof of result**.

Each scatter agent must output:

- Claims (what it believes)
- Proof links (repo file links, command output excerpts, URLs)
- Uncertainties (what it could not verify)
- A short capsule draft (tight, bounded)

### Gather step (8⁰)

Run **1 high-reasoning model** to:

- Compare the 8 drafts
- Identify agreements, conflicts, and missing evidence
- Require proof for any important claim
- Produce a **final baton handoff capsule** (the one future agents load first)

Think of this as “quorum analysis”: the gather step does not blindly average; it demands receipts.

## What the Port 6 Gateway Does

The Port 6 gateway is the automation wrapper:

1) Auto-builds an initial capsule from local SSOT inputs (Silver reports + memory ledger + blackboard + pointers).
2) Runs the 8¹ scatter step (OpenRouter; rotate models).
3) Runs the 8⁰ gather step (one high reasoning model) to produce the baton capsule.
4) Writes outputs back into the repo with provenance.

## Tools (Preflight / Postflight)

The system is simplified into two calls:

- **Preflight (start of run):** compile a bounded capsule.
- **Postflight (end of run):** write the outcome + proof as an append-only receipt.

Current tool names (MCP Gateway Hub):

- `port6_preflight` / `port6_postflight`
- `hfo_preflight` / `hfo_postflight` (hub-level consolidated start/end)

## Proof of Result (What “Proof” Means Here)

“Proof” is anything that a future run can re-check:

- File paths in the repo
- Hashes / timestamps
- Tool outputs (bounded and captured)
- URLs (when web evidence is used)

Rule of thumb: if a claim can’t be linked to a checkable source, it must be labeled **unverified**.

## How Options 2 / 3 / 4 Help (Benefits)

This section answers: what do you gain from the “heavier” options?

### Option 2 benefit: Gateway-run as the one canon process

- **Consistency:** every capsule is produced the same way.
- **Lower drift:** agents don’t invent formats; the gateway forces the format.
- **Better audits:** you can point to “the run” that produced the capsule.

Tradeoff: if the gateway is down or misconfigured, capsule creation stalls.

### Option 3 benefit: Time-based memory becomes easy

- **Fast recall across months:** “what was true around date X?” becomes easier.
- **Better change narratives:** you can auto-explain how a belief evolved over time.
- **Reduced re-reading:** agents don’t need to scan long histories.

Tradeoff: adds another system that must stay trustworthy (ingestion + hygiene).

### Option 4 benefit: Relationship queries become easy

- **Multi-hop questions:** “how does this decision connect to that spec and those tests?”
- **Better “why” explanations:** relationships can be shown explicitly.
- **Better retrieval:** you can pull the most connected evidence quickly.

Tradeoff: can become complex and opaque if every claim can’t be traced to sources.

## Recommended rollout (minimal risk)

Start with a Port 6 gateway that does:

1) Build capsule from local SSOT inputs
2) 8¹ scatter with proof
3) 8⁰ gather with proof + quorum/conflict listing
4) Write baton capsule + append memory entry

Then add Option 3 or 4 only when the simple approach can’t answer your questions fast enough.

## Canonical outputs

- A timestamped **context capsule** (draft + final baton)
- A machine-readable receipt (who ran, which models, which sources)
- An append-only MCP memory entry pointing to the capsule
