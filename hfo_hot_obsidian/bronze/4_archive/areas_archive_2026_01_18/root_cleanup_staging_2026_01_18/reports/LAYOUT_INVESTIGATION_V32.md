# Medallion: Bronze | Mutation: 0% | HIVE: V

# 📊 OMEGA V32: GOLDEN LAYOUT & CSS INVESTIGATION REPORT

**Date**: 2026-01-16
**Subject**: Layout Regressions and UI Inaccessibility in Golden Layout Substrate
**Status**: 🔴 RED (Critical Layout Friction Detected)

## 🔍 Executive Summary

The transition to **Omega Gen 4** has introduced several layout-breaking behaviors when utilizing the **Golden Layout (v2.6.0)** substrate on Chromebook hardware. The most critical issue occurs during the **Maximize (Fullscreen)** action on the Hero Component, which causes visual desynchronization and renders several UI elements (including Golden Layout controls) inaccessible.

---

## 🏗️ Technical Root Cause Analysis

### 1. The Fullscreen "Ghost" Offset

Golden Layout v2 manages components by dynamically resizing and re-re-parenting elements within its stack. Our `resizeCanvas()` logic (Line 3027) relies on `parentElement.getBoundingClientRect()` to calculate the **Unified Parity Box (UPE)**.

- **The Breach**: During a maximize animation, the `pRect` dimensions return transient or zeroed values, causing the `offsetX` and `offsetY` calculations to drift.
- **Result**: The video and Babylon.js substrates "jump" several hundred pixels or disappear entirely from the viewport when the component is maximized.

### 2. Z-Index Stacking Warfare

There is a collision in the high-priority z-index layer:

- **Status Bar**: `z-index: 1000` (CSS Line 65)
- **Calibration Overlay**: `z-index: 1000` (JS Line 3097)
- **Tutorial Overlay**: `z-index: 100` (CSS Line 211)
- **Overlay Canvas**: `z-index: 15` (CSS) vs `z-index: 11` (Inline JS)

When the Hero component is maximized, it enters a new stacking context. If the Status Bar is global (outside the layout container), it remains visible but may overlap with maximized component headers, blocking access to the "Restore" buttons.

### 3. Pointer-Event Deadzones

The **Excalidraw Overlay** (`#excalidraw-hero-overlay`) and **Babylon Juice Overlay** currently occupy 100% width/height of the Hero Viewport.

- **The Breach**: The Excalidraw iframe (Line 3156) does **not** have `pointer-events: none` enforced on its container when active.
- **Result**: It acts as a transparent "glass wall," blocking all user inputs (including clicks on underlying Golden Layout tab headers or resize splitters) once the IGNITE OMEGA sequence is initialized.

---

## 🏮 Remediation Roadmap (V32.1)

1. **Enforce Pointer-Event Pass-through**:
    - Gating the Excalidraw overlay behind a refined `pointer-events: none` toggle that only captures events during active `COMMIT` states.
2. **Harmonize Stacking Contexts**:
    - Reducing the Status Bar to `z-index: 2000` and lowering experimental overlays to the `10-50` range.
3. **Harden Layout Resize**:
    - Implementing a `ResizeObserver` on the `HeroView` container instead of relying on the global `window.resize` event, ensuring parity updates happen exactly when Golden Layout finishes its internal layout shifts.
4. **Golden Layout "Header Guard"**:
    - Adding top-padding to the `hero-view-container` to prevent absolute overlays from bleeding into the GL tab header area.

---
*Spider Sovereign (Port 7) | Layout Audit Complete | V32 Investigation Finalized*
