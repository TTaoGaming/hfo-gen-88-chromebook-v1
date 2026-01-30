# Requirements Document

## Introduction

This specification defines the infrastructure-first approach to completing the HFO (Hive Fleet Obsidian) 8-port hexagonal architecture. The goal is to fill all 8 OBSIDIAN ports with their canonical tech stack tools before building products, ensuring the full cognitive symbiote infrastructure is operational.

The canonical tech stack is derived from Gen 63 Obsidian Matrix and the HFO Primitives document, mapping each port to specific vendor-neutral tools that enable the tri-temporal control loop (Past/Present/Future) and JADC2-aligned operations.

## Glossary

- **HFO**: Hive Fleet Obsidian - the polymorphic 8×8 matrix cognitive architecture
- **Port**: One of 8 hexagonal interface points in the HFO architecture (0-7)
- **MCP**: Model Context Protocol - standard for AI tool discovery and execution
- **NATS JetStream**: Persistent pub/sub messaging system for stigmergy
- **Temporal.io**: Durable workflow orchestration engine
- **OpenTelemetry**: Vendor-neutral observability standard (traces/metrics/logs)
- **OpenFeature**: Vendor-neutral feature flag standard for canary/rollback
- **Pydantic**: Python data validation library
- **OPA**: Open Policy Agent - policy enforcement engine
- **MCTS**: Monte Carlo Tree Search - planning algorithm
- **MAP-Elites**: Quality-Diversity algorithm for diverse solution archives
- **HNSW**: Hierarchical Navigable Small World - fast ANN index algorithm
- **Stigmergy**: Indirect coordination through environment modification

## Requirements

### Requirement 1: Port 0 - Observer (SENSE)

**User Story:** As a Swarmlord, I want comprehensive sensing capabilities, so that I can gather data from multiple sources (filesystem, web, APIs, telemetry).

#### Acceptance Criteria

1. WHEN the Observer port is activated THEN the system SHALL provide filesystem read operations via MCP server
2. WHEN web search is requested THEN the system SHALL execute Brave Search API queries and return results
3. WHEN GitHub data is needed THEN the system SHALL query GitHub API for repositories, code, and issues
4. WHEN URL content is required THEN the system SHALL fetch and parse web content (markdown, JSON, HTML)
5. WHEN telemetry data exists THEN the system SHALL read OpenTelemetry traces, metrics, and logs

### Requirement 2: Port 1 - Bridger (CONNECT)

**User Story:** As a Swarmlord, I want message bus and event routing capabilities, so that I can connect components via stigmergy patterns.

#### Acceptance Criteria

1. WHEN messages need routing THEN the system SHALL use NATS JetStream for persistent pub/sub
2. WHEN events are published THEN the system SHALL format them as CloudEvents for interoperability
3. WHEN sequential reasoning is needed THEN the system SHALL use the sequential-thinking MCP server
4. WHEN message replay is requested THEN the system SHALL retrieve historical messages from JetStream streams

### Requirement 3: Port 2 - Shaper (ACT)

**User Story:** As a Swarmlord, I want transformation and execution capabilities, so that I can modify files, run containers, and automate browser actions.

#### Acceptance Criteria

1. WHEN file modifications are needed THEN the system SHALL write, edit, and move files via MCP server
2. WHEN browser automation is required THEN the system SHALL execute Puppeteer actions (navigate, click, fill, screenshot)
3. WHEN container operations are needed THEN the system SHALL manage Docker containers via MCP
4. WHEN code generation is requested THEN the system SHALL produce artifacts following approved primitives

### Requirement 4: Port 3 - Injector (TIME/PULSE)

**User Story:** As a Swarmlord, I want temporal triggering capabilities, so that I can schedule workflows and manage time-based events.

#### Acceptance Criteria

1. WHEN current time is needed THEN the system SHALL return accurate timestamp via time MCP server
2. WHEN durable workflows are required THEN the system SHALL orchestrate via Temporal.io patterns
3. WHEN scheduled triggers are needed THEN the system SHALL support cron-style scheduling
4. WHEN async operations are required THEN the system SHALL manage asyncio-based event loops

