# Medallion: Bronze | Mutation: 0% | HIVE: V

# Omega Project: Gen5 Testing & Production Readiness (Current)

## Current Working File

- `omega_gen4_v40_1.html` (Gen4 v40+ base for Gen5 testing harness)
- `omega_gen5_v1.html` (Gen5 v1 clone with clip replay harness)
- `omega_gen5_v2.html` (Gen5 v2 clone; mirror-aware handedness)

## Gen5 Focus (Testing Harness + Replay)

- Golden master replay via telemetry JSONL
- Clip recording for manual ChromeOS webcam validation
- Clip replay overlay (load .webm/.mp4 to compare)
- Production readiness checks (stability, pointer injection, parity)

## Gen5 Spec + Build Gate

- [GEN5_SPEC.yaml](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_SPEC.yaml)
- [GEN5_BUILD_GATE.yaml](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_BUILD_GATE.yaml)

## Pipeline Docs

- [VIDEO_PIPELINE.md](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/VIDEO_PIPELINE.md)

## Alias Map (Single Project)

- **Canonical**: Omega Gen5 Testing Harness
- **Aliases**:
  - `omega_gen4_*` versions
  - `active_omega.html` (symlink target reference)
  - "Phoenix Core" / "Omega Gen4" / "Omega Workspace" (historical naming)

## Continuity Note

Alpha (MCP Gateway Hub) and Omega (Gen4 pointer stack) are the same long-running mission across 2025–present, evolving under different names.
