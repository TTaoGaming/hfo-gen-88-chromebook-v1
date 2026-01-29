<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
# Omega GEN7 deep research: architecture, capabilities, and SOTA comparison for mobile input microkernel systems

## Evidence base and auditability boundaries

This assessment is grounded in the artifacts you provided locally in this chat session:

- `omega_gen7_v3_spec.yaml`, `omega_gen7_v1.html`, `omega_gen7_v2.html`, `omega_gen7_v3.html`
- `README.md`
- Playwright specs: `omega_gen7_v1_portable_smoke.spec.ts`, `omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts`, `omega_gen7_v1_portable_dino_runner.spec.ts`

Because the current conversation tooling does **not** expose your uploaded files through the citation system (the file-index tool reports no retrievable sources), I **cannot attach line-precise citations** to statements about your internal implementation. To keep this “zero-trust,” I will (a) explicitly mark which claims come from those local artifacts, (b) quote small, auditable snippets where useful, and (c) provide **proper citations only for external SOTA** sources (W3C, Apple/Android docs, academic and major OSS projects).

## Your current architecture and capabilities

### What “microkernel-like” means in Omega GEN7 today

From your spec and v3 runtime, Omega GEN7 is best described as an **application-level microkernel pattern**: a small “kernel” (global system state + configuration + contracts) orchestrates modular subsystems (“ports”) that can be toggled and evolved independently via feature flags. This echoes the *architectural pattern* of microkernels (minimal core + replaceable services), but it is not an OS microkernel in the isolation/IPCs sense (I compare those explicitly later).

Two design moves are especially microkernel-ish:

**A port-based pipeline with explicit boundaries.** Your spec formalizes four top-level ports (P1 Fuse, P2 Shape, P3 Deliver, P7 Navigate). In effect, the kernel’s job is to stabilize: time, identity, state transitions, and delivery contracts; services can be swapped behind each port without rewriting the rest of the system.

**A feature-flagged evolution posture.** Your spec’s flag provider is OpenFeature-backed, with URL query overrides (e.g., `flag-p3-tripwire-injector-fingertips=true|false`). This is an unusually strong stance for an input system because it enables A/B-style experimentation and regression control at architectural seams. OpenFeature’s goal is specifically to provide a **vendor-agnostic, language-agnostic** flagging API/specification. citeturn6search6turn6search2

### Gesture Port 1 bridge and the shared Data Fabric

From `omega_gen7_v3.html`, your runtime defines a `DataFabricSchema` (Zod) containing:

- `cursors`: an array of fused cursor/hand objects (your “FusionSchema”)
- `systemTime` and `frameId`

You additionally define a “Universal Fabric Envelope” described as **CloudEvents-inspired**, with envelope fields such as `specversion`, `id`, `type`, and `source` (local-only in your comment).

This is architecturally important: you are effectively event-sourcing the input world state into a **typed, replayable** snapshot stream. Most mobile input stacks do not provide an externally inspectable “fabric” abstraction; they provide callbacks (Android/iOS) or DOM events (web).

A useful SOTA comparator for your envelope choice is **CloudEvents**, which is a CNCF-hosted specification intended to standardize event metadata across systems. CloudEvents is now a CNCF “Graduated” project, and its core value proposition is interoperable event metadata (the “context”) independent of transport. citeturn10search2turn10search4 The CloudEvents spec defines required attributes including `id`, `source`, `specversion`, and `type`. citeturn10search5

**Where you’re already ahead (architecturally):** adopting an envelope+payload discipline for input events is uncommon in gesture systems; it directly enables deterministic replay, CI-friendly regression tests, and adapter-level audit trails.

### Anti-Midas + dwell/leaky bucket hysteresis in your FSM

From your v3 runtime (local artifact), your P2 FSM uses:

- A **readiness energy** mechanism updated as a leaky bucket: fill proportional to `dt/chargeTimeMs`, drain proportional to `dt/releaseTimeMs`, with a separate slower drain time in COAST (`coastDrainTimeMs`) and a `coastDrainMultiplier`.
- Two thresholds for hysteresis (`hysteresisHigh` and `hysteresisLow`) controlling transition stability.
- A feature-flagged **anti-Midas READY gate**: when enabled, the READY gate depends on palm-cone orientation (“isFacingCamera”) rather than `(isFacingCamera || isCharging)`.

