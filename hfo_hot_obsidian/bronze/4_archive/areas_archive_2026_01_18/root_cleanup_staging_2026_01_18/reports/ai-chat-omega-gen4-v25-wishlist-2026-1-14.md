# Medallion: Bronze | Mutation: 0% | HIVE: V

## Where you are vs. your Omega/V25 vision

You are *very close* on the **core control-plane** (Sense → Bridge/Contracts → Shape → Inject), and you’ve already built several “production-ish” properties that most prototypes never reach: **fail-closed gating**, **contract validation**, **feature flags**, **resource lifecycle control**, **telemetry record/replay**, and **viewport parity**.

### What you clearly have now (aligned to the vision)

* **Anti-Midas interaction contract is real, not hand-wavy**

  * Palm-facing gate + leaky-bucket readiness + explicit commit gesture → **IDLE/READY/COMMIT/COAST** with seat/primary-hand logic and confidence handling (this is the right family of “gaze-and-commit” / “dwell-and-commit” patterns). ([Microsoft Learn][1])
  * Your UI already visualizes readiness/hysteresis (sparklines + thresholds + state coloring).
* **Contracts + tunables are first-class (good “no magic numbers” trajectory)**

  * Zod config schema + validated sync into recognizer options + UI sliders (this is the correct direction for V25 “user-tunable dynamics”).
* **Viewport/coordinate parity work is solid**

  * You explicitly compute the `object-fit: contain` video box and apply the same bounds to overlay layers and the Excalidraw layer to prevent drift/misalignment.
* **Hardening mechanics that matter**

  * Lifecycle manager + single-engine invariant disposal (prevents “zombie engines” / leaks when panels re-init).
  * Telemetry recorder + JSONL export + player (the beginnings of your “golden master” harness).
  * Feature-flag substrate (OpenFeature) to keep experiments reversible. (Present in your code; aligns with your overall doctrine.)

## What you’re missing (relative to V25 “production hardening”)

These are directly called out by your V25 spec, and they’re also the things most likely to block “works anywhere”:

1. **Offline / dependency assimilation**

* V25 requires staging CDN deps locally and “zero external requests.”
* Right now you’re still pulling multiple critical libs from CDNs (GoldenLayout, Babylon, OpenFeature, etc.). *This will bite reliability and reproducibility.*

1. **User-tunable readiness dynamics (fill/drain) as *rates*, not time constants**

* V25 explicitly wants `fillRate` / `drainRate` that update visual feedback and transitions immediately.
* Current implementation is effectively “derived rates” from `chargeTimeMs/releaseTimeMs/coastDrainTimeMs`. It works, but production tuning is easier if the UI controls the actual rates (and you derive times where needed).

1. **Excalidraw spatial buffer (ergonomic bezel margin)**

* V25 calls out “edge collisions” and requires a user-defined buffer for the iframe to make near-bezel UI reachable on Chromebook.
* You have the parity box; you still need the *buffer* control and the proof (50px requirement).

1. **Onboarding + calibration (your stated weakest point)**

* You don’t yet have a tight “first 60 seconds” guided flow that teaches:

  * what READY looks like,
  * how COMMIT triggers,
  * how to *exit* (palm-away),
  * what COAST means,
  * and how to recover.
* This is exactly where touchless systems win/lose; Ultraleap explicitly warns that clear guidance is critical for touchless scrolling/interaction. ([Ultraleap Documentation][2])

## Your “charge bar with ticks” idea: what the pattern is called

* **Dwell progress indicator** / **dwell-to-activate progress** (often paired with **gaze-and-dwell** or **dwell-to-select** UI). ([Microsoft Learn][3])
* In your case it’s “**dwell-to-arm + commit**” (two-stage), which maps closely to “**gaze and commit**” style interaction models (targeting + explicit commit). ([Microsoft Learn][1])

Your proposed mapping (grey IDLE → amber READY → cyan COMMIT) is correct as long as:

* color is redundant with shape/animation (accessibility),
* and COMMIT has an unmistakable “down / captured” indicator.

## Project killers (highest risk first)

1. **“ANY W3C Pointer consumer” assumption**

* In a normal browser sandbox you cannot arbitrarily control cross-origin apps the way you can control your own DOM; **same-origin policy** limits programmatic access to iframe contents and DOM. ([Invicti][4])

  * If your “any consumer” plan includes *cross-origin* web apps, you’ll likely need a **browser extension**, **native wrapper**, or make the target **same-origin** (self-host / bundle).

