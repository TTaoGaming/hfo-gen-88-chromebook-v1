# Medallion: Bronze | Mutation: 0% | HIVE: V

# GEN6 — Tripwire Thread (PlanckJS + Babylon) — Trade Study (2026-01-21)

## What is being built

A **physical tripwire thread** in **touch2d screen space** that can be interacted with like a web strand.

- Geometry: one “thread” anchored across the **middle of the screen** (default horizontal), optionally expanded into a thin **middle band** (thread thickness + weave halo).
- Activation gating: only armed when cursor `fsmState === 'COMMIT'` (from P1 DataFabric contract).
- Trigger semantics:
  - Detect **crossing** of the thread (enter/leave) and classify by **direction** (up-cross vs down-cross) and **velocity magnitude**.
  - Map to intents (example): up-cross ⇒ `keyUp`, down-cross ⇒ `keyDown`.
- Prediction: compute **time-to-impact (TTI)** against the thread/band using PlanckJS state and/or kinematic prediction so we can preview the trigger before collision.
- Visualization: a **GoldenLayout component** that renders the thread/web (Babylon overlay or 2D canvas), including a subtle “web tension” effect when a hand approaches or intersects.

## Architectural constraint (Gen6 Ports)

- **P2 SHAPE owns semantics**: physics world, collision, TTI, intent synthesis.
- **P3 remains the injector**: translates intents into W3C/keyboard nematocysts.
- Default posture: **telemetry-only** until explicitly enabling P3 dispatch (fail-closed, avoid destabilizing current flows).

Grounding anchors in current v11:

- P1 DataFabric includes `fsmState: 'IDLE'|'READY'|'COMMIT'|'COAST'`.
- There is already a **P2 hook** that runs after P1 fabric update and before P3 injection.

## Trade study matrix (4 viable paths)

| Path | Authoritative “physics” | How collision/TTI is computed | Pros | Cons / Risks | Effort (MVP) | Determinism & testability | Best fit |
|---|---|---|---|---|---:|---|---|
| A. PlanckJS authoritative + Babylon viz | PlanckJS 2D world (meters), Babylon for rendering only | Planck: represent thread as thin segment/edge or thin sensor box; predict cursor body motion (kinematic) and compute TTI from Planck contact manifold or raycast-like query | Most aligned with “Planck + Babylon” requirement; tight control over contacts; easiest to keep P2 semantics pure | Need careful unit mapping (screen→meters); Planck edge/segment contact may require modeling thread as thin box for stable contact | 1–2 days | High: can run deterministic stepping + debugEvaluate inputs; Playwright can assert P2 events | Recommended baseline for Gen6 P2
| B. Babylon Physics authoritative (plugin) + Planck secondary | Babylon Physics engine (Havok/Cannon/Ammo) for contacts; Planck used for simplified prediction | Use Babylon colliders in overlay scene; compute TTI via Babylon raycasts / swept tests; Planck used only for predictor model validation | Fast to visualize + tweak; GoldenLayout viz is “native” in Babylon | Babylon physics backend choice impacts determinism; plugin availability/licensing; harder to make a stable Playwright gate across machines | 2–4 days | Medium: physics backend variance can cause flakiness | Good if you want heavy 3D interaction later
| C. Hybrid: Planck predictor + Babylon confirmer | Planck handles TTI prediction; Babylon handles visual + optional collision confirmation | Compute predicted crossing time analytically/Planck; confirm actual crossing via Babylon thin band collider | Best UX: predictive preview + pretty visuals; de-risks backend mismatch | Two engines means more sync points (unit transforms/time step); higher integration overhead | 3–5 days | Medium–High: keep tests on Planck predictor, treat Babylon as best-effort visuals | Good if you need “predictive pointer” *and* richer visuals quickly
| D. Bridge MVP: Planck for canonical thread body, TTI analytic (still Babylon viz) | Planck used for canonical “thread” body + contact; TTI computed from kinematics (distance to band / velocity component) | Use Planck only for collision events; compute TTI from cursor point+velocity vs thread plane/band (fast) | Minimal moving parts; deterministic gates are easiest; still uses Planck + Babylon from day 1 | TTI is not fully “physics-derived” initially; must later upgrade to swept contact for edge cases | 0.5–1.5 days | Very high: closed-form math in P2 + reproducible | Best first step if your primary goal is reliable direction+velocity tripwire

## Recommendation

Start with **Path A or D**.

- If the priority is **predictive stability + clean Port2 semantics**: start with **D**, then upgrade the TTI calculation to full Planck swept-contact/queries.
- If the priority is “physics-first” from day 1: start with **A**.

## MVP acceptance criteria (shared)

1. While `fsmState !== 'COMMIT'`, crossings are ignored (telemetry may still be emitted as “disarmed”).
2. While `fsmState === 'COMMIT'`, crossing the mid-screen thread emits:
   - `p2:tripwire:cross` with `{ direction: 'up'|'down', speed, ttiMs, handIndex, pointerId, traceId?, targetId? }`.
3. A GoldenLayout panel (or overlay layer) renders a visible “web” at mid-screen with:
   - subtle animated strands,
   - highlight when a hand is within a proximity radius,
   - pulse on trigger.
4. Deterministic test path exists (debugEvaluate-style) so Playwright can drive synthetic cursors and assert events.

## Next concrete step (if you want me to implement)

- Add a new P2 adapter: `TripwireThreadAdapter` inside the existing gesture-language module.
- Add a GoldenLayout pane “Tripwire Web” (Babylon or Canvas2D) that reads the P2 telemetry buffer.
- Add a Playwright smoke: synthetic cursor crosses midline up then down in COMMIT; assert 2 events + correct direction.
