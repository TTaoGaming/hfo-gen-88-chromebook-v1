# HFO Mosaic Gesture Cursor - SSOT Spec Manifest

> **Last Updated**: 2025-12-20T19:00:00Z
> **Generation**: 78.0
> **Spec**: `hfo-mosaic-gesture-cursor-2025-12-20T1900Z`
> **Tests**: 317 passing (276 vitest + 41 E2E) ✅ VALIDATED
> **Stigmergy**: `ObsidianBlackboard.jsonl`

---

## 🎯 Vision

A **polymorphic adapter system** that transforms noisy gesture data into trustworthy cursor input with UX protection against false positives and misclicks. Strict 8-port hexagonal architecture with BDD/TDD enforcement.

```
Noisy Gesture Data → [8-Port Pipeline] → Trustworthy Cursor + Click Protection
```

---

## 📍 Active Spec

| Spec | Purpose | Status |
|:-----|:--------|:-------|
| **hfo-mosaic-gesture-cursor-2025-12-20T1900Z** | Polymorphic gesture-to-cursor with antifragile protection | ✅ Spec Complete |

### Documents

| Document | Purpose |
|:---------|:--------|
| `requirements.md` | Phased requirements (0-N+1) with strict port contracts |
| `design.md` | Architecture, data models, BDD scenarios |
| `tasks.md` | Implementation tasks with port enforcement |

---

## 🕸️ 8-Port Architecture (STRICT Boundaries)

| Port | Trigram | Role | MUST DO | MUST NOT |
|:-----|:--------|:-----|:--------|:---------|
| 0 | ☷ Earth | **SENSE** | Pass raw data unchanged | Transform, filter, compute |
| 1 | ☶ Mountain | **CONNECT** | Route events, pub/sub | Transform, decide |
| 2 | ☵ Water | **TRANSFORM** | Filter, smooth, compute | Store, strategic decisions |
| 3 | ☴ Wind | **DELIVER** | Output to targets | Transform, store |
| 4 | ☳ Thunder | **CHAOS** | Inject faults, test | Normal operation |
| 5 | ☲ Fire | **VALIDATE** | Enforce contracts | Transform |
| 6 | ☱ Lake | **REMEMBER** | Log, record, replay | Transform |
| 7 | ☰ Heaven | **NAVIGATE** | Strategic decisions, flags | Transform |

### Port Violation Detection

```typescript
// BDD: Port 0 MUST NOT transform
Given landmarks from Human.js
When Port 0 receives landmarks
Then Port 0 SHALL emit unchanged landmarks
And Port 0 SHALL NOT compute angles
And Port 0 SHALL NOT apply filters
```

---

## 📊 Implementation Status

### ✅ DONE (Verified 2025-12-20T17:25:00Z)

| Port | Components | Tests | Status |
|:-----|:-----------|:------|:-------|
| 0 Observer | HumanJsAdapter, FingerCurlEngine*, AngleKalman* | 36 | ⚠️ *Move to Port 2 |
| 1 Bridger | EventEmitter, Stigmergy (Memory/File/Composite) | 28 | ✅ Real |
| 2 Shaper | 1Euro, StateMachine, CurlToClick, DwellToClick | 38 | ✅ Real |
| 3 Injector | DOMConsumer, PhaserPong, Input Adapters | 49 | ✅ Real |
| 5 Immunizer | Property tests, Golden masters, RED/GREEN | 64 | ✅ Real |
| 6 Assimilator | JSONLRecorder, ReplayAdapter, StigmergyLogger | 18 | ✅ Real |
| 7 Navigator | FlagManager, FlagControlPanel | 14 | ✅ Real |

**⚠️ Port Violation Found**: `FingerCurlEngine` and `AngleKalman` are in Port 0 but perform transformation. Should be in Port 2.

### ⏳ PENDING

| Port | Components | Priority |
|:-----|:-----------|:---------|
| 4 Disruptor | Red team testing, chaos injection | P3 |
| 5 Immunizer | Contract gates, schema validation | P1 |
| Infrastructure | NATS, JetStream | P2 |

### 🎭 THEATER (Code exists, not wired)

| Component | Issue | Fix |
|:----------|:------|:----|
| FireJuiceScene | Not receiving intent | Wire to Port 3 output |
| SpatialPaddleAssigner | Not used | Wire to multi-hand |
| AR Effects (Trail, Spark, Particles) | Not rendering | Wire to FireJuiceScene |

---

