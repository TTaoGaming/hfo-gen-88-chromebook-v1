## Executive summary (1-pager): OMEGA / Total Tool Virtualization — Gesture → Ghost Cursor → W3C Pointer Events

### Mission

Build a **replayable, fail-closed control plane** that converts **camera hand tracking** into a **CanonicalPointerState** and drives target GUIs via **Pointer Events semantics**, with “green but meaningless” blocked by **evidence gates**.

### Current reality (already working)

* **Sense→Shape spine exists:** MediaPipe **Hand Landmarker** can output image landmarks, world landmarks, and handedness for a stream. ([Google AI for Developers][1])
* **Smoothing exists:** 1€ filter is a real, well-known interactive-systems filter (CHI 2012). ([Inria Bordeaux][2])
* **Operator shell exists:** GoldenLayout + config UI (per your note). *(No web citation needed; this is your stated state.)*

### Non-negotiable invariants (spec-anchored)

* **No stuck pointer:** any degradation/teardown must terminate the pointer stream using **`pointercancel`** and release capture, consistent with Pointer Events. ([W3C][3])
* **Envelope correctness:** every cross-port message is a valid **CloudEvent** with required attributes (`id`, `source`, `specversion`, `type`). ([GitHub][4])
* **End-to-end traceability:** propagate **W3C Trace Context** (`traceparent`/`tracestate`) so you can correlate actions ↔ shaping ↔ injection ↔ failures. ([W3C][5])
* **Durable replay:** if you use JetStream, **AckExplicit** (or equivalent) is baseline to prevent silent drops. ([NATS Docs][6])

---

## Quorum evidence rule (anti-hallucination / anti-cosmetic)

A claim is “promotion-eligible” only if it has **2-of-3 evidence quorum**:

1. **Normative spec** (W3C / CloudEvents)
2. **Authoritative implementation docs** (vendor/project docs)
3. **Harness evidence** (replay log + receipt + CI artifact)

Examples:

* “Cancel releases capture correctly” ⇒ Pointer Events spec + a replayable test run artifact. ([W3C][3])
* “Event envelopes are valid” ⇒ CloudEvents spec + schema-validation CI logs. ([GitHub][4])

---

## Phased plan with checkpoints (PASS/FAIL, minimal theater)

### Phase 1 — Contract spine (Ports 1↔2 boundary)

**Deliverable:** versioned schemas for `HandFrame` + `CanonicalPointerState` wrapped as CloudEvents + trace context. ([GitHub][4])
**PASS:** 100% boundary validation; invalid payloads are quarantined (no “best effort”).
**FAIL:** any implicit parsing or missing required CloudEvents fields.

### Phase 2 — Record/replay spine (Port 6 minimal)

**Deliverable:** append-only session log + replay runner; JetStream (optional) uses AckExplicit. ([NATS Docs][6])
**PASS:** replay reproduces pointer trajectory within a declared tolerance and emits a receipt `{input_hash, config_hash, version_pin}`.
**FAIL:** “can’t reproduce” or unexplained gaps/duplication.

### Phase 3 — Injection truth path (Port 3) + stuck-pointer tests

**Deliverable:** a real E2E harness that records traces for failures (Playwright trace viewer is a practical standard). ([Playwright][7])
**PASS:** golden tasks (stroke / drag / resize) succeed ≥95% across replays; mid-gesture target switch always triggers safe cancel. ([W3C][3])
**FAIL:** any wedged drag, missing cancel, or non-replayable failure.

### Phase 4 — Disruptor gates: property + mutation (Ports 4/5)

**Deliverable:**

* Property tests that shrink counterexamples (fast-check supports shrinking / readable reports). ([fast-check][8])
* Mutation testing reports with explicit mutant metrics (Stryker). ([Stryker Mutator][9])
  **PASS (Mutant Goldilocks):** mutation score in your band **0.80–0.99** (target 0.88) **on the critical modules** (gating, cancel mapping, injection state).
  **FAIL:** score <0.80, or 1.00 with low mutant count / shallow suite (treat as suspicious).

