# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen 5 v9: Rendering Pipeline & Sub-Optimality Report

**Status**: Forensic Audit | **Timestamp**: 2026-01-20 | **HIVE**: V

## 📋 Rendering Pipeline Overview

The Omega Gen 5 v9 pipeline is a multi-substrate rendering engine that handles high-frequency hand tracking and pointer synthesis. It consists of three primary layers:

1. **P0 SENSE (MediaPipe/DOM)**: The raw video feed and input buffer.
2. **Visual Substrate (Babylon.js)**: 3D particle systems (Phoenix Core), skeletons, and trail meshes.
3. **UI Overlay (2D Canvas/Golden Layout)**: 2D cursors, tactile grids, and diagnostic overlays.

---

## ⚠️ Sub-Optimality Breakdown

Based on a forensic review of `omega_gen5_v9.html`, the following areas exhibit sub-optimal performance characteristics:

### 1. Unified Draw Loop Overload (P1/P0 Coupling)

The `predictLoop` (the main render loop) performs significant per-frame processing before even reaching the renderers.

- **Sub-Optimality**: The loop combines MediaPipe inference (`recognizeForVideo`), P1 Bridging (coordinate fusion), Zod schema validation, telemetry recording, and multiple render calls (`drawResults`, `updateVisualPanels`, `layer.update`) in a single synchronous block.
- **Impact**: Any stall in sensing or contract validation immediately drops the frame rate for UI interactions.

### 2. Port 2 (SHAPE) Authority Violation (Logic Fragmentation)

Rendering and Geometry are mandated to live under **Port 2 (SHAPE)** authority. Currently, this authority is fragmented across the `omega_gen5_v9.html` monolithic script block:

- **Fragmentation**: `BabylonJuiceSubstrate` (3D) is defined as an inline class, while `drawResults` (2D) is a global function in the same scope.
- **Authority Leak**: `P1_FUSE` logic (Bridging) and `P3_DELIVER` logic (Pointer Injection) are both interleaved with render-loop calls, making it impossible to swap or isolate the rendering substrate without breaking the entire sensing chain.
- **Missing Module**: There is no dedicated `p2_renderer.js`. Port 2 is currently an "implicit" port rather than a hardened interface.

### 3. Redundant Mirroring & Projection (UPE Friction)

- **Sub-Optimality**: While v9 implements the Universal Projection Engine (UPE), many components still manually calculate projections or re-validate mirroring logic every frame inside `drawResults` and `BabylonJuiceSubstrate.update`.
- **Inefficiency**: Landmarks are mapped to "buffer space" using `toBufferX/Y` inside the render loop, which involves repeated math operations on 21 landmarks per hand, even when the hand is relatively static.

### 3. GPU Overdraw in "Phoenix Core"

The Babylon.js implementation (`BabylonJuiceSubstrate`) uses high-density particle emitters.

- **Sub-Optimality**: The `tuneFireSystem` logic scales `emitRate` based on motion velocity and a `perfMultiplier`. However, it can emit up to **2000 particles per hand** with `BLENDMODE_ONEONE`.
- **Impact**: High GPU fill-rate consumption on integrated graphics (e.g., Chromebooks), especially when multiple hands are active or during "COMMIT" states where particle intensity is maximized.

### 4. DOM & CSS Filter Bottlenecks

- **Sub-Optimality**: The `<video>` feed uses `filter: grayscale(0.5) contrast(1.1);` and the tutorial overlay uses `backdrop-filter: blur(10px);`.
- **Impact**: CSS filters on large elements (like a full-screen video feed) are notoriously expensive as they trigger full layout repaints and GPU composite cycles on every frame.

### 5. Excessive Telemetry Recording

- **Sub-Optimality**: `window.hfoTelemetry.record('P1_FUSE', systemState.dataFabric)` is called every frame (~60Hz).
- **Impact**: While necessary for "Golden Master" replay, serializing the entire `dataFabric` (including all cursors and metadata) to a storage buffer every 16ms creates significant main-thread pressure and GC (Garbage Collection) churn.

---

## 🏛️ Port 2 (SHAPE) Consolidation Plan

To resolve the "dispersed rendering" violation, the following architectural migration is required:

### 1. Babylon.js Modularization (Completed)

The Babylon rendering logic has been extracted into a standalone Port 2 module:

- **Module**: [lib/js/hfo_p2_babylon.js](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/lib/js/hfo_p2_babylon.js)
- **Authority**: Encapsulates `BabylonJuiceSubstrate`, `HAND_CONNECTIONS`, and particle tuning logic.
- **Action**: `omega_gen5_v9.html` must be updated to import this module instead of defining the class inline.

### 2. 2D Canvas Modularization (Pending)

The `drawResults` function and specialized cursor drawers (`drawFireCursor`, `drawWaterCursor`) currently leak P1/P2 boundaries by accessing internal FSM states directly within the draw loop.

- **Proposed Module**: `hfo_p2_canvas_2d.js`
- **Focus**: Pure geometric rendering of 2D substrates based on the `dataFabric` contract.

### 3. Substrate Orchestration

Port 2 should expose a unified `P2_Manager` that handles the visibility and lifecycle of both 2D and 3D substrates, preventing the "Visual Substrate Gating" hacks currently littering the `predictLoop`.

---

## 🛠️ Optimization Mandate (V10 Roadmap)

1. **Decouple Sensing from Rendering**: Move MediaPipe inference to a Web Worker to prevent UI blocking.
2. **Static Layer Caching**: The "Tactical Grid" in `drawResults` should be drawn to a secondary static canvas once, rather than cleared and redrawn every frame.
3. **Visual "Tiering" (Opt-in)**: Implement the **Thermal Throttling Mode** to automatically disable Backdrop Blurs, Particle Emitters, and Skeleton Wireframes when frame time exceeds 24ms.
4. **Delta Telemetry**: Only record `P1_FUSE` events when cursors move beyond a threshold or state changes, rather than every clock tick.

---
*Generated by GitHub Copilot | HFO Forensic Division*
