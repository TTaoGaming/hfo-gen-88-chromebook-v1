<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# Gen6 v22.1 Tracer Venom Latency Report (Grounded)

Date anchor: 2026-01-23 (workspace context)

## Scope

This report describes **observed latency** in the Gen6 v22.1 knuckle predictive pipeline using the **Tracer Venom Battery** (flag-gated stage breadcrumbs).

Constraints:

- No runtime behavior changes were made for this report.
- Measurements are limited to the fixtures executed; where a latency source is *possible but not exercised*, it is explicitly labeled as such.

## Executive Findings

- **Predictive COMMIT behavior (P3 inject relative to crossing) is working in these runs**: injection occurred at or before the crossing sample (`injectNow - crossNow` avg ≈ -1ms).
- **No evidence of extra COMMIT “debounce/timer latency” inside P3** was observed in these fixtures: P3 inject happens immediately once triggered.
- The only clear positive latency observed is at the **wrapper ACK boundary**: in the minimal fixture, `rx.hfo:nematocyst:ack` arrived ~53ms after `p3.inject.deliverEffect` (wall-clock `Date.now()` timestamps).

Interpretation (grounded): any “AI slop” would have to manifest as (a) non-zero scheduled delay (`delayMs`), (b) late firing drift (`driftMs`), (c) cooldown suppression postponing triggers, or (d) slow delivery/ack. In these fixtures, only (d) is measurable.

## Instrumentation (What the battery measures)

Tracer Venom Battery entries are stored in `window.__hfoTracerVenomBatteryEvents` and each entry includes:

- `ts`: wall-clock (`Date.now()`)
- `stage`: string identifier
- Optional fields (per stage): `now`, `delayMs`, `injectAtNow`, `driftMs`, `pointerId`, `sensorId`, `traceId`, `ok`, etc.

Source: [omega_gen6_v22_1.html](../para/omega_gen6_current/omega_gen6_v22_1.html)

## Pipeline Stages & Where Latency Can Exist

### A) P2 → P3 receipt (no intentional latency)

Stages:

- `p3.rx.tripplane_lookahead`
- `p3.rx.tripwire_cross`

Potential latency here is primarily **event-loop/dispatch overhead**, not an intentional timer.

### B) Predictive scheduling gate (intentional latency *when* TTC is nonzero)

Stages:

- `p3.lookahead.schedule` (emits `ttcMs`, `windowMs`, computed `delayMs`, `injectAtNow`)
- `p3.lookahead.scheduled` (when a future fire is queued)
- `p3.lookahead.fire` (emits `driftMs = now - injectAtNow`)

This is the principal place where a hidden timer would show up.

Measured in our fixtures:

- `ttcMs` was 0 → `delayMs` computed as 0 → **immediate path** taken.
- Therefore **no `p3.lookahead.fire` events** were produced, and drift is unmeasured here.

### C) COMMIT injection (should be immediate; code smell if delayed)

Stages:

- `p3.inject.payload`
- `p3.inject.deliverEffect` (or `p3.inject.sendNematocyst` fallback)

There is no intentional timer in this segment; latency here would be a code smell.

### D) Delivery boundary / wrapper ACK (positive latency observed)

Stages:

- `p3.dino.send.attempt` / `p3.dino.deliverEffect` (adapter delivery attempt)
- `rx.hfo:nematocyst:ack`

This is where cross-context messaging and wrapper scheduling can add latency.

## Measurements (Observed)

### Fixture 1: v20 knuckle press/release golden (real-time replay)

Fixture:

- `hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl`

Observed stage counts (top):

- `p3.rx.tripwire_cross`: 2
- `p3.inject.payload`: 2
- `p3.inject.deliverEffect`: 2
- `rx.hfo:nematocyst:ack`: 2
- Lookahead: schedule present (1), **immediate path** present (1), **no fire**

**Cross → Inject latency (fabric time `now`)**

- `injectNow - crossNow`: avg ≈ -1ms (min -2ms, max 0ms)

Meaning:

- Injection is occurring *before* or *at* crossing in COMMIT; this is consistent with the “predictive” requirement.

### Fixture 2: v22 extension-only minimal crossing fixture (real-time replay)

Fixture:

- `hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v22_knuckle_tripplane_extension_only_cross_min_golden.jsonl`

Observed:

- Lookahead has `ttcMs=0` and `windowMs=120`, producing `delayMs=0` and taking **immediate** injection.
- ACK observed.

**ACK boundary latency (wall clock `ts = Date.now()`)**

- `p3.inject.deliverEffect.ts = 1769217490012`
- `rx.hfo:nematocyst:ack.ts = 1769217490065`
- Delta ≈ **53ms**

Meaning:

- There is a measurable post-injection latency between effect delivery and wrapper acknowledgment.
- This is the clearest “where latency exists” signal from the current fixtures.

## Latency “Code Smell” Checklist (COMMIT)

Given READY/COMMIT anti-midas already gates intent upstream, additional COMMIT delays are suspicious when they are:

- **Non-deterministic** (high jitter in `driftMs`)
- **Large** relative to the lookahead window (`delayMs` near or above `windowMs`)
- **Added after COMMIT** (timers between `p3.inject.payload` and `p3.inject.deliverEffect`)

In the current evidence set:

- No extra P3 COMMIT delay was observed.
- The only positive latency measured is at the **ACK boundary (~53ms)**.

## Limitations / What is not yet measured

The tracer battery supports measuring these, but the executed fixtures did not exercise them:

- **Non-zero lookahead delay** (`delayMs > 0`) and **scheduler drift** (`p3.lookahead.fire.driftMs`)
- **Cooldown suppression** delaying repeats (P3 has a cooldown gate; this is a potential intentional latency source)

If the suspected “debounce” exists, it will likely appear as either:

- non-zero `delayMs` even when `ttcMs` should be small, or
- positive/variable `driftMs`, or
- cooldown suppression preventing expected injections.

## Reproduction Commands (No code changes)

- Ensure server: `bash scripts/hfo_omega_server_ctl.sh ensure`
- Run tracer battery smoke (existing): `npx playwright test scripts/omega_gen6_v22_1_p3_tracer_venom_battery_smoke.spec.ts --project=chromium`
- For latency extraction, a one-off Playwright run can replay fixtures in real time and read `window.__hfoTracerVenomBatteryEvents` (as done in-session).

## Source Links

- Runtime: [omega_gen6_v22_1.html](../para/omega_gen6_current/omega_gen6_v22_1.html)
- Smoke spec: [omega_gen6_v22_1_p3_tracer_venom_battery_smoke.spec.ts](../../../../../../scripts/omega_gen6_v22_1_p3_tracer_venom_battery_smoke.spec.ts)
- Fixture (minimal): [gen6_v22_knuckle_tripplane_extension_only_cross_min_golden.jsonl](../fixtures/touch2d/gen6_v22_knuckle_tripplane_extension_only_cross_min_golden.jsonl)
