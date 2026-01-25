<!--
Medallion: Bronze | Mutation: 0% | HIVE: V
Provenance: Forensic analysis requested after introducing strict palm-cone READY gate in Gen6 v17.4.
-->

# Gen6 v17.4 — Forensic: Palm-Cone READY Gate vs Readiness Meter

## Executive verdict

- **Yes: the unflagged change risks violating the readiness-meter architecture.**
- **Recommendation:** keep the interaction doctrine, but **gate it behind an OpenFeature flag (default off)** until readiness semantics are explicitly split or aligned.

This keeps default behavior stable while allowing you to opt-in and iterate safely.

## Evidence (SSOT anchors)

- Readiness meter fill/drain and `isCharging` (`tensionMs`) logic:
  - [omega_gen6_v17_4.html](omega_gen6_v17_4.html#L1910-L2070)
- FSM transition delegation to P2 adapter (`computeSovereignFsmNext`):
  - [omega_gen6_v17_4.html](omega_gen6_v17_4.html#L1988-L2040)
- P2 Mirror Magus FSM semantics (`computeSovereignFsmNext`) where the READY gate is enforced:
  - [omega_gen6_v17_4.html](omega_gen6_v17_4.html#L3830-L4010)

## Baseline architecture (what the system already does)

### Readiness is a leaky-bucket energy meter (P1)

In v17.4, P1 computes:

- `isFacingCamera = isPalmVisible || isBackVisible`
- `isCharging = isFacingCamera || (now - lastPalmFacingTime < tensionMs)`
- `shouldFill = isCharging && hasConfidence` (except COAST forces drain-only)

So readiness can **continue filling for `tensionMs` after the palm turns away**, by design.

### FSM semantics are delegated to P2 (adapter layer)

P1 calls P2 as:

- `computeSovereignFsmNext({ fsmState, readiness, isFacingCamera, isCharging, ... })`

So P2 can use readiness thresholds, but it also receives raw intent signals.

## What changed (the disputed doctrine)

A strict “palm-cone READY gate” was implemented in P2:

- IDLE → READY requires **gate open**
- READY → IDLE when gate closes
- COMMIT → IDLE when gate closes (also clears primary seat)
- COAST recovery requires gate open

Where “gate open” was set to `isFacingCamera`.

## Why this can violate the readiness-meter architecture

The system now has **two competing “readiness-like” mechanisms**:

1) **Readiness meter** (P1) can remain high (and even increase) under `isCharging` during `tensionMs`.
2) **READY gate** (P2) can deny READY/COMMIT and/or force IDLE purely from `isFacingCamera`.

This creates a split-brain state:

- Readiness may be $\approx 1.0$ (high), suggesting “armed”,
- while P2 forcibly disarms to IDLE because the palm gate is closed.

That mismatch is what you flagged as an architectural violation: **the meter stops being the single source of truth for arming/lock-on semantics**.

## Design interpretation (why the doctrine is still valid)

The doctrine (“anti-midas: palm-away cancels lock-on and requires re-ready + re-commit”) is coherent.

The issue is not the doctrine itself, but that it was introduced **unflagged** and **without explicitly splitting**:

- “readiness energy” (leaky-bucket + coyote time), vs
- “ready-gate orientation” (strict palm-cone).

## Recommendation (safe path)

### 1) Keep the behavior, but feature-flag it (default off)

Add an OpenFeature key:

- `p2-ready-gate-palm-cone` (default `false`)

When enabled:

- enforce strict gate (`isReadyGateOpen = isFacingCamera`) and gate-close drop.

When disabled (legacy):

- treat the gate as `isFacingCamera || isCharging` and do not force IDLE purely on `isFacingCamera=false`.

This preserves the readiness-meter contract for default users while allowing your doctrine as an opt-in evolution.

### 2) If you want this to become default later: split signals explicitly

Promote two distinct concepts into the fabric (future work):

- `readinessEnergy` (leaky-bucket with tension/coyote semantics)
- `readyGateOpen` (strict palm-cone)

Then make FSM transitions depend on **both** explicitly, with crisp invariants.

## “Should we revert?”

- **Do not hard revert** if you still want the doctrine.
- **Do revert the default semantics** by feature-flagging the change (default off). This is a practical rollback that keeps the work while restoring architectural integrity.
