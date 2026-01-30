# Requirements Document: HFO Knowledge Powers Manifest

## Introduction

This spec defines a comprehensive manifest of **Knowledge Base Powers** (documentation-only, no MCP servers) that provide AI playbooks for the HFO ecosystem. The goal is to stop AI from "flying blind" by giving it reference documentation for every major technology, pattern, and exemplar used in the project.

**Problem Statement**: AI agents repeatedly reinvent solutions, hallucinate APIs, and make inconsistent decisions because they lack grounded reference documentation. This leads to:
- Reinventing Human.js finger curl detection instead of using built-in
- Inconsistent TypeScript patterns across files
- Forgetting NATS message formats
- Not knowing DuckDB SQL patterns for the data lake
- Missing JSONL conventions for replay files

**Solution**: Create Knowledge Base Powers (POWER.md + optional steering/) for each major technology. When AI mentions keywords, Kiro activates the power and provides grounded documentation.

**Phoenix Protocol**: Convert existing Human.js MCP Power to Knowledge Base Power (remove mcp.json, keep POWER.md + steering).

---

## Glossary

- **Knowledge_Base_Power**: A Kiro Power with only POWER.md (+ optional steering/), no mcp.json
- **Playbook**: Documentation that guides AI behavior for a specific technology
- **Exemplar**: A working open-source solution adopted into HFO
- **DSE**: Design Space Exploration - systematic evaluation of alternatives
- **AoA**: Analysis of Alternatives - NASA/DoD trade study methodology
- **HNSW**: Hierarchical Navigable Small World - vector index algorithm
- **Medallion**: Bronze→Silver→Gold data lake architecture
- **Stigmergy**: Indirect coordination via shared environment (NATS/JSONL)

---

## Requirements

### Requirement 1: Convert Human.js to Knowledge Base Power

**User Story:** As a developer, I want Human.js documentation available as a Knowledge Base Power, so that AI knows what Human.js provides without needing an MCP server.

#### Acceptance Criteria

1. WHEN converting Human.js power THEN the system SHALL remove mcp.json, package.json, tsconfig.json, src/, dist/, node_modules/
2. WHEN converting Human.js power THEN the system SHALL keep POWER.md and steering/ directory
3. WHEN Human.js keywords are mentioned THEN Kiro SHALL activate the power and provide documentation
4. WHEN AI needs finger curl detection THEN the documentation SHALL clearly state "Human.js provides this - DO NOT REINVENT"
5. WHEN AI needs gesture recognition THEN the documentation SHALL list all built-in gestures

### Requirement 2: TypeScript Patterns Power

**User Story:** As a developer, I want TypeScript best practices documented, so that AI writes consistent, idiomatic TypeScript code.

#### Acceptance Criteria

1. WHEN creating TypeScript power THEN the system SHALL document: strict mode, interface vs type, async/await patterns, error handling
2. WHEN AI writes TypeScript THEN the documentation SHALL provide import/export conventions
3. WHEN AI creates interfaces THEN the documentation SHALL show naming conventions (I-prefix or not)
4. WHEN AI handles errors THEN the documentation SHALL show Result<T, E> pattern vs try/catch
5. WHEN AI writes tests THEN the documentation SHALL reference fast-check for property-based testing

### Requirement 3: Python Patterns Power

**User Story:** As a developer, I want Python best practices documented, so that AI writes consistent, idiomatic Python code.

#### Acceptance Criteria

1. WHEN creating Python power THEN the system SHALL document: type hints, dataclasses, Pydantic models, async patterns
2. WHEN AI writes Python THEN the documentation SHALL provide import conventions (absolute vs relative)
3. WHEN AI creates data models THEN the documentation SHALL show Pydantic v2 patterns
4. WHEN AI handles errors THEN the documentation SHALL show exception hierarchy patterns
5. WHEN AI writes tests THEN the documentation SHALL reference Hypothesis for property-based testing

