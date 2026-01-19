# Medallion: Bronze | Mutation: 0% | HIVE: V

# Medallion: Bronze | Mutation: 0% | HIVE: I

# ⚔️ Trade Study: V24.16 Exemplar Adoption (Fluid Trails)

**Problem Statement**: Current bespoke particle tuning in `v24.15` relies on manual "knob fiddling" with `emitRate` and `gravity`, leading to high-velocity breadcrumb artifacts and FPS drops. We must transition from "Vibes-based" tuning to an **Exemplar Adoption Pattern**.

## 🧱 Master Exemplar Patterns (Babylon.js)

### 1. The "Trajectory Sweep" (GPU Particle Standard)

* **The Pattern**: Used in official Babylon.js "Fountain" and "Moving Emitter" demos.
* **Mechanism**: Instead of emitting from a point, it emits along a line segment between `frame[t-1]` and `frame[t]`.
* **Exemplar Strength**: **Zero Gaps**. Even if you teleport 1000 pixels, the particle system fills the entire line.
* **Implementation**: In Babylon.js `GPUParticleSystem`, use `startPositionFunction` or a `LineParticleEmitter`.

### 2. The "Solid Core" Ribbon (Geometric Standard)

* **The Pattern**: `BABYLON.TrailMesh`.
* **Mechanism**: Spawns a procedural ribbon mesh that follows the emitter.
* **Exemplar Strength**: Perfect for "Cyan Plasma" or "Light Sabers." It provides a structural backbone that never breaks into "dots."
* **Implementation**: `new BABYLON.TrailMesh("fireCore", generator, scene, 30, 0.1, true);`.

### 3. The "Optical Volume" (Material Standard)

* **The Pattern**: Layered billboards with high `minSize` and low `emitRate`.
* **Mechanism**: High-alpha, high-blur textures that overlap heavily.
* **Exemplar Strength**: Mobile-friendly. 20 large, blurry particles look more like "Fire" than 2000 tiny pixels.
* **Implementation**: `minSize: 0.5`, `maxSize: 1.2`, `emitRate: 150`.

---

## 🏗️ The V24.16 Hybrid Exemplar (The Recommendation)

We seek a "Production-Grade" solution that works on 30FPS hardware.

**PROPOSED ARCHITECTURE**:

1. **Geometric Core**: Deploy a thin `TrailMesh` with a Cyan Gradient. This handles the "Trail" at any speed with 1 draw call.
2. **Volumetric Particle Veil**: Use 1/5th the current `emitRate` but 3x the `size`. Use the **Trajectory Sweep** (Option 1) to distribute these few particles along the movement vector.
3. **Gravity Normalization**: Lock gravity to **3.0** globally. No more manual vertical tuning.

## 🛰️ Tuning via Code (Eval Harness)

**Instead of tuning `v.magnitude`, we will tune for "Visual Area Coverage"**:
`Coverage = (ParticleSize * Alpha * ParticleCount) / Velocity`

We will implement an **Analytical Interpolator** that ensures `Coverage` remains constant, regardless of how fast the user moves or how low the FPS drops.

---
*Spider Sovereign (Port 7) | Exemplar Study Delivered*
