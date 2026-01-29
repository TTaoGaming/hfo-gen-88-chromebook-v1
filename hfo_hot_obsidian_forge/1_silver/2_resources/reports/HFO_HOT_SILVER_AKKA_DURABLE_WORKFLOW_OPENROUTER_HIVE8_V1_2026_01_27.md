<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->

---

title: "Hot/Silver Report — Akka Durable HIVE8 Workflow + OpenRouter (9 LLM calls/turn)"
date: "2026-01-27"
layer: "silver"
mutation_score: "0% (not measured)"
scope: ["hive8", "akka", "durable-workflow", "openrouter"]
status: "proposal"

---

# Hot/Silver — Akka Durable Workflow for HIVE8 Turns (OpenRouter, cheap model)

## Page 1 — What You Want (as I understand it)

## Consolidation Target: GitHub Copilot HIVE/8 Gen88v4 Agent Mode

We are consolidating around a single operational posture:

- Primary operator interface: **GitHub Copilot “HIVE/8 Gen88v4 agent mode”** (this repo’s strict artifact + meta workflow)
- Execution substrate: an **Akka durable workflow** that runs one turn as a deterministic, restartable state machine
- Storage + coordination: artifacts directory + manifest SSOT + append-only blackboards (stigmergy)

You want to **formalize the HIVE8 per-turn process** as a **durable, deterministic, auditable workflow** implemented in Akka, where:

- Each user prompt triggers **exactly 9 LLM calls per turn**:
  - 8 per-port artifacts (P0–P7)
  - 1 final meta synthesis artifact
- The **port execution order is fixed** (baton passing / paired-stage doctrine):
  - P0 → P7 → P1 → P6 → P2 → P5 → P3 → P4 → META
- **Port 0 runs tools first** (MCP/tools/context gathering) before its LLM call; remaining ports typically just consume prior artifacts (and optionally tool outputs) plus the manifest.
- The workflow is **durable**:
  - If the process crashes mid-turn, Akka restarts and resumes from the last completed step.
  - Every step is idempotent and deduplicated by `(turn_id, step)`.
- The workflow is **fail-closed**:
  - Strict validators must pass before advancing to the next step.
  - **Stigmergy is emitted per port** (one append-only signal after each port artifact is strict-valid) and optionally once at meta finalization.
- LLM calls go through **OpenRouter using a cheap model** (low-cost inference), with repeatability controls (temperature=0, stable prompt envelopes, optional seed if supported).

## Deliverables (outputs per turn)

You’re aiming for a stable “turn envelope” artifact set that mirrors the existing repo pattern:

- Turn directory: `artifacts/hive8/turns/<date>/<turn_id>/`
- `turn_manifest.json` (SSOT for the run)
- 8 per-port markdown artifacts
- `HIVE8__meta_synthesis.md`
- Optional: receipts / traces / step logs (append-only)
- Optional: stigmergy blackboard JSONL line (only on success)

## Core invariants (non-negotiable)

- **Deterministic structure**:
  - Each port artifact contains exactly **8 artifact items** with pow2 IDs `[1,2,4,8,16,32,64,128]`.
  - Meta-promoted items: **P0–P3 promote 2**, **P4–P7 promote 1**.
- **Strict gating**:
  - If any invariant fails, the workflow stops and records a failure receipt; no blackboard append.
- **Auditability**:
  - Meta synthesis is derived from artifacts + manifest (no hidden state).
  - Each step records inputs, outputs, and OpenRouter request metadata (minus secrets).

## Suggested Akka architecture (durable-by-default)

## Canonical Microturn Primitive (Fractal 0→1→2→3)

Within each port step, the “unit of work” is a microcycle that composes fractally:

- 0 = **OBSERVE (P0 domain)**: tools/context acquisition (may be “read prior artifacts” even if no MCP tools)
- 1 = **BRIDGE (P1 domain)**: LLM synthesis under schema contract
- 2 = **SHAPE (P2 domain)**: materialize the baton artifact + update manifest (SSOT)
- 3 = **INJECT (P3 domain)**: broadcast coordination via stigmergy (append-only CloudEvent)

Rule: phase 3 is allowed only after phase 2 passes strict validation.

### A. One turn = one persistent workflow entity

Model each user prompt as a durable entity:

- `TurnWorkflowEntity(turnId)` as an Akka **Persistent Actor** / EventSourcedBehavior
- State contains:
  - `turn_id`, `created_utc`, `mission_thread`, `user_prompt`
  - current `step` (P0, P7, …, META)
  - file paths to produced artifacts
  - validation results
  - OpenRouter call receipts (request/response hashes)

### B. Step execution = command → persist event → run side-effect → persist completion

For each step:

1) Receive `RunStep(step)` command
2) If already completed, **no-op** (idempotency)
3) Persist `StepStarted(step, input_hash)`
4) Perform side-effect (tooling + OpenRouter LLM call)
5) Write the artifact file atomically (temp → rename)
6) Persist `StepCompleted(step, output_hash, artifact_path)`
7) Run strict validators and either:
   - advance to next step, or
   - persist `TurnFailed(reason)`

