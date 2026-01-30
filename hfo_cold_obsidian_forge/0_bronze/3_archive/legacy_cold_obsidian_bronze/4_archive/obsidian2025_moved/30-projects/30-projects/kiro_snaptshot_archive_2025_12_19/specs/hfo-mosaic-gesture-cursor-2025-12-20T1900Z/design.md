---
hfo:
  gen: 78
  ts: 2025-12-19T19:08:48.199Z
  port: 6
  role: REMEMBER
  trigram: ☱
  pillar: Assimilator
  greek: Μνήμη
  phase: PERCEIVE
  status: active
  desc: design
---

# Design Document: HFO Mosaic Gesture Cursor

## Overview

This design specifies the architecture for the Mosaic Gesture Cursor system, including the Cold Stigmergy Header format, the 3-layer cursor visualization, and the fire elemental effects. The system transforms noisy gesture data into trustworthy cursor input with visual feedback at each pipeline stage.

**Key Innovation**: Three simultaneous cursor layers showing raw → smooth → predictive transformation, with fire particle effects on the predictive cursor.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MOSAIC CURSOR VISUALIZATION                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    CAMERA BACKGROUND                            │   │
│   │                    (Full-screen, mirrored)                      │   │
│   │                                                                 │   │
│   │     ○ Raw (gray)                                                │   │
│   │        ↓                                                        │   │
│   │     ● Smooth (blue) [TRACKING]                                  │   │
│   │        ↓                                                        │   │
│   │     🔥 Predictive (fire trail)                                  │   │
│   │                                                                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   PHASER OVERLAY (transparent background)                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Architecture

### Pipeline Flow (Port-to-Port)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW PIPELINE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Human.js          Port 0           Port 2           Port 3            │
│   ┌──────┐         ┌──────┐         ┌──────┐         ┌──────┐          │
│   │Camera│────────>│Observ│────────>│Shaper│────────>│Inject│          │
│   │ Feed │         │  er  │         │      │         │  or  │          │
│   └──────┘         └──────┘         └──────┘         └──────┘          │
│                        │                │                │              │
│                        │                │                │              │
│                        ▼                ▼                ▼              │
│                   ┌────────┐      ┌────────┐      ┌────────┐           │
│                   │  Raw   │      │ Smooth │      │  Fire  │           │
│                   │ Cursor │      │ Cursor │      │ Cursor │           │
│                   │ (gray) │      │ (blue) │      │(orange)│           │
│                   └────────┘      └────────┘      └────────┘           │
│                                                                         │
│   Contracts:                                                            │
│   - CanonicalHandState (Port 0 → Port 2)                               │
│   - CanonicalIntent (Port 2 → Port 3)                                  │
│   - PredictiveIntent (Port 2 → Port 3, with Kalman state)              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Cold Stigmergy Integration

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COLD STIGMERGY FLOW                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Source Files                Port 1              Port 5                │
│   ┌──────────┐               ┌──────┐            ┌──────┐              │
│   │@hfo-cold │──────────────>│Bridger│──────────>│Immun │              │
│   │-stigmergy│   Parse       │Parser │  Validate │ izer │              │
│   │ header   │               └──────┘            └──────┘              │
│   └──────────┘                   │                   │                  │
│                                  │                   │                  │
│                                  ▼                   ▼                  │
│                             ┌──────┐            ┌──────┐               │
│                             │ Port │            │Errors│               │
│                             │  6   │            │  &   │               │
│                             │Assim │            │Warns │               │
│                             │ilator│            └──────┘               │
│                             └──────┘                                    │
│                                  │                                      │
│                                  ▼                                      │
│                             ┌──────────┐                               │
│                             │Knowledge │                               │
│                             │  Graph   │                               │
│                             └──────────┘                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Cold Stigmergy Header Contract

