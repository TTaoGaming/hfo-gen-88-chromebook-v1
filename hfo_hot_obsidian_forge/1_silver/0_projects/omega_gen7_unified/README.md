<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# Omega Gen7 Unified (Canonical Project)

Goal: a self-contained, cloneable *canonical* Gen7 root to prevent drift.

This project vendors the known-good Gen7 v1 portable baseline (including its Playwright regressions).

- **Runnable cap:** Gen7 v1.1
- **Next draft:** Gen7 v1.2 (spec-only; not yet implemented)

## What’s inside

- `app/`: portable Omega HTML entrypoints + local libs/adapters.
- `specs/omega_gen7_v1_spec.yaml`: Gen7 v1 starting point.
- `specs/omega_gen7_v1_1_spec.yaml`: Gen7 v1.1 cap spec (canonical pointer).
- `specs/omega_gen7_v1_2_spec.yaml`: Gen7 v1.2 draft spec (work-in-progress).
- `references/gen6_v23_10/omega_gen6_v23_10.html`: vendored Gen6 v23.10 reference artifact.
- `tests/`: portable regression suites.

## How to run locally

1) Ensure the Omega static server is running on `:8889`.
2) Open:

- `http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/app/omega_gen7_v1.html`
- `http://localhost:8889/hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/app/omega_gen7_v1.html`

Anything claiming **> v1.2** is treated as non-canonical and is archived under `archive/hallucinated_above_v1_1/`.

Gen6 v23.10 reference:

- `http://localhost:8889/hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/references/gen6_v23_10/omega_gen6_v23_10.html`

## Regression tests

Playwright specs are vendored here:

- `tests/playwright/omega_gen7_v1_portable_smoke.spec.ts`
- `tests/playwright/omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts`
- `tests/playwright/omega_gen7_v1_portable_dino_runner.spec.ts`

Recommended run (low-RAM safe runner):

- `.venv/bin/python scripts/hfo_playwright_safe_run.py --force-low-ram hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/tests/playwright/omega_gen7_v1_portable_smoke.spec.ts hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/tests/playwright/omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/tests/playwright/omega_gen7_v1_portable_dino_runner.spec.ts --project=chromium --reporter=line`