### Requirement 4: NATS Messaging Power

**User Story:** As a developer, I want NATS messaging patterns documented, so that AI correctly uses stigmergy coordination.

#### Acceptance Criteria

1. WHEN creating NATS power THEN the system SHALL document: JetStream, subjects, consumers, CloudEvents envelope
2. WHEN AI publishes messages THEN the documentation SHALL show CloudEvents format with specversion, type, source, id, time, data
3. WHEN AI subscribes to streams THEN the documentation SHALL show consumer patterns (push vs pull)
4. WHEN AI needs replay THEN the documentation SHALL show JetStream replay from sequence
5. WHEN AI needs tracing THEN the documentation SHALL show W3C Trace Context (traceparent header)

### Requirement 5: DuckDB Data Lake Power

**User Story:** As a developer, I want DuckDB patterns documented, so that AI correctly queries the Bronze/Silver/Gold data lake.

#### Acceptance Criteria

1. WHEN creating DuckDB power THEN the system SHALL document: Medallion architecture, Parquet files, SQL patterns
2. WHEN AI queries Bronze THEN the documentation SHALL explain raw ingested data (28.77 GB, 75 tables)
3. WHEN AI queries Silver THEN the documentation SHALL explain validated/cleaned data (15.19 GB, 51 tables)
4. WHEN AI queries Gold THEN the documentation SHALL explain LanceDB vectors (15,024 vectors)
5. WHEN AI writes SQL THEN the documentation SHALL show DuckDB-specific syntax (COPY, Parquet, JSON)

### Requirement 6: JSONL Conventions Power

**User Story:** As a developer, I want JSONL conventions documented, so that AI correctly formats replay files and logs.

#### Acceptance Criteria

1. WHEN creating JSONL power THEN the system SHALL document: line format, timestamp conventions, schema evolution
2. WHEN AI writes JSONL THEN the documentation SHALL show one JSON object per line, newline-terminated
3. WHEN AI reads JSONL THEN the documentation SHALL show streaming parse patterns
4. WHEN AI needs replay THEN the documentation SHALL show monotonic timestamp requirements
5. WHEN AI needs schema evolution THEN the documentation SHALL show version field patterns

### Requirement 7: LanceDB Vector Search Power

**User Story:** As a developer, I want LanceDB patterns documented, so that AI correctly uses semantic search.

#### Acceptance Criteria

1. WHEN creating LanceDB power THEN the system SHALL document: HNSW index, embedding models, search patterns
2. WHEN AI searches vectors THEN the documentation SHALL show semantic_search() usage
3. WHEN AI adds vectors THEN the documentation SHALL show embedding generation patterns
4. WHEN AI needs hybrid search THEN the documentation SHALL show combining vector + keyword search
5. WHEN AI needs DSE THEN the documentation SHALL show AoA trade analysis patterns

### Requirement 8: Kiro Powers & Hooks Power

**User Story:** As a developer, I want Kiro-specific patterns documented, so that AI correctly creates powers and hooks.

#### Acceptance Criteria

1. WHEN creating Kiro power THEN the system SHALL document: POWER.md frontmatter, steering files, hooks
2. WHEN AI creates a power THEN the documentation SHALL show the 5 valid frontmatter fields (name, displayName, description, keywords, author)
3. WHEN AI creates hooks THEN the documentation SHALL show trigger types (file_saved, session_created, manual)
4. WHEN AI creates steering THEN the documentation SHALL show inclusion modes (always, fileMatch, manual)
5. WHEN AI needs activation THEN the documentation SHALL show kiroPowers() action patterns

### Requirement 9: XState State Machine Power

**User Story:** As a developer, I want XState patterns documented, so that AI correctly implements state machines.

#### Acceptance Criteria

