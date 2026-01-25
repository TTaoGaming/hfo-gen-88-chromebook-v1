# Medallion: Bronze | Mutation: 0% | HIVE: V
# Provenance: MDN Breakout (Gamedev Canvas Workshop)
# Date: 2026-01-21

## Adapter ID
- appId: `breakout-mdn`
- title: `Breakout (MDN Workshop)`
- Local entrypoint: `hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/official_adapters/mdn_breakout_end3r/index.html`

## Upstream (Official Source)
- Project: `end3r/Gamedev-Canvas-workshop`
- URL: https://github.com/end3r/Gamedev-Canvas-workshop
- Pinned commit: `5199692d8acb9770dc5c16b5b18afbadd95fa497`
- License: see `LICENSE` in this folder (vendored from upstream)

## Why this is “official / beloved / tested”
- This repository is the canonical code companion for the MDN “2D Breakout game using pure JavaScript” tutorial.
- It is widely referenced, tutorial-driven, and stable for coordinate/touch/pointer tuning.

## Local integration notes
- Same-origin: required and satisfied (vendored locally).
- Modifications: renamed `lesson10.html` → `index.html` only.

## Verification (planned)
- Playwright: activate `breakout-mdn` via dropdown and assert P3 target router resolves inside the iframe document.