## 🔴 Known Issues

| Issue | Severity | Root Cause | Phase |
|:------|:---------|:-----------|:------|
| Port 0 transforms data | High | FingerCurlEngine in wrong port | Phase 0 |
| Lag (60-90ms) | Medium | Human.js inference + filters | Phase 1 |
| Arming inconsistent | High | Threshold mismatch (noneMax: 0.8) | Phase 1 |
| AR effects not working | Medium | FireJuiceScene not wired | Phase 2 |

---

## 📅 Spec Timeline (26 Archived)

### Week 1: 2025-12-14 to 2025-12-16

| Date | Spec | Status | Deliverables |
|:-----|:-----|:-------|:-------------|
| 12-14 | hfo-database-consolidation | ❌ | DuckDB (broken) |
| 12-15 | hfo-daily-2025-12-15 | ✅ | Project structure |
| 12-15 | hfo-ai-memory-system | ⚠️ | Memory concepts |
| 12-15 | hfo-silver-datalake | ❌ | LanceDB (broken) |
| 12-16 | gesture-ninja-mvp | ✅ | Initial gesture detection |
| 12-16 | gesture-ninja-golden-testing | ✅ | Golden fixtures |

### Week 2: 2025-12-17 to 2025-12-19

| Date | Spec | Status | Deliverables |
|:-----|:-----|:-------|:-------------|
| 12-17 | hfo-mosaic-ghost-cursor-2025-12-17 | ✅ | Contracts, physics |
| 12-18 | hfo-mosaic-ghost-cursor-2025-12-18 | ✅ | Core pipeline, 55 tests |
| 12-18 | hfo-prey-powers-2025-12-18 | ✅ | Stigmergy substrate |
| 12-19 | hfo-mosaic-ghost-cursor-2025-12-19 | ✅ | Multi-hand, handedness |
| 12-19 | ghost-cursor-ar-fire-juice | ✅ | AR effects code |

### Week 3: 2025-12-20

| Date | Spec | Status | Deliverables |
|:-----|:-----|:-------|:-------------|
| 12-20 | gesture-pong-ar-2025-12-20 | ✅ | Pong + AR integration |
| 12-20 | hfo-genesis-2025-12-20T1530Z | ✅ | Debug spec, validation |
| 12-20 | **hfo-mosaic-gesture-cursor-2025-12-20T1900Z** | 🔄 | Unified SSOT |

---

## 🎯 Phase Roadmap

| Phase | Focus | Requirements | Effort | Status |
|:------|:------|:-------------|:-------|:-------|
| **0 Infra** | Port contracts, BDD enforcement | 0.1-0.3 | 8h | ⚠️ Needs BDD |
| **0 Core** | Canonical contracts, Shaper pipeline | 0.4-0.6 | 12h | ✅ Needs refactor |
| **1 Debug** | WinBox, thresholds, profiler | 1.1-1.3 | 10h | ⏳ Pending |
| **2 Adapters** | Input/Output/Replay adapters | 2.1-2.3 | 8h | ⚠️ Partial |
| **3 Antifragile** | Contract gates, confidence, noise | 3.1-3.3 | 12h | ⏳ Pending |
| **N+1** | Multi-hand, gestures, NATS | N.1-N.3 | 20h+ | ⏳ Future |

---

## 🧪 Test Commands

```bash
npm run test:all    # 317 tests (276 vitest + 41 E2E)
npm run serve       # http://localhost:3000/demo/app.html

# Validate spec rollup
node scripts/validate_spec_rollup.js
```

---

## 📁 Archive Structure

```
.kiro/specs/
├── MANIFEST.md                                    # ← This file (SSOT)
├── hfo-mosaic-gesture-cursor-2025-12-20T1900Z/   # Active spec
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── _archive/
    ├── hfo-genesis-2025-12-20T1530Z/             # Previous debug spec
    ├── 2025-12-20-pre-genesis/
    ├── 2025-12-20-consolidation/
    └── [23+ older specs]
```

---

## 🔗 Related Documents

| Document | Purpose |
|:---------|:--------|
| `MANIFEST.md` (root) | Project navigation |
| `AGENTS.md` | PREY workflow |
| `ObsidianBlackboard.jsonl` | Stigmergy log |
| `.kiro/HANDOFF_2025-12-20.md` | Agent handoff |

---

*HFO Gen 78 | Mosaic Gesture Cursor | 2025-12-20T19:30:00Z | 317 Tests*
