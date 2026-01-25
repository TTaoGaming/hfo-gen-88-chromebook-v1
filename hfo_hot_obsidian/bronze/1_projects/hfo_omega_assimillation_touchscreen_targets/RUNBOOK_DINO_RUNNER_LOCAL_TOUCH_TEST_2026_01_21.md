# Medallion: Bronze | Mutation: n/a | HIVE: V

# Dino Runner (t-rex-runner) — Local Touch Test Runbook

Date: 2026-01-21

Repo vendored at:

- `hfo_hot_obsidian/bronze/1_projects/hfo_omega_assimillation_touchscreen_targets/vendor/t-rex-runner`

Upstream:

- <https://github.com/wayou/t-rex-runner>
- Stars (as of 2026-01-21): 2.1k
- License: BSD-3-Clause

Important provenance note:

- The upstream README describes this as **“extracted from chromium”**. For hardened assimilation, treat bundled art/sprites as potentially third-party IP and be prepared to swap assets for clearly-licensed originals if needed.

## Goal

Validate “single action” touch injection (tap-to-jump) and repeated rhythmic input with minimal UI complexity.

## Fast local serve (static)

From the repo root:

- `cd hfo_hot_obsidian/bronze/1_projects/hfo_omega_assimillation_touchscreen_targets/vendor/t-rex-runner`
- `python3 -m http.server 8002`

Then open:

- `http://localhost:8002/`

## Touch/gesture checklist

- Baseline manual:
  - Tap/click/space triggers jump
  - Hold/long-press behavior (if any)
- Injector-driven:
  - Map “commit” → a single tap/click on the canvas/body
  - Verify repeated taps don’t introduce event duplication (double-jump glitches) or focus loss

## Assimilation notes (Gen5 v12+)

- Static, single-page; should mount cleanly as a same-origin iframe adapter.
- If the app expects keyboard, your P3 injector may need a fallback: tap→jump or synthetic key events via postMessage + adapter shim.
