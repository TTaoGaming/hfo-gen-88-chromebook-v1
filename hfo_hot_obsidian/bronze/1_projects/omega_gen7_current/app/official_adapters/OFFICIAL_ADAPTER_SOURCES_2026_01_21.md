# Medallion: Bronze | Mutation: 0% | HIVE: V
# Official Adapter Sources (shortlist)
# Date: 2026-01-21

Goal: Only vendor “official / beloved / tested” implementations as same-origin iframe adapters.

## Candidates
- MDN Breakout tutorial (pure JS): https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript
  - Note: MDN states code samples are CC0; still capture provenance + link to upstream GitHub lesson repo.
- Excalidraw: https://github.com/excalidraw/excalidraw
  - Note: already integrated as an adapter; treat as an upstream-pinned vendor in this doc going forward.

## Intake checklist (do this every time)
- Pin upstream ref (tag/commit) and record in a provenance doc (use PROVENANCE_TEMPLATE.md)
- Vendor upstream LICENSE file alongside adapter
- Keep adapter same-origin (copy into repo; no external CDN runtime dependency)
- Add 1 Playwright smoke gate per adapter: activation + target routing resolves inside iframe
