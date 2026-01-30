# Requirements Document: HFO Mosaic Ghost Cursor

## Introduction

HFO Mosaic Ghost Cursor is a **Capacity Engineering Platform** that produces a trusted, replayable, engine-agnostic pointer from mobile camera input. The Ghost Cursor is the core deliverable - a spatial computing input layer that any application can consume.

**Mission**: Turn mobile camera into spatial computing input via commodity exemplar composition (Wardley-style capacity engineering).

**Architecture**: Complete HFO 8-Port Hexagonal (Mosaic Warfare DNA)
- All 8 Obsidian roles online with production exemplars
- Physics checks and regression guards BEFORE adding new tech
- Exemplars discovered via web search, wrapped via strangler fig, graded via deterministic test harness
- Score fusion for MAP-Elites / DSE Pareto frontier optimization

**Phoenix Protocol**: This is a cold start. Existing codebase (`src/gesture_ninja/`) is archived as reference only - we assemble verified mosaic tiles with tests first. No tech debt inheritance.

**Zero Magic Numbers Principle**: All thresholds are adaptive to available space, user-tuneable, and guarded. No hardcoded constants - everything flows through configuration with validation.

**Polymorphic Adapter Principle**: If locked into a vendor, language, or format, the architecture is wrong. Every port boundary uses adapters that can be swapped without changing adjacent ports.

**Architecture Progression**:
- Phase 1: Bridger LITE (EventEmitter) + full 8 Mosaic roles
- Phase 2: Upgrade to NATS + OpenTelemetry (required for test harness)
- Phase 3: Full production Bridger with CloudEvents + tracing

**Latency Mitigation**: Device performance offset with async visuals + predictive latency (Kalman prediction renders ahead of actual position).

---

## Dependency Manifest (Verified Exemplars)

### TypeScript/JavaScript (npm)
| Package | Version | Purpose | TRL |
|---------|---------|---------|-----|
| @vladmandic/human | ^3.3.6 | Hand tracking, gesture recognition, finger pose | 8 |
| @webarkit/oneeurofilter-ts | latest | Velocity-adaptive cursor smoothing | 9 |
| xstate | ^5.x | State machine (IDLE→TRACKING→ARMED→DISARMED→COASTING) | 9 |
| cloudevents | ^8.x | Event envelope format | 9 |
| nats.ws | ^1.x | WebSocket messaging (Phase 2) | 8 |
| @opentelemetry/api | ^1.x | Distributed tracing (Phase 2) | 8 |
| fast-check | ^3.x | Property-based testing (JS) | 8 |

### Python (pip)
| Package | Version | Purpose | TRL |
|---------|---------|---------|-----|
| hypothesis | ^6.x | Property-based testing | 9 |
| pyribs | ^0.7.x | MAP-Elites QD optimization | 9 |
| pydantic | ^2.x | Data validation | 9 |

### Human.js Built-in Capabilities (DO NOT REINVENT)
- 21 hand keypoints (palm + 4 per finger)
- Finger curl: none, half, full
- Finger direction: 8 directions
- Gestures: thumbsUp, victory, point, middleFinger, openPalm
- Custom gesture definition via FingerGesture class
- Frame interpolation (time-based weighted average)

### Patterns Adopted from Other Exemplars (MIT License)
| Pattern | Source | Purpose |
|---------|--------|---------|
| Dwell clicking | Tracky Mouse | Hover-to-click with visual feedback |
| Pinch click (thumb-to-index) | NonMouse | Fast click alternative to dwell |
| Scroll gesture (index curl) | NonMouse | Scroll by curling index finger |
| Camera placement modes | NonMouse | Normal/Above/Behind camera positions |
| Smoothing settings UI | Tracky Mouse | User-configurable sensitivity |

---

## Glossary

- **Ghost_Cursor**: The trusted, smoothed pointer output from Shaper - the core deliverable
- **Mosaic_Warfare**: Distributed, composable system where any component can be swapped
- **Capacity_Engineering**: Solving classes of problems, not instances, via commodity adoption
- **Exemplar**: A working open-source solution to a problem class (e.g., 1Euro filter for jitter)
- **Strangler_Fig**: Pattern where new code wraps legacy/exemplar code, gradually replacing it
- **Stigmergy**: Indirect coordination via shared environment (NATS messages)
- **CloudEvents**: Standard event envelope format for inter-port messages
- **CanonicalHandState**: Normalized hand tracking data from any sensor
- **CanonicalIntent**: Trusted cursor output with position, velocity, confidence, armed state
- **1Euro_Filter**: Adaptive low-pass filter (smooth when slow, responsive when fast)
- **Inertial_Coasting**: Physics-based cursor continuation during tracking loss
- **Score_Fusion**: Weighted combination of multiple metrics into single Pareto-comparable score
- **MAP_Elites**: Quality-Diversity algorithm for exploring solution space
- **DSE**: Design Space Exploration - systematic evaluation of alternatives
- **AoA**: Analysis of Alternatives - NASA/DoD trade study methodology

---

## System Architecture

```mermaid
flowchart TB
    subgraph "Port 0: Observer ☷"
        HJS[Human.js Adapter]
        MP[MediaPipe Adapter]
        CHS[CanonicalHandState]
        HJS --> CHS
        MP --> CHS
    end

    subgraph "Port 1: Bridger ☶"
        CE[CloudEvents Envelope]
        TC[W3C Trace Context]
        NATS[NATS Stigmergy]
        CHS --> CE
        CE --> TC
        TC --> NATS
    end

    subgraph "Port 2: Shaper ☵"
        EURO[1Euro Filter]
        KAL[Kalman Predictor]
        SM[State Machine]
        CI[CanonicalIntent]
        NATS --> EURO
        EURO --> KAL
        KAL --> SM
        SM --> CI
    end

    subgraph "Port 3: Injector ☴"
        GAME[Game Consumer]
        DRAW[Excalidraw Consumer]
        CI --> GAME
        CI --> DRAW
    end

    subgraph "Port 4: Disruptor ☳"
        HYP[Hypothesis PBT]
        FUZZ[Fuzz Testing]
        CHAOS[Chaos Injection]
    end

    subgraph "Port 5: Immunizer ☲"
        INV[Invariant Checks]
        TRIP[Tripwires]
        GUARD[Regression Guards]
    end

    subgraph "Port 6: Assimilator ☱"
        JSONL[JSONL Replay]
        GOLD[Golden Masters]
        METRICS[Score Fusion]
    end

    subgraph "Port 7: Navigator ☰"
        MCTS[MCTS Search]
        QD[pyribs Archive]
        DSE[Pareto Frontier]
    end
```

---

## Data Flow Sequence (Bridger as Substrate)

```mermaid
sequenceDiagram
    participant Camera
    participant Observer as Port 0: Observer
    participant Bridger as Port 1: Bridger (Substrate)
    participant Shaper as Port 2: Shaper
    participant Injector as Port 3: Injector
    participant Immunizer as Port 5: Immunizer
    participant Assimilator as Port 6: Assimilator

    Note over Bridger: ALL port-to-port communication goes through Bridger

    Camera->>Observer: Raw frame
    Observer->>Observer: Extract 21 landmarks
    Observer->>Bridger: Publish CanonicalHandState
    Bridger->>Bridger: Wrap CloudEvents + TraceContext
    Bridger->>Immunizer: Validate schema
    Immunizer-->>Bridger: OK / Reject
    Bridger->>Shaper: Deliver validated event
    Shaper->>Shaper: 1Euro + Kalman + StateMachine
    Shaper->>Bridger: Publish CanonicalIntent
    Bridger->>Assimilator: Record to JSONL
    Bridger->>Injector: Deliver intent
    Injector->>Injector: Drive game/app

    Note over Bridger: No port talks directly to another port
```

---

## State Machine (Shaper)

```mermaid
stateDiagram-v2
    [*] --> IDLE: System start

    IDLE --> TRACKING: Hand detected (confidence ≥ 0.7)

    TRACKING --> ARMED: Velocity > arm_threshold
    TRACKING --> COASTING: Tracking lost (confidence < 0.5)
    TRACKING --> IDLE: No hand for > coast_timeout

    ARMED --> DISARMED: Velocity < disarm_threshold for disarm_delay
    ARMED --> COASTING: Tracking lost (confidence < 0.5)

    DISARMED --> ARMED: Velocity > arm_threshold
    DISARMED --> COASTING: Tracking lost (confidence < 0.5)
    DISARMED --> IDLE: No hand for > coast_timeout

    COASTING --> TRACKING: Hand reacquired (confidence ≥ 0.7)
    COASTING --> IDLE: coast_timeout exceeded (500ms default)

    note right of IDLE: No cursor visible
    note right of TRACKING: Cursor visible, gestures blocked
    note right of ARMED: Gestures enabled (fast movement)
    note right of DISARMED: Gestures blocked (slow/still)
    note right of COASTING: Inertial continuation, cursor fading
```

