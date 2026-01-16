# 🦅 HFO Gen 88: Forensic Analysis Report [V28.1]

## 📝 Status Overview
*   **Version**: 0.28.1-Bronze
*   **Mission Thread**: Omega (Phoenix Rebirth)
*   **Status**: 🟠 DEGRADED (Functional PASS / Visual FAIL)

---

## 🔍 The Paradox: Functional Working vs. Visual Broken
The user reports that **FSM state transitions** and **W3C Pointer interactions** (clicks/drags) are working perfectly, but the **Phoenix Core (BabylonJS)** fire visualization and skeleton are either missing, offset, or "stuck."

### 1. Why Interactions Work
The `w3cPointerNematocystInjector` (Port 3) uses a "Double-Derived" projection strategy. It reads `cursor.normX` from the Data Fabric and passes it to the `UniversalProjectionEngine` (UPE) stubs:
```javascript
const viewX = systemState.p1.toViewportX(cursor.normX); // Recalculates uiNorm on the fly
```
Because `normX` is a core property of the `FusionSchema`, it survives the **Port 1 Contract Breach** check. The UPE corrects the offset during the call, allowing the pointer to reach the corners.

### 2. Why Visualization is Broken (The "Zod Scythe")
The `BabylonJuiceSubstrate` (Port 4) relies on pre-fused properties in the `cursors` array:
```javascript
const targetPos = this.projectToWorld(c.uiNormX, c.uiNormY, ...);
```
In `P1Bridger.fuse`, the new `uiNormX/Y` properties are calculated and added to the `rawCursorData`. However, immediately following this, the data is passed through:
```javascript
cursorData = FusionSchema.parse(rawCursorData);
```
**CRITICAL FAILURE**: `FusionSchema` was not updated to include `uiNormX` or `uiNormY`. Zod, performing its duty as the Medallion Gatekeeper, strips these "unknown" properties. Consequently, the Babylon substrate receives `undefined` for coordinates, causing the 3D emitters to fail or default to origin coordinates.

---

## 🛠️ Root Cause Identification
1.  **Contract Asymmetry**: The **Shared Data Fabric** schema (`FusionSchema`) acts as a filter. Introducing new properties to the logic without updating the contracts results in silent data loss.
2.  **Decoupled Calculation**: The injector re-calculates projection, masking the data loss in Port 3, while the visual substrate trusts the fabric, exposing it in Port 4.

---

## 🚀 Corrective Action Plan
1.  **Harden the Contract**: Update `FusionSchema` to explicitly include `uiNormX` and `uiNormY`.
2.  **Back-fill Coasting**: Ensure `uiNorm` coordinates are recalculated during `COAST` states to prevent visual "snapping" during tracking loss.
3.  **Unified Source of Truth**: Refactor Port 3 to use the pre-calculated `cursor.uiNormX` instead of re-deriving it, ensuring that any future visual break is immediately detectable as a functional break (Anti-Theater).

---
*Spider Sovereign (Port 7) | Gen 88 Forensic Analysis*
