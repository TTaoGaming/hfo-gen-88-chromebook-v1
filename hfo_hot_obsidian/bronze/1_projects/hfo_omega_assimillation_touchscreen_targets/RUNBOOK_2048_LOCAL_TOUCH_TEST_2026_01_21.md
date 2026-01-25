# Medallion: Bronze | Mutation: n/a | HIVE: V

# 2048 — Local Touch Test Runbook

Date: 2026-01-21

Repo vendored at:

- `hfo_hot_obsidian/bronze/1_projects/hfo_omega_assimillation_touchscreen_targets/vendor/2048`

## Goal

Validate your “commit + swipe” gesture injector against a known-good, swipe-driven web app.

Success criteria (minimum):

- Swipe up/down/left/right triggers the matching 2048 move.
- Repeated swipes do not break focus or lose input routing.

## Fast local serve (static)

From the repo root:

- `cd hfo_hot_obsidian/bronze/1_projects/hfo_omega_assimillation_touchscreen_targets/vendor/2048`
- `python3 -m http.server 8000`

Then open:

- `http://localhost:8000/`

(2048 generally won’t behave correctly as `file://` in all browsers; a local server is safer.)

## Touch/gesture checklist

- Baseline manual:
  - Swipe left/right/up/down using real touch (or trackpad gesture emulation).
- Injector-driven:
  - “Commit” gesture recognized (your stack-specific)
  - 4-direction swipe is emitted as pointer/touch and is received by the app
  - Confirm the move triggers and the board updates

## Notes for Gen5 adapter assimilation (later)

- 2048 is a single-page static app; it’s a good candidate to mount as a same-origin iframe adapter.
- If you see input loss inside an iframe, suspect:
  - iframe focus / pointer capture
  - incorrect target routing (P3 ACTIVE_APP_ONLY policy)
  - gesture mapping emitting mouse events instead of pointer/touch