---

## Dwell/Hover Click Pattern

```mermaid
stateDiagram-v2
    [*] --> OUTSIDE: Cursor not on target

    OUTSIDE --> HOVERING: Cursor enters target hitbox

    HOVERING --> DWELLING: Cursor still in hitbox
    HOVERING --> OUTSIDE: Cursor exits hitbox

    DWELLING --> ACTIVATED: dwell_time reached (500ms default)
    DWELLING --> OUTSIDE: Cursor exits hitbox (timer reset)

    ACTIVATED --> COOLDOWN: Action triggered

    COOLDOWN --> OUTSIDE: cooldown_time elapsed

    note right of HOVERING: Visual feedback starts
    note right of DWELLING: Progress indicator filling
    note right of ACTIVATED: Action fires once
    note right of COOLDOWN: Prevent double-activation
```

---

## Play Area and Gain Controls

```mermaid
flowchart TB
    subgraph "Physical Space"
        HAND[Hand Position in Camera]
    end

    subgraph "Gain Controls"
        PLAY[Play Area Bounds]
        GAIN[Gain Multiplier]
        DEAD[Deadzone]
        SMOOTH[Smoothing Factor]
    end

    subgraph "Screen Space"
        CURSOR[Cursor Position on Screen]
    end

    HAND --> PLAY
    PLAY --> |"Clamp to bounds"| GAIN
    GAIN --> |"Scale movement"| DEAD
    DEAD --> |"Ignore small movements"| SMOOTH
    SMOOTH --> |"Apply 1Euro filter"| CURSOR

    note1[/"Play Area: Define active region in camera view"/]
    note2[/"Gain: 1.0 = 1:1, >1 = amplified, <1 = reduced"/]
    note3[/"Deadzone: Ignore jitter below threshold"/]
```

---

## Exemplar Composition Matrix

```mermaid
mindmap
  root((Ghost Cursor))
    Port 0 Observer
      Human.js v3.3.6
        TRL 8
        npm install
        21 keypoints
      MediaPipe Hands
        TRL 9
        WASM setup
        Google maintained
    Port 1 Bridger
      CloudEvents SDK
        TRL 9
        CNCF standard
      NATS.ws
        TRL 8
        WebSocket client
      OpenTelemetry JS
        TRL 8
        Tracing standard
    Port 2 Shaper
      1Euro Filter
        TRL 9
        Géry Casiez
        50 lines
      Kalman Filter
        TRL 9
        Textbook algo
      XState
        TRL 9
        State machine
    Port 4 Disruptor
      Hypothesis
        TRL 9
        Python PBT
      fast-check
        TRL 8
        JS PBT
    Port 6 Assimilator
      JSONL
        TRL 9
        Append-only
      Golden Masters
        TRL 9
        Deterministic
```

---

## Score Fusion Test Harness

```mermaid
flowchart LR
    subgraph "Input"
        REPLAY[Replay JSONL]
        GOLDEN[Golden Master]
    end

    subgraph "Metrics"
        LAT[Latency p95]
        JIT[Jitter StdDev]
        FALSE[False Activations]
        TRACK[Tracking Recovery]
        ROUND[Round-Trip Fidelity]
    end

    subgraph "Fusion"
        NORM[Normalize 0-1]
        WEIGHT[Apply Weights]
        PARETO[Pareto Score]
    end

    subgraph "Output"
        QD[QD Archive]
        FRONTIER[Pareto Frontier]
        GRADE[Test Grade]
    end

    REPLAY --> LAT
    REPLAY --> JIT
    REPLAY --> FALSE
    REPLAY --> TRACK
    GOLDEN --> ROUND

    LAT --> NORM
    JIT --> NORM
    FALSE --> NORM
    TRACK --> NORM
    ROUND --> NORM

    NORM --> WEIGHT
    WEIGHT --> PARETO

    PARETO --> QD
    PARETO --> FRONTIER
    PARETO --> GRADE
```

---

## The 8 Obsidian Ports (Complete Mosaic)

```mermaid
graph TB
    subgraph "Gherkin Flow"
        GIVEN[GIVEN: Observer senses]
        AND1[AND: Bridger connects]
        AND2[AND: Shaper transforms]
        WHEN[WHEN: Injector triggers]
        THEN[THEN: Disruptor tests]
        BUT[BUT: Immunizer validates]
        AS[AS: Assimilator remembers]
        TO[TO: Navigator optimizes]
    end

    GIVEN --> AND1 --> AND2 --> WHEN --> THEN --> BUT --> AS --> TO
```

---

## Architecture Progression

```mermaid
flowchart LR
    subgraph "Phase 1: Bridger LITE"
        EE[EventEmitter]
        LOCAL[Local Only]
        EE --> LOCAL
    end

    subgraph "Phase 2: NATS + Tracing"
        NATS2[NATS.ws]
        OTEL[OpenTelemetry]
        HARNESS[Test Harness Ready]
        NATS2 --> OTEL
        OTEL --> HARNESS
    end

    subgraph "Phase 3: Full Production"
        CE2[CloudEvents SDK]
        JS[JetStream Replay]
        FULL[Full Mosaic]
        CE2 --> JS
        JS --> FULL
    end

    LOCAL --> |"Upgrade ASAP"| NATS2
    HARNESS --> |"When stable"| CE2
```

---

## Elemental Preset System

```mermaid
flowchart TB
    subgraph "MVP: 2 Presets"
        EARTH[☷ Earth<br/>Stable, High Smoothing<br/>minCutoff: 0.5, beta: 0.001]
        THUNDER[☳ Thunder<br/>Responsive, Low Smoothing<br/>minCutoff: 1.5, beta: 0.007]
    end

    subgraph "Future: 8 Presets"
        P0[☷ Earth - Stable]
        P1[☶ Mountain - Precise]
        P2[☵ Water - Flowing]
        P3[☴ Wind - Swift]
        P4[☳ Thunder - Explosive]
        P5[☲ Fire - Aggressive]
        P6[☱ Lake - Calm]
        P7[☰ Heaven - Balanced]
    end

    EARTH --> |"Dwell Select"| SHAPER[Shaper Config]
    THUNDER --> |"Dwell Select"| SHAPER
```

---

## Input Sources

```mermaid
flowchart TB
    subgraph "Live Input"
        CAM[Camera Stream]
        MIRROR[Mirror to TV/Projector]
    end

    subgraph "File Input"
        WEBM[WebM Video]
        MP4[MP4 Video]
        GOLDEN[Golden Master Recording]
    end

    subgraph "Observer"
        OBS[Port 0: Observer]
    end

    CAM --> OBS
    MIRROR --> CAM
    WEBM --> OBS
    MP4 --> OBS
    GOLDEN --> OBS

    note1[/"Future: Gesture Looper for music composition"/]
```

---

## Requirements

### Requirement 0: Cold Start Setup (IDE + Dependencies + Physics Checks)

**User Story:** As a developer, I want a verified development environment with all exemplars tested in isolation, so that I can build with confidence that the foundation is solid.

#### Acceptance Criteria

1. WHEN starting cold start THEN the system SHALL archive existing `src/gesture_ninja/` to `reference/gesture_ninja_archive/`
2. WHEN setting up TypeScript THEN the system SHALL install: @vladmandic/human, @webarkit/oneeurofilter-ts, xstate, cloudevents
3. WHEN setting up Python THEN the system SHALL install: hypothesis, pyribs, pydantic, fast-check (via npm for JS tests)
4. WHEN verifying Human.js THEN the system SHALL confirm hand detection returns 21 keypoints in browser
5. WHEN verifying 1Euro filter THEN the system SHALL confirm smoothing reduces jitter on test data
6. WHEN verifying XState THEN the system SHALL confirm state machine transitions correctly
7. WHEN verifying JSONL THEN the system SHALL confirm round-trip serialization produces equivalent objects
8. WHEN verifying Hypothesis THEN the system SHALL confirm random hand state generation works
9. WHEN verifying pyribs THEN the system SHALL confirm archive accepts fused scores
10. WHEN all physics checks pass THEN the system SHALL emit a READY signal before any glue code is written

### Requirement 1: Ghost Cursor Core (CanonicalIntent Output)

**User Story:** As a developer, I want a trusted pointer output that I can consume in any application, so that I can build spatial computing experiences without dealing with sensor noise.

#### Acceptance Criteria

