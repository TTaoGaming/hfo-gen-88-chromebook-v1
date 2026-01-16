# 🐉 OMEGA GEN 4: CONSOLIDATED ROADMAP & ARCHITECTURE (V26+)

**Medallion**: Bronze | **Status**: Phoenix Rebirth | **HIVE**: E (Evolve)
**Date**: 2026-01-15

---

## 🏗️ CORE ARCHITECTURE: HYPER-FRACTAL OBSIDIAN (HFO)

All work adheres to the **Hexagonal Ports and Adapters** pattern, ensuring components are swappable and testable.

### 📍 Port Mappings (JADC2 Alignment)

- **P0 SENSE (ISR)**: MediaPipe / Camera / Landmark Sensing.
- **P1 FUSE (Data Fabric)**: Coordinate fusion, Mirror-Awareness, Zod Contract Validation.
- **P2 SHAPE (Digital Twin)**: Physics Manifold (Planck.js / Matter.js / Rapier).
- **P3 DELIVER (Effect Delivery)**: W3C Pointer Event Injection (Hydra-Pulse-Adapter).
- **P4 DISRUPT (Feedback Loops)**: Chaos testing, Stress events (NSE), Suppression.
- **P5 DEFEND (Integrity)**: Zero-Trust, Medallion Provenance, Forensic Audits.
- **P6 STORE (Telemetry)**: DuckDB-WASM, JSONL Blackboards, Replay.
- **P7 NAVIGATE (BMC2)**: Orchestration, UI Navigator (Golden Layout), System State.

---

## 🎯 STRATEGIC PRIORITIES (V25/V26 HARDENING)

### 1. Offline & Dependency Resilience (CRITICAL)

- **Goal**: Zero external network requests during runtime.
- **Action**: Localize all CDN assets (GoldenLayout, Babylon.js, OpenFeature, MediaPipe WASM/Models) into the `lib/` directory.
- **Verification**: Must pass `P5 Forensic Audit` in Airplane Mode.

### 2. Readiness Charger (The Leaky Bucket)

- **Goal**: Move from magic dwell timers to a deterministic "Readiness Score" (0-100%).
- **Implementation**:
  - **Fill Rate**: Adjustable charge speed when "Armed" (Index Up).
  - **Drain Rate**: Adjustable decay speed on tracking loss or disengagement.
  - **Visual**: "Gaze-and-Dwell" style charging bar with ticks and color shifts (Grey → Amber → Cyan).

### 3. Spatial Ergonomics & Rectification

- **Goal**: Ensure 1:1 mapping between hand and virtual target on Chromebook V-1.
- **Action**:
  - **Screen Buffer**: User-adjustable `screenBufferPx` (e.g., 50px) bezel-safe zone.
  - **Camera Offset**: Calibrate `object-fit: contain` video box to match overlay layers.
  - **Direct Projection**: Use MCP (Knuckle) as ray origin for superior stability.

### 4. Interactive Parent Discovery (Hydra-Pulse)

- **Goal**: Reliable click injection into complex DOM (Excalidraw/React).
- **Action**: Use `findInteractiveParent` heuristics + 10ms "Pulse" delay to allow state settling before execution.

---

## 🛡️ ANTI-APP-KILLER DEFENSES

- **Midas Touch Defense**: Single dominant intent gate (Palm-Facing + Leaky Bucket).
- **Pointer Semantics**: Absolute compliance with `pointercancel` as the primary abort path.
- **Drift Prevention**: Strict enforcement of Port 1 as the **Single Source of Truth (SSOT)** for coordinates.
- **Cognitive Load Defense**: "Essentials vs Developer" toggle in Port 7 Navigator.

---

## 📅 PHASED EXECUTION ROADMAP

### PHASE ALPHA: INFRASTRUCTURE (IN-PROGRESS)

- [x] Resolve Chronos Fractures (Blackboard repair).
- [x] Consolidate 8-Port Architecture in V26.
- [x] Implement Lifecycle Management (Anti-Zombie engines).

### PHASE BETA: HARDENING (IMMEDIATE)

- [ ] Localize all CDN dependencies.
- [ ] Implement user-tunable Fill/Drain rates for Leaky Bucket.
- [ ] Verify 50px Screen Buffer reachability.
- [ ] Create 30s Interactive Onboarding Tutorial.

### PHASE GOLD: PRODUCTION (FUTURE)

- [ ] Achieve 88% Mutation Score (Silver Layer promotion).
- [ ] Nightly Stress Event (NSE) verification.
- [ ] Multi-Hand "Hot Seat" mutual exclusion.

---
*Spider Sovereign (Port 7) | HFO Gen 88 Coordination*