```typescript
// src/ghost_cursor/contracts/cold_stigmergy_header.ts

export const PORT_ONTOLOGY = {
  0: { role: 'SENSE',     trigram: '☷', pillar: 'Observer',    greek: 'Αἴσθησις',   phase: 'PERCEIVE' },
  1: { role: 'CONNECT',   trigram: '☶', pillar: 'Bridger',     greek: 'Σύνδεσμος',  phase: 'REACT' },
  2: { role: 'TRANSFORM', trigram: '☵', pillar: 'Shaper',      greek: 'Μορφή',      phase: 'EXECUTE' },
  3: { role: 'DELIVER',   trigram: '☴', pillar: 'Injector',    greek: 'Ἔκχυσις',    phase: 'EXECUTE' },
  4: { role: 'CHAOS',     trigram: '☳', pillar: 'Disruptor',   greek: 'Χάος',       phase: 'YIELD' },
  5: { role: 'VALIDATE',  trigram: '☲', pillar: 'Immunizer',   greek: 'Ἀσφάλεια',   phase: 'YIELD' },
  6: { role: 'REMEMBER',  trigram: '☱', pillar: 'Assimilator', greek: 'Μνήμη',      phase: 'PERCEIVE' },
  7: { role: 'NAVIGATE',  trigram: '☰', pillar: 'Navigator',   greek: 'Κυβέρνησις', phase: 'REACT' },
} as const;

export interface ColdStigmergyHeader {
  gen: number;
  ts: string;
  port: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;
  role: string;
  trigram: string;
  pillar: string;
  phase: 'PERCEIVE' | 'REACT' | 'EXECUTE' | 'YIELD';
  status: 'active' | 'deprecated' | 'theater' | 'archived';
  greek?: string;
  contracts?: { input?: string; output?: string };
  desc?: string;
}

export function deriveSubject(header: ColdStigmergyHeader): string {
  return `hfo.${header.gen}.port${header.port}.${header.pillar.toLowerCase()}.${header.phase.toLowerCase()}`;
}
```

### 2. Mosaic Cursor Layers (P0 - Position Only)

```typescript
// src/ghost_cursor/ports/port3_injector/mosaic_cursor_renderer.ts

// Layer offsets (stacked vertically for visual clarity)
const RAW_OFFSET_Y = 0;      // At fingertip
const SMOOTH_OFFSET_Y = -10; // 10px above raw
const FIRE_OFFSET_Y = -20;   // 20px above raw

export interface CursorLayer {
  id: 'raw' | 'smooth' | 'predictive';
  position: { x: number; y: number };
  color: number;
  opacity: number;
  visible: boolean;
}

export interface MosaicCursorState {
  fingertipX: number;           // Raw fingertip X
  fingertipY: number;           // Raw fingertip Y
  smoothX: number;              // 1Euro filtered X
  smoothY: number;              // 1Euro filtered Y
  predictiveX: number;          // Kalman predicted X
  predictiveY: number;          // Kalman predicted Y
  trackingState: 'IDLE' | 'TRACKING' | 'COASTING';
  confidence: number;
}

export class MosaicCursorRenderer {
  private scene: Phaser.Scene;
  private rawDot: Phaser.GameObjects.Arc;
  private smoothDot: Phaser.GameObjects.Arc;
  private fireEmitter: Phaser.GameObjects.Particles.ParticleEmitter;
  private stateLabel: Phaser.GameObjects.Text;
  
  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.initializeLayers();
  }
  
  private initializeLayers(): void {
    // Layer 1: Raw cursor (gray, at fingertip)
    this.rawDot = this.scene.add.arc(0, 0, 8, 0, 360, false, 0x888888);
    this.rawDot.setAlpha(0.6);
    
    // Layer 2: Smooth cursor (blue, 10px above)
    this.smoothDot = this.scene.add.arc(0, 0, 10, 0, 360, false, 0x4488ff);
    
    // Layer 3: Fire cursor (20px above, particle emitter)
    this.fireEmitter = this.scene.add.particles(0, 0, 'fire', {
      speed: { min: 50, max: 100 },
      scale: { start: 0.5, end: 0 },
      alpha: { start: 1, end: 0 },
      lifespan: 500,
      blendMode: 'ADD',
      tint: [0xff4400, 0xff8800, 0xffcc00],
    });
    
    // State label (next to smooth cursor)
    this.stateLabel = this.scene.add.text(0, 0, 'IDLE', {
      fontSize: '12px',
      color: '#4488ff',
    });
  }
  
  update(state: MosaicCursorState): void {
    // Layer 1: Raw cursor at fingertip
    this.rawDot.setPosition(state.fingertipX, state.fingertipY + RAW_OFFSET_Y);
    this.rawDot.setAlpha(state.confidence < 0.3 ? 0.3 : 0.6);
    
    // Layer 2: Smooth cursor 10px above
    this.smoothDot.setPosition(state.smoothX, state.smoothY + SMOOTH_OFFSET_Y);
    this.stateLabel.setPosition(state.smoothX + 15, state.smoothY + SMOOTH_OFFSET_Y - 10);
    this.stateLabel.setText(state.trackingState);
    
    // Layer 3: Fire cursor 20px above
    this.fireEmitter.setPosition(state.predictiveX, state.predictiveY + FIRE_OFFSET_Y);
  }
}
```

