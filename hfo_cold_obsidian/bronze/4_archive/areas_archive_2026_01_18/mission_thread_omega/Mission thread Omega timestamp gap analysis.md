# Mission Thread Omega: V20 vs V21 Gap Analysis

## Executive Summary
This document analyzes the transition from HFO Omega **Port 1 Bridge V20** to **Port 3 Deliver V21 (Robot3 FSM)**. While V21 introduces critical functional state management (FSM) and dwell logic, it inherits several architectural "debts" from V20 regarding provenance, contract strictness, and telemetry discipline.

---

## 🔍 Validation of V20 Analysis

The following points from the V20 analysis remain primarily **TRUE** in V21:

1.  **Standard Envelopes (CloudEvents):** **TRUE**. V21 continues to use a CloudEvents-like envelope with `specversion`, `type`, `source`, `id`, `time`, and `data`.
2.  **OneEuroFilter usage:** **TRUE**. Implementation remains correct for jitter/lag management.
3.  **MediaPipe Monotonicity:** **TRUE**. `performance.now()` is used, but capture vs. emit timestamps are still not separated in the `data` payload.
4.  **Matter.js Lifecycle Risk:** **TRUE**. Hand removal still uses `Matter.World.remove` on an array of bodies/constraints, which may lead to leaks compared to `Composite.remove` patterns.
5.  **Provenance Contradiction:** **STILL TRUE**. The `source` is still set to `"hfo.port.0.sense"`, even though the `data` contains P1 (Bridge) validated objects and P2 (Shape) cursor outputs.
6.  **Contract Strictness:** **STILL TRUE**. Zod validates structure but ignores invariants like NaN/Infinity rejection, coordinate frame declaration (`norm01` vs `px`), and boundary enforcement.
7.  **Pointer ABI Gap:** **STILL TRUE**. There is no emission of W3C `pointerdown`/`pointermove`/`pointerup` events yet.

---

## 🚀 V21 Progress & New Gaps

### What V21 Improved
-   **Robot3 FSM Integration:** Added formal state machines (`IDLE`, `PENDING`, `ARMING`, `COMMITTING`) per hand. This is a credible **Port 3 (Deliver)** seed.
-   **Dwell Logic:** Implemented `dwellMs` for "arming" transitions (sticky Open Palm).
-   **Namespace Isolation:** Renamed global `state` to `hfoState` to avoid collisions with Robot3 imports.
-   **Hand Persistence:** Improved greedy matching and coasting logic (though still nearest-neighbor).

### New/Persistent Gaps in V21
-   **Logic Coupling:** FSM event dispatch and dwell checks are buried inside the `render` loop (P0 logic), rather than being decoupled into a clean P3 handler.
-   **Stale Metadata:** The event `type` in `port1Bridge` is still hardcoded to `"hfo.omega.v20.hand_update"`.
-   **No Replay Evidence:** Still lacking `frame_id`, `drop_count`, and the `t_capture_ms`/`t_emit_ms` distinction required for high-fidelity replay.
-   **Performance Bottleneck:** Per-frame `SafeParse` and deep copying of the hand state object during the `port1Bridge` call remains a potential GC/Jitter risk.

---

## 🛠️ Recommendations for V22
1.  **Update Provenance:** Set `source: "hfo.port.1.bridge"` or `"hfo.omega.pipeline"`.
2.  **Harden Zod Contracts:** Add `.finite()` and `.min(0).max(1)` to coordinate fields.
3.  **Refactor Matter Removal:** Switch to `Composite.remove(engine.world, [...])`.
4.  **Decouple FSM:** Move FSM logic out of the MediaPipe render loop and into a dedicated P3/P4 middleware.
5.  **Telemetry Stamp:** Include `frame_id` and the dual-timestamp (`capture` vs `emit`) discipline.

---
*Spider Sovereign (Port 7) | HFO-Hive8 | 2026-01-10*
