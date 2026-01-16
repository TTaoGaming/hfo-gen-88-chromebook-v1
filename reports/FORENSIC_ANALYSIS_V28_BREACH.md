# 🔍 Forensic Analysis: V28.0 Coordinate Parity Breach

**Medallion**: Hot Bronze | **Status**: 🔴 RED ALARM
**Date**: 2026-01-15

## 📝 Summary of Incident

During the promotion of **Version 28.0 (Overscan Guardian)**, the visual synchronization between the hand skeleton (Sensing Layer) and the Phoenix Core pointer (Interaction Layer) was severed. Despite correct landmark data in the shared fabric, the rendering substrates diverged spatially.

## 💀 Root Cause: The "Triple Axis" Mismatch

The failure occurred because the agent attempted to harmonize three incompatible coordinate systems within a single projection loop:

1. **Buffer Space (Internal Resolution)**:
    - `canvas.width = 1280px`
    - **Logic**: Used by MediaPipe `DrawingUtils` to render the skeleton. It assumes a fixed resolution coordinate system.
2. **Layout Space (CSS Pixels)**:
    - `drawW = drawW_base * zoom` (e.g., 1472px)
    - **Logic**: Used by the agent to calculate `screenX` to match the "zoomed" appearance.
3. **Parent Space (Container)**:
    - `offsetX = (parentWidth - drawW) / 2` (Negative offset)
    - **Logic**: Used to shift the visual substrate to center the crop.

### How I Broke It

In `omega_gen4_v28.html`, I implemented the following projection math:

```javascript
const screenX = (finalProjX * drawW) + offsetX;
```

By multiplying the normalized coordinate (`finalProjX`) by the **CSS width** (`drawW`) and adding the **CSS offset** (`offsetX`), I calculated a coordinate relative to the **visible container**.

However, the `overlay-canvas` on which I am drawing this pointer has:

1. **A scale mismatch**: The internal buffer is 1280px, but I'm telling it to draw at a coordinate based on ~1472px (the zoomed CSS width).
2. **An origin mismatch**: The `overlay-canvas` itself is shifted by `offsetX`. By adding `offsetX` to the `screenX` value *inside* a canvas that is already shifted by `offsetX`, I effectively applied the offset twice (or misaligned the target coordinate relative to the canvas origin).

## 💩 Visual Manifestation

- **Skeleton**: Stays pinned to the "Sensing Reality." It correctly renders at `finalProjX * 1280` because `DrawingUtils` ignores my `systemState.ui.viewBounds` and uses the raw canvas resolution.
- **Phoenix Pointer**: Drifts toward the edges or center with an accelerated velocity because its "Pixels" are wider than the underlying sensor "Pixels" (1472 vs 1280) and its origin is offset into the container's margin.

## 🏁 The Breach Fact

The "Shared Data Fabric" correctly holds the normalized landmarks (0.0 to 1.0). The fabric itself is **PURE**. The **INTERPRETATION** of that fabric in `Bridger.bridge()` was corrupted by injecting CSS Layout logic into the Rendering logic.

**Conclusion**: I broke the parity by confusing the **Physical Screen** with the **Virtual Sensing Buffer**.

---
*Spider Sovereign (Port 7) | Forensic Audit Complete | NO EDITS APPLIED*