This choice maps cleanly onto the classic “Midas Touch problem” literature: whenever a modality is “always on,” the system must distinguish **observation** from **intention** to avoid accidental activation. A large gaze-interaction review explicitly calls this out and notes dwell-based activation windows often in the 200–1000ms range depending on context and user needs. citeturn4search1

Your design is essentially a generalized, multi-signal version of that: dwell-ish charging + hysteresis + anti-Midas gating + fail-closed states.

### Planck.js physics as a pointer stabilizer

Your runtime uses Planck.js (local artifact) as a physics substrate for pointer stabilization/smoothing. Planck.js is a JavaScript rewrite of Box2D for HTML5/web/mobile contexts, with an API closely following Box2D and explicit motivation around being optimized for web/mobile. citeturn6search3

This is a credible engineering choice: instead of ad-hoc smoothing, you’re using a well-studied rigid-body/spring model that can be tuned and reasoned about. In SOTA interactive-input practice, the common baseline is often the **1€ (One Euro) filter**, which is explicitly designed to trade jitter vs lag using speed-adaptive cutoff. citeturn4search0turn4search8 You appear to use OneEuro-style filters in parts of your pipeline as well (local artifact).

### W3C pointer implementation and event injection behavior

Your Port 3 injector constructs and dispatches synthetic `PointerEvent`s (`pointerover/enter/down/move/up/out/leave`) and uses `setPointerCapture`/`releasePointerCapture` when available (local artifact).

The relevant SOTA baseline is the W3C **Pointer Events** specification. Pointer Events Level 3 (Candidate Recommendation Snapshot, Nov 6, 2025) explicitly adds:

- `pointerrawupdate` for higher-frequency pointer updates (secure context)
- `getCoalescedEvents()` for un-coalescing motion samples
- `getPredictedEvents()` for built-in prediction (to reduce perceived latency) citeturn5search18turn5search4turn0search2

Critically, the spec also defines that the `PointerEvent` constructor can accept `coalescedEvents` and `predictedEvents` in `PointerEventInit`, cloning them into the constructed event’s lists. citeturn0search1turn0search2

**Key observation for Omega:** you are aligned with the Pointer Events taxonomy and capture semantics, but you are not yet exploiting the Level 3 “high-fidelity” surfaces (coalesced/predicted lists and `pointerrawupdate`). This becomes a clear “falls short of web SOTA” item.

### Single key press/release support

In your v3 spec (local artifact), the Gen7 target behavior is explicit:

- Per-hand 4 fingertip tripwires map to ASDF keys (A/S/D/F as `KeyboardEvent.code`).
- Tripwire **begin → keydown** and **end → keyup** (edge-triggered, “no repeats while held”).
- Gated by feature flag and COMMIT-only (“fail closed”). (Local artifact)

In your current runtime (local artifact), the tripwire pipeline builds a “keyboard” payload including `action: keydown|keyup|keypress`, plus `code` and `key`, and delivers via an adapter mechanism (not a privileged OS-level key injector).

This distinction matters because on the web, synthetic keyboard events are frequently **not trusted** and generally do not trigger default browser actions—MDN notes that synthetic UIEvents are not “trusted” and only trusted events trigger default actions. citeturn1search9 That is why your approach of **wrapper/adapter-controlled actuation** is pragmatic: where you control the target surface (e.g., your Dino wrapper), you can implement reliable key semantics via message passing.

## SOTA baselines in mobile input and microkernel systems

### Mobile input sampling and prediction baselines

**Android MotionEvent batching (sampling fidelity).** Android’s `MotionEvent` explicitly supports batching multiple movement samples into one event; the historical samples are accessed via `getHistoricalX/Y`, while `getX/Y` return the newest sample. citeturn1search0 This is OS-level support for high-fidelity motion reconstruction without increasing callback overhead.

**iOS coalesced + predicted touches (latency reduction).** Apple’s WWDC 2015 “Advanced Touch Input on iOS” describes touch coalescing (deliver once per display frame but include intermediate samples) and predicted touches (deliver a short horizon of future estimates). The session claims an effective latency improvement from ~4 frames (iOS 8) to ~1.5 frames (iOS 9 with low latency modes, coalescing, and prediction), and explains prediction as “highly tuned algorithms” producing future-touch snapshots. citeturn2search2

