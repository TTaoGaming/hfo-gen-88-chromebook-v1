---
description: HFO ritual prompt for Preflight → Proof Artifact → Postflight.
---

# HFO Gen88 Preflight → Artifact → Postflight (Ritual)

Objective (one sentence): {objective}

Scope: {scope}  
Slug: {slug}  
Title: {title}

## Required ritual (fail-closed)

1) Preflight (capsule + receipt)
- Run: `bash scripts/hfo_flight.sh preflight --scope {scope} --note "{objective}"`
- Capture `receipt_id` as `preflight_receipt_id`.

2) Proof artifact (timestamped)
- Run: `python3 scripts/hfo_make_turn_artifact.py --mode hfo-gen88-preflight-artifact-postflight --slug "{slug}" --title "{title}"`
- Add proof: preflight receipt id + any task/test output + changed file paths.

3) Postflight (verification receipt)
- Run: `bash scripts/hfo_flight.sh postflight --scope {scope} --preflight-receipt-id <id> --summary "<1–2 sentences>" --outcome ok|partial|error --sources <comma-separated> --changes <comma-separated>`

## Response requirements

- If any step cannot be executed: stop and state the smallest fix.
- If evidence is missing: mark as **unproven** and propose next smallest proof step.
