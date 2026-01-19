# Medallion: Bronze | Mutation: 0% | HIVE: V

# Medallion: Bronze | Mutation: 0% | HIVE: I

# ⚔️ Trade Study: V24.12 Aesthetic Refinement (Cyan Plasma)

**Problem Analysis**: The "rectangles" and "artifacting" in the Cyan (COMMIT) fire are likely caused by a combination of high-density overlap (high `emitRate`) and high-opacity centers (`color1` Alpha = 1.0). When particles are smeared along a vector in short batches, these opaque overrides create visible "steps" or blocks rather than a smooth plume.

## 🧱 Analysis of Alternatives (AoA) for Visual Purity

### Option A: Soft Alpha Ramp (Transparency Focus)

* **Mechanism**: Reduce the birth alpha to 0.4 and use a `gradient` to peak at 0.8 before fading to 0.
* **Aesthetic**: Particles will look like "soft glows" that blend into each other, creating a volumetric "steam" effect rather than distinct grains.
* **Mobile Impact**: Neutral. Babylon.js handles transparency gradients efficiently.
* **Pros**: Directly addresses the "rectangles" by eliminating hard opaque edges.

### Option B: Noise-Injected Dithering (Jitter)

* **Mechanism**: Add `Math.random() * jitter` to the `minEmitBox` and `maxEmitBox` coordinates.
* **Aesthetic**: Breaks the "clean lines" of the motion smearing. The fire will look more "chaotic" and "natural," similar to the Amber READY state but faster.
* **Mobile Impact**: Very low. Simple math overhead.
* **Pros**: Hides the "breadcrumb" artifact by mathematically diffusing the emission points.

### Option C: Velocity-Aware Size Modulation

* **Mechanism**: Link `maxSize` and `minSize` to the cursor's velocity. Slow = small/dense; Fast = large/whispy.
* **Aesthetic**: When moving fast, the particles grow larger and more transparent, filling the gaps naturally. When still, they sharpen into a fine needle.
* **Mobile Impact**: Neutral.
* **Pros**: Creates a "dynamic plume" that feels reactive to user movement.

### Option D: Dual-Phase Emission (Hybrid Density)

* **Mechanism**: Reduce the main `emitRate` by 50% but add a persistent, low-poly `Ribbon` mesh or a secondary "Smoke" particle system with very low density.
* **Aesthetic**: Provides a solid visual core (the needle) while the particles provide the "embers."
* **Mobile Impact**: **High Risk**. Managing two systems per hand can hit draw-call limits on older Chromebooks.
* **Pros**: Highest visual fidelity; eliminates the "dots" entirely.

---

## 🛰️ Recommendation

**HFO COMMANDER RECOMMENDATION: OPTION A + B (The "Ghost Fire" Strategy)**
By softening the alpha (Option A) and injecting spatial noise (Option B), we can maintain the high-speed "Needle" feel while making it look like fluid energy.

**PROPOSED TUNING**:
* `color1`: Change Alpha from 1.0 to 0.6.
* `minLifeTime`: Increase from 0.1 to 0.15 (Prevents "popping").
* `minEmitBox`: Add `(Math.random()-0.5) * 0.05` jitter.

*Spider Sovereign (Port 7) | Aesthetic AoA Delivered*
