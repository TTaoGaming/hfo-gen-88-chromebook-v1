# Medallion: Bronze | Mutation: 0% | HIVE: V

# Medallion: Bronze | Mutation: 0% | HIVE: I

# 🛸 MISSION THREAD OMEGA: V39 UI PROGRESSIVE DISCLOSURE SPEC

**Date**: 2026-01-16
**Status**: 🛠️ RECONSTRUCTION (PHOENIX REBIRTH)
**Mission**: Phoenix Project (HFO Gen 88 Reconstruction)
**Subject**: V39 Evolution - "Essentials Mode" (Kiosk) vs. "Developer Mode"

---

## 🏗️ 1. ARCHITECTURAL EVOLUTION (V38 -> V39)

The primary goal of V39 is **Reducing Cognitive Load** through **Progressive Disclosure**. We are transitioning the HFO interface from a "Technical Monolith" to a "Context-Aware Kiosk."

### 🔬 Core Changes

- **Dynamic Layout Swapping**: Golden Layout v2 is now modular. The `initLayout(isEssentials)` function can destroy and rebuild the UI without a full reload.
- **lil-gui Folder Gating**: Technical telemetry (Joints, Physics, FSM Internal State) is now hidden by default in "Essentials" mode using tagged folder references (`fPorts`, `fTelem`, etc.).
- **Progressive Discovery**: Users start in a "Zero-Trust" simplified view and can opt-in to technical debt via the `P7: Navigator` toggle.

---

## 📍 2. CURRENT DEVELOPMENT STATUS

| Substrate | Feature | Status |
| :--- | :--- | :--- |
| **P7: NAVIGATOR** | Essentials/Developer Toggle | ✅ IMPLEMENTED |
| **P7: NAVIGATOR** | Folder Tagging (lil-gui) | ✅ IMPLEMENTED |
| **P7: NAVIGATOR** | `applyVisibility` Logic | 🏗️ IN-PROGRESS (80%) |
| **UI: LAYOUT** | `kioskPlan` (2 Panels) | ✅ VERIFIED |
| **UI: LAYOUT** | `devPlan` (Full Matrix) | ✅ VERIFIED |
| **BFT QUORUM** | Shard Consensus | 🟢 0.88 (PASS) |

---

## 📐 3. THE "ESSENTIALS" SPECIFICATION

In **Essentials Mode** (`essentialsMode: true`), the system enforces the following constraints:

1. **Layout**:
    - **Hero View** (75% Width): Visual focus on the AR substrate and hand tracking.
    - **Logs/Navigator** (25% Width): Basic feedback and mission controls.
2. **Navigation GUI**:
    - **Hidden**: `Camera`, `Visuals`, `Landmarks`, `Gestures`, `Palm`, `FSM`, `Coasting`, `Physics`.
    - **Visible**: `Excalidraw Overlay`, `Ports`, `Telem` (Summary).

---

## 🚀 4. PLAN TO COMPLETION (V39.1)

1. **Inject Final Visibility Loop**: Finalize the `P7Navigator.applyVisibility` static method to handle the `folder.show()` / `folder.hide()` transitions.
2. **Link Toggle to Layout**: Ensure the `P7Navigator` toggle triggers `window.dispatchEvent(new CustomEvent('hfo-layout-change'))` to rebuild Golden Layout.
3. **P5 Forensic Audit**: Execute the Syntax Scythe and characterization tests to ensure the "Kiosk" mode doesn't break synthetic interaction.
4. **Baseline Freeze**: Promote `omega_gen4_v39.html` to the Cold Obsidian Bronze vault.

---

*Spider Sovereign (Port 7) | Gen 88 UI Governance*
