# Medallion: Bronze | Mutation: 0% | HIVE: V

# Gen5 vs Gen4 v40.1 Forensic Diff Report (2026-01-19)

## Scope
- Baseline: Gen4 v40.1 HTML
  - [hfo_hot_obsidian/bronze/1_projects/omega_gen4_current/omega_gen4_v40_1.html](hfo_hot_obsidian/bronze/1_projects/omega_gen4_current/omega_gen4_v40_1.html)
- Target: Gen5 v1 HTML
  - [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v1.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v1.html)

## Summary of Changes
### Added (Gen5 harness features)
1) **Clip replay overlay UI**
   - CSS block for `#hfo-clip-replay` overlay.
   - Overlay player for loading .webm/.mp4 clips.

2) **Clip replay API**
   - `window.hfoClipPlayer.open()/loadFile()/hide()` to load and replay a clip.

3) **Mock results replay (JSONL)**
   - `window.hfoMockPlayer` with `loadFromText/start/stop/nextResults`.
   - Predict loop prioritizes `hfoMockPlayer` results before webcam input.

4) **Mock replay start helper**
   - `window.hfoStartMockReplay()` to run prediction loop without camera.

## Behavior Delta (Risk Assessment)
- **Core gesture/FSM logic unchanged**: No modifications to Port 1 fusion, FSM thresholds, or pointer injection paths.
- **Input source override added**: Gen5 can inject mock results, which *changes runtime input source* when enabled.
- **Impact**: When mock replay is active, live camera is bypassed. This is expected for automated testing but is a functional change in input selection order.

## Evidence (Diff Excerpts)
- Clip replay overlay + player: see Gen5 v1 additions around CSS and new `window.hfoClipPlayer` block.
- Mock results replay + mock start: see Gen5 v1 additions around `window.hfoMockPlayer` and `window.hfoStartMockReplay`.

## Related Harness Files Added
- JSONL generator: [scripts/gen5_clip_to_mock_jsonl.py](scripts/gen5_clip_to_mock_jsonl.py)
- FSM test: [scripts/omega_gen5_video_fsm.spec.ts](scripts/omega_gen5_video_fsm.spec.ts)
- Pipeline docs: [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/VIDEO_PIPELINE.md](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/VIDEO_PIPELINE.md)

## Closeness to Gen4 v40.1
- **Functional parity:** High, except when mock replay is enabled.
- **Operational delta:** Gen5 adds testing entrypoints and optional mock input path.
- **Recommendation:** Keep mock replay disabled by default for manual UX testing; use it only for automated runs.
