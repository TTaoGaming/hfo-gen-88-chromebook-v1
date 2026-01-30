---
hfo:
  gen: 78
  ts: 2025-12-19T19:08:48.200Z
  port: 6
  role: REMEMBER
  trigram: ☱
  pillar: Assimilator
  greek: Μνήμη
  phase: PERCEIVE
  status: active
  desc: requirements
---

# Requirements Document: HFO Mosaic Gesture Cursor

## Introduction

HFO Mosaic Gesture Cursor is a **polymorphic adapter system** that transforms noisy gesture data into trustworthy cursor input with UX protection against false positives and misclicks. The system follows strict 8-port hexagonal architecture with BDD/TDD enforcement.

**Vision**: A robust, antifragile gesture-to-cursor pipeline that accepts plugin-style adapters at each port boundary, enabling polymorphic input sources and output targets.

**Scope**: Noisy gesture data → Trustworthy cursor with click protection → Any target application

## Glossary

- **Mosaic**: Composable, swappable components that form a unified system
- **Polymorphic_Adapter**: Interface that accepts multiple implementations (Human.js, MediaPipe, Leap Motion, etc.)
- **Antifragile**: System that improves under stress through feedback loops
- **Port**: Hexagonal architecture boundary with strict input/output contracts
- **Observer**: Port 0 - SENSE only, NO transformation (raw data passthrough)
- **Bridger**: Port 1 - CONNECT only, routing and pub/sub
- **Shaper**: Port 2 - TRANSFORM only, all data transformation happens here
- **Injector**: Port 3 - DELIVER only, output to target systems
- **Disruptor**: Port 4 - CHAOS, red team testing
- **Immunizer**: Port 5 - VALIDATE, contract enforcement
- **Assimilator**: Port 6 - REMEMBER, logging and replay
- **Navigator**: Port 7 - NAVIGATE, strategic decisions and flags
- **Cold_Stigmergy**: File-based indirect coordination through embedded metadata headers
- **Hot_Stigmergy**: Real-time message-based coordination via NATS JetStream
- **Quine**: Self-describing code that contains its own specification
- **Trigram**: I Ching symbol representing port's nature (☷☶☵☴☳☲☱☰)
- **Greek_Ontology**: Philosophical concept mapping for each port
- **JADC2**: Joint All-Domain Command and Control (military C2 alignment)

## Port Responsibility Matrix (STRICT)

| Port | Role | MUST DO | MUST NOT DO |
|:-----|:-----|:--------|:------------|
| 0 Observer | SENSE | Pass raw data unchanged | Transform, filter, or compute |
| 1 Bridger | CONNECT | Route events, pub/sub | Transform data, make decisions |
| 2 Shaper | TRANSFORM | Filter, smooth, compute state | Store data, make strategic decisions |
| 3 Injector | DELIVER | Output to targets | Transform data, store data |
| 4 Disruptor | CHAOS | Inject faults, test resilience | Normal operation |
| 5 Immunizer | VALIDATE | Enforce contracts, validate | Transform data |
| 6 Assimilator | REMEMBER | Log, record, replay | Transform data |
| 7 Navigator | NAVIGATE | Strategic decisions, flags | Transform data |

---

## Phase 0: Chores (GitOps & Generation Increment)

### Requirement 0.0: Gen 77 → Gen 78 Transition

**User Story:** As a developer, I want to archive Gen 77 state and increment to Gen 78, so that I have a clean quine backup and clear version boundary.

#### Acceptance Criteria

1. WHEN Gen 77 archive is created THEN the system SHALL copy current state to `HFO_buds/generation_77/`
2. WHEN archiving THEN the system SHALL include MANIFEST.md, AGENTS.md, ObsidianBlackboard.jsonl
3. WHEN archiving THEN the system SHALL include all spec documents
4. WHEN archiving THEN the system SHALL create `GEN_77_QUINE.md` with complete state summary
5. WHEN archive is complete THEN the system SHALL log to stigmergy with file list

### Requirement 0.0.1: Cold Stigmergy Header Schema

**User Story:** As a developer, I want a standardized Cold Stigmergy header format for all source files, so that the codebase is self-describing and machine-traversable.

