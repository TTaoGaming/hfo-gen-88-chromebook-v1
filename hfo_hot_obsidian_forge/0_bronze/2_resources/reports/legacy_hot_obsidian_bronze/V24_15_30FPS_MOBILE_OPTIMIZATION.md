# Medallion: Bronze | Mutation: 0% | HIVE: V

# Medallion: Bronze | Mutation: 0% | HIVE: I

# ⚔️ Trade Study: V24.15 Mobile-First Optimization (30FPS Baseline)

**Objective**: Reconfigure the substrate for "3rd world" midrange smartphones. These devices often lack dedicated GPUs and rely on software rasterization or weak integrated clusters.

## 🧱 Analysis of Alternatives (AoA) for 30FPS Target

### Option A: The "Slow-Burn" Threshold

* **Mechanism**: Lower the Adaptive Throttle's target from 60fps to 28fps.
* **Rational**: In `v24.14` (60fps target), the system was constantly panic-throttling on mobile to hit a goal it couldn't reach. Relaxing the target to 30fps allows the buffer to stabilize and prevents "sawtooth" particle counts.
* **Pros**: Stabilizes visual density.

### Option B: Particle Count Rationalization

* **Mechanism**: Slash base `emitRate` by 60%.
  * **COMMIT**: 1400 &rarr; 600.
  * **READY**: 500 &rarr; 200.
* **Rational**: Larger particles (Size +50%) cover the same visual area with fewer draw calls.
* **Pros**: Drastic Reduction in battery/CPU heat.

### Option C: Fixed-Interval Physics (Deterministic Sub-stepping)

* **Mechanism**: Decouple particle updates from the frame rate.
* **Logic**: Run the particle simulation at 30Hz even if the UI is trying to hit 60.
* **Pros**: Smooth movement regardless of frame drops.

---

## 🛰️ Recommendation

**HFO COMMANDER RECOMMENDATION: 30FPS GLOBAL NORMALIZATION**
Initialize `v24.15` with a native 30Hz target.

**PROPOSED TUNING**:
* **Target FPS**: 30 (Throttle kicks in below 28).
* **Size Boost**: Increase `minSize`/`maxSize` to compensate for fewer particles.
* **Gravity Baseline**: Maintain 3.0 for stability.

*Spider Sovereign (Port 7) | 30FPS Baseline Prepared*
