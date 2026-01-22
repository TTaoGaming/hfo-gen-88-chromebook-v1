# Medallion: Bronze | Mutation: 0% | HIVE: V
# Gen5 v12 → v13 Transition: Pareto-Optimal Multi-App Gesture Substrate
Date: 2026-01-21

## Why this doc exists
You are actively iterating on Gen5 v12 (and v12.1 Dino). v13 is the next stabilization step: keep a single, stable HERO tactical substrate while swapping adapter apps (same control plane, same W3C pointer output).

This is a **tight transition checklist**: what’s already true in v12, what must be added/normalized for v13, and what “Pareto optimal” looks like (80–99% mutation-score-style confidence without gold-plating).

## Ground truth (what exists right now)
**v12 multi-app substrate is real and already wired**:
- P7 AppHost can register and activate iframe-based adapters and exposes `getActiveTargetRootElement()` (see AppHost surface in [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html#L2938-L3010)).
- P3 Target Router exists and can enforce `ACTIVE_APP_ONLY` hit-testing inside the active same-origin iframe (see [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html#L3011-L3219)).
- GoldenLayout tab activation → AppHost activation is present (multi-app “App:*” tabs).
- Dropdown → AppHost activation exists and is already gated in Playwright.

**v12.1 Dino variant exists**:
- Dino adapter is registered as `appId: 'dino-v1'` and is intended to be default-active in that variant.
- COMMIT edge → Space keypress synthesis for Dino is implemented inside the P3 injector loop (see [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12_1_dino_v1.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12_1_dino_v1.html#L3270-L3340)).
- Wrapper ensures same-origin vendored Dino is embedded and best-effort focused (see [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/dino_v1_wrapper.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/dino_v1_wrapper.html)).

**Entry point defaults already enable multi-app + active-app routing for v12**:
- v12 is the default target plus key flags are on (see [active_hfo_omega_entrypoint.json](active_hfo_omega_entrypoint.json#L13-L22)).

**There is already a v13 spec draft**:
- Hot-swap goals + optional dual-HERO experiment are spelled out in [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V13_ADAPTER_HOTSWAP_SPEC_2026_01_21.yaml](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V13_ADAPTER_HOTSWAP_SPEC_2026_01_21.yaml).

## Pareto-optimal definition (for this transition)
Pareto-optimal here means:
- **Keep the substrate invariant** (ports + injection pipeline + HERO) while swapping adapters.
- **Hexagonal outputs**: the control plane emits **W3C PointerEvents** (and optionally keyboard events) only.
- **Fail-closed routing when enabled**: if `ACTIVE_APP_ONLY` is requested and no target is routable, injection stops.
- **Minimal yet high-leverage gates**: 1–2 deterministic Playwright gates per adapter class, plus one “rapid hot-swap” gate.
- **Mutation-score mindset** (target zone 80–99): prioritize tests that would actually catch regressions in routing/activation, not broad coverage theater.

## What v13 should be (delta vs v12)
v13 should be a **minimal clone of v12** where we harden hot-swap semantics and normalize adapter intake.

### v13 goals (tight)
1) Hot-swap is **no-reload**: switching adapters does not restart substrate ports.
2) Routing is **always consistent** under `ACTIVE_APP_ONLY`.
3) Adapter-specific behavior is selected by **manifest metadata**, not hardcoded app IDs.
4) Adapter intake is **same-origin vendored** with provenance (official/beloved sources preferred).

### v13 non-goals (keep it lean)
- No architecture rewrite.
- No cross-origin iframe support.
- No heavy end-to-end “strict defend” promotion unless it stays stable on Chromebook constraints.

## Current gaps (what you’re still missing for hardened multi-app)
### A) Readiness / lifecycle correctness (hot-swap stability)
- **Activation readiness barrier**: AppHost can toggle overlays immediately; v13 should standardize a readiness signal so “active” is not declared until the iframe is loaded and routable.
  - Practical: an iframe `load` + a tiny `postMessage('adapter.ready')` handshake (same-origin) is enough.
- **Idempotency & teardown**: activating the same app twice should be a no-op; deactivation should reliably hide overlays and not leave stale pointer-capture locks.

### B) Contracts (P1-owned, cross-port)
- v12 has some schema logic inline (e.g., target policy enum), but v13 needs **one authoritative AdapterManifest contract**.
- Minimum contract fields (suggested):
  - `appId`, `title`, `kind`, `entrypoint`, `targetPolicy`, `pointerAdapter`, `runtime.{overlayKey,iframeKey}`
  - Optional `capabilities` (e.g., `keyboardSynthesis`, `multiTouch`, `stylus`) for gating/tests.

### C) Adapter intake posture (“official-only”)
- Intake docs exist, but v13 needs a repeatable pattern:
  - vendored assets + pinned version
  - LICENSE captured
  - provenance filled
  - one deterministic gate per adapter

### D) Test/gates coverage (Pareto set)
You already have a good v12 gate verifying dropdown swap + `resolveTargetAt()` inside the active iframe.
What’s missing is the minimal set that catches real regressions:
- Rapid swap test: A → B → A within one session, verifying routing each time.
- Dino test (variant): default active + routing + key synthesis lands.

### E) Performance / Chromebook constraints
- Keep adapters lightweight and same-origin.
- Avoid growing per-frame work inside the injector loop.

## Pareto checklist for v12 → v13
### 1) Control plane invariants (keep)
- W3C PointerEvents emission stays the default.
- `ACTIVE_APP_ONLY` routing stays the default policy for adapter iframes.
- No adapter gets special-case logic in the injector *except through metadata*.

### 2) Adapter model (normalize)
- Every adapter is a manifest entry in AppHost.
- Every iframe adapter has:
  - a dedicated overlay element
  - a dedicated iframe element
  - deterministic IDs (`${appId}-overlay`, `${appId}-iframe`) or a strict mapping function

### 3) Hot-swap semantics (harden)
- When an adapter is activated:
  - overlay becomes visible
  - overlay tuning re-applies
  - readiness barrier completes (iframe load + adapter ready)
  - only then does P7 report it “active”

### 4) Routing semantics (harden)
- When `flag-p3-target-active-app=true`:
  - P3 injector always asks P3_TARGET_ROUTER first
  - if policy is `ACTIVE_APP_ONLY` and no inner target is resolvable, injection returns early (already true in v12 routing path)

### 5) Adapter-specific behavior (make contract-first)
- Prefer: `pointerAdapter` / `capabilities` metadata drives any special casing.
- Avoid: `if (activeId === 'some-app') { ... }` patterns in v13.
  - Dino v12.1 currently has a deliberate `activeId === 'dino-v1'` binding; in v13, convert this to a capability-driven mapping.

### 6) Pareto gates (recommended minimum)
- v13: **dropdown hot-swap gate**
  - Select adapter A → confirm overlay visible → confirm `resolveTargetAt` resolves inside A iframe document
  - Select adapter B → same assertions
- v13: **rapid A/B/A**
  - A → B → A without reload; each time routing resolves inside active iframe
- v13: **Dino action binding** (if Dino remains in-catalog)
  - Activate Dino → ensure routing resolves inside Dino iframe
  - Trigger one deterministic action (keypress or pointer) and observe a predictable DOM change if possible

Existing v12 gate reference:
- Dropdown selects `breakout-mdn` and asserts `resolveTargetAt` target ownerDocument is the iframe document in [scripts/omega_gen5_v12_multiapp_intent_pointerlab.spec.ts](scripts/omega_gen5_v12_multiapp_intent_pointerlab.spec.ts#L158-L228).

## Recommended v13 transition steps (do these in order)
1) Create v13 artifact by cloning v12 (rename-only) and do not change substrate ports.
2) Extract/centralize adapter manifest schema (P1-owned) and keep P7 AppHost consuming it.
3) Add readiness barrier semantics for iframe adapters.
4) Convert any per-app binding (like Dino key synthesis) to capability-driven binding.
5) Add the Pareto Playwright gates.
6) Add 1–2 official adapters using the intake template (not bespoke demos).