#### Acceptance Criteria

1. WHEN a TypeScript file is created THEN the system SHALL include a Cold Stigmergy header in JSDoc comment format
2. WHEN a Markdown file is created THEN the system SHALL include a Cold Stigmergy header in YAML frontmatter format
3. WHEN parsing a header THEN the system SHALL extract all fields as structured data
4. IF a header is malformed THEN the system SHALL report validation errors with line numbers
5. WHEN a header is valid THEN the system SHALL be parseable by both regex and YAML parser

### Requirement 0.0.2: Cold Stigmergy Core Identity Layer

**User Story:** As a developer, I want every file to declare its generation and timestamp, so that I can track version history.

#### Acceptance Criteria

1. WHEN a header is created THEN the system SHALL include `gen` field with integer generation number
2. WHEN a header is created THEN the system SHALL include `ts` field with ISO 8601 timestamp
3. WHEN generation increments THEN the system SHALL update all active file headers
4. IF `gen` is missing THEN the Immunizer SHALL reject the file
5. WHEN comparing files THEN the system SHALL use `gen` for version ordering

### Requirement 0.0.3: Cold Stigmergy Port Ontology Layer

**User Story:** As a developer, I want every file to declare its port assignment with full ontology, so that the architecture is self-documenting.

#### Acceptance Criteria

1. WHEN a header is created THEN the system SHALL include `port` field (0-7)
2. WHEN a header is created THEN the system SHALL include `role` field matching port responsibility
3. WHEN a header is created THEN the system SHALL include `trigram` field (☷☶☵☴☳☲☱☰)
4. WHEN a header is created THEN the system SHALL include `pillar` field (Observer/Bridger/Shaper/etc.)
5. WHEN a header is created THEN the system SHALL include `phase` field (PERCEIVE/REACT/EXECUTE/YIELD)
6. IF port and role mismatch THEN the Immunizer SHALL flag for refactoring
7. WHEN Assimilator traverses THEN the system SHALL group files by port

### Requirement 0.0.4: Cold Stigmergy Status and Contracts

**User Story:** As a developer, I want to track file lifecycle status and port boundary contracts, so that deprecated code is visible and data flow is documented.

#### Acceptance Criteria

1. WHEN a header is created THEN the system SHALL include `status` field (active/deprecated/theater/archived)
2. WHEN status is "deprecated" THEN the system SHALL warn on import
3. WHERE file is at port boundary THEN the system SHALL include `contracts` section with input/output
4. IF contract is undefined THEN the Immunizer SHALL reject
5. WHEN Assimilator traverses THEN the system SHALL build contract dependency graph

### Requirement 0.0.5: Cold Stigmergy Validation (Port 5 Immunizer)

**User Story:** As a developer, I want the Immunizer to validate all headers on CI, so that invalid headers are caught early.

#### Acceptance Criteria

1. WHEN CI runs THEN the Immunizer SHALL validate all Cold Stigmergy headers
2. IF header is missing THEN the Immunizer SHALL fail with "MISSING_HEADER" error
3. IF required field is missing THEN the Immunizer SHALL fail with field name
4. IF port/role mismatch THEN the Immunizer SHALL warn with suggestion
5. WHEN all headers valid THEN the Immunizer SHALL report summary statistics

### Requirement 0.0.6: Cold Stigmergy Knowledge Graph (Port 6 Assimilator)

**User Story:** As an AI agent, I want to traverse Cold Stigmergy headers to understand codebase structure, so that I can make informed decisions.

#### Acceptance Criteria

1. WHEN Assimilator starts THEN the system SHALL scan all files for headers
2. WHEN headers are found THEN the system SHALL build in-memory knowledge graph
3. WHEN querying by port THEN the system SHALL return all files for that port
4. WHEN querying by contract THEN the system SHALL return dependency chain
5. WHEN file is modified THEN the system SHALL update knowledge graph incrementally

### Requirement 0.0.7: Hot Stigmergy Bridge (P2+)

**User Story:** As a developer, I want Cold Stigmergy headers to map to Hot Stigmergy subjects, so that file metadata can route NATS messages.

#### Acceptance Criteria

