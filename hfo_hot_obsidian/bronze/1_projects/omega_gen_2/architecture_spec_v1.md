---
# Medallion: Bronze | Mutation: 0% | HIVE: I
# Provenance: Omega Gen 2 Architecture Spec v1.0
---

# 🌀 Thread Omega Gen 2: Virtual Tool Substrate Specification

This document provides a machine-parsable YAML representation of the handwritten architecture notes for the Phoenix Project's virtual tool substrate (MediaPipe to W3C Physics Pointer).

```yaml
mission: Thread Omega
generation: 2
status: Bootstrap
medallion_layer: Bronze

pipeline_stack:
  p0_sense:
    - stage: MediaPipe Landmarks
      data: 21_points
      tracking: [confidence, status_track_lost]
    - stage: MediaPipe Gesture
      data: gesture_recognition
      trigger: hand_pointer_up
      confidence: high_threshold
  p1_fuse:
    - stage: One Euro Preprocessing
      behavior: [smooth, snap]
  p2_shape:
    - stage: Physics Core (Mass-Spring-Dampener)
      parameters: [coordinate_gap, lock_status]
    - stage: Physics Predictive Kinetic Lookahead
      intent: reduce_latency_jitter
  p3_deliver:
    - stage: FSM Orchestration
      logic: leaky_bucket_anti_midas
    - stage: W3C Pointer Dispatch
      intent: browser_event_injection
  visualization_layer:
    - stage: Excalidraw Integration
      shell: [Golden Layout, Lit GUI]
      transparency: tunable_opacity
    - stage: Elemental Juice Animations
      source: wrist_to_tip_fire
    - stage: Projection Mapping
      intent: multi_hand_hot_seat

fsm_configuration:
  states: [IDLE, READY, COMMIT]
  leaky_bucket:
    description: Anti-Midas Palm Orientation Dwell
    fill_rate: tunable
    drain_rate: tunable
    hysteresis:
      enter: high
      exit: low
    timing:
      state_stickiness_enter: fast
      state_stickiness_exit: slower
    behavior_modes:
      initial_acquire: longer_fresh_bucket
      reacquire: fast_partially_filled_bucket
  transitions:
    idle_to_ready:
      trigger: palm_orientation_dwell
      visual: wireframe_to_fill_animation
    ready_to_commit:
      trigger: high_confidence_gesture
      visual: active_anim_ghost_pointer_to_phase_shift
    commit_to_idle:
      trigger: drain_release
      visual: drain_animation
  fault_tolerance:
    tracking_loss:
      confidence_hysteresis: active
      behaviors: [Coast, Snaplock]

governance:
  multi_user:
    assignment: Hot Seat
    primacy: 1st_to_commit_lockout_priority
  coordinate_space:
    parity: 1_to_1_iframe_mirror
```

## 📜 Metadata
- **Last Updated:** 2026-01-13
- **Source:** Handwritten Notes (Thread Omega Gen 2)
- **Status:** Pending Clarification
