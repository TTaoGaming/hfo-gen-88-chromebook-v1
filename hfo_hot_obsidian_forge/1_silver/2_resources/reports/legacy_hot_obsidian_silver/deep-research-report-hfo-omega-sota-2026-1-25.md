<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
# Omega Gen7 mobile input microkernel deep research and SOTA gap analysis

## Scope, evidence, and what I can verify

This report is based on two evidence streams:

Your in-repo artifacts (Omega Gen7 v1–v3 HTML + v3 spec YAML + Playwright tests) were inspected directly from the files you uploaded to this chat session (`/mnt/data/*`). Where I describe concrete implementation details (e.g., schema fields, flag names, injector behavior, tripwire scheduling), that is *from your provided artifacts*. These are “verified” only to the extent that the uploaded files reflect your current trunk.

State-of-the-art comparisons are grounded in primary/authoritative sources: W3C specifications (Pointer Events, UI Events, WebXR, WebMIDI, Gamepad), Apple WWDC transcripts and official Apple Developer video pages where accessible, Android Developers API references, Google AI Edge/MediaPipe docs, and canonical microkernel projects (seL4, QNX, Zircon/Fuchsia). These claims are cited.

A hard constraint to be aware of: your current Playwright tests prove *internal monotonicity* and *protocol correctness* (e.g., “lead time increases with lookahead window,” “Dino ack protocol works”), but they do **not** yet prove *device-level end-to-end latency* (gesture-to-photon / gesture-to-actuation) or *prediction error* in physical units. Those are the central bars in true input SOTA, so I treat them as “unknown” until you instrument them.

## Current architecture inventory and “microkernel-like” assessment

Omega Gen7 implements a clear **application-level microkernel pattern**: a small stable core (“kernel”) coordinates ports with strict boundaries, with most semantics expressed as data contracts + feature flags rather than hard-coded app logic. In your terms, P7 is the “Navigator microkernel,” and the rest of the system is structured as domain ports (P1 fuse/fabric, P2 shape/FSM, P3 delivery/injection, P7 navigate). This is not an OS microkernel (no process isolation, no capability enforcement, no kernel/user separation), but it is meaningfully “microkernel-like” as an **architectural style**.

### Port contracts and the shared Data Fabric

Your P1 “gesture port_1_bridge shared data fabric” is a major differentiator: the system maintains a structured world-state snapshot (DataFabric) with `cursors[]`, `systemTime`, and `frameId`, validated via a schema, and optionally wrapped in a CloudEvents-inspired envelope with metadata fields like `specversion`, `id`, `type`, `source`, `time`, and `datacontenttype`. This mirrors the separation CloudEvents promotes: consistent event metadata independent of payload, enabling routing, replay, and interoperability. The CloudEvents spec makes `id`, `source`, and `specversion` required and requires producers to ensure `source + id` uniqueness. citeturn6search4turn6search6

Architecturally, this gives you something most mobile input systems do not: **an explicit, typed, replayable “input fabric”** that can be fed by live sensors or by deterministic fixtures, and then consumed by multiple ports and adapters. That is a foundation for serious evaluation and CI (if you finish the measurement work).

### Anti-Midas + readiness leaky-bucket hysteresis as an intent doctrine

Your FSM is anchored on a four-state model (`IDLE → READY → COMMIT → COAST`) with explicit readiness charge/drain dynamics (leaky bucket) and high/low thresholds for hysteresis. You also have a feature-flagged “anti-Midas” READY gate where READY can be conditioned on palm-cone orientation (facing camera) rather than looser “facing OR charging” semantics.

This aligns with published approaches for the Midas Touch problem: dwell-time–driven activation suffers accidental triggers and requires careful temporal tuning; research in non-conventional interaction repeatedly returns to dwell-time modification and gating mechanisms to reduce involuntary activation. citeturn14search0turn14search5

What’s notable is not that you have hysteresis—many systems do—but that you’ve made it **configurable, testable, and port-governed**. That’s closer to research rigor than most “gesture recognizer” implementations.

![Illustrative readiness leaky-bucket dynamics with hysteresis thresholds](sandbox:/mnt/data/omega_readiness_hysteresis_illustrative.png)

*This figure is model-based using your default constants (charge/release/coast drain + hysteresis thresholds). It illustrates the stability benefit of hysteresis and the latency tradeoffs of fill/drain tuning.*

### Planck.js physics as a first-class input primitive

You use Planck.js (a JavaScript rewrite of Box2D) both as a physics substrate for cursor dynamics and as a contact engine for sensor semantics (tripwire band/contact-only modes). Planck.js explicitly positions itself as a cross-platform HTML5 physics engine optimized for web/mobile and derived from Box2D algorithms. citeturn5search8

