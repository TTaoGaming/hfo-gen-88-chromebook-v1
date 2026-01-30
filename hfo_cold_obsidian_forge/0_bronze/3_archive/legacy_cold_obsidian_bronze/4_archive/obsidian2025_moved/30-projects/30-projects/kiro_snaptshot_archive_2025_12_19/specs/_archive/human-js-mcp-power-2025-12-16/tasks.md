# Tasks: Human.js MCP Server & Kiro Power

## Phase 1: Power Structure Setup

- [x] 1. Create Kiro Power directory structure ✅
  - [x] 1.1 Create `.kiro/powers/human-js/` directory
  - [x] 1.2 Create `POWER.md` with frontmatter and documentation
  - [x] 1.3 Create `mcp.json` with server configuration
  - [x] 1.4 Create `package.json` with dependencies
  - _Requirements: 8_

- [x] 2. Create steering files ✅
  - [x] 2.1 Create `steering/getting-started.md`
  - [x] 2.2 Create `steering/hand-tracking.md`
  - [x] 2.3 Create `steering/gesture-recognition.md`
  - _Requirements: 8_

**Checkpoint 1**: ✅ Power structure exists, can be listed via `kiroPowers(action="list")`

---

## Phase 2: MCP Server Core

- [x] 3. Create MCP server skeleton ✅
  - [x] 3.1 Create `src/human_mcp_server.ts`
  - [x] 3.2 Initialize Human.js with configurable backend
  - [x] 3.3 Set up MCP Server with tool registration
  - [x] 3.4 Implement stdio transport
  - _Requirements: 1_

- [x] 4. Implement detection tools ✅
  - [x] 4.1 Implement `human_detect` tool
  - [x] 4.2 Implement `human_warmup` tool
  - [x] 4.3 Add result caching
  - _Requirements: 2_

**Checkpoint 2**: ✅ Server starts, `human_detect` returns results

---

## Phase 3: Hand Tracking Tools

- [x] 5. Implement hand tracking tools ✅
  - [x] 5.1 Implement `human_get_hands` tool
  - [x] 5.2 Implement `human_get_hand` tool (single hand by ID)
  - [x] 5.3 Implement `human_get_finger` tool (curl, direction, keypoints)
  - [x] 5.4 Implement `human_get_keypoints` tool (all 21 points)
  - _Requirements: 3_

**Checkpoint 3**: ✅ Hand tracking tools return Human.js data

---

## Phase 4: Gesture Tools

- [x] 6. Implement gesture tools ✅
  - [x] 6.1 Implement `human_get_gestures` tool
  - [x] 6.2 Implement `human_get_hand_gestures` tool (filtered)
  - [x] 6.3 Implement `human_check_gesture` tool
  - _Requirements: 4_

**Checkpoint 4**: ✅ Gesture tools detect victory, thumbs up, etc.

---

## Phase 5: Smoothing & Additional Tools

- [x] 7. Implement smoothing tools ✅
  - [x] 7.1 Implement `human_interpolate` tool (human.next())
  - [x] 7.2 Implement `human_configure_smoothing` tool
  - _Requirements: 5_

- [x] 8. Implement face tools ✅
  - [x] 8.1 Implement `human_get_faces` tool
  - [ ] 8.2 Implement `human_match_face` tool (deferred - not in MVP)
  - [ ] 8.3 Implement `human_compare_faces` tool (deferred - not in MVP)
  - _Requirements: 6_

- [x] 9. Implement body tools ✅
  - [x] 9.1 Implement `human_get_bodies` tool
  - [ ] 9.2 Implement `human_get_body_keypoints` tool (deferred - not in MVP)
  - _Requirements: 7_

**Checkpoint 5**: ✅ Core Human.js features exposed via MCP (14 tools)

---

## Phase 6: HFO Integration

- [x] 10. Implement HFO integration ✅
  - [x] 10.1 Implement `human_to_canonical` tool
  - [x] 10.2 Add coordinate normalization
  - [x] 10.3 Map Human.js gestures to CanonicalHandState
  - _Requirements: 9_

- [ ] 11. Test with Ghost Cursor spec
  - [ ] 11.1 Verify CanonicalHandState format matches Ghost Cursor Observer
  - [ ] 11.2 Test data flow through Bridger
  - [ ] 11.3 Verify gesture pass-through works
  - _Requirements: 9_

**Checkpoint 6**: ✅ `human_to_canonical` implemented, integration testing pending

---

## Phase 7: Testing & Documentation

- [ ] 12. Add tests
  - [ ] 12.1 Unit tests for tool handlers
  - [ ] 12.2 Integration test with sample image
  - [ ] 12.3 Golden master test for deterministic output

- [x] 13. Finalize documentation ✅
  - [x] 13.1 Update API reference doc (docs/human-js-api-reference-2025-12-17.md)
  - [x] 13.2 Add usage examples to steering files
  - [x] 13.3 Document environment variables

**Checkpoint 7**: Documentation complete, tests pending

---

## Implementation Summary

| Phase | Status | Tools Implemented |
|-------|--------|-------------------|
| 1. Power Structure | ✅ DONE | - |
| 2. MCP Server Core | ✅ DONE | human_detect, human_warmup |
| 3. Hand Tracking | ✅ DONE | human_get_hands, human_get_hand, human_get_finger, human_get_keypoints |
| 4. Gesture Tools | ✅ DONE | human_get_gestures, human_get_hand_gestures, human_check_gesture |
| 5. Smoothing | ✅ DONE | human_interpolate, human_configure_smoothing |
| 6. HFO Integration | ✅ DONE | human_to_canonical |
| 7. Testing | 🟡 PARTIAL | Documentation done, tests pending |

**Total: 14 tools implemented**

---

## Artifacts Created

- `.kiro/powers/human-js/POWER.md` - Power documentation
- `.kiro/powers/human-js/package.json` - Dependencies
- `.kiro/powers/human-js/mcp.json` - MCP configuration
- `.kiro/powers/human-js/tsconfig.json` - TypeScript config
- `.kiro/powers/human-js/src/human_mcp_server.ts` - MCP server source
- `.kiro/powers/human-js/dist/human_mcp_server.js` - Compiled server
- `.kiro/powers/human-js/steering/getting-started.md` - Quick start guide
- `.kiro/powers/human-js/steering/hand-tracking.md` - 21 keypoint reference
- `.kiro/powers/human-js/steering/gesture-recognition.md` - Gesture guide
- `docs/human-js-api-reference-2025-12-17.md` - Comprehensive API reference

---

## Notes

- Human.js v3.3.6 installed and verified
- MCP server compiles and runs in Node.js
- Result caching implemented (matches Human.js `human.result` pattern)
- **Key principle**: Pass-through, not reinvent - Human.js already provides finger curl, direction, and gestures

---

*Tasks Updated: 2025-12-17 | HFO Gen 76 | Human.js MCP Power*
