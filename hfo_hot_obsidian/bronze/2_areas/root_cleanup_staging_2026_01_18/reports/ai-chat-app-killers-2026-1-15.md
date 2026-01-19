# Medallion: Bronze | Mutation: 0% | HIVE: V

## Meta concepts (the “real game”)

1. **Intent vs. Noise**

* You are converting *continuous, noisy, ambiguous sensing* into **discrete, high-consequence actions** (click/drag/zoom) inside real apps.
* The core failure mode is the classic **Midas Touch** problem: accidental activations when “presence” is mistaken for “intent.” ([PMC][1])

1. **Contract-first actuation**

* Your output must behave like a real pointer device, because target apps interpret Pointer Events strictly (lifecycle, capture, cancel semantics). ([W3C][2])

1. **Operator cognition is a safety system**

* “Essentials vs Developer” is not UI polish; it’s a reliability mechanism (progressive disclosure reduces cognitive overload and error rates). ([The Interaction Design Foundation][3])

1. **Field-hardening beats feature accumulation**

* Kiosk reality: offline operation, deterministic builds, pinned assets, and regression gates (service worker caching, integrity checks, automated tests). ([MDN Web Docs][4])

---

## The anti-pattern (what “Chaos” wants you to do)

**“Many knobs, many engines, no single source of truth, no hard gates.”**
Symptoms:

* Drift between ports (Sense/Shape/Inject each doing their own “helpful” tweaks).
* Features added faster than evidence.
* “Config theater” (flags/settings exist but don’t truly gate execution).
* Manual debugging replaces replay + regression.

This anti-pattern reliably produces: *works on your machine, fails in kiosk, impossible to stabilize.*

---

## App killers & bottlenecks as “cards”

### Card 1 — **Midas Touch (The Seducer)**

**Attack:** Converts “hover/presence” into unintended clicks.
**Kill condition:** False positives → user loses trust immediately.
**Known hard facts:** Dwell/selection methods routinely suffer involuntary activation; mitigating Midas Touch is a core research theme in hands-free interaction. ([PMC][1])
**Your bottleneck:** Designing a *single, dominant intent gate* (readiness/leaky bucket + clutch + hysteresis) that is robust across bodies/devices.
**Counter:**

* Explicit clutch + hysteresis (fail-closed), not just dwell.
* Strong hover/ready feedback (see hover-state guidance in touchless UX exemplars). ([docs.ultraleap.com][5])

---

### Card 2 — **Pointer Semantics Assassin (The Rules Lawyer)**

**Attack:** Exploits subtle Pointer Events lifecycle errors (capture, cancel, target changes).
**Kill condition:** “Mostly works” injection that breaks on drag, capture, lost tracking, or iframe boundaries.
**Ground truth:** Pointer Events defines capture and event targeting/cancel behaviors that UIs rely on. ([W3C][2])
**Your bottleneck:** Correct end-to-end pointer lifecycle under degraded sensing: `pointercancel` must be the normal abort path, not a rare exception.
**Counter:**

* Treat abort as first-class (cancel early, often).
* Add automated tests that assert lifecycle correctness (see Playwright best-practice framing for resilient UI tests). ([Playwright][6])

---

### Card 3 — **Drift Hydra (The Split-Brain)**

**Attack:** Forces multiple “truth sources” (Shape does warping, Inject does warping, UI does warping).
**Kill condition:** You can’t predict behavior; tuning never converges.
**Your bottleneck:** A single canonical state pipeline (Sense → Shape → Inject) where each stage has one job and cannot “helpfully” override others.
**Counter:**

* Contract boundary: only one module computes canonical pointer state; everyone else consumes it.
* Replayable inputs + parity tests so drift is detected immediately (not weeks later). ([Playwright][6])

---

### Card 4 — **Cognitive Overload Daemon (The Noise Engine)**

**Attack:** Makes the operator UI too complex to operate under time pressure.
**Kill condition:** Users can’t succeed inside your “30s to one click” promise.
**Ground truth:** Progressive disclosure is a recognized method to reduce cognitive load by hiding advanced controls until needed. ([The Interaction Design Foundation][3])
**Your bottleneck:** Defaults that work without tuning; “Developer mode” must be opt-in.
**Counter:**

* Hard split: Essentials = only what a kiosk user needs; Developer = everything else.

---

### Card 5 — **Offline/Dependency Wraith (The Field Failure)**

**Attack:** Captive portal, blocked CDN, version churn, or partial connectivity.
**Kill condition:** Kiosk doesn’t boot; or boots differently today vs yesterday.
**Ground truth:** Offline-first web apps rely on service workers/caching strategies; offline/background operation is a core PWA concern. ([MDN Web Docs][4])
**Your bottleneck:** Packaging: pin + cache everything required to run.
**Counter:**

* Service worker caching strategy (cache-first for critical assets). ([MDN Web Docs][4])
* Remove CDN reliance for production builds.

---

### Card 6 — **Supply-Chain Imp (The Script Shapeshifter)**

