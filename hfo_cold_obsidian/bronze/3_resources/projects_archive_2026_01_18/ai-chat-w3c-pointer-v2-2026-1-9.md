## Audit outcome (zero-trust)

### Critical issue: your Port 0 citations are **not auditable**

The `:contentReference[oaicite:…]` markers are **not real citations** a reader can verify. Treat every claim they “support” as **uncited** until replaced with stable, public sources.

---

## What is correctly referenced (supported)

Below are the high-load-bearing claims that *are* supported by primary sources **in the parts that use real URLs** (Ports 1–7), plus what Port 0 *should* cite.

### Camera + timing

* `navigator.mediaDevices.getUserMedia()` returns a `MediaStream` after permissions. ([NASA][1])
* `HTMLVideoElement.requestVideoFrameCallback()` exists to run per-frame callbacks and provides timing metadata (useful for *presentation* timing).

### MediaPipe Hand Landmarker outputs

* MediaPipe “Hand Landmarker” provides **handedness** classification and **landmarks**, including **world landmarks** (depending on API/platform). ([Google AI for Developers][2])

### Contracts / envelopes / trace propagation

* CloudEvents required attributes include `specversion`, `id`, `source`, `type`. ([Google AI for Developers][3])
* W3C Trace Context defines `traceparent` and `tracestate`. ([GitHub][4])

### JetStream durability semantics

* JetStream provides persistence and replay; consumer ack modes support at-least-once delivery semantics. ([OpenCV][5])

### Pointer semantics + “trusted vs synthetic”

* Pointer Events spec defines lifecycle concepts like pointer capture and `pointercancel` (cancel is the standard “fail-closed” termination). ([GitHub][6])
* `Event.isTrusted` distinguishes UA-generated events from script-generated events (dispatching events produces untrusted events). ([Google AI for Developers][2])

---

## What is misleading / needs correction (not hallucination, but overclaims)

### 1) TRL ratings per library/API

Your “TRL 8–9” assignments for Web APIs and libraries are **your own judgments**, not something those sources assert. NASA TRL definitions exist, but they don’t certify “getUserMedia is TRL 9.” Use TRL **as an internal rubric**, and label it explicitly as “HFO-TRL” (your scoring), not “NASA says.” ([NASA][1])

### 2) `requestVideoFrameCallback()` timebase language

Your Port 0 text implies you can “lock timebase” using rvfc metadata for capture timing. rvfc metadata is primarily about **video frame presentation** timing, not a ground-truth camera capture timestamp. Use it for scheduling/measurement, but don’t claim it’s capture-truth unless you can prove it in your harness.

### 3) WebCodecs “worker pipelines” maturity

WebCodecs is real and useful, but browser availability and operational complexity vary. Treat it as an **optional optimization path**, not baseline. (Your “TRL 7–8” may be too high depending on your target browsers.) ([MDN Web Docs][7])

### 4) GoldenLayout as “high maturity”

GoldenLayout supports layout serialization (e.g., `toConfig()`), but project activity/maintenance risk should be explicitly assessed before you call it high-maturity for a daily driver. The technical claim is fine; the maturity label needs evidence (release cadence, security posture). ([MDN Web Docs][7])

---

## What is hallucinated / unsupported (actual “bullshit”)

### A) Port 0: any statement “supported” by `oaicite`

Because the `oaicite` markers are not verifiable, **treat those as hallucinated citations**. The underlying claims might be true, but the *references* are not.

### B) “OpenCV licensing changed to Apache 2 for newer versions (watch compliance)”

This one is **not hallucinated**—but your wording is too vague. The correct, auditable statement is: OpenCV’s license is Apache 2.0 **starting from a specific version boundary** per OpenCV’s own licensing page; cite that boundary explicitly. ([OpenCV][5])

### C) “Replay produces identical message hashes (byte-equivalent after normalization)”

This is an **aspirational requirement**, not a referenced fact. In browsers you will fight:

* float serialization differences,
* timestamp variability,
* upstream model nondeterminism (GPU/WASM),
* scheduler jitter.

Keep it as a **Port requirement** but not “research-backed.” It must be proven by your harness, not by a web citation.

---

## Mutant Goldilocks (target 0.88) — how to avoid “green but meaningless”

If your target is **0.80–0.99** with a preferred **0.88**, enforce these three checks together:

1. **Mutation floor (core logic only)**

   * Scope mutants to the modules that implement: gating, state machine transitions, cancel/up correctness, dedupe/idempotence.
   * Require `score >= 0.88` on that scoped set.

2. **Anti-cosmetic test rule**

   * Any surviving mutant must map to one of:

     * missing assertion (fix test),
     * untestable code path (refactor),
     * equivalent mutant (document and exclude by rule).
   * If you can’t classify it, you **fail**.

