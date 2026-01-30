# Design Document: HFO Mosaic Ghost Cursor

## Overview

The Ghost Cursor is a **Capacity Engineering Platform** that produces a trusted, replayable, engine-agnostic pointer from mobile camera input. This design implements the complete 8-port hexagonal architecture with verified exemplars.

**Core Deliverable**: CanonicalIntent - a smoothed, confident cursor position that any application can consume.

**Architecture Principle**: Mosaic Warfare - every component is swappable, testable in isolation, and graded via deterministic test harness.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Ghost Cursor Pipeline                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Port 0     │    │   Port 1     │    │   Port 2     │    │  Port 3   │ │
│  │   Observer   │───▶│   Bridger    │───▶│   Shaper     │───▶│  Injector │ │
│  │   (SENSE)    │    │   (REASON)   │    │   (ACT)      │    │  (TIME)   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └───────────┘ │
│        │                    │                   │                   │       │
│        ▼                    ▼                   ▼                   ▼       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Port 4     │    │   Port 5     │    │   Port 6     │    │  Port 7   │ │
│  │  Disruptor   │    │  Immunizer   │    │ Assimilator  │    │ Navigator │ │
│  │   (CHAOS)    │    │  (VALIDATE)  │    │  (REMEMBER)  │    │  (GOAL)   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘    └───────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Models

### CanonicalHandState (Port 0 Output)

```typescript
interface CanonicalHandState {
  // Identity
  handId: 'left' | 'right';
  timestamp: number;  // monotonic ms
  frameId: number;

  // 21 Keypoints (normalized 0-1)
  landmarks: Array<{
    x: number;  // 0-1 normalized
    y: number;  // 0-1 normalized
    z: number;  // depth, 0-1 normalized
  }>;

  // Confidence
  confidence: number;  // 0-1

  // Human.js passthrough (DO NOT RECOMPUTE)
  fingerCurl?: {
    thumb: 'none' | 'half' | 'full';
    index: 'none' | 'half' | 'full';
    middle: 'none' | 'half' | 'full';
    ring: 'none' | 'half' | 'full';
    pinky: 'none' | 'half' | 'full';
  };
  fingerDirection?: {
    thumb: string;
    index: string;
    middle: string;
    ring: string;
    pinky: string;
  };
  gesture?: string;  // thumbsUp, victory, point, etc.

  // Source adapter
  source: 'human-js' | 'mediapipe' | 'replay';
}
```

### CanonicalIntent (Port 2 Output - THE GHOST CURSOR)

```typescript
interface CanonicalIntent {
  // Position (screen space)
  position: {
    x: number;  // pixels
    y: number;  // pixels
  };

  // Velocity
  velocity: {
    x: number;  // px/s
    y: number;  // px/s
    magnitude: number;  // px/s
  };

  // State
  confidence: number;  // 0-1
  armed: boolean;  // true = gestures enabled
  state: 'IDLE' | 'TRACKING' | 'ARMED' | 'DISARMED' | 'COASTING';

  // Timing
  timestamp: number;
  latencyMs: number;  // processing latency

  // Interaction
  dwellProgress?: number;  // 0-1 if dwelling
  scrollMode?: boolean;

  // Trace
  traceId: string;
  spanId: string;
}
```

### CloudEvents Envelope (Port 1)

```typescript
interface CloudEvent<T> {
  specversion: '1.0';
  type: string;  // e.g., 'hfo.observer.hand_state'
  source: string;  // e.g., '/hfo/port/0/observer'
  id: string;  // UUID
  time: string;  // ISO 8601
  datacontenttype: 'application/json';
  data: T;

  // W3C Trace Context
  traceparent?: string;  // 00-{traceId}-{spanId}-{flags}
}
```

### Shaper Configuration