1. WHERE NATS integration is enabled THEN the system SHALL derive subject from header
2. WHEN deriving subject THEN the system SHALL use pattern: `hfo.{gen}.port{port}.{pillar}.{phase}`
3. WHEN file is modified THEN the system SHALL publish change event to derived subject
4. IF NATS is unavailable THEN the system SHALL fallback to Cold Stigmergy only

---

## Cold Stigmergy Header Format

### TypeScript Format

```typescript
/**
 * @hfo-cold-stigmergy
 * ---
 * gen: 78
 * ts: 2025-12-20T20:00:00Z
 * port: 2
 * role: TRANSFORM
 * trigram: ☵
 * pillar: Shaper
 * greek: Μορφή
 * phase: EXECUTE
 * status: active
 * contracts:
 *   input: CanonicalHandState
 *   output: CanonicalIntent
 * desc: One Euro Filter - Position smoothing
 * ---
 */
```

### Markdown Format

```yaml
---
hfo:
  gen: 78
  ts: 2025-12-20T20:00:00Z
  port: 6
  role: REMEMBER
  trigram: ☱
  pillar: Assimilator
  greek: Μνήμη
  phase: PERCEIVE
  status: active
---
```

### Port Ontology (Single Source of Truth)

| Port | Trigram | Pillar | Greek | Role | Phase |
|:-----|:--------|:-------|:------|:-----|:------|
| 0 | ☷ | Observer | Αἴσθησις | SENSE | PERCEIVE |
| 1 | ☶ | Bridger | Σύνδεσμος | CONNECT | REACT |
| 2 | ☵ | Shaper | Μορφή | TRANSFORM | EXECUTE |
| 3 | ☴ | Injector | Ἔκχυσις | DELIVER | EXECUTE |
| 4 | ☳ | Disruptor | Χάος | CHAOS | YIELD |
| 5 | ☲ | Immunizer | Ἀσφάλεια | VALIDATE | YIELD |
| 6 | ☱ | Assimilator | Μνήμη | REMEMBER | PERCEIVE |
| 7 | ☰ | Navigator | Κυβέρνησις | NAVIGATE | REACT |

---

### Requirement 0.0.8: Repo Cleanup

**User Story:** As a developer, I want the repo cleaned of stale files, so that the codebase is focused and navigable.

#### Acceptance Criteria

1. WHEN stale test files exist THEN the system SHALL archive to `reference/`
2. WHEN duplicate implementations exist THEN the system SHALL consolidate to SSOT
3. WHEN unused imports exist THEN the system SHALL remove them
4. WHEN dead code exists THEN the system SHALL archive or remove
5. WHEN cleanup is complete THEN the system SHALL run all tests to verify

### Requirement 0.0.9: Git Commit & Push

**User Story:** As a developer, I want a clean Git commit for Gen 78, so that the version boundary is clear in history.

#### Acceptance Criteria

1. WHEN all chores complete THEN the system SHALL stage all changes
2. WHEN committing THEN the system SHALL use message: "chore: Gen 78 - Mosaic Gesture Cursor SSOT"
3. WHEN commit includes THEN the system SHALL list: archive, version headers, cleanup, spec
4. IF tests fail THEN the system SHALL NOT commit
5. WHEN commit succeeds THEN the system SHALL log to stigmergy

---

## Phase 0: Mosaic Cursor Visualization (Vertical Slice)

### Requirement 0.1.0: Full-Screen Camera Background

**User Story:** As a developer, I want a full-screen WinBox with camera view as background, so that I can see my hand while testing the cursor pipeline.

#### Acceptance Criteria

1. WHEN app loads THEN the system SHALL display full-screen WinBox with camera feed
2. WHEN camera feed is active THEN the system SHALL mirror horizontally (scaleX: -1)
3. WHEN camera feed is active THEN the system SHALL fill entire WinBox background
4. IF camera permission denied THEN the system SHALL display fallback gradient
5. WHEN Phaser overlay is active THEN the system SHALL render on top of camera

### Requirement 0.1.1: Mosaic Cursor Layers (3-Layer Visualization)

**User Story:** As a developer, I want to see three cursor layers simultaneously, so that I can compare raw, smooth, and predictive cursor behavior.

