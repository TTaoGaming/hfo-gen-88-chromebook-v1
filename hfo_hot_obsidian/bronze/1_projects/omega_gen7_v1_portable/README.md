# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen7 v1 (Portable Project)

Goal: a self-contained, cloneable baseline for evolving from Gen6 v23.10 toward Gen7 multi-hand tripplane→key orchestration.

## What’s inside

- `app/omega_gen6_v23_10.html`: known-good Gen6 v23.10 baseline.
- `app/omega_gen7_v1.html`: Gen7 v1 starting point (currently a clone baseline).
- `app/lib/`: local JS/CSS/WASM/model assets required by the HTML.
- `specs/omega_gen7_v1_spec.yaml`: SSOT notes/spec for Gen7 v1.
- `specs/omega_gen7_v2_spec.yaml`: v2 spec (refactor + fork-and-evolve posture).
- `specs/omega_gen7_v3_spec.yaml`: v3 spec (multi-finger tripplane → ASDF).
- `tests/fixtures/`: portable test fixtures (JSONL).

## How to run locally

1) Ensure the Omega static server is running on `:8889` (repo task: **Omega Server: Ensure (:8889)**).
2) Open:

- `http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen7_v1_portable/app/omega_gen6_v23_10.html`
- or `http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen7_v1_portable/app/omega_gen7_v1.html`

Gen7 v2+ are currently **spec-only** (YAML) and do not ship HTML entrypoints yet.

## Regression tests

Playwright specs live inside this portable project:

- `tests/playwright/omega_gen7_v1_portable_smoke.spec.ts`
- `tests/playwright/omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts`
- `tests/playwright/omega_gen7_v1_portable_dino_runner.spec.ts`

Recommended run (low-RAM safe runner):

- `.venv/bin/python scripts/hfo_playwright_safe_run.py --force-low-ram hfo_hot_obsidian/bronze/1_projects/omega_gen7_v1_portable/tests/playwright/omega_gen7_v1_portable_smoke.spec.ts hfo_hot_obsidian/bronze/1_projects/omega_gen7_v1_portable/tests/playwright/omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts hfo_hot_obsidian/bronze/1_projects/omega_gen7_v1_portable/tests/playwright/omega_gen7_v1_portable_dino_runner.spec.ts --project=chromium --reporter=line`
