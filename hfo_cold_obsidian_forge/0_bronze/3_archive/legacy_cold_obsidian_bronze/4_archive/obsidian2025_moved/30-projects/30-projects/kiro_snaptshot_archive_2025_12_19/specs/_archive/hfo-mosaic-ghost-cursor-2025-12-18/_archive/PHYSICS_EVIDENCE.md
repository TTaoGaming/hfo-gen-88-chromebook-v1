# Physics Evidence Report - Ghost Cursor Gen 77
> Timestamp: 2025-12-18T18:30:00-07:00
> Test: Golden Video `two_hands_baseline_idle_v1.mp4`
> Auditor: Playwright Headful Browser Test

## Executive Summary

| Metric | Expected | Actual | Status |
|:-------|:---------|:-------|:-------|
| Total Frames | ≥30 | 158 | ✅ PASS |
| Frames with Hands | ≥20 | 73 | ✅ PASS |
| Frames with 2 Hands | ≥5 | 29 | ✅ PASS |

**GOLDEN TEST: ✅ PASSED**

---

## Input Analysis

### Video File
- **Path:** `Inputs/Safe_Data/Spatial Input Mobile/September2025/TectangleHexagonal/videos/two_hands_baseline_idle_v1.mp4`
- **Duration:** 5.23 seconds
- **FPS:** 30
- **Total Frames:** 158

### Human.js Configuration
```javascript
{
  modelBasePath: 'https://cdn.jsdelivr.net/npm/@vladmandic/human/models',
  backend: 'webgl',
  hand: { enabled: true, maxDetected: 2 },
  gesture: { enabled: true }
}
```

---

## Output Analysis

### Hand Detection Timeline

| Frame Range | Hands Detected | Confidence | Notes |
|:------------|:---------------|:-----------|:------|
| 0-21 | 0 | - | No hands visible |
| 22-55 | 1 | 0.68-0.95 | Single hand detected |
| 56-84 | 2 | 0.85-0.88 | **TWO HANDS DETECTED** |
| 85-95 | 1 | 0.94 | One hand lost |
| 96-158 | 0 | - | Hands exit frame |

### Key Observations

1. **Multi-Hand Detection Works**: Frames 56-84 consistently detected 2 hands
2. **High Confidence**: Peak confidence 0.95 for single hand, 0.88/0.85 for dual hands
3. **21 Landmarks**: All detections returned full 21-point hand skeleton
4. **Index Tip Available**: `index_tip` coordinates extracted for cursor positioning

---

## Truth vs Theater Analysis

### ✅ TRUTH (Physics-Verified)

| Component | Evidence | Status |
|:----------|:---------|:-------|
| Human.js Detection | 73/158 frames with hands | ✅ WORKS |
| Multi-Hand | 29 frames with 2 hands | ✅ WORKS |
| 21 Landmarks | All detections have 21 | ✅ WORKS |
| Index Tip Extraction | Coordinates logged | ✅ WORKS |
| 1Euro Filter | Cursor smoothing visible | ✅ WORKS |
| Video Processing | 158 frames processed | ✅ WORKS |

### 🎭 THEATER (Not Yet Verified)

| Component | Claim | Reality |
|:----------|:------|:--------|
| `detectAll()` in TypeScript | Code exists | Demo uses inline JS, not bundle |
| Finger-curl arming | Code exists | Demo doesn't use state machine |
| Multi-cursor rendering | Code exists | Demo only renders 1 cursor |
| Pipeline orchestration | Code exists | Demo uses direct Human.js |

### 🔴 GAPS

| Gap | Impact | Fix |
|:----|:-------|:----|
| Demo uses inline code | TypeScript ports not tested | Wire `index-bundled.html` |
| Single cursor only | Can't verify multi-hand UX | Add second cursor element |
| No state machine | Can't verify arming logic | Wire Shaper to demo |
| No JSONL output | Can't replay/compare | Add Port 6 Assimilator |

---

## Replay & Standardization Status

### Current State
- **Input:** Golden video file (MP4)
- **Output:** Console logs only (not standardized)
- **Replay:** Not implemented (no JSONL recording)

### Required for DID AI Assistance

| Requirement | Status | Notes |
|:------------|:-------|:------|
| Standardized Input Format | ⚠️ Partial | Video works, JSONL replay not wired |
| Standardized Output Format | 🔴 Missing | Need CloudEvent JSONL output |
| Deterministic Replay | 🔴 Missing | Need Port 6 Assimilator |
| Golden Master Comparison | 🔴 Missing | Need diff tool |

### Reward Hack Prevention

| Check | Status | Notes |
|:------|:-------|:------|
| Input validation | ⚠️ Partial | Video file checked, no schema validation |
| Output validation | 🔴 Missing | No Immunizer checks |
| Determinism test | 🔴 Missing | Can't verify same input → same output |
| Golden master diff | 🔴 Missing | No regression detection |

---

## Recommendations

### Immediate (Today)
1. **Wire `index-bundled.html`** to use real TypeScript pipeline
2. **Add second cursor element** for multi-hand visualization
3. **Log CanonicalIntent** to console in standardized format

### Short-term (This Week)
1. **Implement Port 6 Assimilator** - JSONL recording
2. **Create golden master JSONL** from this video
3. **Add replay mode** - feed JSONL instead of video

### Long-term (Phase 3)
1. **Determinism test** - same JSONL → same output
2. **Golden master diff** - detect regressions
3. **Immunizer validation** - reject bad data

---

## Raw Evidence

### Sample Hand Detection (Frame 60)
```json
{
  "frame_id": 60,
  "timestamp_ms": 2000,
  "hands_count": 2,
  "hands": [
    { "hand_id": 0, "handedness": "hand", "confidence": 0.88, "landmark_count": 21 },
    { "hand_id": 1, "handedness": "hand", "confidence": 0.85, "landmark_count": 21 }
  ]
}
```

### Processing Performance
- **Average latency:** 20-50ms per frame
- **Peak latency:** 387ms (first frame, model loading)
- **Effective FPS:** 20-50 fps

---

## Confidence Score

| Metric | Score | Notes |
|:-------|:------|:------|
| Human.js Detection | 100% | Physics-verified |
| Multi-Hand Detection | 100% | 29 frames with 2 hands |
| TypeScript Pipeline | 30% | Code exists, not wired to demo |
| Replay/Standardization | 10% | Console logs only |
| Reward Hack Prevention | 5% | No validation infrastructure |

**Overall Truth Score: 49%**

---

*Generated by Playwright Golden Video Test | Gen 77 | 2025-12-18*