1. WHEN the Shaper produces output THEN the system SHALL emit a CanonicalIntent with position, velocity, confidence, and armed state
2. WHEN serializing and deserializing CanonicalIntent THEN the round-trip SHALL produce an equivalent object
3. WHEN the Ghost Cursor is consumed by an Injector THEN the Injector SHALL receive position updates at ≥30fps
4. WHEN confidence drops below 0.5 THEN the system SHALL mark the cursor as low-confidence in the output
5. WHEN velocity exceeds 500px/s THEN the system SHALL mark the cursor as "armed" for gesture detection
6. WHEN velocity drops below 100px/s for 100ms THEN the system SHALL mark the cursor as "disarmed"

### Requirement 2: Port 0 Observer (Swappable Sensing)

**User Story:** As a developer, I want to swap between Human.js and MediaPipe without changing downstream code, so that I can choose the best sensor for each device.

#### Human.js Built-in Capabilities (DO NOT REINVENT):
- 21 hand keypoints (palm + 4 per finger)
- Finger curl detection: none, half, full
- Finger direction: verticalUp/Down, horizontalLeft/Right, diagonal variants
- Built-in gestures: thumbsUp, victory, point, middleFinger, openPalm
- Custom gesture definition via FingerGesture class
- Frame interpolation (time-based weighted average)

#### Acceptance Criteria

1. WHEN the Observer adapter is Human.js THEN the system SHALL extract 21 keypoints from HandResult
2. WHEN the Observer adapter is MediaPipe THEN the system SHALL extract 21 keypoints from HandLandmarkerResult
3. WHEN either adapter produces output THEN the format SHALL conform to CanonicalHandState interface
4. WHEN confidence is below 0.7 THEN the Observer SHALL mark the hand as low-confidence
5. WHEN serializing and deserializing CanonicalHandState THEN the round-trip SHALL produce an equivalent object
6. WHEN the Observer produces a hand state THEN the system SHALL publish to the Bridger
7. WHEN Human.js provides finger curl/direction THEN the Observer SHALL pass through without recomputation
8. WHEN Human.js provides gesture recognition THEN the Observer SHALL include gesture in CanonicalHandState

### Requirement 2.5: Multi-Hand Support (2 Hands = 2 Cursors)

**User Story:** As a user, I want to use both hands simultaneously with independent cursors, so that I can interact with the system using natural two-handed gestures.

#### Acceptance Criteria

1. WHEN two hands are detected THEN the system SHALL render two independent cursor elements
2. WHEN each hand is tracked THEN the system SHALL position its cursor above the index finger tip (landmark 8)
3. WHEN left hand is detected THEN the system SHALL render a cursor with distinct visual style (e.g., blue tint)
4. WHEN right hand is detected THEN the system SHALL render a cursor with distinct visual style (e.g., purple tint)
5. WHEN one hand is lost THEN the system SHALL continue tracking the remaining hand independently
6. WHEN both hands are lost THEN the system SHALL apply coasting to both cursors independently
7. WHEN serializing multi-hand state THEN the round-trip SHALL preserve both hand states correctly
8. WHEN the Observer detects hands THEN the system SHALL return an array of CanonicalHandState (up to maxDetected)

### Requirement 3: Port 1 Bridger (Contract Boundary + Telemetry)

**User Story:** As a developer, I want all inter-port communication to go through a contract boundary with trace context, so that I can debug, replay, and evolve the system without breaking changes.

#### Acceptance Criteria

1. WHEN an event crosses a port boundary THEN the Bridger SHALL wrap it in a CloudEvents envelope with specversion, type, source, id, time, and data
2. WHEN an event is published THEN the Bridger SHALL attach W3C Trace Context (traceparent) for distributed tracing
3. WHEN the event schema changes THEN the Bridger SHALL include a schema version field for evolution
4. WHEN NATS is unavailable THEN the Bridger SHALL buffer events locally and retry with exponential backoff
5. WHEN the Bridger receives an event THEN the system SHALL validate required fields before processing
6. WHEN validation fails THEN the Bridger SHALL reject the event and emit an error span

### Requirement 4: Port 2 Shaper (Predictive Latency Engine)

**User Story:** As a developer, I want a filter pipeline that converts noisy sensor data into reliable intent with negative perceived latency, so that the cursor feels instant despite processing delays.

#### Exemplar Stack:
- 1Euro Filter: @webarkit/oneeurofilter-ts (npm) - velocity-adaptive smoothing
- Kalman Filter: Custom ~50 lines - prediction for negative latency
- State Machine: XState (npm) - IDLE→TRACKING→ARMED→DISARMED→COASTING
- Human.js interpolation: Use alongside 1Euro for frame smoothing

#### Acceptance Criteria

1. WHEN the Shaper receives CanonicalHandState THEN the system SHALL apply 1Euro filtering via @webarkit/oneeurofilter-ts
2. WHEN 1Euro filter smooths position THEN the system SHALL adapt cutoff based on velocity (smooth when slow, responsive when fast)
3. WHEN tracking is lost for less than 500ms THEN the system SHALL apply inertial coasting instead of cursor disappearance
4. WHEN tracking is reacquired THEN the system SHALL apply magnetic snap (LERP over 100ms) to prevent teleportation
5. WHEN cursor position jumps more than 100px in one frame THEN the system SHALL blend with previous position (teleport rejection)
6. WHEN the cursor is disarmed THEN the system SHALL NOT emit gesture events (state machine gating via XState)
7. WHEN confidence drops below 0.5 THEN the system SHALL disarm the cursor regardless of velocity
8. WHEN printing and parsing a Shaper configuration THEN the round-trip SHALL produce an equivalent configuration
9. WHEN Human.js provides frame interpolation THEN the Shaper MAY use it in addition to 1Euro for smoother output

### Requirement 5: Port 3 Injector (Consumer Interface)

**User Story:** As a game developer, I want a stable interface to consume Ghost Cursor output, so that I can build gesture-controlled games without coupling to the cursor implementation.

#### Acceptance Criteria

1. WHEN an Injector subscribes to Ghost Cursor THEN the system SHALL provide CanonicalIntent events via callback or stream
2. WHEN CanonicalIntent includes armed=true THEN the Injector MAY interpret fast movement as a gesture
3. WHEN CanonicalIntent includes armed=false THEN the Injector SHALL NOT trigger gesture actions
4. WHEN the Injector needs position THEN the system SHALL provide screen-space coordinates (pixels)
5. WHEN the Injector needs velocity THEN the system SHALL provide velocity vector (px/s)

### Requirement 6: Port 4 Disruptor (Chaos Testing)

**User Story:** As a developer, I want adversarial testing that finds edge cases I wouldn't think of, so that the system is robust before adding new tech.

#### Acceptance Criteria

1. WHEN running property tests THEN the Disruptor SHALL generate random hand states using polymorphic PBT adapters (Hypothesis for Python, fast-check for TypeScript)
2. WHEN running fuzz tests THEN the Disruptor SHALL inject corrupted events (missing fields, invalid values)
3. WHEN running chaos tests THEN the Disruptor SHALL simulate tracking loss, jitter spikes, and latency
4. WHEN a property test fails THEN the Disruptor SHALL report the minimal failing example
5. WHEN the system is under chaos THEN the Shaper SHALL maintain safety invariants (no false activations)
6. WHEN adding a new PBT adapter THEN the system SHALL require only implementing the TestStrategy interface
7. WHEN test results are produced THEN the system SHALL serialize to JSONL for cross-language comparison

### Requirement 7: Port 5 Immunizer (Validation + Regression Guards)

**User Story:** As a developer, I want invariant checks and regression guards that catch violations before they cause harm, so that the system fails safely and new tech doesn't break existing behavior.

#### Acceptance Criteria

1. WHEN a CanonicalHandState is produced THEN the Immunizer SHALL validate all required fields are present
2. WHEN confidence is outside [0, 1] THEN the Immunizer SHALL reject the event and emit an anomaly span
3. WHEN velocity exceeds physically plausible limits (>2000px/s) THEN the Immunizer SHALL flag as anomaly
4. WHEN the cursor is disarmed THEN the Immunizer SHALL verify no gesture events are emitted (invariant)
5. WHEN a new exemplar is added THEN the Immunizer SHALL run regression tests against golden masters
6. WHEN regression tests fail THEN the Immunizer SHALL block the change and report the delta

### Requirement 8: Port 6 Assimilator (Replay + Score Fusion)

**User Story:** As a developer, I want to record sessions, replay them deterministically, and compute fused scores for Pareto optimization, so that I can measure improvements and explore the design space.

#### Acceptance Criteria

1. WHEN a session starts THEN the Assimilator SHALL begin recording all events to JSONL with monotonic timestamps
2. WHEN a session ends THEN the Assimilator SHALL auto-save the replay to local storage
3. WHEN a replay is loaded THEN the Assimilator SHALL feed events to the Shaper in recorded order
4. WHEN replaying THEN the Shaper SHALL produce the same output sequence within tolerance (determinism)
5. WHEN computing metrics THEN the Assimilator SHALL measure latency, jitter, false activations, tracking recovery, and round-trip fidelity
6. WHEN fusing scores THEN the Assimilator SHALL normalize each metric to [0,1] and apply configurable weights
7. WHEN a golden baseline exists THEN the system SHALL compare actual vs expected and report regressions

