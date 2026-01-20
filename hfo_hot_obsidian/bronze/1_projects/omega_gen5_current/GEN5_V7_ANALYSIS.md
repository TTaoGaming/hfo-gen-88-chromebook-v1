# Medallion: Bronze | Mutation: 0% | HIVE: V

# Gen5 V7 Analysis (Governance + Frame Skipping)

## Executive Summary

V7 introduces a performance governor that can skip frames inside the main `predictLoop()` and adds new runtime performance controls in `systemState.parameters.performance`. This is a behavior change versus V6 and can explain inconsistent tracking because sensing and fusion are gated behind a frame-skipping check.

## Evidence (V7 vs V6)

- V7 adds a performance governor block under `systemState.parameters.performance` (FPS cap + fallback visuals). V6 does not have this block. See the parameter block in [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v7.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v7.html#L820-L879) vs V6 in [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v6.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v6.html#L820-L879).
- V7 calls `applyPerformanceGovernor()` inside `predictLoop()` and can return early (frame skip) before sensing/fusion/injection. See [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v7.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v7.html#L2165-L2190).
- The governor implementation can skip frames based on FPS cap and low-FPS thresholds. See [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v7.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v7.html#L2269-L2299).

## Issues Observed

1. **Frame skipping occurs before sensing/fusion**: `predictLoop()` returns early when the governor triggers, which can starve P0/P1/P3 and appear as inconsistent hand tracking.
2. **Governor is enabled by default**: `governorEnabled: true` in V7 parameters, so the behavior is always active without explicit opt‑in.
3. **Behavioral change is not isolated to P4 visuals**: the gating happens in the main loop, not just the rendering path, so it can bypass your architecture boundaries.

## Architecture Alignment Assessment

- **Aligned**: V7 retains the same P0/P1/P2/P3 pipeline structure and contracts as V6.
- **Misaligned**: The governor operates in the core loop and can bypass P0/P1/P3 progression. This crosses port boundaries and can violate your “sensing → fusion → FSM → injection” integrity when frame skipping is active.

## Recommendation

- **Recoverable**: This does not require a full purge. Clone V6 into V8 to restore baseline behavior and then re‑introduce thermal governance only within visual/render layers or at controlled P0/P1 input rates.

## Thermal Governance Options (Non‑Breaking)

1. **Render‑only decimation (P4‑only)**
   - Keep P0/P1/P3 running at full cadence.
   - Reduce Babylon/overlay render frequency or visual effects when FPS drops.
   - Avoid early return in `predictLoop()`; only throttle render/update frequency.

2. **Dynamic camera resolution and FPS target (P0‑scoped)**
   - Gradually lower `camera.resolution` or `fpsTarget` via `setOptions()` when device heat rises.
   - Sensing still runs every loop; input quality scales down instead of skipping fusion steps.

3. **Adaptive visual complexity (P4‑scoped)**
   - Reduce particle emission rates, trail meshes, and extra overlays when FPS is low.
   - Keep `predictLoop()` intact; only adjust visual layers and UI diagnostics.

4. **Idle‑aware throttling with strict gating**
   - When FSM is `IDLE` for sustained time, lower render intensity and optional UI refresh.
   - Immediately restore full cadence on `READY` or `COMMIT` transitions.
   - Never skip P1 fusion or P3 injection while non‑IDLE.
