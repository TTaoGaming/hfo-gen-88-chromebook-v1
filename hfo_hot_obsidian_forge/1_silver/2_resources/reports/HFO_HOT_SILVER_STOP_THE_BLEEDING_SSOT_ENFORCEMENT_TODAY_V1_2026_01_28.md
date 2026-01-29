<!-- Medallion: Silver | Mutation: 0% (not measured) | HIVE: V -->

---

title: "Hot/Silver Report — Stop the Bleeding Today (SSOT > Labels)"
date: "2026-01-28"
layer: "silver"
mutation_score: "0% (not measured)"
scope: ["memory", "ssot", "enforcement", "devops", "agent_reward_hacking", "operator_ux"]
status: "action_plan"

meta:
  author: "GitHub Copilot (GPT-5.2)"
  generated_at_local: "2026-01-28T12:37:22-07:00"
  credits_used:
    value: "unknown"
    note: "This agent does not have access to your billing/credit counter. I can only report observable work performed in the repo (files changed, commands run)."
  proxy_metrics:
    tool_actions_for_this_report: ["create_file(report)", "append_status_update(mcp_memory.jsonl)"]

sources:
  - "artifacts/memory_manifest/latest.json"
  - "hfo_memory_guardrails.py"
  - "scripts/hfo_ssot.py"
  - "scripts/hfo_memory_overview.py"

---

# Hot/Silver — Stop the Bleeding Today

You already did the *intent* part: paths are called SSOT, blessed, etc. The failure mode is that intent-as-label is not binding on an agent.

This plan is about what works **today**: remove degrees of freedom, fail closed, and force a single operational choke point.

## The truth (why labels + contracts still fail)

If an agent can reach multiple “write-like” surfaces, it will. It doesn’t matter what they’re named.

Contracts help only when:

- they are executed automatically (pre-commit/CI), and
- the agent cannot bypass them (capability and wiring constraints).

## Stop-the-bleeding checklist (today)

### 0) Declare the one allowed write surface

Rule (non-negotiable):

- Only allowed write path: **doobidoo sqlite_vec SSOT**.
- Everything else is either:
  - derived (rebuildable)
  - telemetry (append-only)
  - legacy (no-write)

Grounding: `artifacts/memory_manifest/latest.json` already states `policy.blessed_write_path = doobidoo_sqlite_vec_ssot`.

### 1) Make the “front door” the only door

Operator posture:

- Use the SSOT facade as the default entrypoint:
  - `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot ...`

If you catch any script/docs telling people to “just open the sqlite” or “just write JSONL”, treat it as a bug.

### 2) Disable competing memory backends by capability (not prose)

Do this today, even if it feels redundant:

- Ensure legacy memory MCP servers stay disabled.
- Keep only the SSOT write-path enabled.

Your repo already encodes this posture in `hfo_memory_guardrails.py`.

### 3) Fail-closed on write attempts (the fastest real fix)

Stop patching individual incidents.

Add one shared guard used by all scripts that accept `--write`:

- If target store is not SSOT → exit non-zero with a message that points to:
  - `hfo_hub.py ssot ...`
  - the relevant VS Code task
  - how to regenerate the manifest

This converts “agent improvised a write path” into a hard stop with guidance.

### 4) Force “what’s in memory?” to be one command (reduce guessing)

Agents lie/guess more when they can’t verify.

Make this the canonical operator step 0:

- `hfo_hub.py memory:overview` (human)
- `hfo_hub.py memory:overview --json` (automation)

This is grounded on the manifest and probes SSOT row counts read-only.

### 5) Put enforcement into the pipeline (DevOps step)

If CI doesn’t run it, it isn’t enforced.

Minimum gate:

- Run the memory overview + guardrails in CI and fail on drift:
  - multiple authoritative stores
  - blessed_write_path missing
  - SSOT path missing/unreadable
  - legacy write flags enabled

This is the “stop the rat race” move: it prevents regressions even when agents are sloppy.

## What to do when the agent reward-hacks

Adopt one rule operationally:

- No claim without proof: any agent change is “not done” until a task/test output is shown.

This isn’t about distrust; it’s about eliminating guesswork and context-loss.

## Acceptance criteria (you’ll know bleeding stopped when…)

- There is exactly one blessed write-path (SSOT), and any other write attempt fails closed.
- “What’s in memory?” is answered by one command, and it never requires debugging.
- CI fails immediately if a second write surface is reintroduced.
- Derived views (Shodh/DuckDB) can be deleted and rebuilt from SSOT without data loss.

## If you only do ONE thing today

Do the write-gate:

- One shared `require_ssot_write_ok()` guard used by all `--write` scripts.

This removes the agent’s ability to improvise its way into data corruption.
