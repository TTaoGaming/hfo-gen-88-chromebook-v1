# Medallion: Bronze | Mutation: 0% | HIVE: H
# OMEGA Workspace V34 Analysis

## 1. Architecture Overview
V34 transitions to a Hero Pattern Layout.

```mermaid
graph LR
    H[Excalidraw] --- RT[Stack]
    H --- RB[Sense]
```

### Layout Strategy
- **Stage (70%)**: **Excalidraw** acts as the primary "Apex Interaction Surface."
- **Stack (30% Top)**: Diagnostic panels (FSM, Physics, Settings) are layered behind tabs to prevent UI clutter.
- **Sense (30% Bottom)**: The raw MediaPipe feed is pinned for real-time tracking audit.

---

## 2. Identity Security: The High-Inertia Tracker
The primary challenge in V34 is the unreliability of MediaPipe's `Left/Right` labels. We utilize a **Geometric Bipartite Solver** with High-Inertia constraints to maintain hand identity.

### Assignment Logic Flow
```mermaid
graph TD
    A[Raw Landmarks] --> B{Discovery}
    B --> C[Calculate Costs]

    C --> C1[Active: Dist]
    C --> C2[Inactive: Dist + 0.5]
    C --> C3[Reject: Dist > 0.3]

    C1 --> D[Sort Matrix]
    C2 --> D

    D --> E{Assignment}

    E --> E1{Prox < 0.12?}
    E1 -- Yes --> F[Reject]
    E1 -- No --> G[Final ID]
```

### Key Constants
- **Snap Distance ($0.15$)**: The max range for an ID to re-acquire its tracking.
- **Repulsion Distance ($0.12$)**: The territorial boundary to prevent "ID Ghosting" on the same hand.
- **Teleport Limit ($0.3$)**: Hard rejection of non-physical landmark jumps.
- **Discovery Barrier ($+0.5$)**: Favoring existing active IDs to prevent ID swapping.

---

## 3. Persistence: Coastal Recovery
To survive noisy sensing frames where landmarks may vanish temporarily, V34 implements **Coastal Persistence**.

```mermaid
stateDiagram-v2
    [*] --> TRACKING
    TRACKING --> COASTING : Lost
    COASTING --> TRACKING : Found
    COASTING --> INACTIVE : Timeout
    INACTIVE --> [*]
```

---

## 4. Data Flow: Pipeline P0 -> P7
The interaction data flows through a series of filters and physics engines before reaching the virtual surface.

```mermaid
sequenceDiagram
    participant Cam as Camera
    participant P0 as SENSE (MediaPipe)
    participant P1 as BRIDGE (Solver)
    participant P2 as SHAPE (Matter.js)
    participant P3 as INJECT (W3C Events)
    participant HW as OMEGA (Excalidraw)

    Cam->>P0: Raw Pixels
    P0->>P1: Landmarks
    Note over P1: High-Inertia Filtering
    P1->>P2: Normalised Coords
    Note over P2: Physics Lookahead
    P2->>P3: FSM + Corrected XY
    P3->>HW: Dispatch PointerEvent
```

---

## 5. 🛠️ Current Implementation Summary
| Feature | Implementation | Medallion Layer |
| :--- | :--- | :--- |
| **Solver** | Bipartite Minimal Cost (Geometric Only) | Bronze (V34) |
| **Identity** | High-Inertia (+0.5 Barrier for discovery) | Bronze (V34) |
| **Persistence** | 1.0s (60f) Coastal Window | Bronze (V34) |
| **Repulsion** | 0.12 Territorial Exclusion | Bronze (V34) |
| **Physics** | Matter.js Spring + Lookahead Prediction | Bronze (V34) |
| **UI** | Golden Layout Hero Pattern | Bronze (V34) |

---
*Spider Sovereign (Port 7) | Architectural Evidence Archive | 2026-01-10*


