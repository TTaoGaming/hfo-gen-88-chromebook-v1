# Design Document: HFO Powers Expansion

## Overview

This design expands the HFO Hexagonal Power from 10 MCP servers to ~20 servers, targeting ~8 tools per port. The expansion includes fixing broken connections, adding new official MCP servers, and creating verification/enforcement hooks.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    HFO Hexagonal Power                          │
├─────────────────────────────────────────────────────────────────┤
│  Port 0: Observer (SENSE)     │  Port 4: Disruptor (CHAOS)     │
│  - for-observing              │  - for-disrupting-playwright   │
│  - for-observing-brave        │  - for-disrupting-jest         │
│  - for-observing-github       │  - hfo-mcp-server (hypothesis) │
│  - for-observing-fetch        │                                │
├───────────────────────────────┼────────────────────────────────┤
│  Port 1: Bridger (REASON)     │  Port 5: Immunizer (VALIDATE)  │
│  - for-bridging               │  - for-immunizing-eslint       │
│  - for-bridging-graphql       │  - for-immunizing-semgrep      │
│  - hfo-mcp-server (nats)      │  - hfo-mcp-server (pydantic)   │
├───────────────────────────────┼────────────────────────────────┤
│  Port 2: Shaper (ACT)         │  Port 6: Assimilator (REMEMBER)│
│  - for-shaping                │  - for-assimilating (duckdb)   │
│  - for-shaping-puppeteer      │  - for-assimilating-memory     │
│  - for-shaping-docker         │  - for-assimilating-sqlite     │
│  - for-shaping-git            │  - for-assimilating-redis      │
├───────────────────────────────┼────────────────────────────────┤
│  Port 3: Injector (TIME)      │  Port 7: Navigator (GOAL)      │
│  - for-injecting (time)       │  - for-navigating-linear       │
│  - hfo-mcp-server (temporal)  │  - for-navigating-notion       │
│  - hfo-mcp-server (cron)      │  - hfo-mcp-server (mcts/pyribs)│
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### MCP Server Naming Convention

All servers follow the pattern: `for-{port_name}[-{sub_tool}]`

| Port | Prefix | Examples |
|:----:|:-------|:---------|
| 0 | `for-observing-*` | for-observing-brave, for-observing-github |
| 1 | `for-bridging-*` | for-bridging, for-bridging-graphql |
| 2 | `for-shaping-*` | for-shaping-puppeteer, for-shaping-docker |
| 3 | `for-injecting-*` | for-injecting, for-injecting-cron |
| 4 | `for-disrupting-*` | for-disrupting-playwright, for-disrupting-jest |
| 5 | `for-immunizing-*` | for-immunizing-eslint, for-immunizing-semgrep |
| 6 | `for-assimilating-*` | for-assimilating-sqlite, for-assimilating-redis |
| 7 | `for-navigating-*` | for-navigating-linear, for-navigating-notion |

Exception: `hfo-mcp-server` contains custom tools spanning multiple ports.

### Hook Architecture

```
.kiro/hooks/
├── session-start.hook.md       # Existing - remind about tools
├── search-before-create.hook.md # Existing - anti-hallucination
├── blackboard-handoff.hook.md  # Existing - session end
├── port-verification.hook.md   # NEW - verify MCP connectivity
├── port-enforcement.hook.md    # NEW - suggest correct port
└── tool-usage-audit.hook.md    # NEW - log tool usage patterns
```

## Data Models

### MCP Server Configuration (mcp.json)

```json
{
  "mcpServers": {
    "for-{port}-{tool}": {
      "command": "npx" | "uvx" | "python",
      "args": ["@package/server", ...],
      "env": { "KEY": "value" },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Hook Configuration (*.hook.md)

```yaml
---
version: 1
trigger:
  type: session_created | file_saved | manual
  filePattern: "**/*.py"  # optional
action:
  type: send_message
  message: |
    Hook content here
---
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: All configured servers have tools
*For any* MCP server in mcp.json that is not disabled, activating the power SHALL return at least 1 tool for that server.
**Validates: Requirements 1.1, 1.2, 6.1**

### Property 2: Server naming follows port convention
*For any* MCP server name in mcp.json (except hfo-mcp-server), the name SHALL start with `for-{port_name}` where port_name matches the server's assigned port.
**Validates: Requirements 2.4, 3.5, 4.5, 5.5, 6.5, 7.5**

### Property 3: Each port has minimum tool coverage
*For any* of the 8 ports, the total tool count across all servers assigned to that port SHALL be at least 3.
**Validates: Requirements 2.1-2.3, 3.1-3.4, 4.1-4.4, 5.1-5.4, 6.1-6.4, 7.1-7.4**

### Property 4: Verification hook checks all ports
*For any* port verification hook execution, the hook content SHALL reference all 8 port names (Observer, Bridger, Shaper, Injector, Disruptor, Immunizer, Assimilator, Navigator).
**Validates: Requirements 8.1, 8.3**

### Property 5: Enforcement hook maps actions to ports
*For any* port enforcement hook, the hook content SHALL map file operations to correct ports (read→Port 0, write→Port 2, test→Port 4, validate→Port 5, store→Port 6).
**Validates: Requirements 9.1-9.5**

### Property 6: Documentation lists all servers
*For any* server in mcp.json, POWER.md SHALL contain a reference to that server name.
**Validates: Requirements 10.1, 10.3**

### Property 7: Steering files have usage examples
*For any* port documented in toolbox.md, there SHALL be at least one code example showing tool usage.
**Validates: Requirements 10.2, 10.5**

### Property 8: Disabled servers have explanation
*For any* MCP server with `disabled: true`, the mcp.json SHALL have a comment or the POWER.md SHALL explain why it's disabled.
**Validates: Requirements 1.5**

## Error Handling

| Error | Detection | Recovery |
|:------|:----------|:---------|
| Server returns 0 tools | Verification hook | Check command/args, restart server |
| Server connection timeout | MCP protocol | Retry with backoff, mark disabled |
| Invalid server name | Property test | Rename to follow convention |
| Missing documentation | Property test | Generate from mcp.json |

## Testing Strategy

### Property-Based Testing

Use `hypothesis` library for Python property tests:
- Minimum 100 iterations per property
- Test against actual mcp.json and hook files
- Tag format: `**Feature: hfo-powers-expansion, Property {N}: {name}**`

### Unit Tests

- Test MCP server configuration parsing
- Test hook file format validation
- Test naming convention regex

### Integration Tests

- Test power activation returns expected servers
- Test hook triggers fire correctly
- Test documentation sync with mcp.json

---

*Created: 2025-12-16 | Gen 76 | HFO Powers Expansion Design*
