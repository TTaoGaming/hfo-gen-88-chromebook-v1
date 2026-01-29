# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Gen6 v16 — Sensor Thread (TripwireThread) Progress Report

Timestamp (UTC): 2026-01-22T21:53:16Z

## What is implemented (v16)

- **P2 Sensor Thread runtime**: `window.hfoP2TripwireThread` (alias: `window.hfoP2SensorThread`) runs a horizontal sensor band in uiNorm space.
- **Contact-only semantics**: When `flag-p2-tripwire-contact-only=true`, v16 suppresses geometric fallback and emits `p2/tripwire_cross` events **only** from Planck begin/end contacts.
- **Begin + end phases**: In contact-only mode, v16 emits `sensor.phase: begin` and `sensor.phase: end` from Planck contact callbacks.
- **Direction + velocity aware payload**: `tripwire_cross` includes `vxUiNormPerS`, `vyUiNormPerS`, and `speedUiNormPerS`, plus `direction` derived from vertical velocity.
- **P3 injection pipeline**: `window.hfoP3PlanckSensorInjector` subscribes to `p2/tripwire_cross` and injects **Space** into Dino Runner on **COMMIT + down + begin-phase**.

## What is now verified (Golden Master BDD)

All GREEN using Playwright with `--workers=1`:

- P2 contact-only **does not emit** on sparse replay frames (no in-band overlap).
- P2 contact-only **does emit begin+end** on an in-band enter/exit golden fixture.
- P3 injector **injects Space** on COMMIT down-pluck and carries velocity fields.
- P3 injector **does not inject** on sparse frames in contact-only mode.

## Key fixes made to reach GREEN

- Fixed a Planck contact handler bug in v16 where the contact listener referenced an out-of-scope `cursorFixture`, preventing queued contacts from being processed.
- Ensured `p2-tripwire-contact-only` implies Planck contact mode (so tests do not require a second flag).
- Switched Planck cursor bodies to dynamic + bullet and ensured movement uses `setTransform` + `setLinearVelocity` for reliable contact begin/end detection.
- Updated Zod contract to allow v16’s additional velocity component fields.

## Known limitations / what’s still missing (for “rich metadata”)

- **Contact manifold richness**: v16 captures a best-effort world-manifold snapshot (normal + points). Impulses/TOI/CCD details are not guaranteed and not yet standardized in the event contract.
- **Sparse sampling limitation**: Contact-only intentionally emits nothing if the replay never overlaps the band; if you want “true contact-only” in the presence of sparse frames, you must either:
  - record more in-band samples (preferred), or
  - implement CCD/TOI-style stepping or interpolation (more complex, riskier).
- **Runtime contract enforcement**: Zod validation is currently enforced in tests (node-side). Runtime emission is not fail-closed beyond try/catch guards.

## Operational guardrails (stability)

- Added a lightweight test URL + retry wrappers for Playwright to reduce crashes/window-killed issues.
- Recommended validation command: `npx playwright test scripts/omega_gen6_v16_p2_tripwire_contact_only_* scripts/omega_gen6_v16_p3_tripwire_contact_only_* --project=chromium --workers=1`.

## Sources (workspace)

- Runtime: hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v16.html
- Contracts: contracts/hfo_tripwire_events.zod.ts
- Fixtures: hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v16_tripwire_planck_contact_inband_enter_exit_golden.jsonl
- Specs: scripts/omega_gen6_v16_p2_tripwire_contact_only_*.spec.ts, scripts/omega_gen6_v16_p3_tripwire_contact_only_*.spec.ts
- Test guards: scripts/omega_gen6_test_guards.ts
