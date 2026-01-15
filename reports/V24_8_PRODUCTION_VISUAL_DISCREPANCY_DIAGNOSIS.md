# Medallion: Bronze | Mutation: 0% | HIVE: V

# 🛡️ HFO FORENSIC AUDIT: V24.8 Production Visual Discrepancy

**Target**: `omega_gen4_v24_8.html`  
**Reference**: `v24_8_fire_lab_v3.html`  
**Incident**: "Not Scion-Like" (Cyan Plasma Failure in Production)

## 🔍 Executive Summary

A structural diagnosis reveals that the **Production Monolith** is suffering from **Substrate Ghosting**. While the `BabylonJuiceSubstrate` was updated to the V24.8 Cyan Plasma spec, the legacy **Canvas-based** and **PIXI-based** substrates are still active and hardcoded to the old **Red/Orange** FIRE (LI) theme. These substrates are painting over the Babylon layer, resulting in a "muddied" visual that fails to match the clean Cyan Needle of Lab V3.

---

## 🏗️ Root Cause Analysis (Technical)

### 1. Legacy Path Conflict (The "Ghost" in the Machine)

In the production app, the `predictLoop` calls `drawResults` every frame. Inside `drawResults`, the system executes `drawFireCursor` if the theme is `LI`:

```javascript
// Line 2389 (approx) in Production
if (theme === 'LI') {
    drawFireCursor(ctx, rawX, rawY, screenX, screenY, fsmState);
}
```

This function is hardcoded with **Red/Orange** values:

* `COMMIT`: `rgba(255, 69, 0, 0.8)` (Orange-Red)
* `READY`: `rgba(255, 195, 0, 0.5)` (Amber)

This Canvas overlay is additive and occurs on the main video canvas, effectively drowning out the subtle Cyan particle jet underneath.

### 2. PIXI Substrate Divergence

The `JuiceSubstrate` (PIXI engine) also retains legacy hardcodings:

```javascript
// Line 725 (approx) in Production
this.texRed = createGlowTexture(128, 0xFF4500); // HARDCODED RED
```

If the user's `visuals.engine` parameter is set to `PIXI` (or if it's defaulting there), they will never see Cyan.

### 3. Z-Index and Transparency Conflict

The `BabylonJuiceSubstrate` canvas is likely layered *behind* or *under* the PIXI/Canvas overlays. Because the video canvas (`systemState.p0.canvas`) is cleared every frame (`ctx.clearRect`), any `drawFireCursor` calls will be vibrant, opaque, and dominant over the Babylon particle systems which are rendered in a separate DOM element or layer.

### 4. Coordinate Calibration Error

* **Lab V3**: Uses `BABYLON.Vector3.Unproject` with `clientX/Y` for direct per-pixel mapping.
* **Production**: Uses `normalized coordinates (c.normX, c.normY)` scaled by `width/height`. While technically equivalent, any jitter in the P1 Bridge (OneEuro filters) is magnified differently between the two implementations.

---

## 📊 Discrepancy Matrix

| Feature | Fire Lab V3 (Reference) | Production v24.8 (Current) | Status |
| :--- | :--- | :--- | :--- |
| **Color (COMMIT)** | Cyan Plasma (`#00CCFF`) | Red-Orange (`#FF4500`) | ❌ **FAIL** (Legacy Overlap) |
| **Color (READY)** | Amber (`#FF991A`) | Amber (`#FFC300`) | ⚠️ **Divergent** |
| **Jet Shape** | Needle (Propulsion) | Sphere (Orb) | ❌ **FAIL** |
| **Substrates** | 1 (Babylon only) | 3 (Canvas, PIXI, Babylon) | ❌ **Conflict** |

---

## 🛡️ Recommended Corrective Actions (Next Steps)

1. **Enforce Engine Exclusion**: Modify `drawResults` to skip the `drawFireCursor` and `drawWaterCursor` calls if a "Higher Substrate" (Babylon/PIXI) is active.
2. **Harmonize Themes**: Update the legacy `drawFireCursor` and `PIXI` textures to support the Cyan Plasma palette when the theme is `LI_PHOENIX` or `LI_V24`.
3. **Parameter Passthrough**: Ensure the `systemState.parameters.visuals.scale` and `intensity` from the Lab sliders are correctly mapped into the `BabylonJuiceSubstrate` update loop.
4. **BFT Purge**: Remove or comment out the `PIXI.Container` logic if Babylon is the designated "Gold" visual path for Linux/Chromebook.

---
*Spider Sovereign (Port 7) | Forensic Analysis Complete | Red Truth Signalled*