**Web Pointer Events prediction/coalescing (standardized API surface).** Pointer Events Level 3 standardizes access to coalesced and predicted pointer events lists and defines `pointerrawupdate` for high-frequency updates in secure contexts, while explicitly not standardizing how browsers predict/coalesce—only the API. citeturn0search1turn0search2turn5search18 MDN’s summary of `getPredictedEvents()` highlights that UAs base predictions on history + velocity + trajectory and that apps can “draw ahead” to reduce perceived latency. citeturn5search8

**Research SOTA in prediction accuracy (stylus).** Samsung Research’s 2020 work on latency compensation for active stylus input proposes a GRU-CNN predictor and reports prediction errors of **0.07mm (≈16.6ms), 0.24mm (≈33.3ms), 0.47mm (50ms)**, claiming substantially lower error than LSTM baselines and real-time feasibility (reported ~4ms on Galaxy Note 9). citeturn5search15

This stylus work is a strong “accuracy SOTA” anchor because it provides numeric error by horizon and a concrete device runtime.

### Microkernel OS SOTA: what “microkernel” buys at the systems level

If we define SOTA microkernels by *strong isolation, minimal trusted computing base, and message-passing IPC*, then canonical anchors include:

- **seL4**: machine-checked functional correctness proofs (and additional binary correctness/security properties for some configs), with clear claims about the implications (absence of whole classes of bugs). citeturn3search1turn3search0
- **QNX Neutrino**: a modular microkernel architecture built on message passing; documentation emphasizes that keeping the microkernel minimal bounds non-preemptible paths and pushes heavy work to user processes. citeturn3search3turn3search10
- **Zircon (Fuchsia)**: an object/handle based kernel model where user-mode code interacts with OS resources via handles; Fuchsia docs describe sockets/channels as IPC objects (channels are datagram-oriented and can transfer handles). citeturn3search4turn3search21

These are relevant comparators not because Omega is an OS, but because they define what “microkernel” means at the strongest end of the spectrum—particularly around isolation and IPC semantics.

## Comparative analysis across your requested dimensions

### Latency and prediction accuracy

**Where SOTA is today.** On-device touch/stylus stacks are optimized around (a) high-rate sampling, (b) coalescing/batching, and (c) prediction. Android’s `MotionEvent` batching preserves intermediate samples without extra callbacks. citeturn1search0 Apple’s touch pipeline uses coalesced and predicted touches and claims frame-level latency reductions when fully adopted. citeturn2search2 On the web, Pointer Events Level 3 exposes predicted/coalesced lists and `pointerrawupdate`. citeturn0search1turn0search2turn5search18

**What Omega has today (from local artifacts).** You have two distinct prediction-like elements:

- A **tripwire lookahead window** that schedules (or at least attempts to schedule) actuation earlier than the geometric crossing moment.
- A **physics-based smoothing/prediction** approach (Planck + filters) to mitigate jitter and stabilize the pointer.

Your Playwright regression spec `omega_gen7_v1_portable_tripwire_lookahead_monotonic.spec.ts` asserts that increasing lookahead window increases “lead time” (cross timestamp minus inject timestamp). That is a real, testable “predictive latency” mechanism—just not yet a quantified *accuracy* mechanism.

**Where you plausibly surpass SOTA (conditionally).** If you can demonstrate that your lookahead mechanism delivers lower perceived latency *without increasing false activations* under noisy vision inputs, you may outperform OS baselines in one niche: **camera-based gesture→key orchestration**, where OS stacks don’t offer a built-in concept of “tripwire crossing predicted from hand pose.” OS stacks assume the sensor is touch/stylus hardware with predictable sampling and noise.

**Where you fall short (today, unavoidably and measurably).** A camera/ML pipeline is almost certainly behind direct touch/stylus pipelines in raw latency and accuracy unless you invest heavily in measurement and optimization. Moreover, your current W3C pointer adapter does not expose predicted/coalesced lists, so high-fidelity drawing apps (Excalidraw-like) cannot benefit from the same smoothing quality that iOS coalescing provides or that Pointer Events Level 3 enables. citeturn1search0turn2search2turn0search2

