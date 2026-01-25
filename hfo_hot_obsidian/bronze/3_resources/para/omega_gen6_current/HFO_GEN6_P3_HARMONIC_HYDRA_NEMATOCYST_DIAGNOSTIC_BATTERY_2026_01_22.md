# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Gen6 — Port 3 Harmonic Hydra: Nematocyst Diagnostic Battery (Pareto 8)

# Date: 2026-01-22

## Goal

Define a **simple, reliable, extendable** “battery” of diagnostic injection payloads for P3 (Harmonic Hydra) that behave like surgical imaging tracers:

- each tracer shot isolates one failure domain
- each emits unambiguous observability signals
- each is deterministic enough for Playwright
- all are **deny-by-default** and **fail-closed**

This is a **separate hot-bronze note** (not embedded inside HTML). It’s intended to guide a v17.5+ implementation.

## Grounded context (current Gen6 reality)

- P3 injection already supports:
  - W3C pointer nematocyst injection (PointerEvent path)
  - a tracer shorthand payload kind (`tracer_bullet_venom`) that maps to a trace-tagged Space keypress (v17.3+) and is OpenFeature-gated deny-by-default (v17.4).
- Delivery boundary reality:
  - Primary: `window.hfoAdapterHost.deliverEffect('dino-v1', payload)`
  - Fallback: P3 delivery path
  - When iframe/adapter isn’t ready: effects can queue → later flush/drain.

Practical implication: the biggest bottleneck is often not “tripwire timing”, but **adapter/iframe readiness and queue/flush**.

## Battery design principles (Pareto)

1) **Correlation-first**: every shot produces a correlation id (`traceId`) that appears in every emitted event.
2) **Stage stamps**: every shot produces stage timestamps to compute where time accumulates.
3) **Fail-closed gates**: tracer injection only executes when explicitly enabled.
4) **Deterministic by construction**: avoid UI-specific DOM dependencies unless the payload is explicitly “DOM-targeted”.
5) **Extensible envelope**: add new variants by adding new `kind`/`variant` values, never by overloading unrelated fields.

## Recommended envelope (payload contract shape)

Use a stable envelope so all 8 payload styles can share routing, logging, and policy.

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "...one_of_8...",
  "traceId": "tb_...",
  "targetId": "dino-v1 | p3.tripwire_injector | ...",
  "ts": "2026-01-22T...Z",
  "now": 123456.78,
  "pointerId": 12,
  "handIndex": 0,
  "readiness": 0.93,
  "params": { }
}
```

Policy fields:

- `traceId` required when enabled (and MUST NOT contain PII)
- `variant` required
- `params` must be JSON-serializable

## Observability bus

Emit events through a single surface for tests and dashboards:

- `window.hfoPortsEffects.emit(port, type, payload)`

Prefer events with:

- `traceId`
- `stage` and/or `spanId`
- `ok` boolean
- `reason` string

---

# The Pareto 8 diagnostic payload styles

## 1) Trace-Span Chain Shot (correlation + stage timing)

**What it images:** where time accumulates across P2→P3→adapter→queue→flush→ack.

Payload (example):

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "trace_span_chain",
  "traceId": "tb_span_001",
  "targetId": "dino-v1",
  "params": { "stages": ["p2.detect","p3.schedule","p3.deliver","p3.queue","p3.flush","p7.ack"] }
}
```

Signals emitted:

- `p3/tracer_span` `{ traceId, stage, ts, now, ok, details }`

Failure signatures:

- large gap `schedule → deliver` ⇒ tick jitter/timer
- `deliver ok=false` + `queued` ⇒ readiness boundary bottleneck
- `deliver ok=true` but no `ack` ⇒ wrapper/ack path bottleneck

Extensibility:

- Add `attributes` (OTel-style) for adapter id, queue depth, etc.

## 2) Synthetic Canary Verdict Shot (single outcome)

**What it images:** “is the pipeline healthy” with a crisp verdict.

Payload:

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "synthetic_canary",
  "traceId": "tb_canary_001",
  "targetId": "dino-v1",
  "params": { "deliverWithinMs": 50, "ackWithinMs": 150, "drainWithinMs": 500 }
}
```

Signals emitted:

- `p3/canary_start`
- `p3/canary_verdict` `{ verdict: "PASS|SOFT_FAIL|HARD_FAIL", failedStage, durationsMs, queueDepth }`

Failure signatures:

- `HARD_FAIL failedStage=deliver` ⇒ adapter host not accepting effects
- `SOFT_FAIL failedStage=ack` ⇒ delivered but ack missing/late

Extensibility:

- Add `budget` fields (error budget style) for CI gating.

## 3) Queue Ultrasound Probe (saturation + backlog imaging)

**What it images:** queue depth/age, drain behavior, “stuck flush”.

Payload:

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "queue_ultrasound",
  "traceId": "tb_queue_001",
  "targetId": "dino-v1",
  "params": { "sampleWindowMs": 2000, "sampleEveryMs": 200 }
}
```

