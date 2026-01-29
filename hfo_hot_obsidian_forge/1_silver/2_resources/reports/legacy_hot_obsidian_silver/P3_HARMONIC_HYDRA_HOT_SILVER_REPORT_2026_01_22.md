<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
<!--
Medallion: Silver | Mutation: 0% | HIVE: V
Provenance: Synthesized from existing HFO in-repo artifacts + user directive (2026-01-22).
Scope: Port 3 doctrine + escalation battery spec; implementation details remain in Bronze.
-->

# Port 3 — Harmonic Hydra (formerly “Spore Storm”): Hot Silver Report

Date: 2026-01-22

## Executive intent

Port 3 (“INJECT”) evolves from the older alias **Spore Storm** into **Harmonic Hydra**: a many-headed, regenerative effect-delivery commander that can deploy a **battery** of specialized “venom” payloads (nematocysts + other modalities) with **octal escalation**.

The core goal is to out-scale a propagating incident/problem by saturating the CYNEFIN **complex** domain with safe, diverse probes that rapidly produce evidence.

## Grounding anchors (repo evidence)

- P3 battery doctrine (multi-shot, multi-modality):
  - hfo_hot_obsidian/silver/4_archive/20260122_102102_P3_HARMONIC_HYDRA_INJECTION_BATTERIES_SPEC_2026_01_21.md
- P3 “Pareto 8” diagnostic nematocyst battery (detailed payload styles + events + flags):
  - hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/HFO_GEN6_P3_HARMONIC_HYDRA_NEMATOCYST_DIAGNOSTIC_BATTERY_2026_01_22.md
- Tracer bullet venom evolution patterns (trace/canary/metrics/export):
  - hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/GEN6_V17_5_TRACER_BULLET_VENOM_VARIANTS_REPORT_2026_01_22.md
- Tripwire lookahead + P3 inject contract (fail-closed, schema-checked):
  - contracts/hfo_tripwire_events.zod.ts

## The myth translated into engineering constraints

Hydra traits are not “flavor”; they are invariants that keep Port 3 safe and useful.

- **Many-headed** ⇒ multiple independent injection heads can run in parallel without shared failure.
- **Harmonic** ⇒ heads coordinate via rhythm/phase (timed salvos, interleaving, resonance windows).
- **Regenerative** ⇒ if one head fails (suppressed, blocked, wrong target), the system can regrow new heads without losing auditability.
- **Venom battery** ⇒ not one payload style; a set of purpose-built probes with distinct signatures.
- **Nematocyst strike semantics** ⇒ precise discharge with explicit ACK/telemetry of “strike landed”.
- **Durable + governed** ⇒ deny-by-default, fail-closed, bounded blast radius, receipts.

## What “battery” means in Port 3

A **battery** is the Port 3 unit of work:

- **Composition:** 2..N injections per battery.
- **Variety:** batteries mix payload styles (not just repeated shots).
- **Telemetry:** every injection emits structured events; the battery emits a roll-up verdict.
- **Safety posture:** missing ACKs are explicit failures; silent success is forbidden.

This is consistent with the existing Silver spec:

- “Never one shot” and “many injector modalities” are non-negotiables.

## Octal escalation: $8^N$ means “combinatorics over 8 venom classes”

In Harmonic Hydra doctrine, $8^N$ is not “one venom in $N$ stages”. It is the scaling law for **how many venom programs you can express by composing 8 primitive venom classes**.

- $8^0$ = one minimal probe (the cheapest “is anything alive?” pulse).
- $8^1$ = **8 distinct classes** of venoms (a palette).
- $8^2$ = up to **64** two-venom compositions (ordered sequences of length 2).
- $8^k$ = $8^k$ possible ordered compositions of length $k$.

Escalation is governed: the Hydra can increase *probe diversity* and *search breadth* without increasing unsafe/destructive effects.

### The 8 venom classes (the palette; $8^1$)

These are **classes**, not a fixed list of one-off payloads. Each class has exemplar implementations in the existing Gen6 battery docs, but the class is broader than the exemplar.

1) **Sanity/Canary venoms** — single verdict, fast health pulse.

- Exemplar anchor: “Synthetic Canary Verdict Shot”.

2) **Trace/Span venoms** — correlation-first stage timing and attribution.

- Exemplar anchor: “Trace-Span Chain Shot” and tracer span events.

3) **Backpressure/Queue venoms** — saturation imaging (depth/age/drain).

- Exemplar anchor: “Queue Ultrasound Probe” + RED/USE profiler variant.

4) **Export/Waterfall venoms** — human-readable timelines (Chrome-trace style).

- Exemplar anchor: “Waterfall Trace Export Shot”.

5) **Protocol/Ordering venoms** — W3C pointer packet integrity (ordering/capture).

- Exemplar anchor: “W3C Pointer Packet Shot”.

6) **Minimal-substrate venoms** — deterministic low-DOF probes (keyboard packet, no DOM dependency).

- Exemplar anchor: “Keyboard Packet Shot”.

7) **Boundary/Handshake venoms** — adapter/iframe boundary proof (echo, RTT, ack paths).

- Exemplar anchor: “Adapter Handshake / Echo Shot”.

8) **Target/Biopsy venoms** — hit-test + DOM/capture biopsy for precise target verification.

- Exemplar anchor: “DOM Target Biopsy Shot”.

### $8^2$ and beyond — batteries as composed venom programs

A **battery** is an ordered composition of venoms chosen from the palette.

Example compositions (illustrative):

- $8^0$ (single pulse): Sanity/Canary
- $8^2$ (two-step): Trace/Span → Backpressure/Queue
- $8^3$ (three-step): Sanity/Canary → Boundary/Handshake → Trace/Span
- $8^k$ (search): many small batteries spawned in parallel, each testing a disjoint hypothesis.

