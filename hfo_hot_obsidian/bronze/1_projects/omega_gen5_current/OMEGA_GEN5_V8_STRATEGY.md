# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen5 V8 Strategic Refactoring

**Medallion:** Bronze | **Mutation Status:** 0% | **Hive:** V
**Timestamp:** 2026-01-20T11:15:00-07:00

---

## 1. V8 Baseline Status

- **Source:** [omega_gen5_v6.html](omega_gen5_v6.html) (Hard clone verified, 193KB).
- **Status:** Pure baseline restored. All Port 7 performance governor hacks and v7 framing drift have been purged.
- **Goal:** Prepare for "Hardened Silver" integration by decoupling behavioral hacks from the W3C pointer core.

## 2. Refactoring Steps Forward (Phase VI Transition)

### A. Port 3: Injector Standardisation

- **Current Issue:** Injector uses synthetic `PointerEvent` objects combined with a manual `MouseEvent('click')` hack for Excalidraw UI.
- **Refactor:** Create an `AbstractPointerAdapter` class.
  - Implement `StandardW3CAdapter`: Pure pointer-only (capture, focus, move).
  - Implement `LegacyTouchAdapter`: Includes the click-synthesis-on-up logic.
- **Outcome:** Decouples the "workaround" from the core injection pipeline.

### B. Thermal Governance (Opt-in Policy)

- **Current Issue:** V7 used brute-force FPS capping in the main loop.
- **Refactor:** Implement a "Degradation Stack" managed by Port 5 (Defend):
  1. **Tier 1 (Visuals):** Disable high-fidelity hand masks and palm-cone shaders.
  2. **Tier 2 (Sensing):** Decimate video input resolution (720p -> 480p) while maintaining high-frequency landmarks.
  3. **Tier 3 (Logic):** Only cap FPS as a last resort when thermal pressure violates the `HFO_THERMAL_SAFE` contract.
- **Integration:** This must be an *explicit* user choice or automated via `requestIdleCallback` to avoid breaking the predictability of tracking.

### C. Trusted Input Bridge

- **Current Issue:** Synthetic events are untrusted and can be blocked by certain browser security contexts or complex wrappers.
- **Refactor:** Prepare for Port 1 (Bridge) stabilization using Playwright-style trusted injection or an OS-level HID bridge if available.
- **Outcome:** Moves from "DOM Theater" to "OS Reality."

### D. Excalidraw Wrapper Hardening

- **Refactor:** Update [excalidraw_v20_wrapper.html](excalidraw_v20_wrapper.html) to expose a direct `hitTest` and `selectTool` API to the parent.
- **Outcome:** Allows Port 7 (Navigate) to set tools via direct API without needing a "fake click" to trigger the UI buttons.

## 3. Next Grounded Step

1. **Sanity Check:** Run `npm run test:omega:fast` against `omega_gen5_v8.html`.
2. **Implement Step A/D:** Standardize the Excalidraw interface to remove the click hack.

---
*Spider Sovereign (Port 7) | Gen 88 Guidance*