This is uncommon in mobile input stacks: OS touch pipelines typically rely on sensor timing + prediction, not rigid-body contact models, for base pointer semantics. Your approach becomes powerful when you treat “tools” as physical entities with constraints (more on that in the future-proofing section).

### W3C PointerEvents implementation and active-app routing

Your P3 injection layer synthesizes `PointerEvent`s (`pointerover/enter/down/move/up/out/leave/cancel`) and uses pointer capture when available (`setPointerCapture`, `releasePointerCapture`). You also attempt deep target resolution across iframes when same-origin, and have an (optional) active-app target routing policy (“ACTIVE_APP_ONLY” vs fallback).

On the standards side, Pointer Events Level 3 (Candidate Recommendation Snapshot, Nov 6, 2025) adds exactly the features drawing and high-fidelity apps care about: `pointerrawupdate` (high-frequency events), access to coalesced events, and access to built-in predicted events to reduce perceived latency. citeturn0search1turn0search4turn1search9 The spec’s editor draft also clarifies that the `PointerEvent` constructor can accept `coalescedEvents` and `predictedEvents` via `PointerEventInit`, cloning them into the event’s associated lists—meaning even “untrusted” synthetic events can carry these data structures if your adapter chooses to. citeturn1search2turn1search9

This is a key gap/opportunity: you currently inject “plain” pointer events (single sample per dispatch). To match web SOTA for drawing apps, you should emit either (a) higher-rate samples and/or (b) structured coalesced/predicted lists.

### Single key press and release via deterministic fingertip tripwires

Your Gen7 v3 spec formalizes a per-hand 4-fingertip tripplane→ASDF mapping (pinky/ring/middle/index → KeyA/KeyS/KeyD/KeyF), where begin edges produce `keydown` and end edges produce `keyup`, with “COMMIT-only” gating and fail-closed defaults. That is a clean “single press/release” contract.

However, browser security semantics matter: W3C UI Events defines “trusted events” vs script-generated “untrusted events,” and notes that most untrusted events should not trigger default actions (except `click`, retained for backward compatibility). citeturn8search1turn8search2 This is why your Dino Runner integration’s “nematocyst” postMessage protocol with explicit `ack` is not a hack—it’s the correct architectural pattern for reliable actuation under modern browser security constraints.

## SOTA baselines for mobile input systems and microkernel architectures

### High-fidelity mobile input pipelines

Modern SOTA input stacks share a common strategy: **sample fast, deliver efficiently, and predict ahead**.

On Android, `MotionEvent` explicitly supports batching multiple movement samples into one object: the newest sample is accessed via `getX/getY`, and historical samples via `getHistoricalX/getHistoricalY`, which preserves fidelity without spamming callbacks. citeturn0search2turn0search8

On iOS, Apple’s “Advanced Touch Input on iOS” (WWDC 2015 Session 233) describes a pipeline where higher touch scan rates (e.g., 120Hz) produce multiple samples per display frame, and “touch coalescing” delivers one main touch per frame plus intermediate coalesced touches to reduce wasted work while preserving detail. The same session introduces “predicted touches” via `predictedTouchesForTouch`, to “look into the future” and reduce perceived latency. It further claims that combining low-latency Core Animation + coalescing + prediction can reduce effective latency from ~4 frames (iOS 8) to ~1.5 frames (iOS 9) in optimized apps. citeturn13search1

On the web, Pointer Events Level 3 standardizes the **API surface** for coalesced and predicted events and provides `pointerrawupdate` for high-frequency updates in secure contexts. It does not standardize the prediction algorithm—only access to the results. citeturn1search9turn1search2turn1search1 MDN summarizes `getPredictedEvents()` as returning estimated future positions based on past points, velocity, and trajectory, enabling apps to “draw ahead” to reduce perceived latency. citeturn1search6

### Prediction accuracy SOTA in academic/commercial stylus work

For quantitative prediction claims, Samsung Research’s 2020 stylus work is a strong baseline: it reports prediction errors of **0.07mm (~16.6ms horizon), 0.24mm (~33.3ms), 0.47mm (50ms)**, and claims ~4ms runtime on a Galaxy Note 9 for the GRU-CNN predictor. citeturn0search0

![SOTA reference: active stylus prediction error vs horizon](sandbox:/mnt/data/sota_stylus_prediction_error_samsung_2020.png) citeturn0search0

This is a very high bar. Even if your “predictive latency” reduces perceived delay, you will not be able to claim “prediction SOTA” without comparable error-by-horizon measurements.

### Computer-vision hand tracking and gesture recognition SOTA (relevant to Omega’s sensing)

If your sensor front-end is MediaPipe Tasks (your v3 config explicitly names `p0_recognizer: MEDIAPIPE_HANDS`), then MediaPipe is part of your system’s effective SOTA baseline.

