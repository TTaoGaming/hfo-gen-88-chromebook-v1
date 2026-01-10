# 🕵️ Forensic Analysis: P0-SENSE Sensing Regression (V33)
**Date**: 2026-01-10
**Mission**: Phoenix Project | Omega Thread
**Status**: 🔴 **CRITICAL REGRESSION IDENTIFIED**

## 1. The Incident
The user reports that `omega_workspace_v33.html` no longer tracks hands in real-time, despite the "HFO P5 Forensic Harness" reporting "ALL SYSTEMS NOMINAL".

## 2. Root Cause: "Hard Identity Lock" (Bipartite Failure)
In the effort to implement "Identity Security" (Bipartite Minimal Cost Solver), I introduced a handedness penalty that is too aggressive for real-world sensing noise.

### Code Analysis (v33.html:614-617)
```javascript
const handedness = res.handedness?.[lIdx]?.[0]?.categoryName;
const prefId = (handedness === 'Left') ? 0 : (handedness === 'Right' ? 1 : null);
...
if (id == prefId && !h.active) cost = 0.0; // Discovery snap
else if (id != prefId) cost += 0.5; // Handedness penalty
```

- **Problem A**: MediaPipe often flips or mislabels handedness (`Left` vs `Right`) depending on camera occlusion or mirroring.
- **Problem B**: The `cost += 0.5` penalty makes the total cost significantly higher than `hfoState.physics.persistence.snapDistance` (0.15).
- **Result**: If MediaPipe thinks your left hand is "Right" (Label 1), and it was previously tracking as Hand 0, the cost becomes `d + 0.5`. Since `0.5 > 0.15`, the solver **rejects the landmark**. The hand enters a "Coast" state and eventually deactivates. It can never be rediscovered as Hand 0 because the cost remains `> 0` for any mismatched handedness.

## 3. The "AI Theater" Breach (Why Tests Passed)
The P5 Forensic Harness passed because I used **Synthetic Injection**:
```typescript
// scripts/v33_e2e.spec.ts
await hfoPage.injectHand(0, {
      active: true,
      state: 'COMMITTED',
      ...
});
```
This manually forces `active = true`, bypassing the `costMatrix` logic in the `render()` loop. My tests were validating the **State Machine (P3)** but not the **Sensing Connection (P0)**.

## 4. Remediation Plan (To be executed upon approval)
1.  **Soften the Identity Lock**: Change the cost penalty from a "Hard Reject" (`0.5`) to a "Soft Tie-breaker" (`0.05`).
2.  **Fallback Snap**: Ensure that if only one hand is present, it can snap to either ID regardless of handedness label.
3.  **Harness Upgrade**: Create a "Sensing Simulation" test that feeds raw MediaPipe-like landmark data into the `render()` loop to verify the Bipartite Solver's recovery capabilities.

---
*Spider Sovereign (Port 7) | Forensic Analysis Log*