#### Acceptance Criteria

1. WHEN hand is detected THEN the system SHALL render Layer 1: Raw Cursor (noisy fingertip)
2. WHEN hand is detected THEN the system SHALL render Layer 2: Smooth Cursor (state machine + coasting)
3. WHEN hand is detected THEN the system SHALL render Layer 3: Predictive Cursor (Kalman + fire juice)
4. WHEN rendering layers THEN the system SHALL use distinct colors (raw=gray, smooth=blue, predictive=orange)
5. WHEN confidence is low THEN Layer 2 SHALL coast on last known position
6. WHEN all layers render THEN the system SHALL show position delta between layers

### Requirement 0.1.2: Layer 1 - Raw Cursor (Gray Dot)

**User Story:** As a developer, I want to see the raw noisy fingertip position, so that I can understand input quality.

#### Acceptance Criteria

1. WHEN index fingertip is detected THEN the system SHALL render gray dot at raw position
2. WHEN rendering raw cursor THEN the system SHALL NOT apply any smoothing
3. WHEN rendering raw cursor THEN the system SHALL show jitter magnitude
4. WHEN confidence < 0.3 THEN the system SHALL fade raw cursor to 50% opacity
5. WHEN hand is lost THEN the system SHALL hide raw cursor immediately

### Requirement 0.1.3: Layer 2 - Smooth Cursor (Blue Dot with State)

**User Story:** As a developer, I want to see the smoothed cursor with state machine visualization, so that I can tune state transitions.

#### Acceptance Criteria

1. WHEN index fingertip is detected THEN the system SHALL render blue dot at smoothed position
2. WHEN rendering smooth cursor THEN the system SHALL apply 1Euro filter
3. WHEN state changes THEN the system SHALL show state label (IDLE/TRACKING/ARMED/COASTING)
4. WHEN confidence < 0.5 THEN the system SHALL enter COASTING state
5. WHEN COASTING THEN the system SHALL maintain last position with decay
6. WHEN state is ARMED THEN the system SHALL show armed indicator (ring around cursor)

### Requirement 0.1.4: Layer 3 - Predictive Cursor (Fire Juice)

**User Story:** As a developer, I want to see the predictive cursor with fire visual effects, so that I can tune the "feel" of the cursor.

#### Acceptance Criteria

1. WHEN index fingertip is detected THEN the system SHALL render fire cursor at predicted position
2. WHEN rendering fire cursor THEN the system SHALL apply Kalman filter with prediction
3. WHEN cursor moves THEN the system SHALL render fire particle trail
4. WHEN cursor velocity > threshold THEN the system SHALL increase fire intensity
5. WHEN cursor is stationary THEN the system SHALL show ember glow effect
6. WHEN fire renders THEN the system SHALL use orange/red color palette

### Requirement 0.1.5: Fire Elemental Configuration

**User Story:** As a developer, I want to tune fire visual parameters, so that the cursor feels responsive and satisfying.

#### Acceptance Criteria

1. WHEN tuning panel opens THEN the system SHALL expose fire particle count (10-100)
2. WHEN tuning panel opens THEN the system SHALL expose trail length (5-30 frames)
3. WHEN tuning panel opens THEN the system SHALL expose ember glow radius (5-20px)
4. WHEN tuning panel opens THEN the system SHALL expose velocity-to-intensity mapping
5. WHEN tuning panel opens THEN the system SHALL expose color temperature (warm/hot)
6. WHEN "Save Preset" is clicked THEN the system SHALL persist fire config to localStorage

### Requirement 0.1.6: Phaser Overlay Integration

**User Story:** As a developer, I want Phaser to render cursor layers on top of camera, so that I have a unified visualization.

#### Acceptance Criteria

1. WHEN Phaser scene loads THEN the system SHALL set transparent background
2. WHEN Phaser scene loads THEN the system SHALL match camera dimensions
3. WHEN rendering cursors THEN the system SHALL use Phaser graphics for dots
4. WHEN rendering fire THEN the system SHALL use Phaser particle emitter
5. WHEN rendering state labels THEN the system SHALL use Phaser text objects
6. WHEN window resizes THEN the system SHALL scale Phaser canvas proportionally