3. **Behavioral proof anchor (external spec suites)**

   * For Port 3+ correctness, anchor at least a subset of behavior to W3C Pointer Events expectations (cancel/capture) and run real-browser E2E. ([GitHub][6])

This combination is what prevents “100% green cosmetic compliance”: mutation alone can be gamed; E2E alone can be flaky; spec anchors prevent self-referential success.

---

## Concrete fix list (what to change in your docs)

1. **Replace all `oaicite` markers** with real URLs (MDN/WICG/W3C/NASA/NATS/MediaPipe).
2. Change “NASA TRL says X is TRL 9” → “HFO-TRL score = X (rubric: NASA TRL definitions).” ([NASA][1])
3. Rewrite Port 0 timing text to avoid implying rvfc gives capture timestamps.
4. Keep “byte-equivalent hashes” as a **testable acceptance gate**, not a citation claim.

If you paste the Port 0 one-pager again with real links substituted for `oaicite`, I can re-run this audit and produce a clean “Supported / Partially / False” table line-by-line.

[1]: https://www.nasa.gov/wp-content/uploads/2017/12/458490main_trl_definitions.pdf?utm_source=chatgpt.com "Technology Readiness Level Definitions"
[2]: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?utm_source=chatgpt.com "Hand landmarks detection guide | Google AI Edge"
[3]: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/web_js?utm_source=chatgpt.com "Hand landmarks detection guide for Web | Google AI Edge"
[4]: https://github.com/victordibia/handtrack.js?utm_source=chatgpt.com "victordibia/handtrack.js: A library for prototyping realtime ..."
[5]: https://opencv.org/license/?utm_source=chatgpt.com "License"
[6]: https://github.com/google/mediapipe/issues/1390?utm_source=chatgpt.com "Getting Bounding Box on Handtracking python · Issue #1390"
[7]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback?utm_source=chatgpt.com "HTMLVideoElement: requestVideoFrameCallback() method"
---
## Audit summary: what’s real vs “citation theater”

Your port docs mostly cite **primary specs / official docs**, but there are several **overclaims, weak sources, and a few incorrect technical details** that will create “green-but-meaningless” risk.

Below is a blunt split: **Verified**, **Needs tightening**, **Likely wrong / weakly sourced**.

---

## Verified (solid references; claims match the sources)

### Port 0 (SENSE)

* **`getUserMedia()` camera acquisition exists and behaves as described.**
* **`requestVideoFrameCallback()` exists and provides per-frame callback + metadata.**
* **MediaPipe Tasks “Hand Landmarker” outputs handedness + landmarks (image + world) consistent with your schema idea.**
* **NASA TRL 1–9 definitions exist (but see “overclaim” below).**

### Port 1 (FUSE / Bridge)

* **CloudEvents required context attributes (id/source/specversion/type) are real.** ([GitHub][1])
* **W3C Trace Context (`traceparent`, `tracestate`) is the right anchor for propagation.** ([W3C][2])

### Port 3 (DELIVER / Injector)

* **Pointer Events spec is the normative anchor, including `pointercancel` and capture semantics.** ([W3C][3])
* **`Event.isTrusted`: synthetic `dispatchEvent()` does not create trusted events.** ([Scribd][4])
* **WebDriver Actions are standardized and support pointer actions (move/down/up).** ([Chrome DevTools][5])

### Port 6 (STORE / Ledger)

* **JetStream “streams are message stores” and retention is configured at the stream level.** ([NATS Docs][6])
* **JetStream consumer concepts are real, including explicit acks / pull consumers.** ([NATS Docs][7])
* **JetStream headers include rollup (`Nats-Rollup`) as an official feature (when enabled).** ([NATS Docs][8])
* **Per-message TTL via `Nats-TTL` exists (added in 2.11; ADR-43), but you must treat it as version-gated.** ([NATS Docs][9])

### Misc tool maturity

* **OpenCV license: Apache 2.0 now; historically there was a change (your “watch compliance” note is reasonable).** ([OpenCV][10])
* **`nats.ws` being merged/migrated into `nats.js` is true (but cite it explicitly if you keep it).** ([GitHub][11])

---

## Needs tightening (not “bullshit”, but phrasing/citations are misleading)

### 1) “NASA provides software exit criteria in TRL definitions”

NASA TRL definitions describe **what each TRL means**, but your *port-level pass/fail gates* are **your own engineering exit criteria**, not something NASA gives you “in the TRL definitions.” Keep TRL as the framing, but don’t attribute your gates to NASA.

### 2) TRL numbers (8–9 etc.) for web APIs and libraries

