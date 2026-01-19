# 🧠 HFO FSM V38: Palm-Oriented "Predict then Confirm" Architecture

**Medallion**: Bronze | **Mutation**: 0% | **HIVE**: I

## 🛠️ Behavioral States

### 1. IDLE (Baseline)

- **Entrance**: System startup or Palm departure.
- **Trigger**: Palm faces camera.
- **Transition**: `ARMING`.
- **Logic**: Lock SNN (Sticky Nearest Neighbor) target to this hand index.

### 2. ARMING (Leaky Bucket Dwell)

- **Constraint**: Must maintain Palm Orientation.
- **Trigger**: Continuous dwell for `X ms` (Target: 300ms).
- **Wait**: `ARMING_THRESHOLD`.
- **Success**: `ARMED`.
- **Failure**: Palm departures/rotation resets bucket to `IDLE`.

### 3. ARMED (Sticky Tracking)

- **Context**: Virtual cursor is active but not "clicking".
- **Trigger**: Detect `NONE` gesture (Relaxed state).
- **Transition**: `COMMITTING`.
- **Logic**: Begin "Predict then Confirm" loop for the intent to point.

### 4. COMMITTING (Intent Validation)

- **Mechanism**: Predict and Confirm.
- **Trigger**: High confidence `POINTING_UP` detected.
- **Success**: `COMMITTED` (Dispatches `pointerdown`).
- **Failure**: Persistent `NONE` or other gestures revert to `ARMED` or `IDLE` after timeout.

### 5. COMMITTED (Action Lock)

- **Context**: State of pointer down/drag.
- **Persistence**: Coasting and Snap-lock enabled for noisy tracking.
- **Trigger**: Transition from `POINTING_UP` to `NONE`.
- **Transition**: `RELEASING`.

### 6. RELEASING (Ambiguity Resolution)

- **Predictive Pattern**:
  - **Confirmed Release**: High confidence `OPEN_PALM` -> `ARMED` (Dispatches `pointerup`).
  - **Noisy Re-grip**: `POINTING_UP` detected -> `COMMITTED` (Cancels release, treats as noise).
  - **Cancellation**: Any other gesture (or sustained unknown) -> Leaky bucket dwell -> `IDLE` (Dispatches `pointercancel`).

## 🛡️ Global Departure Logic

- **Scope**: Applied to `ARMING`, `ARMED`, `COMMITTING`, `COMMITTED`, `RELEASING`.
- **Trigger**: Palm Orientation Normal leaves active zone (facing camera).
- **Wait**: Leaky bucket dwell (Coastal persistence).
- **Result**: Forced fallback to `IDLE`.
