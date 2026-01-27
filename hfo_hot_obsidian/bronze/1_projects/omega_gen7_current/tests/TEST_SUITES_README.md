# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen7 Test Suites (Fast vs Slow)

This folder is intentionally portable: no absolute paths, no external network dependencies.

## Fast suite (default developer loop)

Properties:

- Bounded runtime (target: < 60s on low-RAM)
- No video recording by default
- Fail-closed assertions (no flaky waits)

Included tests:

- `tests/playwright/omega_gen7_v1_portable_smoke.spec.ts`
- `tests/playwright/omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts`
- `tests/playwright/omega_gen7_v1_portable_dino_runner.spec.ts`

## Slow suite (CI / nightly)

Adds:

- Golden master comparisons (DOM/state snapshots, deterministic telemetry)
- Optional MP4 clips for human review when regressions occur

Planned artifacts:

- `tests/golden_masters/manifest.json` (declares what is “golden”)
- `tests/clips/manifest.json` (declares clip capture scenarios and filenames)

Notes:

- Do not commit large MP4s until we decide governance rules (size limits, receipts, CI storage).
