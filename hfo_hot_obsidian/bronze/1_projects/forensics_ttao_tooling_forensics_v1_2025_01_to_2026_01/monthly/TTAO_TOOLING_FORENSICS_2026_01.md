# Medallion: Bronze | Mutation: 0% | HIVE: V

# TTao Tooling Forensics v1: 2026-01

## Provenance
- Generated (UTC): 2026-01-22T02:17:56.734506Z
- DuckDB: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
- MCP memory: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
- Hot blackboard: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl
- Window (DuckDB modified_at): 2026-01-01T00:00:00 .. 2026-02-01T00:00:00 (start inclusive, end exclusive)
- Window (UTC): 2026-01-01T00:00:00Z .. 2026-02-01T00:00:00Z (start inclusive, end exclusive)
- High-signal mode: True

## Summary
- DuckDB path records: total=62528 used=11290
- MCP memory entries in month: 86
- Blackboard entries in month: 2268
- Inferred stacks: node, docker, playwright, eslint, typescript, python-code

## Manifests/configs (top)
| signal | n |
|---|---|
| node/package.json | 41 |
| node/tsconfig | 38 |
| node/vite | 37 |
| node/package-lock | 32 |
| node/playwright | 25 |
| node/vitest | 18 |
| docker/compose | 2 |
| ci/github-actions | 2 |

## Extensions (top; post-filter)
| ext | n |
|---|---|
| ts | 3774 |
| md | 1795 |
| json | 1181 |
| html | 1170 |
| py | 768 |
| js | 427 |
| jsonl | 327 |
|  | 310 |
| png | 291 |
| map | 287 |
| webm | 228 |
| yaml | 177 |
| mp3 | 176 |
| gitignore | 72 |
| mjs | 47 |
| txt | 44 |
| sh | 33 |
| ps1 | 22 |
| db | 19 |
| yml | 18 |

## Tests/commands (from MCP memory; heuristic)
### Tool counts
| tool | n |
|---|---|
| unknown | 35 |
| npm | 30 |
| playwright | 18 |
| python | 3 |
| eslint | 1 |

### Status counts
| status | n |
|---|---|
| PASS | 46 |
| UNKNOWN | 36 |
| FAIL | 5 |

### Samples
- Not run (not requested).
- Not run (analysis only).
- npm run test:omega:excalidraw (fail then pass with palm-release JSONL)
- npm run test:omega:excalidraw (mirrored clip)
- Not run (report only).
- Not run (not requested).
- Not run (not requested).
- npm run lint:omega:gen5
- npm run test:omega:fast (failed: server not running)
- npm run test:omega:fast
- Pre-commit fast suite ran during commits
- HFO_BASE_URL=... HFO_CLIP_VERSION=v6 npx playwright test scripts/omega_clip_fsm_replay.spec.ts --project=chromium
- HFO_BASE_URL=... HFO_CLIP_VERSION=v7 npx playwright test scripts/omega_clip_fsm_replay.spec.ts --project=chromium (both failed: last state COMMIT)
- Not run (not requested).
- Not run (diff only).

## Tripwires (from hot blackboard; TOOL_TRIPWIRE FAIL)
### Fails by tool
| tool | fail_count |
|---|---|
| tavily | 347 |
| openrouter | 347 |
| duckdb | 72 |

### Samples
- tavily: TAVILY_API_KEY missing
- openrouter: OPENROUTER_API_KEY missing
- duckdb: DuckDB file missing
- tavily: TAVILY_API_KEY missing
- openrouter: OPENROUTER_API_KEY missing
- duckdb: DuckDB file missing
- tavily: TAVILY_API_KEY missing
- openrouter: OPENROUTER_API_KEY missing
- duckdb: DuckDB file missing
- tavily: TAVILY_API_KEY missing

## Patterns (heuristic)
- High-signal mode enabled (derived artifact substrings filtered).

## Anti-patterns / risks (heuristic)
- Tool tripwires (missing keys/config) occurred this month; see Tripwires section.
- At least one recorded test/tool command indicates FAIL/nonzero exit.

## Suggested friction fixes (actionable)
- Set tavily credentials/env vars (tripwire FAIL x347).
- Set openrouter credentials/env vars (tripwire FAIL x347).
- Set duckdb credentials/env vars (tripwire FAIL x72).
