# Medallion: Bronze | Mutation: 0% | HIVE: V

<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# Omega Gen6 v3 — Dino Runner Hero (User Story)

## Goal

Provide a Gen6 v3 base HERO substrate (video background + Touch2D + Babylon overlay) with a Dino Runner overlay mode, and use the existing Gen6 FSM (unchanged) to trigger a single jump keypress when any tracked hand crosses the **IDLE → READY** threshold.

## Behavior

- Inputs: up to 2 hands tracked.
- Readiness: leaky-bucket dwell + hysteresis (existing logic).
- Trigger edge: any hand **IDLE → READY** emits one nematocyst payload (keyboard `Space`) with per-hand cooldown.
- Reset: turning palm/back away drains readiness; when it falls under hysteresis low, the state returns to IDLE, allowing a future trigger.

## Wiring (High Level)

- UI: the HERO substrate stays mounted; switching to “Dino” mode shows an iframe overlay that loads `dino_v1_wrapper.html` (same-origin).
- Injection: Gen6 v3 posts `postMessage({ type: 'hfo:nematocyst', payload })` to the wrapper iframe.
- Adapter: the wrapper includes `official_adapters/dino_runner_nematocyst/adapter.js`, which synthesizes keyboard events into the runner frame.

## Source Links

- Gen6 v3 UI + trigger: hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v3.html
- Dino wrapper: hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/dino_v1_wrapper.html
- Nematocyst adapter: hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/official_adapters/dino_runner_nematocyst/adapter.js
