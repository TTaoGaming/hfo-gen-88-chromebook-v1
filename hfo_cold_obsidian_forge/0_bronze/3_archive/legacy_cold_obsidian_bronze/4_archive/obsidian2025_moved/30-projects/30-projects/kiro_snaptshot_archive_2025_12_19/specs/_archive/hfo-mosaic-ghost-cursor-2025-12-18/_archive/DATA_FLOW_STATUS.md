# Ghost Cursor Data Flow Status

**Updated:** 2025-12-19T06:15:00Z
**Gen:** 77.2

## ✅ VERIFIED DATA FLOW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        GHOST CURSOR PIPELINE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Golden Video (MP4)                                                         │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ PORT 0: OBSERVER (Human.js Adapter)                                 │   │
│  │                                                                     │   │
│  │ Input:  HTMLVideoElement frame                                      │   │
│  │ Output: CanonicalHandState[]                                        │   │
│  │                                                                     │   │
│  │ Data Extracted:                                                     │   │
│  │   ✅ 21 landmarks (normalized 0-1)                                  │   │
│  │   ✅ handId: 'left' | 'right' (via HandednessTracker)               │   │
│  │   ✅ confidence: 0-1                                                │   │
│  │   ✅ gesture: string | undefined (from Human.js)                    │   │
│  │   ✅ fingerCurl: FingerCurlState (mapped from gesture)              │   │
│  │   ✅ frameId, timestamp                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ PORT 1: BRIDGER (EventEmitter)                                      │   │
│  │                                                                     │   │
│  │ Events Published:                                                   │   │
│  │   • hand.detected → CanonicalHandState                              │   │
│  │   • intent.updated → CanonicalIntent                                │   │
│  │                                                                     │   │
│  │ CloudEvent Envelope:                                                │   │
│  │   ✅ traceId, spanId (W3C Trace Context)                            │   │
│  │   ⚠️ Schema validation NOT enforced (TODO: Task 15.6)               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ PORT 2: SHAPER (1Euro + XState)                                     │   │
│  │                                                                     │   │
│  │ Input:  CanonicalHandState                                          │   │
│  │ Output: CanonicalIntent                                             │   │
│  │                                                                     │   │
│  │ Transformations:                                                    │   │
│  │   ✅ 1Euro filter (jitter reduction)                                │   │
│  │   ✅ Normalized → Screen coords (landmark[8] * screenWidth/Height)  │   │
│  │   ✅ Teleport rejection (blend jumps > 100px)                       │   │
│  │   ✅ Velocity calculation (px/s)                                    │   │
│  │                                                                     │   │
│  │ State Machine (XState v5):                                          │   │
│  │   ✅ IDLE → TRACKING (on HAND_DETECTED, confidence >= 0.7)          │   │
│  │   ✅ TRACKING → ARMED (on INDEX_STRAIGHT, fingerCurl.index='none')  │   │
│  │   ✅ ARMED → DISARMED (on INDEX_CURLED)                             │   │
│  │   ✅ * → COASTING (on HAND_LOST, 500ms timeout)                     │   │
│  │                                                                     │   │
│  │ GEN 77.2 FIX: Initial state now triggers INDEX_STRAIGHT event       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ PORT 3: INJECTOR (DOMConsumer)                                      │   │
│  │                                                                     │   │
│  │ Input:  CanonicalIntent                                             │   │
│  │ Output: DOM cursor element positioned at intent.position            │   │
│  │                                                                     │   │
│  │ Cursor Styling:                                                     │   │
│  │   • Left hand: Purple gradient                                      │   │
│  │   • Right hand: Blue gradient                                       │   │
│  │   • Opacity based on confidence                                     │   │
│  │   • Fades on COASTING                                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ PORT 6: ASSIMILATOR (JSONLRecorder)                                 │   │
│  │                                                                     │   │
│  │ Records:                                                            │   │
│  │   ✅ metadata event (session start)                                 │   │
│  │   ✅ hand events (per frame, per hand)                              │   │
│  │   ✅ intent events (per frame, per hand)                            │   │
│  │                                                                     │   │
│  │ Output: JSONL file for replay/testing                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📊 GOLDEN VIDEO TEST RESULTS (2025-12-19)

**Video:** `two_hands_baseline_idle_v1.mp4` (5.23s, 158 frames)