**What you should measure to make this rigorous.** Borrow from “motion-to-photon” measurement practice: high-speed camera + co-registration techniques can quantify end-to-end latency changes across a movement (important because prediction often reduces effective latency mid-movement but is worse at sudden accelerations). A recent open-access VR latency paper shows exactly this: initial latencies of ~21–42ms reduce functionally to ~2–13ms once prediction “catches up,” and the transition happens ~25–58ms after onset. citeturn5search3turn5search0 This is the kind of analysis your system needs, adapted to “gesture-to-photon” and “gesture-to-actuation.”

![Illustrative readiness hysteresis dynamics](sandbox:/mnt/data/omega_readiness_hysteresis_illustrative.png)

*This plot is model-based using the default timing constants observed in your runtime (not a measured trace). It is included to make the hysteresis/latency tradeoff explicit.*

### Gesture recognition, anti-Midas, and hysteresis mechanisms

**SOTA principle.** Always-on modalities require explicit intent disambiguation. The Midas Touch literature argues that dwell-time activation (often hundreds of milliseconds) is a common mitigation but has drawbacks (fatigue, accidental triggers, UI constraints). citeturn4search1turn4search3

**Omega’s approach (from local artifacts).** You’ve implemented a strong “safety doctrine” stack:

- **Leaky-bucket readiness** is a clean abstraction for “intent energy.”
- **Two-threshold hysteresis** reduces oscillation.
- **COAST as a sink state** (drains only) plus deadman timeouts create fail-closed behavior under uncertainty.
- **Anti-Midas READY gate** is feature-flagged, which makes it scientifically tunable rather than ideology.

**Where you already surpass typical systems.** In most commercial mobile gesture recognizers, hysteresis exists but is often buried in heuristics (touch slop, velocity thresholds, gesture cancellation). Your system elevates it into explicit, configurable parameters and ties it to a consistent state machine + contract stream. That’s unusually good for auditability and research iteration.

**Where you likely fall short.** Your architecture will live or die on per-user tuning and robustness under diverse lighting/backgrounds—an area where OS touch/stylus stacks have a huge advantage because their sensors are physically constrained and calibrated. On the web, Pointer Events exposes `pointerId` strategies and device typing (`pointerType`) to help apps reason about input context; if Omega’s injection always presents `pointerType: "mouse"` and a simplistic `isPrimary`, you’ll be leaving accuracy/usability on the table in complex apps. citeturn0search2turn0search1

![Tripwire predictive lead-time expectation](sandbox:/mnt/data/omega_tripwire_lookahead_leadtime.png)

*This chart reflects the monotonic relationship enforced by your Playwright regression expectations; it is not a device latency benchmark.*

### Shared data fabric design and “port_1_bridge” semantics

Your Data Fabric plus envelope mirrors a key CloudEvents idea: separate *context metadata* from *data payload*, and make the metadata consistent. CloudEvents is explicitly about interoperable event metadata across systems. citeturn10search2turn10search4 The spec’s required attributes (`id`, `source`, `specversion`, `type`) give you a strong blueprint for versioning and traceability. citeturn10search5

**Where you surpass SOTA.** The web platform’s input model does not give you a typed, validated “fabric” that you can replay deterministically. It gives you event streams. Android/iOS give callback streams. Your fabric gives you a chance to make input behavior reproducible and testable.

**Where you fall short and what to fix.** CloudEvents-style metadata typically lives in ecosystems where there is also standard tracing propagation (e.g., OpenTelemetry semantic conventions for CloudEvents). citeturn10search6 If you want Omega to become a serious open-source input platform, you should standardize *trace IDs* and “causality links” across ports (P1 frame → P2 decision → P3 delivery), and make them schema-stable. CloudEvents’ emphasis on `source + id` uniqueness is a useful discipline for your fabric event IDs. citeturn10search5

### Integration with Excalidraw, Babylon VFX, and Dino Runner

