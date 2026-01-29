# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Gen88 — Preflight → Artifact → Postflight Agent Mode

Version (Z): 2026-01-28T00:00:00Z

**Purpose:** A strict, obvious, fail-closed agent mode that enforces a single ritual every turn:

1) **Preflight** (compile a bounded capsule + receipt)
2) **Proof Artifact** (timestamped Markdown + stigmergy JSONL)
3) **Postflight** (verification receipt)

This mode exists to reduce reward hacking by requiring **receipts + artifacts** before any claim of completion.

## Non-Negotiables (every turn)

1) **Sequential Thinking:** Always run sequential thinking with **4–8 steps**.
2) **Preflight must run before any substantive work.**
3) **Proof Artifact must be written before postflight.**
4) **Postflight must run after the artifact is written.**

If any step fails (tool unavailable, command fails, missing receipt id), you must **fail-closed**:
- Do not continue with substantive work.
- Return only the smallest action needed to restore compliance.

## Canonical Commands (preferred)

### Option A (one command ritual)
Use the repo wrapper (recommended):

- `bash scripts/hfo_gen88_preflight_artifact_postflight.sh --scope P6 --note "<objective>" --slug "<slug>" --title "<title>" --summary "<1–2 sentence postflight summary>" --outcome ok|partial|error`

This wrapper:
- Runs preflight and captures `preflight_receipt_id`
- Creates a proof artifact under `artifacts/agent_proof/`
- Runs postflight and writes a postflight JSON receipt

### Option B (manual, explicit steps)
1) Preflight:
- `bash scripts/hfo_flight.sh preflight --scope <HFO|P6|P0.3.5.7.1> --note "<objective>"`

2) Proof artifact:
- `python3 scripts/hfo_make_turn_artifact.py --mode hfo-gen88-preflight-artifact-postflight --slug "<slug>" --title "<title>"`

3) Postflight:
- `bash scripts/hfo_flight.sh postflight --scope <same scope> --preflight-receipt-id <id> --summary "<1–2 sentences>" --outcome ok|partial|error --sources <comma-separated> --changes <comma-separated>`

## Artifact Rules

- Proof artifact must be timestamped and include:
  - Objective
  - What was executed (commands/tasks)
  - Receipts (preflight + postflight)
  - Proof paths (artifact path + flight JSON paths)
  - Next smallest step

## Suggested Scope Defaults

- Use `--scope HFO` when spanning multiple ports.
- Use `--scope P6` for assimilation / memory / receipts.
- Use a fractal scope `P<port>.<...>` when zoomed into a subshard.
