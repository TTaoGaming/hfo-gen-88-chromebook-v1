# Medallion: Bronze | Mutation: 0% | HIVE: V

# Gen5 Clip Harness (Video → MediaPipe → Mock Replay)

## Purpose
- Convert a video clip into MediaPipe JSONL mock results.
- Replay those results in Gen5 v1 to validate FSM sequence and motion.

## Paths
- Clip input (mirrored):
  - hfo_hot_obsidian/silver/1_projects/omega_gen5_current/clips/right-hand-palm-ready-pointer-up-commit-move-right-turn-palm-release.mirrored.mp4
- JSONL output (default):
  - hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/clip_harness/output/clip_mock_results.jsonl

## Commands
1) Generate JSONL from clip:
   - python clip_harness/clip_to_mock_results.py --input <clip> --output <jsonl>

2) Run FSM replay test:
   - HFO_CLIP_JSONL=<jsonl> HFO_BASE_URL=http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_ HFO_ACTIVE_VERSION=v1 npm run test:omega:clip

## Expected FSM
- IDLE → READY → COMMIT → (move right during COMMIT) → IDLE