---

## Phase 0: Infrastructure Foundation

### Requirement 0.2: Port Contract Enforcement

**User Story:** As a developer, I want strict BDD contracts at each port boundary, so that port responsibilities are never violated.

#### Acceptance Criteria

1. WHEN data enters Port 0 THEN the system SHALL pass it unchanged to Port 1
2. WHEN Port 0 receives landmarks THEN the system SHALL NOT compute angles or curl state
3. WHEN Port 2 receives data THEN the system SHALL perform all transformations
4. IF any port violates its contract THEN the system SHALL log violation to stigmergy
5. WHEN running tests THEN the system SHALL verify port contracts via BDD scenarios

### Requirement 0.3: Polymorphic Observer Adapters

**User Story:** As a developer, I want to swap gesture input sources without changing downstream code, so that I can support multiple tracking systems.

#### Acceptance Criteria

1. WHEN Human.js adapter is active THEN the system SHALL produce CanonicalLandmarks
2. WHEN MediaPipe adapter is active THEN the system SHALL produce CanonicalLandmarks
3. WHEN Replay adapter is active THEN the system SHALL produce CanonicalLandmarks
4. WHERE a new adapter is added THEN the system SHALL only require implementing IObserverAdapter
5. WHEN adapter produces data THEN the system SHALL NOT transform it in Port 0

### Requirement 0.4: Stigmergy Coordination

**User Story:** As a developer, I want all port events logged to ObsidianBlackboard, so that I have complete audit trail and can replay sessions.

#### Acceptance Criteria

1. WHEN any port processes data THEN the system SHALL log PREY phase to stigmergy
2. WHEN threshold is changed THEN the system SHALL log old and new values
3. WHEN error occurs THEN the system SHALL log error with port and phase
4. WHEN session starts THEN the system SHALL create session ID in stigmergy
5. WHEN session ends THEN the system SHALL log session summary

---

## Phase 0: Mosaic Gesture Cursor Core

### Requirement 0.5: Canonical Data Contracts

**User Story:** As a developer, I want well-defined data contracts between ports, so that components are truly swappable.

#### Acceptance Criteria

1. WHEN Port 0 outputs data THEN the system SHALL use CanonicalLandmarks contract
2. WHEN Port 2 outputs data THEN the system SHALL use CanonicalIntent contract
3. WHEN Port 3 receives intent THEN the system SHALL accept any CanonicalIntent
4. IF contract validation fails THEN the system SHALL reject data with error
5. WHEN contracts change THEN the system SHALL version them with breaking change detection

### Requirement 0.6: Shaper Transformation Pipeline

**User Story:** As a developer, I want all data transformation in Port 2 Shaper, so that port responsibilities are clear.

#### Acceptance Criteria

1. WHEN landmarks arrive at Port 2 THEN the system SHALL compute joint angles
2. WHEN angles are computed THEN the system SHALL apply Kalman filtering
3. WHEN filtered angles exist THEN the system SHALL compute curl state
4. WHEN curl state changes THEN the system SHALL update armed/clicking state
5. WHEN position is computed THEN the system SHALL apply 1Euro smoothing
6. WHEN all transformations complete THEN the system SHALL emit CanonicalIntent

### Requirement 0.7: Click Protection (Antifragile)

**User Story:** As a user, I want protection against false positives and misclicks, so that the cursor is trustworthy.

#### Acceptance Criteria

1. WHEN curl state flickers THEN the system SHALL apply hysteresis debouncing
2. WHEN click is detected THEN the system SHALL require minimum hold time (50ms)
3. WHEN release is detected THEN the system SHALL require minimum release time (30ms)
4. IF rapid click/release occurs THEN the system SHALL suppress as noise
5. WHEN confidence is low THEN the system SHALL increase thresholds dynamically
6. WHEN confidence is high THEN the system SHALL decrease thresholds for responsiveness

---

## Phase 1: Debug & Tuning

### Requirement 1.1: Single Finger Debug WinBox

**User Story:** As a developer, I want a dedicated debug WinBox for single finger analysis, so that I can tune thresholds and identify issues.