### Phase 5 — Fail-closed governor + promotion policy (Port 5)

**Deliverable:** policy that blocks promotion unless quorum evidence bundles exist (schemas+traces+mutation+replay receipts).
**PASS:** any confidence collapse / routing handover forces CANCEL and produces a signed decision record. ([MDN Web Docs][10])
**FAIL:** any bypass path that allows actions without an attached gate decision.

---

## Key risk to manage explicitly

**“Synthetic input lies”**: Pointer Events semantics are normative, but many targets won’t accept in-page synthetic events as trusted input; you’ll need an explicit “embedded target” track vs “unmodified target via automation/protocol” track (WebDriver is the standards anchor). ([W3C][11])

---

## Next action (highest ROI)

Implement **Phase 1** (CloudEvents + trace context + schema validation) and immediately wire it to **Phase 2 replay receipts**. This converts the current demo into an auditable system and prevents future “documentation green” from drifting away from runtime truth.

[1]: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?utm_source=chatgpt.com "Hand landmarks detection guide | Google AI Edge"
[2]: https://direction.bordeaux.inria.fr/~roussel/publications/2012-CHI-one-euro-filter.pdf?utm_source=chatgpt.com "A Simple Speed-based Low-pass Filter for Noisy Input in ..."
[3]: https://www.w3.org/TR/pointerevents3/?utm_source=chatgpt.com "Pointer Events"
[4]: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md?utm_source=chatgpt.com "spec/cloudevents/spec.md at main"
[5]: https://www.w3.org/TR/trace-context/?utm_source=chatgpt.com "Trace Context"
[6]: https://docs.nats.io/nats-concepts/jetstream/consumers?utm_source=chatgpt.com "Consumers - NATS Docs"
[7]: https://playwright.dev/docs/trace-viewer?utm_source=chatgpt.com "Trace viewer"
[8]: https://fast-check.dev/docs/tutorials/quick-start/read-test-reports/?utm_source=chatgpt.com "Read test reports | fast-check"
[9]: https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/?utm_source=chatgpt.com "Mutant states and metrics"
[10]: https://developer.mozilla.org/en-US/docs/Web/API/Element/pointercancel_event?utm_source=chatgpt.com "Element: pointercancel event - Web APIs | MDN"
[11]: https://www.w3.org/TR/webdriver2/?utm_source=chatgpt.com "WebDriver"

---
## Executive summary (1-pager)

You have a working **kernel** (GoldenLayout operator UI + MediaPipe landmarks + 1€ smoothed cursor + lil-gui controls). The report’s real objective is to convert that kernel into a **fail-closed, replayable, spec-anchored “gesture → canonical pointer → W3C Pointer Events → target app” control plane** with evidence gates (anti-cosmetic compliance).

### The non-negotiables (what makes it “real” vs “demo”)

1. **Spec-anchored teardown:** any loss of confidence / mode switch / target switch must produce a safe termination (`pointercancel`), and capture state must not be left dangling. Pointer Events explicitly ties `pointerup`/`pointercancel` to clearing pointer capture override state. ([W3C][1])
2. **Contract spine:** every cross-port message is validated and versioned, and wrapped in a standard envelope (CloudEvents) with required context attributes (`specversion`, `id`, `source`, `type`). ([GitHub][2])
3. **Replayable evidence:** record/replay is the truth serum. Use a durable log (JetStream) with explicit acknowledgements to avoid silent drops; use trace propagation so you can correlate operator actions ↔ shaping ↔ injection outcomes. ([NATS Docs][3])
4. **“No fake input” honesty:** if you intend to drive *unmodified* apps, in-page synthetic events often fail the trust boundary (`Event.isTrusted` is false for events created/initialized by script). Plan for WebDriver/Playwright-class injection + artifacts. ([MDN Web Docs][4])
5. **Anti-cosmetic test gates:** mutation testing is an integrity tool, but 100% can be misleading (equivalent mutants). Treat mutation score as a gate *with audit rules*, not a vanity metric. ([Stryker Mutator][5])

