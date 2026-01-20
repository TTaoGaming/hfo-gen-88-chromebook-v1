# Medallion: Bronze | Mutation: 0% | HIVE: V

# Gen5 Video Pipeline (Clip → MediaPipe → JSONL → Mock Replay)

## Inputs
- Clip: hfo_hot_obsidian/silver/1_projects/omega_gen5_current/clips/*.mirrored.mp4
- Model: hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/lib/models/gesture_recognizer.task

## Convert clip to JSONL
- Script: scripts/gen5_clip_to_mock_jsonl.py
- Output: .jsonl with MediaPipe-like results per frame

## Replay in Gen5 v1
- Open omega_gen5_v1.html
- Console:
  - window.hfoMockPlayer.open()
  - window.hfoMockPlayer.start()

## Expected FSM
- IDLE → READY → COMMIT → MOVE_RIGHT → IDLE

## Notes
- This pipeline is designed for automated Playwright tests and manual verification.