#### Acceptance Criteria

1. WHEN debug WinBox opens THEN the system SHALL display raw landmark positions
2. WHEN debug WinBox opens THEN the system SHALL display computed angles (from Port 2)
3. WHEN debug WinBox opens THEN the system SHALL display curl state with visual indicator
4. WHEN debug WinBox opens THEN the system SHALL display armed state
5. WHEN debug WinBox opens THEN the system SHALL display latency breakdown by port
6. WHEN bypass toggles are enabled THEN the system SHALL show raw vs filtered comparison

### Requirement 1.2: Threshold Tuning Interface

**User Story:** As a developer, I want interactive threshold tuning, so that I can find optimal values for different users.

#### Acceptance Criteria

1. WHEN tuning panel opens THEN the system SHALL display current threshold values
2. WHEN noneMax slider is adjusted THEN the system SHALL update straight finger threshold (0.3-1.5 rad)
3. WHEN halfMax slider is adjusted THEN the system SHALL update half curl threshold (0.8-2.0 rad)
4. WHEN clickThreshold slider is adjusted THEN the system SHALL update click trigger (0.5-1.5 rad)
5. WHEN releaseThreshold slider is adjusted THEN the system SHALL update release trigger (0.3-1.0 rad)
6. WHEN "Save Preset" is clicked THEN the system SHALL persist to localStorage
7. WHEN "Reset Defaults" is clicked THEN the system SHALL restore original values

### Requirement 1.3: Latency Profiler

**User Story:** As a developer, I want to see latency at each port boundary, so that I can optimize the slowest components.

#### Acceptance Criteria

1. WHEN profiling is enabled THEN the system SHALL measure time at each port boundary
2. WHEN profiling is enabled THEN the system SHALL display latency waterfall chart
3. WHEN any port exceeds 20ms THEN the system SHALL highlight it in red
4. WHEN filters are bypassed THEN the system SHALL show latency comparison
5. WHEN total latency exceeds 100ms THEN the system SHALL warn user

---

## Phase 2: Polymorphic Adapters

### Requirement 2.1: Input Adapter Interface

**User Story:** As a developer, I want a standard interface for input adapters, so that I can add new gesture sources easily.

#### Acceptance Criteria

1. WHEN implementing IObserverAdapter THEN the system SHALL require `start()`, `stop()`, `onFrame()` methods
2. WHEN adapter produces frame THEN the system SHALL emit CanonicalLandmarks
3. WHEN adapter errors THEN the system SHALL emit error event without crashing
4. WHERE adapter supports confidence THEN the system SHALL include confidence in output
5. WHEN adapter is swapped THEN the system SHALL seamlessly continue pipeline

### Requirement 2.2: Output Adapter Interface

**User Story:** As a developer, I want a standard interface for output adapters, so that I can target different applications.

#### Acceptance Criteria

1. WHEN implementing IInjectorAdapter THEN the system SHALL require `onIntent()` method
2. WHEN intent arrives THEN the system SHALL call adapter's `onIntent()`
3. WHEN adapter is DOM THEN the system SHALL move cursor element
4. WHEN adapter is Phaser THEN the system SHALL update virtual pointer
5. WHEN adapter is WebSocket THEN the system SHALL send intent to remote
6. WHERE multiple adapters exist THEN the system SHALL broadcast to all

### Requirement 2.3: Replay Adapter

**User Story:** As a developer, I want to replay recorded sessions, so that I can test and debug without live camera.

#### Acceptance Criteria

1. WHEN replay adapter loads JSONL THEN the system SHALL parse frames
2. WHEN replay starts THEN the system SHALL emit frames at recorded timestamps
3. WHEN replay pauses THEN the system SHALL stop emitting frames
4. WHEN replay seeks THEN the system SHALL jump to specified timestamp
5. WHEN replay ends THEN the system SHALL emit end event

---

## Phase 3: Antifragile Protection

### Requirement 3.1: Contract Gates (Port 5 Immunizer)

**User Story:** As a developer, I want contract validation at port boundaries, so that invalid data is rejected early.

#### Acceptance Criteria