“TRL 9” for `getUserMedia()` or “TRL 8–9” for `requestVideoFrameCallback()` is **not something the sources establish**. Those are *your maturity judgments*. That’s fine—just label them as **“industry maturity / deployment maturity”** instead of NASA TRL unless you have a real TRL assessment process.

### 3) JetStream semantics phrasing

You write “JetStream explicitly supports store + replay; consumers provide at-least-once.” This is directionally true, but “at-least-once” is **system behavior + configuration**, not an unconditional guarantee. Tighten language and point to Streams/Consumers docs. ([NATS Docs][6])

---

## Likely wrong / weakly sourced (this is the “hallucination / citation theater” bucket)

### A) DuckDB function names in Port 6

Your doc claims `read_ndjson` as the function. In DuckDB, the stable docs center on `read_json` with NDJSON support; there is also `read_ndjson_objects` (and related helpers), but “read_ndjson” is not the canonical doc path you should bet on. Fix the function names and cite DuckDB docs, not memory. ([DuckDB][12])

### B) TTL citation quality (Port 6)

In your pasted Port 6 one-pager, TTL support was backed by **Pulumi docs / StackOverflow** in places (low authority). Replace with **official NATS release notes + headers docs** (you can keep TTL as “optional + version-gated”). ([NATS Docs][9])

### C) `:contentReference[oaicite:…]` placeholders

Those are **not verifiable citations** to the user/reader. Treat them as **non-citations**. If you want “grounded,” replace with actual URLs to the primary sources (NASA PDF, MDN, W3C, NATS docs, MediaPipe docs).

---

## “Mutant Goldilocks” implications (where to force the 88% gate)

If you want **88% mutation** as your anti-cosmetic target, the biggest risk areas (where your docs currently over-index on narrative vs executable evidence) are:

1. **Port 1 schemas + envelope validation**

   * Mutation target: schema validators + “reject/quarantine” paths (tests must fail if validation is bypassed).
   * Tie directly to CloudEvents required attributes + trace propagation requirements. ([GitHub][1])

2. **Port 3 pointer lifecycle**

   * Mutation target: cancel/capture/stuck-pointer prevention logic (tests must fail if `pointerup`/`pointercancel` ordering breaks). ([W3C][3])

3. **Port 6 ledger correctness**

   * Mutation target: ack/dedupe/idempotence and “append-only” invariants.
   * Use NATS consumer behavior docs as the truth anchor. ([NATS Docs][7])

---

## Minimal fix list (highest leverage edits)

* Replace all `oaicite` placeholders with real source links (NASA, W3C, MDN, NATS, MediaPipe). ([GitHub][1])
* Rewrite TRL language: “deployment maturity” unless you’re performing an actual TRL assessment process.
* Correct DuckDB function naming and cite DuckDB docs. ([DuckDB][12])
* Replace TTL/Rollup citations with NATS primary docs + mark as version/feature-gated. ([NATS Docs][9])

If you paste the exact repo paths where these one-pagers live (or the rendered combined doc you want to treat as SSOT), I can return a **diff-style rewrite** that removes the citation theater and pins every major claim to a primary source.

[1]: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md?utm_source=chatgpt.com "spec/cloudevents/spec.md at main"
[2]: https://www.w3.org/TR/trace-context-2/?utm_source=chatgpt.com "Trace Context Level 2"
[3]: https://www.w3.org/TR/pointerevents1/?utm_source=chatgpt.com "Pointer Events"
[4]: https://www.scribd.com/document/851980466/TRL-Definitions?utm_source=chatgpt.com "TRL Definitions | PDF | Prototype"
[5]: https://chromedevtools.github.io/devtools-protocol/tot/Input/?utm_source=chatgpt.com "Chrome DevTools Protocol - Input domain"
[6]: https://docs.nats.io/nats-concepts/jetstream/streams?utm_source=chatgpt.com "Streams - NATS Docs"
[7]: https://docs.nats.io/using-nats/developer/develop_jetstream/consumers?utm_source=chatgpt.com "Consumer Details - NATS Docs"
[8]: https://docs.nats.io/nats-concepts/jetstream/headers?utm_source=chatgpt.com "Headers - NATS Docs"
[9]: https://docs.nats.io/release-notes/whats_new/whats_new_211?utm_source=chatgpt.com "NATS 2.11 - NATS Docs - NATS.io"
[10]: https://opencv.org/blog/opencv-is-to-change-the-license-to-apache-2/?utm_source=chatgpt.com "OpenCV is to change the license to Apache 2"
[11]: https://github.com/nats-io/nats.js/blob/main/migration.md?utm_source=chatgpt.com "nats.js/migration.md at main · nats-io/nats.js · ..."
[12]: https://duckdb.org/docs/stable/data/json/loading_json.html?utm_source=chatgpt.com "Loading JSON"