## Notes for your current v12.1 Dino experimentation
- The Space synthesis code is already best-effort focusing the iframe window/doc before dispatching keydown/keyup (see [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12_1_dino_v1.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12_1_dino_v1.html#L3270-L3340)).
- The wrapper also attempts focus on `load` and `pointerdown` (see [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/dino_v1_wrapper.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/dino_v1_wrapper.html)).
- If jump is flaky, the next Pareto tweak is: ensure the iframe’s inner canvas/body receives focus deterministically, and optionally map `ArrowUp` as fallback.

## Source map
- v12 baseline artifact: [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html)
- v12.1 Dino variant: [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12_1_dino_v1.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12_1_dino_v1.html)
- Dino wrapper: [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/dino_v1_wrapper.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/dino_v1_wrapper.html)
- v12.1 Dino spec: [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V12_1_DINO_V1_ASSIMILATION_SPEC_2026_01_21.yaml](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V12_1_DINO_V1_ASSIMILATION_SPEC_2026_01_21.yaml)
- v13 spec draft: [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V13_ADAPTER_HOTSWAP_SPEC_2026_01_21.yaml](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V13_ADAPTER_HOTSWAP_SPEC_2026_01_21.yaml)
- v12 multiapp routing gate: [scripts/omega_gen5_v12_multiapp_intent_pointerlab.spec.ts](scripts/omega_gen5_v12_multiapp_intent_pointerlab.spec.ts)
- Active entrypoint config (v12 default + flags): [active_hfo_omega_entrypoint.json](active_hfo_omega_entrypoint.json)
