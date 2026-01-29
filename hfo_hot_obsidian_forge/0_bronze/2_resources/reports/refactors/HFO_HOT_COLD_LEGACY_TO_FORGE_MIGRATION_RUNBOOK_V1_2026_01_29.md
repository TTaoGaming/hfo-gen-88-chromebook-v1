# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Hot/Cold Legacy → Forge Migration Runbook (V1)

Date: 2026-01-29

This is the execution playbook to migrate legacy trees (hfo_hot_obsidian/, hfo_cold_obsidian/) into the forge layout (hfo_hot_obsidian_forge/, hfo_cold_obsidian_forge/) with a **Bronze-first** posture.

## Principles

- Bronze-first: default landing zone is forge Bronze unless proven stable.
- Non-destructive first: copy + validate before deleting/moving originals.
- Fail-closed interfaces: anything cross-port must remain schema’d (contracts/) and pointer-resolved (hfo_pointers.json).
- No split-brain: only one canonical blackboard per domain; legacy paths must redirect.

## Inputs you already have

- Move manifest (plan-only mapping):
  - hfo_hot_obsidian_forge/0_bronze/2_resources/reports/refactors/HFO_HOT_OBSIDIAN_ROOT_TO_FORGE_PARA_MOVE_MANIFEST_V1_2026_01_29.yaml
- Breakage matrix (what can break + mitigations):
  - hfo_hot_obsidian_forge/1_silver/2_resources/reports/refactors/HFO_HOT_OBSIDIAN_TO_FORGE_BREAKAGE_MATRIX_V1_2026_01_29.md

## Target structure (Forge)

- hfo_hot_obsidian_forge/
  - 0_bronze/{0_projects,1_areas,2_resources,3_archive}
  - 1_silver/{0_projects,1_areas,2_resources,3_archive}
  - 2_gold/{0_projects,1_areas,2_resources,3_archive}
  - 3_hfo/{...}
- hfo_cold_obsidian_forge/ mirrors the same.

## Step 0 — Confirm your “canonical” paths

Before migrating content, lock down the infrastructure invariants:

- Canonical blackboards are forge-root (and legacy paths redirect).
- hfo_pointers.json points at forge blackboards and forge roots.
- GitOps gates are green (Chronos, provenance).

If any of these are not true, stop and fix first.

## Step 1 — Inventory what exists (legacy)

Inventory and classify legacy content by purpose:

- Content/docs: notes, reports, playbooks, templates.
- Tooling: scripts, linters, generators, tests.
- Infrastructure/state: JSONL logs, DuckDB files, SSOT sqlite, artifacts.

Rule of thumb: **state stays where it is** unless there is a deliberate migration plan.

## Step 2 — Classify into Bronze vs Silver

Default rules:

- Forge Bronze (most things):
  - new/experimental docs, brainstorming, drafts
  - raw research, reports, one-off analyses
  - WIP scripts that are not depended on by pipelines

- Forge Silver (useful + integrated):
  - docs referenced by tasks/scripts, runbooks, “how we operate”
  - verified schemas/contracts and their tests
  - scripts used by GitOps, memory sync, blackboard emission/verification

- Forge Gold (rare, hardened):
  - automation that is proven stable and run repeatedly without manual patching
  - anything with strong validation (tests + invariants) and minimal moving parts

Promotion rule: “Silver if it’s referenced and stable; Gold if it’s stable and automatic.”

## Step 3 — Execute migration as a staged copy

Use a copy-first approach:

1) Copy legacy → forge Bronze destinations
2) Validate pointers + scripts + pre-commit gates
3) Add redirects (symlinks) for compatibility
4) Only then: delete/move legacy originals (optional, later)

You can do this in small batches aligned with your move manifest.

### Exclusions (do not migrate blindly)

Do NOT bulk-move these without a deliberate plan:

- artifacts/
- any *.jsonl blackboards that are canonical logging targets
- SSOT SQLite files (sqlite_vec)
- large derived caches (duckdb, parquet, zim)

## Step 4 — Maintain compatibility via redirects

After copying, preserve existing callers:

- If any tools still read from legacy paths, add symlinks from legacy → canonical forge.
- Keep these redirects until you’ve removed hardcoded paths.

## Step 5 — Validation gates (what to run)

Minimum checks per batch:

- GitOps batching (plan+run) should succeed.
- Pre-commit P5 gate must be green (Chronos/Provenance).
- If you touched contracts/: run the relevant tests.

Optional checks:

- Grep for hardcoded legacy paths (hfo_hot_obsidian/, hfo_cold_obsidian/).
- Sanity run any “memory overview”/“hub health” tasks.

## Step 6 — Promotion loop (Bronze → Silver)

Once something in Bronze is actually being used:

- Move it into forge Silver (same PARA category) when:
  - it has clear purpose, stable naming, and is referenced by tooling or runbooks
  - the references are pointer-resolved or relative-path resilient

## Step 7 — Decommission legacy safely (later)

Only after a full cycle of successful runs:

- Keep a final “legacy snapshot” folder (read-only).
- Remove redirects only after verifying no writers/readers depend on them.

## Suggested migration order (lowest risk → highest)

1) Docs/reports/playbooks → forge Bronze
2) Stable runbooks/specs used by tooling → forge Silver
3) Contracts + tests → forge Silver
4) Tooling scripts (GitOps, blackboard tools, memory sync helpers) → forge Silver
5) Only then: consider decommissioning legacy roots

## What you tell yourself during migration

- Bronze is the “holding bay.” It’s okay if it’s messy.
- Silver is where you integrate + stabilize.
- Gold is where you automate and stop thinking about it.