### C. Isolation boundaries

- Tooling (MCP/tools) is executed only in P0 (by your preference) and its outputs are embedded as evidence into the P0 prompt.
- All later LLM calls consume:
  - the manifest
  - prior artifacts (as “source of truth”)
  - any “tool evidence” sections that P0 stored

## OpenRouter LLM call contract (cheap + repeatable)

You likely want:

- `temperature = 0`
- `top_p = 1`
- deterministic prompt templates (repo-tracked)
- consistent “system” message enforcing schema and markers
- response validation (must include markers and exact counts)

For cost, pick a cheap OpenRouter model (examples only):

- `google/gemma-7b-it` or similarly priced small instruct
- `meta-llama/llama-3.1-8b-instruct` (if cheap in your plan)

(Exact choice depends on your OpenRouter account pricing + supported `seed` behavior.)

---

## Page 2 — Concrete Workflow Spec (baton order + 9 calls)

## Turn state machine (canonical)

**Steps (LLM calls):**

0. `P0` — tool-augmented sense-making → writes `P0__*.md`
1. `P7` — navigation packaging constraints → writes `P7__*.md`
2. `P1` — interface contracts + validators → writes `P1__*.md`
3. `P6` — store/tendrils+pearl memory framing → writes `P6__*.md`
4. `P2` — proof/shape/derivation readiness → writes `P2__*.md`
5. `P5` — forensic audit gate → writes `P5__*.md`
6. `P3` — deliver/diagrams/pipeline → writes `P3__*.md`
7. `P4` — disrupt/pitfalls/red-team → writes `P4__*.md`
8. `META` — final synthesis (auto-composed from promoted shards) → writes `HIVE8__meta_synthesis.md`

**Non-LLM actions (gated):**

- `VALIDATE_STRICT` — run per-port + meta validators (may run after every step, but must pass at least at the end)
- `STIGMERGY_APPEND` — append a single blackboard JSONL CloudEvent line only if strict PASS after META

## Minimal event schema (so this is actually durable)

Recommended event set:

- `TurnStarted(turn_id, created_utc, mission_thread, prompt_hash)`
- `ToolingCaptured(step=P0, tool_run_receipt_hash, evidence_path?)`
- `LlmCallStarted(step, model, request_hash)`
- `LlmCallCompleted(step, response_hash, usage)`
- `ArtifactWritten(step, artifact_path, artifact_hash)`
- `ValidatorsPassed(step, report_path, report_hash)`
- `ValidatorsFailed(step, reason, report_path, report_hash)`
- `MetaFinalized(meta_path, meta_hash)`
- `StigmergyAppended(blackboard_path, line_hash)`
- `TurnCompleted(turn_id)`

## Idempotency rules (practical)

- Use `turn_id` as the stable primary key.
- For each `step`, store:
  - `input_hash` derived from (manifest + required prior artifacts + tool evidence)
  - `output_hash` of the written artifact
- If a retry happens and `input_hash` matches an already completed step, return the existing artifact path and do not re-call the LLM.

## Filesystem semantics (avoid half-writes)

- Write artifacts to `*.tmp` then rename to final path.
- Keep a per-turn `turn_manifest.json` updated after each step.
- Prefer append-only receipts (JSON) under `artifacts/`.

## Validation placement (recommended)

- Run light validators after every port artifact write:
  - markers present
  - exactly 8 items
  - pow2 IDs
  - promoted count correct for that port
- Run full manifest/meta validators after meta finalization:
  - meta includes Stage Flow + Debate/Map‑Elites blocks
  - promoted shards in meta match artifacts
  - exact artifact set present (P0–P7)

## What “Port 0 with tools” means in the workflow

P0 gets two sub-phases:

- `P0_TOOLS`: gather context (repo grep/read, memory tails, etc) and persist a tool receipt
- `P0_LLM`: call OpenRouter with tool evidence embedded

This preserves your “9 LLM calls per turn” requirement while still letting P0 be tool-augmented.

## Open questions (decisions you’ll need)

- Language/runtime: Scala vs Java for Akka, and where the existing Python scripts sit (kept as subprocess? rewritten?).
- Where to host the OpenRouter key and how to sign/record request hashes without leaking secrets.
- Which strict validators must be in-workflow vs post-processing.
- Whether you want per-step parallelism later (right now you want strict baton order).

## Proposed next step (actionable)

Create a single Akka workflow skeleton:

- `TurnWorkflowEntity` + step enum in the exact baton order
- A pluggable `OpenRouterClient`
- A `TurnArtifactStore` writing into `artifacts/hive8/turns/...`
- A `StrictValidator` module

Once that skeleton exists, we can wire one “turn” end-to-end with a cheap model and verify it creates the same artifact/manifest layout you already have.

---

## Provenance

- Repo context: existing HIVE8 artifact/manifest/meta patterns under `artifacts/hive8/turns/`
- Related meta doctrine: `HFO_HIVE8_GEN88_V4_PHASES_1_3_INTERFACES_VALIDATION_EVOLUTION.md`
