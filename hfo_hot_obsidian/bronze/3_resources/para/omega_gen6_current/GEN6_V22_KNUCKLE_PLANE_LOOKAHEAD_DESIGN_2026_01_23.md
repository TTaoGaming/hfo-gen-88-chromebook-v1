# Medallion: Bronze | Mutation: 0% | HIVE: V

# GEN6 v21 Actual Logic (Knuckle Tripwire → Dino) + v22 Design (Knuckle Plane + Lookahead)

## Purpose

1) Document the **actual current behavior** (what the code is doing today) so it’s debuggable.

2) Define a **v22 usability plan** for “feels good”: a knuckle **plane** target that is easier to trigger under mono-camera uncertainty, plus **predictive lookahead** to compensate camera/Mediapipe latency while staying **COMMIT-gated** (anti‑Midas).

## SSOT Anchors (Current)

- Runtime: [hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v21.html](hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v21.html)
- P2/P3 contracts: [contracts/hfo_tripwire_events.zod.ts](contracts/hfo_tripwire_events.zod.ts)
- Dino adapter boundary: [hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/official_adapters/dino_runner_nematocyst/adapter.js](hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/official_adapters/dino_runner_nematocyst/adapter.js)
- Deterministic fixture: [hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl](hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl)
- Golden tests (v21):
  - [scripts/omega_gen6_v21_p2_knuckle_tripwire_hysteresis_golden.spec.ts](scripts/omega_gen6_v21_p2_knuckle_tripwire_hysteresis_golden.spec.ts)
  - [scripts/omega_gen6_v21_p3_knuckle_tripwire_space_press_release_golden.spec.ts](scripts/omega_gen6_v21_p3_knuckle_tripwire_space_press_release_golden.spec.ts)
  - [scripts/omega_gen6_v21_e2e_knuckle_tripwire_to_dino_ack_golden.spec.ts](scripts/omega_gen6_v21_e2e_knuckle_tripwire_to_dino_ack_golden.spec.ts)

---

## Part A — v21 Actual Logic (What Happens Today)

### 1) Substrate: DataFabric cursor inputs

Each tick, P2 consumes `dataFabric.cursors[]` entries (derived from MediaPipe and stabilization/coasting). For each cursor, it uses:

- `fsmState` (IDLE / READY / COMMIT / COAST)
- `readinessScore`
- `landmarks[21]` (hand skeleton)
- `uiNormX/uiNormY` for cursor-style velocities

**Important:** In v21, the knuckle tripwire thread is guarded by the flag `flag-p2-tripwire-knuckle=true` and is also **readiness gated** (minimum readiness threshold).

### 2) P2 Knuckle Tripwire geometry (the “plane” proxy)

The “knuckle plane” proxy is a **line** in uiNorm space:

- Bar endpoints: index MCP (`landmarks[5]`) to pinky MCP (`landmarks[17]`)
- Pointer point: index fingertip (`landmarks[8]`)

The thread computes a signed distance from the fingertip to the bar line:

- `rawDistanceUiNorm = signedCross(tip, bar) / barLen`
- A sign normalization step makes the **wrist** (`landmarks[0]`) land on a fixed side of the bar.
  - In current v21, wrist is normalized to the **positive** side.

Resulting primary features:

- `orientedDistanceUiNorm` (signed distance, wrist-positive)
- `featureDistanceUiNorm` (Kalman-filtered value of `orientedDistanceUiNorm`)

### 3) P2 Knuckle Tripwire state machine (hysteresis)

There is a per-pointer pressed state and a hysteresis rule:

- If not pressed and `featureDistanceUiNorm >= onDistanceUiNorm` ⇒ pressed becomes true ⇒ **phase = begin**
- If pressed and `featureDistanceUiNorm <= offDistanceUiNorm` ⇒ pressed becomes false ⇒ **phase = end**

Then **and only then**, P2 emits an event if and only if `fsmState === 'COMMIT'`:

- Event: `p2:tripwire_cross` with `sensorId='knuckle'`
- Payload includes:
  - `sensor.distance.*` (raw/oriented/feature distances, thresholds, bar length)
  - `vxUiNormPerS/vyUiNormPerS/speedUiNormPerS`
  - `sensor.distance.*VelUiNormPerS` (distance derivative metadata)
  - `direction` (currently derived from signed distance velocity; always `down|up`)

### 4) Why fast motion can “miss” in v21

Even if your fingertip truly crossed the knuckle plane in real space, **v21 can fail to emit** for non-latency reasons:

- **Filter lag:** the press decision uses `featureDistanceUiNorm` (Kalman filtered), not `rawDistanceUiNorm`.
  - On very fast motion, `rawDistanceUiNorm` may cross the threshold in one frame, but the Kalman filter may not rise above `onDistanceUiNorm` immediately.
  - If you cross and come back quickly, the filtered value may never reach the “on” threshold.

- **Discrete sampling:** if the camera feed drops frames or dt spikes, you can “teleport” from one side to the other without getting a stable filtered threshold crossing.

- **COMMIT-only emission:** even if geometry crosses, if the FSM is not in COMMIT at the exact tick where hysteresis flips, the emission is suppressed.

Net: it can feel like “moving fast doesn’t trigger at all.” This is a *semantics mismatch* (thresholding on filtered value) not simply latency.

### 5) P3 mapping (Space press/release)

In v21, P3 listens for knuckle tripwire crossings and maps:

- `phase='begin'` ⇒ deliver keyboard `action='keydown'` Space
- `phase='end'` ⇒ deliver keyboard `action='keyup'` Space

P3 is still **COMMIT-gated** (defense-in-depth). A cooldown policy may exist, but keyup is intended to be allowed even soon after keydown.

### 6) P7 delivery + Dino adapter boundary

- P7 posts `hfo:nematocyst` messages to the Dino wrapper iframe.
- The Dino adapter now accepts `action in {'keypress','keydown','keyup'}`.
- The wrapper replies with `hfo:nematocyst:ack` and `{ ok: true }` when it successfully injected the event.

The v21 E2E golden spec asserts this ack path so “P3 emitted inject but Dino ignored it” is caught.

---

## Part B — v22: Make It Feel Good (Plane + Extrusion + Lookahead)

### Goals

- **Usability:** trigger reliably even when mono-camera pose/orientation is imperfect.
- **Responsiveness:** compensate camera/Mediapipe latency with lookahead while staying **COMMIT-gated**.
- **Anti‑Midas:** keep accidental triggers rare by (a) COMMIT gating and (b) short predictable windows.

### 1) Replace “filtered threshold crossing” with “plane intersection crossing”

Today the event is keyed to `featureDistanceUiNorm >= on`.

For v22, prefer a geometric crossing test based on the segment between frames:

- Let `d0 = orientedDistanceUiNorm(t-Δt)` and `d1 = orientedDistanceUiNorm(t)`.
- A plane/line crossing exists if `d0` and `d1` straddle 0 (or straddle the band threshold).

This catches “fast movement” because it does **not** require the filtered distance to reach a threshold — it only needs the sign to change.

Recommended split:

- Use `rawDistanceUiNorm` (or `orientedDistanceUiNorm`) for **crossing detection**.
- Use `featureDistanceUiNorm` for **stability / visualization / noise estimation**.

### 2) Extrude the knuckle bar into a band (make the plane thicker)

Mono-camera ambiguity means the knuckle bar estimate can jitter/rotate.

To make triggering easier and more stable:

- Define a band of half-thickness `ε` (uiNorm) around the plane.
- Treat “pressed” as being inside the band on the wrist-positive side.

Concretely:

- `enterThreshold = +ε_on`
- `exitThreshold = +ε_off`

This becomes a true “plane with thickness.”

### 3) Extend the knuckle segment endpoints (make the plane wider)

If the MCP endpoints are slightly wrong, the effective plane can be too short.

