# Ghost Cursor Architecture Audit - Gen 77.3

**Date:** 2025-12-19T05:30:00Z
**Auditor:** KIRO (HFO PREY Power)
**Status:** 🔴 CRITICAL VIOLATIONS FOUND

---

## 🔴 REWARD HACKING / THEATER IDENTIFIED

### 1. `index.html` = PURE THEATER (DELETE)

**Location:** `src/ghost_cursor/demo/index.html`

**Violations:**
- Lines 50-90: INLINE `OneEuroFilter` class - NOT using Port 2 Shaper
- Lines 150+: Directly calls `Human.js` - NOT using Port 0 Observer
- NO state machine (XState)
- NO CloudEvents envelope
- NO Bridger (Port 1)
- NO Assimilator (Port 6)

**Impact:** Tests using this file pass but don't validate the real architecture.

**Evidence:**
```javascript
// INLINE CODE - VIOLATES SPEC
class OneEuroFilter {
  constructor(freq, minCutoff = 1.0, beta = 0.0, dcutoff = 1.0) {
    // ... inline implementation
  }
}
```

### 2. Demo Fragmentation (3 files → should be 1)

| File | Uses Pipeline? | Status |
|:-----|:---------------|:-------|
| `index.html` | ❌ NO (inline code) | 🔴 DELETE |
| `index-bundled.html` | ✅ YES | 🟢 KEEP → RENAME |
| `pong.html` | ✅ YES | 🟡 MERGE as mode |

### 3. Soft Threshold Tests = REWARD HACKING

**Problem:** Tests use `minFrames >= 30` style thresholds that pass even when broken.

**Example:**
```javascript
// SOFT THRESHOLD - REWARD HACKING
if (results.totalFrames < CONFIG.expected.minFrames) {
  // This passes even if system is broken
}
```

**Fix:** Use strict golden master comparison with exact JSONL match.

---

## ✅ CORRECT ARCHITECTURE (pipeline.ts)

The spec-driven architecture follows HFO 8-port pattern:

```
Human.js → Port 0 Observer → Port 1 Bridger → Port 2 Shaper → Port 3 Injector
                                    ↓
                              Port 6 Assimilator (JSONL)
```

| Port | Role | Implementation | Status |
|:----:|:-----|:---------------|:-------|
| 0 | Observer | `HumanJsAdapter` | ✅ |
| 1 | Bridger | `EventEmitterBridger` | ✅ |
| 2 | Shaper | `Shaper` (1Euro + XState) | ✅ |
| 3 | Injector | `DOMConsumer` | ✅ |
| 6 | Assimilator | `JSONLRecorder` | ✅ |

---

## 🔧 CONSOLIDATION PLAN

### Phase 1: Delete Theater
- [ ] Delete `src/ghost_cursor/demo/index.html`

### Phase 2: Establish SSOT
- [ ] Rename `index-bundled.html` → `index.html`
- [ ] Update all test paths

### Phase 3: Merge Pong
- [ ] Add mode selector to index.html: 'cursor' | 'pong'
- [ ] Pong mode loads Phaser overlay dynamically
- [ ] Delete standalone `pong.html`

### Phase 4: Strict TDD
- [ ] Add golden master comparison (exact JSONL match)
- [ ] Add RED tests that FAIL on bad input
- [ ] Remove soft threshold tests

---

## 📊 Test File Analysis

| Test File | Uses Correct Demo? | Threshold Type |
|:----------|:-------------------|:---------------|
| `test_golden_video.js` | ✅ index-bundled.html | 🟡 Soft |
| `test_bundled_pipeline.js` | ✅ index-bundled.html | 🟡 Soft |
| `test_golden_2hands_armed.js` | ✅ index-bundled.html | 🟡 Soft |
| `pong_deterministic.test.ts` | N/A (unit test) | ✅ Strict |
| `test_red_green_contracts.ts` | N/A (unit test) | ✅ Strict |
| `test_property_based.ts` | N/A (unit test) | ✅ Strict |

---

## 🎯 VERDICT

**Architecture Compliance:** 60% (pipeline correct, demos fragmented)
**Test Integrity:** 70% (unit tests strict, integration tests soft)
**Reward Hacking Risk:** HIGH (index.html theater)

**Action Required:** Execute consolidation plan to achieve SSOT.

---

*Gen 77.3 | PREY Audit | 2025-12-19*