---

## Phased approach with checkpoints (and quorum rules)

### Quorum rule (system-wide)

* **ARM (enable actions):** requires **3/3** checks: *(a)* schema-valid CloudEvent, *(b)* trace context present/assigned, *(c)* governor state ARMED and not expired. ([GitHub][2])
* **CANCEL (fail-closed):** triggers on **1/1** critical tripwire (any one is sufficient): confidence collapse, timebase discontinuity, target handover requested mid-interaction, injection error. Map CANCEL → `pointercancel` semantics. ([MDN Web Docs][6])
* **PROMOTE (phase completion):** requires **2/3 evidence quorum**: replay proof, E2E artifact proof, mutation/property proof (details below). ([Playwright][7])

### Phase plan (high signal)

| Phase                                        | Objective                             | PASS checkpoint (hard)                                                                                                                  | Evidence artifacts                                                                       |
| -------------------------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **P0: Kernel receipt**                       | Turn “works” into measurable baseline | Record 30–60s session and replay through SHAPE with bounded divergence; emit receipt `{input_hash, config_hash, version_pin}`           | `sessions/*.jsonl`, `receipts/*.json`                                                    |
| **P1: Contract spine (Port 1)**              | Stop implicit structs                 | 100% cross-port messages are valid CloudEvents **and** schema-valid; invalid → quarantine (no best-effort parsing)                      | `contracts/*.schema.json`, `ce_samples/*.json` ([GitHub][2])                             |
| **P2: Ledger + replay (Port 6)**             | Make every bug replayable             | Durable stream with explicit ACK discipline; replay produces same IDs/order within declared tolerance                                   | JetStream stream/consumer config; replay runner; integrity report ([NATS Docs][3])       |
| **P3: Pointer lifecycle safety (Ports 5→3)** | “No stuck pointer” invariant          | Mid-drag confidence drop or target switch always ends with cancel/teardown; capture not left hanging                                    | “stuck pointer” regression suite; cancel receipts ([W3C][1])                             |
| **P4: Injection truth path (Port 3)**        | Real interactions (not fake events)   | 3 golden tasks (stroke, drag, resize) succeed ≥95% across N replays **using automation-grade injection** when targeting unmodified apps | Playwright traces (`trace.zip`) + screenshots/snapshots for failures ([MDN Web Docs][4]) |
| **P5: Disruptor gates (Port 4)**             | Kill “green but meaningless”          | Mutation gate passes with audit (equivalent mutants acknowledged); property tests produce minimized counterexamples for key invariants  | mutation reports + counterexamples + replay IDs ([Stryker Mutator][5])                   |
| **P6: Navigator hardening (Port 7)**         | Add targets without fragility         | New target added by TargetSpec + adapter, inherits same CANCEL/ARM/PROMOTE quorums and regression gates                                 | `TargetSpec`, handover tests, capability registry                                        |

---

## What to do next (given your current state)

**Do P0 → P1 → P3 in that order** (fastest path to “non-cosmetic”):

1. **P0:** add recording + replay + receipt (local JSONL is fine).
2. **P1:** make every frame a **schema-valid CloudEvent** with required attributes. ([GitHub][2])
3. **P3:** wire your governor so any instability forces CANCEL → `pointercancel`, and prove “no stuck pointer” via replayed tests. ([MDN Web Docs][6])

If your near-term target includes *unmodified apps*, start P4 early: you’ll need Playwright/WebDriver-class evidence (trace viewer, screenshots, snapshots) to debug and to prevent self-deception. ([Playwright][7])

---

## Reference anchors (auditable)

