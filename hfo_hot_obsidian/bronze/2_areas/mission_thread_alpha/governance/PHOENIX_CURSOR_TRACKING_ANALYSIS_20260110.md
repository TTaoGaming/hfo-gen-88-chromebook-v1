# 🧬 PHOENIX CURSOR TRACKING ANALYSIS: V30 BEYOND GREEDY NEIGHBORS
**Date**: 2026-01-10
**Author**: GitHub Copilot (Gemini 3 Flash)
**Subject**: Problem Deconstruction & Trade Study: Hand-to-Cursor Association and Zero-Start Optimization.

---

## 🛠️ 1. PROBLEM DECONSTRUCTION

### **A. Startup Friction (The "Center Ghost" Bug)**
*   **Core Issue**: Initialization Bias.
*   **Mechanism**: Cursors are pre-allocated in `hfoState.hands` with coordinates (0.5, 0.5). 
*   **Constraint Failure**: The proximity-based "capture" logic (`snapDistance: 0.15`) prevents immediate control unless the hand is physically aligned with the screen's center at launch.
*   **Impact**: High end-user disorientation; feels like the system is "broken" until a manual capture occurs.

### **B. Interaction Collision (The "Greedy Neighbor" Flaw)**
*   **Core Issue**: Local Optima over Global Consistency.
*   **Mechanism**: Simple Euclidean distance matching from the current frame's landmarks to the last frame's cursor positions.
*   **Failure Modes**:
    1.  **Identity Swap**: When two hands pass within $\delta$ of each other, the "closest" hand claims the first available ID, causing "jittery switching".
    2.  **Tracking Drift**: High-speed movements exceed the `snapDistance`, causing the cursor to "drop" and wait at the center for re-capture.
    3.  **Label Blindness**: The system ignores MediaPipe's semantic labels (Left Hand vs. Right Hand), treating hands as generic spatial points.

---

## 📊 2. MATRIX TRADE STUDY: ASSOCIATION ALGORITHMS

| Criterion | **1. Greedy Spatial (Current)** | **2. Hungarian Optimal** | **3. Semantic Sidedness** | **4. Predictive Kalman** |
| :--- | :--- | :--- | :--- | :--- |
| **Logic Type** | Local Minimum Distance | Global Min-Cost Flow | Classification Mapping | Temporal Projection |
| **ID Consistency** | Low (Swaps on cross) | Medium/High | **Extreme (Sided)** | High |
| **Startup Speed** | Slow (Requires Snap) | Medium | **Instant (Semantic)** | Slow (Needs Data) |
| **CPU Overhead** | Negligible | O(N³) | Negligible | O(N) |
| **Resilience** | Poor | Medium | **High** | Medium |
| **Ease of Build** | Trivial | Complex | **Medium** | High |

---

## ⚖️ 3. OPTION ANALYSIS & TRADEOFFS

### **I. Global Hungarian Optimization**
*   **Analysis**: Solves for the minimum total error for all hands simultaneously using a cost matrix.
*   **Tradeoff**: Prevents one hand from "stealing" an assignment that is mathematically better for the other. However, it still lacks "Hand Memory"—if two hands cross paths, the spatial "optimum" might still swap their IDs.

### **II. MediaPipe Sidedness-Lock (Recommended for v31)**
*   **Analysis**: Forces `H0` to follow Landmarks labeled as "Left" and `H1` to follow "Right" using `multi_handedness` metadata.
*   **Tradeoff**: This is the most "human-aligned" model. It eliminates crossover swaps entirely. The primary risk is MediaPipe "label-flipping" (e.g., mistaking a palm for a back-of-hand), which is less frequent than spatial crossing in standard usage.

### **III. Lazy Initialization (Instant Capture)**
*   **Analysis**: Remove (0.5, 0.5) pre-allocation. Keep cursors hidden or `null` until the first valid landmarks are detected.
*   **Tradeoff**: The first hand seen instantly "claims" a cursor slot. This eliminates the "weird middle start" completely.

---

## 📍 4. STRATEGIC DISPATCH: V31 TARGET ARCHITECTURE
The transition from **v30** to **v31** will implement **Semantic Snapback**:
1.  **State**: Cursors start as `active: false`. Positions are `null` initially (no center ghosting).
2.  **Assignment**: Loop through detections; if `handedness == 'Left'`, update `H0`. If `'Right'`, update `H1`. 
3.  **Acquisition**: If a hand is seen and its corresponding ID is `inactive`, perform an **Instant Snap** to the new landmark coordinates, ignoring distance.

---
*Spider Sovereign (Port 7) | Hive/8 Governance Audit*
