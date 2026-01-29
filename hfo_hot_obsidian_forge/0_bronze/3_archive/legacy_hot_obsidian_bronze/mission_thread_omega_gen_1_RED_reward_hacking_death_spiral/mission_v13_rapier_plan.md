# Medallion: Bronze | Mutation: 0% | HIVE: LEGACY
# 🧶 Mission Thread Omega: Physics Cursor V13 (Rapier Integration)

**Medallion**: Hot Bronze | **Status**: 🛠️ Planning | **Date**: 2026-01-09

## 🎯 Objective
Integrate **Rapier WASM** (Physics Engine) to expand the cursor ensemble from 2 to **4 high-fidelity cursors**. This will bridge the gap between sensing (P0) and physical impact (P2).

## 📍 Cursor Ensemble (The Quadratic Cursors)
1.  **Cursor Alpha (Smooth)**: 1€ Filter (MinCutoff: 0.5, Beta: 0.001). [STABLE]
2.  **Cursor Beta (Snappy)**: 1€ Filter (MinCutoff: 2.0, Beta: 0.1). [STABLE]
3.  **Cursor Gamma (Spring)**: Rapier Spring-Mass-Dampener. Physics-based elasticity for "fluid" feel. [PENDING]
4.  **Cursor Delta (Predictive)**: Rapier-backed predictive cursor using velocity extrapolation to minimize visual lag. [PENDING]

## 🏗️ Implementation Roadmap (Step-by-Step)

### Step 1: Rapier WASM Injection
- Add `@dimforge/rapier2d` to `importmap`.
- Initialize `Rapier.init()`.
- Set up a `World` with zero gravity (for top-down cursor interaction).

### Step 2: Physics Bridge (Port 2 SHAPE)
- Create a `PhysicsCursor` class to manage Rapier rigid bodies.
- Map MediaPipe landmarks (0.0 - 1.0) to Rapier screen-space coordinates.

### Step 3: The Spring Mass System
- Implement a RigidBody (Cursor) connected to a Target (Hand Landmark) via a `SpringJoint`.
- Tune damping (D) and stiffness (K) parameters in real-time via P7 Navigate (lil-gui).

### Step 4: The Predictive Core
- Calculate velocity vectors from sensor data.
- Apply `RigidBody.setNextKinematicTranslation` with a temporal offset to "lead" the movement.

## 🛡️ Governance & Safety
- **Anti-Hallucination**: No custom physics math; use Rapier native methods (joints, forces).
- **Medallion Path**: Validating each step with Playwright before moving to next.
- **Reference**: See `hfo_cold_obsidian/bronze/2_areas/architecture/physics_cursor.md` for grounding.

---
*Spider Sovereign (Port 7) | Mission Control | Thread Omega V13*