* **W3C Pointer Events** (capture + cancel teardown semantics). ([W3C][1])
* **MDN `pointercancel`** (cancel meaning/trigger conditions). ([MDN Web Docs][6])
* **CloudEvents spec** (required attributes). ([GitHub][2])
* **NATS JetStream consumers** (AckPolicy / AckExplicit). ([NATS Docs][3])
* **OpenTelemetry context propagation** (correlation across boundaries). ([OpenTelemetry][8])
* **MDN `Event.isTrusted`** (why in-page synthetic injection doesn’t generalize). ([MDN Web Docs][4])
* **Playwright Trace Viewer** (trace.zip artifacts; screenshots/snapshots). ([Playwright][7])
* **Stryker mutation testing docs** (mutation score caveats; equivalent mutants). ([Stryker Mutator][5])

[1]: https://www.w3.org/TR/pointerevents/ "Pointer Events"
[2]: https://raw.githubusercontent.com/cloudevents/spec/main/cloudevents/spec.md "raw.githubusercontent.com"
[3]: https://docs.nats.io/nats-concepts/jetstream/consumers "Consumers | NATS Docs"
[4]: https://developer.mozilla.org/en-US/docs/Web/API/Event/isTrusted "Event: isTrusted property - Web APIs | MDN"
[5]: https://stryker-mutator.io/docs/stryker-js/introduction/ "Introduction | Stryker Mutator"
[6]: https://developer.mozilla.org/en-US/docs/Web/API/Element/pointercancel_event "Element: pointercancel event - Web APIs | MDN"
[7]: https://playwright.dev/docs/trace-viewer "Trace viewer | Playwright"
[8]: https://opentelemetry.io/docs/concepts/context-propagation/ "Context propagation | OpenTelemetry"

---
# Executive summary (1-pager): 8-port “Gesture → Ghost Cursor → W3C Pointer Events → Target GUI” control plane

## What you have now (credible baseline)

* **Operator shell (Port 7)**: GoldenLayout + lil-gui panels (live tuning surface).
* **Sense→Shape spine (Ports 0→2)**: MediaPipe landmarks → **One-Euro smoothed cursor** (your “ghost cursor” is already real and controllable).

Your next risk is not “better smoothing.” It’s **proof, safety, and portability**: contracts, replay, teardown correctness, and an injection path that works beyond your own sandbox.

---

## Non-negotiable invariants (fail-closed, not “best effort”)

1. **Contract integrity at every boundary**

   * Every cross-port message is a **CloudEvent** with required context attributes (`specversion`, `type`, `source`, `id`) and a strict schema for `data`. 
2. **End-to-end correlation**

   * Every event carries trace context (W3C TraceContext is the default in many OTel setups), so you can tie: operator action → shaping → injection → outcome. ([OpenTelemetry][1])
3. **No “stuck pointer” ever**

   * Any loss of tracking / target switch / instability must force a safe teardown using **Pointer Events lifecycle rules**. Pointer capture must be released after `pointerup` / `pointercancel`. ([W3C][2])
4. **Replayable evidence is the source of truth**

   * If you can’t replay it, you can’t promote it. Durable streaming should enforce explicit acknowledgements (no silent drops). ([NATS Docs][3])
5. **Truth about “injection”**

   * In-page `dispatchEvent()` produces events that are typically **not trusted** (`isTrusted=false`), so it’s not a valid “works in real apps” claim. ([OpenTelemetry][1])
   * Use a real input driver (e.g., Playwright’s input APIs) when validating “unmodified target” paths. ([Playwright][4])

---

## Evidence quorum model (prevents “green but meaningless”)

For any promotion checkpoint, require **2-of-3**:

* **Spec anchor** (normative behavior + citation)
* **Replay proof** (session log + deterministic-ish output + hashes)
* **E2E artifact** (Playwright trace/video + action receipts + failure reproduction recipe)

No single artifact is sufficient alone.

---

## Phased approach with checkpoints (pass/fail)

### Phase 0 — Baseline replay (you should do this first)

**Goal:** “same input session → same shaped cursor” (within declared tolerance).
**Checkpoint (PASS):** record 60s of `{landmarks → shaped cursor}` and replay to reproduce trajectory; emit `Receipt{input_hash, config_hash, build/version}`.