### Requirement 9: Port 7 Navigator (DSE + Pareto Optimization)

**User Story:** As a developer, I want the system to explore the design space and optimize toward the Pareto frontier, so that it improves as new exemplars become commoditized.

#### Acceptance Criteria

1. WHEN replay data is available THEN the Navigator SHALL compute fused scores for the QD archive
2. WHEN scores are computed THEN the Navigator SHALL store them in the pyribs MAP-Elites archive
3. WHEN optimizing THEN the Navigator SHALL use MCTS to explore parameter space (filter cutoffs, thresholds)
4. WHEN a better parameter set is found THEN the Navigator SHALL propose it as a new preset
5. WHEN evaluating alternatives THEN the Navigator SHALL perform AoA trade analysis with TRL, integration effort, and test coverage
6. WHEN score fusion weights are needed THEN the Navigator SHALL load them from configurable YAML (default: equal weights)
7. WHEN genetic programming is enabled THEN the Navigator SHALL evolve optimal weight configurations via QD archive
8. WHEN printing and parsing score fusion configuration THEN the round-trip SHALL produce an equivalent configuration

### Requirement 10: Dwell/Hover Click Interaction

**User Story:** As a user, I want to activate UI elements by hovering over them for a set time, so that I can interact without needing a physical click gesture.

#### Acceptance Criteria

1. WHEN the cursor enters a target hitbox THEN the system SHALL start a dwell timer
2. WHEN the cursor remains in the hitbox for dwell_time (default 500ms) THEN the system SHALL trigger the activation
3. WHEN the cursor exits the hitbox before dwell_time THEN the system SHALL reset the timer
4. WHEN activation occurs THEN the system SHALL enter cooldown to prevent double-activation
5. WHEN dwelling THEN the system SHALL provide visual feedback (progress indicator)

### Requirement 10.5: Pinch Click Interaction (Thumb-to-Index)

**User Story:** As a user, I want to click by pinching my thumb and index finger together, so that I have an alternative to dwell clicking for faster interactions.

#### Gesture Pattern (Adopted from NonMouse):
- Click: Thumb tip touches index finger second joint
- Release: Thumb and index finger separate
- Double-click: Two pinches within 500ms

#### Acceptance Criteria

1. WHEN thumb tip approaches index finger second joint (distance < threshold) THEN the system SHALL trigger a click event
2. WHEN thumb and index finger separate (distance > threshold) THEN the system SHALL trigger a release event
3. WHEN two click events occur within 500ms THEN the system SHALL emit a double-click event
4. WHEN pinch click is detected THEN the system SHALL provide visual feedback (color change on cursor)
5. WHEN pinch click mode is active THEN the system SHALL disable dwell clicking to prevent conflicts
6. WHEN the user configures interaction mode THEN the system SHALL allow switching between dwell and pinch modes
7. WHEN Human.js provides finger curl/direction THEN the system SHALL use it to detect pinch gesture

### Requirement 10.6: Scroll Gesture (Index Finger Curl)

**User Story:** As a user, I want to scroll by curling my index finger, so that I can navigate content without switching interaction modes.

#### Gesture Pattern (Adopted from NonMouse):
- Scroll mode: Index finger curled (half or full curl)
- Scroll direction: Hand movement up/down while in scroll mode
- Exit scroll: Index finger extended

#### Acceptance Criteria

1. WHEN index finger curl is detected (half or full) THEN the system SHALL enter scroll mode
2. WHEN in scroll mode AND hand moves up THEN the system SHALL emit scroll-up events
3. WHEN in scroll mode AND hand moves down THEN the system SHALL emit scroll-down events
4. WHEN index finger extends (no curl) THEN the system SHALL exit scroll mode
5. WHEN in scroll mode THEN the system SHALL provide visual feedback (scroll indicator)
6. WHEN scroll mode is active THEN the system SHALL pause cursor movement
7. WHEN Human.js provides finger curl detection THEN the system SHALL use it for scroll gesture

### Requirement 11: Play Area and Gain Controls

**User Story:** As a user, I want to configure the active region and sensitivity of the cursor, so that I can use the system comfortably in different physical setups.

#### Acceptance Criteria

1. WHEN configuring play area THEN the system SHALL allow defining bounds within the camera view
2. WHEN the hand is outside play area THEN the system SHALL clamp cursor to screen edges
3. WHEN gain is configured THEN the system SHALL scale cursor movement (1.0 = 1:1, >1 = amplified)
4. WHEN deadzone is configured THEN the system SHALL ignore movements below the threshold
5. WHEN printing and parsing gain configuration THEN the round-trip SHALL produce an equivalent configuration

### Requirement 12: Ghost Cursor Presets (Elemental Styles)

**User Story:** As a user, I want to choose between different cursor behavior presets, so that I can pick the style that feels best for my use case.

#### Acceptance Criteria

1. WHEN the system starts THEN the system SHALL offer 2 presets: Earth (stable, high smoothing) and Thunder (responsive, low smoothing)
2. WHEN a preset is selected THEN the Shaper SHALL apply that preset's filter parameters (1Euro cutoffs, arm/disarm thresholds)
3. WHEN switching presets THEN the system SHALL log the change to the replay stream
4. WHEN a preset is active THEN the cursor visual style SHALL reflect the element (color, trail effect)
5. WHEN the system evolves THEN the system SHALL support up to 8 elemental presets with custom tuning

### Requirement 13: Video Input Mode (Replay from File)

**User Story:** As a developer, I want to load a video file (webm/mp4) instead of live camera, so that I can test and debug without needing a live hand.

#### Acceptance Criteria

1. WHEN a video file is loaded THEN the Observer SHALL process frames from the video instead of camera
2. WHEN processing video THEN the system SHALL maintain the same pipeline (Observer → Bridger → Shaper → Injector)
3. WHEN video playback ends THEN the system SHALL emit an end-of-stream event
4. WHEN video is paused THEN the system SHALL pause event emission
5. WHEN video is seeked THEN the system SHALL reset state machine and resume from new position

### Requirement 14: User Environment Prompting

**User Story:** As a user, I want guidance on setting up my environment, so that I can get the best tracking quality.

#### Acceptance Criteria

1. WHEN the system starts THEN the system SHALL prompt user to ensure clean background and good lighting
2. WHEN tracking quality is poor THEN the system SHALL suggest environment improvements
3. WHEN confidence is consistently low THEN the system SHALL offer to switch to a more robust preset
4. WHEN the user dismisses prompts THEN the system SHALL remember the preference

### Requirement 14.5: Multiple Camera Placement Modes

**User Story:** As a user, I want to choose how my camera is positioned relative to my hand, so that I can use the system in different physical setups.

#### Camera Placement Options (Adopted from NonMouse):
- **Normal**: Camera facing user (laptop webcam, standard setup)
- **Above**: Camera pointing down at hands on desk (overhead mount)
- **Behind**: Camera behind user pointing at display (AR/projection setup)

#### Acceptance Criteria

1. WHEN the system starts THEN the system SHALL offer camera placement selection: Normal, Above, or Behind
2. WHEN Normal placement is selected THEN the system SHALL expect hand in front of camera (standard webcam)
3. WHEN Above placement is selected THEN the system SHALL expect hand below camera (overhead view)
4. WHEN Behind placement is selected THEN the system SHALL expect hand between camera and display
5. WHEN camera placement changes THEN the system SHALL adjust coordinate mapping accordingly
6. WHEN printing and parsing camera placement configuration THEN the round-trip SHALL produce an equivalent configuration
7. WHEN the user selects a placement THEN the system SHALL persist the preference
8. WHEN Above placement is active THEN the system SHALL invert Y-axis for natural cursor movement

### Requirement 15: Adaptive Thresholds (Zero Magic Numbers)

**User Story:** As a developer, I want all thresholds to be adaptive and configurable, so that the system works across different screen sizes, camera setups, and user preferences without hardcoded constants.

#### Acceptance Criteria

1. WHEN a threshold is defined THEN the system SHALL express it as a ratio of available space (not absolute pixels)
2. WHEN arm_threshold is needed THEN the system SHALL compute it as a percentage of screen diagonal per second
3. WHEN disarm_threshold is needed THEN the system SHALL compute it as a percentage of screen diagonal per second
4. WHEN play_area bounds are needed THEN the system SHALL express them as normalized coordinates [0,1]
5. WHEN a magic number is detected in code THEN the Immunizer SHALL reject the change and require configuration
6. WHEN thresholds are loaded THEN the system SHALL validate ranges and emit warnings for extreme values
7. WHEN printing and parsing threshold configuration THEN the round-trip SHALL produce an equivalent configuration
8. WHEN the user tunes thresholds THEN the system SHALL persist preferences and log changes to replay stream

