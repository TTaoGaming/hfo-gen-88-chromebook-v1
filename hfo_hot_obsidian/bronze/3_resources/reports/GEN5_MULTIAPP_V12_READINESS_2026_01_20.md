# Medallion: Bronze | Mutation: 0% | HIVE: V

# Report: Gen5 Multi-App v12 Readiness

Date: 2026-01-20

## Executive Summary

Gen5 v11 is **very close to being a multi-app substrate** in the sense that it already has:

- A working **GoldenLayout shell** with a “hero” workspace container.
- A stable **W3C-ish PointerEvent injection pipeline (P3)** that can target elements inside iframes when same-origin.
- A stable **Babylon visual substrate** for cursor/visual overlays.
- A strict-hex façade surface (`window.hfoPorts`) + tokenized registry (`window.hfoRegistry`) that is already used by the test harness.

What it does **not** yet have is the missing *orchestration layer* that turns “a single integrated demo app (Hero + Excalidraw overlay)” into “multiple apps you can swap in/out as tabs” **safely**:

- No explicit **App Host** abstraction (app registry, lifecycle, capabilities, activation).
- No explicit **active target routing** for P3 injection (currently uses `elementFromPoint` discovery at runtime).
- No contract-enforced **AppManifest** / **IntentManifest** schema that other apps can depend on.

So: **v11 = substrate + one app. v12 = substrate + app host + app plugins.**

## Evidence: What v11 already has (ready for reuse)

### 1) GoldenLayout shell is already in the artifact