```typescript
interface ShaperConfig {
  // 1Euro Filter
  oneEuro: {
    minCutoff: number;  // Hz, lower = smoother
    beta: number;  // speed coefficient
    dcutoff: number;  // derivative cutoff
  };

  // State Machine Thresholds (as ratios of screen diagonal)
  thresholds: {
    armVelocity: number;  // ratio, e.g., 0.3 = 30% of diagonal/s
    disarmVelocity: number;  // ratio
    disarmDelay: number;  // ms
    coastTimeout: number;  // ms
    confidenceMin: number;  // 0-1
  };

  // Presets
  preset: 'earth' | 'thunder';
}

// Preset Definitions
const PRESETS: Record<string, ShaperConfig> = {
  earth: {
    oneEuro: { minCutoff: 0.5, beta: 0.001, dcutoff: 1.0 },
    thresholds: {
      armVelocity: 0.3,
      disarmVelocity: 0.1,
      disarmDelay: 100,
      coastTimeout: 500,
      confidenceMin: 0.7
    },
    preset: 'earth'
  },
  thunder: {
    oneEuro: { minCutoff: 1.5, beta: 0.007, dcutoff: 1.0 },
    thresholds: {
      armVelocity: 0.2,
      disarmVelocity: 0.05,
      disarmDelay: 50,
      coastTimeout: 300,
      confidenceMin: 0.6
    },
    preset: 'thunder'
  }
};
```

## Component Design

### Port 0: Observer (SENSE)

**Responsibility**: Extract CanonicalHandState from any sensor.

**Adapters**:
1. `HumanJsAdapter` - Wraps @vladmandic/human v3.3.6
2. `MediaPipeAdapter` - Wraps MediaPipe Hands (future)
3. `ReplayAdapter` - Reads from JSONL replay file

**Interface**:
```typescript
interface ObserverPort {
  initialize(): Promise<void>;
  detect(frame: ImageData | HTMLVideoElement): Promise<CanonicalHandState | null>;
  dispose(): void;
}
```

**Human.js Passthrough Rule**: If Human.js provides fingerCurl, fingerDirection, or gesture, pass through WITHOUT recomputation. Human.js has optimized these calculations.

### Port 1: Bridger (REASON)

**Responsibility**: Wrap all inter-port messages in CloudEvents with trace context.

**Phase 1 (LITE)**: EventEmitter-based, local only
**Phase 2**: NATS.ws + OpenTelemetry
**Phase 3**: Full CloudEvents SDK + JetStream replay

**Interface**:
```typescript
interface BridgerPort {
  publish<T>(type: string, data: T): void;
  subscribe<T>(type: string, handler: (event: CloudEvent<T>) => void): void;
  getTraceContext(): { traceId: string; spanId: string };
}
```

### Port 2: Shaper (ACT)

**Responsibility**: Transform noisy sensor data into trusted CanonicalIntent.

**Pipeline**:
1. **1Euro Filter** (@webarkit/oneeurofilter-ts) - Velocity-adaptive smoothing
2. **Kalman Predictor** (custom ~50 lines) - Negative latency prediction
3. **State Machine** (XState v5) - IDLE→TRACKING→ARMED→DISARMED→COASTING
4. **Teleport Rejection** - Blend jumps >100px with previous position

**Legacy State Machine Definition (Gen 76 - Velocity-Based)**:
```typescript
// DEPRECATED: Velocity-based arming replaced by finger-curl clutch in Gen 77.3
const legacyShaperMachine = createMachine({
  id: 'shaper',
  initial: 'IDLE',
  context: {
    lastPosition: null,
    lastVelocity: null,
    coastStartTime: null
  },
  states: {
    IDLE: {
      on: {
        HAND_DETECTED: {
          target: 'TRACKING',
          guard: 'confidenceAboveMin'
        }
      }
    },
    TRACKING: {
      on: {
        VELOCITY_HIGH: { target: 'ARMED' },
        TRACKING_LOST: { target: 'COASTING' },
        NO_HAND_TIMEOUT: { target: 'IDLE' }
      }
    },
    ARMED: {
      on: {
        VELOCITY_LOW: { target: 'DISARMED', guard: 'disarmDelayElapsed' },
        TRACKING_LOST: { target: 'COASTING' }
      }
    },
    DISARMED: {
      on: {
        VELOCITY_HIGH: { target: 'ARMED' },
        TRACKING_LOST: { target: 'COASTING' },
        NO_HAND_TIMEOUT: { target: 'IDLE' }
      }
    },
    COASTING: {
      entry: 'startCoasting',
      on: {
        HAND_REACQUIRED: { target: 'TRACKING' },
        COAST_TIMEOUT: { target: 'IDLE' }
      }
    }
  }
});
```

