# Medallion: Bronze | Mutation: 0% | HIVE: V

// Medallion: Bronze | Mutation: 0% | HIVE: I

# 🛰️ HFO MISSION OMEGA: FSM ARCHITECTURAL REPORT (V1.2)

**Date**: 2026-01-12
**Status**: 🟠 FORMALIZING
**Mission Thread**: Omega (Total Tool Virtualization)
**Objective**: "Elemental Fire" Symbolic FSM for high-fidelity gestural intent.

---

## 🏛️ Executive Summary

The Omega FSM is evolving from a structural state machine to a **Multisensory Intent Manifold**. We utilize "Elemental Fire" as a symbolic bridge for the user to perceive the internal state of the **Leaky Bucket**.

---

## 📐 Formalized FSM: The Pyre Sentinel

### 1. 🌑 IDLE (Ghostly State)

- **Trigger**: Hand tracked, but `isPalmFacing` is **FALSE**.
- **Visuals**:
  - Cursor: Ghostly, 20% opacity, desaturated.
  - Hand: No elemental effects.
- **Intent**: The system is aware but passive. No accidental "Midas" triggers.

### 2. ⚡ POINTER_READY (Ignition/Dwell)

- **Trigger**: `isPalmFacing` is **TRUE** (Dwell starts filling Leaky Bucket).
- **Visuals**:
  - **Ignition Flow**: Fire spreads procedurally from **Wrist (lm 0)** $\rightarrow$ **Knuckles** $\rightarrow$ **Fingertips**.
  - **Fireball Cursor**: A procedural particle fireball at the index tip ($+Offset$).
  - **Smoothing**: OneEuroFilter provides high-stability coordinate bridging.
- **Geometry**: Cursor offset **-20px** above the index tip (Laser Pointer Gap).
- **Intent**: High-intent dwell. User is "charging" the interaction.

### 3. 🔥 POINTER_COMMIT (The Flare)

- **Trigger**: High-confidence gestural trigger (e.g., `POINTING_UP`) from `READY` state.
- **Visuals**:
  - **Flare**: Intense fire effect, color shift to deep red/white core.
  - **Persistence**: "Sticky" state until hand orientation change or bucket drain.
- **Intent**: Executive commitment. Virtual tool engagement.

---

## 🧪 Visual Engineering: "The Fire spread"

The "Magic" feel is achieved by mapping the `dwellRatio` ($0.0 - 1.0$) to the landmark hierarchy:

- $0.0 - 0.2$: Wrist ignition.
- $0.2 - 0.6$: Metacarpal fire flow.
- $0.6 - 1.0$: Fingertip saturation + Fireball maturity.

---

## 🛰️ Dispatch Receipt

**BFT Quorum**: 72.5% | **Status**: PASS
**Recommendation**: Proceed to V62.0 Implementation.

*Spider Sovereign (Port 7) | Gen 88 Canalization*