The Hydra’s “many heads” are parallel batteries, not a single long scripted chain.

## DSE fractal octree chunking: identity search across large domains

Harmonic Hydra is the Port 3 answer to identity/root-cause discovery in large, high-dimensional domains:

- DSE posture: propose safe probes → measure signals → update hypotheses.
- Fractal octree posture: chunk the domain into 8 parts, probe each chunk, then **recurse** on the chunk(s) that carry signal.

### What “identity problem” means here

An identity problem is “we don’t know which boundary is failing” (or which one dominates): injector vs adapter vs target vs queue vs ack vs timing vs gating vs schema.

### Octree chunking loop (high-level)

1) **Define the search space** (the domain): e.g., pipeline boundaries P2→P3→AdapterHost→Queue→Flush→Ack.
2) **Choose 8 chunk axes** for one level of partition:

- readiness boundary, queue/flush, ack path, target mapping, protocol ordering, timing jitter, contract/schema, suppression/gating.

3) **Deploy one small battery per chunk** (parallel heads), using the venom class best suited to discriminate that chunk.
2) **Score signal strength** (verdicts, stage gaps, error rates, missing acks) and select the top chunk(s).
3) **Recurse**: subdivide the winning chunk into 8 sub-chunks and repeat until the root cause is isolated.

Stop conditions (governed):

- Evidence threshold met (dominant bottleneck identified with repeatable signal).
- Budget exceeded (time, attempts, queue growth, error budget).
- Safety tripwire triggers (COAST/low-confidence, deadman, suppression storms).

## Hydra intelligence: exemplar primitives + tool-driven composition

Hot Silver doctrine target: the “AI powering Harmonic Hydra” should not be handed a brittle fixed list of 8 payloads; it should be given **exemplar primitives** and a governed composition interface so it can synthesize new venoms on demand.

### Venom primitive contract (conceptual)

Each venom (or battery) should be representable as:

- **Class:** one of the 8 venom classes (palette).
- **Intent:** what ambiguity it resolves (which chunk it discriminates).
- **Target selector:** adapterId/targetId/DOM selector/etc.
- **Correlation:** `traceId` propagation (non-PII).
- **Emissions:** a stable set of port/type telemetry events.
- **Guards:** flags, rate limits, cooldowns, queue caps, and fail-closed defaults.
- **Verdict mapping:** how emitted signals roll up into PASS/SOFT_FAIL/HARD_FAIL.

### Tool-driven composer (conceptual)

Given the above, a composer can:

- Generate a battery template for a hypothesis.
- Choose venoms that maximize discrimination (information gain) while minimizing blast radius.
- Run the octree loop and produce a compact evidence rollup (with links/exports).

## CYNEFIN alignment (how the Hydra saturates “complex” safely)

Hydra is designed for complex domains where cause/effect is only coherent *after* probing:

- **Obvious:** $8^0$ pulses are sufficient (simple PASS/FAIL with clear remediations).
- **Complicated:** $8^1$ tracing + $8^2$ profiling isolate the bottleneck for expert diagnosis.
- **Complex:** run $8^3$ multi-modal biopsy batteries across multiple hypotheses; prefer many safe probes over a single “clever” probe.
- **Chaotic:** Hydra remains fail-closed; it can increase observation density, but must not increase destructive actions.

## Governance, durability, and tripwire safety

Hydra is only viable if it is safe for the hydra.

### Fail-closed / deny-by-default

- Every venom/battery is behind explicit enablement flags.
- When disabled, emit suppression telemetry (so “nothing happened” is still observable).

Anchor: tracer venom gating patterns (deny-by-default) in the v17.4/v17.5 reports.

### Contract boundaries

- Cross-port messages and injected payloads must be schema-validated.
- Tripwire-derived P3 inject events already have a Zod contract:
  - `P3TripwireInjectV1Schema` in contracts/hfo_tripwire_events.zod.ts

### Bounded blast radius

- Prefer deterministic, low-degree-of-freedom probes first (keyboard packet, synthetic canary).
- Only run DOM/pointer biopsies when explicitly requested by the battery template.
- Rate-limit attempts and cap queue growth; treat runaway as a HARD_FAIL.

### Receipts and auditability

- Every battery should produce:
  - per-injection ACK/failure classification
  - a rollup verdict
  - an exportable trace buffer when explicitly enabled

This keeps Port 3 compatible with “immutable provenance” expectations.

## The Hydra venom battery (Pareto 8)

Port 3 should maintain a “Pareto 8” set of venoms that cover most diagnosis needs.

Canonical set (grounded in the existing Bronze battery doc):

1) Trace-Span Chain Shot
2) Synthetic Canary Verdict Shot
3) Queue Ultrasound Probe
4) Waterfall Trace Export Shot
5) W3C Pointer Packet Shot
6) Keyboard Packet Shot
7) Adapter Handshake / Echo Shot
8) DOM Target Biopsy Shot

## What is known vs missing (drift control)

Known (grounded):

- Port 3 is already modeled as injection/effect delivery with tripwire-driven inject events and deny-by-default gating patterns.
- The “Pareto 8” diagnostic battery is already specified with event names and recommended flags.

Missing (needs follow-up to harden to Gold):

- A single canonical “Battery/Injection/ACK” schema in contracts/ (Silver-level integration target).
- A unified, version-independent “battery runner” API with strict adapter boundary semantics.
- A minimal rollup format suitable for DuckDB/telemetry ingestion (Port 6).

Next grounded steps:

- Promote the Battery/Injection/ACK schema into contracts/ and enforce it in the injector path.
- Add a small set of Playwright specs that assert: suppression telemetry exists when disabled, and deterministic verdicts exist when enabled.