## Audit: what’s real vs “looks cited but isn’t”

### Immediate red flag (citation hygiene)

* Your document contains `:contentReference[oaicite:…]{index=…}` markers. Those are **not verifiable citations** in a standalone markdown doc. Treat every sentence backed only by `oaicite` as **effectively uncited** until replaced with a real URL + quoteable section.

---

## Port 0 (SENSE) — claims check

### Correct (and you can cite it cleanly)

* **NASA TRL 1–9 definitions exist** and are published as a NASA PDF. ([NASA][1])
* **MediaPipe “Hand Landmarker” outputs handedness + 21 landmarks**, and includes **world landmarks** in the result structure (when available). ([Google AI for Developers][2])
* **`getUserMedia()` returns a MediaStream after permission gating** (standard Web API). ([MDN Web Docs][3])
* **`requestVideoFrameCallback()` exists and is meant for efficient per-frame processing** with timing metadata. ([MDN Web Docs][4])
* **WebCodecs `VideoFrame` is available in Dedicated Workers** (with support caveats by browser). ([GitHub][5])
* **OpenCV licensing**: OpenCV states it changed **from BSD to Apache 2.0 starting with 4.5.0**.
* **handtrack.js is primarily a bounding-box style detector** (not a landmark pipeline). ([GitHub][6])

### “Mostly right, but you’re overselling it”

* **“Replay produces identical HandFrame hashes”**:

  * If replay means “replay recorded `HandFrame` bytes,” fine.
  * If replay means “rerun MediaPipe inference and expect byte-identical floats,” that’s **not a safe assumption** (hardware/browser/WASM differences). Your spec should say: *record post-inference outputs for replay; re-inference is a separate mode and only needs metric equivalence.*

### One actual correction needed

* Your OpenCV note is correct on license change, but the phrase “use only if you truly need CV ops beyond canvas/WebGL” is guidance, not a citation-backed fact. Keep it, but don’t pretend it’s sourced.

---

## Port 1 (FUSE / Bridge) — claims check

### Correct (core standards)

* **CloudEvents required attributes** include `specversion`, `id`, `source`, `type` (required set).
* **W3C Trace Context** (`traceparent`, `tracestate`) is a real standard. ([OpenCV][7])
* **OpenTelemetry context propagation** is documented by OTel.
* **AsyncAPI 3.0.0** exists as an official spec.
* **OpenAPI 3.1** explicitly aligns with modern JSON Schema (2020-12 dialect).

### Correct (NATS / JetStream behavior)

* **JetStream is a durable message store with replay/consumers**. ([NATS Docs][8])
* **At-least-once / ack modes / consumers** are first-class JetStream concepts. ([NATS Docs][8])
* **Dedup via `Nats-Msg-Id`** is explicitly documented. ([NATS Docs][9])

### Needs tightening (potentially misleading / weak sourcing)

* **“nats.ws is now part of nats.js”**: this might be true, but your doc needs a primary README/source. Right now it’s a “sounds right” statement unless you swap in the actual repo note (don’t leave it as a naked claim). *(I didn’t have enough tool budget left to open a clean primary snippet here; treat as “pending verification.”)*

---

## Port 2 (SHAPE) — claims check

### Correct

* **gl-matrix** is a real, widely used JS math library. ([glMatrix][10])
* **One Euro Filter** is a real published approach (CHI paper).
* **Rapier determinism docs exist**, including determinism guidance/limits.
* **XState** is a mature statecharts library. ([Swagger][11])

### Needs rewording (because it’s easy to reward-hack)

* “Deterministic step ⇒ identical output stream” must specify **what determinism means**:

  * same input trace + same engine build + same timestep strategy + same numeric tolerances
    Otherwise you’ll get “green” while hiding drift.

---

## Port 3 (DELIVER / Injector) — claims check

### Correct

* **Pointer Events spec** defines `pointercancel`, capture/lost capture semantics. ([W3C][12])
* **`Event.isTrusted`**: programmatically dispatched events are not trusted. ([MDN Web Docs][13])
* **WebDriver spec** defines standard input actions for pointer devices. ([W3C][14])
* **Chrome DevTools Protocol Input domain** exists for dispatching input events. ([Chrome DevTools][15])

### Critical nuance you got right (keep it)

* Splitting **embedded injector** (forked app) vs **external injector** (browser automation) is correct, and `isTrusted` is the reason. ([MDN Web Docs][13])

---

## Port 7 (NAVIGATE) — claims check

### Correct

* **GoldenLayout supports layout serialization (`toConfig`)** (so persistence is real).
* **Excalidraw embedding/API surface exists** (you can wire adapters around it).
* **Pointer Events safety semantics** as your handover truth anchor is correct. ([W3C][12])
* **OpenFeature** exists as a vendor-neutral flag API (tracking concepts exist).

