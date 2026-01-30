# Design Document: Human.js MCP Server & Kiro Power

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Kiro Power: human-js                      │
├─────────────────────────────────────────────────────────────┤
│  POWER.md │ mcp.json │ steering/*.md │ src/server.ts        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   MCP Server (TypeScript)                    │
├─────────────────────────────────────────────────────────────┤
│  Tool Handlers:                                              │
│  - human_detect      - human_get_hands    - human_get_faces │
│  - human_warmup      - human_get_finger   - human_get_bodies│
│  - human_interpolate - human_get_gestures - human_to_canonical│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Human.js v3.3.6                            │
├─────────────────────────────────────────────────────────────┤
│  - Face: 468 mesh points, age, gender, emotion              │
│  - Body: MoveNet, BlazePose, EfficientPose                  │
│  - Hand: 21 keypoints, curl, direction, gestures            │
│  - Gesture: Built-in recognition (victory, thumbs up, etc.) │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Models

### Human.js Types (Pass-Through)

```typescript
// These are Human.js types - we pass them through, not reinvent
interface HandResult {
  id: number;
  score: number;
  boxScore: number;
  fingerScore: number;
  box: [number, number, number, number];
  boxRaw: [number, number, number, number];
  label: "left" | "right";
  keypoints: Point[];
  annotations: Record<Finger, Point[]>;
  landmarks: Record<Finger, { curl: FingerCurl; direction: FingerDirection }>;
}

type Finger = "thumb" | "index" | "middle" | "ring" | "pinky";
type FingerCurl = "none" | "half" | "full";
type FingerDirection =
  | "verticalUp" | "verticalDown"
  | "horizontalLeft" | "horizontalRight"
  | "diagonalUpRight" | "diagonalUpLeft"
  | "diagonalDownRight" | "diagonalDownLeft";

type HandGesture =
  | "thumb forward" | "thumb up"
  | "index forward" | "index up"
  | "middle forward" | "middle up"
  | "ring forward" | "ring up"
  | "pinky forward" | "pinky up"
  | "victory" | "thumbs up";
```

### HFO Integration Types

```typescript
// CanonicalHandState for HFO hexagonal integration
interface CanonicalHandState {
  timestamp: number;
  handId: number;
  label: "left" | "right";
  confidence: number;

  // Normalized coordinates [0,1]
  keypoints: Array<{
    name: string;
    x: number;
    y: number;
    z?: number;
  }>;

  // Human.js built-in analysis (pass-through)
  fingers: Record<Finger, {
    curl: FingerCurl;
    direction: FingerDirection;
  }>;

  // Human.js built-in gestures (pass-through)
  gestures: HandGesture[];

  // Raw box for play area calculations
  boundingBox: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
}
```

---

## MCP Server Implementation

### Server Structure

```typescript
// src/human_mcp_server.ts
import { Human, Config, Result } from '@vladmandic/human';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

class HumanMcpServer {
  private human: Human;
  private lastResult: Result | null = null;

  constructor(config?: Partial<Config>) {
    this.human = new Human({
      backend: 'webgl',
      modelBasePath: 'https://cdn.jsdelivr.net/npm/@vladmandic/human/models/',
      hand: { enabled: true, maxDetected: 2, landmarks: true },
      gesture: { enabled: true },
      face: { enabled: true },
      body: { enabled: true },
      ...config
    });
  }

  async detect(input: string, config?: Partial<Config>): Promise<Result> {
    // input is base64 image data
    const result = await this.human.detect(input, config);
    this.lastResult = result;
    return result;
  }

  getHands(): HandResult[] {
    return this.lastResult?.hand ?? [];
  }

  // ... other methods
}
```

### Tool Registration

```typescript
const TOOLS = [
  // Detection
  {
    name: 'human_detect',
    description: 'Run Human.js detection on an image',
    inputSchema: {
      type: 'object',
      properties: {
        input: { type: 'string', description: 'Base64 encoded image' },
        config: { type: 'object', description: 'Optional config override' }
      },
      required: ['input']
    }
  },
  {
    name: 'human_warmup',
    description: 'Preload Human.js models for faster detection',
    inputSchema: { type: 'object', properties: {} }
  },

  // Hand tracking
  {
    name: 'human_get_hands',
    description: 'Get all detected hands from last detection',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'human_get_finger',
    description: 'Get finger curl, direction, and keypoints',
    inputSchema: {
      type: 'object',
      properties: {
        handId: { type: 'number', description: 'Hand ID' },
        finger: { type: 'string', enum: ['thumb', 'index', 'middle', 'ring', 'pinky'] }
      },
      required: ['handId', 'finger']
    }
  },

  // Gestures
  {
    name: 'human_get_gestures',
    description: 'Get all gestures from last detection',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'human_check_gesture',
    description: 'Check if a specific gesture is detected',
    inputSchema: {
      type: 'object',
      properties: {
        gesture: { type: 'string', description: 'Gesture name to check' }
      },
      required: ['gesture']
    }
  },

  // Smoothing
  {
    name: 'human_interpolate',
    description: 'Get smoothed/interpolated result via human.next()',
    inputSchema: { type: 'object', properties: {} }
  },

  // HFO Integration
  {
    name: 'human_to_canonical',
    description: 'Convert HandResult to CanonicalHandState for HFO',
    inputSchema: {
      type: 'object',
      properties: {
        handId: { type: 'number', description: 'Optional hand ID (default: first hand)' }
      }
    }
  }
];
```

---

## Kiro Power Structure

### POWER.md

```markdown
---
name: "human-js"
displayName: "Human.js Detection"
description: "AI-powered human detection: face, body, hand, gesture recognition via Human.js v3.3.6"
keywords:
  - human
  - face
  - body
  - hand
  - gesture
  - pose
  - tracking
  - detection
  - recognition
  - finger
  - curl
  - direction
author: "HFO Gen 76"
---

# Human.js Kiro Power

AI-powered human detection for face, body, hand, and gesture recognition.

## Quick Start

1. Activate: `kiroPowers(action="activate", powerName="human-js")`
2. Detect: `human_detect({ input: base64Image })`
3. Get hands: `human_get_hands()`
4. Get gestures: `human_get_gestures()`

## Built-in Capabilities (DO NOT REINVENT)

Human.js already provides:
- Finger curl detection (none/half/full)
- Finger direction (8 directions)
- Hand gestures (victory, thumbs up, etc.)
- Frame interpolation
- Multi-hand tracking
- Left/right hand labeling

## Available Tools

### Detection
- `human_detect` - Run full detection on image
- `human_warmup` - Preload models

### Hand Tracking
- `human_get_hands` - Get all detected hands
- `human_get_finger` - Get finger curl/direction
- `human_get_keypoints` - Get 21 hand keypoints

### Gestures
- `human_get_gestures` - Get all gestures
- `human_check_gesture` - Check for specific gesture

### Smoothing
- `human_interpolate` - Get smoothed result

### HFO Integration
- `human_to_canonical` - Convert to CanonicalHandState
```

### mcp.json

```json
{
  "mcpServers": {
    "human-js": {
      "command": "node",
      "args": ["src/human_mcp_server.js"],
      "env": {
        "HUMAN_BACKEND": "webgl",
        "HUMAN_MODEL_PATH": "https://cdn.jsdelivr.net/npm/@vladmandic/human/models/"
      },
      "disabled": false,
      "autoApprove": [
        "human_get_hands",
        "human_get_finger",
        "human_get_gestures",
        "human_check_gesture",
        "human_interpolate",
        "human_to_canonical"
      ]
    }
  }
}
```

---

## HFO Port Integration

### Port Mapping

| Human.js Feature | HFO Port | Role | Notes |
|------------------|----------|------|-------|
| Detection | Port 0 | Observer | Primary sensing |
| Interpolation | Port 2 | Shaper | Smoothing (alongside 1Euro) |
| Gesture Events | Port 3 | Injector | Trigger game actions |
| Validation | Port 5 | Immunizer | Confidence checks |
| Recording | Port 6 | Assimilator | JSONL replay |

### Data Flow

```
Camera Frame
    │
    ▼
┌─────────────────────────────────────┐
│ human_detect (Port 0: Observer)     │
│ - Returns full Result               │
│ - Caches for subsequent queries     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ human_to_canonical (Port 0→1)       │
│ - Converts HandResult to            │
│   CanonicalHandState                │
│ - Normalizes coordinates            │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Bridger (Port 1)                    │
│ - Wraps in CloudEvents envelope     │
│ - Adds trace context                │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Shaper (Port 2)                     │
│ - 1Euro filter (velocity-adaptive)  │
│ - Kalman prediction                 │
│ - human_interpolate (frame smooth)  │
│ - State machine (armed/disarmed)    │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ CanonicalIntent (Ghost Cursor)      │
│ - Position, velocity, confidence    │
│ - Armed state for gesture gating    │
└─────────────────────────────────────┘
```

---

## Steering Files

### getting-started.md
- Installation steps
- Basic detection example
- Configuration options

### hand-tracking.md
- 21 keypoint reference
- Finger curl/direction usage
- Multi-hand handling

### gesture-recognition.md
- Built-in gesture list
- Custom gesture patterns
- Integration with game actions

---

## Implementation Notes

### Browser vs Node.js

Human.js works in both environments but with different backends:
- Browser: webgl (GPU), wasm (CPU fallback)
- Node.js: tfjs-node (native), wasm

The MCP server will run in Node.js, so we need tfjs-node or wasm backend.

### Model Loading

Models are loaded on first detection or via `warmup()`. For MCP server:
- Load models on server start (warmup)
- Cache loaded models
- Support custom model paths via env var

### Result Caching

The server caches the last detection result so subsequent queries (get_hands, get_gestures) don't require re-detection. This matches Human.js's `human.result` property pattern.

---

*Design Created: 2025-12-17 | HFO Gen 76 | Human.js MCP Power*
