# Medallion: Bronze | Mutation: 0% | HIVE: V
# PlanckJS One-Pager — Practical Usage + Exemplars (Omega Gen6)

## What PlanckJS is (in HFO terms)
PlanckJS is a Box2D-style 2D rigid-body physics engine.
In Omega Gen6 we use it as a *deterministic semantics engine* for Port2: sensors, triggers, and time-to-impact (TTI) predictions.

## Core mental model
- **World**: simulation container (gravity, broadphase, contact manager)
- **Body**: rigid entity (static / dynamic / kinematic)
- **Fixture**: shape + material + sensor flag; attached to a body
- **Sensor fixture**: does not collide (no forces), but *does* generate contacts
- **Step**: `world.step(dtSeconds)` advances simulation

## Minimal “sensor band” tripwire exemplar
Use a static sensor band + a kinematic cursor body.

- Band: `static` body + `planck.Box(hx, hy, center, angle)` fixture with `{ isSensor: true }`
- Cursor: `kinematic` body with a tiny circle fixture; set position each tick
- Crossing detection:
  - simplest: compare previous and current `uiNormY` vs `bandY`
  - upgrade: use contact callbacks + TOI/sweep (CCD)

## Canonical APIs you’ll use constantly
- Create world:
  - `const world = planck.World({ gravity: planck.Vec2(0, 0) });`
- Bodies:
  - `world.createBody({ type: 'static' | 'dynamic' | 'kinematic', position: planck.Vec2(x, y) })`
- Fixtures:
  - `body.createFixture(planck.Box(hx, hy, center, angle), { isSensor: true })`
  - `body.createFixture(planck.Circle(r), { isSensor: true })`
- Stepping:
  - `world.step(Math.min(dtMs / 1000, 0.033))`

## Contacts (sensor events)
Planck supports world events:
- `world.on('begin-contact', (contact) => { ... })`
- `world.on('end-contact', (contact) => { ... })`

Pattern:
- Tag fixtures/bodies with userData so you can identify them in callbacks.
- In callback: inspect `contact.getFixtureA()` / `contact.getFixtureB()`.

## Determinism tips (important for golden replays)
- Keep `dt` bounded (cap at ~33ms).
- Use the same unit mapping every time (pick *one*:
  - uiNorm units (0..1) in Planck; or
  - meters with a SCALE constant and explicit transforms)
- Avoid random numbers unless seeded and recorded.
- When replaying frames: set kinematic target positions directly; don’t depend on user input.

## Time-to-impact (TTI) MVP formula
For a horizontal band centered at `yBand`, a cursor at `y` with velocity component `vy` toward the band:

- Distance: `d = |yBand - y|`
- Speed component: `s = |vy|`
- `ttiSeconds ≈ d / max(s, eps)`

Upgrade path:
- Use swept/TOI style queries for high-speed oblique crossings.

## Where this is used in Omega Gen6
- Runtime: `omega_gen6_v12.html`
  - Physics exemplar: Planck adapter (cursor/target + joint)
  - Tripwire MVP: `window.hfoP2TripwireThread` emits `tripwire_cross` in COMMIT only
- Spec: `GEN6_V12_TRIPWIRE_THREAD_PLANCK_BABYLON_SPEC_2026_01_21.yaml`

## Quick checklist for adding a new sensor primitive
- Define sensor geometry (fixture) + coordinate mapping
- Track per-pointer state (previous position/time)
- Decide gating (FSM state, readiness thresholds)
- Emit Port2 telemetry (and keep Port3 injection separate)
- Add a golden JSONL replay + Playwright assertion
