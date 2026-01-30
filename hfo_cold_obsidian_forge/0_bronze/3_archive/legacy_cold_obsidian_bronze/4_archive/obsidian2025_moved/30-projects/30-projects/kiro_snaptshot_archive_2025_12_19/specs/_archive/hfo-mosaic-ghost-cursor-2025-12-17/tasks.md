# Tasks: HFO Mosaic Ghost Cursor

## Phase 0: Cold Start Setup (Phoenix Protocol)

- [x] 1. Archive existing gesture_ninja code ✅
  - [x] 1.1 Create `reference/gesture_ninja_archive/` directory
  - [x] 1.2 Move `src/gesture_ninja/` to archive (preserve for reference)
  - [x] 1.3 Document what was archived and why
  - _Requirements: 0_

- [x] 2. Create new project structure ✅
  - [x] 2.1 Create `src/ghost_cursor/` directory
  - [x] 2.2 Create `src/ghost_cursor/ports/` for 8 ports
  - [x] 2.3 Create `src/ghost_cursor/contracts/` for data models
  - [x] 2.4 Create `src/ghost_cursor/demo/` for test page
  - [x] 2.5 Create `src/ghost_cursor/tests/` for test files
  - _Requirements: 0_

- [x] 3. Install and verify exemplars ✅
  - [x] 3.1 Install @vladmandic/human v3.3.6
  - [x] 3.2 Install @webarkit/oneeurofilter-ts
  - [x] 3.3 Install xstate v5
  - [x] 3.4 Install cloudevents
  - [x] 3.5 Install fast-check
  - _Requirements: 0_

- [x] 4. Physics checks (GATE - must pass before glue code) ✅
  - [x] 4.1 Verify Human.js returns 21 keypoints in browser (requires browser test)
  - [x] 4.2 Verify 1Euro filter reduces jitter on test data (43.5% reduction)
  - [x] 4.3 Verify XState transitions correctly (5/5 transitions)
  - [x] 4.4 Verify JSONL round-trip serialization (792 bytes)
  - [x] 4.5 Verify fast-check generates random hand states (100 valid)
  - _Requirements: 0_

**Checkpoint 0**: All physics checks pass, ready for glue code ✅ (2025-12-17)

---

## Phase 1: Data Contracts

- [x] 5. Implement CanonicalHandState contract ✅
  - [x] 5.1 Create `src/ghost_cursor/contracts/canonical_hand_state.ts`
  - [x] 5.2 Define interface with 21 landmarks, confidence, fingerCurl, gesture
  - [ ] 5.3 Add Pydantic model in `canonical_hand_state.py` for cross-language
  - [x] 5.4 Write round-trip serialization test (in physics_check_node.ts)
  - _Requirements: 2_

- [x] 6. Implement CanonicalIntent contract ✅
  - [x] 6.1 Create `src/ghost_cursor/contracts/canonical_intent.ts`
  - [x] 6.2 Define interface with position, velocity, confidence, armed, state
  - [ ] 6.3 Add Pydantic model for cross-language
  - [x] 6.4 Write round-trip serialization test
  - _Requirements: 1_

- [x] 7. Implement CloudEvent envelope ✅
  - [x] 7.1 Create `src/ghost_cursor/contracts/cloud_event.ts`
  - [x] 7.2 Define CloudEvent<T> generic interface
  - [x] 7.3 Add W3C Trace Context fields
  - [x] 7.4 Write round-trip serialization test
  - _Requirements: 3_

**Checkpoint 1**: All contracts defined with passing round-trip tests ✅ (2025-12-17)

---

## Phase 2: Core Pipeline (TypeScript Ports)

- [x] 8. Implement Port 0 Observer ✅
  - [x] 8.1 Create `src/ghost_cursor/ports/port0_observer/index.ts`
  - [x] 8.2 Implement HumanJsAdapter wrapping @vladmandic/human
  - [x] 8.3 Extract 21 keypoints to CanonicalHandState
  - [x] 8.4 Pass through fingerCurl, fingerDirection, gesture (DO NOT RECOMPUTE)
  - [ ]* 8.5 Write unit tests for adapter
  - _Requirements: 2_