Google’s Hand Landmarker documentation describes a pipeline that avoids re-running expensive palm detection every frame by using tracking across frames, explicitly to reduce latency, and reports benchmark latencies on Pixel 6: **~17.12ms CPU / ~12.27ms GPU** for the “HandLandmarker (full)” pipeline. citeturn9search1 The older MediaPipe Hands solution docs similarly describe a mode that detects once then tracks landmarks, reducing latency, with a tradeoff between robustness and latency via tracking confidence thresholds. citeturn9search4

For gesture classification, MediaPipe Gesture Recognizer supports a live-stream mode with timestamps and an async callback; it notes that if recognition is called while the recognizer is busy, it can ignore the new frame—i.e., your application needs explicit backpressure awareness if you don’t want to drop time-critical frames. citeturn9search3turn9search9

### OS microkernel SOTA and what Omega is not

OS microkernels earn the name via **minimal trusted computing base, strong isolation, and message-passing IPC**.

seL4 is notable as the first general-purpose OS kernel with a full code-level functional correctness proof (and additional proofs like binary correctness and security properties in some configurations). citeturn4search0turn4search3turn15search4

QNX Neutrino emphasizes modular components around a small microkernel, with message-passing APIs and an explicit architecture meant to scale from small embedded targets to large SMP systems. citeturn15search7turn4search12

Fuchsia’s Zircon is “microkernel-like” but explicitly “does not strive to be minimal”; Fuchsia docs describe reducing trusted code to core functions like memory management, scheduling, and IPC, and describe channels/handles as the basis of IPC and capability transfer. citeturn15search0turn4search1turn4search4

Omega’s microkernel-like quality is real at the *application architecture* level (ports, adapter boundaries, contract discipline), but it should not be marketed as “microkernel” in the OS sense unless you plan to adopt stronger isolation/security properties.

## Comparative analysis across your requested dimensions

### Input latency and prediction accuracy

**Where Omega appears ahead (architecturally):**  
Your system already has explicit **predictive scheduling** concepts (tripwire lookahead, TTC-based lead time, pre-arm injection ticks). That is a larger conceptual toolkit than most gesture applications build. OS stacks predict pointer movement; you predict *semantic crossings* in a physics/contact model (tripwire), which is a different—and sometimes more directly useful—prediction.

Your Playwright regression test demonstrates a key invariant: when lookahead is enabled and the lookahead window is increased (0ms → 200ms), the computed “lead time” between cross and inject increases substantially, with assertions that the 200ms case yields ≥150ms lead while 0ms yields ≤30ms. That’s a genuine, testable predictive behavior—just not yet a measured “real-world latency reduction.”

![Tripwire lookahead regression expectation](sandbox:/mnt/data/omega_tripwire_lookahead_leadtime.png)

**Where Omega falls short of input SOTA today:**  
Mobile input SOTA is dominated by hardware-integrated pipelines (iOS coalesced+predicted touches; Android batched historical samples) that operate at high sampling rates and are tightly scheduled to display refresh. citeturn13search1turn0search2 If Omega’s primary sensing is camera + CV inference, your raw end-to-end latency will almost certainly be worse than direct touch/stylus—unless you invest in (a) high-FPS capture, (b) GPU inference, (c) motion-to-photon measurement, and (d) aggressive prediction/compensation.

Also, web SOTA now includes standardized access to high-fidelity coalesced and predicted pointer events (`getCoalescedEvents`, `getPredictedEvents`) and high-frequency `pointerrawupdate`, which drawing apps can consume for smoother strokes and lower perceived lag. citeturn0search1turn1search0turn1search6turn1search1 Your current injector does not emit these multi-sample structures, meaning Excalidraw-like rendering will be limited compared to what browsers+hardware can provide.

**What you need to claim “surpasses SOTA”:**  
To credibly say “we beat SOTA,” you need a metrics suite that matches the baselines:

- End-to-end latency (gesture onset → visible effect) measured externally, not only by internal timestamps.
- Prediction error vs horizon (e.g., 16/33/50ms), ideally in screen-space mm, comparable to stylus literature. citeturn0search0
- False-activation rate under non-intent motion, comparable to Midas-touch mitigations.

Right now, Omega’s “surpass SOTA” claim is supportable only in the realm of **architecture for experimentation** (contracts, replay, knobs), not physics latency numbers.

### Gesture recognition and hysteresis mechanisms

**Where Omega is strong (and plausibly above most systems):**  
Most production gesture stacks implement hysteresis implicitly (touch slop, velocity thresholds, “debounce” logic). Omega makes hysteresis a first-class, tunable, testable concept: leaky-bucket readiness + explicit high/low thresholds + COAST as a formal ambiguity state + anti-Midas gating. That is more aligned with research-grade interaction systems than typical app-level recognizers.

