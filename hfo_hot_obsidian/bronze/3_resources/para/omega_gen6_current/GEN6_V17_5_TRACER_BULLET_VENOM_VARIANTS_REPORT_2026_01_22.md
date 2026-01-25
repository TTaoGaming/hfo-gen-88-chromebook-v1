# Medallion: Bronze | Mutation: 0% | HIVE: V

# Gen6 v17.5 — Tracer Bullet Venom Variants (4 exemplar patterns)

# Date: 2026-01-22

## Why this report

Gen6 already has a working tracer payload path ("tracer_bullet_venom" → trace-tagged keyboard Space) plus fail-closed OpenFeature gating in v17.4.

The goal for v17.5 is to evolve tracer venom into **stronger, more legible signals** that make pipeline bottlenecks obvious (especially adapter/iframe readiness + queue/flush) while staying:

- COMMIT-only and deny-by-default
- deterministic in Playwright
- low overhead unless explicitly enabled

## Current grounded baseline (v17.4)

The existing tracer venom is implemented as:

- **Payload kind:** `tracer_bullet_venom`
- **Fail-closed gate:** `p3-tracer-bullet-venom` (default false)
- **Suppression telemetry:** `p3/tracer_venom_suppressed`
- **Mapping:** tracer payload maps into `{ kind:'keyboard', action:'keypress', code:'Space' }` and propagates `traceId/targetId`.

Grounding references:

- P3 injector gate + mapping: `omega_gen6_v17_4.html` (P3InjectorPort `sendNematocystToDino`)
- Tripwire injector tracer mode (buildPayload routes through P3InjectorPort): `omega_gen6_v17_4.html` (Tripwire injector `buildPayload` + `inject`)

Files:

- `hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v17_4.html`
- `scripts/omega_gen6_v17_4_tracer_bullet_venom_flag_gate.spec.ts`

## Exemplar sources (industry)

These are the patterns we’re borrowing from:

- W3C Trace Context (standard trace id propagation): <https://www.w3.org/TR/trace-context/>
- OpenTelemetry traces/spans/events mental model: <https://opentelemetry.io/docs/concepts/signals/traces/>
- Chrome DevTools tracing (waterfall/timeline capture concepts): <https://chromedevtools.github.io/devtools-protocol/tot/Tracing/>

### HFO hub (Tavily) — 2026 exemplar scan (raw results)

The HFO hub Tavily-backed scan for “2026 observability exemplars” returned several 2026-focused pieces that reinforce the **correlation-first** and **synthetic/canary** patterns we want for tracer bullets:

- Platform Engineering (2026 tools evaluation): stresses correlation across logs/metrics/traces as “non-negotiable” during incident navigation.
  - <https://platformengineering.org/blog/10-observability-tools-platform-engineers-should-evaluate-in-2026>
- APMdigest 2026 Predictions series (multi-part): emphasizes OpenTelemetry as a unifying layer and agent-first correlation workflows.
  - <https://www.apmdigest.com/2026-observability-predictions-6>
  - <https://www.apmdigest.com/2026-observability-predictions-1>
  - <https://www.apmdigest.com/2026-observability-predictions-3>
  - <https://www.apmdigest.com/2026-observability-predictions-7>
- “Application Monitoring Best Practices” (2026): explicitly calls out structured logging with `trace_id` correlation plus synthetic monitoring as a maturity step.
  - <https://tasrieit.com/blog/application-monitoring-best-practices-complete-guide-2026>

How these map to v17.5 variants:

- **Variant 1 (Trace-Context Shot)**: aligns to correlation-first (trace id everywhere).
- **Variant 2 (Synthetic Canary)**: aligns to synthetic monitoring maturity + deployment validation.
- **Variant 3 (RED/USE Queue Profiler)**: aligns to operational metrics as the default incident entrypoint.

## The pipeline we want to illuminate

This is the minimal “critical path” we should be able to see clearly:

1) **P2 detection**: `p2/tripwire_cross` and/or `p2/tripwire_lookahead`
2) **P3 scheduling**: pre-arm decision + `injectAtNow` calculation
3) **P3 injection attempt**: build payload → deliverEffect → fallback/sendNematocystToDino
4) **Adapter/iframe readiness**: deliver ok vs queued
5) **Queue flush + ack**: when iframe becomes ready, queue drains; optional ack/receipt

If tracer shows “queued but never drained”, the bottleneck is readiness/flush, not tripwire timing.

---

# Variant 1 — “W3C Trace-Context Shot” (trace/span correlation)

**Exemplar pattern:** W3C Trace Context + OpenTelemetry spans.

### What it is

Make every tracer bullet create a structured **trace** with:

- `traceId` (stable across the shot)
- `spanId` per stage (P2 detect, P3 schedule, P3 deliver, queue, flush, ack)
- events on spans for significant instants (suppressed, queued, delivered)

### Why it makes bottlenecks obvious

You get a true per-shot “waterfall” even without a UI: you can compute durations between stage timestamps and identify which stage dominates.

### Minimal v17.5 payload shape

Use an internal “traceparent-like” string (no HTTP needed) to keep formatting stable:

```js
{
  kind: 'tracer_bullet_venom',
  variant: 'trace_context',
  trace: {
    traceId: '32hex...',
    parentSpanId: '16hex...' | null,
    spanId: '16hex...',
    sampled: true,
    tracestate: { hfo: 'gen6' }
  },
  targetId: 'p3.tripwire_injector',
  reason: 'tripwire_down_cross',
  pointerId: 12,
  handIndex: 0,
  now: 123456.7
}
```

### Telemetry to emit (bus: `window.hfoPortsEffects`)

Emit a normalized event at each stage, always including `trace.traceId` and `trace.spanId`:

- `p2/tracer_span_event`: `{ stage:'detect', ... }`
- `p3/tracer_span_event`: `{ stage:'schedule' | 'deliver_attempt' | 'queued' | 'flush' | 'ack', ... }`

### Deterministic tests

- “flag off” should still produce only `p3/tracer_venom_suppressed`
- “flag on” should produce a complete span chain up to `queued` in the missing-iframe path

### When to use

Best default “strong variant” when you want consistent, queryable bottleneck attribution.

---

# Variant 2 — “Synthetic Transaction Canary” (health probe + SLO verdict)

**Exemplar pattern:** synthetic monitoring / canary transactions.

### What it is

A tracer bullet that behaves like a synthetic test: it runs a controlled shot and produces an explicit verdict:

- `PASS`: delivered and acknowledged within threshold
- `SOFT_FAIL`: queued but drained later
- `HARD_FAIL`: suppressed, dropped, or timeout waiting for readiness/ack

### Why it makes bottlenecks obvious

Instead of hunting raw events, you get a single outcome with:

- where it failed (stage)
- how long it waited (duration)
- what the system thought readiness was

### Minimal v17.5 payload shape

```js
{
  kind: 'tracer_bullet_venom',
  variant: 'synthetic_canary',
  traceId: 'tb_canary_...',
  thresholds: {
    deliverWithinMs: 50,
    ackWithinMs: 150,
    drainWithinMs: 500
  },
  targetId: 'dino-v1',
  reason: 'canary_probe'
}
```

### Telemetry to emit

- `p3/tracer_canary_start`
- `p3/tracer_canary_verdict` with:
  - `verdict: 'PASS'|'SOFT_FAIL'|'HARD_FAIL'`
  - `failedStage: 'deliver'|'queue'|'flush'|'ack'|null`
  - `durationsMs: { ... }`
  - `queueDepthAtFail`

### Deterministic tests

- Missing iframe: should verdict `SOFT_FAIL` or `HARD_FAIL` (depending on configured timeout), and include queueDepth.
- “Ready iframe” fixture: should verdict `PASS` and report deliver/ack durations.

### When to use

When you want a single “is the pipeline healthy?” signal in CI or during refactors.

---

# Variant 3 — “RED/USE Queue Profiler” (rate/errors/duration + saturation)

