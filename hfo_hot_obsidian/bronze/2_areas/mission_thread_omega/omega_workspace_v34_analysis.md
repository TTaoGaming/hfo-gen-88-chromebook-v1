# Medallion: Bronze | Mutation: 0% | HIVE: H
# 🧬 OMEGA WORKSPACE V34: Architectural Analysis & Logic Mapping

**Date**: 2026-01-10  
**Context**: Mission Thread Omega (Total Tool Virtualization)  
**Goal**: Analyze High-Inertia Identity Tracking and Hero Pattern Layout in V34.

---

## 1. 🏗️ Architecture Overview: The Hero Pattern
V34 transitions to a **Hero Pattern Layout** to maximize the interaction area for Excalidraw while maintaining diagnostic visibility for the 8-Port sensing pipeline.

```mermaid
grid-layout
    title V34 Workspace Layout (Hero Pattern)
    [Excalidraw (Left 70%)] [Diagnostic Stack (Right Top 30% / 50% H)]
    [Excalidraw (Left 70%)] [MediaPipe P0 Sense (Right Bottom 30% / 50% H)]
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
    B -->|Calculate Costs| C[Cost Matrix: Distance between Hand[ID] and Landmark]
    
    subgraph Cost Barriers
    C1[Active Hand: Cost = Distance]
    C2[Inactive Hand: Cost = Distance + 0.5 Barrier]
    C3[Teleport Reject: Distance > 0.3 = Reject]
    end
    
    C --> C1
    C --> C2
    C --> C3
    
    B --> D[Sort Matrix by Cost ASC]
    D --> E[Bipartite Assignment Loop]
    
    subgraph Mutual Exclusion
    E1{Is Physical Proximity < 0.12?}
    E2{Is Hand ID assigned?}
    E3{Is Landmark assigned?}
    end
    
    E --> E1
    E1 -- Yes --> F[Reject: Landmark Doubling]
    E1 -- No --> E2
    E2 -- No --> E3
    E3 -- No --> G[Assign ID to Landmark]
    G --> H[Update Coordinates & Filter State]
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
    [*] --> TRACKING: Landmark Seen
    TRACKING --> TRACKING: assignment[ID] exists
    TRACKING --> COASTING: assignment[ID] LOST
    
    COASTING --> TRACKING: Re-acquired within 60 frames
    COASTING --> INACTIVE: frames > 60
    
    subgraph Interaction Persistence
    TRACKING: Interaction Active
    COASTING: Interaction STICKY (IsDown preserved)
    INACTIVE: Released
    end
```

---

## 4. 🚀 Data Flow: Pipeline P0 -> P7
The interaction data flows through a series of filters and physics engines before reaching the virtual surface.

```mermaid
sequenceDiagram
    participant Camera
    participant P0: SENSE (MediaPipe)
    participant P1: BRIDGE (Geometric Solver)
    participant P2: SHAPE (Matter.js / Filters)
    participant P3: INJECT (W3C Pointer Events)
    participant OMEGA: EXCALIDRAW
    
    Camera->>P0: Raw Pixels
    P0->>P1: Normalised Landmarks
    P1->>P1: Apply High-Inertia Barrier
    P1->>P2: Smooth & Snappy Coords
    P2->>P2: Predictive Physics (Lookahead)
    P2->>P3: Corrected X/Y + FSM State
    P3->>OMEGA: PointerDown / PointerMove
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