- v11 imports and instantiates GoldenLayout and builds a kiosk/dev layout plan.
  - See layout engine + `initLayout()` in [omega_gen5_v11.html](../../1_projects/omega_gen5_current/omega_gen5_v11.html#L4217-L4545).
- The current plan includes a single “hero” stack and supporting panels (`navigator`, `logs`, etc).
  - The “hero” component owns the main workspace (video + overlays + app iframe overlay).

### 2) A “Hero” workspace container exists (good for being the multi-app host)

- The `hero` component creates the `hero-view-container` and mounts:
  - video (`#video-feed`)
  - Babylon overlay container (`#babylon-juice-overlay`)
  - overlay canvas (`#overlay-canvas`)
  - an Excalidraw iframe overlay (`#excalidraw-iframe`) behind a flag
  - See [omega_gen5_v11.html](../../1_projects/omega_gen5_current/omega_gen5_v11.html#L4262-L4441).

This is already the right place to evolve into “AppHost”: it’s one bounded rectangle with known lifecycle hooks (`destroy` handler exists).

### 3) P3 delivers W3C-ish pointer injection and already handles iframes

- P3 chooses targets by:
  - preferring the Excalidraw overlay iframe when visible,
  - else doing `document.elementFromPoint(viewX, viewY)` and, if it hits an iframe, probing inside.
  - It also supports pointer capture semantics.
  - See target resolution + dispatch in [omega_gen5_v11.html](../../1_projects/omega_gen5_current/omega_gen5_v11.html#L2700-L3070).

This is a strong baseline for multi-app, but it needs explicit routing rules.

### 4) Hex modular monolith scaffolding (tokens/registry/ports) is present

- Port doctrine metadata exists (`window.hfoPortMeta`).
- Tokens/registry exist (`window.hfoTokens`, `window.hfoRegistry`).
- Facades exist (`window.hfoPorts`) and strict mode exists (`flag-p5-defend-strict-v11`).
  - See [omega_gen5_v11.html](../../1_projects/omega_gen5_current/omega_gen5_v11.html#L2328-L4740).

### 5) Minimal stigmergy surface exists (useful for “app switched”, “intent changed”, etc)

- `window.hfoStigmergy.emit/getRecent/subscribe` exists and is inert unless called.
  - See [omega_gen5_v11.html](../../1_projects/omega_gen5_current/omega_gen5_v11.html#L4560-L4626).

## What is missing for true multi-app v12 (the gap list)

### A) App Host (P7-owned) is not implemented

Right now P7 exposes configuration and intent state, but it does **not** expose an app system:

- Present P7 surface: `getMissionVision`, `patchParameters`, `setExcalidrawTool`, `setVisualEngine`, `setIntent`.
  - See adapter + facade at [omega_gen5_v11.html](../../1_projects/omega_gen5_current/omega_gen5_v11.html#L2573-L2688) and [omega_gen5_v11.html](../../1_projects/omega_gen5_current/omega_gen5_v11.html#L4658-L4684).

For v12 you need (at minimum) something like:

- `Ports.p7.apps.list()`
- `Ports.p7.apps.register(manifest)`
- `Ports.p7.apps.activate(appId, opts)`
- `Ports.p7.apps.deactivate(appId)`
- `Ports.p7.apps.getActive()`

And a lifecycle contract:

- `mount(containerEl, services)` / `unmount()`
- optional `onIntent(intent)`

### B) Explicit routing for P3 injection (active app target) is missing

Current behavior:

- P3 injects wherever `elementFromPoint` resolves (with special-casing for Excalidraw overlay).

For multi-app, you need a deterministic rule:

- Inject only into the **active app’s DOM root** (or its iframe’s document) *unless explicitly configured otherwise*.

Practical requirement:

- AppHost must expose `getActiveTargetAt(viewX, viewY)` or `getActiveRoot()`.
- P3 must ask the AppHost (via a token/adapter) for the target resolution policy.

### C) GoldenLayout is present, but “apps as tabs” is not yet a first-class plugin model

The current layout plans create a single `hero` component in the main stack.

- There is no mechanism that maps “tab = appId” to “mount this app into hero container”.

v12 needs:

- a stable “hero tabs” concept (even if still using GoldenLayout stacks), and
- a mapping from tab selection → `Ports.p7.apps.activate(appId)`.

### D) Contracts for cross-app integration are missing

The v10 spec’s direction is “contracts are SSOT, owned by P1”. v11 has strong P1 schemas for DataFabric + envelope, but nothing for apps.

v12 needs Zod contracts for:

- `AppManifest` (id, title, kind, origin, entrypoint, capabilities)
- `IntentManifest` (what P7 means by “intent”, typed)
- `AppCapability` (what services each app can request: pointer injection, telemetry, etc)

Without these, “swap apps safely” will regress into ad-hoc coupling.

### E) Isolation boundaries need an explicit choice (same DOM vs iframes)

You’re already using iframes for Excalidraw (same-origin wrapper).

For v12, pick one:

- **Same-origin iframes** (recommended): stronger isolation, clearer mount/unmount, safer teardown.
- **Same DOM**: fastest, but higher risk of CSS/event collisions.

If you want “other apps” to be drop-in, iframes + a tiny message bridge is usually the cleanest.

## Recommended path to v12 (minimal disruption, aligns with current architecture)

### Step 1: Add a P7 AppHost adapter + facade (no behavior change yet)

- Add token: `p7.apphost` (or `ui.apphost`).
- Register an adapter that holds an in-memory registry and exposes the APIs above.
- Expose it at `window.hfoPorts.p7.apps`.

### Step 2: Teach P3 to target the active app (policy injection)

- Update P3 target discovery to:
  1) ask AppHost for “active iframe/document/root”,
  2) only fall back to `document.elementFromPoint` when AppHost says “global”.

### Step 3: Make GoldenLayout tabs drive activation

- Keep the existing `hero` component as the physical host.
- Add “app tabs” to the hero stack, and when a tab becomes active:
  - mount the selected app iframe into the hero container,
  - set it as the active target for P3.

### Step 4: Add one end-to-end gate for v12

A single Playwright gate that proves the architecture:

- open v12
- switch tab from Excalidraw → App B
- inject a COMMIT pointer sequence
- assert App B receives pointer events and Excalidraw does not

## “How close are we?”

If you define “multi-app v12” as:

- “same substrate” + “swap apps like tabs” + “pointer injection works per app”

Then you’re roughly:

- **~70% there on substrate + injection** (already implemented in v11)
- **~20% there on app orchestration** (P7 has intent/config but no app host)
- **~0% there on contract-enforced app manifests** (not present yet)

The shortest path is **P7 AppHost + P3 target routing + GoldenLayout tab wiring**.
