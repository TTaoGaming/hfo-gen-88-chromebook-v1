---
hfo:
  gen: 78
  ts: 2025-12-19T19:08:48.201Z
  port: 6
  role: REMEMBER
  trigram: ☱
  pillar: Assimilator
  greek: Μνήμη
  phase: PERCEIVE
  status: active
  desc: tasks
---

# Implementation Plan: HFO Mosaic Gesture Cursor

## Overview

This plan implements the Mosaic Cursor Visualization vertical slice with Cold Stigmergy headers. Focus is on position tracking with 3-layer visualization (raw → smooth → predictive) and fire particle effects.

---

## Phase 0: Cold Stigmergy Header Infrastructure

- [x] 1. Create Cold Stigmergy Header Contract ✅
  - [x] 1.1 Create `cold_stigmergy_header.ts` in contracts/ ✅
    - Define PORT_ONTOLOGY constant
    - Define ColdStigmergyHeader interface
    - Implement deriveSubject() function
    - Implement validateOntology() function
    - _Requirements: 0.0.1-0.0.3_

  - [x] 1.2 Write property test for header round-trip ✅
    - **Property 1: Cold Stigmergy Header Round-Trip**
    - **Validates: Requirements 0.0.1.3, 0.0.1.5**

  - [x] 1.3 Write property test for port ontology consistency ✅
    - **Property 2: Port Ontology Consistency**
    - **Validates: Requirements 0.0.3.1-0.0.3.5**

- [x] 2. Implement Header Parser (Port 1 Bridger) ✅
  - [x] 2.1 Create `cold_stigmergy_parser.ts` in port1_bridger/ ✅
    - Implement parseTypeScriptHeader() with regex + YAML
    - Implement parseMarkdownHeader() with frontmatter
    - Implement generateTypeScriptHeader()
    - Implement generateMarkdownHeader()
    - _Requirements: 0.0.1.1-0.0.1.5_

- [x] 3. Implement Header Validator (Port 5 Immunizer) ✅
  - [x] 3.1 Create `header_validator.ts` in port5_immunizer/ ✅
    - Implement validateHeader() with error codes
    - Implement validateDirectory() for batch validation
    - _Requirements: 0.0.5.1-0.0.5.5_

  - [x] 3.2 Write property test for validation error detection ✅
    - **Property 4: Validation Error Detection**
    - **Validates: Requirements 0.0.5.2-0.0.5.4**

- [x] 4. Checkpoint - Ensure all tests pass ✅
  - 295 vitest tests passing + 22 cold stigmergy property tests

---

## Phase 0: Mosaic Cursor Visualization (P0 Vertical Slice)

- [x] 5. Create Mosaic Cursor Scene ✅
  - [x] 5.1 Create `MosaicCursorScene.ts` in port3_injector/apps/ ✅
    - Extend Phaser.Scene with transparent background
    - Initialize 3 cursor layers (raw, smooth, predictive)
    - Set up Phaser physics for coasting
    - _Requirements: 0.1.0, 0.1.6_

  - [x] 5.2 Implement raw cursor layer (gray dot) ✅
    - Create gray arc at fingertip position
    - No smoothing, direct Human.js passthrough
    - Fade on low confidence
    - _Requirements: 0.1.2_

  - [x] 5.3 Write property test for raw cursor position fidelity ✅
    - **Property 5: Raw Cursor Position Fidelity**
    - **Validates: Requirements 0.1.2.2**

- [x] 6. Implement Smooth Cursor Layer ✅
  - [x] 6.1 Create smooth cursor with 1Euro filter ✅
    - Blue arc, 10px above raw
    - Apply 1Euro filter (tuned responsive)
    - Show state label (IDLE/TRACKING/COASTING)
    - _Requirements: 0.1.3_

  - [x] 6.2 Implement coasting with Phaser physics ✅
    - Enable physics body on smooth cursor
    - Set drag coefficient (0.95)
    - Preserve velocity on confidence drop
    - Resume tracking on confidence recovery
    - _Requirements: 0.1.3.4-0.1.3.5_

  - [x] 6.3 Write property test for coasting state transition ✅
    - **Property 6: Coasting State Transition**
    - **Validates: Requirements 0.1.3.4**

  - [x] 6.4 Write property test for coasting preserves velocity ✅
    - **Property 10: Coasting Preserves Velocity**
    - **Validates: Coasting Behavior**