**Exemplar pattern:** RED + USE (operational metrics), adapted to a browser pipeline.

### What it is

Instead of focusing on one shot, this variant turns tracer bullets into **metric probes**:

- deliver attempt rate
- deliver error rate
- deliver duration / drain duration histograms
- queue depth / age (saturation)

### Why it makes bottlenecks obvious

If you’re stuck on adapter/iframe readiness, you’ll see:

- queue depth increases
- oldest queue age increases
- drain duration spikes
- deliver error rate rises

### Minimal v17.5 telemetry (aggregated)

Emit an aggregated snapshot every N seconds while enabled:

```js
{
  port: 'p3',
  type: 'tracer_metrics',
  ts: 'ISO',
  windowMs: 2000,
  metrics: {
    deliver_attempts: 12,
    deliver_ok: 3,
    deliver_fail: 9,
    queue_depth_max: 9,
    queue_age_max_ms: 842,
    flush_count: 1,
    flush_duration_ms_p95: 110
  }
}
```

### Deterministic tests

- Force missing iframe → assert `queue_depth_max > 0` and `deliver_fail > 0`.
- Force iframe ready → assert `deliver_ok > 0` and `queue_depth_max === 0`.

### When to use

When the bottleneck isn’t “one bad trace”, but “system degraded over time” during refactors.

---

# Variant 4 — “Chrome Trace Waterfall Export” (Perfetto/DevTools style timeline)

**Exemplar pattern:** Chrome trace event timeline (waterfall visualization), Perfetto.

### What it is

Record tracer bullet stages into an in-memory array that can be exported as a JSON trace (compatible with Chrome/Perfetto tooling). Even without integrating CDP, we can emit “trace-like” events for later viewing.

### Why it makes bottlenecks obvious

The bottleneck becomes visually obvious as gaps between:

- `schedule` → `deliver_attempt`
- `deliver_attempt` → `queued`
- `queued` → `flush`

### Minimal trace event format

Record “complete events” (`ph: 'X'`) per stage:

```js
{
  name: 'gen6.p3.deliverEffect',
  cat: 'hfo',
  ph: 'X',
  ts: 1234567890,   // microseconds
  dur: 2300,        // microseconds
  pid: 1,
  tid: 3,
  args: { traceId: '...', ok: false, queueDepth: 4 }
}
```

### UX recommendation (v17.5)

Add a tiny Port7 control (or console command) while `flag-p3-tracer-trace-export=true`:

- `window.hfoTraceExport.download()` → downloads `trace.json`

### Deterministic tests

- Enable export → run a single synthetic tracer shot → assert trace buffer has ≥ N events and contains traceId.

### When to use

When you want the fastest human comprehension for “what’s stalling?” (waterfall beats logs).

---

## Recommended v17.5 flag surface

Keep deny-by-default, but add a single selector + one export flag:

- `p3-tracer-bullet-venom` (boolean) — master enable (already exists in v17.4)
- `p3-tracer-venom-variant` (string enum) — one of:
  - `trace_context`
  - `synthetic_canary`
  - `metrics_probe`
  - `trace_export`
- Optional:
  - `p3-tracer-trace-export` (boolean) — allow download/export

## Bottleneck signatures (how to read the signals)

- **Immediate suppression**: lots of `p3/tracer_venom_suppressed` ⇒ flags/gating misconfigured (expected deny-by-default).
- **Deliver fails + queued grows**: bottleneck is adapter/iframe readiness.
- **Deliver ok but no ack**: bottleneck is wrapper-side event handling / postMessage / ack path.
- **Schedule delay dominates**: bottleneck is pre-arm calculation / tick cadence / timer jitter.

## Minimal implementation order (keep it surgical)

1) Add Variant 1 (trace_context) because it strengthens *all* other variants.
2) Add Variant 3 (metrics_probe) to see sustained regressions.
3) Add Variant 2 (synthetic_canary) to make CI fail loudly.
4) Add Variant 4 (trace_export) for human debugging sessions.