Signals emitted:

- `p3/queue_snapshot` `{ traceId, depth, ageMaxMs, ageP95Ms, flushCount, flushDurP95Ms }`

Failure signatures:

- depth increases monotonically ⇒ downstream not draining
- ageMax grows without flush ⇒ readiness never achieved

Extensibility:

- Add histogram buckets (cheap JSON) for age and flush durations.

## 4) Waterfall Trace Export Shot (human-fast visual)

**What it images:** a Perfetto/DevTools-like timeline of stages.

Payload:

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "trace_export",
  "traceId": "tb_trace_001",
  "params": { "bufferSize": 200, "exportFormat": "chrome-trace-json" }
}
```

Signals emitted:

- `p3/trace_event` entries stored in a buffer
- optional: `p3/trace_export_ready` with a download hook

Failure signatures:

- obvious gaps between events show the bottleneck visually.

Extensibility:

- add categories (`cat`) for p2/p3/p7 and adapter boundaries.

## 5) W3C Pointer Packet Shot (PointerEvent sequence integrity)

**What it images:** pointer event ordering + capture correctness (down/move/up/cancel).

Payload:

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "w3c_pointer_packet",
  "traceId": "tb_ptr_001",
  "targetId": "dom.hit_test",
  "params": { "sequence": ["pointerdown","pointermove","pointerup"], "moves": 2, "capture": true }
}
```

Signals emitted:

- `p3/pointer_packet_stage` `{ traceId, eventType, deliveredToTarget, captureActive }`

Failure signatures:

- down delivered, moves missing ⇒ capture/target mismatch
- cancel emitted unexpectedly ⇒ lifecycle/pointer-loss conditions

Extensibility:

- add `pressure/tilt/buttons` to probe richer pointer semantics.

## 6) Keyboard Packet Shot (minimal substrate probe)

**What it images:** key injection path minimalism (best for determinism).

Payload:

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "keyboard_packet",
  "traceId": "tb_key_001",
  "targetId": "dino-v1",
  "params": { "code": "Space", "repeat": 3, "intervalMs": 80 }
}
```

Signals emitted:

- `p3/keyboard_inject` `{ traceId, ok, via: "adapter|fallback|queue", queued: boolean }`

Failure signatures:

- all queued ⇒ readiness bottleneck
- ok=false even in fallback ⇒ injector regression

Extensibility:

- add `combo` sequences (e.g., Space then ArrowDown) as needed.

## 7) Adapter Handshake / Echo Shot (boundary proof)

**What it images:** whether the adapter boundary can round-trip a diagnostic token.

Payload:

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "adapter_echo",
  "traceId": "tb_echo_001",
  "targetId": "dino-v1",
  "params": { "token": "tb_echo_001", "timeoutMs": 250 }
}
```

Signals emitted:

- `p3/adapter_echo_send`
- `p7/adapter_echo_recv` (or wrapper-side ack event)
- `p3/adapter_echo_verdict` `{ ok, rttMs }`

Failure signatures:

- send occurs but no recv ⇒ postMessage/iframe bridge bottleneck

Extensibility:

- add versioning to token format (`tokenV":1`) for compat.

## 8) DOM Target Biopsy Shot (hit-test + capture + cancel)

**What it images:** target discovery and pointer capture reliability in real DOM.

Payload:

```json
{
  "kind": "nematocyst_diagnostic",
  "variant": "dom_target_biopsy",
  "traceId": "tb_dom_001",
  "targetId": "dom.selector",
  "params": { "selector": "canvas", "x": 0.5, "y": 0.5, "expectCapture": true }
}
```

Signals emitted:

- `p3/dom_target_resolve` `{ found, elementTag, reason }`
- `p3/dom_capture_probe` `{ captureOk, releaseOk }`

Failure signatures:

- resolve fails ⇒ DOM changes / iframe layering / selector drift
- capture fails ⇒ pointer capture API/regression or wrong target

Extensibility:

- add “multi-app” targeting: `appId`, `frameId`.

---

## Recommended enablement flags (deny-by-default)

- `p3-diagnostic-battery` (boolean): master enable
- `p3-diagnostic-variant` (string enum): selects which of the 8 to run
- `p3-diagnostic-export` (boolean): allow exporting trace buffers

## Minimal rollout plan

1) Implement **#6 Keyboard Packet** first (most deterministic, best smoke test).
2) Implement **#1 Trace-Span Chain** next (unlocks real bottleneck attribution).
3) Add **#3 Queue Ultrasound** to see sustained readiness regressions.
4) Add the DOM/pointer variants (#5/#8) only when you need DOM-level biopsy.

## Notes on “surgical imaging” semantics

- Think of `traceId` like a contrast agent: it must flow through every stage.
- Think of stage stamps like an imaging timeline: gaps are the pathology.
- Prefer probes that reduce degrees of freedom (keyboard packet) before probes that add them (DOM biopsy).