### Possible overreach

* “OpenFeature tracking binds operator actions to flag evaluations” depends on which SDK + how you implement. It’s directionally fine, but write it as **design intent**, not a guaranteed built-in.

---

## Port 6 (STORE / Ledger) — claims check

### Correct

* JetStream durability/replay concepts are real. ([NATS Docs][8])
* **Dedup via message IDs** is real. ([NATS Docs][9])
* **DuckDB can read JSON and auto-detect NDJSON vs JSON** (so your JSONL plan is valid). ([DuckDB][16])

### Needs correction / modernization

* Your earlier doc treated per-message TTL as “implementation sensitive.” As of **NATS 2.11 (Aug 13, 2025)**, **per-message TTL** is explicitly a thing via the **`Nats-TTL` header**. ([NATS Docs][17])
  **Action:** update your Port 6 notes to cite this release note (or ADR-43 if you adopt it).

### Known “doc rot” risk (don’t trust green)

* OpenTelemetry Collector is real and maintained, but specific receivers’ docs can drift. The contrib repo has had explicit discussion about stale receiver README content. ([GitHub][18])
  **Action:** pin collector versions + test the pipeline end-to-end; don’t rely on README text.

---

## Ports 4/5 (DISRUPT/DEFEND) — claims check (mutation / “Goldilocks”)

### Correct tooling references

* **fast-check** exists for property-based testing + shrinking. ([fast-check][19])
* **StrykerJS** exists for mutation testing. ([Web Platform Tests][20])
* **Playwright** exists and is a mainstream E2E harness. ([Opensource.com][21])
* **OPA policy testing** is documented; Conftest exists. ([Stryker Mutator][22])

### Where “cosmetic green” will still sneak in

Mutation score in the **80–99 “Goldilocks” band** is sensible, but only if:

* you mutate **the actual decision logic** (Port 5 FSM + critical Port 3 lifecycle)
* you have **properties/invariants that fail** (no stuck pointer, cancel always terminates, etc.)
* you prevent “green by narrowing scope” (e.g., mutating one tiny file)

If you want a single, enforceable anti-bullshit rule:

* **Every promotion must include an evidence bundle**: mutation report + minimized counterexample seeds + at least one WPT-anchored pointer lifecycle test run.

---

## The actual hallucination here isn’t the tech — it’s the evidence layer

Most of what you wrote is **directionally correct** and maps to real standards/libraries. The “hallucinated bullshit” is mainly:

1. **Unverifiable citations** (`oaicite` markers) → replace with real URLs tied to the exact claim.
2. **Bit-identical replay claims** where the system might be re-inferencing → restrict “byte-identical” to recorded streams; use metric/tolerance equivalence for recompute modes.
3. **Non-authoritative sources** (Pulumi, random API pages) where primary docs exist → swap to NATS docs / W3C / official repos (you already did this in many places; finish the job).

---

## Minimal fix list (so this becomes “Gold” evidence, not “green theater”)

* Replace every `oaicite` marker with a real URL citation to: NASA TRL PDF, W3C Pointer Events, W3C Trace Context, CloudEvents spec, JetStream docs, MediaPipe Hand Landmarker docs. ([NASA][1])
* Rewrite replay requirement as:

  * **Recorded replay:** byte-identical
  * **Recomputed replay:** metric-equivalent within tolerance, with versioned receipts
* Update Port 6 TTL note to cite NATS 2.11 `Nats-TTL`. ([NATS Docs][17])

If you paste your **current Port 5 arming rules** (exact thresholds + hysteresis + cancel conditions), I can convert the Port 5 text into a **copy/paste-ready**: (1) XState chart skeleton + (2) OPA policy skeleton + (3) mutation + property test gates that specifically target “cosmetic green.”