1. WHEN data enters any port THEN the system SHALL validate against contract schema
2. IF validation fails THEN the system SHALL reject with descriptive error
3. WHEN validation fails THEN the system SHALL log to stigmergy
4. WHERE schema is versioned THEN the system SHALL check version compatibility
5. WHEN contract gate is disabled THEN the system SHALL pass data through (dev mode)

### Requirement 3.2: Confidence-Based Thresholds

**User Story:** As a user, I want the system to adapt thresholds based on tracking confidence, so that it's more forgiving when tracking is poor.

#### Acceptance Criteria

1. WHEN confidence < 0.5 THEN the system SHALL increase click threshold by 20%
2. WHEN confidence < 0.3 THEN the system SHALL disable clicking entirely
3. WHEN confidence > 0.8 THEN the system SHALL use default thresholds
4. WHEN confidence > 0.95 THEN the system SHALL decrease thresholds for responsiveness
5. WHEN confidence changes THEN the system SHALL smooth threshold transitions

### Requirement 3.3: Noise Rejection

**User Story:** As a user, I want the system to reject noisy input, so that I don't get false clicks.

#### Acceptance Criteria

1. WHEN landmark jitter exceeds threshold THEN the system SHALL increase smoothing
2. WHEN angle change exceeds physical limits THEN the system SHALL reject as noise
3. WHEN hand disappears briefly (<200ms) THEN the system SHALL maintain last state
4. WHEN hand reappears THEN the system SHALL smoothly transition from last state
5. IF impossible state detected THEN the system SHALL log and recover gracefully

---

## Phase N+1: Future Expansion

### Requirement N.1: Multi-Hand Coordination

**User Story:** As a user, I want to use both hands simultaneously, so that I can have two cursors or gestures.

#### Acceptance Criteria

1. WHEN two hands detected THEN the system SHALL track both independently
2. WHEN hands cross THEN the system SHALL maintain identity via handedness
3. WHEN one hand disappears THEN the system SHALL continue tracking other
4. WHERE spatial zones exist THEN the system SHALL assign hands to zones

### Requirement N.2: Gesture Recognition

**User Story:** As a user, I want to perform gestures beyond pointing, so that I can trigger actions.

#### Acceptance Criteria

1. WHEN pinch gesture detected THEN the system SHALL emit pinch intent
2. WHEN swipe gesture detected THEN the system SHALL emit swipe intent with direction
3. WHEN custom gesture matches THEN the system SHALL emit custom intent
4. WHERE gesture conflicts with click THEN the system SHALL prioritize based on context

### Requirement N.3: Distributed Stigmergy (NATS)

**User Story:** As a developer, I want stigmergy events distributed via NATS, so that multiple agents can coordinate.

#### Acceptance Criteria

1. WHEN NATS is available THEN the system SHALL publish events to JetStream
2. WHEN NATS is unavailable THEN the system SHALL fallback to local stigmergy
3. WHEN events arrive from NATS THEN the system SHALL process as local events
4. WHERE multiple instances exist THEN the system SHALL coordinate via stigmergy

---

## Implementation Priority

| Phase | Requirements | Effort | Status |
|:------|:-------------|:-------|:-------|
| **0 Chores** | 0.0-0.0.9 | 6h | ✅ Cold Stigmergy Done |
| **0 Mosaic Viz (P0 Vertical Slice)** | 0.1.0-0.1.6 | 8h | 🔄 Next |
| 0 Cold Stigmergy | 0.0.1-0.0.7 | 4h | ✅ Done (22 tests) |
| 0 Infrastructure | 0.2-0.4 | 8h | ⚠️ Partial (needs BDD) |
| 0 Core | 0.5-0.7 | 12h | ✅ Done (needs refactor) |
| 1 Debug | 1.1-1.3 | 10h | ⏳ Pending |
| 2 Adapters | 2.1-2.3 | 8h | ⚠️ Partial |
| 3 Antifragile | 3.1-3.3 | 12h | ⏳ Pending |
| N+1 Future | N.1-N.3 | 20h+ | ⏳ Future |

---

*HFO Gen 78 | Mosaic Gesture Cursor + Cold Stigmergy | 2025-12-20T20:00:00Z*