| Metric | Value | Status |
|:-------|:------|:-------|
| Total frames | 158 | ✅ |
| Frames with hands | 71 | ✅ |
| Frames with 2 hands | 27 | ✅ |
| Left hand detections | 27 | ✅ |
| Right hand detections | 71 | ✅ |
| ARMED state | ✅ Working | ✅ |

## 📦 CANONICAL OUTPUT SHAPES

### CanonicalHandState (Observer → Shaper)

```typescript
{
  handId: 'left' | 'right',
  timestamp: number,        // monotonic ms
  frameId: number,
  landmarks: Landmark[],    // 21 points, normalized 0-1
  confidence: number,       // 0-1
  fingerCurl?: {
    thumb: 'none' | 'half' | 'full',
    index: 'none' | 'half' | 'full',  // 'none' = straight = ARMED
    middle: 'none' | 'half' | 'full',
    ring: 'none' | 'half' | 'full',
    pinky: 'none' | 'half' | 'full'
  },
  gesture?: string,         // 'openPalm', 'fist', 'point', etc.
  source: 'human-js' | 'mediapipe' | 'replay'
}
```

### CanonicalIntent (Shaper → Injector/Phaser)

```typescript
{
  position: { x: number, y: number },  // screen pixels
  velocity: { x: number, y: number, magnitude: number },  // px/s
  confidence: number,       // 0-1
  armed: boolean,           // true when index finger straight
  state: 'IDLE' | 'TRACKING' | 'ARMED' | 'DISARMED' | 'COASTING',
  timestamp: number,
  latencyMs: number,
  traceId: string,
  spanId: string
}
```

## 🎮 PHASER PONG INTEGRATION (DONE)

**File:** `src/ghost_cursor/demo/pong.html`

### Integration Pattern

```typescript
// Hand intent state (updated by pipeline)
const handIntents = {
  left: { y: GAME_HEIGHT / 2, armed: false, state: 'IDLE' },
  right: { y: GAME_HEIGHT / 2, armed: false, state: 'IDLE' }
};

// Wire pipeline callback
pipeline.onIntent = (handId, intent) => {
  if (handId === 'left' || handId === 'right') {
    handIntents[handId] = {
      y: intent.position.y,
      armed: intent.armed,
      state: intent.state
    };
  }
};

// In Phaser scene update()
update() {
  // Map screen Y to game Y
  const leftY = (handIntents.left.y / screenHeight) * GAME_HEIGHT;
  this.leftPaddle.y = Phaser.Math.Clamp(leftY, ...);
  
  // Armed = paddle active (can hit ball)
  this.leftPaddle.body.enable = handIntents.left.armed;
  this.leftPaddle.setFillStyle(handIntents.left.armed ? 0xff6b35 : 0x444466);
}
```

### Features

| Feature | Implementation |
|:--------|:---------------|
| Left hand → Left paddle | `handIntents.left.y` → `leftPaddle.y` |
| Right hand → Right paddle | `handIntents.right.y` → `rightPaddle.y` |
| Armed = Active | `intent.armed` → `paddle.body.enable` |
| Visual feedback | Orange when armed, gray when inactive |
| Ball collision | Only bounces off ARMED paddles |
| Score tracking | Ball past paddle = point for opponent |

## 🔧 BUGS FIXED (Gen 77.2)

| Bug | Root Cause | Fix |
|:----|:-----------|:----|
| State always TRACKING | `lastCurlState` initialized to 'straight', so first call never triggered INDEX_STRAIGHT | Initialize to `null`, send event on first call |

## 📋 WHAT YOU HAVE vs WHAT YOU NEED

### ✅ HAVE

- 2-hand detection with handedness (left/right)
- ARMED state based on finger curl (index straight = armed)
- Smooth cursor position via 1Euro filter
- JSONL recording for replay
- 55 RED-GREEN-REFACTOR tests
- 110KB ESM bundle

### ❌ NEED

- [ ] Phaser Pong integration (PhaserConsumer)
- [ ] Live camera working
- [ ] Bridger schema validation (anti-fragile gate)
- [ ] Golden JSONL master for regression testing
- [ ] Additional gestures (pinch click, scroll)

---

*Gen 77.2 | 2025-12-19T06:15:00Z*