1. WHEN creating XState power THEN the system SHALL document: v5 syntax, states, transitions, guards, actions
2. WHEN AI creates state machines THEN the documentation SHALL show createMachine() patterns
3. WHEN AI needs guards THEN the documentation SHALL show condition-based transitions
4. WHEN AI needs actions THEN the documentation SHALL show entry/exit/transition actions
5. WHEN AI needs context THEN the documentation SHALL show typed context patterns

### Requirement 10: 1Euro Filter Power

**User Story:** As a developer, I want 1Euro filter patterns documented, so that AI correctly implements cursor smoothing.

#### Acceptance Criteria

1. WHEN creating 1Euro power THEN the system SHALL document: minCutoff, beta, dcutoff parameters
2. WHEN AI configures smoothing THEN the documentation SHALL explain velocity-adaptive behavior
3. WHEN AI needs presets THEN the documentation SHALL show Earth (stable) vs Thunder (responsive) configs
4. WHEN AI combines filters THEN the documentation SHALL show 1Euro + Kalman combination
5. WHEN AI needs tuning THEN the documentation SHALL show parameter sweep patterns

### Requirement 11: Hypothesis/fast-check PBT Power

**User Story:** As a developer, I want property-based testing patterns documented, so that AI correctly writes PBT tests.

#### Acceptance Criteria

1. WHEN creating PBT power THEN the system SHALL document: Hypothesis (Python), fast-check (TypeScript)
2. WHEN AI writes Python PBT THEN the documentation SHALL show @given decorator patterns
3. WHEN AI writes TypeScript PBT THEN the documentation SHALL show fc.property() patterns
4. WHEN AI needs generators THEN the documentation SHALL show custom strategy patterns
5. WHEN AI needs shrinking THEN the documentation SHALL explain minimal failing example

### Requirement 12: pyribs MAP-Elites Power

**User Story:** As a developer, I want pyribs patterns documented, so that AI correctly uses Quality-Diversity optimization.

#### Acceptance Criteria

1. WHEN creating pyribs power THEN the system SHALL document: archive, emitters, schedulers
2. WHEN AI adds to archive THEN the documentation SHALL show behavior descriptor + objective patterns
3. WHEN AI queries archive THEN the documentation SHALL show elite retrieval patterns
4. WHEN AI needs DSE THEN the documentation SHALL show Pareto frontier visualization
5. WHEN AI needs evolution THEN the documentation SHALL show emitter configuration

### Requirement 13: Godot 4 Integration Power

**User Story:** As a developer, I want Godot 4 patterns documented, so that AI correctly integrates with the game engine.

#### Acceptance Criteria

1. WHEN creating Godot power THEN the system SHALL document: GDScript patterns, signals, WebSocket bridge
2. WHEN AI writes GDScript THEN the documentation SHALL show typed syntax (var x: int)
3. WHEN AI needs signals THEN the documentation SHALL show signal declaration and connection
4. WHEN AI needs WebSocket THEN the documentation SHALL show JavaScript↔Godot bridge patterns
5. WHEN AI needs export THEN the documentation SHALL show HTML5 export configuration

### Requirement 14: HFO Architecture Power (Enhance Existing)

**User Story:** As a developer, I want the existing hfo-hexagonal power enhanced with more detailed playbooks, so that AI deeply understands the 8-port architecture.

#### Acceptance Criteria

1. WHEN enhancing HFO power THEN the system SHALL add steering files for each port
2. WHEN AI needs Observer patterns THEN the documentation SHALL show CanonicalHandState format
3. WHEN AI needs Bridger patterns THEN the documentation SHALL show CloudEvents + TraceContext
4. WHEN AI needs Shaper patterns THEN the documentation SHALL show filter pipeline
5. WHEN AI needs Navigator patterns THEN the documentation SHALL show MCTS + pyribs integration

### Requirement 15: Powers Manifest Registry

**User Story:** As a developer, I want a manifest of all required powers, so that I can track creation progress and ensure completeness.

#### Acceptance Criteria

