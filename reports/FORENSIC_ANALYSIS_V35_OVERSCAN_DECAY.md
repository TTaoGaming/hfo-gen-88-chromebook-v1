# Medallion: Bronze | Mutation: 0% | HIVE: V

# Forensic Report: Architectural Decay vs. Functional Stability (Overscan Reversion)

**Date**: 2026-01-16
**Status**: 🔴 RED TRUTH DOCUMENTED
**HFO Port**: P7 (NAVIGATE / Orchestration Audit)

---

## 🎯 Executive Summary

The transition to **OMEGA V35** involved a surgical reversion of the `zoomFactor` from **1.15x** to **1.0x**. While this successfully resolved the critical "Excalidraw Clipping" (where UI toolbars were pushed into the container's hidden overflow), it has introduced **Architectural Decay** in the **Overscan Substrate**.

## 🔍 Forensic Chain of Events

1. **V28 (The Overscan Origin)**: The `zoomFactor: 1.15` was introduced to create a "Bleed" effect. By scaling the camera feed and canvas to 115% of the viewport, landmarks at the edges of the physical camera FOV were pushed off-screen, ensuring the visible area was 100% covered by the virtual substrate (no black bars).
2. **V33 (Interaction Integration)**: The Excalidraw Interaction Layer (Iframe) was bonded to this zoomed substrate. Because Excalidraw is an external application inside an iframe, its toolbars (Help, Tools, Layers) are anchored to the *iframe edges*.
3. **V35 (The Clipping Crisis)**: In maximized state (1280px container), the 1.15x zoom forced the iframe to **1369px**. The Excalidraw toolbars, residing at the absolute edges of the 1369px frame, became inaccessible because the Golden Layout container (1280px) has `overflow: hidden`.
4. **V35 (The Junction Fix)**: I reverted the zoom to **1.0x**. This "fixed" the UI issue by shrinking the iframe back into the container bounds (**1191px**), but at the cost of the architectural vision.

## 📊 Behavioral Impact Audit

| Feature | Overscan (1.15x) | Reversion (1.0x) | Impact |
| :--- | :--- | :--- | :--- |
| **Visible UI** | ❌ Clipped (Toolbars hidden) | ✅ Pure (Full UI visible) | Functional Gain |
| **Gutters** | ✅ Seamless (Cover) | ❌ Letterboxed (Contain) | **Architectural Decay** |
| **Edge Sensing** | ❌ Clipped (Hand disappears) | ✅ Absolute (1:1 Coverage) | Sensing Gain |
| **Corner Reach** | ✅ Full Reach | ❌ Restricted (Bound to Video) | **Interaction Loss** |

## 🛠️ The "Architecture Destruction" Analysis

The user’s concern that the architecture has been "destroyed" is **Valid**.

- **Sensing Integrity**: Hand gestures will **NOT** be clipped relative to the camera FOV; in fact, the entire FOV is now visible. However, gestures *at the camera edges* no longer reach the *panel edges*.
- **Coordinate Drift**: By moving to 1.0x, the virtual interaction space is now smaller than the physical display panel. If the user expects to draw in the "black bars" area, the sensing will fail because those areas are outside the re-projected `viewBounds`.

## 📈 Recommendation (Medallion Evolution)

The current V35 state is a **"Safety Baseline."** To restore the architecture without re-introducing clipping, the system requires a **Decoupled Zoom Engine**:

1. **Video/Babylon**: Maintain 1.15x zoom for immersive "Cover."
2. **Excalidraw Iframe**: Maintain 1.0x width/height but apply internal canvas scaling via `postMessage`.
3. **Alternative**: Use CSS `transform: scale()` on the video/canvas layer while keeping the Iframe container at 1:1, then manually offsetting the projection math.

---

## ✅ Receipt: SUCCESS_V35_HARDENED (Functional) / FAIL_ARCH_OVERSCAN (Design)

The fix was a functional trade-off. The architecture is currently in a **"Degraded Defensive"** state to ensure Kiosk readiness.

*Spider Sovereign (Port 7) | HFO Shards Unit | Red Truth Verified*
