# Requirements Document: HFO Powers Expansion

## Introduction

The HFO Hexagonal Power is installed and working with 10 MCP servers. However, several ports have gaps:
- Port 1 (Bridger): Only 4 tools - needs reasoning/connection tools
- Port 2 (Shaper): Missing puppeteer, docker, git servers
- Port 3 (Injector): Time server shows 0 tools - needs fix
- Port 4 (Disruptor): Only 2 tools - needs testing/fuzzing tools
- Port 5 (Immunizer): Only 3 tools - needs validation/security tools
- Port 6 (Assimilator): DuckDB shows 0 tools - needs fix
- Port 7 (Navigator): Only 3 tools - needs planning/goal tools

This spec expands the power with additional MCP servers, fixes broken connections, and adds verification/enforcement hooks.

## Glossary

- **Port**: One of 8 hexagonal roles in HFO architecture (Observer, Bridger, Shaper, Injector, Disruptor, Immunizer, Assimilator, Navigator)
- **MCP Server**: Model Context Protocol server providing tools to AI agents
- **Tool Coverage**: Number of working tools per port (target: ~8 per port)
- **Verification Hook**: Hook that validates MCP server connectivity
- **Enforcement Hook**: Hook that ensures agents use appropriate port tools
- **Port Balance**: Even distribution of tools across all 8 ports

## Requirements

### Requirement 1: Fix Broken MCP Server Connections

**User Story:** As a developer, I want all configured MCP servers to actually connect, so that tools are accessible.

#### Acceptance Criteria

1. WHEN `for-injecting` server is checked THEN the system SHALL return time-related tools (not 0 tools)
2. WHEN `for-assimilating` server is checked THEN the system SHALL return DuckDB SQL tools (not 0 tools)
3. WHEN any MCP server shows 0 tools THEN the system SHALL diagnose and fix the connection
4. WHEN a server connection fails THEN the system SHALL log the error with diagnostic info
5. IF a server cannot be fixed THEN the system SHALL mark it as disabled with explanation

### Requirement 2: Expand Port 1 Bridger (REASON)

**User Story:** As a developer, I want more reasoning/connection tools, so that agents can better analyze and connect information.

#### Acceptance Criteria

1. WHEN reasoning is needed THEN the system SHALL provide sequential-thinking tool (existing)
2. WHEN data connection is needed THEN the system SHALL provide GraphQL query tools
3. WHEN complex analysis is needed THEN the system SHALL provide chain-of-thought tools
4. WHEN adding Bridger tools THEN the system SHALL use `for-bridging-*` naming convention
5. WHERE tools overlap with other ports THEN the system SHALL prefer the most specific port

### Requirement 3: Expand Port 2 Shaper (ACT)

**User Story:** As a developer, I want browser automation, container, and git tools, so that agents can perform complex actions.

#### Acceptance Criteria

1. WHEN browser automation is needed THEN the system SHALL provide puppeteer or playwright tools
2. WHEN container management is needed THEN the system SHALL provide docker tools
3. WHEN git operations are needed THEN the system SHALL provide git tools
4. WHEN shell commands are needed THEN the system SHALL provide shell execution tools
5. WHEN adding Shaper tools THEN the system SHALL use `for-shaping-*` naming convention

### Requirement 4: Expand Port 4 Disruptor (CHAOS)

**User Story:** As a developer, I want more testing and fuzzing tools, so that agents can thoroughly test code.

#### Acceptance Criteria

1. WHEN E2E testing is needed THEN the system SHALL provide playwright or puppeteer test tools
2. WHEN unit testing is needed THEN the system SHALL provide test runner tools
3. WHEN code coverage is needed THEN the system SHALL provide coverage analysis tools
4. WHEN fuzzing is needed THEN the system SHALL provide hypothesis_generate (existing)
5. WHEN adding Disruptor tools THEN the system SHALL use `for-disrupting-*` naming convention

### Requirement 5: Expand Port 5 Immunizer (VALIDATE)

**User Story:** As a developer, I want more validation and security tools, so that agents can ensure code quality.

#### Acceptance Criteria