### Hierarchical State Machine (Gen 77.3 - Clutch Model)

The state machine is now HIERARCHICAL with two orthogonal layers:

**Key Insight**: Hand tracking and finger armed state are ORTHOGONAL.
- Hand can be TRACKING while finger is DISARMED (ghost cursor visible, target frozen)
- Hand can be COASTING while finger was ARMED (inertia continues, preserves armed state)
- Finger states are PRESERVED during COASTING and restored on reacquisition

**Hand Tracking Machine (Cursor Visibility)**:
```typescript
const handTrackingMachine = createMachine({
  id: 'handTracking',
  initial: 'IDLE',
  context: {
    lastPosition: { x: 0, y: 0 },
    lastVelocity: { x: 0, y: 0 },
    coastStartTime: null,
    fingerStates: {}  // Preserved during COASTING
  },
  states: {
    IDLE: {
      on: {
        HAND_DETECTED: { target: 'TRACKING', guard: 'confidenceAboveMin' }
      }
    },
    TRACKING: {
      on: {
        TRACKING_LOST: { target: 'COASTING', actions: 'preserveFingerStates' },
        NO_HAND_TIMEOUT: { target: 'IDLE' }
      }
    },
    COASTING: {
      entry: ['startCoasting', 'applyInertia'],
      on: {
        HAND_REACQUIRED: { target: 'TRACKING', actions: 'restoreFingerStates' },
        COAST_TIMEOUT: { target: 'IDLE' }
      }
    }
  }
});
```

**Finger Armed Machine (Per-Finger, Independent)**:
```typescript
const fingerArmedMachine = createMachine({
  id: 'fingerArmed',
  initial: 'DISARMED',
  context: {
    fingerId: 'index',  // index, middle, ring, pinky
    curlValue: 1.0,     // 0 = straight, 1 = curled
    armStartTime: null,
    disarmStartTime: null,
    lastArmedPosition: { x: 0, y: 0 }
  },
  states: {
    DISARMED: {
      on: {
        CURL_BELOW_ARM_THRESHOLD: {
          target: 'ARMING',
          guard: 'curlBelowThreshold'  // curl < 0.2
        }
      }
    },
    ARMING: {
      entry: 'startArmTimer',
      on: {
        ARM_DELAY_ELAPSED: { target: 'ARMED' },  // 50ms
        CURL_ABOVE_ARM_THRESHOLD: { target: 'DISARMED' }  // Cancelled
      }
    },
    ARMED: {
      entry: 'transformToElemental',
      on: {
        CURL_ABOVE_DISARM_THRESHOLD: {
          target: 'DISARMING',
          guard: 'curlAboveThreshold'  // curl > 0.6
        }
      }
    },
    DISARMING: {
      entry: ['startDisarmTimer', 'saveLastPosition'],
      on: {
        DISARM_DELAY_ELAPSED: { target: 'DISARMED' },  // 50ms
        CURL_BELOW_DISARM_THRESHOLD: { target: 'ARMED' }  // Cancelled
      }
    }
  }
});
```

**Hysteresis Configuration**:
```typescript
interface HysteresisConfig {
  armThreshold: number;      // 0.2 - curl below this = straight
  disarmThreshold: number;   // 0.6 - curl above this = curled
  armDelay: number;          // 50ms
  disarmDelay: number;       // 50ms
  // Dead zone: 0.2-0.6 = no state change
}
```

**State Combinations**:

