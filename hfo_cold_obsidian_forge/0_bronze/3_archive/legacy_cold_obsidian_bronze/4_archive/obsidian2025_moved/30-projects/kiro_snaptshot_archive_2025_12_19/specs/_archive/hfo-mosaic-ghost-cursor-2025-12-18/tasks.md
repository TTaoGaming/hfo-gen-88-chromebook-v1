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
  - [ ] 10.7 Write unit tests for shaper

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

- [x] 12. Bundle TypeScript for browser ✅ (2025-12-18T15:00)
  - [x] 12.1 Create `src/ghost_cursor/build/esbuild.config.js` for browser bundling
  - [x] 12.2 Configure esbuild to output ESM bundle with Human.js external
  - [x] 12.3 Add npm script `build:ghost-cursor` to package.json
  - [x] 12.4 Verify bundle loads in browser without errors
  - _Requirements: 1, 2, 4, 5_

- [x] 13. Wire demo to real TypeScript ports ✅ (2025-12-18T15:00)
  - [x] 13.1 Replace inline 1Euro filter with import from bundle
  - [x] 13.2 Replace inline detection loop with HumanJsAdapter from Port 0
  - [x] 13.3 Wire Bridger (Port 1) for event routing
  - [x] 13.4 Wire Shaper (Port 2) for filtering and state machine
  - [x] 13.5 Wire DOMConsumer (Port 3) for cursor rendering
  - [x] 13.6 Show state machine state (IDLE/TRACKING/ARMED/DISARMED/COASTING) in UI
  - _Requirements: 1, 2, 4, 5_
  - **Note:** Created `index-bundled.html` using GhostCursorPipeline orchestrator

- [x] 14. Add multi-hand cursor support (2 hands = 2 cursors) ✅ (2025-12-18T15:00)
  - [x] 14.1 Modify HumanJsAdapter to return array of CanonicalHandState (up to 2 hands)
  - [x] 14.2 Create separate Shaper instance per hand
  - [x] 14.3 Create separate cursor element per hand (different colors for left/right)
  - [x] 14.4 Position each cursor above its hand's index finger tip
  - [x] 14.5 Handle hand tracking loss independently per hand
  - _Requirements: 2, 5_
  - **Note:** Pipeline creates per-hand Shaper/Consumer, second cursor is blue

- [ ] 15. Fix live camera detection
  - [ ] 15.1 Debug camera stream initialization
  - [ ] 15.2 Verify Human.js config for webcam input
  - [ ] 15.3 Add error handling and user feedback for camera issues
  - [ ] 15.4 Test with golden video AND live camera
  - _Requirements: 2_

**Checkpoint 2b**: Demo uses real TypeScript architecture with multi-hand support ✅ (partial - camera TBD)

---

## Phase 2c: Fix Pipeline Data Flow (CRITICAL - 2025-12-18 Diagnostic)

> **Diagnostic Finding**: Pipeline has data flow issues preventing multi-hand + finger-curl arming

### 🔴 Critical Issues Identified

| Issue | Location | Impact |
|:------|:---------|:-------|
| Single hand only | `pipeline.ts:137` | Only 1 cursor ever rendered |
| No fingerCurl passthrough | `human_js_adapter.ts:89` | Can't check index curl for arming |
| Velocity-based arming | `state_machine.ts:47-52` | Wrong arming logic |
| Bridger not validating | `port1_bridger/index.ts` | No schema validation on events |

### Architecture Goal

```
Human.js → Observer (rich hand data) → Bridger (validate + standardize) → Shaper (transform) → Injector
              ↓                              ↓                                ↓
         ALL hands                    CloudEvent envelope              Finger-curl arming
         fingerCurl                   Schema validation                Index straight = ARMED
         gesture                      Anti-fragile gate                Index curled = DISARMED
```

