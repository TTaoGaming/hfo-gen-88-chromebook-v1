# Requirements Document: Human.js MCP Server & Kiro Power

## Introduction

This spec defines an MCP server that wraps Human.js v3.3.6 capabilities and packages them as a Kiro Power. The goal is to expose Human.js's built-in hand tracking, gesture recognition, and face/body detection through the MCP protocol.

**Key Insight**: Human.js already provides finger curl, finger direction, and gesture recognition. This MCP server exposes these capabilities - it does NOT reinvent them.

**Relationship to HFO**: This power integrates with the HFO Hexagonal architecture as a specialized Observer (Port 0) for human sensing.

**Reference**: See `docs/human-js-api-reference-2025-12-17.md` for complete Human.js API documentation.

---

## Glossary

- **Human.js**: AI-powered library for face, body, hand, and gesture detection
- **MCP**: Model Context Protocol - standard for AI tool integration
- **Kiro Power**: Packaged MCP server with documentation and steering files
- **CanonicalHandState**: HFO's normalized hand tracking data format
- **HandResult**: Human.js's hand detection output (21 keypoints + landmarks)
- **FingerCurl**: Human.js built-in: "none" | "half" | "full"
- **FingerDirection**: Human.js built-in: 8 directions (verticalUp, horizontalLeft, etc.)
- **HandGesture**: Human.js built-in: victory, thumbs up, finger forward/up patterns

---

## Human.js Built-in Capabilities (DO NOT REINVENT)

| Feature | Human.js Provides | Notes |
|---------|-------------------|-------|
| Hand Detection | ✅ 21 keypoints | Box + landmarks |
| Finger Curl | ✅ none/half/full | Per finger |
| Finger Direction | ✅ 8 directions | Per finger |
| Hand Gestures | ✅ victory, thumbs up, etc. | Built-in |
| Frame Interpolation | ✅ `human.next()` | Smoothing |
| Multi-hand | ✅ maxDetected config | Up to N hands |
| Left/Right Label | ✅ HandResult.label | Automatic |
| Confidence Scores | ✅ Multiple scores | box, finger, overall |
| Face Detection | ✅ 468 mesh points | Age, gender, emotion |
| Body Pose | ✅ Multiple models | MoveNet, BlazePose |

---

## Requirements

### Requirement 1: MCP Server Core

**User Story:** As a developer, I want Human.js exposed as MCP tools, so that I can use hand/face/body detection from any MCP-compatible AI assistant.

#### Acceptance Criteria

1. WHEN the MCP server starts THEN the system SHALL initialize Human.js with configurable backend (webgl, wasm, cpu)
2. WHEN listing tools THEN the server SHALL expose detection, hand, gesture, face, and body tool categories
3. WHEN a tool is called THEN the server SHALL return results as JSON in the MCP response format
4. WHEN Human.js throws an error THEN the server SHALL return an MCP error response with details
5. WHEN the server is configured THEN the system SHALL support environment variables for model paths and backend

### Requirement 2: Detection Tools

**User Story:** As a developer, I want to run Human.js detection on images, so that I can analyze frames for hands, faces, and bodies.

#### Acceptance Criteria

1. WHEN `human_detect` is called with base64 image THEN the system SHALL return full Result object
2. WHEN `human_detect` is called with config override THEN the system SHALL merge with default config
3. WHEN detection completes THEN the system SHALL cache the result for subsequent queries
4. WHEN `human_warmup` is called THEN the system SHALL preload models for faster first detection

### Requirement 3: Hand Tracking Tools

**User Story:** As a developer, I want to query hand tracking data, so that I can build gesture-controlled applications.

#### Acceptance Criteria

1. WHEN `human_get_hands` is called THEN the system SHALL return array of HandResult from last detection
2. WHEN `human_get_hand` is called with handId THEN the system SHALL return specific hand or null
3. WHEN `human_get_finger` is called THEN the system SHALL return curl, direction, and keypoints for that finger
4. WHEN `human_get_keypoints` is called THEN the system SHALL return all 21 keypoints for specified hand
5. WHEN Human.js provides landmarks THEN the system SHALL pass through curl/direction without recomputation

### Requirement 4: Gesture Tools

**User Story:** As a developer, I want to query gesture recognition results, so that I can respond to user gestures.

#### Acceptance Criteria

1. WHEN `human_get_gestures` is called THEN the system SHALL return all GestureResult from last detection
2. WHEN `human_get_hand_gestures` is called THEN the system SHALL filter to hand gestures only
3. WHEN `human_check_gesture` is called with gesture name THEN the system SHALL return detected boolean and hand id

