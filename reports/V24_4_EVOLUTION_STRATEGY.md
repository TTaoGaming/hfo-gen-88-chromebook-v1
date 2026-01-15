# HFO Gen 88 | Evolution Report: V24.3 -> V24.4

## 🛰️ Mission Thread: Omega Phoenix Reconstruction

### 🔍 Audit Legitimacy Assessment

The audit points raised in [ai-chat-omega-gen4-v24-3-weakness-2026-1-14.md](reports/ai-chat-omega-gen4-v24-3-weakness-2026-1-14.md) are **Highly Legitimate** and represent critical path blockers for Silver Medallion promotion.

| Issue | Legitimacy | Technical Impact |
| :--- | :--- | :--- |
| **Status Consistency** | Legitimate | Prevents reliable forensic tracking of regressions. |
| **Pointer Lifecycle** | **CRITICAL** | Hardcoded `pointerId: 1` prevents multi-hand stability; missing `pointercancel` causes "stuck" UI states in Excalidraw/React. |
| **Lifecycle Teardown** | **CRITICAL** | Zero `.dispose()` calls leads to WebGL context exhaustion and FPS collapse on Chromebook hardware. |
| **Regression Harness** | Legitimate | We are currently "tuning by feel," which leads to behavioral oscillation. |

---

### 🛠️ V24.4 Evolution Strategy: Hardening & Sovereignty

The next iteration, **V24.4**, will focus on **Sovereign ABI** and **Resource Zero-Trust**.

#### 1. Pointer ABI Hardening (The "Hydra Contract")

We will implement a state-aware injector that guarantees lifecycle completion.

- **Stable pointerId**: Map `handIndex` directly to `pointerId` (Hand 0 -> ID 10, Hand 1 -> ID 11) to avoid system mouse collisions.
- **Lifecycle Invariant**: Every `pointerdown` must be balanced by exactly one `pointerup` or `pointercancel`. If tracking is lost (`COAST` timeout), a `pointercancel` is forcefully emitted.
- **Exemplar Composition**:

  ```javascript
  class PointerStreamSovereign {
    constructor(pointerId) {
      this.id = pointerId;
      this.isActive = false;
    }
    dispatch(type, target, init) {
      if (type === 'pointerdown') this.isActive = true;
      if (type === 'pointerup' || type === 'pointercancel') this.isActive = false;
      target.dispatchEvent(new PointerEvent(type, { ...init, pointerId: this.id }));
    }
  }
  ```

#### 2. Lifecycle Hardening (Medallion Teardown)

Transition from "Static Snippets" to "Managed Components."

- **Dispose Hooks**: Implement a `registry` that tracks all animation frames, video streams, and Babylon engines.
- **Singleton Scoping**: Enforce a strict "One Engine" policy. Before initializing a new `BabylonJuiceSubstrate`, the existing instance must be explicitly destroyed via `engine.dispose()`.

#### 3. Regression Harness (The "Kraken Trace")

- **Record/Replay**: Add a simple `TraceSubstrate` to Port 6 (Store).
- **Deterministic E2E**: Use Playwright to load a pre-recorded hand landmark trace and assert that the cursor satisfies the Ballistic Inertia math within a $\pm$ 5px threshold.

---

### 📝 Todo Notes for V24.4

[ ] **Update Headers**: Synchronize all UI status bars and provenance headers to **V24.4**.
[ ] **Implement `PointerRegistry`**: Replace the current `w3cPointerNematocystInjector` logic with a stateful class-based approach.
[ ] **Hard-code `pointercancel` path**: Replace the `// pointercancel` comments with real event dispatches when FSM leaves `COMMIT` without a valid `pointerup`.
[ ] **Dispose Registry Integration**: Add `window.hfoDisposeAll()` to the GoldenLayout unmount events.
[ ] **Playwright Deterministic Test**: Create `tests/v24_4_ballistic_replay.spec.js` using a mock gesture stream.

---
*Spider Sovereign (Port 7) | Gen 88 Guidance | Evolution V24.4 Initialized*