Your anti-Midas posture also connects to known mitigation strategies: dwell-time tuning is fragile; multimodal gating (e.g., requiring an explicit “activation” action or entering a safe zone) reduces accidental triggers. Research on dwell-time gaze systems reports that smoothing and temporal delays can improve usability, and that dwell times around hundreds of ms affect performance and error rates. citeturn14search5turn14search0 Omega’s readiness meter is a generalized version of dwell-time activation with built-in hysteresis and gating.

**Where Omega likely falls short:**  
Camera-based gesture recognition is exposed to edge-of-frame occlusions and pose ambiguity. Apple’s Vision hand pose talk explicitly warns about accuracy limitations: hands near edges, hands oriented parallel to the camera, gloves, and even “feet detected as hands” can occur. citeturn12search1 MediaPipe similarly exposes quality/latency tradeoffs via tracking confidence. citeturn9search4  
Your system’s hysteresis/COAST helps, but you need explicit evaluation on these known failure regimes.

### Shared data fabric design

**Where Omega is already SOTA-ish:**  
Treating the input world as a **shared data fabric** with strict schema validation and an event envelope is closer to how large event-driven systems are engineered than how gesture systems are typically built. CloudEvents’ core value is interoperability via consistent metadata. citeturn6search6turn6search4

This is a structural advantage in two ways:

- You can build deterministic replays and CI regression tests that don’t depend on live sensors.
- You can make adapters (Excalidraw, Dino, Babylon) depend only on contracts, not on internal state.

**Where it falls short (and what to upgrade):**  
A “fabric” becomes genuinely ecosystem-grade when it has strong **traceability and observability conventions**. The OpenTelemetry spec explicitly includes semantic conventions for CloudEvents instrumentation and distributed tracing integration. citeturn6search0turn6search1  
If you standardize a trace/span model across P1→P2→P3→P7, you will unlock real “input diffs” (“why did this begin edge happen?”) and make performance regressions visible in CI.

### Integration with Excalidraw, Babylon VFX, and Dino Runner

**Excalidraw integration:**  
Excalidraw is a widely embedded MIT-licensed editor, and the modern integration surface is `@excalidraw/excalidraw`. citeturn5search1turn5search3 Your wrapper+adapter approach is practical, but the key risk is that drawing smoothness depends heavily on high-fidelity pointer samples. Web SOTA expects `getCoalescedEvents()` for drawing apps to reconstruct smoother curves from coalesced input points. citeturn1search0turn1search9  
Today, Omega’s pointer injector emits a single `pointermove` per tick; you should treat coalesced events support as a top-tier integration improvement.

**Babylon VFX integration:**  
Babylon.js is Apache-2.0 and actively evolving. citeturn5search7 Babylon.js 8.0 introduces major pipeline control via the “Node Render Graph” (alpha) and other rendering improvements; the key implication for Omega is that VFX can become a significant main-thread and GPU budget consumer. citeturn11search0turn11search7  
If your input pipeline shares the main thread with heavy render graph work, you can easily regress latency and responsiveness. You need explicit performance budgets and “input under load” test scenes.

**Dino Runner integration:**  
Your Dino integration is actually a model of robust actuation: it uses a message protocol (`hfo:nematocyst`) and requires an explicit ack (`hfo:nematocyst:ack`) that your Playwright tests enforce. This is the right approach given UI Events’ “untrusted event” semantics. citeturn8search1turn8search2  
In other words, Dino Runner is a strong “reference adapter” pattern you can replicate.

### Evaluation harness and CI/CD robustness

**Where you are ahead:**  
You already have meaningful, non-trivial invariants under test:

- “System exports required globals / ports.”
- “Tripwire lookahead increases lead time monotically.”
- “Dino wrapper loads; nematocyst injection is fail-closed and acked.”

This is better than most experimental input systems, which often have little or no CI-level regression coverage.

**Where you fall short of SOTA infra:**  
The W3C ecosystem expects a test suite + cross-implementation dashboard (web-platform-tests + wpt.fyi runs results across major browsers daily). citeturn7search5turn0search4 You don’t need to copy that scale immediately, but you should copy the **discipline**: versioned fixtures, clear conformance surfaces, multi-browser matrices, and performance regressions treated as first-class failures.

## Comparison tables and matrices

### Key technical attribute comparison

