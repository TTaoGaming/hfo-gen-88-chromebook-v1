# Design Document: HFO Knowledge Powers Manifest

## Overview

This design implements **8 Versioned Port Powers** with Z-time timestamps for TTL tracking and auto-update capability. Each Obsidian port gets ONE Knowledge Base Power that is continuously updated as patterns emerge.

**Key Design Decisions**:
1. **Navigator First**: Port 7 Navigator is highest priority (DSE, AoA, MCTS, MPC, pyribs, JADC2, Mosaic)
2. **Z-Time Versioning**: All powers use ISO 8601 timestamps for TTL tracking
3. **Continuous Update**: Powers evolve daily/weekly as Ghost Cursor development reveals gaps
4. **HFO DNA**: Mosaic Warfare, Capacity Engineering, Apex Assimilation are core concepts

## Versioning Schema

```yaml
# POWER.md frontmatter with versioning
---
name: hfo-port-7-navigator
displayName: HFO Navigator (Port 7) ☰
description: DSE, AoA, MCTS, MPC, pyribs, Pareto, JADC2, Mosaic Warfare
keywords: navigator, dse, aoa, mcts, mpc, pyribs, pareto, qd, jadc2, mosaic, capacity
author: HFO Gen 76
version: 2025-12-17T00:00:00Z
ttl: P7D
lastUpdated: 2025-12-17T00:00:00Z
---
```

**TTL Values**:
- `P1D` - Daily update (active development)
- `P7D` - Weekly update (stable patterns)
- `P30D` - Monthly update (mature documentation)

## Architecture

```
.kiro/powers/
├── hfo-hexagonal/           # EXISTING - enhance with port steering
│   ├── POWER.md
│   └── steering/
│       ├── getting-started.md
│       ├── port-reference.md
│       ├── port-0-observer.md      # NEW
│       ├── port-1-bridger.md       # NEW
│       ├── port-2-shaper.md        # NEW
│       ├── port-3-injector.md      # NEW
│       ├── port-4-disruptor.md     # NEW
│       ├── port-5-immunizer.md     # NEW
│       ├── port-6-assimilator.md   # NEW
│       └── port-7-navigator.md     # NEW
├── human-js/                # CONVERT to Knowledge Base
│   ├── POWER.md             # KEEP (update keywords)
│   └── steering/            # KEEP
│       ├── gesture-recognition.md
│       └── hand-tracking.md
│   # DELETE: mcp.json, src/, package.json, tsconfig.json
├── typescript-patterns/     # NEW Knowledge Base Power
│   ├── POWER.md
│   └── steering/
│       └── coding-standards.md
└── python-patterns/         # NEW Knowledge Base Power
    ├── POWER.md
    └── steering/
        └── coding-standards.md
```

## Data Models

### POWER.md Frontmatter Schema

```yaml
---
name: power-name           # kebab-case identifier
displayName: Power Name    # Human-readable name
description: Brief desc    # One-line description
keywords: kw1, kw2, kw3    # Comma-separated activation keywords
author: HFO Gen 76         # Author attribution
---
```

### Port Steering File Structure

Each port steering file follows this template:

```markdown
---
inclusion: fileMatch
fileMatchPattern: "**/*.{ts,py,gd}"
---

# Port N: Role Name (Trigram) - Purpose

## Quick Reference
- Key tools/patterns
- Common commands

## Exemplars (DO NOT REINVENT)
- Package: version - what it provides

## Patterns
### Pattern Name
- When to use
- Code example

## Anti-Patterns
- What NOT to do

## Integration Points
- How this port connects to others
```

## Component Design

### Component 0: Port 7 Navigator Power (HIGHEST PRIORITY)

**Purpose**: Core HFO methodology - DSE, AoA, optimization, Mosaic Warfare.

