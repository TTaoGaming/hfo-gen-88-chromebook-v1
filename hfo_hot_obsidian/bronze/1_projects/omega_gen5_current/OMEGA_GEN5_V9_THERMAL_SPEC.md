# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Gen 5 v9: Thermal Throttling Design Spec

**Status**: Initial Draft | **Timestamp**: 2026-01-20 | **HIVE**: V

## 📋 Overview: Thermal Throttling Mode (Opt-In)

The **Thermal Throttling Mode** is a defensive performance layer designed for heavy compute scenarios (extended sessions, high ambient temperature, or limited hardware). To ensure mission continuity without unpredictable performance drops, this mode provides a structured degradation path.

**Invariance Rule**: This mode is **OFF by default** and must be explicitly enabled via the settings UI or `hfo_config.json`.

---

## 🌡️ Mechanism 1: Rendering Optimization ("Visual Fidelity Preservation")

The goal of this mechanism is to reduce GPU/CPU load while maintaining a "nice" and professional visual aesthetic. It avoids the "blocky" look of low-resolution scaling by optimizing the rendering pipeline itself.

### 🛠️ Optimization Levers:
- **Adaptive Frame Pacing**: Locks the UI refresh rate to a stable 30FPS or 45FPS instead of fluctuating towards 60FPS.
- **Layer Pruning**: Automatically disables non-essential visual flair:
    - Drop shadows on landing elements.
    - Backdrop blurs (frosted glass effects).
    - High-frequency particle or transition animations.
- **Vector Path Simplification**: Reduces the complexity of SVG/Canvas path drawing for Port 2 (SHAPE) interactions.

---

## 📽️ Mechanism 2: Resolution Input Downscaling

The most significant power savings come from reducing the workload on **Port 0 (SENSE)** landmark extraction. By downscaling the raw video input, we reduce the total pixels processed by the MediaPipe/TensorFlow models.

### 📉 Downscaling Path:
- **Standard (Default)**: HD (1280x720) or Full HD (1920x1080).
- **Throttled Tier 1**: 480p (854x480). Optimized for balance between gesture precision and thermal output.
- **Throttled Tier 2**: 360p (640x360). "Deep Throttle" mode for critical thermal events or low-battery scenarios.

---

## ⚙️ Configuration & Implementation

### Flag Matrix

| Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `thermal_throttle_enabled` | Boolean | `false` | Master opt-in toggle. |
| `thermal_render_mode` | String | `"standard"` | `standard` \| `optimized` |
| `thermal_input_res` | String | `"auto"` | `hd` \| `480p` \| `360p` |

### Signal Architecture (Stigmergy)
When `thermal_throttle_enabled` is true, Port 7 (NAVIGATE) broadcasts the state to all ports via the `hot_obsidian_blackboard.jsonl`:
```json
{"timestamp": "2026-01-20T...", "agent": "P7_NAVIGATE", "signal": "THERMAL_THROTTLE_LOCK", "state": "ACTIVE", "tier": "480p_OPTIMIZED"}
```

---

## 🏁 Next Steps for Swarm
1. **P0 Update**: Implement resolution-switching logic in the Mediapipe wrapper.
2. **P3/P5 Audit**: Ensure that pointer precision scales correctly with lower input resolutions to avoid "coordinate drift."
3. **UI Integration**: Add a "Thermal Saver" toggle to the Omega Gen 5 settings panel.

---
*Created by GitHub Copilot | HFO Omega Protocol*
