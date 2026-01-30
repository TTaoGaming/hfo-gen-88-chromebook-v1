# Requirements Document

## Introduction

This spec establishes the HFO Kiro Power as the Single Source of Truth (SSOT) for Generation 77. HFO (Hive Fleet Obsidian) is a polymorphic capability abstract factory engineering platform that uses an 8-port hexagonal architecture. The current vertical slice targets SOTA ghost cursor from mid-range smartphone selfie camera - total tool virtualization through gesture control.

The power consolidates MCP server configurations, knowledge base steering files, and coding patterns into a single SSOT power. This update ensures compliance with Kiro Power Builder standards and completes the Gen 76→77 transition.

## Glossary

- **HFO**: Hive Fleet Obsidian - polymorphic capability abstract factory engineering platform
- **Ghost Cursor**: SOTA gesture-controlled cursor from smartphone selfie camera
- **Total Tool Virtualization**: Using gestures to control any tool/interface without physical input devices
- **Power**: A Kiro Power package containing POWER.md, optional mcp.json, and optional steering files
- **SSOT**: Single Source of Truth - consolidated documentation avoiding fragmentation
- **Frontmatter**: YAML metadata at the top of POWER.md files
- **Steering**: Additional workflow guides loaded on-demand by agents
- **Generation**: HFO version number (currently 76, transitioning to 77)
- **Vertical Slice**: End-to-end implementation of one complete feature (ghost cursor)

## Requirements

### Requirement 1

**User Story:** As a Kiro agent, I want the HFO power to have valid frontmatter, so that the power activates correctly and appears in the Powers UI.

#### Acceptance Criteria

1. WHEN the POWER.md frontmatter is parsed THEN the system SHALL contain only valid fields: name, displayName, description, keywords, author
2. WHEN the frontmatter contains a `version` field THEN the system SHALL remove it and use timestamps in the document body instead
3. WHEN the power is activated THEN the system SHALL return the correct power metadata without errors

### Requirement 2

**User Story:** As a Kiro agent, I want the mcp.json to follow the correct schema, so that MCP servers connect properly.

#### Acceptance Criteria

1. WHEN the mcp.json is parsed THEN the system SHALL contain only valid fields: command, args, env, cwd, url, headers, disabled, autoApprove, disabledTools
2. WHEN the mcp.json contains `description` fields THEN the system SHALL remove them (descriptions belong in POWER.md)
3. WHEN MCP servers are configured THEN the system SHALL connect without schema validation errors

### Requirement 3

**User Story:** As a Kiro agent, I want all hooks and steering files to reference the correct power name, so that power activation works consistently.

#### Acceptance Criteria

1. WHEN the session-start hook fires THEN the system SHALL reference `powerName=hfo` (not `hfo-hexagonal`)
2. WHEN steering files reference the power THEN the system SHALL use the name `hfo` consistently
3. WHEN the AGENTS.md references the power THEN the system SHALL use the name `hfo` consistently

### Requirement 4

**User Story:** As a Warlock, I want all files versioned with timestamps and generation numbers, so that I can track changes across generations.

#### Acceptance Criteria

1. WHEN a file is updated THEN the system SHALL include an ISO-8601 timestamp in the document body
2. WHEN generation changes from 76 to 77 THEN the system SHALL update all generation references
3. WHEN the MANIFEST.md is updated THEN the system SHALL reflect the current generation and timestamp

### Requirement 5

**User Story:** As a Kiro agent, I want the power structure to pass the Power Builder validation checklist, so that the power is production-ready.

#### Acceptance Criteria

1. WHEN the power directory is validated THEN the system SHALL have POWER.md with valid frontmatter
2. WHEN the power has MCP servers THEN the system SHALL have mcp.json with mcpServers format
3. WHEN the power has steering files THEN the system SHALL list them in POWER.md
4. WHEN the power is installed locally THEN the system SHALL appear in Installed Powers list

### Requirement 6

**User Story:** As a Warlock, I want the POWER.md to accurately describe HFO as a polymorphic capability abstract factory, so that agents understand the full scope of the platform.

#### Acceptance Criteria

1. WHEN the POWER.md overview is read THEN the system SHALL describe HFO as Hive Fleet Obsidian
2. WHEN the description mentions architecture THEN the system SHALL reference polymorphic capability abstract factory
3. WHEN the vertical slice is described THEN the system SHALL mention ghost cursor and total tool virtualization
4. WHEN keywords are listed THEN the system SHALL include ghost-cursor, tool-virtualization, selfie-camera, gesture-control

### Requirement 7

**User Story:** As a Kiro agent, I want the steering files to reflect the current product focus (ghost cursor), so that I can assist with the vertical slice implementation.

#### Acceptance Criteria

1. WHEN port-0-observer steering is read THEN the system SHALL include Human.js selfie camera integration patterns
2. WHEN port-2-shaper steering is read THEN the system SHALL include ghost cursor coordinate transformation
3. WHEN cross-cutting steering is read THEN the system SHALL include total tool virtualization workflow