**Excalidraw integration SOTA considerations.** Excalidraw is MIT-licensed and widely embedded; the modern approach is `@excalidraw/excalidraw` as a component. citeturn9search0turn6search7 Your approach (local artifact) uses wrappers/iframes and a pointer adapter, which is pragmatic for a “universal input layer,” but it introduces version fragility. Excalidraw’s release notes show meaningful packaging changes—e.g., deprecating UMD bundles in favor of ESM and changes in TS module resolution expectations. citeturn6search16  
**Actionable risk:** adapters must be version-pinned and CI-tested against known Excalidraw releases.

**Babylon VFX integration SOTA considerations.** Babylon.js is a major open rendering engine (Apache-2.0). citeturn7search1turn7search0 It is evolving quickly (e.g., Babylon.js 8.0 adds a “Node Render Graph” and includes WGSL shader improvements for WebGPU). citeturn7search6  
**Actionable risk:** intensive VFX on the main thread can sabotage input responsiveness unless you aggressively budget frame time and test under load.

**Dino Runner integration.** Your Dino wrapper test enforces “fail-closed” loading and requires an ack for nematocyst injection (local artifact). This is a strong pattern: for non-trusted key events, use explicit message protocols with acknowledgments and timeouts.

### Robustness of evaluation harness and CI/CD pipeline

**What you have (from local artifacts).** You already have real regression tests:

- A smoke test asserting expected globals exist (system state, port effect emitters, etc.).
- A monotonicity test proving that increased lookahead window increases injection lead time (and that the zero-window case remains near-zero lead).
- An integration test proving the Dino wrapper loads and that nematocyst injection produces a visible game state change.

**How this maps to SOTA testing discipline.** The web platform’s own SOTA for interoperability is web-platform-tests (WPT); wpt.fyi runs these suites across browsers daily to surface regressions. citeturn8search5turn8search9 Pointer Events Level 3 even links directly to its WPT test suite and implementation report. citeturn5search18

Your direction is aligned with this philosophy, but you’re not yet operating at that “matrix-tested” scale.

## Strengths, weaknesses, and where you surpass SOTA versus fall short

### Where Omega already surpasses SOTA

Your clearest “already surpasses” wins are architectural and evaluative, not raw latency:

**Reproducibility-first input architecture.** A typed fabric + explicit ports + feature-flagged semantics is far more testable than most gesture systems. It resembles how web standards evolve (spec + tests + implementation reports), which is a real advantage if you plan to open-source. citeturn5search18turn8search5

**Explicit intent safety doctrine.** Anti-Midas gating + leaky bucket + hysteresis + fail-closed COAST/deadman creates a principled approach to accidental activation that mirrors the core motivation in Midas Touch mitigation research. citeturn4search1

**Adapterized actuation rather than pretending synthetic input is trusted.** Because synthetic UIEvents aren’t trusted by default and don’t trigger default actions, the adapter/message-based approach (Dino nematocyst with ack) is actually more honest and robust than trying to “fake keys” universally. citeturn1search9

### Where Omega falls short of SOTA

**Web Pointer Events Level 3 fidelity.** Pointer Events Level 3 provides standard access to coalesced and predicted pointer samples and `pointerrawupdate` for high-frequency updates. citeturn0search2turn5search18 Your current injector does not expose these capabilities, which is particularly relevant for drawing (Excalidraw-like) workloads.

**Quantitative prediction accuracy.** SOTA stylus prediction work reports sub-millimeter errors across specific horizons and provides runtime cost. citeturn5search15 Omega currently lacks published accuracy/error metrics for its prediction/lookahead mechanisms, so it cannot claim parity.

**OS-level sampling/latency advantages.** Android touch batching and iOS coalesced/predicted touches are deeply integrated into the OS pipeline. citeturn1search0turn2search2 A camera-based system must work much harder to compete, and it needs rigorous measurement (high-speed camera or equivalent) to be credible. citeturn5search3turn5search2

**Microkernel in the OS sense.** Compared to seL4/QNX/Zircon, Omega does not provide process isolation, verified correctness, or capability-enforced security boundaries. citeturn3search1turn3search3turn3search21 This is not a flaw if you brand it correctly; it becomes a flaw only if you claim OS-microkernel properties.

### Comparison table across key dimensions

