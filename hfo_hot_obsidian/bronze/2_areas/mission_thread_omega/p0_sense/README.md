# Medallion: Bronze | Mutation: 0% | HIVE: I
# 🎯 PORT-0-SENSE: MediaPipe Hand Tracking Module

## Purpose
Port 0 (P0 SENSE) is responsible for raw sensing from the physical world using MediaPipe hand tracking.
This module captures hand landmarks and gestures, outputting structured data conforming to the P0SensingSchema.

## Architecture
```
Camera → MediaPipe → P0 SENSE → [P0SensingSchema] → P1 FUSE
```

## Core Responsibilities
1. **Hand Tracking**: Initialize and manage MediaPipe HandLandmarker
2. **Gesture Detection**: Detect pinch, fist, and open hand gestures
3. **Coordinate Extraction**: Extract index tip (landmark 8) coordinates
4. **Schema Compliance**: Output data conforming to P0SensingSchema (Zod 6.0)
5. **Lifecycle Management**: Event-driven initialization (no race conditions)
6. **Blackboard Logging**: Log all sensor events with provenance

## Files
- `mediapipe_sensor.js` - Core MediaPipe initialization and sensing logic
- `gesture_detector.js` - Gesture detection algorithms
- `p0_validator.js` - Zod schema validation for P0 output
- `p0_lifecycle.js` - Event-driven initialization management
- `README.md` - This file

## Contract Output
All P0 output must conform to `omega_contracts.zod.ts::P0SensingSchema`:
```typescript
{
  type: 'hfo.omega.p0.sensing',
  data: {
    timestamp: number,
    source: 'mediapipe-hand-8',
    coords: { x: [0,1], y: [0,1], z: number },
    confidence: [0,1],
    tuning: 'smooth' | 'snappy'
  }
}
```

## Testing
- Playwright smoke tests in `../tests/p0_smoke_test.spec.ts`
- Mutation testing target: 88-98% (Goldilocks Zone)

## Provenance
- **Created**: 2026-01-10T06:55:00Z
- **Commander**: P7 Spider Sovereign
- **Mission**: Thread Omega V20
- **Medallion**: Bronze
