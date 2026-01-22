# Medallion: Bronze | Mutation: n/a | HIVE: V

# Hextris — Local Touch Test Runbook

Date: 2026-01-21

Repo vendored at:

- `hfo_hot_obsidian/bronze/1_projects/hfo_omega_assimillation_touchscreen_targets/vendor/hextris`

Upstream:

- <https://github.com/Hextris/hextris>
- Stars (as of 2026-01-21): 2.4k
- License: GPL-3.0

## Goal

Validate tap/drag-style touch handling and rapid input cadence against a simple, canvas-heavy arcade puzzle.

## Fast local serve (static)

From the repo root:

- `cd hfo_hot_obsidian/bronze/1_projects/hfo_omega_assimillation_touchscreen_targets/vendor/hextris`
- `python3 -m http.server 8001`

Then open:

- `http://localhost:8001/`

## Touch/gesture checklist

- Baseline manual:
  - Tap/drag controls (whatever Hextris exposes in your browser)
  - Confirm no focus loss after repeated input
- Injector-driven:
  - Map a minimal gesture set (tap / short drag) to the game’s expected control surface
  - Verify timing: rapid repeated gestures still register correctly

## Assimilation notes (Gen5 v12+)

- Hextris is a static site; good iframe-adapter candidate.
- Licensing caveat: GPL-3.0 may constrain how you redistribute integrated artifacts; keep it vendored for local testing unless/until you decide on compliance strategy.