### Requirement 16: Polymorphic Adapter Architecture

**User Story:** As a developer, I want every port boundary to use swappable adapters, so that I am never locked into a vendor, language, or format.

#### Acceptance Criteria

1. WHEN an Observer adapter is added THEN the system SHALL require only implementing the ObserverPort interface
2. WHEN a Bridger transport is added THEN the system SHALL require only implementing the BridgerPort interface
3. WHEN a Shaper filter is added THEN the system SHALL require only implementing the FilterPort interface
4. WHEN an Injector consumer is added THEN the system SHALL require only implementing the InjectorPort interface
5. WHEN a Disruptor test strategy is added THEN the system SHALL require only implementing the TestStrategyPort interface
6. WHEN an Assimilator storage is added THEN the system SHALL require only implementing the StoragePort interface
7. WHEN cross-language communication is needed THEN the system SHALL use JSONL as the interchange format
8. WHEN printing and parsing port configuration THEN the round-trip SHALL produce an equivalent configuration

### Requirement 17: Exemplar Composition Workflow

**User Story:** As a developer, I want a systematic workflow for discovering, wrapping, and grading exemplars, so that I can assemble mosaic tiles with confidence.

#### Acceptance Criteria

1. WHEN a new problem class is identified THEN the system SHALL search for exemplars via web search
2. WHEN an exemplar is found THEN the system SHALL record it with TRL, source, and integration notes
3. WHEN an exemplar is wrapped via strangler fig THEN the system SHALL run physics checks before integration
4. WHEN an exemplar is tested THEN the system SHALL compute a fused score and update the grade
5. WHEN the matrix is queried THEN the system SHALL return all exemplars for a given problem class sorted by score

### Requirement 18: MCP Wrapper Architecture (Exemplar Isolation)

**User Story:** As a developer, I want each exemplar wrapped as an MCP tool, so that I can test, swap, and monitor components independently.

#### Acceptance Criteria

1. WHEN Human.js is used THEN the system SHALL expose it via mcp-human-js wrapper with detect, gesture, and fingerpose tools
2. WHEN 1Euro filter is used THEN the system SHALL expose it via mcp-1euro wrapper with smooth and configure tools
3. WHEN XState is used THEN the system SHALL expose it via mcp-xstate wrapper with transition and getState tools
4. WHEN JSONL replay is used THEN the system SHALL expose it via mcp-jsonl wrapper with record, playback, and compare tools
5. WHEN score fusion is computed THEN the system SHALL expose it via mcp-score-fusion wrapper with compute and configure tools
6. WHEN an MCP wrapper is called THEN the system SHALL log the call to the Assimilator for replay
7. WHEN swapping an exemplar THEN the system SHALL require only changing the MCP wrapper configuration
8. WHEN testing in isolation THEN the system SHALL allow calling any MCP wrapper without the full pipeline

---

## Non-Functional Requirements

### NFR-1: Performance (Target: Mid-Range Smartphone)

1. WHEN running on mid-range smartphone (3rd world market) THEN the system SHALL maintain ≥30fps for gesture processing
2. WHEN running on target device THEN the system SHALL keep p95 input→output latency ≤100ms
3. WHEN mirroring to TV/projector THEN the system SHALL maintain ≥30fps with acceptable latency
4. WHEN running on-device (no mirror) THEN the system SHALL maintain ≥30fps

### NFR-2: Reliability

1. WHEN tracking is lost THEN the system SHALL apply coasting for ≤500ms before marking as lost
2. WHEN NATS connection is lost THEN the system SHALL buffer events and reconnect automatically

### NFR-3: Evolvability

1. WHEN adding a new Observer adapter THEN the system SHALL require only implementing the CanonicalHandState interface
2. WHEN adding a new Injector consumer THEN the system SHALL require only consuming CanonicalIntent
3. WHEN adding a new exemplar THEN the system SHALL require passing regression guards before merge

### NFR-4: Anti-Hallucination

1. WHEN claiming completion THEN the system SHALL show executable test output as proof
2. WHEN adding new tech THEN the system SHALL pass physics checks and regression guards first
3. WHEN searching for exemplars THEN the system SHALL verify source exists via web fetch

---

*Gen 76 | HFO Mosaic Ghost Cursor | Capacity Engineering Platform | Phoenix Protocol Cold Start | 2025-12-17*


---

## NEW REQUIREMENTS (Gen 77.1 - Test Harness Integrity)

### Requirement 16: Test Harness Integrity (RED-GREEN-REFACTOR)

**User Story:** As a developer, I want tests that can fail (RED) when given bad input, so that I can trust GREEN means correct and avoid reward hacking.

#### Acceptance Criteria

1. WHEN invalid CanonicalHandState (< 21 landmarks) is fed to Shaper THEN the system SHALL reject with validation error
2. WHEN CanonicalIntent has confidence > 1 THEN isValidIntent() SHALL return false
3. WHEN CanonicalIntent has confidence < 0 THEN isValidIntent() SHALL return false
4. WHEN CanonicalHandState has invalid handId (not 'left' or 'right') THEN isValidHandState() SHALL return false
5. WHEN golden JSONL is replayed THEN output SHALL match expected JSONL within tolerance
6. WHEN output differs from expected THEN test SHALL fail with diff report (RED)
7. WHEN output matches expected THEN test SHALL pass (GREEN)

### Requirement 17: JSONL Recording (Port 6 Assimilator Implementation)

**User Story:** As a tester, I want to record all pipeline events to JSONL, so that I can replay and verify deterministic behavior.

#### JSONL Schema:
```jsonl
{"type":"metadata","timestamp":0,"video_path":"...","config_hash":"..."}
{"type":"hand","timestamp":123,"handId":"left","landmarks":[...],"fingerCurl":{...},"confidence":0.9}
{"type":"intent","timestamp":124,"handId":"left","position":{"x":400,"y":300},"armed":true,"state":"ARMED"}
```

#### Acceptance Criteria

1. WHEN a hand is detected THEN the system SHALL append a hand event to JSONL with all CanonicalHandState fields
2. WHEN Shaper produces intent THEN the system SHALL append an intent event to JSONL with all CanonicalIntent fields
3. WHEN session starts THEN the system SHALL write a metadata event with video path and config hash
4. WHEN session ends THEN the system SHALL save JSONL to file (download or local storage)
5. WHEN JSONL is replayed THEN output SHALL be identical to original recording (deterministic)
6. WHEN timestamps are recorded THEN they SHALL be monotonically increasing

### Requirement 18: Deterministic Pong Paddle Mapping

**User Story:** As a game developer, I want to map ghost cursor to Pong paddles deterministically, so that I can test 2-player hand tracking with golden video.

#### Acceptance Criteria

1. WHEN left hand is detected THEN left paddle Y SHALL equal intent.position.y (clamped to game bounds)
2. WHEN right hand is detected THEN right paddle Y SHALL equal intent.position.y (clamped to game bounds)
3. WHEN intent.armed=true THEN paddle SHALL be able to hit ball (collision enabled)
4. WHEN intent.armed=false THEN paddle SHALL pass through ball (collision disabled)
5. WHEN golden video is processed THEN paddle positions SHALL match expected trajectory within tolerance
6. WHEN paddle trajectory differs from expected THEN test SHALL fail with position diff (RED)

### Requirement 19: Property-Based Test Invariants

**User Story:** As a developer, I want property-based tests that verify invariants hold for all valid inputs, so that I can catch edge cases I wouldn't think of.

#### Invariants to Test:

1. **Position Bounds**: For any valid handState, Shaper output position.x SHALL be in [0, screenWidth]
2. **Position Bounds**: For any valid handState, Shaper output position.y SHALL be in [0, screenHeight]
3. **Confidence Bounds**: For any Shaper output, confidence SHALL be in [0, 1]
4. **State Validity**: For any Shaper output, state SHALL be one of IDLE, TRACKING, ARMED, DISARMED, COASTING
5. **Armed Consistency**: WHEN state=ARMED THEN armed SHALL be true
6. **Disarmed Consistency**: WHEN state=DISARMED THEN armed SHALL be false
7. **Round-Trip**: For any valid CanonicalIntent, serialize then deserialize SHALL produce equivalent object

#### Acceptance Criteria

1. WHEN fast-check generates random valid handState THEN Shaper output SHALL satisfy all invariants
2. WHEN an invariant is violated THEN fast-check SHALL report minimal failing example
3. WHEN all invariants pass THEN property test SHALL pass (GREEN)
4. WHEN any invariant fails THEN property test SHALL fail (RED) with counterexample

