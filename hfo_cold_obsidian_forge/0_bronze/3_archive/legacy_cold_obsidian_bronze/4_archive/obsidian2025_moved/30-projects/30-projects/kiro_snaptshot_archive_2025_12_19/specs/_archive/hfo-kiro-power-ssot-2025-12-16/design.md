# Design Document

## Overview

This design establishes the HFO Kiro Power as the SSOT for Generation 77, addressing 4 structural issues:

1. **POWER.md frontmatter** - Remove invalid `version` field
2. **mcp.json schema** - Remove invalid `description` fields
3. **Power name consistency** - Update all references from `hfo-hexagonal` to `hfo`
4. **Generation transition** - Update all Gen 76 references to Gen 77

## Correctness Properties

### Property 1: Valid Frontmatter
```
∀ field ∈ POWER.md.frontmatter:
  field ∈ {name, displayName, description, keywords, author}
```

### Property 2: Valid mcp.json Schema
```
∀ server ∈ mcp.json.mcpServers:
  server.keys ⊆ {command, args, env, cwd, url, headers, disabled, autoApprove, disabledTools}
```

### Property 3: Power Name Consistency
```
∀ file ∈ {hooks, steering, AGENTS.md}:
  powerName references = "hfo"
```

### Property 4: Generation Consistency
```
∀ file ∈ {POWER.md, AGENTS.md, steering}:
  generation references = 77
```

## Files to Modify

| File | Change |
|:-----|:-------|
| `.kiro/powers/hfo/POWER.md` | Remove `version` from frontmatter, update Gen 76→77, update description to "Hive Fleet Obsidian" |
| `.kiro/powers/hfo/mcp.json` | Remove all `description` fields from mcpServers |
| `.kiro/hooks/session-start.hook.md` | Change `powerName=hfo-hexagonal` to `powerName=hfo`, update Gen 76→77 |
| `.kiro/steering/hfo-context.md` | Update power name references, update Gen 76→77 |
| `.kiro/steering/toolbox.md` | Update power name references |
| `AGENTS.md` (root) | Update Gen 76→77 |
| `HFO_buds/generation_76/AGENTS.md` | Update Gen 76→77 |
| `.kiro/powers/MANIFEST.md` | Update Gen 76→77 |

## POWER.md Updated Frontmatter

```yaml
---
name: "hfo"
displayName: "Hive Fleet Obsidian"
description: "Polymorphic capability abstract factory engineering platform with 8-port hexagonal architecture, 57 MCP tools, and ghost cursor vertical slice for total tool virtualization"
keywords:
  - hfo
  - hive-fleet-obsidian
  - hexagonal
  - ghost-cursor
  - tool-virtualization
  - selfie-camera
  - gesture-control
  - ports
  - observer
  - bridger
  - shaper
  - injector
  - disruptor
  - immunizer
  - assimilator
  - navigator
  - nats
  - temporal
  - hypothesis
  - pydantic
  - mcts
  - pyribs
  - gesture
  - hand
  - tracking
  - human
  - humanjs
  - mediapipe
  - cloudevents
  - 1euro
  - kalman
  - xstate
  - godot
  - gherkin
  - tdd
  - bdd
  - jsonl
  - duckdb
  - lancedb
  - wardley
  - apex
  - strangler
  - typescript
  - python
author: "HFO Gen 77"
---
```

## mcp.json Cleaned Schema

Remove all `description` fields. Example before/after:

**Before:**
```json
{
  "for-observing": {
    "command": "npx",
    "args": [...],
    "description": "Port 0: Observer - Read workspace files"
  }
}
```

**After:**
```json
{
  "for-observing": {
    "command": "npx",
    "args": [...]
  }
}
```

## Timestamp Convention

All updated files will include ISO-8601 timestamp in document body:
- Format: `2025-12-17T12:00:00Z`
- Location: Footer or version line in document

---

*Design v1.0 | 2025-12-17T12:00:00Z | HFO Kiro Power SSOT | Gen 77*