1. WHEN creating manifest THEN the system SHALL list all powers with status (exists, needs-creation, needs-enhancement)
2. WHEN a power is created THEN the manifest SHALL be updated with creation date
3. WHEN a power needs enhancement THEN the manifest SHALL list specific gaps
4. WHEN querying manifest THEN the system SHALL show keyword coverage
5. WHEN all powers exist THEN the manifest SHALL show 100% coverage

---

## Powers Manifest by Obsidian Port

### Port 0: Observer ☷ (SENSE)

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| human-js | EXISTS (convert to KB) | human, hand, gesture, finger, keypoints, curl, direction | HIGH | Ghost Cursor Req 2 |
| mediapipe-hands | NEEDS CREATION | mediapipe, hands, landmarks, wasm, google | MEDIUM | Ghost Cursor Req 2 |
| canonical-hand-state | NEEDS CREATION | canonical, hand, state, 21, keypoints, normalized | HIGH | Ghost Cursor Req 1-2 |
| camera-placement | NEEDS CREATION | camera, normal, above, behind, placement, coordinate | MEDIUM | Ghost Cursor Req 14.5 |

### Port 1: Bridger ☶ (REASON)

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| nats-messaging | NEEDS CREATION | nats, jetstream, cloudevents, stigmergy, pubsub | HIGH | Ghost Cursor Req 3 |
| cloudevents-envelope | NEEDS CREATION | cloudevents, envelope, specversion, type, source, id | HIGH | Ghost Cursor Req 3 |
| w3c-trace-context | NEEDS CREATION | traceparent, tracecontext, opentelemetry, span, distributed | HIGH | Ghost Cursor Req 3 |
| sequential-thinking | NEEDS CREATION | sequential, thinking, reasoning, chain, thought | MEDIUM | HFO Architecture |

### Port 2: Shaper ☵ (ACT)

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| oneeuro-filter | NEEDS CREATION | 1euro, oneeuro, smoothing, filter, jitter, cursor, mincutoff, beta | HIGH | Ghost Cursor Req 4 |
| kalman-filter | NEEDS CREATION | kalman, prediction, latency, negative, predictor | MEDIUM | Ghost Cursor Req 4 |
| xstate-machines | NEEDS CREATION | xstate, state, machine, transition, guard, action, context | HIGH | Ghost Cursor Req 4 |
| canonical-intent | NEEDS CREATION | canonical, intent, position, velocity, confidence, armed | HIGH | Ghost Cursor Req 1 |
| inertial-coasting | NEEDS CREATION | coasting, inertial, tracking, loss, physics, continuation | MEDIUM | Ghost Cursor Req 4 |

### Port 3: Injector ☴ (TIME)

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| dwell-click | NEEDS CREATION | dwell, hover, click, timer, activation, cooldown | HIGH | Ghost Cursor Req 10 |
| pinch-click | NEEDS CREATION | pinch, thumb, index, click, gesture, nonmouse | HIGH | Ghost Cursor Req 10.5 |
| scroll-gesture | NEEDS CREATION | scroll, curl, index, finger, gesture | MEDIUM | Ghost Cursor Req 10.6 |
| temporal-workflows | NEEDS CREATION | temporal, workflow, activity, schedule, durable | MEDIUM | HFO Architecture |
| godot-integration | NEEDS CREATION | godot, gdscript, signal, websocket, game, export | HIGH | Ghost Cursor Req 5 |

### Port 4: Disruptor ☳ (CHAOS)

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| hypothesis-pbt | NEEDS CREATION | hypothesis, property, based, testing, python, given, strategy | HIGH | Ghost Cursor Req 6 |
| fastcheck-pbt | NEEDS CREATION | fast-check, fastcheck, property, testing, typescript, arbitrary | HIGH | Ghost Cursor Req 6 |
| chaos-testing | NEEDS CREATION | chaos, inject, failure, latency, error, timeout | MEDIUM | Ghost Cursor Req 6 |
| fuzz-testing | NEEDS CREATION | fuzz, fuzzing, corrupted, invalid, edge, case | MEDIUM | Ghost Cursor Req 6 |
| playwright-e2e | NEEDS CREATION | playwright, e2e, browser, automation, test | MEDIUM | HFO Architecture |

