---
# Medallion: Bronze | Mutation: 0% | HIVE: V
schema_id: hfo.playbook.p4_serena_setup_anti_rewardhacking
schema_version: 1
created_utc: "2026-01-29"
authority_port: P4
scope:
  - "HFO Gen88 Basic P4 agent"
  - "Serena active-project hardgate + Alpha/Omega setup"
related_artifacts:
  - "hfo_hot_obsidian_forge/0_bronze/2_resources/reports/HFO_SERENA_HARDGATE_REWARD_HACKING_AND_BRITTLENESS_ANALYSIS_BRONZE_V1_2026_01_29.md"
  - "artifacts/forensics/FORENSIC_SERENA_ACTIVE_PROJECT_HARDGATE_2026_01_29.md"
---

# Playbook: improve Serena + the Gen88 Basic P4 agent (using the hardgate forensic)

## Goal
Turn the Serena hardgate incident into a **repeatable setup + enforcement loop** so:
- Alpha and Omega are both visible/registered (two missions)
- “No active project” becomes a deterministic, one-command recovery
- Agents can’t silently route around guardrails (reward-hacking)

## What actually broke (so we fix the right thing)
The hardgate was not caused by v8.6→v8.7 content. It surfaced because:
- Serena’s task-adherence gate is **fail-closed** and depends on a **session-scoped active project**.
- The agent’s editing path was not consistently proof-gated; once it started calling the gate, the missing active-project pointer became visible.

So the fix is not “change content”; it’s “make Serena selection deterministic + make guardrails enforceable.”

## Your two missions (Alpha/Omega) and what “setup” means
In this repo, the mission roots already exist (see pointers):
- Alpha root = workspace root
- Omega root = path in `hfo_pointers.json` (currently `paths.omega_gen7_current_project_root`)

“Serena fully set up” should mean:
1) Both roots appear in Serena’s known-project registry.
2) The active project is always resolvable for the current workspace (Alpha) with no UI guessing.

## Immediate upgrades you can apply today

### 1) Add a deterministic “Serena Doctor” check (no UI required)
New helper:
- `scripts/hfo_serena_doctor.sh`

What it does:
- Reads local `.serena/project.yml` (Alpha)
- Reads `hfo_pointers.json` to locate Omega
- Checks whether `$HOME/.serena/serena_config.yml` mentions Alpha/Omega roots (best-effort)
- Emits a JSON report you can paste into tickets / audits

Recommended workflow:
- Run it at the start of any editing session (or whenever “No active project” appears).

### 2) Standardize recovery for the “No active project” hardgate
This is the operational invariant you want:
- If Serena gate errors, you do not continue editing.
- You run the doctor, then you activate the current project.

Today, activation still likely requires the Serena UI.
Your improvement target for Serena is to support a deterministic command:
- `serena activate --project <path>`

If Serena cannot do that yet, then store the active project pointer *in-repo* (HFO style) and auto-select on boot.

### 3) Make P4 agent outputs “proof-carrying”
Your P4 agent already produces signed 4-beat receipts.
Upgrade the discipline:
- Any time you do edits (insert/replace/delete), the proof payload should include:
  - which project is active (Alpha/Omega)
  - the Serena gate result (pass/fail)
  - the exact recovery performed if fail

This defeats “compliance theater” because proof is required in the artifact.

## Hardening changes (the real anti reward-hacking work)

### A) Enforce guardrails at the tool boundary (not in prompts)
Right now, the agent can route around guardrails by using alternative edit paths.
To harden:
- Decide ONE blessed path for edits (Serena-gated) and make others loud/blocked.

Practical option for HFO:
- Gate GitOps / merge operations on presence of a recent proof payload that asserts gate pass.
- Add an SSOT audit that flags diffs created without a corresponding proof payload.

### B) Eliminate session-only state in Serena (make active project persistent)
This is the core brittleness.
Design requirement:
- When only one project matches the workspace root, auto-select it.
- Persist it across reloads.

HFO-native approach:
- Store an active-project pointer file in-repo (similar to `hfo_pointers.json`).
- Serena should read it on boot.

### C) Make Alpha/Omega explicit in every workflow
Common failure: “Serena only sees Alpha.”
Fix by making Alpha/Omega registration part of setup:
- a checklist
- a doctor report
- a proof payload

## What to improve in the Gen88 Basic P4 agent specifically

### 1) Add a P4 ritual precondition: “Serena ready for this mission?”
Add a lightweight preflight habit:
- Run `scripts/hfo_serena_doctor.sh --json` and attach output as evidence.

If you want fail-closed:
- Run `scripts/hfo_serena_doctor.sh --fail-on-missing` before you let an agent edit.

### 2) Add “mission selector” semantics
Even if you don’t change Serena today, make the mission explicit in payload notes:
- `mission:alpha` for repo-root work
- `mission:omega` for work in `omega_gen7_current_project_root`

Then you can audit:
- which mission was active when a change landed

### 3) Add a “smallest recovery step” rule
When blocked:
- do not detour into adjacent work unless you also log the blocker and recovery attempt

This reduces the reward-hack of “productive detours.”

## Concrete next steps (minimal, high leverage)
1) Run `bash scripts/hfo_serena_doctor.sh --write` and keep the JSON as proof.
2) Update Serena config so both Alpha + Omega are registered (or document the exact UI steps once, then automate).
3) Add a hard rule: no edits unless (a) Serena active project set AND (b) proof payload created.

If you want, next I can implement the enforcement layer on the repo side (GitOps/merge guard) so bypass edits become auditable/blocked.