1. WHEN linting is needed THEN the system SHALL provide eslint or ruff tools
2. WHEN security scanning is needed THEN the system SHALL provide semgrep or similar tools
3. WHEN schema validation is needed THEN the system SHALL provide JSON Schema tools
4. WHEN type checking is needed THEN the system SHALL provide type checker tools
5. WHEN adding Immunizer tools THEN the system SHALL use `for-immunizing-*` naming convention

### Requirement 6: Expand Port 6 Assimilator (REMEMBER)

**User Story:** As a developer, I want more storage and memory tools, so that agents can persist and retrieve information.

#### Acceptance Criteria

1. WHEN SQL queries are needed THEN the system SHALL provide DuckDB tools (fix existing)
2. WHEN caching is needed THEN the system SHALL provide Redis or similar tools
3. WHEN document storage is needed THEN the system SHALL provide SQLite tools
4. WHEN vector search is needed THEN the system SHALL provide semantic_search (existing)
5. WHEN adding Assimilator tools THEN the system SHALL use `for-assimilating-*` naming convention

### Requirement 7: Expand Port 7 Navigator (GOAL)

**User Story:** As a developer, I want more planning and goal-tracking tools, so that agents can manage complex tasks.

#### Acceptance Criteria

1. WHEN task planning is needed THEN the system SHALL provide MCTS search (existing)
2. WHEN issue tracking is needed THEN the system SHALL provide Linear or GitHub Issues tools
3. WHEN knowledge management is needed THEN the system SHALL provide Notion or similar tools
4. WHEN project management is needed THEN the system SHALL provide task management tools
5. WHEN adding Navigator tools THEN the system SHALL use `for-navigating-*` naming convention

### Requirement 8: Create Port Verification Hooks

**User Story:** As a developer, I want hooks that verify MCP server connectivity, so that I know when tools are broken.

#### Acceptance Criteria

1. WHEN a session starts THEN the system SHALL verify all 8 ports have connected servers
2. WHEN a port has 0 tools THEN the system SHALL alert the user with diagnostic info
3. WHEN verification runs THEN the system SHALL log results to blackboard
4. WHEN a server reconnects THEN the system SHALL update verification status
5. IF verification fails repeatedly THEN the system SHALL suggest fix actions

### Requirement 9: Create Port Enforcement Hooks

**User Story:** As a developer, I want hooks that enforce correct port usage, so that agents use the right tools for each task.

#### Acceptance Criteria

1. WHEN an agent reads files THEN the system SHALL suggest Port 0 Observer tools
2. WHEN an agent writes files THEN the system SHALL suggest Port 2 Shaper tools
3. WHEN an agent runs tests THEN the system SHALL suggest Port 4 Disruptor tools
4. WHEN an agent validates data THEN the system SHALL suggest Port 5 Immunizer tools
5. WHEN an agent stores data THEN the system SHALL suggest Port 6 Assimilator tools

### Requirement 10: Update Power Documentation

**User Story:** As a developer, I want POWER.md and steering files updated with new tools, so that agents know what's available.

#### Acceptance Criteria

1. WHEN new servers are added THEN the system SHALL update POWER.md tool list
2. WHEN new servers are added THEN the system SHALL update toolbox.md with examples
3. WHEN new servers are added THEN the system SHALL update port-reference.md steering file
4. WHEN tool count changes THEN the system SHALL update hfo-context.md infrastructure count
5. WHEN documentation is updated THEN the system SHALL include usage examples

---

## Port Tool Targets

| Port | Role | Current | Target | Gap |
|:----:|:-----|:-------:|:------:|:---:|
| 0 | Observer | 46 | 46 | ✅ |
| 1 | Bridger | 4 | 8 | +4 |
| 2 | Shaper | 14 | 20 | +6 |
| 3 | Injector | 2 | 6 | +4 |
| 4 | Disruptor | 2 | 8 | +6 |
| 5 | Immunizer | 3 | 8 | +5 |
| 6 | Assimilator | 5 | 10 | +5 |
| 7 | Navigator | 3 | 8 | +5 |

---

*Created: 2025-12-16 | Gen 76 | HFO Powers Expansion*
