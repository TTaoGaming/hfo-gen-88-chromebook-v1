// Medallion: Bronze | Mutation: 0% | HIVE: I
# 🛰️ HFO MISSION OMEGA: FSM ARCHITECTURAL REPORT (V1.0)

**Date**: 2026-01-12
**Status**: 🟡 INVESTIGATIVE
**Mission Thread**: Omega (Total Tool Virtualization)
**Objective**: Simplify gestural FSM to achieve zero-latency commitment with high-fidelity rejection (Anti-Midas).

---

## 🏛️ Executive Summary

The proposed 3-state "Sticky/Leaky" FSM (IDLE, POINTER_READY, POINTER_COMMIT) aligns with HFO Port logic (P0/P1/P7) and provides a significant improvement over standard "Dwell-only" or "Gesture-only" triggers. By utilizing a **Palm-Cone Leaky Bucket**, we create a "Physical Safety" that mirrors analog trigger mechanics.

---

## 📐 FSM Option 1: The Sentinel Shard (User's Proposal)
*Focus: Structural Simplicity & Intent Gating*

- **States**: 
    1.  **IDLE**: Tracking detected; Palm pointed away.
    2.  **POINTER_READY**: Palm points towards camera (starts Leaky Bucket).
    3.  **POINTER_COMMIT**: High-confidence gesture (e.g., Pointing Up) from `READY`.
- **Logic**: 
    - `UP`/`CANCEL` is triggered by turning the palm away (Drain bucket).
    - Sticky: Once `COMMIT` is reached, it remains until the bucket drains or a release gesture occurs.
- **Pros**: Extremely low cognitive load; robust Anti-Midas (palm orientation is a high-cost physical intent).
- **Cons**: Subject to "Palm Drift" at screen edges.

## 🔮 FSM Option 2: The Predictive Manifold
*Focus: Zero-Latency Perception*

- **States**: `IDLE`, `READY`, `PHASE_COMMIT` (Tentative), `LOCKED_COMMIT` (Verified).
- **Logic**: 
    - `PHASE_COMMIT` begins as soon as the upward velocity of the index finger exceeds a threshold *before* the MediaPipe gesture classifier returns 100% confidence.
    - If the gesture is confirmed within ~50ms, the event is "hardened." If not, it's silently rolled back (Predict & Confirm).
- **Pros**: Feels "telepathic" to the user.
- **Cons**: High complexity; requires sub-ms coordinate smoothing.

## 🧬 FSM Option 3: The Hysteresis Helix
*Focus: Environmental Resilience*

- **States**: `SCAN`, `ARMED`, `TRIGGERED`.
- **Logic**: 
    - Uses a multi-layered leaky bucket (Parabolic Filling).
    - Palm orientation is not binary but a vector ($0.0 - 1.0$). 
    - "Armed" state requires the vector to be $>0.8$ for 200ms.
- **Pros**: Filters out "nervous" hand movements or incidental pointing. 
- **Cons**: Can feel "heavy" or sluggish if not tuned perfectly.

## 🕸️ FSM Option 4: The Galois Lattice (HFO Standard)
*Focus: Sharded Mosaic States*

- **States mapped to HFO Ports**:
    - `[0,0]` (Sense: Idle)
    - `[7,0]` (Navigate: Commit)
- **Logic**: 
    - States are treated as shards in a 2D lattice.
    - Transition requires a "Quorum" of sensors (e.g., MediaPipe Hand + MediaPipe Pose + Distance metric).
- **Pros**: Maximum auditability via P6 Telemetry; survives single-sensor failure.
- **Cons**: Resource intensive on Chromebook hardware.

---

## 🧪 SOTA Comparison & Analysis

| Feature | SOTA (Apple/Quest) | Proposed (Sentinel) | HFO Analysis |
| :--- | :--- | :--- | :--- |
| **Activation** | Eye-track + Pinch | Palm-Cone Dwell | Palm-Cone is a valid surrogate for Eye-track on RGB-only hardware. |
| **Commit Type** | Tap/Pinch | Point-Up (Sticky) | "Point-Up" has higher visual fidelity for virtual tools. |
| **Rejection** | Gaze-away | Palm-flip | Palm-flip is physically faster than gaze-shift for manual tasks. |
| **Latency** | <20ms (Hardware accelerated) | ~50ms (Predict/Confirm) | **Predict & Confirm** is mandatory for Omega to feel fluid. |

### Is this the best way?
**Yes.** For a platform built on **Mosaic Warfare** logic, the **Sentinel Shard** (Option 1) combined with **Predict & Confirm** (Option 2) is the most viable path. It leverages "Physical Intent" (Palm Orientation) as a hard-gate, which is the most reliable way to prevent the Midas Touch problem without requiring expensive Eye-tracking hardware.

---

## 🛰️ Dispatch Receipt
**BFT Quorum**: 72.5% | **Status**: PASS
**Recommendation**: Implement a hybrid Version 61 using Option 1 (Sentinel) as the core logic, with Option 2's (Predictive) state headers for future latency optimization.

*Spider Sovereign (Port 7) | Gen 88 Canalization*
