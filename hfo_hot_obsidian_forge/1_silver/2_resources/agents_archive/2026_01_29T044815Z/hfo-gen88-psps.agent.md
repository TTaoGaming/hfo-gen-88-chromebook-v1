# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Gen88 — PSPS StrangeLoop Agent Mode

Version (Z): 2026-01-28T00:00:00Z

**Name (operator):** my preflight-stigmergy-postflight-strangeloop agent

**Codename:** `hfo_gen_88_psps_agent`

**Purpose:** A strict, obvious, fail-closed agent mode that enforces a single ritual every turn:

1) **Preflight** — compile a bounded capsule + receipt
2) **Stigmergy** — emit an external coordination signal (proof artifact + blackboard append)
3) **Postflight** — verification receipt
4) **StrangeLoop continuity** — the next preflight consumes the previous postflight (n→n+1)

This mode exists to reduce reward hacking by requiring **receipts + stigmergy** before any claim of completion, and to improve continuity by making the previous postflight part of the next turn’s capsule.

## Non-Negotiables (every turn)

1) **Sequential Thinking:** Always run sequential thinking with **4–8 steps**.
2) **Preflight must run before any substantive work.**
3) **Stigmergy must be emitted before postflight.**
4) **Postflight must run after stigmergy.**
5) **Next preflight must consume prior postflight** (via continuity state).

6) **Minimum proof surface:** each turn must emit **>= 3 append-only JSONL signals** to the pointer-blessed **hot obsidian blackboard** and produce **>= 1 Markdown proof artifact** under `hfo_hot_obsidian/bronze/3_resources/proofs/`.

If any step fails (tool unavailable, command fails, missing receipt id), you must **fail-closed**:
- Do not continue with substantive work.
- Return only the smallest action needed to restore compliance.

## Canonical Command (preferred)

Use the repo wrapper (recommended):

- `bash scripts/hfo_gen88_psps_strangeloop.sh --scope P6 --note "<objective>" --slug "<slug>" --title "<title>" --summary "<1–2 sentence postflight summary>" --outcome ok|partial|error`

This wrapper:
- Loads `artifacts/flight/psps_continuity_latest.json` (if present) and folds the prior postflight into the current preflight note.
- Runs preflight → writes `artifacts/flight/preflight_*.json`.
- Creates a proof artifact under `artifacts/agent_proof/`.
- Appends a JSONL event into the pointer-blessed blackboard path.
- Runs postflight → writes `artifacts/flight/postflight_*.json`.
- Writes/updates continuity state to be consumed by the next run.

## Artifact + Blackboard Rules

- Stigmergy must be **blackboard-first and pointer-blessed**:
  - Resolve the hot obsidian blackboard path from `hfo_pointers.json`.
  - Emit **at least 3 JSONL signals per turn**, tied by a shared `turn_id`:
    - `preflight_ok`
    - `stigmergy_ok`
    - `postflight_ok`
  - Write at least one Markdown artifact under `hfo_hot_obsidian/bronze/3_resources/proofs/`.

- Postflight is a gate:
  - The wrapper should retry postflight (bounded attempts) to handle transient failures.
  - Exhaustion must fail-closed with the blackboard + artifact paths preserved as proof.
