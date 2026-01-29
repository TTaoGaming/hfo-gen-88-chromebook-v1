---
# Medallion: Bronze | Mutation: 0% | HIVE: V
schema_id: hfo.playbook.serena_setup_alpha_omega
schema_version: 1
created_utc: "2026-01-29"
authority_port: P4
scope:
  - "Serena setup for HFO Alpha/Omega missions"
  - "Fix: Omega missing from Serena global projects registry"
---

# Serena setup (Alpha + Omega) for this repo

## Goal
Make Serena reliably aware of **both** HFO missions:
- **Alpha**: repo workspace root
- **Omega**: `hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified`

…and prevent the recurring fail-closed error:
- “No active project” (task-adherence hardgate)

## What was wrong
Serena’s global registry at `$HOME/.serena/serena_config.yml` only contained **Alpha** in `projects:`.
That’s why Serena could list Alpha but did not surface Omega in the same tool context.

## What we changed (deterministic)
1) **Registered Omega in Serena global config**
- Patched: `$HOME/.serena/serena_config.yml`
- Backup saved inside repo for proof:
  - `artifacts/forensics/serena_config.yml.bak_2026_01_29T205254Z`

After patch, `projects:` contains both:
- `/home/tommytai3/active/hfo_gen_88_chromebook_v_1`
- `/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified`

2) **Created an Omega-local Serena project config**
- Added: `hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/.serena/project.yml`
- `project_name: omega_gen7_unified`
- `languages: [typescript, python]`

## How to verify (no Serena UI required)
Run:
- `bash scripts/hfo_serena_doctor.sh --json`

Expected:
- `status: ok`
- `home_config_mentions_alpha_root: true`
- `home_config_mentions_omega_root: true`

If you want a persisted proof artifact:
- `bash scripts/hfo_serena_doctor.sh --write --json`
  - writes: `artifacts/reports/serena_doctor_latest.json`

VS Code task shortcut:
- `Serena: Doctor (Alpha/Omega)`

## Remaining limitation (what we still can’t fully automate)
Serena’s **active project selection** appears to be session/UI scoped.
Even with both projects registered, you may still need to select the active project in Serena when a new session starts.

Operational rule for Gen88 P4 agent:
- If Serena gate errors “No active project”, stop edits and run the doctor; then activate the correct mission (Alpha/Omega).

## Next improvements (what to build next)
- Deterministic activation: add a non-UI command (ideal) or a pointer file (HFO-style) that Serena reads on boot to auto-select the matching project.
- Proof-carrying edits: require a recent doctor/gate proof before accepting edits or GitOps runs.
