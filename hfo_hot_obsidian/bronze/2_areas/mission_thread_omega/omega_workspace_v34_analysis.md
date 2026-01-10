# Medallion: Bronze | Mutation: 0% | HIVE: H
# 🧬 OMEGA WORKSPACE V34: Architectural Analysis & Logic Mapping

**Date**: 2026-01-10  
**Context**: Mission Thread Omega (Total Tool Virtualization)  
**Goal**: Analyze High-Inertia Identity Tracking and Hero Pattern Layout in V34.

---

## 1. 🏗️ Architecture Overview: The Hero Pattern
V34 transitions to a **Hero Pattern Layout** to maximize the interaction area for Excalidraw while maintaining diagnostic visibility for the 8-Port sensing pipeline.

```mermaid
graph LR
    subgraph "V34 Workspace"
        H[Excalidraw HERO - 70%]
        subgraph "Diagnostic Column - 30%"
            RT[Diagnostic STACK - Top 50%]
            RB[MediaPipe P0 SENSE - Bottom 50%]
        end
    end
```

### Layout Strategy
- **Stage (70%)**: **Excalidraw** acts as the primary "Apex Interaction Surface."
- **Stack (30% Top)**: Diagnostic panels (FSM, Physics, Settings) are layered behind tabs to prevent UI clutter.
- **Sense (30% Bottom)**: The raw MediaPipe feed is pinned for real-time tracking audit.

---

## 2. 🧩 Identity Security: The High-Inertia Tracker
The primary challenge in V34 is the unreliability of MediaPipe's `Left/Right` labels. We utilize a **Geometric Bipartite Solver** with High-Inertia constraints to maintain hand identity.

### Assignment Logic Flow
```mermaid
graph TD
    A[Raw Landmarks from MediaPipe] --> B{Discovery vs Tracking}
    B --> C[Calculate Costs]
    
    subgraph Cost_Constraints
        C1[Active Hand: Cost = Distance]
        C2["Inactive Hand: Cost = Distance + 0.5 Barrier"]
        C3["Teleport Reject: Distance > 0.3 = Reject"]
    end
    
    C --> C1
    C --> C2
    C --> C3
    
    C1 --> D[Sort Matrix by Cost ASC]
    C2 --> D
    
    D --> E{Bipartite Assignment}
    
    subgraph Mutual_Exclusion
        E1{"Prox < 0.12?"}
        E2[Hand Assigned?]
        E3[Landmark Assigned?]
    end
    
    E --> E1
    E1 -- Yes --> F[Reject Phantom]
    E1 -- No --> E2
    E2 -- No --> E3
    E3 -- No --> G[Final Assignment]
    G --> H[Update Filters]
```

### Key Constants
- **Snap Distance ($0.15$)**: The max range for an ID to re-acquire its tracking.
- **Repulsion Distance ($0.12$)**: The territorial boundary to prevent "ID Ghosting" on the same hand.
- **Teleport Limit ($0.3$)**: Hard rejection of non-physical landmark jumps.
- **Discovery Barrier ($+0.5$)**: Favoring existing active IDs to prevent ID swapping.

---

## 3. 🛡️ Persistence: Coastal Recovery
To survive noisy sensing frames where landmarks may vanish temporarily, V34 implements **Coastal Persistence**.

```mermaid
stateDiagram-v2
    [*] --> TRACKING
    TRACKING --> COASTING: "Landmark LOST"
    COASTING --> TRACKING: "Re-acquired (< 60f)"
    COASTING --> INACTIVE: "Timed Out (> 60f)"
    INACTIVE --> [*]
```

---

## 4. 🚀 Data Flow: Pipeline P0 -> P7
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