| Dimension | Omega GEN7 (current, from local artifacts) | Web SOTA | Mobile OS SOTA | Research SOTA | Verdict |
|---|---|---|---|---|---|
| Pointer model | Synthetic PointerEvents + capture; adapter routing | Pointer Events L3 adds predicted/coalesced lists + `pointerrawupdate` citeturn5search18turn0search2 | N/A | N/A | **Behind web SOTA on fidelity APIs** |
| Sampling fidelity | Fabric snapshots at your loop cadence; CV-dependent | Coalescing APIs allow un-coalescing fast moves citeturn0search2turn0search6 | Android batches motion samples in `MotionEvent` citeturn1search0 | — | **Behind OS SOTA unless you add higher-rate capture or reconstruction** |
| Prediction surface | Tripwire lookahead + physics smoothing | `getPredictedEvents()` surface exists citeturn5search8turn0search2 | iOS predicted touches described as “look into the future” citeturn2search2 | Stylus DL predictors report mm-scale errors citeturn5search15 | **Conceptually aligned; quantitatively unproven** |
| Intent gating | Anti-Midas + leaky bucket + hysteresis + fail-closed | Not standardized | Gesture frameworks are heuristic | Midas Touch + dwell research exists citeturn4search1 | **Strong; likely above typical prototypes** |
| Shared data fabric | Typed SSOT + CloudEvents-inspired envelope | Events, not SSOT | Callbacks/objects, not SSOT | Event meta standards exist (CloudEvents) citeturn10search5turn10search2 | **Architectural advantage** |
| CI/eval | Playwright regression specs + replay fixtures (local artifacts) | WPT + wpt.fyi style dashboards citeturn8search5turn8search9 | OEM internal | Academic benchmarks vary | **Promising; needs scaling + performance budgets** |

## Recommendations for evaluation harness and CI/CD improvements

### Make latency and prediction accuracy testable like a research system

You need two layers of truth:

**Software-internal timing traces** (every port boundary). This validates logical sequencing, scheduling, and regressions.

**External “gesture-to-photon” / “gesture-to-actuation” measurement**. This validates real device behavior, including camera latency, inference, rendering, and OS scheduling. High-speed camera co-registration techniques used in VR research are directly relevant. citeturn5search3turn5search2

A credible minimum benchmark suite should report:

- End-to-end latency distribution (p50/p95) for pointer motion and for keydown events.
- Prediction error vs horizon (e.g., 16ms/33ms/50ms), comparable to the stylus literature. citeturn5search15
- False-activation rate under “non-intent” movements (anti-Midas effectiveness), using dwell/hysteresis parameter sweeps.

![SOTA stylus prediction error reference](sandbox:/mnt/data/sota_stylus_prediction_error_samsung_2020.png)

*This plot reproduces the prediction-error-by-horizon numbers reported by Samsung Research (not Omega results). citeturn5search15*

### Expand CI from “correctness” to “correctness + performance budgets”

You already have Playwright tests; now harden the pipeline:

**Use Playwright CI the recommended way.** Playwright’s own guidance discourages relying on the deprecated GitHub Action and instead recommends using the CLI (`npx playwright install --with-deps`) in CI workflows. citeturn8search2turn8search7 Playwright’s CI docs also discuss headed execution on Linux via Xvfb and caution that caching browsers is generally not recommended. citeturn8search12

**Turn on trace artifacts for flaky failures.** Playwright tracing can capture browser operations and network activity and is designed to be opened in Trace Viewer for debugging. citeturn8search6

**Add performance budgets.** Lighthouse supports `budget.json` performance budgets (timing budgets, resource counts, resource sizes). citeturn8search4 The Lighthouse CI Action makes this straightforward in GitHub Actions and is explicitly designed for CI gating of performance regressions. citeturn8search0turn8search1

### Tooling options table for evaluation and CI/CD

