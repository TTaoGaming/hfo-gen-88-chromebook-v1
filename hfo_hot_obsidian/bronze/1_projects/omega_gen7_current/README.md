# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen7 Current (Canonical Project)

Goal: a self-contained, cloneable *canonical* Gen7 root to prevent drift.

This project vendors the known-good Gen7 v1 portable baseline (including its Playwright regressions), and adds a canonical microkernel/spec surface for Gen7 v4 evolution.

## What’s inside

- `app/`: portable Omega HTML entrypoints + local libs/adapters.
- `specs/omega_gen7_v1_spec.yaml`: Gen7 v1 starting point.
- `specs/omega_gen7_v1_2_spec.yaml`: Gen7 v1.2 pointer spec (zlayers: runtime zIndex controls; Touch2D default OFF; Excalidraw opacity 0.8; kiosk enforced).
- `specs/omega_gen7_v2_spec.yaml`: Gen7 v2 refactor/hydra-bud posture (may be RED until re-validated).
- `specs/omega_gen7_v3_spec.yaml`: Gen7 v3 multi-fingertip → ASDF spec (explicitly allowed to be RED until wired).
- `specs/OMEGA_GEN7_MICROKERNEL_V4_SPEC_2026_01_25.yaml`: canonical microkernel boundaries + plugin interfaces + versioning + RED TDD plan.
- `references/gen6_v23_10/omega_gen6_v23_10.html`: vendored Gen6 v23.10 reference artifact.
- `tests/`: portable regression suites.

## How to run locally

1) Ensure the Omega static server is running on `:8889`.
2) Open:

- `http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/app/omega_gen7_v1.html`

Gen7 v2+ are currently **spec-only** (YAML) and do not ship HTML entrypoints yet.

Gen6 v23.10 reference:

- `http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/references/gen6_v23_10/omega_gen6_v23_10.html`

## Regression tests

Playwright specs are vendored here:

- `tests/playwright/omega_gen7_v1_portable_smoke.spec.ts`
- `tests/playwright/omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts`
- `tests/playwright/omega_gen7_v1_portable_dino_runner.spec.ts`

Recommended run (low-RAM safe runner):

- `.venv/bin/python scripts/hfo_playwright_safe_run.py --force-low-ram hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/tests/playwright/omega_gen7_v1_portable_smoke.spec.ts hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/tests/playwright/omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/tests/playwright/omega_gen7_v1_portable_dino_runner.spec.ts --project=chromium --reporter=line`