| Hand State | Finger State | Cursor | Target |
|:-----------|:-------------|:-------|:-------|
| TRACKING | ARMED | Elemental, follows hand | Moves with cursor |
| TRACKING | DISARMED | Ghost, follows hand | Frozen |
| COASTING | ARMED (preserved) | Elemental, inertia | Continues with inertia |
| COASTING | DISARMED (preserved) | Ghost, inertia | Frozen |
| IDLE | N/A | Not visible | Frozen |

### CanonicalFingerCurl (Gen 77.3)

```typescript
interface CanonicalFingerCurl {
  // Raw Human.js value (data source)
  humanJsValue: 'none' | 'half' | 'full';

  // Computed from smoothed landmarks (continuous 0-1)
  computedValue: number;

  // Fused value (weighted combination)
  fusedValue: number;

  // Confidence in the measurement
  confidence: number;

  // Which source was used for final value
  source: 'humanjs' | 'computed' | 'fused';
}

interface PerFingerState {
  fingerId: 'index' | 'middle' | 'ring' | 'pinky' | 'thumb';
  curl: CanonicalFingerCurl;
  armedState: 'ARMED' | 'DISARMED' | 'ARMING' | 'DISARMING';
  lastArmedPosition: { x: number; y: number };
  element: 'fire' | 'water' | 'earth' | 'thunder';  // Visual style when armed
}
```

### Finger Curl Geometry

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

### Finger Curl Processing Pipeline

```
Smoothed Landmarks → Compute Angle → CanonicalFingerCurl
                                           ↓
Human.js Curl ──────────────────────→ Fuse Sources
                                           ↓
                              1Euro Filter → Kalman Predict → Hysteresis → State
                                                   ↓
                                         Biomechanics Weight
```

### Biomechanics Weighting

| Finger | Curl Speed | Curl Range | Weight | Notes |
|:-------|:-----------|:-----------|:-------|:------|
| Index | Fast | Full (0-1) | 1.0 | Primary control finger |
| Middle | Fast | Full (0-1) | 0.9 | Secondary control |
| Ring | Medium | Partial (0-0.8) | 0.7 | Coupled to middle |
| Pinky | Slow | Limited (0-0.6) | 0.5 | Least independent |
| Thumb | Variable | Rotation | 0.8 | Used for pinch/modifier |

### Inertia Physics (Coasting)

```typescript
interface InertiaConfig {
  coastTimeout: number;      // 500ms - max coasting duration
  velocityDecay: number;     // 0.95 - per-frame velocity multiplier
  blendDuration: number;     // 100ms - blend to reacquired position
  minVelocity: number;       // 10px/s - stop coasting below this
}

// During COASTING:
// position += velocity * dt
// velocity *= velocityDecay
// if (velocity.magnitude < minVelocity) stop coasting
```

### Port 3: Injector (TIME)

**Responsibility**: Deliver CanonicalIntent to consumers (games, apps).

**Consumers**:
1. `GodotConsumer` - WebSocket bridge to Godot 4
2. `DOMConsumer` - Move a DOM element as cursor
3. `ExcalidrawConsumer` - Drawing app integration (future)

**Interaction Modes**:
1. **Dwell Click** - Hover for 500ms to activate
2. **Pinch Click** - Thumb-to-index pinch
3. **Scroll Gesture** - Index finger curl

**Interface**:
```typescript
interface InjectorPort {
  onIntent(intent: CanonicalIntent): void;
  setInteractionMode(mode: 'dwell' | 'pinch'): void;
}
```

### Port 4: Disruptor (CHAOS)

**Responsibility**: Adversarial testing to find edge cases.

**Tools**:
1. **Hypothesis** (Python) - Property-based testing
2. **fast-check** (TypeScript) - Property-based testing
3. **Chaos Injection** - Simulate tracking loss, jitter spikes

**Test Strategies**:
```typescript
interface TestStrategyPort {
  generateHandState(): CanonicalHandState;
  generateCorruptedEvent(): unknown;
  injectChaos(type: 'tracking_loss' | 'jitter_spike' | 'latency'): void;
}
```

