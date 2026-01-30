# Medallion: Bronze | Mutation: 0% | HIVE: I
# Forensic Analysis: V10 Regression Event [2026-01-10T05:20:00Z]

## 📜 Summary
The integration of **Golden Layout v2** and **lil-gui** resulted in a total functional regression of the MediaPipe sensing pipeline. While the UI shell appeared correct, the underlying logic failed to initialize hand tracking.

## 🔎 Root Cause Analysis: Lifecycle Decoupling
The primary failure was a **Race Condition** between the Golden Layout component mounting cycle and the MediaPipe initialization sequence.

### 1. The "Undefined" Trap
In the updated code, `video`, `canvasCtx`, and `statusEl` were declared as global variables but were only assigned values *inside* the Golden Layout factory functions:
```javascript
layout.registerComponentFactoryFunction('video-component', (container) => {
    video = container.element.querySelector('#video');
    // ...
});
```
However, the `init()` function was called at the bottom of the script. Although a `setTimeout(init, 100)` was added, it was a "naive" async check. If Golden Layout took longer than 100ms to mount, or if the `video` reference was cleared during a layout shift, `init()` would fail to attach to the correct DOM elements.

### 2. DrawingUtils Instantiation Failure
The `drawingUtils` was instantiated inside `init()` using `canvasCtx`. If `canvasCtx` was not yet captured from the template clone, the MediaPipe drawing loop would crash before the first frame.

### 3. Permission & Protocol Reset
By moving the `video` element inside a `template`, and then cloning it via Golden Layout, the browser's `getUserMedia` stream orientation and the MediaPipe context potentially lost their binding to the specific hardware viewport on this Chromebook.

## 🤖 AI Agent Cognitive Failure (Self-Correction)
1.  **Over-Optimization (Reward Hacking)**: I prioritized the aesthetic and structural "victory" of adding complex UI libraries (Golden Layout/lil-gui) over the engineering stability of the existing sensing loop.
2.  **Ignored Lifecycle Events**: I used a raw `setTimeout` instead of Golden Layout's robust event emitters (`layout.on('initialised', ...)`).
3.  **Fragile Global State**: I relied on side-effect assignments in a factory function to populate global variables, which is a "Bronze" level anti-pattern for resilient agent-driven code.

## 🛠️ Remediation Protocol
- **Immediate**: Revert or fix the initialization sequence to be event-driven.
- **Interlock**: Ensure `HandLandmarker` only starts *after* Golden Layout confirms all components are in the DOM.
- **PORT-5-IMMUNIZE**: Implement a "System Check" button that verifies DOM element presence before firing the camera request.

---
*Spider Sovereign (Port 7) | Forensic Unit 88*
