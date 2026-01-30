# Design Document: HFO PREY Powers Architecture

## Overview

The HFO PREY Powers system restructures the monolithic `hfo` power into 4 focused powers aligned with the PREY workflow (Perceive-React-Execute-Yield) and JADC2 Mosaic Warfare's Sense-Make Sense-Act loop.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    JADC2 MOSAIC WARFARE LOOP                        │
├─────────────────────────────────────────────────────────────────────┤
│  SENSE ──────► MAKE SENSE ──────► ACT ──────► ASSESS               │
│    │              │                │             │                  │
│    ▼              ▼                ▼             ▼                  │
│ PERCEIVE ─────► REACT ─────────► EXECUTE ────► YIELD               │
│ (Port 0)      (Port 1)         (Ports 2,3)   (Ports 4-7)           │
│    │              │                │             │                  │
│    ▼              ▼                ▼             ▼                  │
│ hfo-perceive  hfo-react        hfo-execute   hfo-yield             │
└─────────────────────────────────────────────────────────────────────┘
```

## Architecture

### Power-to-Port Mapping

| Power | PREY Phase | JADC2 Phase | Ports | Gherkin | Tools |
|:------|:-----------|:------------|:------|:--------|:------|
| hfo-perceive | Perceive | Sense | 0 | GIVEN | for-observing, brave, github, fetch |
| hfo-react | React | Make Sense | 1 | AND | for-bridging, nats_* |
| hfo-execute | Execute | Act | 2, 3 | AND, WHEN | for-shaping, for-injecting, temporal_* |
| hfo-yield | Yield | Assess | 4, 5, 6, 7 | THEN, BUT, AS, TO | for-disrupting, hypothesis_*, pydantic_*, opa_*, for-assimilating, memory, kg, mcts_*, pyribs_* |

### Directory Structure

```
.kiro/powers/
├── hfo-perceive/
│   ├── POWER.md           # ~30 lines, Port 0 focus
│   ├── mcp.json           # for-observing, brave, github, fetch
│   └── steering/
│       └── perceive.md    # Anti-hallucination, search-first
│
├── hfo-react/
│   ├── POWER.md           # ~30 lines, Port 1 focus
│   ├── mcp.json           # for-bridging, nats tools
│   └── steering/
│       └── react.md       # Sequential thinking, stigmergy
│
├── hfo-execute/
│   ├── POWER.md           # ~40 lines, Ports 2+3 focus
│   ├── mcp.json           # for-shaping, for-injecting, temporal
│   └── steering/
│       ├── execute.md     # Pattern enforcement
│       ├── typescript.md  # TS patterns
│       └── python.md      # Python patterns
│
└── hfo-yield/
    ├── POWER.md           # ~50 lines, Ports 4-7 focus
    ├── mcp.json           # disrupting, immunizing, assimilating, navigating
    └── steering/
        ├── yield.md       # Validation workflow
        ├── testing.md     # Property-based testing
        └── storage.md     # DuckDB, LanceDB, KG
```

## Components and Interfaces

### Power Activation Flow

```
User Message
    │
    ▼
┌─────────────────────────────────────┐
│ Keyword Detection                    │
│ - perceive/search/read → hfo-perceive│
│ - react/plan/reason → hfo-react      │
│ - execute/write/code → hfo-execute   │
│ - yield/test/validate → hfo-yield    │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Prerequisite Check (Immunizer)       │
│ - hfo-execute requires hfo-perceive  │
│ - hfo-yield requires hfo-execute     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Power Activation                     │
│ kiroPowers(activate, powerName)      │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Tool Execution                       │
│ kiroPowers(use, powerName, ...)      │
└─────────────────────────────────────┘
```

### Enforcement Rules (Immunizer)

| Transition | Enforcement Rule |
|:-----------|:-----------------|
| Start → Perceive | Always allowed |
| Perceive → React | Allowed if search was performed |
| React → Execute | Allowed if plan exists |
| Execute → Yield | Allowed if code was written |
| Yield → Commit | Allowed if tests pass |

## Data Models

### Power Manifest (POWER.md frontmatter)

```yaml
---
name: "hfo-perceive"
displayName: "HFO Perceive"
description: "PREY Phase 1: Sense the environment (Port 0 Observer)"
keywords:
  - perceive
  - search
  - read
  - fetch
  - observe
  - sense
  - given
prey_phase: "perceive"
jadc2_phase: "sense"
ports: [0]
gherkin: "GIVEN"
requires: []  # No prerequisites
author: "HFO Gen 77"
---
```

### MCP Server Config (mcp.json)

```json
{
  "mcpServers": {
    "for-observing": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@2025.11.25", "."]
    }
  }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Power Isolation
*For any* power activation, the activated power SHALL only provide tools from its designated ports, not tools from other PREY phases.
**Validates: Requirements 2.1, 3.1, 4.1, 5.1**

### Property 2: Prerequisite Enforcement
*For any* hfo-execute activation, if hfo-perceive was not activated in the current session, the system SHALL warn about missing context.
**Validates: Requirements 4.6, 6.1**

### Property 3: Keyword Activation Consistency
*For any* message containing a PREY keyword, the system SHALL suggest the corresponding power activation.
**Validates: Requirements 7.1, 7.2, 7.3, 7.4**

### Property 4: Validation Gate
*For any* code commit attempt, if hfo-yield validation was not performed, the system SHALL block the commit.
**Validates: Requirements 5.7, 6.2**

### Property 5: Audit Trail Completeness
*For any* power activation or enforcement action, the system SHALL log the event to the Immunizer audit trail.
**Validates: Requirements 6.4, 6.5**

## Error Handling

| Error | Handling |
|:------|:---------|
| Power not found | Suggest installing from `.kiro/powers/` |
| Prerequisite not met | Show which power needs activation first |
| Tool not in power | Suggest correct power for the tool |
| Validation failed | Show specific failure and remediation |
| Enforcement bypassed | Log warning, allow with audit trail |

## Testing Strategy

### Unit Tests
- Power manifest parsing
- Keyword detection accuracy
- Prerequisite checking logic

### Property-Based Tests (Hypothesis)
- Property 1: Generate random tool requests, verify isolation
- Property 2: Generate activation sequences, verify prerequisites
- Property 3: Generate messages with keywords, verify suggestions
- Property 4: Generate commit attempts, verify validation gate
- Property 5: Generate actions, verify audit completeness

### Integration Tests
- Full PREY workflow: Perceive → React → Execute → Yield
- Cross-power tool access (should fail)
- Enforcement bypass logging

---

*HFO Gen 77 | PREY Powers Design | 2025-12-18*