| Category | Tool | Why it fits Omega | Key caveats | Primary refs |
|---|---|---|---|---|
| E2E regression (browser) | Playwright | Cross-browser automation, strong assertions, CI docs, tracing | Browser-dependency install time; mobile Safari requires WebKit strategy | citeturn8search12turn8search3turn8search6 |
| E2E alternative | Cypress | Strong interactive runner workflow; clear E2E docs | Browser coverage differs; architecture differs from Playwright | citeturn9search3turn9search7 |
| Automation alternative | Puppeteer | High-level automation API (Chrome/Firefox via CDP/WebDriver BiDi) | Not a full test-runner stack like Playwright Test | citeturn9search6 |
| Web performance gating | Lighthouse CI + budgets | Budget.json lets you fail builds on regressions | Performance variance; must run multiple times | citeturn8search4turn8search0 |
| Spec conformance mindset | WPT / wpt.fyi | Model for cross-browser regression + spec alignment | Heavyweight; but good inspiration for your port-level tests | citeturn8search9turn8search5 |
| Pointer spec baseline | Pointer Events L3 | Defines predicted/coalesced and `pointerrawupdate` | Doesn’t define algorithms; only API surface | citeturn5search18turn0search2 |

## Prioritized roadmap for open-sourcing Omega GEN7

### Roadmap principle: open-source the “kernel + contracts + harness” before any flashy demos

If Omega is to become a real community project, the differentiator is not “cool demos,” it is: **reproducible input research and adapterized integration**.

**Priority: define the kernel boundary and name it correctly.**  
Be explicit that Omega is a *microkernel-like application architecture*, not an OS microkernel. Otherwise you will invite misplaced criticism about isolation and security that belong to seL4/QNX/Zircon comparisons. citeturn3search1turn3search3turn3search21

**Priority: stabilize contracts and versioning.**  
Publish the Data Fabric schema and envelope contract, and adopt CloudEvents-like discipline: stable required fields and traceability. citeturn10search5turn10search2

**Priority: publish evaluation harness early.**  
Your Playwright-based regression approach is already aligned with modern web CI practice; harden it and ship it as a flagship feature. citeturn8search12turn8search3

**Priority: formalize the adapter API.**  
The adapter approach is the only realistic way to support “single key press/release” across real-world web apps due to untrusted event limitations. citeturn1search9

### A staged open-source plan

| Stage | Deliverable | What “done” looks like | Why this is high leverage |
|---|---|---|---|
| Kernel extraction | Minimal runnable core (fabric + ports + flags) | Runs in replay mode with no camera; deterministic outputs | Lets others contribute without your hardware/setup |
| Contract hardening | Versioned schemas + changelog | Clear backwards-compat rules; tests for schema compatibility | Prevents ecosystem breakage |
| Harness-first release | CI running Playwright + budgets | Tests run via recommended Playwright CLI approach; traces uploaded on failure citeturn8search7turn8search6 | Makes regressions visible and prevents “demo-only” reputation |
| Adapter SDK | Adapter interface + reference adapters | Excalidraw and Dino adapters pinned and CI-tested against known versions | Enables community integrations |
| Performance benchmark suite | Latency + prediction + false-activation metrics | Reports comparable to stylus prediction literature and platform baselines citeturn5search15turn2search2turn1search0 | Enables credible “surpasses SOTA” claims |

### Licensing and dependency hygiene checklist

You integrate major OSS components with differing licenses; before open-sourcing, produce a third-party notices list:

- Excalidraw is MIT licensed. citeturn9search0  
- Babylon.js is Apache-2.0 licensed. citeturn7search1  
- Planck.js is Zlib licensed. citeturn6search3  
- OpenFeature spec/protocol is Apache-2.0 in GitHub org materials (and OFREP is positioned as a vendor-agnostic protocol). citeturn6search0turn6search6

You’ll want automated license scanning (not discussed here), but at minimum: ship NOTICE files and ensure you comply with attribution requirements.

---

### Bottom line assessment

Omega GEN7 is already **architecturally ahead** of most gesture-input systems in one key way: it treats input as a **versioned, replayable, contract-driven pipeline** with explicit safety semantics (anti-Midas + hysteresis) and real regression tests. That is rare, and it is exactly what makes the project open-sourceable.

Where you are **not yet SOTA** is where SOTA is defined by **measured latency and quantified prediction accuracy**. OS-level stacks (Android/iOS) and recent research predictors provide concrete claims and APIs for batching/coalescing/prediction. citeturn1search0turn2search2turn5search15turn5search18 The fastest path to credible “we surpass SOTA” claims is: instrument port-boundary timing, adopt external high-speed measurement, and publish error-by-horizon metrics comparable to the stylus literature. citeturn5search3turn5search15