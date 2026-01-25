# Medallion: Bronze | Mutation: 0% | HIVE: V

# GEN6 v20/v21 Primitives + FSM Layering (Touch2D → Instrument Scale)

## Purpose

Define the **minimum stable primitives** needed to scale from v20 “1×1 key” (Dino jump: Space press/release) into v21 “instrument-class” interaction (piano/guitar/accordion: multi-finger, multi-key, velocity, dwell, chords), without breaking Port boundaries.

Scope is GEN6 **Touch2D** only.

## SSOT Anchors (Current)

- Runtime: hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v20.html
- v20 spec: hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/specs/omega_gen6_v20_spec.yaml
- Tripwire contracts: contracts/hfo_tripwire_events.zod.ts
- Deterministic v20 fixture: hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl
- v20 tests:
  - scripts/omega_gen6_v20_p2_knuckle_tripwire_press_release_metadata_red.spec.ts
  - scripts/omega_gen6_v20_p3_knuckle_tripwire_space_press_release_red.spec.ts

## v20 Baseline: Primitives (What Exists)

### P1: DataFabric (shared substrate)

- `dataFabric.cursors[]` carries:
  - `fsmState` ∈ { IDLE, READY, COMMIT, COAST }
  - `readinessScore`
  - stabilized cursor coordinates (`uiNormX/uiNormY`, plus screen-space fields)
  - `landmarks[]` (hand skeleton)

Key rule: **coasting + smoothing belong to DataFabric**; downstream ports consume it.

### P2: Tripwire primitives

v20 uses a unified primitive family:

- `p2/tripwire_cross`
  - `sensorId`: `'static'` or `'knuckle'`
  - `sensor.phase`: `'begin' | 'end'`
  - `fsmState` and `readiness` for gating
  - velocity metadata in uiNorm space (for expressiveness)

Static tripwire is screen-anchored (center/thickness in uiNorm). Knuckle tripwire is hand-anchored using landmarks (index tip vs the MCP bar).

### P3: Effects mapping (current v20 goal)

- Map knuckle begin/end to **Space keydown/keyup** while `fsmState === 'COMMIT'`.
- Injection is fail-closed and has cooldown/deadman constraints.

## v21 Expansion: Primitives (What You Need Next)

The big step is to add **identity** (finger/key), **time semantics** (hold/dwell), and **grouping** (chords/strums), while keeping P2 “signal-only” and P3 “effects-only”.

### 1) Stable IDs

Introduce these IDs on all event payloads:

- `handId` (stable across frames while tracked; can still include `handIndex`)
- `fingerId` (e.g., `index_tip`, `middle_tip`, …)
- `keyId` (which key/string/button was actuated)
- `sensorId` (which sensing method produced it: static, knuckle, keybar, etc.)

### 2) Contact/crossing semantics

Keep the edge model, but make it composable:

- `phase`: `begin | end` (still the universal edge)
- `crossing` metadata:
  - `value` (signed distance / feature)
  - `enterThreshold` / `exitThreshold`
  - `direction`
  - `speed` / `vx` / `vy`

### 3) Dwell + hold

Instrument behaviors need time-based features:

- `downAtMs`, `upAtMs`
- `dwellMs` (time spent “pressed”)
- `holdState` (optional): `tap | hold | repeat`

### 4) Chords and strums

Add grouping keys that let P3 interpret patterns without re-deriving geometry:

- `gestureId` / `groupId` (per frame-window)
- `chordId` (simultaneous press set)
- `strokeId` (ordered plucks/strums)

### 5) Target geometry primitives (for multi-key grids)

To scale beyond one key, define targets explicitly:

- `target.kind`: `line | band | box | circle | polygon`
- `target.space`: `uiNorm | handNorm` (avoid ambiguity)
- `target.pose` and `target.params`

## Do we need a separate FSM?

Recommendation: **keep the global 4-state FSM** (IDLE/READY/COMMIT/COAST) as the *intent gate* and add a **micro-FSM per (handId, fingerId, keyId)**.

Why:

- The global FSM is about “can we act?” (safety + readiness + coasting).
- Instrument interaction is about “what note is down, for how long, in what grouping?” which is inherently per-key/per-finger.

### Suggested micro-FSM (per key)

- `UP` → `ENTERING` → `DOWN` → `RELEASING` → `UP`
- Transitions driven strictly by `phase begin/end` + thresholds.
- Attach timers for `dwellMs`, and optional repeat behavior.

P2 should emit edges + metadata; P3 owns the micro-FSM if it’s effect-specific (e.g., auto-repeat), otherwise P2 can emit neutral “down/up” edges if they are purely geometric.

## Visualization Implications (Touch2D)

Touch2D should visualize all sensing surfaces simultaneously:

- Cursor (already)
- Static tripwire: **two thin lines** = band edges (center ± thickness/2)
- Knuckle tripwire: **palm triangle** (wrist, index MCP, pinky MCP) + two thin hysteresis lines parallel to the MCP bar

All visualization should be derived from the same DataFabric/coasting fields used by P2, to avoid divergent smoothing.

## Next concrete v21 step

Add a second target (e.g., a 3-key strip) by:

1) Defining `keyId` and `target.kind/space` for each key.
2) Extending `p2/tripwire_cross` metadata to include `keyId` + `fingerId`.
3) Extending P3 to map `(keyId, phase)` → keydown/keyup for multiple keys.
4) Adding a deterministic JSONL fixture + Playwright test that presses two keys in sequence and as a chord.
