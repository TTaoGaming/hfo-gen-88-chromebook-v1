# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Gen6 v18 Hot Bronze Report: COMMIT Knuckle Sensor Bar (Keybar)

# Timestamp: 2026-01-22

## What this adds (one sentence)

A COMMIT-only “Knuckle Sensor Bar” overlay and detector that makes curling/pressing fingers feel like keyboard keys, with fail-closed gating on readiness + palm-facing hysteresis.

## Grounded anchors (what already exists in v16)

Gen6 v16 already provides the signals needed to build this without inventing new semantics:

- **FSM state + readiness hysteresis knobs**: `systemState.parameters.fsm.hysteresisHigh/hysteresisLow` and per-hand `cursor.fsmState` + `cursor.readinessScore`.
- **Palm-facing hysteresis**: `systemState.parameters.palm.enterThreshold/exitThreshold` and `cursor.isPalmFacing` is already hysteresis-filtered.
- **Finger curls**: `cursor.curls.{index,middle,ring,pinky}` computed in P1.
- **Landmarks**: `cursor.landmarks[]` already carried (mirrored for fabric parity when `camera.mirror=true`).

Sources:

- hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v16.html

## Why knuckles (and why it’s Pareto-optimal)

- **Stable anchor**: the MCP knuckles (index MCP → pinky MCP) form a robust line on most camera angles.
- **Low cognitive load**: “press along knuckles” maps to familiar keyboard muscle memory.
- **Better than bespoke UI glue**: this is a ports-first interaction (P2 detect, P3 inject). The UI is a thin adapter overlay (microkernel plugin) and can be disabled without breaking semantics.

## The interaction contract (operator mental model)

- **ARM**: when a hand reaches **COMMIT** *and* readiness stays above the high hysteresis threshold *and* palm-facing remains true.
- **SHOW**: the knuckle bar appears along the knuckles (cyan COMMIT token).
- **PRESS**: curling a finger past a threshold generates a press begin/end.
- **INJECT**: press begin triggers a keyboard effect (v18 demo: Space for Dino jump).
- **DISARM (fail-closed)**: if readiness drops below low hysteresis or palm-facing flips false beyond a short timeout, the bar disappears and no injections happen.

## Anatomy model (v18)

Knuckle bar definition (per hand):

- Endpoints: index MCP (landmark 5) to pinky MCP (landmark 17)
- Segment markers: middle MCP (9) and ring MCP (13)
- Finger “keys”: index/middle/ring/pinky, each with press hysteresis

This is intentionally simple: start with curl-only press detection (deterministic, replayable), then add optional proximity/3D signals once tests are green.

## Fail-closed posture (non-negotiables)

These conditions must suppress the entire feature:

- Not in `COMMIT` (including `COAST`)
- Readiness below `hysteresisLow`
- Palm-facing false beyond `palmAwayTimeoutMs`

Defense-in-depth recommendation:

- Keep the injector strict: require `fsmState==COMMIT` in the event payload (same philosophy as v16 tripwire injector hardening).

## UI shell alignment (Apple HIG + Material 3)

UI overlay should be a microkernel plugin (per v17) that consumes port events:

- **Clarity**: one bar, four marks, minimal legend.
- **Deference**: semi-transparent; only visible while armed.
- **Depth**: no nested panels required for baseline.
- **Tokens**: use the consolidated mapping (IDLE gray, READY amber, COMMIT cyan, COAST yellow).
- **Motion restraint**: bounded pulse on press; no per-frame heavy redraw.

## RED-first test gates (what to implement next)

To avoid regressions and “AI theater,” treat these as required RED-first tests:

1) **P2 emits begin/end** for a known press sequence under COMMIT.
2) **P2 fail-closed**: emits nothing in IDLE/READY/COAST.
3) **Disarm on palm away**: stops emitting after hysteresis-based disarm.
4) **P3 injects Space** on press begin and does not inject when not COMMIT.

Suggested fixtures/specs are captured in the v18 YAML spec:

- hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/specs/omega_gen6_v18_spec.yaml

## Next grounded step

Clone v16 → v18 entrypoint and implement P2 `KnuckleKeybarThread` + P3 `KnuckleKeyInjector`, driven by the RED-first fixtures.