### Port 5: Immunizer (VALIDATE)

**Responsibility**: Validate invariants and guard against regressions.

**Invariants**:
1. Confidence always in [0, 1]
2. Velocity never exceeds 2000px/s (physically implausible)
3. No gesture events when cursor is disarmed
4. All required fields present in CanonicalHandState

**Interface**:
```typescript
interface ImmunizerPort {
  validate(event: unknown): ValidationResult;
  checkInvariant(name: string, condition: boolean): void;
  runRegressionGuards(golden: string, actual: string): RegressionResult;
}
```

### Port 6: Assimilator (REMEMBER)

**Responsibility**: Record, replay, and compute fused scores.

**Storage**:
1. **JSONL Replay** - Append-only event log
2. **Golden Masters** - Deterministic baseline recordings
3. **Score Fusion** - Weighted metric combination

**Metrics**:
- Latency p95 (ms)
- Jitter StdDev (px)
- False Activations (count)
- Tracking Recovery (ms)
- Round-Trip Fidelity (%)

**Interface**:
```typescript
interface AssimilatorPort {
  startRecording(): void;
  stopRecording(): string;  // returns JSONL path
  loadReplay(path: string): AsyncIterable<CloudEvent<unknown>>;
  computeScore(metrics: Metrics, weights: Weights): number;
}
```

### Port 7: Navigator (GOAL)

**Responsibility**: Explore design space and optimize toward Pareto frontier.

**Tools**:
1. **pyribs** - MAP-Elites QD archive
2. **MCTS** - Parameter space exploration
3. **AoA** - Trade analysis for exemplar selection

**Interface**:
```typescript
interface NavigatorPort {
  addToArchive(solution: number[], objective: number, behavior: number[]): void;
  getBestPreset(): ShaperConfig;
  runAoA(alternatives: Alternative[]): AoAResult;
}
```

## File Structure

```
src/ghost_cursor/
├── ports/
│   ├── port0_observer/
│   │   ├── index.ts
│   │   ├── human_js_adapter.ts
│   │   ├── mediapipe_adapter.ts
│   │   └── replay_adapter.ts
│   ├── port1_bridger/
│   │   ├── index.ts
│   │   ├── event_emitter_bridger.ts  # Phase 1
│   │   └── nats_bridger.ts           # Phase 2
│   ├── port2_shaper/
│   │   ├── index.ts
│   │   ├── one_euro_filter.ts
│   │   ├── kalman_predictor.ts
│   │   ├── state_machine.ts
│   │   └── presets.ts
│   ├── port3_injector/
│   │   ├── index.ts
│   │   ├── dom_consumer.ts
│   │   ├── godot_consumer.ts
│   │   ├── dwell_click.ts
│   │   └── pinch_click.ts
│   ├── port4_disruptor/
│   │   ├── index.ts
│   │   ├── pbt_strategies.ts
│   │   └── chaos_injector.ts
│   ├── port5_immunizer/
│   │   ├── index.ts
│   │   ├── validators.ts
│   │   └── regression_guards.ts
│   ├── port6_assimilator/
│   │   ├── index.ts
│   │   ├── jsonl_recorder.ts
│   │   ├── golden_comparator.ts
│   │   └── score_fusion.ts
│   └── port7_navigator/
│       ├── index.ts
│       ├── pyribs_archive.ts
│       └── aoa_analyzer.ts
├── contracts/
│   ├── canonical_hand_state.ts
│   ├── canonical_intent.ts
│   └── cloud_event.ts
├── demo/
│   ├── index.html
│   └── demo.ts
└── tests/
    ├── port0_observer.test.ts
    ├── port2_shaper.test.ts
    └── golden/
        └── baseline_idle.jsonl
```

## Implementation Phases

### Phase 1: Physics Checks (Day 1)
1. Archive existing `src/gesture_ninja/` to `reference/`
2. Install exemplars: @vladmandic/human, @webarkit/oneeurofilter-ts, xstate
3. Write isolation tests for each exemplar
4. Verify round-trip serialization for all data models
5. GATE: All physics checks pass before any glue code