### 3. Fire Elemental Configuration (Inverse Velocity)

```typescript
// src/ghost_cursor/ports/port3_injector/fire_config.ts

export interface FireConfig {
  // Particle settings
  maxParticleCount: number;   // Max particles when stationary (30-100)
  minParticleCount: number;   // Min particles when moving fast (5-20)
  
  // Trail settings (for fast movement)
  trailEnabled: boolean;
  trailMultiplier: number;    // velocity * multiplier = trail length
  trailFadeTime: number;      // ms for trail to fade
  
  // Ember glow (for stationary)
  emberGlowRadius: number;    // 5-20px
  emberPulseSpeed: number;    // Pulse frequency
  
  // Velocity thresholds
  maxVelocity: number;        // px/s, above this = min fire
  
  // Colors
  colorTemperature: 'warm' | 'hot';
}

export const DEFAULT_FIRE_CONFIG: FireConfig = {
  maxParticleCount: 50,       // Big fire when still
  minParticleCount: 10,       // Small fire when moving
  trailEnabled: true,
  trailMultiplier: 0.1,       // Trail length = velocity * 0.1
  trailFadeTime: 300,         // 300ms fade
  emberGlowRadius: 12,
  emberPulseSpeed: 2,         // 2Hz pulse
  maxVelocity: 500,           // px/s
  colorTemperature: 'hot',
};

/**
 * Calculate fire intensity from velocity (INVERSE relationship)
 * Low velocity = high intensity (big fire)
 * High velocity = low intensity (small fire + trail)
 */
export function calculateFireIntensity(velocity: number, config: FireConfig): number {
  const normalized = Math.min(velocity / config.maxVelocity, 1);
  return 1.0 - normalized; // Inverse!
}

/**
 * Calculate particle count from intensity
 */
export function calculateParticleCount(intensity: number, config: FireConfig): number {
  const range = config.maxParticleCount - config.minParticleCount;
  return Math.round(config.minParticleCount + (range * intensity));
}

/**
 * Calculate trail length from velocity
 */
export function calculateTrailLength(velocity: number, config: FireConfig): number {
  if (!config.trailEnabled) return 0;
  return velocity * config.trailMultiplier;
}

export function getFireColors(temp: 'warm' | 'hot'): number[] {
  return temp === 'hot'
    ? [0xff4400, 0xff6600, 0xff8800, 0xffaa00]  // Orange-red
    : [0xffcc00, 0xffdd44, 0xffee88, 0xffffcc]; // Yellow-white
}
```

### 4. Predictive Intent (Kalman Extension)

```typescript
// src/ghost_cursor/contracts/predictive_intent.ts

import { CanonicalIntent } from './canonical_intent';

export interface KalmanState {
  x: number;          // Position
  vx: number;         // Velocity
  ax: number;         // Acceleration (predicted)
  y: number;
  vy: number;
  ay: number;
  uncertainty: number; // Kalman uncertainty
}

export interface PredictiveIntent extends CanonicalIntent {
  kalman: KalmanState;
  predictedPosition: { x: number; y: number };
  predictionHorizon: number; // ms into future
}
```

## Data Models

### Vertical Slice Scope (P0)

**In Scope**:
- Index fingertip X/Y position tracking
- 3-layer cursor visualization (raw → smooth → predictive)
- Fire particle effects on predictive cursor
- Physics-based coasting (Phaser physics, inertia)

