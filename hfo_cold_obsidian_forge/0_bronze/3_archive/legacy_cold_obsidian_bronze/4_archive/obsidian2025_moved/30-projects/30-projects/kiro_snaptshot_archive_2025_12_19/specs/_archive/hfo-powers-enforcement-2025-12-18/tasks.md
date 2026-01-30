# Implementation Plan: HFO Powers Enforcement

## Phase 1: Power Structure (DONE from Dec 17)

- [x] 1. Fix HFO Power Structure ✅
  - [x] 1.1 Rename power.json to mcp.json
  - [x] 1.2 Update POWER.md with proper frontmatter
  - [x] 1.3 Write property test for power structure validity (6 tests)
  - [x] 1.4 Write property test for MCP config validity (8 tests)
  - _Requirements: 1.1, 1.2, 1.5_

- [x] 2. Create Enforcement Hooks (WEAK - reminders only) ✅
  - [x] 2.1 Create session-start hook (reminder, not blocking)
  - [x] 2.2 Create search-before-create hook (manual button, not automatic)
  - [x] 2.3 Verify blackboard-handoff hook exists
  - [x] 2.4 Write property test for hook format validity (9 tests)
  - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 3. Checkpoint - Power structure verified ✅
  - 25 tests pass

---

## Phase 2: Strengthen Enforcement (NEW - Dec 18)

- [ ] 4. Make search-before-create AUTOMATIC
  - [ ] 4.1 Change hook trigger from `manual` to `file_created`
    - Hook should fire BEFORE file creation, not after
    - _Requirements: 2.2_
  - [ ] 4.2 Add blocking language to hook prompt
    - Change "you should search" to "you MUST search or operation will be rejected"
    - _Requirements: 2.2_
  - [ ] 4.3 Test automatic triggering
    - Create a test file, verify hook fires
    - _Requirements: 2.2_

- [ ] 5. Add MUST language to steering files
  - [ ] 5.1 Update toolbox.md with blocking language
    - Change "should" to "MUST" for search-before-create
    - _Requirements: 5.1_
  - [ ] 5.2 Update canalization.md with enforcement rules
    - Add "HARD RULES" section with blocking requirements
    - _Requirements: 5.2_
  - [ ] 5.3 Update hfo-context.md anti-hallucination checklist
    - Make checklist items mandatory, not optional
    - _Requirements: 5.3_

- [ ] 6. Fix for-assimilating DuckDB server
  - [ ] 6.1 Diagnose why for-assimilating shows 0 tools
    - Check mcp.json configuration
    - Check server startup logs
    - _Requirements: 3.4_
  - [ ] 6.2 Fix server configuration
    - Update mcp.json with correct settings
    - _Requirements: 3.4_
  - [ ] 6.3 Verify DuckDB tools accessible
    - Test read_query, list_tables, describe_table
    - _Requirements: 3.4_

- [ ] 7. Checkpoint - Verify enforcement strengthened
  - Hooks trigger automatically
  - Steering uses MUST language
  - DuckDB server working

---

## Phase 3: Measure Enforcement Effectiveness (NEW)

- [ ] 8. Create enforcement metrics
  - [ ] 8.1 Add logging to hooks
    - Log when hooks fire and agent response
    - _Requirements: 2.5_
  - [ ] 8.2 Track search-before-create compliance
    - Count: hook fired, search performed, search skipped
    - _Requirements: 2.5_
  - [ ] 8.3 Create daily enforcement report
    - Summary of hook triggers and compliance rate
    - _Requirements: 2.5_

- [ ] 9. Final Checkpoint - Enforcement verified
  - Automatic hooks working
  - Compliance metrics tracked
  - DuckDB server operational

---

## Progress Summary

| Phase | Status | Notes |
|:------|:-------|:------|
| 1. Power Structure | ✅ DONE | 25 tests pass |
| 2. Strengthen Enforcement | 🔴 TODO | Hooks are weak reminders |
| 3. Measure Effectiveness | 🔴 TODO | No metrics yet |

**Overall Progress**: 40% (Phase 1 complete, Phases 2-3 pending)

**Key Issue**: Hooks are reminders, not blockers. Agent can ignore them.

---

*Updated: 2025-12-18 | Gen 77 | HFO Powers Enforcement*
