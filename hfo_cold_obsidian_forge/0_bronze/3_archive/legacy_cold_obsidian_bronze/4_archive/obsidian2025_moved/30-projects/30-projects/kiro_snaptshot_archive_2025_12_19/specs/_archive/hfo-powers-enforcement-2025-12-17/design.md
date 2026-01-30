# Design Document: HFO Powers Enforcement

## Overview

This design addresses the gap between documented HFO tooling (57 MCP tools) and actual enforcement. The infrastructure is built but agents don't use it because:
1. The HFO Power uses wrong file format (`power.json` instead of `mcp.json`)
2. No enforcement hooks exist
3. The power isn't installed in Kiro

The solution involves fixing the power structure, creating enforcement hooks, and updating steering files.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     KIRO POWERS SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│  .kiro/powers/hfo-hexagonal/                                    │
│  ├── POWER.md (frontmatter + docs)                              │
│  ├── mcp.json (MCP server config)                               │
│  └── steering/ (workflow guides)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ENFORCEMENT HOOKS                           │
├─────────────────────────────────────────────────────────────────┤
│  .kiro/hooks/                                                   │
│  ├── session-start.hook.md (remind about HFO tools)             │
│  ├── search-before-create.hook.md (enforce search first)        │
│  └── blackboard-handoff.hook.md (session end handoff)           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     STEERING FILES                              │
├─────────────────────────────────────────────────────────────────┤
│  .kiro/steering/                                                │
│  ├── toolbox.md (power activation syntax)                       │
│  ├── canalization.md (hook references)                          │
│  └── hfo-context.md (power status)                              │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Component 1: HFO Power Package

**Location:** `.kiro/powers/hfo-hexagonal/`

**Files:**
- `POWER.md` - Documentation with YAML frontmatter
- `mcp.json` - MCP server configuration (renamed from power.json)
- `steering/getting-started.md` - Quick start guide
- `steering/port-reference.md` - Detailed port documentation

**POWER.md Frontmatter Schema:**
```yaml
---
name: "hfo-hexagonal"
displayName: "HFO Hexagonal Architecture"
description: "8-port hexagonal architecture for AI-assisted development with 57 MCP tools"
keywords: ["hfo", "hexagonal", "ports", "observer", "bridger", "shaper", "injector", "disruptor", "immunizer", "assimilator", "navigator", "nats", "temporal", "hypothesis", "pydantic", "mcts", "pyribs", "gesture", "memory", "search"]
author: "HFO Gen 76"
---
```

**mcp.json Schema:**
```json
{
  "mcpServers": {
    "server-name": {
      "command": "string",
      "args": ["array"],
      "env": {"KEY": "value"},
      "disabled": false,
      "autoApprove": ["tool_name"]
    }
  }
}
```

### Component 2: Enforcement Hooks

**Location:** `.kiro/hooks/`

**Hook Format:**
```markdown
---
trigger: <event-type>
description: <what the hook does>
---

# Hook Title

<prompt content for agent>
```

**Hooks to Create:**

1. **session-start.hook.md**
   - Trigger: `session_created`
   - Purpose: Remind agent about HFO tools on session start

2. **search-before-create.hook.md**
   - Trigger: `manual` (button click)
   - Purpose: Enforce "search before create" pattern

3. **blackboard-handoff.hook.md** (already exists)
   - Trigger: `agent_execution_complete`
   - Purpose: Prompt for blackboard handoff

### Component 3: Steering File Updates

**Files to Update:**

1. **toolbox.md** - Add power activation syntax
2. **canalization.md** - Reference enforcement hooks
3. **hfo-context.md** - Add power installation status

## Data Models

### Power Metadata (POWER.md frontmatter)

```typescript
interface PowerMetadata {
  name: string;           // kebab-case identifier
  displayName: string;    // Human-readable title
  description: string;    // Max 3 sentences
  keywords: string[];     // Search keywords
  author?: string;        // Creator name
}
```

### MCP Server Configuration (mcp.json)

```typescript
interface McpConfig {
  mcpServers: {
    [serverName: string]: {
      command: string;
      args: string[];
      env?: Record<string, string>;
      disabled?: boolean;
      autoApprove?: string[];
    };
  };
}
```

### Hook Configuration

```typescript
interface HookConfig {
  trigger: 'session_created' | 'agent_execution_complete' | 'file_saved' | 'manual';
  description: string;
  filePattern?: string;  // For file_saved trigger
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Power file structure validity
*For any* valid HFO power directory, the directory SHALL contain `mcp.json` (not `power.json`) and `POWER.md` with valid frontmatter containing name, displayName, and description fields.
**Validates: Requirements 1.1, 1.2**

### Property 2: MCP server configuration validity
*For any* mcp.json file, all server entries SHALL have required fields (command, args) and valid structure matching the McpConfig interface.
**Validates: Requirements 1.1, 1.5**

### Property 3: Hook file format validity
*For any* hook file in `.kiro/hooks/`, the file SHALL have YAML frontmatter with trigger and description fields.
**Validates: Requirements 2.4**

### Property 4: No MCP server name conflicts
*For any* two installed powers, their mcp.json files SHALL NOT have overlapping server names.
**Validates: Requirements 4.4**

### Property 5: Steering file power references
*For any* steering file that references MCP tools, the file SHALL use power activation syntax (`kiroPowers action=activate`) rather than direct tool calls.
**Validates: Requirements 5.4**

## Error Handling

| Error | Cause | Resolution |
|:------|:------|:-----------|
| Power not found | Directory missing or wrong name | Verify `.kiro/powers/hfo-hexagonal/` exists |
| Invalid frontmatter | Missing required fields | Add name, displayName, description to POWER.md |
| MCP server conflict | Duplicate server names | Rename conflicting servers |
| Hook not triggering | Wrong trigger type | Verify trigger matches Kiro hook events |
| Power not activating | Keywords don't match | Add relevant keywords to frontmatter |

## Testing Strategy

### Unit Tests (Examples)
- Verify mcp.json exists and has valid structure
- Verify POWER.md has valid frontmatter
- Verify hook files have correct format
- Verify steering files contain expected content

### Property-Based Tests
- **Property 1**: Generate random power directories, verify structure
- **Property 4**: Generate random MCP configs, verify no name conflicts
- **Property 5**: Parse steering files, verify power activation syntax

### Integration Tests
- Install power via Kiro UI, verify it appears in list
- Activate power, verify tool schemas returned
- Trigger hooks, verify agent receives prompts

### Testing Framework
- **Python**: pytest with hypothesis for property-based testing
- **Manual**: Kiro UI verification for installation/activation

---

*Created: 2025-12-16 | Gen 76 | HFO Powers Enforcement Design*