### Phase 1 — Port 1 “contract spine” (CloudEvents + schema + trace)

**Goal:** eliminate implicit structs and silent drift.
**Checkpoint (PASS):** 100% of cross-port messages validate as CloudEvents with required attributes. 
**Also:** trace context present on every hop. ([OpenTelemetry][1])

### Phase 2 — Port 6 “ledger spine” (durable record/replay)

**Goal:** every bug is replayable and explainable (gaps/dupes/out-of-order become detectable).
**Checkpoint (PASS):** consumer requires explicit ack discipline; missing acks are visible and actionable. ([NATS Docs][3])

### Phase 3 — Port 3 “truth path” injection (controlled target first)

**Goal:** execute 3 “golden tasks” in a target you control (embedded/fork).
**Golden tasks:** draw stroke, drag object, resize.
**Checkpoint (PASS):** ≥95% success across N replays + action receipts.

### Phase 4 — Port 5 governor (ARM/DISARM/CANCEL wired to real teardown)

**Goal:** instability cancels *by construction*.
**Checkpoint (PASS):** mid-drag confidence collapse always triggers cancel + release of capture; no wedged interactions. Pointer capture release after cancel is required behavior. ([W3C][2])

### Phase 5 — Unmodified targets (realistic external integration)

**Goal:** “works on apps you didn’t write.”
**Checkpoint (PASS):** same golden tasks using a real input driver; do **not** claim success based on `dispatchEvent` (untrusted). ([OpenTelemetry][1])

---

## Immediate next step (highest leverage)

Implement **Phase 0 + Phase 1** as a hard gate:

* `HandFrame` + `CanonicalPointerState` schemas
* CloudEvents envelope everywhere (required attrs) 
* Trace context propagation everywhere ([OpenTelemetry][1])
* Replay receipts + hashes

That turns every later debate (“does it really work?”) into an evidence query instead of an argument.

[1]: https://opentelemetry.io/docs/concepts/context-propagation/ "Context propagation | OpenTelemetry"
[2]: https://www.w3.org/TR/pointerevents/ "Pointer Events"
[3]: https://docs.nats.io/nats-concepts/jetstream/consumers "Consumers | NATS Docs"
[4]: https://playwright.dev/docs/input "Actions | Playwright"
---
## Executive summary (1-pager)

### Mission

Deliver a **gesture → ghost cursor → W3C Pointer Events** control plane that can drive real GUIs, with **replayable evidence** and **fail-closed safety** (no “green but meaningless” demos).

### Current baseline (confirmed)

You already have an operator shell and the core “Sense→Shape” path:

* **Operator UI:** GoldenLayout + live tuning panels (lil-gui class UX).
* **Sense:** MediaPipe Hand Landmarker producing **handedness + landmarks (image + world)**. ([Google AI for Developers][1])
* **Shape:** One-Euro smoothing on the cursor signal (your existing work lives here).

### What still needs to become “hard truth” (not prose)

The missing pieces are not more smoothing; they are **contracts, evidence, and teardown correctness**:

* **Contract/envelope spine (Port 1):** every cross-port message is a valid **CloudEvent** with the required context attributes (`specversion`, `id`, `source`, `type`) and versioned schemas. ([GitHub][2])
* **Trace correlation:** propagate **W3C Trace Context** (traceparent/tracestate) end-to-end so any failure is attributable. ([W3C][3])
* **Lifecycle safety:** enforce Pointer Events teardown invariants; after `pointerup`/`pointercancel`, capture overrides must be cleared and pending capture processed. ([W3C][4])
* **Replay ledger:** durable record/replay with explicit acknowledgement semantics (JetStream `AckExplicit`). ([NATS Docs][5])

---

## Phased approach with checkpoints (evidence-first)

### Phase 0 — Replayable kernel (Sense→Shape)

