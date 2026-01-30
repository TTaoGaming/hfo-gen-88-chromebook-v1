# Requirements Document: HFO Powers Enforcement

## Introduction

The HFO infrastructure (57 MCP tools, 14 custom HFO tools, 4 Docker containers) is built and tested but NOT enforced. AI agents don't automatically use the tools because:
1. The HFO Power at `.kiro/powers/hfo-hexagonal/` uses wrong format (`power.json` instead of `mcp.json`)
2. No enforcement hooks exist to remind agents to use MCP tools
3. The power is not installed in Kiro

This spec focuses on making the documented tooling actually work and be enforced through Kiro Powers and Hooks.

## Glossary

- **Kiro Power**: A package of documentation, MCP configuration, and steering files that provides capabilities to AI agents
- **MCP Server**: Model Context Protocol server that provides tools to AI agents
- **Enforcement Hook**: A Kiro hook that triggers on events to remind/enforce agent behavior
- **Canalization**: Making the "right path" the "easy path" - channeling AI toward productive outcomes
- **Steering File**: Markdown file in `.kiro/steering/` that provides context to agents
- **POWER.md**: Required documentation file for a Kiro Power with frontmatter metadata
- **mcp.json**: MCP server configuration file for a Kiro Power (NOT power.json)

## Requirements

### Requirement 1: Fix HFO Power Structure

**User Story:** As a developer, I want the HFO Hexagonal Power to install correctly, so that AI agents can discover and use the 57 MCP tools.

#### Acceptance Criteria

1. WHEN the power directory is examined THEN the system SHALL have `mcp.json` (not `power.json`)
2. WHEN POWER.md is examined THEN the system SHALL have valid frontmatter with name, displayName, description
3. WHEN the power is installed via Kiro UI THEN the system SHALL appear in "Installed Powers" list
4. WHEN an agent activates the power THEN the system SHALL return tool documentation and schemas
5. IF power.json exists THEN the system SHALL rename it to mcp.json and move metadata to POWER.md frontmatter

### Requirement 2: Create Enforcement Hooks

**User Story:** As a developer, I want hooks that enforce MCP tool usage, so that AI agents are reminded to use the documented tooling.

#### Acceptance Criteria

1. WHEN a new agent session starts THEN the system SHALL remind the agent about available HFO tools
2. WHEN an agent attempts to create a new file THEN the system SHALL remind to "search before create"
3. WHEN an agent session ends THEN the system SHALL prompt for blackboard handoff
4. WHEN hooks are created THEN the system SHALL follow Kiro hook format (`.kiro/hooks/*.hook.md`)
5. IF an agent ignores the hook THEN the system SHALL log the bypass for review

### Requirement 3: Verify Power Installation

**User Story:** As a developer, I want to verify the power is correctly installed, so that I know the tooling is accessible.

#### Acceptance Criteria

1. WHEN `kiroPowers action=list` is called THEN the system SHALL show "hfo-hexagonal" in installed powers
2. WHEN `kiroPowers action=activate powerName=hfo-hexagonal` is called THEN the system SHALL return tool schemas
3. WHEN an agent mentions "hfo", "hexagonal", or "ports" THEN the system SHALL consider activating the power
4. WHEN MCP servers are checked THEN the system SHALL show all 8 ports as connected (or disabled for placeholders)
5. IF installation fails THEN the system SHALL provide clear error message with fix instructions

### Requirement 4: Hunt for Additional Powers

**User Story:** As a developer, I want to discover and install additional powers that complement HFO, so that I can expand the tooling ecosystem.

#### Acceptance Criteria

1. WHEN searching for powers THEN the system SHALL check Kiro Powers marketplace/registry
2. WHEN evaluating powers THEN the system SHALL check: relevance to HFO, tool overlap, maintenance status
3. WHEN a useful power is found THEN the system SHALL document it in the Grimoire
4. WHEN installing external powers THEN the system SHALL verify they don't conflict with HFO MCP servers
5. WHERE a power provides overlapping tools THEN the system SHALL prefer HFO's implementation

### Requirement 5: Document Power Usage in Steering

**User Story:** As a developer, I want steering files updated to reference the installed power, so that agents know how to use it.

#### Acceptance Criteria

1. WHEN the power is installed THEN the system SHALL update `toolbox.md` with power activation instructions
2. WHEN the power is installed THEN the system SHALL update `canalization.md` with enforcement hooks
3. WHEN the power is installed THEN the system SHALL update `hfo-context.md` with power status
4. WHEN steering files reference MCP tools THEN the system SHALL use power activation syntax
5. IF steering files are outdated THEN the system SHALL flag them for update

---

## Success Metrics

- **Power Installation**: HFO Hexagonal Power appears in `kiroPowers action=list`
- **Tool Discovery**: `kiroPowers action=activate` returns all 57 tool schemas
- **Hook Enforcement**: Agents receive reminders on session start and file creation
- **Steering Alignment**: All steering files reference the installed power

---

*Created: 2025-12-16 | Gen 76 | MCP/Powers Enforcement*
