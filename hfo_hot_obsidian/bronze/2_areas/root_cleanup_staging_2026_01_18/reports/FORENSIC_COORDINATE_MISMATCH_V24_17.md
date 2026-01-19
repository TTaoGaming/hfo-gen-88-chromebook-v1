# Medallion: Bronze | Mutation: 0% | HIVE: V

# Forensic Analysis: Skeletal Coordinate Mismatch (v24.17)

## 📌 Executive Summary

A visual misalignment was detected in the Babylon.js skeletal substrate of `omega_gen4_v24_17.html`. While landmarks were correctly mirrored and projected, the depth calculation failed to account for perspective foreshortening.

## 🔍 Root Cause: "Z-Overwrite" Fallacy

The `projectToWorld` utility function was designed to project 2D screen coordinates onto the static `Z=0` world plane. In `v24.17`, the implementation followed this pattern:

1. **Project**: Screen `(x, y)` &rarr; World `(X, Y, 0)`.
2. **Overwrite**: World `(X, Y, 0)` &rarr; World `(X, Y, Depth)`.

### 📉 Mathematical Fracture

In a perspective camera (e.g., `BABYLON.FreeCamera`), the relationship between world coordinates $(X, Y)$ and screen coordinates $(x, y)$ is:
$x \propto \frac{X}{Z}$ and $y \propto \frac{Y}{Z}$

By projecting to $Z=0$ first and *then* moving the point along the Z-axis without adjusting $X$ and $Y$, the resulting 3D point no longer maps back to its original screen coordinate. The bone structure "shifts" and appearing disconnected from the 2D video backdrop.

## 🛠️ Remediation Strategy

1. **Dynamic Depth Projection**: Modify `projectToWorld` to project along the camera ray until it hits the specific $Z$ depth provided by MediaPipe.
2. **Alpha Attenuation**: Reduce `skeletonMat` alpha to $0.2$ to shift focus back to the "Phoenix Core" fire visuals.
3. **Global Parity**: Ensure `projectToWorld` is used consistently for both the "Pointer Tip" and "Landmark Spheres" at their respective depths.

---
*Spider Sovereign (Port 7) | Forensic Unit 88*