### Port 5: Immunizer ☲ (VALIDATE)

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| pydantic-validation | NEEDS CREATION | pydantic, validation, schema, model, v2, basemodel | HIGH | Ghost Cursor Req 7 |
| invariant-checks | NEEDS CREATION | invariant, check, guard, assertion, safety | HIGH | Ghost Cursor Req 7 |
| regression-guards | NEEDS CREATION | regression, guard, golden, master, baseline, delta | HIGH | Ghost Cursor Req 7 |
| opa-policies | NEEDS CREATION | opa, policy, rego, evaluate, authorization | LOW | HFO Architecture |
| zero-magic-numbers | NEEDS CREATION | magic, number, threshold, adaptive, configurable | MEDIUM | Ghost Cursor Req 15 |

### Port 6: Assimilator ☱ (REMEMBER)

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| jsonl-conventions | NEEDS CREATION | jsonl, replay, log, append, streaming, line | HIGH | Ghost Cursor Req 8 |
| duckdb-datalake | NEEDS CREATION | duckdb, parquet, medallion, bronze, silver, gold, sql | HIGH | HFO Architecture |
| lancedb-vectors | NEEDS CREATION | lancedb, hnsw, vectors, semantic, embedding, search | HIGH | HFO Architecture |
| golden-masters | NEEDS CREATION | golden, master, baseline, deterministic, comparison | HIGH | Ghost Cursor Req 8 |
| score-fusion | NEEDS CREATION | score, fusion, metrics, normalize, weight, pareto | HIGH | Ghost Cursor Req 8 |

### Port 7: Navigator ☰ (GOAL)

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| pyribs-qd | NEEDS CREATION | pyribs, map-elites, qd, quality, diversity, archive, emitter | HIGH | Ghost Cursor Req 9 |
| mcts-search | NEEDS CREATION | mcts, monte, carlo, tree, search, ucb1, exploration | MEDIUM | Ghost Cursor Req 9 |
| dse-aoa | NEEDS CREATION | dse, aoa, design, space, exploration, alternatives, trade | HIGH | Ghost Cursor Req 9 |
| pareto-frontier | NEEDS CREATION | pareto, frontier, optimal, tradeoff, dominated | MEDIUM | Ghost Cursor Req 9 |
| mpc-replan | NEEDS CREATION | mpc, model, predictive, control, horizon, replan | LOW | HFO Architecture |

### Cross-Cutting Powers

| Power Name | Status | Keywords | Priority | Source |
|------------|--------|----------|----------|--------|
| hfo-hexagonal | EXISTS (enhance) | hfo, hexagonal, ports, observer, bridger, shaper, injector, disruptor, immunizer, assimilator, navigator | HIGH | HFO Architecture |
| typescript-patterns | NEEDS CREATION | typescript, ts, interface, type, async, await, strict | HIGH | All TypeScript code |
| python-patterns | NEEDS CREATION | python, py, dataclass, typing, async, ruff | HIGH | All Python code |
| kiro-development | NEEDS CREATION | kiro, power, hook, steering, mcp, frontmatter | HIGH | Kiro IDE |
| strangler-fig | NEEDS CREATION | strangler, fig, wrap, legacy, exemplar, gradual | MEDIUM | Ghost Cursor Req 17 |
| polymorphic-adapters | NEEDS CREATION | polymorphic, adapter, port, interface, swap, vendor | MEDIUM | Ghost Cursor Req 16 |
| exemplar-workflow | NEEDS CREATION | exemplar, trl, source, integration, mosaic, commodity | HIGH | Ghost Cursor Req 17 |

