# Medallion: Bronze | Mutation: n/a | HIVE: V

# Touch Apps: Top 4 Clone/Fork Targets (Trade Study)

Date: 2026-01-21

Context: You already have Excalidraw running as an adapter. This list focuses on projects that are naturally touch-driven (1–2 touch), and are good “first 1,000 apps” seeds for your W3C Pointer Injector + gesture stack.

## Selection Criteria (what matters for the injector)

- **Pointer semantics**: uses DOM/Canvas input paths that map cleanly to Pointer Events.
- **Low gesture set**: mostly tap, drag, swipe; limited reliance on hover/keyboard.
- **Iframe-friendly**: can be hosted same-origin in an iframe (ideal for the Gen5 v12 AppHost model).
- **License**: explicitly open (MIT/Apache/GPL) so cloning/forking is unambiguous.
- **Complexity**: small-to-medium codebase to adapt quickly.

## Top 4 Clone/Fork Recommendations

### 1) cracker0dks/whiteboard (collaborative sketchboard)

- Repo: <https://github.com/cracker0dks/whiteboard>
- License: MIT (repo declares MIT)
- Why it’s a top pick:
  - Designed for **tablet & mobile**, explicitly collaborative.
  - Rich pointer-driven surface (draw, pan, select) that will stress-test your injector’s drag/pressure-ish behavior.
  - Self-hostable Node app (lets you own the whole stack).
- Likely integration shape:
  - Run it as a same-origin app and mount it in an iframe adapter.
  - Map gestures: 1-finger draw/drag, 2-finger pan/zoom (if supported) or map 2-finger to pan.

### 2) Itimoto/Pong (online multiplayer Pong)

- Repo: <https://github.com/Itimoto/Pong>
- License: MIT (repo declares MIT)
- Why it’s a top pick:
  - **Multiplayer + real-time** (WebSocket) with a relatively simple input surface.
  - Explicit mobile controls: “tap left/right side of the screen” for paddle movement.
  - Great for validating low-latency event routing + active-app-only pointer targeting.
- Likely integration shape:
  - Start with local multiplayer mode, then mount the online server version.
  - Map gestures: tap zones, press-and-hold, drag as “continuous move”.

### 3) gabrielecirulli/2048 (touch-swipe puzzle)

- Repo: <https://github.com/gabrielecirulli/2048>
- License: MIT (repo declares MIT)
- Why it’s a top pick:
  - Tiny, classic, battle-tested.
  - Clean swipe handling baseline (and plenty of forks to compare).
  - Perfect for validating swipe recognition + direction locking.
- Likely integration shape:
  - Host as a static app in an iframe.
  - Map gestures: 1-finger swipe (4 directions), optional 2-finger reset/undo.

### 4) vincentriemer/io-808 (touch-first drum machine)

- Repo: <https://github.com/vincentriemer/io-808>
- License: MIT (repo declares MIT)
- Why it’s a top pick:
  - Dense grid UI: many tap targets, sequencing grid interactions.
  - Strong “instrument panel” feel (good for your HERO substrate + overlays idea).
  - Great to validate multi-touch “chording” (two taps close together) without needing true multi-pointer support.
- Likely integration shape:
  - Host as a static build or dev server and mount in iframe.
  - Map gestures: tap pads, tap grid steps, drag knobs/sliders.

## Matrix Trade Study (quick scoring)

Scoring: 1 (weak) → 5 (strong). “Injector Fit” is: how cleanly it maps to Pointer Events + your 1–2 touch gesture set.

| Option | Touch UX (1–2 touch) | Multiplayer | Injector Fit | Build Complexity | License Safety | Notes |
|---|---:|---:|---:|---:|---:|---|
| cracker0dks/whiteboard | 5 | 4 | 5 | 4 | 5 | High-value canvas stress test; rich toolset; self-hostable. |
| Itimoto/Pong | 4 | 5 | 4 | 3 | 5 | Great “multiplayer tap/drag” gate; older deps but straightforward. |
| gabrielecirulli/2048 | 5 | 1 | 5 | 2 | 5 | Best swipe baseline; minimal surface area. |
| vincentriemer/io-808 | 4 | 1 | 4 | 4 | 5 | Lots of UI interactions; good for precision tapping + drag sliders. |

## Recommended First Integration Path (fastest wins)

1. **2048** as the simplest swipe gate (prove your gesture-to-direction mapping).
2. **Pong** next for real-time feel + mobile control scheme.
3. **Whiteboard** next as the “hard mode” pointer/drag stress test.
4. **io-808** as the “dense control panel” precision test.

## “Next 1,000 apps” workflow template (repeatable)

For each candidate app, capture:

- Repo URL + commit pin
- License file link
- Input types required (tap/drag/swipe/2-finger)
- Hosting mode (static / dev server / needs backend)
- Best mounting strategy (same-origin iframe vs embed)
- Minimal adapter fields (appId, entrypoint, pointerAdapter, targetPolicy)
- One Playwright gate: “can open + perform one core gesture + observe UI state change”

## Watchlist (not in top 4)

- tldraw/tldraw: <https://github.com/tldraw/tldraw>
  - Caveat: its license includes production restrictions and license key enforcement; treat as dev-only unless you obtain an appropriate license.

## Local HFO sources to connect this to

- Gen5 v12 multi-app substrate baseline: [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html)
- v12 shared substrate spec: [hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V12_MULTIAPP_SHARED_SUBSTRATE_SPEC_2026_01_20.yaml](hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V12_MULTIAPP_SHARED_SUBSTRATE_SPEC_2026_01_20.yaml)