- [x] 9. Implement Port 1 Bridger (LITE) ✅
  - [x] 9.1 Create `src/ghost_cursor/ports/port1_bridger/index.ts`
  - [x] 9.2 Implement EventEmitterBridger (Phase 1 LITE)
  - [x] 9.3 Wrap events in CloudEvents envelope
  - [x] 9.4 Generate trace context (traceId, spanId)
  - [ ]* 9.5 Write unit tests for bridger
  - _Requirements: 3_

- [x] 10. Implement Port 2 Shaper ✅
  - [x] 10.1 Create `src/ghost_cursor/ports/port2_shaper/index.ts`
  - [x] 10.2 Implement 1Euro filter wrapper
  - [x] 10.3 Implement XState state machine (IDLE→TRACKING→ARMED→DISARMED→COASTING)
  - [x] 10.4 Implement teleport rejection (blend jumps >100px)
  - [x] 10.5 Implement inertial coasting (500ms timeout)
  - [x] 10.6 Create Earth and Thunder presets
  - [ ]* 10.7 Write unit tests for shaper
  - _Requirements: 4_

- [x] 11. Implement Port 3 Injector (DOM Consumer) ✅
  - [x] 11.1 Create `src/ghost_cursor/ports/port3_injector/index.ts`
  - [x] 11.2 Implement DOMConsumer that moves a cursor element
  - [x] 11.3 Subscribe to CanonicalIntent from Bridger
  - [x] 11.4 Update cursor position at ≥30fps
  - [ ]* 11.5 Write unit tests for injector
  - _Requirements: 5_

**Checkpoint 2a**: TypeScript ports implemented ✅ (2025-12-17)
- Note: Ports exist but are NOT wired to demo yet

---

## Phase 2b: Bundle & Wire TypeScript to Demo (NEW - CRITICAL)

- [ ] 12. Bundle TypeScript for browser
  - [ ] 12.1 Create `src/ghost_cursor/build/esbuild.config.js` for browser bundling
  - [ ] 12.2 Configure esbuild to output ESM bundle with Human.js external
  - [ ] 12.3 Add npm script `build:ghost-cursor` to package.json
  - [ ] 12.4 Verify bundle loads in browser without errors
  - _Requirements: 1, 2, 4, 5_

- [ ] 13. Wire demo to real TypeScript ports
  - [ ] 13.1 Replace inline 1Euro filter with import from bundle
  - [ ] 13.2 Replace inline detection loop with HumanJsAdapter from Port 0
  - [ ] 13.3 Wire Bridger (Port 1) for event routing
  - [ ] 13.4 Wire Shaper (Port 2) for filtering and state machine
  - [ ] 13.5 Wire DOMConsumer (Port 3) for cursor rendering
  - [ ] 13.6 Show state machine state (IDLE/TRACKING/ARMED/DISARMED/COASTING) in UI
  - _Requirements: 1, 2, 4, 5_

- [ ] 14. Add multi-hand cursor support (2 hands = 2 cursors)
  - [ ] 14.1 Modify HumanJsAdapter to return array of CanonicalHandState (up to 2 hands)
  - [ ] 14.2 Create separate Shaper instance per hand
  - [ ] 14.3 Create separate cursor element per hand (different colors for left/right)
  - [ ] 14.4 Position each cursor above its hand's index finger tip
  - [ ] 14.5 Handle hand tracking loss independently per hand
  - _Requirements: 2, 5_

- [ ] 15. Fix live camera detection
  - [ ] 15.1 Debug camera stream initialization
  - [ ] 15.2 Verify Human.js config for webcam input
  - [ ] 15.3 Add error handling and user feedback for camera issues
  - [ ] 15.4 Test with golden video AND live camera
  - _Requirements: 2_

**Checkpoint 2b**: Demo uses real TypeScript architecture with multi-hand support

---

## Phase 3: Test Harness

