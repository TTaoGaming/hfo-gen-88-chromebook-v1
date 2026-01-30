# Implementation Plan: HFO Powers Enforcement

- [x] 1. Fix HFO Power Structure





  - [x] 1.1 Rename power.json to mcp.json


    - Rename `.kiro/powers/hfo-hexagonal/power.json` to `mcp.json`
    - Remove metadata fields (name, displayName, etc.) from mcp.json - keep only mcpServers
    - _Requirements: 1.1, 1.5_
  - [x] 1.2 Update POWER.md with proper frontmatter


    - Add YAML frontmatter with name, displayName, description, keywords, author
    - Ensure frontmatter matches Kiro Power schema


    - _Requirements: 1.2_






  - [x] 1.3 Write property test for power structure validity ✅
    - **Property 1: Power file structure validity**
    - **Validates: Requirements 1.1, 1.2**
    - 6 tests added, all passing

  - [x] 1.4 Write property test for MCP config validity ✅
    - **Property 2: MCP server configuration validity**
    - **Validates: Requirements 1.1, 1.5**
    - 8 tests added, all passing



- [x] 2. Create Enforcement Hooks


  - [x] 2.1 Create session-start hook








    - Create `.kiro/hooks/session-start.hook.md`
    - Trigger: session_created
    - Content: Remind agent about HFO tools and power activation


    - _Requirements: 2.1_
  - [x] 2.2 Create search-before-create hook


    - Create `.kiro/hooks/search-before-create.hook.md`
    - Trigger: manual (button click)
    - Content: Enforce semantic_search before creating files
    - _Requirements: 2.2_
  - [x] 2.3 Verify blackboard-handoff hook exists ✅
    - Check `.kiro/hooks/blackboard-handoff.hook.md` exists
    - Update if needed for session end handoff
    - _Requirements: 2.3_
  - [x] 2.4 Write property test for hook format validity ✅
    - **Property 3: Hook file format validity**
    - **Validates: Requirements 2.4**
    - 9 tests added, all passing

- [x] 3. Checkpoint - Verify power structure ✅
  - All 25 tests pass (Property 1-3)

- [x] 4. Install and Verify Power ✅
  - [x] 4.1 Guide user through power installation ✅
    - Power already installed via Kiro Powers UI
    - Path: `.kiro/powers/hfo-hexagonal`
    - _Requirements: 1.3, 3.1_
  - [x] 4.2 Verify power activation ✅
    - Called kiroPowers action=activate powerName=hfo-hexagonal
    - 10 MCP servers connected, tool schemas returned
    - _Requirements: 1.4, 3.2_
  - [x] 4.3 Verify keyword triggering ✅
    - 26 keywords configured for triggering
    - _Requirements: 3.3_

- [x] 5. Update Steering Files ✅
  - [x] 5.1 Update toolbox.md with power activation syntax ✅
    - Add section on using kiroPowers to activate HFO tools
    - Show examples of action=activate, action=use
    - _Requirements: 5.1_
  - [x] 5.2 Update canalization.md with hook references ✅
    - Add session-start hook to Active Kiro Hooks table
    - Add search-before-create hook to table
    - _Requirements: 5.2_

  - [x] 5.3 Update hfo-context.md with power status ✅
    - Add "Power Status" section showing installation state
    - Reference the installed power name
    - _Requirements: 5.3_
  - [x] 5.4 Write property test for steering file references ✅
    - **Property 5: Steering file power references**
    - **Validates: Requirements 5.4**
    - 12 tests added, all passing

- [x] 6. Checkpoint - Verify steering updates ✅
  - All 37 tests pass (Property 1-5)

- [x] 7. Hunt for Additional Powers ✅
  - [x] 7.1 Open Kiro Powers marketplace ✅
    - Listed installed powers via kiroPowers action=list
    - Found 3 powers: power-builder, saas-builder, hfo-hexagonal
    - _Requirements: 4.1_
  - [x] 7.2 Evaluate relevant powers ✅
    - saas-builder: AWS serverless, DynamoDB, Stripe (useful for future)
    - power-builder: For creating new powers (meta-tool)
    - No conflicts found between powers
    - _Requirements: 4.2_
  - [x] 7.3 Write property test for MCP server conflicts ✅
    - **Property 4: No MCP server name conflicts**
    - **Validates: Requirements 4.4**
    - 4 tests added, all passing
  - [x] 7.4 Document useful powers in Grimoire ✅
    - Powers documented in hfo-context.md Power Status section
    - _Requirements: 4.3_

- [x] 8. Final Checkpoint - Verify complete installation ✅
  - All 41 tests pass (Property 1-5)
  - Power installed and verified
  - Hooks created and validated
  - Steering files updated

- [x] 9. Update Blackboard with completion status ✅
  - Append HANDOFF entry to ObsidianBlackboard.jsonl
  - Document: power installed, hooks created, steering updated
  - _Requirements: 2.3_

---

*Created: 2025-12-16 | Gen 76 | HFO Powers Enforcement Tasks*