**Out of Scope (Future)**:
- Finger angle computation
- Curl-to-click detection
- Dwell-to-click
- ARMED state
- Multi-finger gestures

### Pipeline Contracts (Strict Layering)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      STRICT PIPELINE LAYERING                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Human.js ──────> CanonicalHandState ──────> CanonicalIntent           │
│   (Raw)            (Smooth)                   (Predictive)              │
│                                                                         │
│   Layer 1:         Layer 2:                   Layer 3:                  │
│   - Unprocessed    - 1Euro filter (tuned)     - Kalman filter           │
│   - Noisy          - State machine            - Prediction horizon      │
│   - Gray dot       - Coasting (physics)       - Fire particles          │
│                    - Blue dot                 - Orange fire             │
│                                                                         │
│   IMPORTANT: Predictive NEVER sees raw. Only smooth → predictive.       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Coasting Behavior (Physics-Based)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      COASTING WITH PHASER PHYSICS                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   When confidence < 0.5:                                                │
│   1. Stop updating position from Human.js                               │
│   2. Apply Phaser physics body with:                                    │
│      - Current velocity (inertia)                                       │
│      - Drag coefficient (gradual slowdown)                              │
│      - No gravity (2D cursor)                                           │
│   3. Cursor coasts with natural deceleration                            │
│   4. When confidence > 0.5, resume tracking                             │
│                                                                         │
│   Phaser Physics Config:                                                │
│   - drag: 0.95 (per frame)                                              │
│   - maxVelocity: 1000                                                   │
│   - bounce: 0 (no bouncing off edges)                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Kalman Prediction Config

```typescript
// Default prediction horizon: 100ms ahead
const DEFAULT_PREDICTION_HORIZON_MS = 100;

// Tunable via WinBox settings panel
interface KalmanConfig {
  predictionHorizonMs: number;  // 50-500ms, default 100
  processNoise: number;         // How much we trust the model
  measurementNoise: number;     // How much we trust the input
}
```

### Fire Intensity Mapping (Inverse Velocity)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      FIRE INTENSITY = INVERSE VELOCITY                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Velocity → Fire Intensity (INVERSE relationship)                      │
│                                                                         │
│   Low velocity (stationary):                                            │
│   - BIG fire, lots of particles                                         │
│   - Ember glow effect                                                   │
│   - "Charging up" visual                                                │
│                                                                         │
│   High velocity (moving fast):                                          │
│   - SMALL fire, fewer particles                                         │
│   - Polypath trailing effect                                            │
│   - "Cutting through air" visual                                        │
│   - Trail shows movement path                                           │
│                                                                         │
│   Formula:                                                              │
│   fireIntensity = 1.0 - clamp(velocity / maxVelocity, 0, 1)            │
│   trailLength = velocity * trailMultiplier                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Cursor Layer Positions

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      3-LAYER CURSOR STACK                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                    🔥 Predictive (fire)                                 │
│                       ↑ +20px offset                                    │
│                    ● Smooth (blue)                                      │
│                       ↑ +10px offset                                    │
│                    ○ Raw (gray)                                         │
│                       ↑ fingertip position                              │
│                    ✋ Index Fingertip                                    │
│                                                                         │
│   Visual Stack:                                                         │
│   - Raw cursor: At exact fingertip position (gray, 8px)                │
│   - Smooth cursor: 10px above raw (blue, 10px)                         │
│   - Fire cursor: 20px above raw (orange particles)                     │
│                                                                         │
│   This stacking shows the pipeline transformation visually              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Simple State Machine (P0)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      TRACKING STATE MACHINE (P0)                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                         ┌──────────┐                                    │
│                         │   IDLE   │                                    │
│                         └────┬─────┘                                    │
│                              │ hand detected                            │
│                              ▼                                          │
│                         ┌──────────┐                                    │
│              ┌─────────>│ TRACKING │<─────────┐                         │
│              │          └────┬─────┘          │                         │
│              │               │                │                         │
│              │    confidence │ confidence     │                         │
│              │    > 0.5      │ < 0.5          │                         │
│              │               ▼                │                         │
│              │          ┌──────────┐          │                         │
│              │          │ COASTING │──────────┘                         │
│              │          └────┬─────┘  confidence > 0.5                  │
│              │               │                                          │
│              │               │ timeout (2s)                             │
│              │               ▼                                          │
│              │          ┌──────────┐                                    │
│              └──────────│   IDLE   │                                    │
│                         └──────────┘                                    │
│                                                                         │
│   Note: No ARMED state in P0 - just position tracking                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Cold Stigmergy Header Round-Trip
*For any* valid ColdStigmergyHeader object, serializing to YAML then parsing back SHALL produce an equivalent object.
**Validates: Requirements 0.0.1.3, 0.0.1.5**