Approach:

- Compute unit direction along the bar: `u = (b-a)/|b-a|`.
- Extend endpoints: `a' = a - u * ext`, `b' = b + u * ext`.

This acts like a wider plane cut through the knuckles.

**v22 microkernel tuning knobs (Port7):**

- Default is symmetric extension (0.5 + 1.0 + 0.5): extend each endpoint by `0.5 * barLen`.
- Asymmetric extension supports a “sword”: extend one end more than the other.

Runtime knobs (planned stable names):

- `systemState.parameters.p2.knuckleTripwire.barExtensionFracA` (endpoint A extension fraction)
- `systemState.parameters.p2.knuckleTripwire.barExtensionFracB` (endpoint B extension fraction)

URL overrides (Port7 microkernel flags):

- `?flag-p2-knuckle-tripwire-ext-a-frac=<number>`
- `?flag-p2-knuckle-tripwire-ext-b-frac=<number>`

**UI/Debug request:** classify this as a distinct semantic target (CSS class / color token), e.g.

- `targetClass: 'knuckle_plane_ext'`
- render bar and its extended ends in a distinct color.

### 4) Lookahead (predictive triggering) for latency compensation

We already have the ingredients:

- current oriented distance `d` (uiNorm)
- oriented distance velocity `v = dVelUiNormPerS`

We can compute a simple time-to-contact (TTC):

- If `v > 0` and `d < enterThreshold`, then `ttcSec ≈ (enterThreshold - d) / v`

Then, in COMMIT only, we can “arm early”:

- If `0 <= ttcMs <= lookaheadWindowMs`, emit a **lookahead event**.

Two safe patterns:

1) **Early begin only**: allow predictive firing for begin, but require a real crossing (or hard minimum dwell) for end.
2) **Predictive press + real release**: press early, but release only when the real band exit condition occurs.

This keeps the feel snappy without causing sticky keys.

### 5) Proposed v22 primitive additions

Add (or formalize) a v22 lookahead event:

- `p2/tripwire_lookahead`
  - `sensorId='knuckle'`
  - `ttcMs`, `lookaheadWindowMs`
  - `d`, `v`, thresholds

Then P3 can decide:

- In COMMIT: if `tripwire_lookahead` suggests imminent begin, issue keydown early.

### 6) Test plan (must catch fast-motion misses)

Add a v22 golden fixture containing a deliberately fast crossing (large jump in oriented distance between frames).

BDD expectations:

- A begin/end pair is emitted even when the crossing is one-frame.
- Lookahead produces a begin before the real crossing when `ttcMs` is within window.
- E2E ack remains ok:true.

---

## Practical next steps

1) Add a dedicated v22 doc/spec + fixture for fast crossings (one-frame straddle).
2) Implement plane crossing detection using `orientedDistanceUiNorm` sign change + band thresholds.
3) Implement endpoint extension + band thickness parameters.
4) Implement lookahead event (COMMIT gated) and tune `lookaheadWindowMs` to measured pipeline latency.

---

## Part C — v23 Aspirational Goals (Non-binding)

v23 is intended to promote this v22 primitive (COMMIT-gated knuckle trip-plane + lookahead) into a full “tool” abstraction:

- **Flaming sword / tool geometry (Babylon):** render an extended knuckle-anchored plane/rod as an actual 3D tool.
- **Physics-backed sensors (Planck/Rapier):** represent the tool as a physics sensor object (capsule/box/plane) with begin/end contacts.
- **Unified Port2 primitive:** same semantic sensor can be emitted as:
  - distance/velocity plane-crossing (fallback mode)
  - physics contact begin/end (authoritative mode)
- **Port3 delivery policy:** predictable mapping of tool contacts to actions (keydown/keyup) with safety gates (COMMIT + deadman + cooldowns).

## One-command regression loop

- Run: `npm run -s test:gen6:v21:golden`
- Use it as the gate while iterating v22 (add a v22 test target when the implementation lands).