1. **Onboarding/calibration failure**

* If a user can’t learn it in <1 minute and can’t recover from mistakes confidently, they’ll churn even if the core tech is strong. Touchless UI guidance is repeatedly emphasized in real deployments. ([Ultraleap Documentation][2])

1. **Pointer semantics edge cases**

* Production reliability requires strict adherence to Pointer Events behaviors (capture/cancel/up/down ordering, tracking loss → cancel, etc.). The spec is clear but the edge cases are where “feels broken” happens. ([W3C][5])

1. **Offline reliability / reproducibility**

* CDNs and remote models are a hidden “random failure injector.” V25 already flags this as a must-fix.

1. **Performance cliffs on midrange mobile**

* You’re doing the right thing by keeping Babylon to “secondary visuals only,” but onboarding overlays + telemetry + multi-window + video can still push thermal throttling. Treat perf budgets as part of the contract.

## V25 wishlist to be production-ready “SOTA”

This is the shortest list that closes the biggest gaps:

* **Offline mode (must)**

  * Localize all dependencies into `lib/` and load MediaPipe WASM/model locally; prove “0 external requests.”

* **Readiness dynamics as first-class tunables (must)**

  * Replace time-based magic with explicit `fillRate/drainRate` controls; visuals update immediately.

* **Excalidraw buffer slider + passing proof (must)**

  * Implement and verify 50px+ buffer reachability; this is explicitly a success criterion.

* **Onboarding tutorial overlay (must)**

  * 3 steps, always visible:

    1. “Show palm to arm (watch bar fill)”
    2. “Commit gesture to click/drag”
    3. “Turn palm away to exit”
  * Include live “why not armed” hints (palm angle too low, confidence low, etc.).

* **Hard pointer-event compliance mode (should)**

  * A debug panel that shows current pointer state machine + emitted events + cancellations (grounded to Pointer Events spec). ([W3C][5])

* **Reality check on “any consumer” (must decision)**

  * Decide: **same-origin targets only** (self-hosted apps like Excalidraw) vs. **extension/native wrapper** path for general web apps (because SOP is not negotiable). ([Invicti][4])

If you want, I can turn the wishlist into a V25 “Definition of Done” checklist that matches your medallion style (Bronze/Silver/Gold) and maps each item to a measurable test (network tab, pointer-event trace, onboarding pass rate, etc.).

[1]: https://learn.microsoft.com/en-us/windows/mixed-reality/design/gaze-and-commit-eyes?utm_source=chatgpt.com "Eye-gaze and commit - Mixed Reality"
[2]: https://docs.ultraleap.com/TouchFree/touchless-interfaces/scrolling-panning-rotating.html?utm_source=chatgpt.com "Scrolling, Panning and Rotating - Ultraleap documentation"
[3]: https://learn.microsoft.com/en-us/windows/mixed-reality/design/gaze-and-dwell?utm_source=chatgpt.com "Gaze and dwell - Mixed Reality"
[4]: https://www.invicti.com/white-papers/whitepaper-same-origin-policy?utm_source=chatgpt.com "Definitive Guide to Same-origin Policy (SOP)"
[5]: https://www.w3.org/TR/pointerevents1/?utm_source=chatgpt.com "Pointer Events"
---
## Most helpful (highest leverage for v25)

### 1) Cursor-attached **dwell / charge feedback** with a clear “final state”

* Use a **continuous progress indicator** while arming (your leaky-bucket). Microsoft explicitly recommends continuous feedback and a clear final state indicator for dwell-based activation. ([Microsoft Learn][1])
* Ultraleap’s TouchFree guidance emphasizes keeping onboarding **simple and immediately understandable**, with clear visual guidance for touchless interaction. ([Ultraleap Documentation][2])

**Your idea (vertical bar + ticks + color shift) maps cleanly to:**

* “**dwell progress indicator**” / “**progress-to-click**” patterns. ([Microsoft Learn][1])

### 2) A 30–60s **interactive micro-tutorial** (practice before use)

* Ultraleap recommends onboarding/tutorials that let users **practice interactions** before real tasks (especially when the interaction model is new). ([Ultraleap Documentation][3])

Minimal steps that match your model:

1. Show palm → reach READY (bar fills)
2. Pinch+PointerUp → COMMIT (click/drag)
3. Turn palm away → exit/reset

### 3) “Look-away / exit-to-reset” as a first-class safety rule