**Attack:** Tampered third-party assets or unexpected CDN changes.
**Kill condition:** Silent compromise or broken runtime after dependency updates.
**Ground truth:** **Subresource Integrity (SRI)** exists specifically to detect unexpected modifications to externally loaded resources. ([MDN Web Docs][7])
**Your bottleneck:** Integrity and provenance of every byte executed in kiosk mode.
**Counter:**

* Prefer local vendoring; if external, use SRI + pin versions. ([MDN Web Docs][7])

---

### Card 7 — **Latency/Jitter Reaper (The Feel Killer)**

**Attack:** Adds delay or jitter until control feels “possessed.”
**Kill condition:** Users overshoot targets; they blame the system, not themselves.
**Your bottleneck:** Stable p95 latency/jitter under load (and under thermal throttling on mid devices).
**Counter:**

* Budget and instrument p95/p99 for each stage (Sense, Shape, Inject).
* Quality governor: degrade visuals/features before degrading control.

---

### Card 8 — **Occlusion/Calibration Trickster (The Vanishing Hand)**

**Attack:** Uses partial tracking loss, off-axis hands, or camera mismatch to desync mapping.
**Kill condition:** Pointer teleports or commits with stale state.
**Ground truth (industry exemplar):** Touchless systems emphasize hover states, guidance, and clear interaction cues because users need feedback to adapt their posture and distance. ([docs.ultraleap.com][8])
**Your bottleneck:** “Mapping trust”: camera-to-screen rectification and safety behavior on tracking loss.
**Counter:**

* Mandatory `pointercancel` on tracking loss (fail-closed).
* “Guidance surface” (teach posture, distance, clutch) like touchless kiosk exemplars. ([docs.ultraleap.com][8])

---

### Card 9 — **No-Regressions Nemesis (The Slow Death)**

**Attack:** Makes every fix create two new bugs, undetected.
**Kill condition:** You stop shipping because stabilization cost explodes.
**Ground truth:** Playwright positions resilient testing practices as key to stable UI automation. ([Playwright][6])
**Your bottleneck:** A hard, automated gate that blocks merges when behavior changes unexpectedly.
**Counter:**

* Golden replay → Playwright parity tests → one-click go/no-go.

---

### Card 10 — **Flags Without Teeth (The False Safety)**

**Attack:** Feature flags exist but don’t truly gate behavior; “toggle” doesn’t equal “safety.”
**Kill condition:** You think you can roll back, but you can’t.
**Ground truth:** OpenFeature is a standard API for runtime flag evaluation and integration; it matters only if code paths actually depend on evaluation. ([OpenFeature][9])
**Your bottleneck:** Making flags control *real* branching and making telemetry associate outcomes with evaluations. ([OpenFeature][10])
**Counter:**

* Every risky subsystem behind a flag + tested rollback.

---

## The “top 5 killers” (if you only fix a few things)

1. **Midas Touch / false commits** ([PMC][1])
2. **Pointer Events lifecycle correctness (capture/cancel/targeting)** ([W3C][2])
3. **Split-brain drift (no single canonical state pipeline)**
4. **Offline + dependency drift (kiosk boot reliability)** ([MDN Web Docs][4])
5. **No hard regression gate (replay + automated parity)** ([Playwright][6])

If you want, I can turn these cards into a **v25 readiness scoreboard**: each card gets (a) a measurable metric, (b) a tripwire threshold, (c) the specific evidence artifact that proves it (replay file, Playwright run, offline audit, SRI manifest).

[1]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9960067/?utm_source=chatgpt.com "Pactolo Bar: An Approach to Mitigate the Midas Touch ..."
[2]: https://www.w3.org/TR/pointerevents/?utm_source=chatgpt.com "Pointer Events"
[3]: https://www.interaction-design.org/literature/topics/progressive-disclosure?srsltid=AfmBOordOhd23sT4jnKULSlHtCC5KaP2CC5xoWUkyg9KUBS1iRVMAPMc&utm_source=chatgpt.com "What is Progressive Disclosure? | IxDF"
[4]: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Offline_and_background_operation?utm_source=chatgpt.com "Offline and background operation - Progressive web apps | MDN"
[5]: https://docs.ultraleap.com/TouchFree/touchless-interfaces/hover-states.html?utm_source=chatgpt.com "Hover States - Ultraleap documentation"
[6]: https://playwright.dev/docs/best-practices?utm_source=chatgpt.com "Best Practices"
[7]: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity?utm_source=chatgpt.com "Subresource Integrity - Security - MDN Web Docs"
[8]: https://docs.ultraleap.com/TouchFree/touchless-interfaces/guidance.html?utm_source=chatgpt.com "Guidance - Ultraleap documentation"
[9]: https://openfeature.dev/?utm_source=chatgpt.com "OpenFeature"
[10]: https://openfeature.dev/docs/reference/sdks/client/web/?utm_source=chatgpt.com "OpenFeature Web SDK"