| Attribute | Omega Gen7 (current) | Web platform SOTA | Mobile OS SOTA | Research SOTA |
|---|---|---|---|---|
| Input event model | Contracted fabric + adapters; synthetic PointerEvents and keyboard protocol | Pointer Events L3 adds `pointerrawupdate`, coalesced & predicted events APIs citeturn0search1turn1search9 | UIKit touch callbacks + coalesced/predicted touches (iOS); MotionEvent batching (Android) citeturn13search1turn0search2 | Stylus DL predictors with quantitative error/horizon metrics citeturn0search0 |
| Sampling fidelity | Your tick cadence + CV frame throughput | `getCoalescedEvents()` returns un-coalesced samples for drawing citeturn1search0 | Android historical samples in batched `MotionEvent` citeturn0search2 | High-rate sensor capture + prediction in stylus pipelines |
| Prediction surface | TTC/TOI lookahead for tripwire; “predictive latency” scheduling | `getPredictedEvents()` standardized; algorithm UA-defined citeturn1search6turn1search9 | iOS predicted touches “look into the future” + coalescing citeturn13search1 | Reported sub-mm errors at common horizons citeturn0search0 |
| Intent gating | Anti-Midas gate + leaky bucket + hysteresis + COAST | Not standardized | Gesture stacks are heuristic; OS-level palm rejection exists but proprietary | Dwell/Midas literature provides mitigation patterns citeturn14search0turn14search5 |
| Shared data fabric | Typed SSOT with envelope metadata | DOM events; no SSOT | OS callback objects; no SSOT | Eventing standards like CloudEvents exist citeturn6search4turn6search6 |
| Adapter robustness | Strong where you control wrappers (Dino); moderate elsewhere | Untrusted events won’t trigger many default actions citeturn8search1 | OS frameworks have privileged input paths | Research prototypes often operate in controlled apps |

### Matrix comparing Omega against leading “input” and “microkernel” systems

This matrix is intentionally split: Omega’s “microkernel-like” axis is architectural; seL4/QNX/Zircon are OS kernels.

| Dimension | Omega Gen7 | W3C Pointer Events L3 | iOS (coalesced/predicted touches) | Android (MotionEvent batching) | MediaPipe Tasks | seL4 | QNX Neutrino | Zircon (Fuchsia) |
|---|---|---|---|---|---|---|---|---|
| Primary domain | App-level input virtualization | Web standard for pointer input citeturn0search4 | OS touch pipeline citeturn13search1 | OS touch pipeline citeturn0search2 | CV hand+gesture inference citeturn9search1 | Verified OS microkernel citeturn15search4 | RTOS microkernel OS citeturn15search7 | “Microkernel-like” OS core citeturn15search0turn15search2 |
| Isolation boundary | Port/adapters in one process | N/A | Kernel/user boundary | Kernel/user boundary | N/A | Strong isolation + formal proofs citeturn4search0turn15search4 | Process separation + message passing citeturn4search12 | Processes isolated; handles + channels IPC citeturn4search1turn4search4 |
| Built-in coalesced samples | Not yet exposed in injected events | `getCoalescedEvents()` API citeturn1search0 | Coalesced touches API described citeturn13search1 | Historical batched samples citeturn0search2 | Tracking reduces re-detection cost citeturn9search1 | N/A | N/A | N/A |
| Built-in prediction API | Tripwire TTC lookahead | `getPredictedEvents()` API citeturn1search6 | Predicted touches API described citeturn13search1 | Varies by OEM; not a standard API | N/A | N/A | N/A | N/A |
| Event envelope discipline | CloudEvents-inspired metadata | DOM event model | UIKit objects/callbacks | Android event objects | N/A | IPC message semantics | IPC message passing | IPC channels and handles |
| Formal assurance level | Test-driven, contract-driven | Spec + WPT model citeturn0search4turn7search5 | Apple internal QA | Android CTS + OEM QA | Benchmarks provided for models citeturn9search1 | Machine-checked proofs citeturn4search3turn15search4 | RTOS architecture docs; commercial QA citeturn4search12 | Production OS docs; security posture focus citeturn15search2 |

### Tooling options for evaluation and CI/CD

| Need | Tool | What it buys you | What to watch | Sources |
|---|---|---|---|---|
| Multi-browser E2E tests | Playwright | Cross-browser automation, strong fixtures, trace capture | Browser installs; device lab integration takes work | citeturn7search7turn7search3 |
| CI best practices | Playwright CLI in CI | Recommended vs deprecated marketplace action; `install --with-deps` | Pin versions; avoid relying on implicit browser downloads | citeturn7search1turn7search14 |
| Debugging flakes | Playwright Trace Viewer | Artifact-based debugging; “on-first-retry” tracing | Trace size overhead if always-on | citeturn7search3 |
| Performance regression gating | Lighthouse budgets (`budget.json`) | CI thresholds for timing + resource budgets | Variance; need multiple runs + stable env | citeturn7search0 |
| Interop mindset model | wpt.fyi approach | Daily cross-browser execution + dashboard | Heavy if copied fully; emulate principles first | citeturn7search5 |