* In dwell systems, “look away before reselecting” is a known mitigation against repeated/unintended activation. Your “turn palm away to exit/reset” is the hand-tracking analog. ([Tobii Dynavox Global][4])

### 4) Make **pointercancel** the dominant failure mode under uncertainty

* Pointer interactions can be aborted by the UA; if you rely only on `pointerup`, you can create stuck-drag states. Implementing `pointercancel` handling is explicitly important. ([Client-Side JavaScript][5])
* Treat: tracking loss, confidence collapse, state violations, perf collapse ⇒ **immediate cancel + cleanup**.

### 5) Decide your “ANY W3C pointer consumer” strategy upfront (security boundary)

* You cannot programmatically reach into **cross-origin iframes** due to same-origin policy; this is not negotiable. ([MDN Web Docs][6])
  **Practical paths:**
* Same-origin wrapper (self-host targets like Excalidraw)
* Browser extension / native wrapper if you truly want “any site/app”

### 6) Simple printed/overlay “awareness” cues (kiosk lesson)

* TouchFree docs explicitly call out **awareness + simple guidance** as step 1 and step 2 of onboarding. ([Ultraleap Documentation][2])

---

## Most harmful (things likely to derail you)

### 1) Expanding gesture vocab before onboarding is solved

More gestures increases: user confusion, misclassification edges, and accidental mode transitions. You already have a strong minimal language—keep it minimal until onboarding is proven.

### 2) Relying on color alone for state safety

Grey/amber/cyan is fine, but if you don’t also change **shape/label/animation**, some users will misread state. Microsoft warns about feedback that creates anxiety or misleads intent; clarity matters more than flair. ([Microsoft Learn][7])

### 3) Shipping without hard invariants (down must end in up/cancel)

The fastest way to kill trust is a stuck-down pointer or a “ghost drag.” Make invariants measurable and enforced (especially around `pointercancel`). ([Client-Side JavaScript][5])

### 4) Assuming cross-origin DOM access will “work later”

If your injection depends on `iframe.contentDocument`, it will fail as soon as the target is hosted differently. Same-origin restrictions are fundamental. ([MDN Web Docs][6])

### 5) Adding heavy visuals that compete with control reliability

Even if performance “feels good” in your setup, extra GPU particles/meshes increase thermal/GC risk on midrange devices. Reliability beats spectacle until you have budgets + degrade modes.

---

## Concrete v25 priority order (if you want SOTA in your lane)

1. **Onboarding overlay**: cursor-attached charge bar + labels + 3-step practice tutorial. ([Ultraleap Documentation][2])
2. **Safety invariants**: pointercancel-first under uncertainty; “no stuck down” gates. ([Client-Side JavaScript][5])
3. **Calibration**: quick distance/posture capture to tune thresholds/rates. (Keep it 10–15s.)
4. **Security model decision**: same-origin target set vs extension/native wrapper. ([MDN Web Docs][6])

If you paste your current onboarding UI plan (screens/steps), I can rewrite it into production-ready microcopy + state-based triggers tied directly to IDLE/READY/COMMIT/COAST and the dwell meter behavior.

[1]: https://learn.microsoft.com/en-us/windows/mixed-reality/design/gaze-and-dwell-eyes?utm_source=chatgpt.com "Eye-gaze and dwell - Mixed Reality"
[2]: https://docs.ultraleap.com/TouchFree/touchless-interfaces/guidance.html?utm_source=chatgpt.com "Guidance - Ultraleap documentation"
[3]: https://docs.ultraleap.com/xr-guidelines/Getting%20started/tutorials_hints_tip.html?utm_source=chatgpt.com "Tutorials, hints, and help - Ultraleap documentation"
[4]: https://www.tobiidynavox.com/blogs/support-articles/what-selection-options-are-available-in-windows-control?utm_source=chatgpt.com "What selection options are available in Windows Control?"
[5]: https://blog.carlosrojas.dev/the-complete-guide-to-pointer-events-21e44b2f9da0?utm_source=chatgpt.com "The Complete Guide to Pointer Events. | by Carlos A. Rojas"
[6]: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy?utm_source=chatgpt.com "Same-origin policy - Security - MDN Web Docs - Mozilla"
[7]: https://learn.microsoft.com/en-us/windows/mixed-reality/design/gaze-and-dwell-head?utm_source=chatgpt.com "Head-gaze and dwell - Mixed Reality"
