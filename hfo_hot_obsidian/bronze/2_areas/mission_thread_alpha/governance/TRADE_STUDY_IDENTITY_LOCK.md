# 📊 Trade Study: Identity Lock & Landmark Assignment (P0-SENSE)

**Date**: 2026-01-10
**Mission**: Phoenix Project | Omega Thread
**Objective**: Robust 1:1 Hand-to-ID mapping under sensor noise and occlusion.

---

## 🏛️ Trade Matrix: Assignment Algorthims

| Option | logic | Pros | Cons | Reliability |
| :--- | :--- | :--- | :--- | :--- |
| **1. Soft Cost Bias** | Euclidean Dist + Soft Handedness Penalty (`0.05`). | Simple, backward compatible with V31. | Still relies on MP labels (noisy). | **Medium** |
| **2. Pure Geometric Lock** | Global greedy match based *only* on distance from prev raw pos. | Immune to handedness label flips. | Hands can "swap" during close crossings. | **High** (Single Hand) / **Low** (Multi-Cross) |
| **3. Temporal Voting** | Average handedness labels over 10 frames before applying cost. | Filters transient MP label noise. | Adds latency to ID discovery. | **Medium-High** |
| **4. Kinetic Prediction** | Cost = Dist from (Prev Pos + Velocity * dt). | High robustness for fast movement. | Complexity; sensitive to framerate. | **High** |
| **5. Hungarian Constraint** | Optimize global cost matrix (not greedy). | Mathematical "Best" for the whole scene. | Can cause both hands to "jump" if noise is high. | **Very High** |

---

## ⚖️ Tradeoffs: Label-Based (V33) vs. Geometric Memory (Simple)

Moving away from the handedness label simplifies the P0-SENSE layer but introduces a key spatial constraint.

| Factor | Label-Based (Current) | Geometric Memory (Simple) |
| :--- | :--- | :--- |
| **Logic** | Snap to ID 0 if MP says "Left". | Snap to ID 0 if it's the closest ID. |
| **MP Label Flip** | **CRASHES** (The point of failure). | **IMMUNE**. |
| **Hand Crossing** | Survives (if labels hold). | **SWAPS** (Hand 0 becomes Hand 1). |
| **Complexity** | High (Bipartite + Penalty). | Low (Raw Distance Matrix). |
| **Startup** | Predetermined IDs. | "First come, first served" discovery. |

### 🚀 The "Simple" Tradeoff: **Predictable Swaps**

The primary tradeoff of moving to Geometric Memory is the **"X-Crossing" problem**.

- **The Risk**: If you cross your hands, Hand 0 (Left) and Hand 1 (Right) will swap identities at the moment of intersection.
- **The Recovery**: Because we are building a *Physics Cursor*, a swap is actually less jarring than a tracking drop. A swap just means the cursor labels change; a tracking drop means the interaction (like a drag) is terminated.

### 🧭 Option: The "Catch-All" Discovery

We can make the geometric logic even simpler by allowing any landmark to claim any **Inactive** ID with zero cost. This solves the "Cold Start" problem where a hand needs to be recognized for the first time.

---

## 🧭 Recommendation: **Hybrid Kinetic-Geometric (Option 5 Lite)**

We should use a **Minimal Total Cost Solver** (Bipartite) but change the cost function to prioritize **Temporal Continuity** over **MediaPipe Labels**.

**The New Formula**:
`Cost = (Distance Weight) + (Temporal Continuity Weight) + (Handedness Tie-breaker)`

1. **Distance**: Raw Euclidean squared.
2. **Persistence**: If hand `H0` was `active` and at `(x,y)`, matching any landmark far from `(x,y)` incurs a massive penalty.
3. **Labels**: Use labels *only* as a tie-breaker (cost = 0.01) if distance is equal.

---
*Spider Sovereign (Port 7) | Mission Engineering Office*