- [ ] 16. Implement Port 6 Assimilator (Recording)
  - [ ] 16.1 Create `src/ghost_cursor/ports/port6_assimilator/index.ts`
  - [ ] 16.2 Implement JSONLRecorder (append-only event log)
  - [ ] 16.3 Record all CloudEvents with monotonic timestamps
  - [ ] 16.4 Auto-save to local storage on session end
  - [ ]* 16.5 Write unit tests for recorder
  - _Requirements: 8_

- [ ] 17. Implement replay functionality
  - [ ] 17.1 Implement ReplayAdapter for Port 0 Observer
  - [ ] 17.2 Load JSONL and feed events in recorded order
  - [ ] 17.3 Verify deterministic output (same input → same output)
  - [ ]* 17.4 Write replay tests
  - _Requirements: 8, 13_

- [ ] 18. Create golden master recordings
  - [ ] 18.1 Record baseline_idle.jsonl (hand still)
  - [ ] 18.2 Record baseline_swipe.jsonl (hand moving)
  - [ ] 18.3 Record baseline_tracking_loss.jsonl (hand disappears)
  - [ ] 18.4 Store in `src/ghost_cursor/tests/golden/`
  - _Requirements: 8_

- [ ] 19. Implement Port 5 Immunizer
  - [ ] 19.1 Create `src/ghost_cursor/ports/port5_immunizer/index.ts`
  - [ ] 19.2 Implement validators for CanonicalHandState
  - [ ] 19.3 Implement validators for CanonicalIntent
  - [ ] 19.4 Implement invariant checks (confidence in [0,1], velocity < 2000px/s)
  - [ ]* 19.5 Write unit tests for validators
  - _Requirements: 7_

- [ ] 20. Implement Port 4 Disruptor
  - [ ] 20.1 Create `src/ghost_cursor/ports/port4_disruptor/index.ts`
  - [ ] 20.2 Implement fast-check strategies for random hand states
  - [ ] 20.3 Implement chaos injection (tracking loss, jitter spikes)
  - [ ]* 20.4 Write property-based tests
  - _Requirements: 6_

- [ ] 21. Implement regression guards
  - [ ] 21.1 Compare replay output against golden masters
  - [ ] 21.2 Report delta if output differs
  - [ ] 21.3 Block changes that break golden masters
  - _Requirements: 7, 8_

**Checkpoint 3**: Test harness complete with golden masters and regression guards

---

## Phase 4: Interactions

- [ ] 22. Implement dwell click
  - [ ] 22.1 Create `src/ghost_cursor/ports/port3_injector/dwell_click.ts`
  - [ ] 22.2 Start timer when cursor enters target hitbox
  - [ ] 22.3 Trigger activation after 500ms dwell
  - [ ] 22.4 Reset timer if cursor exits
  - [ ] 22.5 Add visual feedback (progress indicator)
  - [ ] 22.6 Add cooldown to prevent double-activation
  - _Requirements: 10_

- [ ] 23. Implement pinch click
  - [ ] 23.1 Create `src/ghost_cursor/ports/port3_injector/pinch_click.ts`
  - [ ] 23.2 Detect thumb-to-index pinch using Human.js fingerCurl
  - [ ] 23.3 Trigger click on pinch, release on separate
  - [ ] 23.4 Detect double-click (two pinches within 500ms)
  - [ ] 23.5 Add visual feedback (color change)
  - _Requirements: 10.5_

- [ ] 24. Implement scroll gesture
  - [ ] 24.1 Create `src/ghost_cursor/ports/port3_injector/scroll_gesture.ts`
  - [ ] 24.2 Enter scroll mode when index finger curled
  - [ ] 24.3 Emit scroll events based on hand movement
  - [ ] 24.4 Exit scroll mode when index extended
  - [ ] 24.5 Add visual feedback (scroll indicator)
  - _Requirements: 10.6_

- [ ] 25. Add interaction mode selector
  - [ ] 25.1 Add UI to switch between dwell and pinch modes
  - [ ] 25.2 Persist preference
  - [ ] 25.3 Disable conflicting modes
  - _Requirements: 10, 10.5_

