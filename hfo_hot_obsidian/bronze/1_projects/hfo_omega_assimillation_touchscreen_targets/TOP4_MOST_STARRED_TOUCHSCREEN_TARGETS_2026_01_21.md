# Medallion: Bronze | Mutation: n/a | HIVE: V

# HFO Omega Assimillation Touchscreen Targets — Top 4 (Most Stars)

Date: 2026-01-21

Goal: shortlist **widely popular** (GitHub stars) open-source targets that are plausible to mount as same-origin web/iframe adapters under Gen5 v12+.

Notes:

- Star counts and licenses are taken from the upstream GitHub repo pages as of 2026-01-21.
- This list is **not** “best touch UX”; it is “most-starred + broadly known”, with caveats called out.

## Top 4 (ranked by stars)

### 1) jgraph/drawio-desktop — 59.1k stars (Apache-2.0)

- Repo: <https://github.com/jgraph/drawio-desktop>
- What it is: Electron desktop distribution wrapping the draw.io editor.
- Touch relevance: draw.io’s core UI is pointer-driven; for Gen5 web/iframe assimilation you’ll likely vendor/build the web app from `jgraph/drawio` (3.3k stars) or use the official Docker image path described in draw.io docs.
- Caveats:
  - Project states it does **not accept PRs** ("Not open-contribution").
  - Desktop wrapper is not the same as a clean web-iframe target.

### 2) mozilla/pdf.js — 52.7k stars (Apache-2.0)

- Repo: <https://github.com/mozilla/pdf.js>
- What it is: PDF viewer in JavaScript (ubiquitous; used in Firefox and via extensions).
- Touch relevance: natural touch gestures (scroll/pan/zoom) are a good stress-test for multi-pointer routing and wheel/pinch emulation.
- Integration sketch:
  - For iframe mounting: use the built viewer (`web/viewer.html`) and feed it PDFs from same-origin.

### 3) gabrielecirulli/2048 — 13.3k stars (MIT)

- Repo: <https://github.com/gabrielecirulli/2048>
- What it is: canonical 2048 web clone.
- Touch relevance: extremely simple input surface (swipe 4 directions) — ideal first deterministic injector gate.
- Local status in this repo:
  - Vendored at: `hfo_hot_obsidian/bronze/1_projects/hfo_omega_assimillation_touchscreen_targets/vendor/2048`

### 4) piskelapp/piskel — 12.2k stars (Apache-2.0)

- Repo: <https://github.com/piskelapp/piskel>
- What it is: web-based pixel art / spriting editor.
- Touch relevance: *weak by default* — the README explicitly says **“There is no support for mobile.”**
- Why it’s still on the list: it’s very popular, and could be a later-stage target once P3 injection covers hover-ish/editor interactions.

## Next candidates (not in top 4)

- mozilla/BrowserQuest — 9.4k stars (MPL-2.0 code + CC-BY-SA content), archived/read-only
  - Repo: <https://github.com/mozilla/BrowserQuest>
  - Worth tracking for multiplayer + real-time input, but archival/licensing complexity makes it less “first-pass” friendly.
- Hextris/hextris — 2.4k stars (GPL-3.0)
  - Repo: <https://github.com/Hextris/hextris>
  - Fun touch game, but GPL may be a non-starter depending on how you plan to ship/redistribute integrated builds.

## Suggested next step

Start with 2048 (already vendored) and add a minimal Gen5 adapter + 1 Playwright gate: “inject swipe right → tile moves right”.