**POWER.md** (`hfo-port-7-navigator`):
```markdown
---
name: hfo-port-7-navigator
displayName: HFO Navigator (Port 7) ☰
description: DSE, AoA, MCTS, MPC, pyribs, Pareto, JADC2, Mosaic Warfare
keywords: navigator, dse, aoa, mcts, mpc, pyribs, pareto, qd, jadc2, mosaic, capacity, wardley, mbse
author: HFO Gen 76
version: 2025-12-17T00:00:00Z
ttl: P7D
---

# Port 7: Navigator ☰ (GOAL)

## Core Concepts

### JADC2 (Joint All-Domain Command and Control)
- Military doctrine for distributed decision-making
- Kill chain: Sense → Make Sense → Decide → Act
- HFO maps to: Observer → Bridger → Navigator → Injector

### Mosaic Warfare
- Composable, swappable force packages
- Any component can be replaced without breaking system
- HFO: Every port is a swappable adapter

### Capacity Engineering (Wardley)
- Solve classes of problems, not instances
- Adopt commoditized exemplars (70% solution)
- Minimal glue code (<200 lines)

### DSE (Design Space Exploration)
- Systematic evaluation of alternatives
- Pareto frontier optimization
- pyribs MAP-Elites for Quality-Diversity

### AoA (Analysis of Alternatives)
- NASA/DoD trade study methodology
- Criteria: TRL, Risk, Cost, Schedule, Performance
- Decision matrix with weighted scoring

### MCTS (Monte Carlo Tree Search)
- UCB1 exploration/exploitation balance
- Parameter space search
- Preset optimization

### MPC (Model Predictive Control)
- Receding horizon planning
- Replan as new information arrives
- Kalman prediction for negative latency

### pyribs MAP-Elites
- Quality-Diversity optimization
- Archive of elite solutions
- Behavior descriptors for diversity
```

**Steering Files**:
- `steering/dse-aoa-patterns.md` - Trade analysis templates
- `steering/pyribs-patterns.md` - MAP-Elites usage
- `steering/mosaic-warfare.md` - JADC2 and composability

### Component 1: Port 4 Disruptor Power (TDD/BDD/Gherkin)

**Purpose**: Testing methodology - TDD, BDD, Gherkin, PBT, chaos.

**Key Topics**:
- TDD: Red-Green-Refactor cycle
- BDD: Behavior-Driven Development
- Gherkin: Given/When/Then syntax
- PBT: Hypothesis (Python), fast-check (TypeScript)
- Chaos: Failure injection patterns

### Component 2: Port 6 Assimilator Power (Mermaid + Storage)

**Purpose**: Documentation and storage patterns.

**Key Topics**:
- Mermaid: flowchart, sequenceDiagram, stateDiagram-v2, mindmap
- JSONL: Append-only event logs
- DuckDB: Medallion architecture (Bronze/Silver/Gold)
- LanceDB: Vector search, HNSW index
- Golden Masters: Deterministic baselines

### Component 3: Remaining Port Powers

| Port | Power | Key Topics |
|------|-------|------------|
| 0 | hfo-port-0-observer | Human.js, MediaPipe, CanonicalHandState, camera |
| 1 | hfo-port-1-bridger | NATS, CloudEvents, TraceContext, stigmergy |
| 2 | hfo-port-2-shaper | 1Euro, Kalman, XState, CanonicalIntent |
| 3 | hfo-port-3-injector | Godot, dwell, pinch, scroll, game |
| 5 | hfo-port-5-immunizer | Pydantic, invariants, MBSE, regression guards |

### Component 4: Cross-Cutting Power

**Purpose**: HFO-specific methodology that spans all ports.

**Key Topics**:
- Apex Assimilation: Exemplar adoption workflow
- Strangler Fig: Legacy wrapping pattern
- Exemplar Composition: 70% exemplar / 30% glue
- Capacity Engineering: Wardley value chain
- MBSE: Model-Based Systems Engineering

### Component 2: Converted human-js Power (Knowledge Base Only)

**Current State**: MCP Power with server code
**Target State**: Knowledge Base Power (docs only)

**Files to DELETE**:
- `.kiro/powers/human-js/mcp.json`
- `.kiro/powers/human-js/src/` (entire directory)
- `.kiro/powers/human-js/package.json`
- `.kiro/powers/human-js/tsconfig.json`
- `.kiro/powers/human-js/node_modules/` (if exists)

**Files to KEEP and UPDATE**:
- `POWER.md` - Update to remove MCP server references
- `steering/gesture-recognition.md` - Keep as-is
- `steering/hand-tracking.md` - Keep as-is