- [x] 7. Checkpoint - 312 vitest tests passing ✅

- [x] 8. Implement Predictive Cursor Layer (Fire) ✅
  - [x] 8.1 Create Kalman filter for prediction ✅
    - Input: smooth cursor position (never raw!)
    - Output: predicted position (100ms ahead default)
    - Tunable prediction horizon
    - _Requirements: 0.1.4.2_

  - [x] 8.2 Write property test for predictive never sees raw ✅
    - **Property 9: Predictive Never Sees Raw**
    - **Validates: Pipeline Contracts**

  - [x] 8.3 Implement fire particle emitter ✅
    - Phaser particle emitter at predictive position
    - 20px above raw cursor
    - Orange/red color palette
    - _Requirements: 0.1.4.1, 0.1.4.3_

  - [x] 8.4 Implement inverse velocity fire intensity ✅
    - Low velocity = big fire (ember glow)
    - High velocity = small fire + trail
    - Polypath trailing effect
    - _Requirements: 0.1.4.4-0.1.4.5_

  - [x] 8.5 Write property test for fire intensity inverse velocity ✅
    - **Property 7: Fire Intensity Inverse Velocity**
    - **Validates: Requirements 0.1.4.4**

- [x] 9. Implement Fire Config Panel ✅
  - [x] 9.1 Create WinBox settings panel ✅
    - Particle count slider (10-100)
    - Trail length slider
    - Ember glow radius slider
    - Prediction horizon slider (50-500ms)
    - Color temperature toggle
    - _Requirements: 0.1.5_

  - [x] 9.2 Persist config to localStorage ✅
    - Save on change
    - Load on startup
    - Reset to defaults button
    - _Requirements: 0.1.5.6_

- [x] 10. Checkpoint - 312 vitest tests passing ✅

---

## Phase 0: Integration

- [x] 11. Create Full-Screen Camera Background ✅
  - [x] 11.1 Update app.html with full-screen WinBox ✅
    - Camera feed as background
    - Mirrored horizontally (scaleX: -1)
    - Phaser canvas overlay
    - _Requirements: 0.1.0_

  - [x] 11.2 Wire Human.js to Mosaic Cursor Scene ✅
    - Connect Human.js hand detection
    - Extract index fingertip position
    - Feed to 3-layer pipeline
    - Created `mosaic_cursor_demo.html` standalone demo
    - _Requirements: 0.1.1_

- [x] 12. Seed Cold Stigmergy Headers ✅ (Done in previous session)
  - [x] 12.1 Create seeding script ✅
    - Scan src/ghost_cursor/**/*.ts
    - Detect port from path
    - Generate header with correct ontology
    - Insert at top of file
    - _Requirements: 0.0.1-0.0.3_

  - [x] 12.2 Run seeding script on codebase ✅
    - Seeded 136 files across src/ghost_cursor/, HFO_buds/, .kiro/specs/, .kiro/steering/
    - Verify with validator
    - _Requirements: 0.0.5_

- [x] 13. Checkpoint - 312 vitest tests passing ✅

---

## Handoff Summary

**Key Files to Create**:
1. `src/ghost_cursor/contracts/cold_stigmergy_header.ts`
2. `src/ghost_cursor/ports/port1_bridger/cold_stigmergy_parser.ts`
3. `src/ghost_cursor/ports/port5_immunizer/header_validator.ts`
4. `src/ghost_cursor/ports/port3_injector/apps/MosaicCursorScene.ts`
5. `src/ghost_cursor/ports/port3_injector/fire_config.ts`
6. `scripts/seed_cold_stigmergy.ts`

**Key Concepts**:
- Raw → Smooth → Predictive (strict layering)
- Predictive NEVER sees raw
- Coasting uses Phaser physics (inertia + drag)
- Fire intensity is INVERSE to velocity
- 100ms default prediction horizon

**Property Tests**:
1. Header round-trip
2. Port ontology consistency
4. Validation error detection
5. Raw cursor position fidelity
6. Coasting state transition
7. Fire intensity inverse velocity
9. Predictive never sees raw
10. Coasting preserves velocity

---

*HFO Gen 78 | Mosaic Gesture Cursor Tasks | 2025-12-20T21:00:00Z*
