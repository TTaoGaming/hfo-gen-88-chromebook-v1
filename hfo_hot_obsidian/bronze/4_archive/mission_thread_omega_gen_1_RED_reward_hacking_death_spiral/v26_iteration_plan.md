# Medallion: Bronze | HIVE: I | Version: V26
# 🚀 V26: OMEGA TOOL ONBOARDING (Excalidraw & Piano Genie)

## 🎯 Objective
Promote the **Physics Cursor** from a visual-only state to a **Functional Injection State**. We will integrate two apex virtual tools as targets for our W3C Pointer Event stack.

## 🛠️ Components Missing / Needed
1.  **Tool Substrates**: 
    - **Excalidraw**: Integrated via Iframe or direct React mount (if environment supports).
    - **Piano Genie**: Integrated via Iframe (Magenta.js web demo).
2.  **Event Passthrough 2.0**:
    - Current `p3InjectPointer` uses `document.elementFromPoint(x, y)`. This fails for `iframes`.
    - **Required**: A coordinate transformation layer that detects if the cursor is over a Tool Panel and maps coordinates relative to that panel's internal space.
3.  **HFO Workspace Panel Expansion**:
    - Update Golden Layout configuration to include `Excalidraw` and `Piano Genie` tabs.
4.  **Gesture Multi-Mode**:
    - Piano Genie requires rapid "taps". Excalidraw requires "drags". We need to verify the **Leaking Bucket FSM** covers both with minimal latency.

## 📐 V26 Architecture Plan
1.  **Clone**: `omega_workspace_active.html` -> `omega_workspace_v26.html`.
2.  **Substrate Injection**:
    - Create `V26_EXCALIDRAW_PATCH`: A small shim to allow PointerEvents to pass through to the iframe (using `postMessage` or same-origin direct access).
    - Create `V26_PIANO_GENIE_BRIDGE`: Mapping the COMMITTED (Down) state to the high-frequency trigger buttons of Piano Genie.
3.  **Coordinate Mapping**:
    ```javascript
    const targetRect = toolPanel.getBoundingClientRect();
    const relX = (x - targetRect.left);
    const relY = (y - targetRect.top);
    // Dispatch to iframe
    ```

## ✅ Success Criteria
- [ ] Excalidraw: Successfully draw a circle using a "Pointing Up" drag.
- [ ] Piano Genie: Successfully trigger notes by "Pointing Up" on the virtual keys.
- [ ] Multi-Hand: Hand 0 on Excalidraw and Hand 1 on Piano Genie simultaneously.

---
*Spider Sovereign (Port 7) | Gen 88 Omega Evolution*
