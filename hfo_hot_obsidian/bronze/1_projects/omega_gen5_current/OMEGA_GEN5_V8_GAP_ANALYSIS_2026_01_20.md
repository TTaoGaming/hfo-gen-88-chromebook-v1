# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen5 v8 — Gap Analysis (App + Architecture)

**Medallion:** Bronze | **Mutation Status:** 0% | **Hive:** V
**Timestamp:** 2026-01-20
**Scope:** Omega Gen5 v8 app runtime + injection/thermal/pointer semantics.

---

## 0) Executive Summary

Omega Gen5 v8 is structurally strong (contracted P1 fuse, deterministic replay harness, and a mostly W3C-shaped injector), but it still contains two coupled “debt knots”:

1) **Injection debt:** the injector is “mostly PointerEvents” but still **depends on legacy click synthesis** to drive complex UIs (e.g., Excalidraw controls). This couples correctness to UI quirks and breaks the promise of a clean W3C pointer substrate.

2) **Thermal debt:** the runtime loop exposes knobs (`camera.resolution`, `camera.fpsTarget`) and has some throttling behavior, but **there is no policy-based degradation stack** (Tier 1 visuals → Tier 2 sensing → Tier 3 FPS) controlling those knobs with explicit opt-in/opt-out semantics.

The gaps below map directly to the four themes you listed.

---

## 1) What v8 is doing today (ground truth)

### A. Injection: PointerEvents + click synthesis

- The injector emits W3C-ish PointerEvents (`pointerover/enter/out/leave`, `pointerdown`, `pointermove`, `pointerup`) and uses pointer capture when available.
- However, delivery (`dispatchToHydraHydrant`) **always synthesizes `MouseEvent('click')` on `pointerup`** (“Touchscreen emulation”). This is the core “legacy click hack”.

Evidence:

- Pointer dispatch + capture path: [omega_gen5_v8.html](omega_gen5_v8.html#L2360-L2465)
- Click synthesis on `pointerup`: [omega_gen5_v8.html](omega_gen5_v8.html#L2505-L2534)

### B. Thermal/loop behavior: RAF loop, dt clamping, camera knobs

- Main loop is `requestAnimationFrame(predictLoop)` with dt clamping to 0..100ms.
- Camera settings include `resolution` and `fpsTarget` (contracted via Zod), but there is **no explicit “Thermal Policy” layer** that decides when/how to degrade.

Evidence:

- Main loop + dt clamp: [omega_gen5_v8.html](omega_gen5_v8.html#L2158-L2255)
- Camera schema includes `resolution`/`fpsTarget`: [omega_gen5_v8.html](omega_gen5_v8.html#L722-L840)

### C. “click()” calls present, but not the injector debt

There are `a.click()` and `input.click()` calls used for export/download and file-open UI, which are fine utility UX behaviors and **not** the injection debt you described.

Evidence:

- Telemetry export / clip record download / file-open helpers: [omega_gen5_v8.html](omega_gen5_v8.html#L410-L640)

---

## 2) Gap Inventory (your four themes)

## 2.1 Abstract Pointer Interface (Decouple OmegaInjector from click hacks)

**Current:** Pointer pipeline and “legacy click synthesis” live in one coupled path.

**Gap:** There is no explicit abstraction boundary separating:

- “How we compute pointer state” (P1/P3)
- “How we emit events” (W3C PointerEvents only)
- “Whether we emulate click” (legacy UI bridging)

**Why it matters:**

- You can’t harden W3C semantics if click synthesis is always-on.
- Tests can’t distinguish pointer correctness vs UI workaround correctness.

**Target:** A pluggable adapter boundary:

- `AbstractPointerAdapter` with implementations:
  - `StandardW3CAdapter` → emits only PointerEvents; never emits click.
  - `LegacyTouchAdapter` → emits PointerEvents + optional click synthesis for specific targets/roles.

**Acceptance criteria:**

- A single feature flag (or policy decision) can disable click synthesis entirely.
- Playwright harness can assert “no click events emitted” when Standard adapter is active.

Related existing spec intent:

- Existing strategy doc already calls this out: [OMEGA_GEN5_V8_STRATEGY.md](OMEGA_GEN5_V8_STRATEGY.md#L14-L23)

## 2.2 Thermal Governance (Opt-in, policy-based degradation)

**Current:** loop runs at RAF; you have knobs (`fpsTarget`, `resolution`) and some v7 history of brute-force caps.

**Gap:** No explicit **policy engine** exists that:

- measures pressure (FPS/latency/queue depth)
- selects a tier
- enforces actions
- records evidence (telemetry)

**Target:** A policy object, not “hardcoded loop throttling”.

Suggested contract (minimal, Bronze):

- Inputs: `fpsProcessed`, `inferenceMsP95` (or rolling), `droppedFrames`, `cpuProxy` (if available)
- Output: `tier` + concrete actions (visual flags, camera constraints, fps cap)

Tier ladder (exactly as you described):

1) **Tier 1 (Visuals):** disable non-critical visuals (fallbacks)
2) **Tier 2 (Sensing):** reduce MediaPipe input resolution (CPU relief)
3) **Tier 3 (Logic):** drop FPS (last resort)

**Opt-in requirement:**

- Tier selection should be enabled via explicit user choice or a deliberate auto-mode gate.

Evidence of current intent in docs:

- [hfo_hot_obsidian/bronze/1_projects/omega_gen_5_v8_manifest.md](../omega_gen_5_v8_manifest.md#L13)
- [OMEGA_GEN5_V8_STRATEGY.md](OMEGA_GEN5_V8_STRATEGY.md#L24)

## 2.3 W3C Ground Truth (strict pointerdown/move/up alignment)

**Current:** v8 emits PointerEvents with:

- `bubbles`, `cancelable`
- `pointerId`, `pointerType: 'mouse'`
- `clientX/clientY`, plus `pressure/buttons/button`
- capture calls if supported

**Gaps / risk areas to audit:**

- `screenX/screenY` are currently assigned from viewport-space (`viewX/viewY`); this is not truly “screen space”. If any downstream consumer depends on `screenX/screenY`, behavior may drift.
- Click synthesis can mask incorrect `buttons/button` semantics because UI might react to click instead of pointer.
- Missing explicit invariants for pointer capture lifecycle: “if captured, release on up/cancel always”. (The code attempts this, but tests should enforce it.)

**Target:** A strict compliance checklist backed by replay tests:

- Always emit `pointerdown` before any “down-move” sequences.
- Always emit `pointerup` OR `pointercancel` to end an active pointer.
- When capture is set, release it on `pointerup` and on `pointercancel`.
- Do not emit “click” unless an adapter explicitly chooses to.

Evidence:

- Capture/release present: [omega_gen5_v8.html](omega_gen5_v8.html#L2421-L2461)
- Cancel path present: [omega_gen5_v8.html](omega_gen5_v8.html#L2448-L2465)

## 2.4 “DispatchEvent” audit: Align all dispatches with pointer specs

**Current:** dispatch is routed through `dispatchToHydraHydrant(t, e)`.

**Gap:** This function is doing 3 responsibilities at once:

1) dispatch event
2) “interactive ancestor selection” (`findControl`)
3) focus priming on down
4) click synthesis on up

**Target:** Split this into 2 layers:

- `PointerEventEmitter.dispatch(target, pointerEvent)` (pure)
- `UiCompatibilityBridge.maybeAugment(target, pointerEvent)` (optional)

This is the key decoupling that removes the tech debt knot.

---

## 3) Recommended Phased Plan (minimal risk)

### Phase 1 — Extract adapter boundary (no behavior change)

- Create `AbstractPointerAdapter` facade (still uses current code internally)
- Move click synthesis behind a boolean `enableClickSynthesis` defaulting to current behavior
- Add a single guardrail test: “Standard adapter emits no click events”

### Phase 2 — Implement ThermalPolicy (opt-in, Tier 1 only)

- Define `ThermalPolicy.evaluate(telemetry) -> { tier, actions }`
- Implement Tier 1 actions as feature flags only (no camera changes yet)
- Record tier decisions to telemetry so replay captures policy decisions

### Phase 3 — Tier 2 sensing controls

- When policy selects Tier 2, change camera constraints (or MediaPipe input) to 480p
- Validate with a deterministic replay that pointer semantics remain unchanged

### Phase 4 — Tier 3 fps drop (last resort)

- Only if Tier 1/2 insufficient: cap processing rate
- Ensure injector timing stays deterministic under cap (replay acceptance)

---

## 4) Concrete “Next Steps” checklist

- [ ] Add `StandardW3CAdapter` vs `LegacyTouchAdapter` switch.
- [ ] Move click synthesis out of `dispatchToHydraHydrant` into legacy adapter.
- [ ] Add pointer semantic invariant tests: “no stuck pointer”, “cancel always tears down capture”.
- [ ] Add `ThermalPolicy` skeleton and Tier 1 visual toggles.

---

## 5) Sources

- App runtime: [omega_gen5_v8.html](omega_gen5_v8.html)
- Current v8 strategy: [OMEGA_GEN5_V8_STRATEGY.md](OMEGA_GEN5_V8_STRATEGY.md)
- v8 manifest: [hfo_hot_obsidian/bronze/1_projects/omega_gen_5_v8_manifest.md](../omega_gen_5_v8_manifest.md)