**Updated POWER.md Content**:
```markdown
---
name: human-js
displayName: Human.js Hand Tracking
description: Documentation for Human.js v3.3.6 hand tracking and gesture recognition
keywords: human, hand, gesture, finger, keypoints, curl, direction, pose, tracking
author: HFO Gen 76
---

# Human.js Knowledge Base Power

## Overview
Human.js v3.3.6 provides comprehensive hand tracking and gesture recognition.
This is a **Knowledge Base Power** - documentation only, no MCP server.

## Built-in Capabilities (DO NOT REINVENT)
- 21 hand keypoints (palm + 4 per finger)
- Finger curl detection: none, half, full
- Finger direction: 8 directions
- Built-in gestures: thumbsUp, victory, point, middleFinger, openPalm
- Custom gesture definition via FingerGesture class
- Frame interpolation (time-based weighted average)

## Steering Files
- `steering/gesture-recognition.md` - Gesture detection patterns
- `steering/hand-tracking.md` - Hand tracking setup and configuration

## API Reference
See `docs/human-js-api-reference-2025-12-17.md` for full API documentation.
```

### Component 3: typescript-patterns Power (NEW)

**Purpose**: TypeScript coding standards for consistent AI-generated code.

**POWER.md**:
```markdown
---
name: typescript-patterns
displayName: TypeScript Patterns
description: TypeScript coding standards and best practices for HFO
keywords: typescript, ts, interface, type, async, await, strict, import, export
author: HFO Gen 76
---

# TypeScript Patterns Knowledge Base

## Overview
Coding standards for TypeScript in the HFO ecosystem.

## Key Patterns
- Strict mode always enabled
- Interface over type for object shapes
- Result<T, E> pattern for error handling
- fast-check for property-based testing

## Steering Files
- `steering/coding-standards.md` - Full coding standards
```

### Component 4: python-patterns Power (NEW)

**Purpose**: Python coding standards for consistent AI-generated code.

**POWER.md**:
```markdown
---
name: python-patterns
displayName: Python Patterns
description: Python coding standards and best practices for HFO
keywords: python, py, dataclass, typing, async, pydantic, ruff, hypothesis
author: HFO Gen 76
---

# Python Patterns Knowledge Base

## Overview
Coding standards for Python in the HFO ecosystem.

## Key Patterns
- Type hints on all functions
- Pydantic v2 for data models
- Hypothesis for property-based testing
- ruff for linting and formatting

## Steering Files
- `steering/coding-standards.md` - Full coding standards
```

## Implementation Phases

### Phase 1: Foundation (Immediate)
1. Convert human-js to Knowledge Base Power
2. Create typescript-patterns Power
3. Create python-patterns Power
4. Add 8 port steering files to hfo-hexagonal

### Phase 2: Validation
1. Test keyword activation for each power
2. Verify steering file inclusion patterns
3. Run sample prompts to confirm documentation surfaces

### Phase 3: Iteration
1. Add content based on Ghost Cursor development needs
2. Update steering files as patterns emerge
3. Track which docs are most useful

## Keyword Coverage Matrix

| Port | Power | Primary Keywords | Secondary Keywords |
|------|-------|------------------|-------------------|
| 0 | hfo-hexagonal + human-js | human, hand, gesture, camera | keypoints, curl, direction, mediapipe |
| 1 | hfo-hexagonal | nats, cloudevents, trace | stigmergy, pubsub, envelope |
| 2 | hfo-hexagonal | 1euro, kalman, xstate | filter, smoothing, state, cursor |
| 3 | hfo-hexagonal | godot, dwell, click | pinch, scroll, game, trigger |
| 4 | hfo-hexagonal | hypothesis, fastcheck, chaos | fuzz, pbt, property, testing |
| 5 | hfo-hexagonal | pydantic, invariant, guard | validation, schema, regression |
| 6 | hfo-hexagonal | jsonl, duckdb, lancedb | replay, golden, parquet, medallion |
| 7 | hfo-hexagonal | pyribs, mcts, dse | pareto, qd, mpc, optimization |
| X | typescript-patterns | typescript, ts, interface | async, await, strict, import |
| X | python-patterns | python, py, dataclass | typing, pydantic, ruff, hypothesis |

## Success Metrics

1. **Activation Rate**: Powers activate when relevant keywords mentioned
2. **Hallucination Reduction**: AI uses documented APIs instead of inventing
3. **Consistency**: Generated code follows documented patterns
4. **Maintenance Burden**: 11 powers (8 ports + 3 cross-cutting) vs 45

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Keyword collisions | Use specific compound keywords (e.g., "1euro filter" not just "filter") |
| Steering file bloat | Keep each file focused, link to external docs |
| Stale documentation | Update steering files as part of exemplar integration |
| Missing coverage | Track which prompts don't activate powers, add keywords |

---

*Design Created: 2025-12-17 | HFO Gen 76 | Knowledge Powers Manifest*
*Architecture: 8 Port-Aligned Powers + 3 Cross-Cutting = 11 Total*