**Output:** `HandFrame[] → CanonicalPointerState[]` recorded as JSONL + config/version hashes.
**Checkpoint (PASS):** replay produces **bounded-divergence** identical outputs under fixed config (tolerance declared).
**Evidence quorum Q0 (2/2):** `{session log}` + `{replay receipt (hashes + tolerance report)}`.

### Phase 1 — Contract spine (Port 1 becomes real)

**Output:** schemas + CloudEvents envelope + trace injection.
**Checkpoint (PASS):** 100% messages validate and include required CloudEvents attributes. ([GitHub][2])
**Evidence quorum Q1 (3/3):**

1. `{schema validation report}`, 2) `{CloudEvents conformance samples}`, 3) `{trace correlation proof (traceparent present across ports)}`. ([W3C][3])

### Phase 2 — Ledger + deterministic replay (Port 6 minimal)

**Output:** append-only event log + replay runner (rate=recorded vs asap).
**Checkpoint (PASS):** every consumer uses explicit ack discipline (no silent drops) and replay reproduces the same session semantics. ([NATS Docs][5])
**Evidence quorum Q2 (3/3):**

1. `{JetStream consumer config/receipts}`, 2) `{gap/dup/out-of-order integrity report}`, 3) `{replay equivalence receipt}`. ([NATS Docs][5])

### Phase 3 — Pointer lifecycle safety (Port 5→3 “no stuck pointer”)

**Output:** ARM/DISARM/CANCEL governor + “safe teardown always” mapping.
**Checkpoint (PASS):** forced cancel **never** leaves capture/drag wedged; `pointerup`/`pointercancel` always terminates cleanly. ([W3C][4])
**Evidence quorum Q3 (2/2):** `{stuck-pointer regression suite}` + `{proof logs showing teardown steps executed}`. ([W3C][4])

### Phase 4 — Injection truth path (Port 3, real target)

**Output:** a target adapter and golden tasks executed via an automation-grade path with artifacts.
**Checkpoint (PASS):** ≥95% success on 3 golden tasks across replay sessions; each run emits trace + artifacts (Playwright trace viewer workflow). 
**Evidence quorum Q4 (3/3):**

1. `{success-rate report}`, 2) `{trace artifacts}`, 3) `{action receipts tied to trace IDs}`. 

### Phase 5 — Anti-cosmetic verification (Ports 4/5 gates)

**Output:** property-based adversarial generators + mutation testing + policy-as-code promotion.
**Checkpoint (PASS):**

* property tests find + **shrink** counterexamples (fast-check style). ([Playwright][6])
* mutation testing reports meaningful outcomes (e.g., distinguish Survived vs NoCoverage) and blocks promotion when coverage is fake. ([GitHub][7])
* promotion enforced by policy-as-code (OPA) + CI gate (Conftest). 
  **Evidence quorum Q5 (3/3):** `{counterexample corpus}`, `{mutation reports}`, `{policy decision logs}`. ([Playwright][6])

---

## Immediate next step (highest leverage)

Implement **Phase 1 + Phase 2** before more UX or filtering work:

1. Define `HandFrame` and `CanonicalPointerState` schemas and wrap every boundary hop as a **CloudEvent** with required attributes. ([GitHub][2])
2. Add W3C Trace Context propagation from ingress through shaping to injection receipts. ([W3C][3])
3. Stand up record/replay with explicit ack semantics (JetStream `AckExplicit`) and produce replay receipts. ([NATS Docs][5])

Once those are in place, every later improvement (targets, smoothing presets, governor logic) is measurable and promotable under quorums, instead of debated.

[1]: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker "Hand landmarks detection guide  |  Google AI Edge  |  Google AI for Developers"
[2]: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md "spec/cloudevents/spec.md at main · cloudevents/spec · GitHub"
[3]: https://www.w3.org/TR/trace-context/ "Trace Context"
[4]: https://www.w3.org/TR/pointerevents/ "Pointer Events"
[5]: https://docs.nats.io/nats-concepts/jetstream/consumers "Consumers | NATS Docs"
[6]: https://playwright.dev/docs/trace-viewer "Trace viewer | Playwright"
[7]: https://github.com/stryker-mutator/stryker-js/blob/master/docs/configuration.md?utm_source=chatgpt.com "stryker-js/docs/configuration.md at master"

