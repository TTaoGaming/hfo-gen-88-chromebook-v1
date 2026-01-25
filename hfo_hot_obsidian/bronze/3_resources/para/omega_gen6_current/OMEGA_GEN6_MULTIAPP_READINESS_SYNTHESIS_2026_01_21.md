# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen6: Multi-App Readiness Synthesis (from Gen5 v12 baseline)

Date: 2026-01-21

## What this folder is

This folder is a **non-destructive staging area** for Gen6 work:

- It contains a copy of the latest Gen5 v12 artifacts + dependencies so we can refactor without risking Gen5 drift.
- It is intended to become the **Gen6 multi-app substrate workbench** (single authority, hot-swap, same substrate).

## What was cloned here (grounded)

Copied from Gen5 current into this folder:

- Gen5 v12 multi-app substrate: [omega_gen5_v12.html](omega_gen5_v12.html)
- Gen5 v12.1 Dino variant: [omega_gen5_v12_1_dino_v1.html](omega_gen5_v12_1_dino_v1.html)
- Wrappers: [excalidraw_v20_wrapper.html](excalidraw_v20_wrapper.html), [dino_v1_wrapper.html](dino_v1_wrapper.html)
- Dependencies: [lib/](lib/), [official_adapters/](official_adapters/)
- Vendored Dino target: [vendor/t-rex-runner/](vendor/t-rex-runner/)
- Reference specs: [GEN5_V12_MULTIAPP_SHARED_SUBSTRATE_SPEC_2026_01_20.yaml](GEN5_V12_MULTIAPP_SHARED_SUBSTRATE_SPEC_2026_01_20.yaml), [GEN5_V13_ADAPTER_HOTSWAP_SPEC_2026_01_21.yaml](GEN5_V13_ADAPTER_HOTSWAP_SPEC_2026_01_21.yaml)

Note: the cloned [dino_v1_wrapper.html](dino_v1_wrapper.html) was made **self-contained** in Gen6 by pointing its iframe to `./vendor/t-rex-runner/index.html`.

## Gen6 goal (single sentence)

Gen6 = **one shared HERO substrate** running one camera + one intent/FSM + one injector/router, while multiple apps are mounted/unmounted as adapters with **correct hot-swap semantics**.

## Biggest issues blocking a clean Gen6 multi-app evolution

These are ordered by “root-cause leverage” (fixing earlier items makes later problems easier).

### 1) App lifecycle correctness (the hot-swap race)

**Problem:** UI can switch “active app” before the iframe is fully loaded, routable, and focused. This creates the illusion that the injector is broken.

**Gen6 requirement:** App activation must be:

- centralized (one authority: AppHost)
- idempotent (activating active app is a no-op)
- readiness-gated (iframe `load` + explicit adapter-ready signal)

Grounding:

- Transition notes already call out the readiness barrier as the missing hardening step.

### 2) Target routing must be fail-closed (ACTIVE_APP_ONLY) across all apps

**Problem:** multi-app only works if hit-testing and injection always resolve inside the *currently active* adapter root.

**Gen6 requirement:**

- `P3_TARGET_ROUTER` must always gate target selection when `ACTIVE_APP_ONLY` is enabled.
- If routing cannot resolve a target inside the active iframe document, injection should **stop**, not “best-effort” into the wrong surface.

Why this matters:

- Without fail-closed routing, multi-app becomes non-deterministic and feels haunted.

### 3) Keyboard injection is a separate capability with focus contracts

**Problem:** some adapters (Dino) are keyboard-driven. Synthetic key events often fail if focus is wrong.

**Gen6 requirement:**

- Treat keyboard synthesis as a **capability** in the adapter manifest (not hardcoded by appId).
- Standardize a “focus interlock” protocol:
  - parent focuses iframe window
  - adapter focuses its inner document/body/canvas
  - only then emit keydown/keyup

Why this matters:

- Multi-app + keyboard is a force multiplier, but only if focus is deterministic.

### 4) Camera / background video failures are often configuration, not rendering

**Problem:** “background video missing” can be a boot flag issue (camera disabled) or autoplay policy mismatch.

**Gen6 requirement:**

- Make camera authority explicit: exactly one capture pipeline.
- Ensure multi-view video mirrors are derived from that authority.
- Ensure defaults don’t silently disable sensing when running “demo” mode.

Grounding:

- The cast-ready transition doc flags default harness camera-disable as a root cause for missing video.

### 5) Contracts drift: Gen6 needs a single authoritative AdapterManifest

**Problem:** multi-app systems die from ‘almost-the-same’ schemas spread across ports.

**Gen6 requirement:**

- One schema for adapter metadata (P1-owned contract), minimally:
  - `appId`, `title`, `entrypoint`, `pointerAdapter`, `targetPolicy`, `capabilities`
  - optional: `heroSlotId` (if dual-HERO experiment is kept)

Why this matters:

- This is how we prevent “per-app if statements” from creeping into P3.

### 6) Performance budget: don’t grow per-frame work in the injector loop

**Problem:** multi-app multiplies surfaces; naive per-frame scanning will tank FPS and add latency.

**Gen6 requirement:**

- Keep per-frame injector work constant-time.
- Move discovery/handshake work to lifecycle (activation time), not injection time.

### 7) Missing Pareto gates for multi-app hot-swap

**Problem:** manual testing hides regressions; multi-app needs at least 2–3 deterministic tests.

**Gen6 minimum gates:**

- A → B hot-swap (no reload) with ACTIVE_APP_ONLY routing assertion.
- A → B → A rapid swap.
- One keyboard-driven adapter gate (Dino) proving at least one deterministic input lands.

## Do we need refactor before “Gen6”?

Yes — but only **surgical refactor**, not a rewrite.

Gen6 should start as:

- a clone of v12 with stricter activation/readiness semantics
- manifest-driven adapter capabilities
- routing always through TargetRouter

Avoid:

- “dual-HERO” or cross-device casting until single-device hot-swap is rock-solid.

## Suggested Gen6 work order (low-drama)

1) Normalize AdapterManifest (single schema) and make AppHost consume it.
2) Add readiness gating for iframe adapters (`load` + `postMessage` ready ack for same-origin).
3) Convert Dino key synthesis from appId-hardcode → capability-driven mapping.
4) Add the 3 Pareto gates.
5) Only then: consider dual-HERO or cast-ready split (controller vs display).

## How to run (local)

- Open [omega_gen5_v12.html](omega_gen5_v12.html) from this folder (Live Server recommended).
- For Dino variant, open [omega_gen5_v12_1_dino_v1.html](omega_gen5_v12_1_dino_v1.html) and select the Dino adapter.

## Source links (design evidence)

- [Gen5 v12→v13 Pareto multi-app substrate](../../reports/GEN5_V12_TO_V13_TRANSITION_PARETO_MULTIAPP_GESTURE_SUBSTRATE_2026_01_21.md)
- [Gen5 v12→v13 cast-ready framing](../../reports/GEN5_V12_TO_V13_TRANSITION_CAST_READY_2026_01_21.md)
- [Gen5 v12 multi-app shared substrate spec](../../1_projects/omega_gen5_current/GEN5_V12_MULTIAPP_SHARED_SUBSTRATE_SPEC_2026_01_20.yaml)
- [Gen5 v13 adapter hotswap spec](../../1_projects/omega_gen5_current/GEN5_V13_ADAPTER_HOTSWAP_SPEC_2026_01_21.yaml)