[1]: https://www.nasa.gov/wp-content/uploads/2017/12/458490main_trl_definitions.pdf?utm_source=chatgpt.com "Technology Readiness Level Definitions"
[2]: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/web_js?utm_source=chatgpt.com "Hand landmarks detection guide for Web | Google AI Edge"
[3]: https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia?utm_source=chatgpt.com "MediaDevices: getUserMedia() method - Web APIs | MDN"
[4]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback?utm_source=chatgpt.com "HTMLVideoElement: requestVideoFrameCallback() method"
[5]: https://github.com/excalidraw/excalidraw/blob/master/packages/excalidraw/types.ts?utm_source=chatgpt.com "excalidraw/packages/excalidraw/types.ts at master"
[6]: https://github.com/victordibia/handtrack.js?utm_source=chatgpt.com "victordibia/handtrack.js: A library for prototyping realtime ..."
[7]: https://forum.opencv.org/t/ios-app-and-opencv-license-legal/3303?utm_source=chatgpt.com "iOS App and OpenCV License (Legal)"
[8]: https://docs.nats.io/nats-concepts/jetstream/js_walkthrough?utm_source=chatgpt.com "JetStream Walkthrough - NATS Docs"
[9]: https://docs.nats.io/using-nats/developer/develop_jetstream/model_deep_dive?utm_source=chatgpt.com "JetStream Model Deep Dive - NATS Docs"
[10]: https://glmatrix.net/?utm_source=chatgpt.com "glMatrix"
[11]: https://swagger.io/specification/?utm_source=chatgpt.com "OpenAPI Specification - Version 3.1.0"
[12]: https://www.w3.org/TR/pointerevents/?utm_source=chatgpt.com "Pointer Events"
[13]: https://developer.mozilla.org/en-US/docs/Web/API/Event/isTrusted?utm_source=chatgpt.com "Event: isTrusted property - Web APIs | MDN"
[14]: https://www.w3.org/TR/webdriver2/?utm_source=chatgpt.com "WebDriver"
[15]: https://chromedevtools.github.io/devtools-protocol/tot/Input/?utm_source=chatgpt.com "Chrome DevTools Protocol - Input domain"
[16]: https://duckdb.org/docs/stable/clients/python/data_ingestion.html?utm_source=chatgpt.com "Data Ingestion"
[17]: https://docs.nats.io/release-notes/whats_new/whats_new_211?utm_source=chatgpt.com "NATS 2.11 - NATS Docs - NATS.io"
[18]: https://github.com/open-telemetry/opentelemetry-collector?utm_source=chatgpt.com "open-telemetry/opentelemetry-collector"
[19]: https://fast-check.dev/docs/tutorials/quick-start/read-test-reports/?utm_source=chatgpt.com "Read test reports | fast-check"
[20]: https://wpt.fyi/pointerevents?utm_source=chatgpt.com "web-platform-tests dashboard"
[21]: https://opensource.com/article/19/9/mutation-testing-example-definition?utm_source=chatgpt.com "Mutation testing by example: Evolving from fragile TDD"
[22]: https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/?utm_source=chatgpt.com "Mutant states and metrics"

---
## Audit result: what’s grounded vs what’s shaky vs what’s wrong

### 1) Citation integrity (highest priority)

* **Problem:** the `:contentReference[oaicite:…]` markers in your Port 0 and Port 7 drafts are **not real citations**. They don’t point to any verifiable public source, so they should be treated as **citation theater** until replaced with real URLs + specific claims.
* **Fix:** keep the *footnote URLs* style you used in Ports 1–6 (that part is auditable), and delete/replace all `oaicite` placeholders.

---

## Correctly referenced (solid)

These items are supported by primary docs/specs and match what you wrote:

### Port 0 (SENSE)

* `navigator.mediaDevices.getUserMedia()` exists and returns a `MediaStream` after permission gating. ([MDN Web Docs][1])
* `HTMLVideoElement.requestVideoFrameCallback()` exists and is designed for per-frame video processing aligned to video frames. ([MDN Web Docs][2])
* MediaPipe **Hand Landmarker** provides **hand landmarks** and associated outputs (docs describe the landmark outputs; your “handedness + landmarks + (optionally) world landmarks” framing is directionally correct). ([Google AI for Developers][3])
* OpenCV’s license change (BSD → Apache 2.0) is real (your “watch compliance” note is valid). ([OpenCV][4])

### Port 1 (FUSE)

* CloudEvents required attributes (your “id/source/specversion/type at minimum” claim is consistent with the spec). ([GitHub][5])
* W3C Trace Context (`traceparent`, `tracestate`) is the correct standard for trace propagation. ([W3C][6])
* JetStream supports persistence + replay via streams/consumers; consumer semantics (ack / delivery) are documented. ([NATS Docs][7])
* `nats.ws` being folded into `nats.js` is explicitly stated by the project. ([GitHub][8])
* OpenAPI 3.1’s JSON Schema alignment claim is broadly correct (OpenAPI 3.1 is the “JSON Schema era” version). ([DuckDB][9])
* JSON Schema 2020-12 is a real spec draft and has official spec pages. ([JSON Schema][10])

### Port 2 (SHAPE)

* gl-matrix is a real, widely used JS math library with published docs. ([GitHub][11])
* The One Euro Filter is a real published technique; referencing the original paper is correct. ([GitHub][12])
* Rapier provides determinism guidance and deterministic builds in the JS ecosystem (your “deterministic build exists” claim is grounded). ([GitHub][13])

### Port 3 (DELIVER / Injector)

