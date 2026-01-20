# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen 5 v8: Medallion Bronze Evolution

**Medallion Layer**: Bronze | **Mutation Score**: 0% | **HIVE**: V

## 🎯 Mission Objective

Resolve the W3C Pointer/API corruption affecting Excalidraw integration. Clone the architectural stability of v6 while pivoting to a non-hacky injection method. Implement opt-in performance throttling to maintain high FPS during complex pointer sequences.

## 🛠️ The Problem: W3C Pointer Corruption

The current `flag-p3-legacy-click` is a manual click hack that bypasses the DataFabric event loop. This causes drift in Excalidraw when the iframe fails to interpret the HFO synthetic pointer stream as "trusted" events.

## 🚀 Throttling Strategy (Opt-in)

Performance should be managed through graceful degradation rather than hard caps.
**Recommended Order of Degradation:**

1. **Visuals**: Disable CSS filters, shadows, and high-frequency UI updates in the HFO overlay (Expected gain: 15-20% FPS).
2. **Video Stream**: Scale input from 720p down to 480p (Expected gain: 30% reduction in P0 Sense latency).

## 🗺️ 4 Options Forward

### 1. Synthetic Pointer Bridge (Clean Injection)

Construct a dedicated `PointerBridge` service in Port 3 (Deliver). This service will generate standard W3C `PointerEvent` objects (pointerdown, pointermove, pointerup) with the `isTrusted` simulation flag optimized for cross-origin iframes.

- **Pros**: Cleanest architecture; no manual clicks.
- **Cons**: Might still hit browser "trusted event" security barriers.

### 2. Direct Excalidraw Scene API

Bypass the DOM event layer entirely. Use the Excalidraw `updateScene` and `exportToCanvas` APIs to sync HFO DataFabric coordinates directly to the drawing engine.

- **Pros**: 100% accuracy; avoids pointer corruption entirely.
- **Cons**: Requires tighter coupling with Excalidraw internals.

### 3. Coordinate Transformer Shim

Implement a high-frequency coordinate transform layer that offsets the "corruption" by re-calculating the viewport bounds of the Excalidraw iframe relative to the HFO root every 16ms (60fps).

- **Pros**: Preserves v6 logic with a simple correction factor.
- **Cons**: Still relies on underlying event delivery.

### 4. P3 Native Event Hook (Shadow DOM)

Move the Excalidraw container into a Shadow DOM with a dedicated event listener that "re-emits" all P3 events as local pointer events, bypassing the global document's corrupted API state.

- **Pros**: Isolates the "corruption" to the global scope.
- **Cons**: Complexity in managing Shadow DOM styling.

## 🧬 Clone v6 & Proceed (Execution Plan)

1. **Clone v6 Core**: Branch `omega_gen4_v6_base` into `omega_gen5_v8`.
2. **Implement Opt-in Throttling**: Add `enable-throttle-visuals` and `enable-throttle-video-480p` flags to `hfoState.parameters`.
3. **Injector Upgrade**: Replace the manual click in `scripts/omega_gen5_injector_harness.spec.ts` with the chosen Option (Recommended: Option 1 or 2).
4. **Verification**: Run `omega_gen5_excalidraw_compat.spec.ts` without legacy click flags.

---
*Spider Sovereign (Port 7) | Gen 88 Guidance*