---

## Summary Statistics

| Port | Powers Needed | HIGH Priority | MEDIUM Priority | LOW Priority |
|------|---------------|---------------|-----------------|--------------|
| 0 Observer | 4 | 2 | 2 | 0 |
| 1 Bridger | 4 | 3 | 1 | 0 |
| 2 Shaper | 5 | 3 | 2 | 0 |
| 3 Injector | 5 | 3 | 2 | 0 |
| 4 Disruptor | 5 | 2 | 3 | 0 |
| 5 Immunizer | 5 | 3 | 1 | 1 |
| 6 Assimilator | 5 | 5 | 0 | 0 |
| 7 Navigator | 5 | 2 | 2 | 1 |
| Cross-Cutting | 7 | 5 | 2 | 0 |
| **TOTAL** | **45** | **28** | **15** | **2** |

---

## Revised Architecture: 8 Versioned Port Powers

**Key Change**: Instead of 45 granular powers, create **8 versioned Knowledge Powers** (one per Obsidian port) that are continuously updated with Z-time timestamps for TTL tracking.

### Versioning Convention

```
POWER.md header:
---
name: hfo-port-7-navigator
displayName: HFO Navigator (Port 7)
description: DSE, AoA, MCTS, MPC, pyribs, Pareto optimization
keywords: navigator, dse, aoa, mcts, mpc, pyribs, pareto, qd, optimization
author: HFO Gen 76
version: 2025-12-17T00:00:00Z
ttl: P7D  # ISO 8601 duration - 7 days until stale
---
```

### The 8 Port Powers

| Port | Power Name | Priority | Key Topics |
|------|------------|----------|------------|
| 0 | hfo-port-0-observer | HIGH | Human.js, MediaPipe, CanonicalHandState, camera |
| 1 | hfo-port-1-bridger | HIGH | NATS, CloudEvents, TraceContext, stigmergy |
| 2 | hfo-port-2-shaper | HIGH | 1Euro, Kalman, XState, CanonicalIntent |
| 3 | hfo-port-3-injector | MEDIUM | Godot, dwell, pinch, scroll, game integration |
| 4 | hfo-port-4-disruptor | HIGH | TDD, BDD, Gherkin, Hypothesis, fast-check, chaos |
| 5 | hfo-port-5-immunizer | HIGH | Pydantic, invariants, regression guards, MBSE |
| 6 | hfo-port-6-assimilator | HIGH | JSONL, DuckDB, LanceDB, golden masters, Mermaid |
| 7 | hfo-port-7-navigator | **HIGHEST** | DSE, AoA, MCTS, MPC, pyribs, Pareto, JADC2, Mosaic |

---

## Requirement 16: Navigator Power (HIGHEST PRIORITY)

**User Story:** As a developer, I want comprehensive Navigator documentation, so that AI correctly uses DSE, AoA, and optimization patterns that are core to HFO's Mosaic Warfare architecture.

#### Acceptance Criteria

1. WHEN creating Navigator power THEN the system SHALL document: DSE (Design Space Exploration), AoA (Analysis of Alternatives)
2. WHEN AI needs optimization THEN the documentation SHALL show pyribs MAP-Elites patterns
3. WHEN AI needs planning THEN the documentation SHALL show MCTS (Monte Carlo Tree Search) patterns
4. WHEN AI needs control THEN the documentation SHALL show MPC (Model Predictive Control) patterns
5. WHEN AI needs trade analysis THEN the documentation SHALL show NASA-style AoA with TRL, risk, cost
6. WHEN AI needs Pareto optimization THEN the documentation SHALL show frontier visualization
7. WHEN AI needs military doctrine THEN the documentation SHALL explain JADC2 and Mosaic Warfare concepts
8. WHEN AI needs capacity engineering THEN the documentation SHALL show Wardley mapping patterns