---
# Executive summary (1-pager): Gesture → Ghost Cursor → W3C Pointer Events (8-port vertical slice)

## Mission

Build a **daily-driver, fail-closed gesture control plane** that turns **MediaPipe hand landmarks** into a **canonical ghost cursor** and then into **standards-correct pointer interactions** in target GUIs, with **record/replay evidence** and **anti-cosmetic gates**.

You already have the kernel: **GoldenLayout operator UI + lil-gui settings**, **MediaPipe landmarks**, and **One Euro–smoothed cursor**. ([W3C][1])

---

## Ground truth constraints (what “real” must mean)

* **Pointer lifecycle must never wedge**: when you cancel, you must unwind capture/drag state. Pointer Events defines **implicit release of pointer capture after `pointerup` or `pointercancel`** and processing of pending capture changes.
* **Synthetic DOM events are not a general injection strategy**: programmatically created events will be `isTrusted === false`, so many apps/UA paths will treat them differently than real input. ([GitHub][2])
* **To drive unmodified targets reliably**, you need an automation/input channel (WebDriver / Playwright-style actions), not “dispatchEvent theater.” 
* **Evidence must be replayable**: JetStream consumers track delivery/acks and can provide at-least-once behavior when acknowledgements are required; Ack policy is explicitly configurable. ([NATS Docs][3])
* **Cross-port contracts must be explicit**: CloudEvents requires core context attributes (`specversion`, `id`, `source`, `type`) so every hop is attributable and replayable. ([GitHub][4])
* **End-to-end correlation requires propagation**: OpenTelemetry propagation exists specifically to carry context across boundaries. ([GitHub][5])

---

## Phased approach with checkpoints (pass/fail) + evidence quorums

### Phase 0 — **Baseline kernel (you have this)**

**Goal:** landmarks → smoothed cursor → operator UI rendering + parameter control.
**PASS:** stable cursor under normal motion; confidence loss yields “no action” (not noise).
**Evidence quorum Q0 (2/2):** (a) recorded session file, (b) config/version receipt (hashes).

### Phase 1 — **Contract spine (Port 1)**

**Goal:** every boundary is **schema-validated + enveloped + traceable**.
**Implement:** canonical messages (`HandFrame`, `CanonicalPointerState`, `GateDecision`, `ActionReceipt`) wrapped as CloudEvents. ([GitHub][4])
**PASS:** 100% boundary validation; invalid payloads quarantine (no “best effort”).
**Evidence quorum Q1 (3/3):**

1. schema validation receipt,
2. CloudEvents compliance receipt (required attrs), ([GitHub][4])
3. trace context present/created at ingress. ([GitHub][5])

### Phase 2 — **Record/replay ledger (Port 6 minimal)**

**Goal:** “every bug is replayable.”
**Implement:** append-only event log + replay runner; if using JetStream, configure consumer ack policy intentionally (don’t allow silent drops). ([NATS Docs][3])
**PASS:** replay reproduces shaped output within declared tolerance; gaps/dupes/out-of-order are detected and reported.
**Evidence quorum Q2 (3/4):**

* (a) replay equivalence report,
* (b) ledger integrity report,
* (c) JetStream consumer config captured (AckPolicy etc.), ([NATS Docs][3])
* (d) trace correlation across replay. ([GitHub][5])

### Phase 3 — **Injection truth path (Port 3) against 1 controlled target**

**Goal:** pointer semantics in a real GUI with **no stuck pointer**.
**Implement:** Playwright/WebDriver actions as the “truth path” for unmodified targets. ([Playwright][6])
**PASS:** 3 golden tasks (draw, drag, resize) succeed ≥95% across N replays; **any cancel leaves no capture/drag wedge**. ([GitHub][2])
**Evidence quorum Q3 (3/3):**