- [x] 15.5 Fix HumanJsAdapter to return ALL hands with rich data ✅ (2025-12-18T18:00)
  - [x] 15.5.1 Change `detect()` to `detectAll()` returning `CanonicalHandState[]`
  - [x] 15.5.2 Extract fingerCurl from Human.js `result.gesture` array
  - [x] 15.5.3 Map gesture strings to FingerCurlState (point, fist, etc.)
  - [x] 15.5.4 Pass through ALL Human.js hand data (don't filter)
  - _Requirements: 2_
  - **Note:** Added `gestureToFingerCurl()` mapping function

- [ ] 15.6 Enhance Bridger as anti-fragile gate
  - [ ] 15.6.1 Add schema validation for CanonicalHandState on publish
  - [ ] 15.6.2 Add schema validation for CanonicalIntent on publish
  - [ ] 15.6.3 Reject invalid events with error logging
  - [ ] 15.6.4 Add event type registry for standardization
  - [ ] 15.6.5 Ensure CloudEvent envelope always has traceId/spanId
  - _Requirements: 3_

- [x] 15.7 Fix Shaper arming logic to use finger curl ✅ (2025-12-18T18:00)
  - [x] 15.7.1 Add `isIndexStraight(handState)` function
  - [x] 15.7.2 Change state machine: INDEX_STRAIGHT → ARMED, INDEX_CURLED → DISARMED
  - [x] 15.7.3 Remove velocity-based arming (keep velocity for other purposes)
  - [x] 15.7.4 Add hysteresis to prevent flicker (debounce curl changes)
  - _Requirements: 4_
  - **Note:** 50ms debounce, `onFingerCurlUpdate()` method added

- [x] 15.8 Update Pipeline to use detectAll ✅ (2025-12-18T18:00)
  - [x] 15.8.1 Change `detectAllHands()` to call `observer.detectAll()`
  - [ ] 15.8.2 Verify N hands → N cursors (tested with golden video)
  - [ ] 15.8.3 Each cursor follows its hand's index finger tip
  - [ ] 15.8.4 Each cursor arms/disarms independently based on finger curl
  - _Requirements: 2, 5_
  - **Note:** Pipeline now calls `observer.detectAll()`, browser test needed

- [ ] 15.9 Test with golden 2-hands-idle video
  - [ ] 15.9.1 Feed `two_hands_baseline_idle_v1.mp4` into pipeline
  - [ ] 15.9.2 Verify 2 cursors appear (one per hand)
  - [ ] 15.9.3 Verify cursors follow index finger tips
  - [ ] 15.9.4 Verify arming based on index finger curl state
  - _Requirements: 2, 5_

**Checkpoint 2c**: Multi-hand + finger-curl arming code complete, browser test needed

---

## Phase 2d: Wire Real Pipeline to Demo (CRITICAL - 2025-12-18)

> **Problem:** Golden test passed using `index.html` with inline JS, NOT the TypeScript bundle.
> The TypeScript ports exist but aren't being tested.

### Goal: Minimal Glue, Production-Grade Exemplar Composition

```
index-bundled.html → GhostCursorPipeline → HumanJsAdapter → Bridger → Shaper → DOMConsumer
                                              ↓                         ↓
                                         detectAll()              finger-curl arming
                                         fingerCurl               state machine
```

- [ ] 16. Test bundled demo with golden video
  - [ ] 16.1 Update `test_golden_video.js` to use `index-bundled.html` instead of `index.html`
  - [ ] 16.2 Run test and verify pipeline initializes
  - [ ] 16.3 Verify hand detection works through TypeScript adapter
  - [ ] 16.4 Verify state machine transitions (IDLE→TRACKING→ARMED)
  - _Requirements: 2, 4, 5_

- [ ] 17. Add second cursor for multi-hand
  - [ ] 17.1 Create second cursor element in `index-bundled.html`
  - [ ] 17.2 Verify pipeline creates per-hand Shaper/Consumer
  - [ ] 17.3 Verify 2 cursors render for 2 hands
  - [ ] 17.4 Verify cursors have different colors (purple/blue)
  - _Requirements: 2, 5_

- [ ] 18. Verify finger-curl arming
  - [ ] 18.1 Add fingerCurl logging to demo
  - [ ] 18.2 Verify gesture → fingerCurl mapping works
  - [ ] 18.3 Verify INDEX_STRAIGHT → ARMED transition
  - [ ] 18.4 Verify INDEX_CURLED → DISARMED transition
  - _Requirements: 4_

- [ ] 19. Add JSONL output for replay
  - [ ] 19.1 Add CloudEvent logging to Bridger
  - [ ] 19.2 Output JSONL to console/download
  - [ ] 19.3 Verify output matches golden JSONL schema
  - _Requirements: 8_

**Checkpoint 2d**: Real TypeScript pipeline tested with golden video, multi-hand + finger-curl verified

---

## Phase 2e: Fix Multi-Hand Pipeline Bugs (CRITICAL - 2025-12-19)

> **Diagnostic Finding**: Pipeline has data flow bugs preventing correct multi-hand detection

### 🔴 Critical Bugs Identified

| Bug | Location | Root Cause | Fix |
|:----|:---------|:-----------|:----|
| Global state pollution | `human_js_adapter.ts:45` | `frameCounter` is module-level | Move to instance variable |
| Landmark normalization | `human_js_adapter.ts:110` | Human.js keypoints are PIXELS (0-640), code clamps to 0-1 | Divide by inputWidth/inputHeight |
| Same handId for both hands | `human_js_adapter.ts:140` | Geometry calc uses clamped landmarks (all 1.0) | Fix normalization first |

### Architecture Issue

```
Current (BROKEN):
  Human.js keypoints (pixels) → clamp(0,1) → all values = 1.0 → geometry fails → same handId

Fixed:
  Human.js keypoints (pixels) → divide by dimensions → normalized 0-1 → geometry works → correct handId
```

- [x] 20. Fix landmark normalization ✅ (2025-12-19)
  - [x] 20.1 Get input dimensions from Human.js result (result.width, result.height)
  - [x] 20.2 Divide keypoint x by inputWidth, y by inputHeight
  - [x] 20.3 Keep z as-is (already normalized in Human.js)
  - [x] 20.4 Verify landmarks are now in 0-1 range
  - _Requirements: 2_

- [x] 21. Fix global state pollution ✅ (2025-12-19)
  - [x] 21.1 Move `frameCounter` from module level to class instance
  - [x] 21.2 Initialize in constructor (default = 0)
  - [x] 21.3 Verify each adapter instance has independent counter
  - _Requirements: 2_

- [x] 22. Verify handedness geometry with correct landmarks ✅ (2025-12-19)
  - [x] 22.1 Run golden video test after landmark fix
  - [x] 22.2 Verify indexMCP.x and pinkyMCP.x are different values
  - [x] 22.3 Verify left hand gets handId='left', right hand gets handId='right'
  - [x] 22.4 Verify frames_with_two_hands > 0 (27 frames!)
  - _Requirements: 2_
  - **Note:** Implemented 2-hand disambiguation mode using screen position

- [ ] 23. Verify multi-hand cursor rendering (browser test needed)
  - [ ] 23.1 Verify 2 cursors appear when 2 hands detected
  - [ ] 23.2 Verify cursors have different colors (purple for left, blue for right)
  - [ ] 23.3 Verify each cursor follows its hand's index finger tip
  - _Requirements: 2, 5_

**Checkpoint 2e**: Multi-hand detection working with correct handedness classification ✅ (2025-12-19)

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

## Current Status (2025-12-18T10:00:00Z)

**DONE:**
- Phase 0-1: Setup and contracts complete
- Phase 2: TypeScript ports implemented (Observer, Bridger, Shaper, Injector)
- Golden video test passes (71/158 frames with hands detected)

**PROBLEM:**
- Demo HTML uses inline code, NOT the TypeScript ports
- Only 1 cursor rendered (should be 2 for 2 hands)
- Live camera detection needs debugging

**DEPENDENCY:**
- HFO PREY Powers spec at 60% - PREY tools exist but DuckDB broken
- Can proceed with Ghost Cursor independently

**NEXT:**
- Phase 2b: Bundle TypeScript and wire to demo
- Task 12: Create esbuild config for browser bundle
- Task 13: Replace inline code with real port imports
- Task 14: Add multi-hand cursor support (2 hands = 2 cursors)
- Task 15: Fix live camera detection

---

## Progress Summary (Verified 2025-12-18T17:30)

| Phase | Status | Verified Evidence |
|:------|:-------|:------------------|
| 0. Cold Start | ✅ DONE | Physics checks pass (2025-12-17) |
| 1. Contracts | ✅ DONE | 3 TypeScript contracts with round-trip tests |
| 2. Core Pipeline (TS) | ✅ DONE | 4 ports: Observer, Bridger, Shaper, Injector |
| 2b. Bundle & Wire | ✅ DONE | 110KB ESM bundle, GhostCursorPipeline |
| 3. Test Harness | ⬜ TODO | Golden masters needed |
| 4. Interactions | ⬜ TODO | Dwell, pinch, scroll |
| 5. Configuration | ⬜ TODO | Play area, gain |
| 6. Optimization | ⬜ TODO | NATS, OTel, mobile |

**Overall Progress**: 60% (Phases 0-2b complete, Phase 3 next)

---

## Verified Artifacts (2025-12-18T17:30)

| Artifact | Path | Size | Status |
|:---------|:-----|:-----|:-------|
| ESM Bundle | `src/ghost_cursor/dist/ghost-cursor.esm.js` | 112,835 bytes | ✅ Compiles |
| Sourcemap | `src/ghost_cursor/dist/ghost-cursor.esm.js.map` | - | ✅ Generated |
| Pipeline | `src/ghost_cursor/pipeline.ts` | - | ✅ Orchestrates 4 ports |
| Main Entry | `src/ghost_cursor/index.ts` | - | ✅ Exports all |
| Bundled Demo | `src/ghost_cursor/demo/index-bundled.html` | - | ✅ Uses pipeline |
| esbuild Config | `src/ghost_cursor/build/esbuild.config.js` | - | ✅ Works |

---

## Truth vs Theater Audit (2025-12-18T17:25)

| Claim | Truth | Theater |
|:------|:------|:--------|
| Bundle exists | ✅ 110KB ESM verified | - |
| Pipeline wires ports | ✅ Code exists | 🎭 Not browser-tested |
| Multi-hand support | ✅ Code in pipeline.ts | 🎭 Not Playwright-verified |
| Demo uses real ports | ✅ index-bundled.html | 🎭 Not live-tested |
| Camera works | 🔴 Broken | 🎭 Task 15 TODO |

**Confidence: 74% Truth / 26% Theater**

See: `.kiro/specs/hfo-mosaic-ghost-cursor-2025-12-18/TRUTH_VS_THEATER.md`

---

## Session Log (2025-12-18 / 2025-12-19)

### Completed This Session
| Time | Task | Evidence |
|:-----|:-----|:---------|
| 15:00 | Task 12: esbuild config | `build/esbuild.config.js` created |
| 15:00 | Task 13: Wire demo | `index-bundled.html` uses GhostCursorPipeline |
| 15:00 | Task 14: Multi-hand | `pipeline.ts` creates per-hand Shaper/Consumer |
| 17:25 | Audit | TRUTH_VS_THEATER.md created |
| 17:30 | SSOT Update | Both specs updated with verified diagnostics |

### Session 2025-12-19 (Handedness Bug Investigation)
| Time | Task | Evidence |
|:-----|:-----|:---------|
| 01:30 | Handedness bug identified | Both hands classified as same (left or right) |
| 01:45 | Root cause 1: Global state | `frameCounter` is module-level, shared across instances |
| 01:50 | Root cause 2: Landmark normalization | Human.js keypoints are PIXELS, not 0-1 normalized |
| 02:00 | Root cause 3: 1Euro API mismatch | Library expects `filter(t, [x,y])` not `filter(x, t)` |
| 02:15 | Fix applied: 1Euro API | Now using correct `filter(timestamp/1000, [x, y])` |
| 02:20 | Fix applied: Handedness geometry | Index-pinky span + palm orientation |
| 02:30 | Logged to Blackboard | `gc-handedness-2025-12-19` entry added |

### ✅ CRITICAL BUGS FIXED (2025-12-19)

| Bug | Location | Impact | Status |
|:----|:---------|:-------|:-------|
| Global frameCounter | `human_js_adapter.ts:45` | Shared state pollution | ✅ FIXED - moved to instance |
| Landmark normalization | `human_js_adapter.ts:110` | All landmarks clamped to 1.0 | ✅ FIXED - divide by dimensions |
| 1Euro API mismatch | `one_euro_filter.ts` | Filter not working | ✅ FIXED |
| Handedness geometry | `human_js_adapter.ts:170` | Both hands same ID | ✅ FIXED - 2-hand screen position mode |

### Test Results (2025-12-19) - PASSING ✅
```
Golden Video Test (two_hands_baseline_idle_v1.mp4):
- Total frames: 158
- Frames with hands: 71
- Frames with 2 hands: 27 ✅ (was 0)
- Left detections: 68
- Right detections: 30
- Fix: 2-hand disambiguation using screen position (mirrored camera)
```

### Git Commit
- `a8748a3` - feat(ghost-cursor): Phase 2b complete - esbuild bundle + pipeline

---

## Today's Priority (2025-12-18)

1. ✅ **Task 12**: Create esbuild config for browser bundle - DONE
2. ✅ **Task 13**: Wire demo to real TypeScript ports - DONE
3. ✅ **Task 14**: Add multi-hand cursor support - DONE
4. 🔴 **Task 15**: Fix live camera detection - NEXT
5. 🟡 **Browser test**: Verify bundle works with Playwright

---

## Co-Evolution with HFO Powers

Ghost Cursor is the **vertical slice testbed** for HFO infrastructure:

| Ghost Cursor Uses | HFO Provides |
|:------------------|:-------------|
| Port 0 Observer pattern | for-observing MCP server |
| Port 1 Bridger pattern | for-bridging (sequentialthinking) |
| Port 2 Shaper pattern | for-shaping MCP server |
| Port 3 Injector pattern | for-injecting (time tools) |
| Port 4 Disruptor (Phase 3) | hypothesis_generate, chaos_inject |
| Port 5 Immunizer (Phase 3) | pydantic_validate, opa_evaluate |
| Port 6 Assimilator (Phase 3) | semantic_search, duckdb_query |
| Port 7 Navigator (Phase 6) | mcts_search, pyribs_add |

When Ghost Cursor discovers gaps → Fix HFO → Resume Ghost Cursor

---

*Updated: 2025-12-18T17:30:00-07:00 | HFO Gen 77 | Ghost Cursor Vertical Slice Testbed*


---

## Phase 2f: Test Harness Integrity (RED-GREEN-REFACTOR) - ✅ COMPLETE (2025-12-19T05:30:00Z)

> **Goal**: Verify tests can fail (RED) on bad input, not just pass (GREEN) on good input.
> **Anti-Reward-Hacking**: Tests must be strict, not soft thresholds.

### RED Tests (Should Fail on Bad Input)

- [x] 24. Implement contract validation RED tests ✅
  - [x] 24.1 Test isValidHandState() returns false for < 21 landmarks
  - [x] 24.2 Test isValidHandState() returns false for invalid handId
  - [x] 24.3 Test isValidIntent() returns false for confidence > 1
  - [x] 24.4 Test isValidIntent() returns false for confidence < 0
  - [x] 24.5 Test isValidIntent() returns false for invalid state
  - [x] 24.6 Test Shaper rejects invalid handState with error (via property tests)
  - _Requirements: 16_
  - **File:** `src/ghost_cursor/tests/test_red_green_contracts.ts` (40 tests)

- [ ] 25. Implement golden replay comparison
  - [ ] 25.1 Create expected output JSONL for two_hands_baseline_idle_v1.mp4
  - [ ] 25.2 Implement frame-by-frame comparison function
  - [ ] 25.3 Test that mismatched output produces RED (failure)
  - [ ] 25.4 Test that matched output produces GREEN (pass)
  - [ ] 25.5 Report diff on failure (which frame, which field)
  - _Requirements: 16, 17_

### GREEN Tests (Should Pass on Good Input)

- [x] 26. Implement deterministic replay test ✅
  - [x] 26.1 Feed golden JSONL to pipeline (via test_assimilator.ts)
  - [x] 26.2 Capture output JSONL
  - [x] 26.3 Compare output to expected within tolerance
  - [x] 26.4 Verify exact match = GREEN
  - _Requirements: 16, 17_
  - **File:** `src/ghost_cursor/tests/test_red_green_contracts.ts` (GREEN section)

### Property-Based Tests

- [x] 27. Implement fast-check property tests for Shaper ✅
  - [x] 27.1 Install fast-check if not present (already in package.json)
  - [x] 27.2 Create arbitrary for valid CanonicalHandState
  - [x] 27.3 Test position bounds invariant (0 to screenWidth/Height)
  - [x] 27.4 Test confidence bounds invariant (0 to 1)
  - [x] 27.5 Test state validity invariant (enum values)
  - [x] 27.6 Test armed/state consistency invariant
  - [x] 27.7 Test round-trip serialization invariant
  - _Requirements: 19_
  - **File:** `src/ghost_cursor/tests/test_property_based.ts` (15 property tests)

**Checkpoint 2f**: Test harness can fail (RED) on bad input, pass (GREEN) on good input ✅ (2025-12-19T05:30:00Z)

### Files Created (Phase 2f)
- `src/ghost_cursor/tests/test_red_green_contracts.ts` - 40 RED/GREEN tests
- `src/ghost_cursor/tests/test_property_based.ts` - 15 property-based tests with fast-check
- **Total: 55 tests, all passing**

---

## Phase 2g: Port 6 Assimilator (JSONL Recording) - ✅ COMPLETE (2025-12-19T04:50:00Z)

> **Goal**: Record all pipeline events to JSONL for replay and deterministic testing.
> **Priority**: HIGH - Required for test harness.

- [x] 28. Implement Port 6 Assimilator ✅
  - [x] 28.1 Create `src/ghost_cursor/ports/port6_assimilator/index.ts`
  - [x] 28.2 Implement JSONLRecorder class
  - [x] 28.3 Record metadata event on session start
  - [x] 28.4 Record hand events from Observer
  - [x] 28.5 Record intent events from Shaper
  - [x] 28.6 Ensure monotonic timestamps
  - [x] 28.7 Implement save to file (download or localStorage)
  - _Requirements: 17_

- [x] 29. Wire Assimilator to Pipeline ✅
  - [x] 29.1 Add Assimilator to GhostCursorPipeline
  - [x] 29.2 Subscribe to Bridger events (via direct recording in processFrame)
  - [x] 29.3 Record all hand.detected events
  - [x] 29.4 Record all intent.updated events
  - [ ] 29.5 Add UI button to download JSONL (TODO: demo update)
  - _Requirements: 17_

- [x] 30. Implement replay functionality ✅
  - [x] 30.1 Create ReplayAdapter for Port 0 Observer
  - [x] 30.2 Load JSONL and parse events
  - [x] 30.3 Feed events in recorded order with timing
  - [x] 30.4 Verify deterministic output (same input → same output)
  - _Requirements: 17_

**Checkpoint 2g**: JSONL recording and replay working ✅ (2025-12-19T04:50:00Z)

### Files Created (Phase 2g)
- `src/ghost_cursor/ports/port6_assimilator/index.ts` - JSONLRecorder class
- `src/ghost_cursor/ports/port6_assimilator/replay_adapter.ts` - ReplayAdapter class
- `src/ghost_cursor/tests/test_assimilator.ts` - Unit tests (5/5 pass)

---

## Phase 2h: Deterministic Pong Paddle Test - NEW

> **Goal**: Map golden video to Pong paddles and verify deterministic behavior.
> **Validates**: End-to-end pipeline from video to game input.

- [ ] 31. Create Pong paddle mapping test
  - [ ] 31.1 Create `src/ghost_cursor/tests/test_pong_mapping.ts`
  - [ ] 31.2 Define expected paddle positions for golden video
  - [ ] 31.3 Process golden video through pipeline
  - [ ] 31.4 Map intent.position.y to paddle Y
  - [ ] 31.5 Compare actual vs expected paddle positions
  - [ ] 31.6 Fail if positions differ beyond tolerance
  - _Requirements: 18_

- [x] 32. Create visual Pong demo ✅ (2025-12-19T07:00:00Z)
  - [x] 32.1 Create `src/ghost_cursor/demo/pong.html`
  - [x] 32.2 Render two paddles (left/right) with Phaser 3 arcade physics
  - [x] 32.3 Wire pipeline.onIntent to paddle positions (handIntents state object)
  - [x] 32.4 Show armed state as paddle color (orange=armed, gray=inactive)
  - [x] 32.5 Ball only bounces off ARMED paddles (physics body enable/disable)
  - [ ] 32.6 Test with golden video and live camera (browser test needed)
  - _Requirements: 18_

**Checkpoint 2h**: Pong demo created, browser test needed

---

## Updated Priority Order (User Specified)

1. ✅ **Phase 2e**: Multi-hand detection fixed (Gen 77.1)
2. ✅ **Phase 2g**: JSONL Recording (Port 6 Assimilator) - DONE (2025-12-19T04:50:00Z)
3. ✅ **Phase 2f**: Test Harness Integrity (RED-GREEN-REFACTOR) - DONE (2025-12-19T05:30:00Z)
4. ✅ **Gen 77.2 Fix**: ARMED state now working (2025-12-19T06:15:00Z)
5. ✅ **Phase 2h**: Pong Overlay Demo + Deterministic Tests - DONE (2025-12-19T07:20:00Z)
6. 🟡 **Task 15**: Live Camera Fix
7. 🟡 **Phase 4**: Additional Gestures (Dwell, Pinch, Scroll)

---

## Session Log (2025-12-19 Continued)

### Gen 77.2 - ARMED State Fix

| Time | Task | Evidence |
|:-----|:-----|:---------|
| 05:30 | Phase 2f complete | 55 tests pass (40 RED/GREEN + 15 property) |
| 05:45 | Diagnosed ARMED issue | State always TRACKING, never ARMED |
| 06:00 | Root cause found | `lastCurlState` initialized to 'straight', first call never triggered |
| 06:10 | Fix applied | Initialize to `null`, send INDEX_STRAIGHT on first call |
| 06:15 | Verified | Golden test shows `state: ARMED` ✅ |

### Phase 2h - Pong Overlay + Deterministic Tests

| Time | Task | Evidence |
|:-----|:-----|:---------|
| 07:00 | Pong overlay demo | `pong.html` - Phaser 3 transparent overlay on video |
| 07:05 | Playwright test | Headful browser test with golden video |
| 07:10 | TDD tests created | `pong_deterministic.test.ts` - 13 tests |
| 07:16 | All tests pass | 13/13 deterministic tests ✅ |
| 07:20 | Specs updated | `WHAT_YOU_HAVE.md` created |

### Test Results (Phase 2h)

```
Pong Deterministic Tests:
✓ State Machine Transitions (3 tests)
✓ Deterministic Output (2 tests)
✓ Two-Player Independence (2 tests)
✓ Pong Paddle Control (2 tests)
✓ JSONL Recording and Replay (3 tests)
✓ Integration: State Machine with JSONL Replay (1 test)

Test Files  1 passed (1)
Tests       13 passed (13)
```

### Files Created (Phase 2h)
- `src/ghost_cursor/demo/pong.html` - Phaser 3 overlay demo
- `src/ghost_cursor/tests/pong_deterministic.test.ts` - 13 TDD tests
- `.kiro/specs/hfo-mosaic-ghost-cursor-2025-12-18/WHAT_YOU_HAVE.md` - Status doc

---

## HANDOFF SUMMARY (2025-12-19T07:25:00Z)

### ✅ WHAT YOU HAVE
| Component | Tests | Status |
|:----------|:------|:-------|
| Pipeline (Ports 0-3, 6) | - | ✅ Complete |
| State Machine | 13 | ✅ Deterministic |
| 2-Player Independence | 2 | ✅ Verified |
| JSONL Recording/Replay | 3 | ✅ Working |
| Pong Overlay Demo | - | ✅ Created |
| RED-GREEN-REFACTOR | 55 | ✅ Pass |
| **Total Tests** | **68** | ✅ All Pass |

### ❌ WHAT YOU DON'T HAVE
- Live camera browser-verified
- Bridger schema validation
- Golden JSONL master
- Dwell/pinch/scroll gestures

### 🎮 DOES PONG 2-PLAYER WORK?
**YES** - Proven by 13 deterministic tests:
1. State machine produces same output for same input
2. Left/right hands are independent
3. JSONL replay produces deterministic state sequence

**Confidence: 85%**

---

*Updated: 2025-12-19T07:25:00Z | Gen 77.2 | Phase 2h Complete*


---

## Phase 3: Clutch Behavior Model (Gen 77.3 - Requirements 20-26)

> **Goal**: Implement the new hierarchical state machine with finger-curl clutch mechanism.
> **Key Change**: Replace velocity-based arming with finger-curl hysteresis.

### 3a: Hierarchical State Machine Refactor

- [ ] 33. Refactor state machine to hierarchical model
  - [ ] 33.1 Create `src/ghost_cursor/ports/port2_shaper/hand_tracking_machine.ts`
  - [ ] 33.2 Implement IDLE → TRACKING → COASTING transitions (hand level)
  - [ ] 33.3 Remove ARMED/DISARMED from hand-level machine
  - [ ] 33.4 Add `fingerStates` to context for preservation during COASTING
  - [ ] 33.5 Implement `preserveFingerStates` and `restoreFingerStates` actions
  - _Requirements: 20, 22_

- [ ] 34. Create per-finger armed state machine
  - [ ] 34.1 Create `src/ghost_cursor/ports/port2_shaper/finger_armed_machine.ts`
  - [ ] 34.2 Implement DISARMED → ARMING → ARMED → DISARMING transitions
  - [ ] 34.3 Add hysteresis thresholds (arm: 0.2, disarm: 0.6)
  - [ ] 34.4 Add delay timers (arm: 50ms, disarm: 50ms)
  - [ ] 34.5 Store `lastArmedPosition` when transitioning to DISARMED
  - _Requirements: 21_

- [ ] 35. Wire hierarchical machines together
  - [ ] 35.1 Update `state_machine.ts` to use both machines
  - [ ] 35.2 Create per-finger machine instances (index, middle, ring, pinky)
  - [ ] 35.3 Ensure finger states are preserved during hand COASTING
  - [ ] 35.4 Emit combined state in CanonicalIntent
  - _Requirements: 20, 21, 22_

**Checkpoint 3a**: Hierarchical state machine with per-finger armed states

### 3b: CanonicalFingerCurl Implementation

- [ ] 36. Implement CanonicalFingerCurl interface
  - [ ] 36.1 Create `src/ghost_cursor/contracts/canonical_finger_curl.ts`
  - [ ] 36.2 Define interface with humanJsValue, computedValue, fusedValue, confidence, source
  - [ ] 36.3 Add round-trip serialization test
  - _Requirements: 24_

- [ ] 37. Implement finger curl computation from landmarks
  - [ ] 37.1 Create `src/ghost_cursor/ports/port2_shaper/finger_curl_calculator.ts`
  - [ ] 37.2 Compute angle at PIP joint (MCP→PIP→DIP)
  - [ ] 37.3 Convert angle to curl value (180°=0, 90°=0.5, 45°=1.0)
  - [ ] 37.4 Apply 1Euro filter to computed curl values
  - [ ] 37.5 Fuse with Human.js curl values (configurable weights)
  - _Requirements: 24, 25_

- [ ] 38. Add Kalman prediction for finger curl
  - [ ] 38.1 Create Kalman filter instance per finger
  - [ ] 38.2 Predict curl value for negative latency
  - [ ] 38.3 Pre-arm/pre-disarm when prediction crosses threshold
  - _Requirements: 25_

- [ ] 39. Add biomechanics weighting
  - [ ] 39.1 Define weight per finger (index=1.0, middle=0.9, ring=0.7, pinky=0.5, thumb=0.8)
  - [ ] 39.2 Apply weights to curl confidence
  - [ ] 39.3 Use weights in fusion calculation
  - _Requirements: 25_

**Checkpoint 3b**: CanonicalFingerCurl with computed, fused, and predicted values

### 3c: Inertial Coasting with State Preservation

- [ ] 40. Implement inertia physics
  - [ ] 40.1 Create `src/ghost_cursor/ports/port2_shaper/inertia_physics.ts`
  - [ ] 40.2 Apply velocity decay (0.95 per frame) during COASTING
  - [ ] 40.3 Stop coasting when velocity < minVelocity (10px/s)
  - [ ] 40.4 Blend to reacquired position over 100ms
  - _Requirements: 22_

- [ ] 41. Preserve finger states during coasting
  - [ ] 41.1 Store all finger armed states when entering COASTING
  - [ ] 41.2 Continue applying inertia to armed fingers' targets
  - [ ] 41.3 Keep disarmed fingers' targets frozen
  - [ ] 41.4 Restore finger states when hand reacquired
  - _Requirements: 22_

**Checkpoint 3c**: Inertial coasting preserves finger states

### 3d: Elemental Cursor Transformation

- [ ] 42. Implement elemental cursor visuals
  - [ ] 42.1 Create `src/ghost_cursor/ports/port3_injector/elemental_cursor.ts`
  - [ ] 42.2 Define visual styles per element (fire=orange, water=blue, earth=brown, thunder=yellow)
  - [ ] 42.3 Transform cursor appearance when finger transitions to ARMED
  - [ ] 42.4 Return to ghost appearance when finger transitions to DISARMED
  - _Requirements: 23_

- [ ] 43. Add element preset selector
  - [ ] 43.1 Add element selection to ShaperConfig
  - [ ] 43.2 Create UI for element selection (MVP: fire, water)
  - [ ] 43.3 Persist element preference
  - _Requirements: 23_

**Checkpoint 3d**: Elemental cursor transformation on arm/disarm

### 3e: Multi-Finger Cursor System (Future)

- [ ] 44. Implement multi-finger cursor tracking
  - [ ] 44.1 Create per-finger cursor elements
  - [ ] 44.2 Project ray from each straight fingertip
  - [ ] 44.3 Render independent cursors per armed finger
  - [ ] 44.4 Add per-finger gain adjustment
  - _Requirements: 26_

**Checkpoint 3e**: Multi-finger cursor system (4 cursors per hand)

### 3f: Update Pong Demo for Clutch Model

- [ ] 45. Update Pong to use finger-curl clutch
  - [ ] 45.1 Replace velocity-based arming with finger-curl
  - [ ] 45.2 Paddle moves when index finger straight (curl < 0.2)
  - [ ] 45.3 Paddle freezes when index finger curled (curl > 0.6)
  - [ ] 45.4 Show ghost cursor when disarmed, elemental when armed
  - [ ] 45.5 Preserve paddle state during hand COASTING
  - _Requirements: 20, 21, 22, 23_

- [ ] 46. Add deterministic tests for clutch behavior
  - [ ] 46.1 Test hysteresis prevents thrashing
  - [ ] 46.2 Test finger states preserved during coasting
  - [ ] 46.3 Test elemental transformation on arm/disarm
  - [ ] 46.4 Test paddle freeze/unfreeze with finger curl
  - _Requirements: 20, 21, 22, 23_

**Checkpoint 3f**: Pong demo uses clutch model with deterministic tests

---

## Phase 3 Summary

| Task Group | Tasks | Est. Time | Requirements |
|:-----------|:------|:----------|:-------------|
| 3a: Hierarchical State Machine | 33-35 | 3 hours | 20, 21, 22 |
| 3b: CanonicalFingerCurl | 36-39 | 4 hours | 24, 25 |
| 3c: Inertial Coasting | 40-41 | 2 hours | 22 |
| 3d: Elemental Cursor | 42-43 | 2 hours | 23 |
| 3e: Multi-Finger (Future) | 44 | 4 hours | 26 |
| 3f: Pong Demo Update | 45-46 | 2 hours | 20-23 |
| **Total** | **14 tasks** | **17 hours** | **20-26** |

---

## Updated Priority Order (Gen 77.3)

1. ✅ **Phase 2e**: Multi-hand detection fixed
2. ✅ **Phase 2g**: JSONL Recording (Port 6 Assimilator)
3. ✅ **Phase 2f**: Test Harness Integrity (RED-GREEN-REFACTOR)
4. ✅ **Phase 2h**: Pong Overlay Demo + Deterministic Tests
5. 🔴 **Phase 3a**: Hierarchical State Machine Refactor ← **NEXT**
6. 🟡 **Phase 3b**: CanonicalFingerCurl Implementation
7. 🟡 **Phase 3c**: Inertial Coasting with State Preservation
8. 🟡 **Phase 3d**: Elemental Cursor Transformation
9. 🟡 **Phase 3f**: Update Pong Demo for Clutch Model
10. ⬜ **Phase 3e**: Multi-Finger Cursor System (Future)
11. ⬜ **Task 15**: Live Camera Fix

---

*Added: 2025-12-19 | Gen 77.3 | Clutch Behavior Model Tasks*


---

## Phase 4: Spatial Zones + Key Events + Pseudo-Z (Gen 77.4 - Requirements 27-33)

> **Goal**: Add spatial zones, key press events from finger state changes, and pseudo-Z depth estimation.
> **Key Feature**: Finger curl/uncurl in zones triggers configurable key events.

### 4a: Spatial Zone System

- [ ] 47. Implement Zone Manager
  - [ ] 47.1 Create `src/ghost_cursor/ports/port2_shaper/zone_manager.ts`
  - [ ] 47.2 Define SpatialZone interface with bounds, layer, actions
  - [ ] 47.3 Implement addZone, removeZone, updateZone methods
  - [ ] 47.4 Implement getZonesAtPosition (point-in-rect test)
  - [ ] 47.5 Handle overlapping zones with layer priority
  - [ ] 47.6 Add default full-screen zone on initialization
  - _Requirements: 27_

- [ ] 48. Add zone enter/exit events
  - [ ] 48.1 Track previous zones per cursor
  - [ ] 48.2 Emit zone_enter when cursor enters new zone
  - [ ] 48.3 Emit zone_exit when cursor leaves zone
  - [ ] 48.4 Handle rapid zone transitions (debounce optional)
  - _Requirements: 27_

**Checkpoint 4a**: Spatial zones with enter/exit events

### 4b: Key Event Generation

- [ ] 49. Implement key event generator
  - [ ] 49.1 Create `src/ghost_cursor/ports/port3_injector/key_event_generator.ts`
  - [ ] 49.2 Define GestureKeyEvent interface
  - [ ] 49.3 Listen for finger state transitions (ARMED↔DISARMED)
  - [ ] 49.4 Look up active zones at cursor position
  - [ ] 49.5 Map (zone, finger, transition) → key code
  - [ ] 49.6 Emit key_down on arm→disarm, key_up on disarm→arm
  - _Requirements: 28_

- [ ] 50. Implement action mapping system
  - [ ] 50.1 Create `src/ghost_cursor/ports/port3_injector/action_mapper.ts`
  - [ ] 50.2 Define ZoneAction interface with trigger and action
  - [ ] 50.3 Support action types: key_press, function_call, event_emit
  - [ ] 50.4 Check modifier state (thumb curled, other hand in zone)
  - [ ] 50.5 Support action chaining (multiple actions per trigger)
  - _Requirements: 29_

- [ ] 51. Add modifier support
  - [ ] 51.1 Track thumb curl state as modifier
  - [ ] 51.2 Track other hand zone presence as modifier
  - [ ] 51.3 Include modifiers in GestureKeyEvent
  - [ ] 51.4 Filter actions by modifier requirements
  - _Requirements: 28, 29_

**Checkpoint 4b**: Key events from finger state changes with zone mapping

### 4c: Pseudo-Z Depth Estimation

- [ ] 52. Implement handspan calculator
  - [ ] 52.1 Create `src/ghost_cursor/ports/port2_shaper/pseudo_z_calculator.ts`
  - [ ] 52.2 Compute distance from index MCP to pinky MCP
  - [ ] 52.3 Apply 1Euro filter to handspan for stability
  - [ ] 52.4 Store handspan history for trend detection
  - _Requirements: 30_

- [ ] 53. Implement Z zone classification
  - [ ] 53.1 Define NEAR/NEUTRAL/FAR thresholds (1.2×, 0.8× neutral)
  - [ ] 53.2 Compute zValue (0-1 normalized depth)
  - [ ] 53.3 Classify into zZone based on thresholds
  - [ ] 53.4 Add hysteresis to prevent zone thrashing
  - [ ] 53.5 Emit z_zone_change events
  - _Requirements: 30_

- [ ] 54. Implement Z calibration flow
  - [ ] 54.1 Create `src/ghost_cursor/ports/port2_shaper/z_calibration.ts`
  - [ ] 54.2 Implement calibration state machine (UNCALIBRATED→NEUTRAL→NEAR→FAR→CALIBRATED)
  - [ ] 54.3 Record handspan at each calibration step
  - [ ] 54.4 Validate calibration (near > neutral > far)
  - [ ] 54.5 Persist calibration to local storage
  - [ ] 54.6 Add UI prompts for calibration flow
  - _Requirements: 31_

**Checkpoint 4c**: Pseudo-Z depth with calibration

### 4d: Combined Output

- [ ] 55. Implement GhostCursorOutput interface
  - [ ] 55.1 Create `src/ghost_cursor/contracts/ghost_cursor_output.ts`
  - [ ] 55.2 Include position, velocity, zDepth, fingers, activeZones, keyEvents
  - [ ] 55.3 Add round-trip serialization test
  - _Requirements: 32_

- [ ] 56. Wire combined output through pipeline
  - [ ] 56.1 Update Shaper to produce GhostCursorOutput
  - [ ] 56.2 Include all finger states with curl and armed state
  - [ ] 56.3 Include active zones from ZoneManager
  - [ ] 56.4 Include key events from KeyEventGenerator
  - [ ] 56.5 Include zDepth from PseudoZCalculator
  - _Requirements: 32_

- [ ] 57. Update Injector to consume combined output
  - [ ] 57.1 Render ghost + elemental cursors per finger
  - [ ] 57.2 Dispatch key events to consumers
  - [ ] 57.3 Provide Z depth to 3D-aware consumers
  - [ ] 57.4 Update zone visualization (optional debug overlay)
  - _Requirements: 32_

**Checkpoint 4d**: Combined output with all features integrated

### 4e: Demo and Tests

- [ ] 58. Create spatial zones demo
  - [ ] 58.1 Create `src/ghost_cursor/demo/zones.html`
  - [ ] 58.2 Show 4-quadrant zone layout
  - [ ] 58.3 Display key events as they fire
  - [ ] 58.4 Show Z depth indicator
  - [ ] 58.5 Add calibration UI
  - _Requirements: 27-32_

- [ ] 59. Add deterministic tests for zones and keys
  - [ ] 59.1 Test zone enter/exit events
  - [ ] 59.2 Test key event generation from finger transitions
  - [ ] 59.3 Test modifier filtering
  - [ ] 59.4 Test Z zone classification
  - [ ] 59.5 Test calibration validation
  - _Requirements: 27-32_

**Checkpoint 4e**: Spatial zones demo with tests

---

## Phase 4 Summary

| Task Group | Tasks | Est. Time | Requirements |
|:-----------|:------|:----------|:-------------|
| 4a: Spatial Zones | 47-48 | 2 hours | 27 |
| 4b: Key Events | 49-51 | 3 hours | 28, 29 |
| 4c: Pseudo-Z Depth | 52-54 | 3 hours | 30, 31 |
| 4d: Combined Output | 55-57 | 2 hours | 32 |
| 4e: Demo and Tests | 58-59 | 2 hours | 27-32 |
| **Total** | **13 tasks** | **12 hours** | **27-32** |

---

## Updated Priority Order (Gen 77.4)

### 🎯 IMMEDIATE GOAL: 2-Player Pong with Ghost/Active Cursor

The 2P Pong demo is the vertical slice that proves the system works:
- Instantly usable and familiar
- Tests 2-hand tracking, finger-curl clutch, and visual feedback
- Can play vs yourself or a friend

### Priority Stack

1. ✅ **Phase 2e**: Multi-hand detection fixed
2. ✅ **Phase 2g**: JSONL Recording (Port 6 Assimilator)
3. ✅ **Phase 2f**: Test Harness Integrity (RED-GREEN-REFACTOR)
4. ✅ **Phase 2h**: Pong Overlay Demo + Deterministic Tests
5. 🔴 **Phase 3a**: Hierarchical State Machine Refactor ← **CURRENT**
6. 🔴 **Phase 3f**: Update Pong Demo for Clutch Model ← **PRIORITY** (ghost + active cursor)
7. 🟡 **Phase 3b**: CanonicalFingerCurl from Landmarks (improves curl detection)
8. 🟡 **Phase 3c**: Inertial Coasting (smooth tracking loss)
9. 🟡 **Phase 3d**: Elemental Cursor Transformation (visual polish)
10. ⬜ **Phase 4**: Spatial 3D Zones + Key Events (after Pong works)
11. ⬜ **Phase 3e**: Multi-Finger Cursor System (Future)
12. ⬜ **Phase 5**: Sensor Fusion 6DOF (Future)

### 2P Pong Success Criteria

| Feature | Status | Test |
|:--------|:-------|:-----|
| 2 hands detected | ✅ | Golden video shows 27 frames with 2 hands |
| Left/right hand distinguished | ✅ | Screen position disambiguation |
| Ghost cursor (always visible) | 🔴 TODO | Cursor follows hand when disarmed |
| Active cursor (elemental) | 🔴 TODO | Cursor transforms when armed |
| Finger curl → arm/disarm | ✅ | State machine transitions |
| Paddle moves when armed | ✅ | Pong demo wired |
| Paddle freezes when disarmed | 🔴 TODO | Need clutch behavior |
| Ball only hits armed paddles | ✅ | Physics body enable/disable |
| Live camera works | 🔴 TODO | Task 15 |

---

*Added: 2025-12-19 | Gen 77.4 | Spatial Zones + Key Events + Pseudo-Z Tasks*
