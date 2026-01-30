# Medallion: Bronze | Mutation: 0% | HIVE: V

# 🛰️ HFO SWARM HANDOFF BATON: [2026-01-17 00:00 UTC]

**Status**: 🔴 **STABILIZED BASELINE / CODE FREEZE**
**Mission Thread**: Omega (V33.1 Purified)
**Medallion**: Hot Bronze
**Consensus**: 0.78 (DEGRADED)

---

## 🚩 CRITICAL ALERT: THE COORDINATE LIE

The current `active_omega.html` (V33.1) contains **Stale Coordinate Math**. It uses a cached `containerRect` that does NOT update when Golden Layout panels are dragged.

- **DO NOT** attempt to "Fix" this with more listeners.
- **RESTORE** the logic from `omega_gen4_v28_4.html` where `getBoundingClientRect()` is called inside the projection function.

## 📦 ACTIVE SUBSTRATE

- **Baseline**: `omega_gen4_v33_1.html`
- **Entry Point**: `active_omega.html`
- **Environment**: `.venv/bin/python` (Required for P5 Audit).

## 🔬 STALE INFO & WIP

- **Chronos Failure**: A timestamp reversal exists at blackboard line 5556. System flags this as a "Red Truth" fracture.
- **Excalidraw Bridge**: Synthetic `PointerEvents` are landing ~40px too high. The math desync is likely in the `toViewportY` scaling factor.
- **Slop Purge**: File `v33_1` is scrubbed of the slop. Keep it that way.

## 🕸️ NEXT STEPS FOR SWARM

1. **Restore Polling**: Revert the UPE to per-frame repolling.
2. **Localize Assets**: Download Excalidraw UMD bundles to `lib/` for 100% offline parity.
3. **Execution**: Once math is restored, run `python scripts/hfo_alpha_trial.py` to verify the pulse.

---
*Spider Sovereign (Port 7) | Handoff Baton DISPATCHED*