1. Playwright trace/video artifact per run (Trace Viewer),
2. action receipts tied to traces,
3. stuck-pointer invariant tests (includes cancel paths).

### Phase 4 — **Fail-closed governor (Port 5)**

**Goal:** degrade → **CANCEL by construction**, not by logs.
**Implement:** ARM/DISARM/CANCEL FSM; CANCEL maps to pointercancel + teardown semantics. (MDN documents when `pointercancel` can fire; spec defines capture release semantics.) ([MDN Web Docs][7])
**PASS:** any confidence collapse / target switch / injection error forces CANCEL and produces a DefenseReceipt.
**Evidence quorum Q4 (3/4):**

* (a) defense decision log,
* (b) cancel-path E2E proof,
* (c) replay reproduces same cancel decision,
* (d) trace correlation.

### Phase 5 — **Disruptor harness (Port 4): property + mutation + replay**

**Goal:** eliminate “green but meaningless.”
**Implement:** property-based generators for dropout/jitter/occlusion with shrinking (fast-check explicitly warns that side effects can break shrinking—so keep properties pure). ([fast-check][8])
**Mutation testing:** define a **promotion floor** (your 0.80) for critical modules; mutation score is a standard metric, and ~80% is commonly discussed as a pragmatic target due to equivalent mutants. ([Stryker Mutator][9])
**PASS:** mutation ≥ floor on shaping/governor/injector mapping; minimized counterexamples are replayable.

### Phase 6 — **Navigator (Port 7): target registry + safe handover**

**Goal:** GoldenLayout becomes a real control plane: **teardown → SAFE_IDLE → validate → enable**.
**PASS:** mid-gesture target switch cannot strand a pointerdown/capture state (validated by the same invariant suite).

---

## Recommended next move (highest leverage, given your current state)

1. **Phase 1 (contracts + CloudEvents + trace)**, then
2. **Phase 2 (record/replay with integrity reports)**, then
3. **Phase 3 (one target via Playwright/WebDriver actions + traces)**. ([GitHub][4])

This sequence forces reality early: every later optimization (physics/Kalman presets, multi-target routing, JetStream scaling) becomes measurable and falsifiable.

---

## References (primary anchors used)

Pointer Events (capture/cancel lifecycle)
CloudEvents required attributes ([GitHub][4])
NATS JetStream consumers + AckPolicy ([NATS Docs][3])
OpenTelemetry propagation ([GitHub][5])
MDN `isTrusted` ([GitHub][2])
WebDriver spec + Playwright input + Trace Viewer 
MediaPipe Hand Landmarker ([W3C][1])
One Euro filter (reference implementation background) ([Géry Casiez][10])
fast-check shrinking caveat ([fast-check][8])
Mutation score target discussion ([Stryker Mutator][9])

[1]: https://www.w3.org/TR/pointerevents/?utm_source=chatgpt.com "Pointer Events"
[2]: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md "spec/cloudevents/spec.md at main · cloudevents/spec · GitHub"
[3]: https://docs.nats.io/nats-concepts/jetstream/consumers "Consumers | NATS Docs"
[4]: https://raw.githubusercontent.com/cloudevents/spec/main/cloudevents/spec.md "raw.githubusercontent.com"
[5]: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md?utm_source=chatgpt.com "spec/cloudevents/spec.md at main"
[6]: https://playwright.dev/docs/input "Actions | Playwright"
[7]: https://developer.mozilla.org/en-US/docs/Web/API/Element/pointercancel_event "Element: pointercancel event - Web APIs | MDN"
[8]: https://fast-check.dev/docs/core-blocks/properties/ "Properties | fast-check"
[9]: https://stryker-mutator.io/docs/stryker-net/configuration/?utm_source=chatgpt.com "Configuration"
[10]: https://gery.casiez.net/1euro/ "1€ Filter"

---