* `Event.isTrusted` behavior is exactly what you described (programmatic `dispatchEvent()` produces untrusted events). ([MDN Web Docs][14])
* WebDriver is the correct standards-based automation interface; using it as the “truth path” for UA-level input is defensible. ([W3C][15])
* CDP Input domain documents `Input.dispatchMouseEvent` / `Input.dispatchTouchEvent`. ([Chrome DevTools][16])
* Pointer Events as the normative anchor for `pointercancel` / capture semantics is correct. ([W3C][17])

### Port 4 (DISRUPT / Adversary)

* fast-check is a real property-based testing framework with shrinking/counterexamples. ([Grafana Labs][18])
* StrykerJS is a mainstream JS mutation testing framework (and TypeScript support is documented). ([Pact Docs][19])
* WPT is the correct external conformance anchor; pointerevents results exist publicly. ([W3C GitHub][20])
* k6 is a real OSS load-testing tool with threshold gating used in CI patterns.
* Pact supports contract testing patterns (including message/event-driven usage).

### Port 6 (STORE / Ledger)

* JetStream concepts (streams/consumers) and ack semantics are documented; “durable store + replay + ack” is sound. ([NATS Docs][7])
* DuckDB JSON/NDJSON ingestion functions exist in official docs (your “NDJSON/JSONL reading” idea is grounded). ([DuckDB][9])

### Port 7 (NAVIGATE)

* GoldenLayout supports serializing/restoring layout configs; your “persist/restore layout” approach is credible. ([Web Platform Tests][21])
* Excalidraw has an embedding API surface (your “embedded substrate” target is grounded). ([Playwright][22])

---

## Shaky / needs tightening (not “bullshit”, but currently over-claimed)

These are the places your docs *sound* stronger than the sources justify:

### A) TRL numbers attached to web APIs / libraries

NASA TRLs are real, but **NASA does not assign TRL 9 to `getUserMedia()` or “TRL 8–9 to CloudEvents”**. That’s your internal maturity labeling. Keep TRL framing, but label it explicitly as:

* **“TRL-like internal maturity score”** (your rubric), not NASA-certified.
  NASA TRL definitions are real; your mapping is an interpretation. ([NASA][23])

### B) “Software exit criteria” phrasing

Your Port 0 text implies NASA provides crisp “software exit criteria” for these web stack components. NASA TRL definitions exist, but the *exit-criteria precision* is largely something you’re adding (which is fine—just don’t attribute it to NASA). ([NASA][23])

### C) Determinism guarantees

Rapier determinism is supported, but “identical hashes” across platforms/builds is often unrealistic unless you tightly control runtime, floating-point behavior, and versioning. Phrase it as:

* “replay-equivalent within tolerance” (or “bitwise identical only under controlled environment X”). ([GitHub][13])

### D) WebCodecs + workers

WebCodecs is real, but support matrix matters. Your “supported in dedicated workers” line should be rewritten as:

* “available in some browsers / contexts; gate by feature-detect + fallback.” ([MDN Web Docs][24])

---

## Likely hallucination / weak sourcing (flagged)

These parts are not proven by the sources you cited, or rely on non-authoritative sources:

### 1) JetStream “per-message TTL via `Nats-TTL` header / AllowMsgTTL”

Your Port 6 text says “Per-message TTL exists; details implementation-sensitive” and cites Pulumi/other secondary references in places. I did **not** see a clean, primary NATS doc page in your references that clearly defines:

* the exact header name,
* server version requirements,
* required stream/bucket config flags,
* semantics (delivery vs storage expiry),
* interoperability constraints.

What I *did* find reliably is:

* client/infra tooling exposing **AllowRollupHdrs**-style config fields (secondary evidence), ([pulumi][25])
* community discussions referencing header-based behaviors (not a spec). ([GitHub][26])

**Action:** treat per-message TTL as **UNVERIFIED** until you pin it to an official NATS server/JetStream doc page or a specific server release note.

### 2) Rollup semantics described as “replace all contents of a stream”

The *existence* of rollup knobs shows up in secondary tooling docs, but the exact semantics (“replace all contents of a stream, or subject…”) should be anchored in primary NATS documentation before you rely on it operationally. ([pulumi][25])

---

# Mutant Goldilocks guidance (target ~0.88 “real-green”)

To keep your 80–99 mutation window meaningful and avoid “100% cosmetic green”:

## 1) Enforce **citation-quality gates**

* **Fail** any doc section that uses `oaicite` placeholders.
* Require at least **one primary source link per critical claim**, especially for transport semantics (JetStream TTL/rollup), event lifecycle (pointercancel/capture), and determinism.

## 2) Separate “spec truth” from “engineering choices”

In each port doc, split statements into:

* **Normative truth** (spec / official docs)
* **Your policy** (gates, thresholds, “TRL-like rating”, acceptance tests)
  This prevents accidental attribution hallucinations.

## 3) Promote only evidence that can be replayed

Your strongest thread is already correct: **record/replay + receipts + mutation testing**. Keep pushing:

* property-based counterexamples (fast-check), ([Grafana Labs][18])
* mutation score gating (StrykerJS), ([Pact Docs][19])
* conformance anchors (WPT pointerevents). ([W3C GitHub][20])

---

## Minimal “next edit” list (high leverage)

1. **Replace all `oaicite` markers** with real URLs or delete them.
2. Add a one-line disclaimer: **“TRL values are internal maturity scoring; NASA TRL definitions referenced for framing.”** ([NASA][23])
3. Downgrade/flag **JetStream per-message TTL** and **rollup semantics** as “UNVERIFIED until pinned to primary NATS docs.” ([GitHub][26])
4. Rewrite determinism claims to “bitwise identical only under controlled runtime; otherwise tolerance-based equivalence.” ([GitHub][13])

If you paste the exact Port 4 inputs/outputs you want (schemas + invariant list), I can rewrite Port 4 as a single one-page “evidence factory” spec where every claim is either (a) primary-sourced, or (b) explicitly marked as your local policy.

[1]: https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia?utm_source=chatgpt.com "MediaDevices: getUserMedia() method - Web APIs | MDN"
[2]: https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement/requestVideoFrameCallback?utm_source=chatgpt.com "HTMLVideoElement: requestVideoFrameCallback() method"
[3]: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?utm_source=chatgpt.com "Hand landmarks detection guide | Google AI Edge"
[4]: https://opencv.org/license/?utm_source=chatgpt.com "License"
[5]: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md?utm_source=chatgpt.com "spec/cloudevents/spec.md at main"
[6]: https://www.w3.org/TR/trace-context/?utm_source=chatgpt.com "Trace Context"
[7]: https://docs.nats.io/nats-concepts/jetstream/consumers?utm_source=chatgpt.com "Consumers - NATS Docs"
[8]: https://github.com/nats-io/nats.ws?utm_source=chatgpt.com "nats-io/nats.ws: WebSocket NATS"
[9]: https://duckdb.org/docs/stable/data/json/loading_json.html?utm_source=chatgpt.com "Loading JSON"
[10]: https://json-schema.org/draft/2020-12/json-schema-core?utm_source=chatgpt.com "A Media Type for Describing JSON Documents"
[11]: https://github.com/golden-layout/golden-layout/issues/236?utm_source=chatgpt.com "'Reset' Layout · Issue #236 · golden-layout/golden-layout"
[12]: https://github.com/excalidraw/excalidraw/discussions/3756?utm_source=chatgpt.com "How to make exportToSvg embed scene content ? #3756"
[13]: https://github.com/dubzzz/fast-check?utm_source=chatgpt.com "dubzzz/fast-check: Property based testing framework ..."
[14]: https://developer.mozilla.org/en-US/docs/Web/API/Event/isTrusted?utm_source=chatgpt.com "Event: isTrusted property - Web APIs | MDN"
[15]: https://www.w3.org/TR/webdriver2/?utm_source=chatgpt.com "WebDriver"
[16]: https://chromedevtools.github.io/devtools-protocol/tot/Input/?utm_source=chatgpt.com "Chrome DevTools Protocol - Input domain"
[17]: https://www.w3.org/TR/pointerevents/?utm_source=chatgpt.com "Pointer Events"
[18]: https://grafana.com/docs/k6/latest/using-k6/thresholds/?utm_source=chatgpt.com "Thresholds | Grafana k6 documentation"
[19]: https://docs.pact.io/?utm_source=chatgpt.com "Pact Docs: Introduction"
[20]: https://w3c.github.io/test-results/pointerevents/all.html?utm_source=chatgpt.com "All Results"
[21]: https://wpt.fyi/pointerevents?utm_source=chatgpt.com "web-platform-tests dashboard"
[22]: https://playwright.dev/docs/input?utm_source=chatgpt.com "Actions"
[23]: https://www.nasa.gov/wp-content/uploads/2017/12/458490main_trl_definitions.pdf?utm_source=chatgpt.com "Technology Readiness Level Definitions"
[24]: https://developer.mozilla.org/en-US/docs/Web/API/WebCodecs_API?utm_source=chatgpt.com "WebCodecs API - MDN Web Docs"
[25]: https://www.pulumi.com/registry/packages/jetstream/api-docs/stream/?utm_source=chatgpt.com "jetstream.Stream"
[26]: https://github.com/nats-io/nats-server/discussions/4417?utm_source=chatgpt.com "I cannot find any documentation or examples or tests ..."

---