### Requirement 5: Port 4 - Disruptor (CHAOS/TEST)

**User Story:** As a Swarmlord, I want chaos testing and fuzzing capabilities, so that I can stress-test systems and find edge cases.

#### Acceptance Criteria

1. WHEN property-based testing is needed THEN the system SHALL generate random inputs via Hypothesis library
2. WHEN chaos injection is required THEN the system SHALL introduce controlled failures (Chaos Monkey patterns)
3. WHEN fuzzing is requested THEN the system SHALL generate malformed inputs to test error handling
4. WHEN red-team scenarios are needed THEN the system SHALL attempt to falsify assumptions

### Requirement 6: Port 5 - Immunizer (VALIDATE/DEFEND)

**User Story:** As a Swarmlord, I want validation and policy enforcement capabilities, so that I can ensure data integrity and security.

#### Acceptance Criteria

1. WHEN data validation is needed THEN the system SHALL enforce schemas via Pydantic models
2. WHEN policy decisions are required THEN the system SHALL evaluate rules via OPA (Open Policy Agent)
3. WHEN feature flags are checked THEN the system SHALL use OpenFeature for vendor-neutral flag evaluation
4. WHEN security gates are needed THEN the system SHALL enforce IAM and access control policies

### Requirement 7: Port 6 - Assimilator (REMEMBER/STORE)

**User Story:** As a Swarmlord, I want comprehensive memory and storage capabilities, so that I can persist state, retrieve precedents, and maintain knowledge graphs.

#### Acceptance Criteria

1. WHEN SQL queries are needed THEN the system SHALL execute against DuckDB via MCP server
2. WHEN semantic search is required THEN the system SHALL query LanceDB vectors via hfo-memory MCP
3. WHEN knowledge graph operations are needed THEN the system SHALL manage entities and relations via memory MCP
4. WHEN historical data is requested THEN the system SHALL access Gen 1-72 backup via filesystem MCP
5. WHEN HNSW retrieval is needed THEN the system SHALL perform fast approximate nearest neighbor search

### Requirement 8: Port 7 - Navigator (GOAL/DECIDE)

**User Story:** As a Swarmlord, I want planning and decision-making capabilities, so that I can navigate solution spaces and allocate resources.

#### Acceptance Criteria

1. WHEN planning is needed THEN the system SHALL use MCTS (Monte Carlo Tree Search) for lookahead
2. WHEN diverse solutions are required THEN the system SHALL maintain MAP-Elites/QD archives via pyribs
3. WHEN receding horizon control is needed THEN the system SHALL implement MPC-style replanning
4. WHEN budget allocation is required THEN the system SHALL distribute resources across candidates

### Requirement 9: Cross-Port Integration

**User Story:** As a Swarmlord, I want all ports to work together seamlessly, so that I can execute the tri-temporal control loop (Past/Present/Future).

#### Acceptance Criteria

1. WHEN the Obsidian Hourglass flips THEN the system SHALL coordinate all 8 ports in the OODA loop
2. WHEN stigmergy coordination is needed THEN the system SHALL use the blackboard pattern via NATS JetStream
3. WHEN apex assimilation occurs THEN the system SHALL verify provenance, run tests, and archive to QD frontier
4. WHEN a port fails THEN the system SHALL gracefully degrade and report status to the Navigator

### Requirement 10: MCP Server Configuration

**User Story:** As a Warlock, I want all MCP servers properly configured, so that AI agents can discover and use tools without manual setup.

#### Acceptance Criteria

1. WHEN a new agent session starts THEN the system SHALL have all 8 ports available via MCP
2. WHEN API keys are required THEN the system SHALL load them from configuration (hardcoded or env)
3. WHEN a server fails to start THEN the system SHALL log the error and continue with available servers
4. WHEN sub-tools are needed THEN the system SHALL expose them under hierarchical naming (e.g., for-observing-brave)