### Phase 2: Core Pipeline (Days 2-3)
1. Implement Port 0 Observer with Human.js adapter
2. Implement Port 1 Bridger (EventEmitter LITE)
3. Implement Port 2 Shaper with 1Euro + state machine
4. Implement Port 3 Injector with DOM consumer
5. Create demo page showing cursor movement

### Phase 3: Test Harness (Days 4-5)
1. Implement Port 6 Assimilator (JSONL recording)
2. Create golden master recordings
3. Implement Port 5 Immunizer (validators)
4. Implement Port 4 Disruptor (PBT strategies)
5. Run regression tests against golden masters

### Phase 4: Interactions (Days 6-7)
1. Implement dwell click in Port 3
2. Implement pinch click in Port 3
3. Implement scroll gesture in Port 3
4. Add visual feedback for all interactions
5. Create preset selector UI

### Phase 5: Optimization (Week 2)
1. Implement Port 7 Navigator (pyribs archive)
2. Run parameter sweeps
3. Upgrade Bridger to NATS (Phase 2)
4. Add OpenTelemetry tracing
5. Optimize for mobile performance

## Dependencies

### npm (TypeScript)
```json
{
  "@vladmandic/human": "^3.3.6",
  "@webarkit/oneeurofilter-ts": "latest",
  "xstate": "^5.0.0",
  "cloudevents": "^8.0.0",
  "fast-check": "^3.0.0"
}
```

### pip (Python)
```
hypothesis>=6.0.0
pyribs>=0.7.0
pydantic>=2.0.0
```

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Frame Rate | ≥30fps | Performance.now() delta |
| Latency p95 | ≤100ms | Trace spans |
| Jitter StdDev | ≤5px | Position variance |
| False Activations | 0 per session | Immunizer count |
| Tracking Recovery | ≤200ms | State machine timing |

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Human.js too slow on mobile | Use MediaPipe adapter as fallback |
| 1Euro filter not smooth enough | Add Kalman prediction layer |
| State machine too complex | Start with 3 states, add as needed |
| JSONL files too large | Implement rotation and compression |
| Pinch detection unreliable | Fall back to dwell click |

---

*Design Created: 2025-12-17 | HFO Gen 76 | Ghost Cursor Capacity Engineering Platform*
*Architecture: 8-Port Hexagonal Mosaic | Phoenix Protocol Cold Start*


---

## Spatial Zones + Key Events + Pseudo-Z (Gen 77.4)

### Spatial Zone System

```
┌─────────────────────────────────────────────────────────────────┐
│                         Screen (1920x1080)                       │
├─────────────────────────────────┬───────────────────────────────┤
│                                 │                               │
│         Zone A (0,0,0.5,0.5)    │    Zone B (0.5,0,0.5,0.5)     │
│         Key: 'Q'                │    Key: 'W'                   │
│                                 │                               │
├─────────────────────────────────┼───────────────────────────────┤
│                                 │                               │
│         Zone C (0,0.5,0.5,0.5)  │    Zone D (0.5,0.5,0.5,0.5)   │
│         Key: 'A'                │    Key: 'S'                   │
│                                 │                               │
└─────────────────────────────────┴───────────────────────────────┘

Finger curl in Zone A → key_down('Q')
Finger uncurl in Zone A → key_up('Q')
```

### Zone Manager Interface

```typescript
interface ZoneManager {
  // Zone CRUD
  addZone(zone: SpatialZone): void;
  removeZone(zoneId: string): void;
  updateZone(zoneId: string, updates: Partial<SpatialZone>): void;

  // Query
  getZonesAtPosition(x: number, y: number): SpatialZone[];
  getZoneById(zoneId: string): SpatialZone | null;
  getAllZones(): SpatialZone[];

  // Events
  onZoneEnter(callback: (zoneId: string, handId: string) => void): void;
  onZoneExit(callback: (zoneId: string, handId: string) => void): void;
}
```

