# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen5 Mirrored Clip PointerUp Error Report (2026-01-20)

## Summary

The mirrored golden‑master replay failed because no `pointerup` event was observed during COMMIT→IDLE in the replay test.

## Symptom

- Test failure: missing `pointerup` in replay events.
- Test: `scripts/omega_gen5_excalidraw_replay.spec.ts`

## Root Cause

1) **Replay window too short**: the test waited 4s even when the clip’s JSONL duration was longer, so it could finish before release.
2) **Tracking‑loss drain cleared the cursor before emitting an IDLE frame**: when readiness drained below threshold, the cursor was dropped without a final IDLE‑state frame, so the injector never emitted `pointerup`.

## Fix

- **Test wait time** now derived from JSONL meta (fps × frame_count) with a capped buffer.
- **Terminal drain** now emits a final IDLE cursor frame before clearing the hand state so COMMIT→IDLE generates `pointerup`.

## Verification

- `npm run test:omega:excalidraw` with mirrored replay JSONL now passes.

## Files Touched

- `scripts/omega_gen5_excalidraw_replay.spec.ts`
- `hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v5.html`

## Sources

- [scripts/omega_gen5_excalidraw_replay.spec.ts](scripts/omega_gen5_excalidraw_replay.spec.ts)
- [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v5.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v5.html)
- [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/replay/right-hand-idle-ready-commit-move-right-release-idle.mirrored.jsonl](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/replay/right-hand-idle-ready-commit-move-right-release-idle.mirrored.jsonl)
