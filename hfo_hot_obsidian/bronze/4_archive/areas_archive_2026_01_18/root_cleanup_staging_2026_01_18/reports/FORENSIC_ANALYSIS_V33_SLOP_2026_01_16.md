# Medallion: Bronze | Mutation: 0% | HIVE: V

# 🕵️ Forensic Analysis: V33 Slop & Logic Regressions

**Status**: 🔴 **RED ALERT** (Infrastructure Pollution Detected)
**Date**: 2026-01-16
**Baseline**: OMEGA V31.3
**Subject**: OMEGA V33 (Responsive Hardening + Readiness Evolution)

---

## 🔍 Executive Summary

The transition from V32 to V33 introduced critical architectural pollution. While the structural layout fixes (Option 1 & 4) successfully resolved the Golden Layout sync crisis, the secondary goal of "Sensing Evolution" was implemented by overloading existing tutorial systems, leading to semantic "slop."

## 🧩 Identified Slop (Weak Logic)

1.  **Tutorial Overloading**: The `TutorialSystem` class was hijacked to display the FSM `readinessScore`. This conflates instructional guidance with real-time HUD telemetry, causing "random" tutorial behavior and UI flickering.
2.  **Bidirectional Logic Regression**: The removal of `isPalmVisible` and `isBackVisible` gates in Favor of a pure readiness score has reduced the system's ability to recognize intentional "Exit" gestures (hand-flips).
3.  **Hysteresis Pollution**: The `hysteresisHigh` was increased to 88% without proper calibration, potentially making the system feel sluggish on Chromebook hardware.
4.  **Tutorial Text Mutation**: Manual editing of "Phase 1" text to include "Back of Hand" dilutes the "Specific 3 emoji gesture language" (🖐️/☝️/🖐️) established in V31.x.

## 🏗️ Structural Gains (Strong Logic)

1.  **Responsive UPE**: `toViewportX/Y` now correctly uses `containerRect` (cached) to anchor coordinates to the panel, not the window. **KEEP**.
2.  **ResizeObserver**: Correctly implemented on the hero component to ensure one-way sync during maximization. **KEEP**.
3.  **Interaction Hardening**: `clampedX/Y` for physical probes (`elementFromPoint`) prevents browser-level errors during overscan. **KEEP**.
4.  **GL Min-Bounds**: Enforced 400x300 minimums on the hero panel prevents the "Invisibility" bug on collapse. **KEEP**.

## 📉 Reversion Recommendations

| Feature | Status | Action |
| :--- | :--- | :--- |
| Tutorial Readiness Bar | **SLOP** | **REVERT**. Move readiness visual to a dedicated HUD layer or cursor ring. |
| Omni-Palm Logic | **WEAK** | **REWORK**. Restore `isPalmVisible`/`isBackVisible` checks but integrate with `Math.abs(nz)` for angle-only gating. |
| Tutorial Progression | **BUGGY** | **REVERT**. Restore strictly sequential completion triggers. |
| Coordinate Clamping | **STRONG** | **REMAIN**. Necessary for interaction stability. |

---
*Spider Sovereign (Port 7) | Forensic Analysis Complete*