### Property 2: Port Ontology Consistency
*For any* port number 0-7, the role, trigram, pillar, and phase fields in a header SHALL match the PORT_ONTOLOGY lookup.
**Validates: Requirements 0.0.3.1-0.0.3.5**

### Property 3: NATS Subject Derivation Determinism
*For any* ColdStigmergyHeader, calling deriveSubject() multiple times SHALL always produce the same subject string.
**Validates: Requirements 0.0.7.2**

### Property 4: Validation Error Detection
*For any* header with missing required fields or port/role mismatch, the Immunizer SHALL return at least one error or warning.
**Validates: Requirements 0.0.5.2-0.0.5.4**

### Property 5: Raw Cursor Position Fidelity
*For any* detected hand landmark, the raw cursor position SHALL equal the index fingertip position without transformation.
**Validates: Requirements 0.1.2.2**

### Property 6: Coasting State Transition
*For any* confidence value < 0.5, the smooth cursor state machine SHALL transition to COASTING state.
**Validates: Requirements 0.1.3.4**

### Property 7: Fire Intensity Inverse Velocity
*For any* two cursor velocities v1 < v2, the fire intensity for v1 SHALL be > the fire intensity for v2 (inverse relationship).
**Validates: Requirements 0.1.4.4**

### Property 8: Cursor Layer Offset Consistency
*For any* fingertip position, the smooth cursor SHALL be offset -10px Y from raw, and predictive SHALL be offset -20px Y from raw.
**Validates: Requirements 0.1.1.1-0.1.1.3**

### Property 9: Predictive Never Sees Raw
*For any* frame, the Kalman filter input SHALL be the smooth (CanonicalHandState) position, never the raw Human.js position.
**Validates: Pipeline Contracts**

### Property 10: Coasting Preserves Velocity
*For any* transition to COASTING state, the cursor SHALL maintain its current velocity and decelerate via Phaser physics drag.
**Validates: Coasting Behavior**

## Error Handling

| Error Code | Description | Recovery |
|:-----------|:------------|:---------|
| `MISSING_HEADER` | File has no Cold Stigmergy header | Add header with current gen |
| `ONTOLOGY_MISMATCH` | Port fields don't match ontology | Auto-fix from PORT_ONTOLOGY |
| `LOW_CONFIDENCE` | Hand tracking confidence < 0.3 | Enter COASTING, fade cursors |
| `HAND_LOST` | No hand detected for > 2s | Return to IDLE, hide cursors |
| `FIRE_OVERFLOW` | Too many particles | Cap at maxParticleCount |

## Testing Strategy

### Property-Based Tests (fast-check)

The following properties will be tested using fast-check:

1. **Header Round-Trip** (Property 1): Generate random valid headers, serialize, parse, compare
2. **Port Ontology** (Property 2): Generate random port numbers, verify ontology match
3. **Subject Derivation** (Property 3): Generate random headers, verify determinism
4. **Coasting Transition** (Property 6): Generate random confidence values, verify state
5. **Fire Intensity** (Property 7): Generate random velocity pairs, verify monotonicity

### Unit Tests

- Parser tests for TypeScript and Markdown header formats
- Validator tests for each error condition
- State machine transition tests
- Fire config serialization tests

### Integration Tests

- Full pipeline from camera to cursor rendering
- Cold Stigmergy header seeding and validation
- Phaser overlay rendering with camera background

---

*HFO Gen 78 | Mosaic Gesture Cursor Design | 2025-12-20T20:30:00Z*