---

*Added: 2025-12-19 | Gen 77.1 | Test Harness Integrity Requirements*


---

## NEW REQUIREMENTS (Gen 77.3 - Clutch Behavior Model)

### Requirement 20: Always-On Hand Tracking

**User Story:** As a user, I want to always see where my hand is being tracked, so that I have visual feedback even when fingers are disarmed.

#### Acceptance Criteria

1. WHEN a hand is detected THEN the system SHALL render a cursor at the hand position
2. WHEN hand is in TRACKING state THEN the cursor SHALL follow the hand continuously
3. WHEN hand transitions to COASTING THEN the system SHALL continue cursor movement with inertia
4. WHEN hand is reacquired after COASTING THEN the system SHALL smoothly blend to new position
5. WHEN serializing hand state THEN the round-trip SHALL preserve tracking/coasting distinction
6. WHEN hand tracking is lost THEN the system SHALL preserve all finger armed states

### Requirement 21: Per-Finger Armed/Disarmed State with Hysteresis

**User Story:** As a user, I want each finger to independently arm/disarm with hysteresis, so that I have precise control without thrashing between states.

#### Acceptance Criteria

1. WHEN finger curl < arm_threshold (0.2) for arm_delay (50ms) THEN the finger SHALL transition to ARMED
2. WHEN finger curl > disarm_threshold (0.6) for disarm_delay (50ms) THEN the finger SHALL transition to DISARMED
3. WHEN finger curl is between arm_threshold and disarm_threshold THEN the finger SHALL maintain current state (hysteresis dead zone)
4. WHEN finger is ARMED THEN the target associated with that finger SHALL move with cursor
5. WHEN finger is DISARMED THEN the target SHALL freeze at last armed position
6. WHEN hand enters COASTING THEN all finger armed states SHALL be preserved
7. WHEN hand is reacquired THEN finger states SHALL resume from preserved values
8. WHEN serializing finger state THEN the round-trip SHALL preserve armed/disarmed per finger

#### Hysteresis Configuration

| Parameter | Default | Description |
|:----------|:--------|:------------|
| arm_threshold | 0.2 | Curl value below which finger arms (very straight) |
| disarm_threshold | 0.6 | Curl value above which finger disarms (clearly curled) |
| arm_delay | 50ms | Time curl must be below threshold to arm |
| disarm_delay | 50ms | Time curl must be above threshold to disarm |
| dead_zone | 0.2-0.6 | Range where no state change occurs |

### Requirement 22: Inertial Coasting with State Preservation

**User Story:** As a user, I want the system to continue smoothly when tracking is lost and preserve my finger states, so that brief tracking interruptions don't reset my control state.

#### Acceptance Criteria

1. WHEN hand tracking is lost THEN the system SHALL enter COASTING state
2. WHEN in COASTING THEN the cursor SHALL continue moving with last known velocity (inertial physics)
3. WHEN in COASTING THEN all finger armed states SHALL be preserved exactly
4. WHEN COASTING exceeds coast_timeout (500ms) THEN the system SHALL transition to IDLE
5. WHEN hand is reacquired during COASTING THEN the system SHALL blend to new position over 100ms
6. WHEN hand is reacquired THEN finger states SHALL resume from preserved values (no reset)
7. WHEN serializing coasting state THEN the round-trip SHALL preserve velocity, position, and all finger states

#### Inertia Physics

| Parameter | Default | Description |
|:----------|:--------|:------------|
| coast_timeout | 500ms | Maximum coasting duration before IDLE |
| velocity_decay | 0.95 | Per-frame velocity multiplier during coast |
| blend_duration | 100ms | Time to blend from coast position to reacquired position |
| min_velocity | 10px/s | Velocity below which coasting stops early |

### Requirement 23: Elemental Cursor Transformation

**User Story:** As a user, I want the cursor to visually transform when I arm a finger, so that I have clear feedback about my control state.

#### Acceptance Criteria

1. WHEN a finger transitions to ARMED THEN that finger's cursor SHALL transform to elemental appearance
2. WHEN a finger is ARMED THEN the cursor SHALL display the active element (fire, water, earth, etc.)
3. WHEN a finger transitions to DISARMED THEN the cursor SHALL return to ghost appearance
4. WHEN the user selects an element preset THEN the system SHALL apply that element's visual style
5. WHEN rendering elemental cursor THEN the system SHALL use distinct color/animation per element
6. WHEN multiple fingers are armed THEN each SHALL show its own elemental cursor
7. WHEN serializing cursor state THEN the round-trip SHALL preserve the element selection per finger

#### Elemental Presets (MVP: 2, Future: 8)

| Element | Trigram | Color | Behavior |
|:--------|:--------|:------|:---------|
| Fire ☲ | Li | Orange/Red | Aggressive, low smoothing |
| Water ☵ | Kan | Blue/Cyan | Flowing, high smoothing |
| Earth ☷ | Kun | Brown/Green | Stable, maximum smoothing |
| Thunder ☳ | Zhen | Yellow/Purple | Explosive, minimal smoothing |

### Requirement 24: CanonicalFingerCurl from Smoothed Landmarks

**User Story:** As a developer, I want to compute finger curl from smoothed landmark positions rather than relying solely on Human.js discrete values, so that I have continuous, noise-resistant curl detection.

#### Acceptance Criteria

1. WHEN computing finger curl THEN the system SHALL use smoothed landmark positions (after 1Euro filter)
2. WHEN Human.js provides curl values (none/half/full) THEN the system SHALL treat them as a DATA SOURCE, not ground truth
3. WHEN computing CanonicalFingerCurl THEN the system SHALL calculate angle between finger segments (MCP→PIP→DIP→TIP)
4. WHEN landmarks are smoothed THEN the computed curl SHALL be more stable than raw Human.js values
5. WHEN both Human.js curl and computed curl are available THEN the system SHALL fuse them with configurable weights
6. WHEN serializing CanonicalFingerCurl THEN the round-trip SHALL preserve both raw and computed values

#### Finger Curl Geometry

```
For each finger:
  MCP (knuckle) → PIP (first joint) → DIP (second joint) → TIP

Curl angle = angle at PIP joint
  - 180° = fully extended (curl = 0.0)
  - 90° = half curled (curl = 0.5)
  - 45° = fully curled (curl = 1.0)

Formula:
  curl = 1.0 - (angle - 45) / 135
  clamped to [0, 1]
```

#### CanonicalFingerCurl Interface

```typescript
interface CanonicalFingerCurl {
  // Raw Human.js value (data source)
  humanJsValue: 'none' | 'half' | 'full';

  // Computed from smoothed landmarks (continuous)
  computedValue: number;  // 0-1

  // Fused value (weighted combination)
  fusedValue: number;  // 0-1

  // Confidence in the measurement
  confidence: number;  // 0-1

  // Which source was used for final value
  source: 'humanjs' | 'computed' | 'fused';
}
```

### Requirement 25: Advanced Finger Curl Detection Pipeline

**User Story:** As a developer, I want robust finger curl detection that handles noise, prediction, and biomechanics, so that the clutch mechanism feels responsive and reliable.

#### Acceptance Criteria

1. WHEN processing finger curl THEN the system SHALL apply 1Euro filter to computed curl values
2. WHEN predicting curl state THEN the system SHALL use Kalman filter for look-ahead prediction (negative latency)
3. WHEN weighting curl confidence THEN the system SHALL apply biomechanics factors per finger
4. WHEN curl state is noisy THEN the system SHALL use temporal inertia (5-frame majority vote)
5. WHEN Human.js provides curl values THEN the system SHALL use them as secondary data source
6. WHEN curl approaches threshold THEN the system SHALL apply hysteresis band (see Req 21)
7. WHEN Kalman predicts threshold crossing THEN the system SHALL pre-arm/pre-disarm for responsiveness

#### Finger Curl Processing Pipeline

```
Smoothed Landmarks → Compute Angle → CanonicalFingerCurl
                                           ↓
Human.js Curl ──────────────────────→ Fuse Sources
                                           ↓
                              1Euro Filter → Kalman Predict → Hysteresis → State
                                                   ↓
                                         Biomechanics Weight
```

#### Biomechanics Weighting

| Finger | Curl Speed | Curl Range | Weight | Notes |
|:-------|:-----------|:-----------|:-------|:------|
| Index | Fast | Full (0-1) | 1.0 | Primary control finger |
| Middle | Fast | Full (0-1) | 0.9 | Secondary control |
| Ring | Medium | Partial (0-0.8) | 0.7 | Coupled to middle |
| Pinky | Slow | Limited (0-0.6) | 0.5 | Least independent |
| Thumb | Variable | Rotation | 0.8 | Used for pinch/modifier |