### Requirement 5: Smoothing Tools

**User Story:** As a developer, I want frame interpolation for smooth results, so that the cursor doesn't jitter.

#### Acceptance Criteria

1. WHEN `human_interpolate` is called THEN the system SHALL return smoothed result via human.next()
2. WHEN `human_configure_smoothing` is called THEN the system SHALL update skipFrames and skipTime config

### Requirement 6: Face Tools

**User Story:** As a developer, I want face detection and matching, so that I can build face-aware applications.

#### Acceptance Criteria

1. WHEN `human_get_faces` is called THEN the system SHALL return array of FaceResult from last detection
2. WHEN `human_match_face` is called THEN the system SHALL compare descriptor against database
3. WHEN `human_compare_faces` is called THEN the system SHALL return similarity score between two descriptors

### Requirement 7: Body Tools

**User Story:** As a developer, I want body pose detection, so that I can track full-body movements.

#### Acceptance Criteria

1. WHEN `human_get_bodies` is called THEN the system SHALL return array of BodyResult from last detection
2. WHEN `human_get_body_keypoints` is called THEN the system SHALL return keypoints for specified body

### Requirement 8: Kiro Power Packaging

**User Story:** As a Kiro user, I want Human.js packaged as a Power, so that I can activate it with `kiroPowers`.

#### Acceptance Criteria

1. WHEN the power is installed THEN the system SHALL have POWER.md with keywords and documentation
2. WHEN the power is installed THEN the system SHALL have mcp.json with server configuration
3. WHEN the power is activated THEN the system SHALL return toolsByServer with all Human.js tools
4. WHEN steering files are requested THEN the system SHALL provide getting-started, hand-tracking, and gesture-recognition guides

### Requirement 9: HFO Integration

**User Story:** As an HFO developer, I want Human.js output to convert to CanonicalHandState, so that it integrates with the hexagonal architecture.

#### Acceptance Criteria

1. WHEN `human_to_canonical` is called THEN the system SHALL convert HandResult to CanonicalHandState
2. WHEN converting THEN the system SHALL preserve all 21 keypoints, curl, direction, and confidence
3. WHEN converting THEN the system SHALL normalize coordinates to [0,1] range
4. WHEN the Ghost Cursor spec needs hand data THEN the Observer port SHALL use this conversion

---

## Tool Signatures

### Detection Tools
```typescript
human_detect: { input: string, config?: object } => Result
human_warmup: {} => { success: boolean }
```

### Hand Tools
```typescript
human_get_hands: {} => HandResult[]
human_get_hand: { handId: number } => HandResult | null
human_get_finger: { handId: number, finger: Finger } => { curl, direction, keypoints }
human_get_keypoints: { handId: number } => Point[]
```

### Gesture Tools
```typescript
human_get_gestures: {} => GestureResult[]
human_get_hand_gestures: {} => { hand: number, gesture: HandGesture }[]
human_check_gesture: { gesture: string } => { detected: boolean, hand?: number }
```

### Smoothing Tools
```typescript
human_interpolate: { result?: Result } => Result
human_configure_smoothing: { skipFrames?: number, skipTime?: number } => { success: boolean }
```

### Face Tools
```typescript
human_get_faces: {} => FaceResult[]
human_match_face: { descriptor: number[], database: number[][] } => { index, similarity }
human_compare_faces: { descriptor1: number[], descriptor2: number[] } => { similarity }
```

### Body Tools
```typescript
human_get_bodies: {} => BodyResult[]
human_get_body_keypoints: { bodyId: number } => BodyKeypoint[]
```

### HFO Integration
```typescript
human_to_canonical: { handId?: number } => CanonicalHandState
```

---

## Power Structure

```
.kiro/powers/human-js/
├── POWER.md                      # Power documentation
├── mcp.json                      # MCP server configuration
├── package.json                  # Dependencies
├── steering/
│   ├── getting-started.md        # Quick start guide
│   ├── hand-tracking.md          # Hand tracking reference
│   └── gesture-recognition.md    # Gesture patterns
└── src/
    └── human_mcp_server.ts       # MCP server implementation
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| @vladmandic/human | ^3.3.6 | Core detection library |
| @modelcontextprotocol/sdk | ^1.x | MCP server SDK |
| typescript | ^5.x | Type safety |

---

*Spec Created: 2025-12-17 | HFO Gen 76 | Human.js MCP Power*