### Requirement 17: Disruptor Power (TDD/BDD/Gherkin)

**User Story:** As a developer, I want testing methodology documentation, so that AI writes tests using proper TDD, BDD, and Gherkin patterns.

#### Acceptance Criteria

1. WHEN creating Disruptor power THEN the system SHALL document: TDD (Test-Driven Development) red-green-refactor
2. WHEN AI writes tests THEN the documentation SHALL show BDD (Behavior-Driven Development) patterns
3. WHEN AI writes acceptance criteria THEN the documentation SHALL show Gherkin Given/When/Then syntax
4. WHEN AI needs property testing THEN the documentation SHALL show Hypothesis (Python) and fast-check (TypeScript)
5. WHEN AI needs chaos testing THEN the documentation SHALL show failure injection patterns

### Requirement 18: Assimilator Power (Mermaid + Storage)

**User Story:** As a developer, I want documentation patterns, so that AI creates proper diagrams and storage patterns.

#### Acceptance Criteria

1. WHEN creating Assimilator power THEN the system SHALL document: Mermaid diagram syntax
2. WHEN AI creates flowcharts THEN the documentation SHALL show Mermaid flowchart patterns
3. WHEN AI creates sequence diagrams THEN the documentation SHALL show Mermaid sequenceDiagram patterns
4. WHEN AI creates state diagrams THEN the documentation SHALL show Mermaid stateDiagram-v2 patterns
5. WHEN AI needs storage THEN the documentation SHALL show JSONL, DuckDB, LanceDB patterns

### Requirement 19: Cross-Cutting Concepts Power

**User Story:** As a developer, I want HFO-specific methodology documentation, so that AI understands Apex Assimilation, Exemplar Composition, and Strangler Fig patterns.

#### Acceptance Criteria

1. WHEN creating cross-cutting power THEN the system SHALL document: Apex Assimilation workflow
2. WHEN AI needs exemplar adoption THEN the documentation SHALL show 70% exemplar / 30% glue pattern
3. WHEN AI needs legacy integration THEN the documentation SHALL show Strangler Fig wrapping pattern
4. WHEN AI needs capacity engineering THEN the documentation SHALL show Wardley value chain mapping
5. WHEN AI needs MBSE THEN the documentation SHALL show Model-Based Systems Engineering patterns

---

## Implementation Order (Revised - Navigator First)

**Phase 1: Navigator Power (Day 1) - HIGHEST PRIORITY**
1. Create hfo-port-7-navigator with DSE, AoA, MCTS, MPC, pyribs
2. Document JADC2 and Mosaic Warfare concepts
3. Document Pareto frontier optimization

**Phase 2: Disruptor Power (Day 1)**
1. Create hfo-port-4-disruptor with TDD, BDD, Gherkin
2. Document Hypothesis and fast-check patterns
3. Document chaos testing

**Phase 3: Core Pipeline Powers (Day 2)**
1. Create hfo-port-0-observer (Human.js, camera)
2. Create hfo-port-1-bridger (NATS, CloudEvents)
3. Create hfo-port-2-shaper (1Euro, XState)

**Phase 4: Remaining Powers (Day 3)**
1. Create hfo-port-3-injector (Godot, interactions)
2. Create hfo-port-5-immunizer (Pydantic, MBSE)
3. Create hfo-port-6-assimilator (Mermaid, storage)

**Phase 5: Cross-Cutting (Day 4)**
1. Create hfo-cross-cutting (Apex Assimilation, Strangler Fig)
2. Convert human-js to Knowledge Base
3. Create typescript-patterns and python-patterns

---

*Requirements Updated: 2025-12-17T00:00:00Z | HFO Gen 76 | Knowledge Powers Manifest*
*Architecture: 8 Versioned Port Powers + Cross-Cutting = 11 Total*
*Versioning: Z-time timestamps with TTL for auto-update tracking*