### Requirement 26: Multi-Finger Cursor System (Future)

**User Story:** As a power user, I want to control multiple cursors per hand using different fingers, so that I can interact with complex interfaces more efficiently.

#### Acceptance Criteria

1. WHEN multi-finger mode is enabled THEN the system SHALL track up to 4 cursors per hand
2. WHEN a finger is straight THEN the system SHALL project a ray from that fingertip
3. WHEN multiple fingers are straight THEN the system SHALL render independent cursors per finger
4. WHEN configuring gain THEN the system SHALL allow per-finger gain adjustment
5. WHEN fingers have different curl states THEN the system SHALL arm/disarm cursors independently
6. WHEN serializing multi-finger state THEN the round-trip SHALL preserve all finger cursor states

#### Ray Casting Model

```
Index Finger → Primary cursor (always available)
Middle Finger → Secondary cursor (optional)
Ring Finger → Tertiary cursor (optional)
Pinky Finger → Quaternary cursor (optional)
Thumb → Modifier (pinch, scroll, etc.)
```

---

## Hierarchical State Model (Gen 77.3)

```
HAND LEVEL (tracking)
├── IDLE: No hand detected
├── TRACKING: Hand visible, cursor follows
└── COASTING: Hand lost, inertial continuation

FINGER LEVEL (per finger, independent)
├── ARMED: Finger straight (curl < arm_threshold)
│   └── Target MOVES with this finger's cursor
└── DISARMED: Finger curled (curl > disarm_threshold)
    └── Target FROZEN at last armed position
```

**Key Insight**: Hand tracking and finger armed state are ORTHOGONAL.
- Hand can be TRACKING while finger is DISARMED (ghost cursor visible, target frozen)
- Hand can be COASTING while finger was ARMED (inertia continues, preserves armed state)

---

## Pong Demo Behavior (Gen 77.3)

```
Hand TRACKING + Finger DISARMED:
- Ghost cursor visible at hand position
- Paddle FROZEN at last armed position
- Visual: Semi-transparent cursor

Hand TRACKING + Finger ARMED:
- Elemental cursor visible at hand position
- Paddle MOVES with cursor Y position
- Visual: Fire/Water/etc. cursor with glow

Hand COASTING (any finger state):
- Cursor continues with inertia
- Paddle state preserved (moving if was armed, frozen if was disarmed)
- Finger states preserved for when tracking resumes

Transitions:
- Straighten index finger (curl < 0.2 for 50ms) → ARMED (paddle follows)
- Curl index finger (curl > 0.6 for 50ms) → DISARMED (paddle freezes)
- Tracking lost → COASTING (inertia + preserve states)
- Tracking reacquired → Resume with preserved finger states
```

### State Combinations

| Hand State | Finger State | Cursor | Target |
|:-----------|:-------------|:-------|:-------|
| TRACKING | ARMED | Elemental, follows hand | Moves with cursor |
| TRACKING | DISARMED | Ghost, follows hand | Frozen |
| COASTING | ARMED (preserved) | Elemental, inertia | Continues moving with inertia |
| COASTING | DISARMED (preserved) | Ghost, inertia | Frozen |
| IDLE | N/A | Not visible | Frozen |

---

*Added: 2025-12-19 | Gen 77.3 | Clutch Behavior Model Requirements*


---

## NEW REQUIREMENTS (Gen 77.4 - Spatial Zones + Key Events + Pseudo-Z)

### Requirement 27: Spatial 3D Hitbox Zones

**User Story:** As a user, I want the interaction space divided into configurable 3D hitbox zones (x, y, z), so that finger state changes in different spatial volumes can trigger different actions.

**Mosaic Warfare Principle:** Zones are hitboxes that adapt to available sensors. With monocamera, Z is pseudo-depth from handspan. With depth camera, Z is real depth. The zone system is sensor-agnostic.

#### Acceptance Criteria

1. WHEN the system initializes THEN the system SHALL define a default zone covering the entire interaction volume
2. WHEN zones are configured THEN the system SHALL support 3D box definitions with normalized coordinates [0,1] for x, y, and z
3. WHEN a cursor enters a zone (x, y, z all within bounds) THEN the system SHALL emit a zone_enter event with zone_id
4. WHEN a cursor exits a zone THEN the system SHALL emit a zone_exit event with zone_id
5. WHEN multiple zones overlap THEN the system SHALL report all active zones for the cursor position
6. WHEN Z depth is unavailable THEN the system SHALL treat z bounds as always-matching (2D fallback)
7. WHEN zones are updated THEN the system SHALL persist zone configuration
8. WHEN serializing zone configuration THEN the round-trip SHALL produce an equivalent configuration

#### Zone Configuration

```typescript
interface SpatialZone3D {
  id: string;                    // Unique zone identifier
  bounds: {
    x: number;                   // 0-1 normalized left edge
    y: number;                   // 0-1 normalized top edge
    z: number;                   // 0-1 normalized near edge (0=far, 1=near)
    width: number;               // 0-1 normalized width
    height: number;              // 0-1 normalized height
    depth: number;               // 0-1 normalized depth (z extent)
  };
  layer: number;                 // Priority for overlapping zones (higher = on top)
  actions: ZoneAction[];         // Actions triggered by events in this zone
  enabled: boolean;              // Zone active/inactive

  // Interaction modes (mission-fit)
  interactionMode: 'dwell' | 'push' | 'pinch' | 'curl' | 'any';
}
```

#### Mission-Fit Sensor Adaptation

| Sensor Config | X,Y Source | Z Source | Precision |
|:--------------|:-----------|:---------|:----------|
| Monocamera only | Human.js landmarks | Handspan pseudo-Z | ~3 zones (NEAR/NEUTRAL/FAR) |
| Monocamera + calibration | Human.js landmarks | Calibrated handspan | ~5 zones |
| Depth camera | Depth + RGB fusion | Real depth (mm) | Continuous |
| Stereo cameras | Triangulation | Stereo depth | mm-level |
| Full 6DOF | Sensor fusion | Kalman-fused | mm-level + orientation |
```

### Requirement 28: Finger State Change as Key Press

**User Story:** As a user, I want finger curl/uncurl transitions to emit key press events, so that I can use hand gestures as keyboard input.

#### Acceptance Criteria

1. WHEN a finger transitions from ARMED to DISARMED (curl) THEN the system SHALL emit a key_down event
2. WHEN a finger transitions from DISARMED to ARMED (uncurl) THEN the system SHALL emit a key_up event
3. WHEN key_down occurs in a spatial zone THEN the event SHALL include zone_id and mapped key code
4. WHEN configuring key mappings THEN the system SHALL allow per-zone, per-finger key assignments
5. WHEN multiple fingers change state simultaneously THEN the system SHALL emit events for each finger
6. WHEN key events are emitted THEN the system SHALL include timestamp, hand_id, finger_id, zone_id, and key_code
7. WHEN serializing key event configuration THEN the round-trip SHALL produce an equivalent configuration

#### Key Event Interface

```typescript
interface GestureKeyEvent {
  type: 'key_down' | 'key_up';
  timestamp: number;
  handId: 'left' | 'right';
  fingerId: 'index' | 'middle' | 'ring' | 'pinky';
  zoneId: string;                // Zone where event occurred
  keyCode: string;               // Mapped key (e.g., 'Space', 'Enter', 'A')
  position: { x: number; y: number };  // Cursor position at event time
  modifiers: {
    thumb: boolean;              // Thumb curled = modifier active
    otherHand: boolean;          // Other hand in specific zone = modifier
  };
}
```

### Requirement 29: Zone-Based Action Mapping

**User Story:** As a developer, I want to map finger state changes to different actions based on which zone the cursor is in, so that I can create context-sensitive gesture interfaces.

#### Acceptance Criteria

1. WHEN a finger state changes THEN the system SHALL look up the action for (zone_id, finger_id, transition_type)
2. WHEN an action is mapped THEN the system SHALL support action types: key_press, function_call, event_emit
3. WHEN no mapping exists THEN the system SHALL use the default action (or no action)
4. WHEN configuring actions THEN the system SHALL allow chaining multiple actions per trigger
5. WHEN actions include modifiers THEN the system SHALL check modifier state before triggering
6. WHEN serializing action mappings THEN the round-trip SHALL produce an equivalent configuration

#### Action Mapping Configuration

```typescript
interface ZoneAction {
  trigger: {
    fingerId: 'index' | 'middle' | 'ring' | 'pinky' | 'any';
    transition: 'arm' | 'disarm' | 'enter' | 'exit' | 'dwell';
    modifiers?: {
      thumbCurled?: boolean;
      otherHandInZone?: string;
    };
  };
  action: {
    type: 'key_press' | 'function_call' | 'event_emit';
    keyCode?: string;            // For key_press
    functionName?: string;       // For function_call
    eventType?: string;          // For event_emit
    eventData?: Record<string, unknown>;
  };
}
```

### Requirement 30: Pseudo-Z Depth from Palm Geometry

**User Story:** As a user, I want the system to estimate depth (Z) from my hand's distance to the camera, so that I can interact in 3D space with a single camera.

#### Acceptance Criteria

1. WHEN a hand is detected THEN the system SHALL compute handspan from index MCP to pinky MCP distance
2. WHEN handspan is computed THEN the system SHALL estimate relative Z depth (larger span = closer)
3. WHEN Z depth changes THEN the system SHALL classify into zones: NEAR, NEUTRAL, FAR
4. WHEN the user calibrates THEN the system SHALL record handspan at neutral, near, and far positions
5. WHEN calibration is complete THEN the system SHALL use calibrated values for zone boundaries
6. WHEN Z zone changes THEN the system SHALL emit a z_zone_change event
7. WHEN serializing Z calibration THEN the round-trip SHALL produce an equivalent configuration

#### Pseudo-Z Estimation

```typescript
interface PseudoZState {
  // Raw measurement
  handspanPixels: number;        // Distance from index MCP to pinky MCP in pixels

