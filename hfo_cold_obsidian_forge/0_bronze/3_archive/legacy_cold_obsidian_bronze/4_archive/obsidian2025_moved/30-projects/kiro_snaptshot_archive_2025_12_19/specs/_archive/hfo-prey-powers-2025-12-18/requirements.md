# Requirements Document: HFO PREY Powers Architecture

## Introduction

This spec defines a 4-power architecture for HFO based on the PREY workflow (Perceive, React, Execute, Yield) aligned with JADC2 Mosaic Warfare's Sense-Make Sense-Act loop. Each power maps to specific hexagonal ports and enforces architectural patterns to prevent "AI slop" - blind code generation without context.

## Glossary

- **PREY**: Perceive-React-Execute-Yield workflow for AI-assisted development
- **JADC2**: Joint All-Domain Command and Control - military decision framework
- **Mosaic Warfare**: Distributed, composable warfare doctrine
- **HFO**: Hive Fleet Obsidian - the 8-port hexagonal architecture
- **Port**: One of 8 hexagonal adapter roles (Observer through Navigator)
- **Power**: A Kiro power package with MCP servers, steering, and enforcement
- **Stigmergy**: Indirect coordination through environment modification
- **Immunizer**: Port 5 - the validation/enforcement gatekeeper

## Requirements

### Requirement 1: PREY Power Structure

**User Story:** As a developer, I want 4 distinct powers aligned with the PREY workflow, so that each phase of development has appropriate tools and enforcement.

#### Acceptance Criteria

1. WHEN the system initializes THEN the system SHALL provide exactly 4 powers: hfo-perceive, hfo-react, hfo-execute, hfo-yield
2. WHEN a power is activated THEN the system SHALL load only the MCP servers relevant to that PREY phase
3. WHEN multiple powers are needed THEN the system SHALL allow concurrent activation without conflict
4. WHEN a power is activated THEN the system SHALL display the PREY phase and port mapping

### Requirement 2: hfo-perceive Power (Sense)

**User Story:** As a developer, I want a Perceive power that handles all observation and data gathering, so that I have complete situational awareness before acting.

#### Acceptance Criteria

1. WHEN hfo-perceive is activated THEN the system SHALL provide Port 0 (Observer) tools: for-observing, brave, github, fetch
2. WHEN searching for information THEN the system SHALL enforce the anti-hallucination protocol (search Silver first)
3. WHEN reading files THEN the system SHALL log the observation to stigmergy
4. WHEN the keyword "search", "read", "fetch", "observe", or "perceive" appears THEN the system SHALL suggest hfo-perceive activation
5. IF hfo-perceive is not active THEN the system SHALL block read operations from other powers

### Requirement 3: hfo-react Power (Make Sense)

**User Story:** As a developer, I want a React power that handles reasoning and connection-making, so that I can plan before executing.

#### Acceptance Criteria

1. WHEN hfo-react is activated THEN the system SHALL provide Port 1 (Bridger) tools: for-bridging, sequential-thinking, NATS publish/subscribe
2. WHEN reasoning about a problem THEN the system SHALL use sequential thinking to break it down
3. WHEN connecting components THEN the system SHALL use NATS stigmergy for coordination
4. WHEN the keyword "reason", "plan", "connect", "bridge", or "react" appears THEN the system SHALL suggest hfo-react activation
5. IF hfo-perceive was not activated first THEN the system SHALL warn about missing context

### Requirement 4: hfo-execute Power (Act)

**User Story:** As a developer, I want an Execute power that handles all code writing and timing, so that I can implement with proper patterns.

#### Acceptance Criteria

1. WHEN hfo-execute is activated THEN the system SHALL provide Port 2 (Shaper) and Port 3 (Injector) tools: for-shaping, for-injecting, temporal
2. WHEN writing TypeScript THEN the system SHALL enforce typescript-patterns.md
3. WHEN writing Python THEN the system SHALL enforce python-patterns.md
4. WHEN writing Human.js code THEN the system SHALL enforce CanonicalHandState contracts
5. WHEN the keyword "write", "create", "edit", "code", "execute", or "shape" appears THEN the system SHALL suggest hfo-execute activation
6. IF hfo-perceive was not activated in this session THEN the system SHALL block write operations

### Requirement 5: hfo-yield Power (Validate/Verify/Learn)

**User Story:** As a developer, I want a Yield power that handles all validation, testing, storage, and planning, so that I can verify correctness and learn from results.

#### Acceptance Criteria

1. WHEN hfo-yield is activated THEN the system SHALL provide Ports 4-7 tools: for-disrupting, hypothesis, pydantic, opa, for-assimilating, memory, kg, mcts, pyribs
2. WHEN validating code THEN the system SHALL run property-based tests via hypothesis
3. WHEN validating data THEN the system SHALL use pydantic_validate
4. WHEN storing results THEN the system SHALL log to DuckDB and LanceDB
5. WHEN planning next steps THEN the system SHALL use mcts_search or pyribs_add
6. WHEN the keyword "test", "validate", "store", "learn", "yield", or "verify" appears THEN the system SHALL suggest hfo-yield activation
7. WHEN code changes are complete THEN the system SHALL require hfo-yield validation before commit

### Requirement 6: Enforcement via Immunizer

**User Story:** As a developer, I want the Immunizer (Port 5) to act as the gatekeeper between PREY phases, so that AI cannot skip validation steps.

#### Acceptance Criteria

1. WHEN transitioning from Execute to Yield THEN the system SHALL require pydantic_validate on all new data structures
2. WHEN committing changes THEN the system SHALL require at least one property test to pass
3. WHEN the Immunizer detects pattern violations THEN the system SHALL block the operation and explain the violation
4. WHEN a power is activated THEN the system SHALL log the activation to the Immunizer audit trail
5. IF enforcement is bypassed THEN the system SHALL log a warning to ObsidianBlackboard.jsonl

### Requirement 7: Power Keywords and Auto-Activation

**User Story:** As a developer, I want powers to auto-suggest based on keywords in my messages, so that the right tools are always available.

#### Acceptance Criteria

1. WHEN a message contains Perceive keywords THEN the system SHALL suggest "Activate hfo-perceive?"
2. WHEN a message contains React keywords THEN the system SHALL suggest "Activate hfo-react?"
3. WHEN a message contains Execute keywords THEN the system SHALL suggest "Activate hfo-execute?"
4. WHEN a message contains Yield keywords THEN the system SHALL suggest "Activate hfo-yield?"
5. WHEN multiple keyword categories match THEN the system SHALL suggest the earliest PREY phase not yet activated

### Requirement 8: Workspace Settings Cleanup

**User Story:** As a developer, I want MCP servers removed from workspace settings and moved to powers, so that power activation is required for tool access.

#### Acceptance Criteria

1. WHEN the cleanup is complete THEN the system SHALL have empty or minimal .kiro/settings/mcp.json
2. WHEN a tool is needed THEN the system SHALL require the appropriate PREY power to be activated
3. WHEN the old hfo power exists THEN the system SHALL archive it to HFO_buds/generation_76/kiro_archive/
4. WHEN redundant hooks exist THEN the system SHALL archive them to HFO_buds/generation_76/kiro_archive/

---

*HFO Gen 77 | PREY Powers Architecture | 2025-12-18*
