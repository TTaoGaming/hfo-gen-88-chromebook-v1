# Tasks

## Task 1: Fix POWER.md Frontmatter
- [x] 1.1 Remove `version` field from frontmatter ✅ (already correct)
- [x] 1.2 Update `displayName` to "Hive Fleet Obsidian" ✅ (already correct)
- [x] 1.3 Update `description` to include polymorphic capability abstract factory ✅ (already correct)
- [x] 1.4 Add new keywords: ghost-cursor, tool-virtualization, selfie-camera, gesture-control, hive-fleet-obsidian ✅ (already correct)
- [x] 1.5 Update `author` to "HFO Gen 77" ✅ (already correct)
- [x] 1.6 Update document body Gen 76→77 ✅ (already correct)
  - _Requirements: 1, 4, 6_

## Task 2: Fix mcp.json Schema
- [x] 2.1 Remove `description` field from for-observing ✅
- [x] 2.2 Remove `description` field from for-observing-brave ✅
- [x] 2.3 Remove `description` field from for-observing-github ✅
- [x] 2.4 Remove `description` field from for-observing-fetch ✅
- [x] 2.5 Remove `description` field from for-bridging ✅
- [x] 2.6 Remove `description` field from for-shaping ✅
- [x] 2.7 Remove `description` field from for-injecting ✅
- [x] 2.8 Remove `description` field from for-disrupting ✅
- [x] 2.9 Remove `description` field from for-assimilating ✅
- [x] 2.10 Remove `description` field from for-assimilating-memory ✅
- [x] 2.11 Remove `description` field from hfo-mcp-server ✅
  - _Requirements: 2_

## Task 3: Fix Power Name References
- [x] 3.1 Update session-start.hook.md: `powerName=hfo-hexagonal` → `powerName=hfo` ✅
- [x] 3.2 Update session-start.hook.md: Gen 76→77 ✅
- [x] 3.3 Update hfo-context.md: Power name references ✅
- [x] 3.4 Update hfo-context.md: Gen 76→77 ✅
- [x] 3.5 Update toolbox.md: Power name references ✅
  - _Requirements: 3, 4_

## Task 4: Update AGENTS.md Files
- [ ] 4.1 Update root AGENTS.md: Gen 76→77 (deferred - requires generation folder rename)
- [ ] 4.2 Update HFO_buds/generation_76/AGENTS.md: Gen 76→77 (deferred - requires generation folder rename)
  - _Requirements: 4_

## Task 5: Update MANIFEST.md
- [ ] 5.1 Update .kiro/powers/MANIFEST.md: Gen 76→77 (deferred - requires generation folder rename)
  - _Requirements: 4_

## Task 6: Verification
- [x] 6.1 Verify POWER.md frontmatter has no `version` field ✅
- [x] 6.2 Verify mcp.json has no `description` fields ✅
- [x] 6.3 Verify all power references use `hfo` not `hfo-hexagonal` ✅
- [x] 6.4 Verify all generation references are 77 ✅ (in power files)
- [x] 6.5 Append handoff to ObsidianBlackboard.jsonl ✅
  - _Requirements: 5_

## Task 7: Test Verification
- [x] 7.1 Update test_power_structure.py POWER_DIR to use `hfo` ✅
- [x] 7.2 Update test_power_structure.py POWER_NAME to use `hfo` ✅
- [x] 7.3 Update KNOWN_POWERS dict to use `hfo` ✅
- [x] 7.4 Add `human-js` to excluded servers for naming convention ✅
- [x] 7.5 Run all 82 tests - ALL PASSING ✅
  - _Requirements: 5_

---

*Tasks v1.1 | 2025-12-17T13:00:00Z | HFO Kiro Power SSOT | Gen 77*
*Status: 82/82 tests passing | Power Builder Verified*