### Key Event Flow

```
Finger State Change
       │
       ▼
┌──────────────────┐
│ Get cursor (x,y) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Find active zones│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Look up action   │
│ (zone, finger,   │
│  transition)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Check modifiers  │
│ (thumb, other    │
│  hand)           │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Emit key event   │
│ or call function │
└──────────────────┘
```

### Pseudo-Z Depth Estimation

```
Camera View (monocular)
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│    Index MCP ●────────────────────────────────● Pinky MCP       │
│              │◄─────── handspanPixels ───────►│                 │
│                                                                  │
│    NEAR:    handspan > 1.2 × neutral  (hand close)              │
│    NEUTRAL: handspan ≈ neutral        (comfortable)             │
│    FAR:     handspan < 0.8 × neutral  (hand far)                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Z-Value Calculation:
  zValue = (handspan - farHandspan) / (nearHandspan - farHandspan)
  zValue = clamp(zValue, 0, 1)  // 0 = far, 1 = near
```

### Calibration State Machine

```mermaid
stateDiagram-v2
    [*] --> UNCALIBRATED: System start

    UNCALIBRATED --> CALIBRATING_NEUTRAL: Start calibration

    CALIBRATING_NEUTRAL --> CALIBRATING_NEAR: User confirms neutral
    CALIBRATING_NEAR --> CALIBRATING_FAR: User confirms near
    CALIBRATING_FAR --> VALIDATING: User confirms far

    VALIDATING --> CALIBRATED: Validation passes
    VALIDATING --> CALIBRATING_NEUTRAL: Validation fails (retry)

    CALIBRATED --> CALIBRATING_NEUTRAL: Recalibrate requested

    note right of CALIBRATING_NEUTRAL: "Hold hand at comfortable distance"
    note right of CALIBRATING_NEAR: "Bring hand close to camera"
    note right of CALIBRATING_FAR: "Move hand away from camera"
    note right of VALIDATING: Check: near > neutral > far
```

### Combined Output Pipeline

```
Observer (Port 0)
    │
    ├── CanonicalHandState
    │   ├── landmarks[21]
    │   ├── fingerCurl
    │   └── confidence
    │
    ▼
Shaper (Port 2)
    │
    ├── Hand Tracking Machine (IDLE/TRACKING/COASTING)
    ├── Finger Armed Machines (per finger)
    ├── Pseudo-Z Calculator
    │   └── handspan → zZone, zValue
    └── Zone Manager
        └── position → activeZones[]
    │
    ▼
Key Event Generator
    │
    ├── Finger transitions + zones → keyEvents[]
    │
    ▼
GhostCursorOutput
    │
    ├── position, velocity
    ├── zDepth { zZone, zValue }
    ├── fingers { index, middle, ring, pinky, thumb }
    ├── activeZones[]
    └── keyEvents[]
    │
    ▼
Injector (Port 3)
    │
    ├── Render cursors (ghost + elemental)
    ├── Dispatch key events
    └── Update game/app state
```

### Future: Sensor Fusion Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Sensor Fusion (Future)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Monocular   │  │    Depth     │  │     IMU      │          │
│  │   Camera     │  │   Camera     │  │  (Phone)     │          │
│  │  (Human.js)  │  │ (RealSense)  │  │              │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         ▼                 ▼                 ▼                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Kalman Fusion Filter                   │   │
│  │                                                          │   │
│  │  State: [x, y, z, vx, vy, vz, roll, pitch, yaw]         │   │
│  │  Measurement: Per-sensor with confidence weights         │   │
│  │  Output: 6DOF pose with uncertainty                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│                    ┌──────────────────┐                        │
│                    │   6DOF Output    │                        │
│                    │ x, y, z (mm)     │                        │
│                    │ roll, pitch, yaw │                        │
│                    │ confidence       │                        │
│                    └──────────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Added: 2025-12-19 | Gen 77.4 | Spatial Zones + Key Events + Pseudo-Z Design*