  // Calibrated values (set during calibration)
  calibration: {
    nearHandspan: number;        // Handspan when hand is close to camera
    neutralHandspan: number;     // Handspan at comfortable distance
    farHandspan: number;         // Handspan when hand is far from camera
  };

  // Computed zone
  zZone: 'NEAR' | 'NEUTRAL' | 'FAR';
  zValue: number;                // 0-1 normalized (0=far, 1=near)
  confidence: number;            // Confidence in Z estimate
}
```

#### Z Zone Thresholds

| Zone | Handspan Ratio | Description |
|:-----|:---------------|:------------|
| NEAR | > 1.2 × neutral | Hand close to camera (push gesture) |
| NEUTRAL | 0.8-1.2 × neutral | Comfortable interaction distance |
| FAR | < 0.8 × neutral | Hand far from camera (pull gesture) |

### Requirement 31: Z-Depth Calibration Flow

**User Story:** As a user, I want to calibrate the Z-depth estimation with my actual hand, so that the system accurately detects my near/neutral/far positions.

#### Acceptance Criteria

1. WHEN calibration starts THEN the system SHALL prompt user to hold hand at neutral distance
2. WHEN user confirms neutral THEN the system SHALL record handspan as neutralHandspan
3. WHEN prompted for near THEN the system SHALL ask user to bring hand close to camera
4. WHEN user confirms near THEN the system SHALL record handspan as nearHandspan
5. WHEN prompted for far THEN the system SHALL ask user to move hand away from camera
6. WHEN user confirms far THEN the system SHALL record handspan as farHandspan
7. WHEN calibration completes THEN the system SHALL persist calibration values
8. WHEN calibration is invalid (near ≤ far) THEN the system SHALL reject and prompt retry

#### Calibration Flow

```
1. "Hold your hand at a comfortable distance" → Record neutralHandspan
2. "Bring your hand close to the camera" → Record nearHandspan
3. "Move your hand away from the camera" → Record farHandspan
4. Validate: nearHandspan > neutralHandspan > farHandspan
5. Save calibration
```

### Requirement 32: Combined Output (Ghost + Elemental + Key + Z)

**User Story:** As a developer, I want a unified output that includes cursor position, armed state, key events, and Z depth, so that I can build rich 3D gesture interfaces.

#### Acceptance Criteria

1. WHEN the pipeline produces output THEN the system SHALL include all cursor states (ghost + elemental per finger)
2. WHEN finger state changes THEN the output SHALL include any triggered key events
3. WHEN Z depth is estimated THEN the output SHALL include zZone and zValue
4. WHEN zones are active THEN the output SHALL include list of zones containing the cursor
5. WHEN serializing combined output THEN the round-trip SHALL produce an equivalent object

#### Combined Output Interface

```typescript
interface GhostCursorOutput {
  // Hand tracking
  handId: 'left' | 'right';
  trackingState: 'IDLE' | 'TRACKING' | 'COASTING';

  // Position (2D)
  position: { x: number; y: number };
  velocity: { x: number; y: number; magnitude: number };

  // Pseudo-Z (3D)
  zDepth: PseudoZState;

  // Per-finger state
  fingers: {
    index: PerFingerOutput;
    middle: PerFingerOutput;
    ring: PerFingerOutput;
    pinky: PerFingerOutput;
    thumb: PerFingerOutput;
  };

  // Spatial zones
  activeZones: string[];         // Zone IDs containing cursor

  // Key events this frame
  keyEvents: GestureKeyEvent[];

  // Timing
  timestamp: number;
  frameId: number;
}

interface PerFingerOutput {
  curl: CanonicalFingerCurl;
  armedState: 'ARMED' | 'DISARMED' | 'ARMING' | 'DISARMING';
  cursorPosition: { x: number; y: number };  // May differ from hand position with gain
  element: 'fire' | 'water' | 'earth' | 'thunder' | 'ghost';
}
```

### Requirement 33: Future Sensor Fusion (6DOF)

**User Story:** As a developer, I want the architecture to support sensor fusion for full 6DOF tracking, so that we can achieve mm-level precision when additional sensors are available.

#### Acceptance Criteria

1. WHEN additional sensors are available (depth camera, IMU, stereo) THEN the system SHALL fuse data via Kalman filter
2. WHEN sensor fusion is active THEN the system SHALL output full 6DOF pose (x, y, z, roll, pitch, yaw)
3. WHEN sensors disagree THEN the system SHALL weight by confidence and recency
4. WHEN a sensor is lost THEN the system SHALL gracefully degrade to remaining sensors
5. WHEN configuring sensors THEN the system SHALL allow enabling/disabling each sensor source
6. WHEN serializing sensor fusion configuration THEN the round-trip SHALL produce an equivalent configuration

#### Sensor Fusion Architecture (Future)

```
Monocular Camera (Human.js) ─┐
                             ├─→ Kalman Fusion ─→ 6DOF Pose
Depth Camera (RealSense) ────┤
                             │
IMU (Phone Accelerometer) ───┤
                             │
Stereo Cameras ──────────────┘

Output: { x, y, z, roll, pitch, yaw, confidence }
```

---

## Mosaic Warfare Mission Engineering

**Principle:** Adapt gesture mechanics to available sensors and mission requirements.

| Mission | Sensors | Interaction Mode | Example |
|:--------|:--------|:-----------------|:--------|
| 2P Pong | Monocamera | Finger curl clutch | Straighten finger = paddle moves |
| Touchfree Kiosk | Monocamera | Push-to-click (Z depth) | Push hand forward = click |
| Drawing App | Monocamera | Dwell + pinch | Hover to select, pinch to draw |
| VR Controller | Depth + IMU | Full 6DOF | mm-level precision |
| Accessibility | Any | Adaptive | Best available for user |

**Spatial zones are 3D hitboxes** that work with whatever Z precision is available:
- Monocamera: 3 Z zones (NEAR/NEUTRAL/FAR) from handspan
- Depth camera: Continuous Z with mm precision
- The zone system adapts - same config, different sensor backends

---

## Interaction Model Summary (Gen 77.4)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Ghost Cursor Interaction Model                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  HAND TRACKING (always on)                                                   │
│  ├── Ghost Cursor: Semi-transparent, follows hand                           │
│  └── Position: (x, y) screen coordinates                                    │
│                                                                              │
│  FINGER CLUTCH (per finger)                                                  │
│  ├── ARMED (straight): Elemental cursor, target moves                       │
│  ├── DISARMED (curled): Ghost cursor, target frozen                         │
│  └── Transition: Emits key_down/key_up events                               │
│                                                                              │
│  SPATIAL ZONES (configurable)                                                │
│  ├── Zone A: Full screen (default)                                          │
│  ├── Zone B: Top-left quadrant → maps to 'W' key                            │
│  ├── Zone C: Top-right quadrant → maps to 'E' key                           │
│  └── Overlapping zones: Multiple actions possible                           │
│                                                                              │
│  PSEUDO-Z DEPTH (monocular)                                                  │
│  ├── NEAR: Hand close to camera (handspan large)                            │
│  ├── NEUTRAL: Comfortable distance (calibrated)                             │
│  ├── FAR: Hand far from camera (handspan small)                             │
│  └── Future: Sensor fusion for mm-level 6DOF                                │
│                                                                              │
│  COMBINED OUTPUT                                                             │
│  └── { position, zDepth, fingers[], activeZones[], keyEvents[] }            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Added: 2025-12-19 | Gen 77.4 | Spatial Zones + Key Events + Pseudo-Z Requirements*