## Strengths, weaknesses, and where you surpass SOTA vs fall short

### Where Omega already surpasses SOTA

Your strongest “already surpasses” claims are about **architecture and evaluability**, not physical latency:

You have a port-and-contract architecture where semantics are expressed in data structures, feature flags, and adapters. Most gesture systems are still callback spaghetti. That makes Omega unusually extensible and testable.

You have an explicit intent doctrine (anti-Midas + readiness hysteresis + COAST + deadman fail-closed) that aligns with known non-conventional interaction pitfalls, rather than ignoring them. citeturn14search0turn14search5

You have deterministic, CI-friendly regression tests for predictive behaviors and integration protocols, which is rare in experimental input systems. Your trajectory resembles the W3C approach of “spec + tests + implementation experience,” even if you’re operating at app scope. citeturn0search4turn7search5

Your Dino integration embodies a key web truth: untrusted synthetic events do not behave like real hardware input, so adapters must implement explicit actuation protocols. citeturn8search1turn8search2

### Where Omega falls short of SOTA

You do not yet expose modern pointer-fidelity surfaces (Pointer Events L3 coalesced/predicted lists, `pointerrawupdate`). This is directly relevant to Excalidraw and any drawing/ink workloads. citeturn0search1turn1search0turn1search6turn1search1

You do not yet have quantitative prediction accuracy and end-to-end latency measurements comparable to (a) iOS frame-based targets, (b) Android batched sample handling, or (c) stylus predictor error-by-horizon data. citeturn13search1turn0search2turn0search0

Because your sensing appears CV-based, you inherit known failure modes: occlusion, edge-of-frame, pose ambiguity, and multi-hand identity issues. Apple explicitly recommends tracking requests to maintain object identifiers during occlusion and warns about latency impacts when detecting many hands. citeturn12search1 Your v3 spec’s “coast + snaplock” identity stabilization is the right direction, but it needs quantitative verification under these scenarios.

Compared to OS microkernel SOTA, your “microkernel” is architectural only; you do not provide process isolation, message-passing IPC between protection domains, or formal proofs. That’s fine—just label it correctly. citeturn4search0turn15search7turn15search0

## Recommendations to improve the evaluation harness and CI/CD

### Turn your current harness into an “SOTA-grade” measurement system

Right now, Omega’s harness validates **logical properties**. To reach SOTA, add **physical and statistical properties**.

Add an “input performance contract” per adapter:

- **Latency budget:** p50/p95 end-to-end time from (a) detected gesture event timestamp or frame timestamp to (b) pointer/actuation visible in target app.
- **Prediction contract:** error vs horizon (e.g., 16/33/50ms), reported in pixels and converted to mm when DPI is known.
- **False activation contract:** rate of unintended begin edges under “non-intent” movements.

For comparison, you can anchor prediction metrics to the stylus literature. citeturn0search0

Add a “sensor throughput contract” for the recognizer:

- Frame acceptance rate under load (how many frames dropped because recognizer was busy), because MediaPipe notes that in live stream mode, frames can be ignored when the task is busy. citeturn9search3
- Benchmark mode (CPU vs GPU) comparable to MediaPipe’s Pixel 6 benchmarks. citeturn9search1

### CI/CD hardening moves you should implement immediately

Run Playwright the recommended way:

- Use Playwright CLI (`npx playwright install --with-deps`) rather than the deprecated marketplace action. citeturn7search1turn7search7
- Ensure your workflow explicitly installs browsers after `npm ci`, because newer Playwright package behavior no longer auto-downloads browsers. citeturn7search14

Make failures debuggable by default:

- Enable traces on first retry (`trace: 'on-first-retry'`), and upload `trace.zip` artifacts. citeturn7search3

Add performance budgets:

- Adopt Lighthouse budgets (`budget.json`) for key pages: Omega shell, Excalidraw wrapper, Babylon VFX page, Dino wrapper. Lighthouse budgets can gate timing metrics and resource sizes in CI. citeturn7search0

Adopt the “wpt.fyi posture,” even if you don’t adopt the full WPT ecosystem:

- Your core adapters should be tested across at least Chromium + WebKit + Firefox on every PR, and daily scheduled runs should record trends (latency, dropped frames, regression counts). wpt.fyi exists specifically because daily cross-browser runs make interop issues easier to find. citeturn7search5turn7search13

## Prioritized roadmap for open sourcing and ecosystem building

### Open-source roadmap that minimizes risk and maximizes adoption

Publish the kernel and contracts first, not the demos:

- Release your DataFabric schema + envelope + port contracts as the stable “core SDK.”
- Release a reference replay harness and fixtures, because that’s how contributors can work without your exact camera setup.

Stabilize plugin/adapters as a public API:

- Make “adapter” a first-class external interface: inputs (fabric snapshots, port events), outputs (pointer/keyboard/tool actuation), and required acknowledgments.

Codify feature flags as part of public ergonomics:

- If you keep OpenFeature, consider documenting OFREP compatibility for remote evaluation and vendor-agnostic flags (this is aligned with your “microkernel knobs” vision). citeturn5search0turn5search4turn5search6

### Building a sustainable ecosystem with open source

A credible pattern here is “open editor + paid extras,” which Excalidraw itself uses: the repository is MIT and promotes sponsorship and a paid offering (“Excalidraw+”). citeturn5search1

For Omega, the ecosystem-friendly monetization options that fit your “tool virtualization” vision:

Skins and add-ons as pure content packs: visual engines (Babylon scenes, particle presets), cursor “weapons,” UI themes, sound packs. This mirrors how game engines monetize without locking core input abstractions.

Paid “tool packs” as certified adapters: “Excalidraw Pro Adapter,” “Babylon VFX Toolkit Adapter,” “Education Mode: guided curricula + evaluation rubrics.” The key is that tools remain decoupled and optional—like QNX modular components (architect selects modules) but at app level. citeturn15search7

Hosted services for teams: cloud fixture storage, replay dashboards, CI telemetry aggregation, performance regression alerts. Observability can leverage OpenTelemetry conventions (including CloudEvents span modelling). citeturn6search0turn6search1

## Checklist to elevate Omega to true SOTA status

This checklist focuses on “admission fit” (how easily new apps/tools can onboard), scalability, extensibility, and robustness, with concrete success criteria.

| Category | Best-practice step | Why it matters (SOTA framing) | Concrete “done” signal |
|---|---|---|---|
| Admission fit | Define a public Adapter Manifest (capabilities, expected inputs, ack protocol, permission needs) | Makes new tools onboardable without core changes | A new adapter can be added by adding a manifest + implementing a small interface |
| Admission fit | Standardize a “Tool State” contract (pose, contact, intent, confidence, timestamps) separate from “Pointer State” | Prevents pointer/keyboard from being the ceiling of the system | You can drive one tool by pointer, another by XR rays, another by MIDI controls |
| Latency | Implement end-to-end latency measurement suite (gesture-to-photon + gesture-to-actuation) | SOTA is measured, not asserted | CI produces p50/p95 for each adapter; regressions fail builds |
| Prediction | Add prediction error-by-horizon benchmarks | Enables comparison to stylus prediction literature | You can plot error vs horizon comparable to Samsung numbers citeturn0search0 |
| Pointer fidelity | Add coalesced/predicted sample emission for drawing adapters | Matches Pointer Events L3 drawing expectations citeturn1search0turn1search6 | Excalidraw strokes show measurable smoothness gains |
| Robustness | Build “known-bad” scenario fixtures: occlusion, edge-of-frame, parallel-to-camera hands | Mirrors Apple/Vision caveats citeturn12search1 | CI confirms no key spam; COAST/IDLE behavior stable |
| Shared fabric | Add trace propagation (traceId across P1→P7) + span semantics | Enables postmortems and perf analysis citeturn6search0turn6search1 | A single action can be traced end-to-end in telemetry |
| Scalability | Move heavy rendering (Babylon) and inference scheduling into explicit budgets | Prevent VFX from causing input jank | “Input under load” test scene stays within latency budget |
| CI/CD | Adopt Playwright CLI install + trace-on-first-retry + artifact upload | Makes CI dependable and diagnosable citeturn7search1turn7search3 | Flakes provide traces; failures are reproducible |
| CI/CD | Add Lighthouse performance budgets | Prevents regressions in responsiveness citeturn7search0 | Budget regressions fail PRs |
| Extensibility | Version contracts like a spec: semver, change logs, deprecation policy | Prevent ecosystem breakage | Adapters declare compatible contract versions |
| Governance | Establish a contribution and compatibility policy (like “WPT posture”) | Enables community trust | You publish a compatibility matrix and run scheduled cross-browser tests citeturn7search5 |

## Evolving beyond pointer and keyboard into future-proof “tool virtualization”

Your app already contains the right “north star” language (“Total Tool Virtualization”), and the architecture supports it. The missing step is formalizing “tool” as the primary abstraction.

### The architecture you want: tool state → drivers → target protocols

Conceptually, evolve from:

**CV gesture → pointer/keyboard events**

to:

**Multimodal sensors → fused tool state (3D pose + constraints + intent) → physics simulation → protocol drivers (Pointer, XR, Gamepad, HID, MIDI, app-specific adapters)**

The web platform already contains several protocol surfaces that map naturally onto “virtual tools”:

WebXR defines `XRInputSource` for input mechanisms like tracked hands, controllers, and gaze, and explicitly describes target rays and grip poses (including guidance like “target ray should point in the same direction as the user’s index finger if outstretched”). citeturn10search5  
This is an excellent future-proof target for your 3D hand+tool model.

Gamepad API defines normalized axes and button arrays and is a stable abstraction for “control surfaces” (joysticks, triggers). citeturn10search11turn10search2

WebHID explicitly exists because many input devices are HID, but the OS drivers typically translate them into high-level APIs; WebHID provides raw access (permissioned). citeturn10search10

Web MIDI API provides a standardized event interface for musical and non-musical controllers (buttons, knobs, sliders), often used in creative tooling. citeturn10search0

Your strategic move is to treat pointer+keyboard as **legacy drivers**, not as the kernel’s native tool language.

### Technical requirements for multimodal sensor fusion and physics-based tool emulation

Sensor fusion:

- Use timestamps aggressively. MediaPipe live-stream APIs require frame timestamps; and the docs warn frames can be dropped when busy. citeturn9search3 Your fabric already carries `systemTime` and per-frame IDs; extend it to preserve sensor timestamps and latency metadata per stage.

- Build an explicit backpressure model: if inference drops frames, the tool state estimator must respond (e.g., predictive coasting with uncertainty growth).

- Incorporate tracking to stabilize identity. Apple’s Vision talk suggests using tracking requests to maintain object identifiers through occlusion and off-screen movement. citeturn12search1 Your “coast + snaplock” identity stabilization is aligned; the next step is to quantify its failure rate and tune it per device / camera FOV.

Physics modeling:

- Your current Planck.js approach is 2D rigid-body physics. That’s excellent for “contact on a plane” metaphors (tripwires, buttons, zones). citeturn5search8  
For 3D tool virtualization, you will likely need a 3D physics engine (or at least 3D kinematics + constraint solvers). Keep Planck for 2D overlays and UI layers; add a 3D “tool world” for XR- and Babylon-class interactions.

Latency management:

- Adopt the OS/web strategy: sample fast, coalesce for efficiency, and predict ahead. iOS coalesces and predicts touches; Pointer Events L3 exposes coalesced/predicted data; Android batches historical samples. citeturn13search1turn1search9turn0search2  
Your fabric should represent both “raw samples” and “presented samples” so adapters can choose fidelity levels.

Extensibility:

- Formalize a “Driver API” layer: ToolState → PointerDriver, XRDriver, GamepadDriver, MIDI Driver, etc. The driver should be swappable behind a port boundary like your current P3.

- Make security/permissions explicit: Pointer events are script-level; WebXR, WebHID, WebMIDI are permissioned and often require secure contexts. citeturn1search1turn10search10turn10search0  
Your Navigator microkernel can treat “permission readiness” as part of state (not just a UI detail).

### Near-term evolution path that leverages what you already built

Implement Pointer Events Level 3 data fidelity for drawing apps:

- Add “multi-sample” emission semantics for `pointermove` using `getCoalescedEvents()`-compatible data (via `PointerEventInit.coalescedEvents`) and optionally predicted samples. citeturn1search2turn1search9  
This is the most direct upgrade for Excalidraw integration quality.

Add an XRInputSource adapter:

- Map your hand model to WebXR’s “tracked-pointer” semantics with `targetRaySpace` pointing along the index direction. citeturn10search5  
This is the cleanest way to evolve beyond 2D pointer metaphors while remaining standards-aligned.

Expand tool actuation surfaces beyond keyboard:

- For creative tools, MIDI controllers are a natural “virtual tool” space (sliders/knobs mapped to parameters). citeturn10search0
- For physical control panels, Gamepad API is a stable abstraction. citeturn10search11turn10search2

---

### Final “tell it like it is” assessment

Omega Gen7 is already unusually strong in **architectural prerequisites for SOTA**: contract-driven ports, a shared fabric, explicit intent gating (anti-Midas + hysteresis + fail-closed COAST), and meaningful CI regression tests. That’s a bigger advantage than it sounds, because it determines whether you can iterate scientifically and build an ecosystem.

But Omega is not yet SOTA on the axes that define SOTA in mobile input: **measured end-to-end latency, prediction accuracy, and high-fidelity sample handling**. The web and mobile OS stacks already expose coalesced/predicted sampling and high-frequency update paths. citeturn13search1turn0search2turn1search9turn1search1 The stylus research world has published mm-scale error curves at standard horizons. citeturn0search0

Your fastest route to “surpass SOTA” is not to chase features; it’s to (a) measure what matters, (b) expose fidelity surfaces (coalesced/predicted lists) for real apps like Excalidraw, and (c) treat tool virtualization as a standards-aligned “ToolState → drivers” platform, with WebXR as the natural future-proof target. citeturn10search5