**Checkpoint 4**: All interaction modes working with visual feedback

---

## Phase 5: Configuration & Polish

- [ ] 26. Implement play area and gain controls
  - [ ] 26.1 Add play area bounds configuration
  - [ ] 26.2 Add gain multiplier configuration
  - [ ] 26.3 Add deadzone configuration
  - [ ] 26.4 Add UI for adjusting controls
  - _Requirements: 11_

- [ ] 27. Implement camera placement modes
  - [ ] 27.1 Add Normal/Above/Behind placement options
  - [ ] 27.2 Adjust coordinate mapping per placement
  - [ ] 27.3 Persist preference
  - _Requirements: 14.5_

- [ ] 28. Implement adaptive thresholds
  - [ ] 28.1 Express all thresholds as ratios of screen diagonal
  - [ ] 28.2 Validate threshold ranges
  - [ ] 28.3 Add Immunizer check for magic numbers
  - _Requirements: 15_

- [ ] 29. Implement video input mode (already partially working)
  - [ ] 29.1 Wire video file input through real TypeScript ports
  - [ ] 29.2 Process video frames through HumanJsAdapter
  - [ ] 29.3 Add playback controls (pause, seek)
  - _Requirements: 13_

**Checkpoint 5**: Full configuration and video input working

---

## Phase 6: Optimization (Week 2)

- [ ] 30. Implement Port 7 Navigator
  - [ ] 30.1 Create `src/ghost_cursor/ports/port7_navigator/index.ts`
  - [ ] 30.2 Implement pyribs archive wrapper
  - [ ] 30.3 Implement score fusion (latency, jitter, false activations)
  - [ ] 30.4 Run parameter sweeps
  - _Requirements: 9_

- [ ] 31. Upgrade Bridger to NATS
  - [ ] 31.1 Install nats.ws
  - [ ] 31.2 Implement NATSBridger
  - [ ] 31.3 Add JetStream replay capability
  - _Requirements: 3_

- [ ] 32. Add OpenTelemetry tracing
  - [ ] 32.1 Install @opentelemetry/api
  - [ ] 32.2 Add spans for each port
  - [ ] 32.3 Measure latency through pipeline
  - _Requirements: 3, NFR-1_

- [ ] 33. Mobile performance optimization
  - [ ] 33.1 Profile on mid-range smartphone
  - [ ] 33.2 Optimize to maintain ≥30fps
  - [ ] 33.3 Add MediaPipe fallback if Human.js too slow
  - _Requirements: NFR-1_

**Checkpoint 6**: Full 8-port architecture with optimization

---

## Summary

| Phase | Tasks | Est. Time |
|-------|-------|-----------|
| 0. Cold Start | 4 | 2 hours ✅ |
| 1. Contracts | 3 | 1 hour ✅ |
| 2. Core Pipeline (TS) | 4 | 3 hours ✅ |
| 2b. Bundle & Wire | 4 | 3 hours ⬅️ **NEXT** |
| 3. Test Harness | 6 | 4 hours |
| 4. Interactions | 4 | 3 hours |
| 5. Configuration | 4 | 2 hours |
| 6. Optimization | 4 | 4 hours |
| **Total** | **33** | **22 hours** |

---

## Current Status (2025-12-18)

**DONE:**
- Phase 0-1: Setup and contracts complete
- Phase 2: TypeScript ports implemented (Observer, Bridger, Shaper, Injector)
- Golden video test passes (71/158 frames with hands detected)

**PROBLEM:**
- Demo HTML uses inline code, NOT the TypeScript ports
- Only 1 cursor rendered (should be 2 for 2 hands)
- Live camera detection needs debugging

**NEXT:**
- Phase 2b: Bundle TypeScript and wire to demo
- Task 12: Create esbuild config for browser bundle
- Task 13: Replace inline code with real port imports
- Task 14: Add multi-hand cursor support (2 hands = 2 cursors)
- Task 15: Fix live camera detection

---

*Tasks Updated: 2025-12-18 | HFO Gen 77 | Ghost Cursor Capacity Engineering Platform*
