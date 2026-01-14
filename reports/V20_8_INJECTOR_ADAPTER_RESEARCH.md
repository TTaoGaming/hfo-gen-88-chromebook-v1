# Medallion: Bronze | Mutation: 0% | HIVE: I
# 🧪 RESEARCH REPORT: UI INJECTION ADAPTERS (V20.8)
# Prepared for HFO Gen 88 Phoenix Reconstruction

## Executive Summary
Interaction with complex React-based UIs like Excalidraw requires more than simple coordinate projection. This report analyzes four industry-leading exemplars for synthetic event injection to eliminate logic-loop friction and achieve DOM parity.

---

## 🏗️ Exemplar Analysis

### 1. Exemplar Alpha: `testing-library/user-event` v14
**Mechanism**: State-Aware Event Sequencing.
- **Description**: Instead of firing isolated events, it simulates the entire lifecycle (hover -> focus -> down -> move -> up -> click).
- **Core Insight**: It uses `wait` periods to allow frameworks to process pending state updates (e.g., button hover effects).
- **Application for HFO**: Implement a 'Sequencer' that handles the 10ms-20ms React-settle time automatically within Port 3.

### 2. Exemplar Beta: Playwright CDP Emulation
**Mechanism**: Kernel-Level Trusted Injection.
- **Description**: Uses the Chrome DevTools Protocol (CDP) `Input.dispatchMouseEvent` with `isTrusted: true`.
- **Core Insight**: Bypasses many security blocks and 'Untrusted' flags used by frameworks to prevent botting.
- **Application for HFO**: Use as a validation baseline. If Playwright can click it but our injector can't, the issue is 'Trusted' event status.

### 3. Exemplar Gamma: React-Native-Web Gesture Handler
**Mechanism**: FSM-to-Event Mapping.
- **Description**: Maps raw PointerEvents into high-level gestures (Tap, LongPress, ForceTouch).
- **Core Insight**: It decouples the *Detection* of a tap from the *Output* of a click.
- **Application for HFO**: Adopt the 'Tap' detector for COMMIT pulses, allowing a click to fire *during* the commit phase if a 'Z-Push' is detected.

### 4. Exemplar Delta: Windows UI Automation (UIA) Patterns
**Mechanism**: The "Invoke" Pattern.
- **Description**: Instead of simulation, it tells the button to "Invoke" itself via the accessibility tree.
- **Core Insight**: Bypasses coordinate issues entirely by targeting the programmatic ID of the control.
- **Application for HFO**: In v20.8, if a target has a known `aria-label` or `role`, use `element.click()` directly as a fallback to coordinate-based injection.

---

## 📊 Matrix Trade Study: UI Injection Strategies

| Strategy | Fidelity | Latency | Complexity | Security Bypass | Best For |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Simple Dispatch** | Low | Low | Low | None | Basic HTML5 Buttons |
| **user-event Sequence** | **High** | Medium | Medium | Low | React/MUI/Material |
| **CDP Injection** | Very High | **Low** | High | **Total** | Multi-Origin / Trusted Only |
| **UIA Invoke Pattern** | Medium | Low | Low | High | Accessibility/Buttons |
| **HFO Pulse (v20.8)** | High | Low | Medium | Medium | Real-time Gesture Control |

---

## 🚀 Recommendation for V20.8
Implement a **Hybrid Pulse Adapter** (HPA). 
1. **Primary**: Sequenced PointerEvents (Alpha-style) fired on `COMMIT` entry.
2. **secondary**: Z-Axis 'Push' detection to trigger multiple clicks while holding `COMMIT`.
3. **Fallback**: Programmatic `Invoke` (Delta-style) for elements with specific ARIA roles to guarantee interaction.

---
*Spider Sovereign (Port 7) | Research Manifest | Cold Freeze Ready*
