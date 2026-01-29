# Medallion: Silver | Mutation: 0% | HIVE: V

# TTao Tooling Forensics v1: 2026-01

## Provenance

- Generated (UTC): 2026-01-25T02:42:12.567960Z
- DuckDB: hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
- MCP memory: hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
- Hot blackboard: hfo_hot_obsidian/hot_obsidian_blackboard.jsonl
- Window (DuckDB modified_at): 2026-01-01T00:00:00 .. 2026-02-01T00:00:00 (start inclusive, end exclusive)
- Window (UTC): 2026-01-01T00:00:00Z .. 2026-02-01T00:00:00Z (start inclusive, end exclusive)
- High-signal mode: True

## Summary

- DuckDB path records: total=62528 used=11290
- MCP memory entries in month: 269
- MCP status_update entries in month: 260
- Blackboard entries in month: 6033
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
| playwright | 57 |
| python | 56 |
| unknown | 50 |
| npm | 40 |
| eslint | 1 |

## Work signals (from MCP status_update; heuristic)

### Topics (top)

| topic | n |
|---|---|
| port0_isr_canonical_8_tools_v2026_1_23 | 2 |
| p0_context_facade_v1_green_fix2 | 2 |
| gen6_v23_preset1_flame_blade_core | 2 |
| omega_gen5_v9_vs_v10_diff_and_tests | 1 |
| omega_gen5_v11_1_goldenlayout_apphost_wiring | 1 |
| gen5_v12_multiapp_shared_substrate_spec | 1 |
| gen6_dino_freeze_coverage_gap_add_v17_liveness_spec | 1 |
| gen6_tripwire_contact_only_multi_inject_regression_fix | 1 |
| gen5_v12_to_v13_transition_cast_ready | 1 |
| omega_gen6_current_non_destructive_clone_and_multiapp_readiness_synthesis | 1 |
| gen6_v1_tactical_view_composition_spec | 1 |
| gen6_v9_dino_readiness_replay_gate | 1 |
| gen6_v9_dino_jump_inconsistency_report | 1 |
| gen6_v9_dino_diagnostics_rerun | 1 |
| forensics_ttao_dev_work_monthly_deep_dive_v1_2025_01_to_2026_01 | 1 |
| forensics_ttao_tooling_forensics_v1_2025_01_to_2026_01 | 1 |
| gen6_v9_cv_to_dino_reliability_diagnostics | 1 |
| ttao_exec_summary_monthly_deep_dives_2025_01_to_2026_01 | 1 |
| pointer_wiring_single_artifact | 1 |
| gen6_v9_dino_fail_closed_precommit_gate | 1 |

### Sources referenced (top)

| source | n |
|---|---|
| hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl | 33 |
| package.json | 32 |
| hfo_hub.py | 32 |
| hfo_pointers.json | 16 |
| scripts/omega_gen6_test_guards.ts | 15 |
| hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V10_HEX_MODULAR_MONOLITH_SPEC_2026_01_20.yaml | 12 |
| contracts/hfo_tripwire_events.zod.ts | 11 |
| hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v16.html | 10 |
| hfo_hot_obsidian/hot_obsidian_blackboard.jsonl | 9 |
| hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html | 8 |
| hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v10_1.html | 7 |
| scripts/omega_gen6_v9_dino_diagnostics.spec.ts | 7 |
| scripts/p0_port0_context_facade_baton_red_test.py | 7 |
| hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v23_flaming_sword_demo.html | 7 |
| scripts/omega_gen5_excalidraw_replay.spec.ts | 6 |
| scripts/omega_gen5_excalidraw_ready.spec.ts | 6 |
| active_hfo_omega_entrypoint.json | 6 |
| playwright.config.ts | 6 |
| .vscode/tasks.json | 6 |
| scripts/hfo_playwright_safe_run.py | 6 |
| hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v6.html | 5 |
| hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v7.html | 5 |
| scripts/hfo_gen5_version_smoke.sh | 5 |
| active_hfo_omega_entrypoint.html | 5 |
| .vscode/mcp.json | 5 |

### Status counts

| status | n |
|---|---|
| UNKNOWN | 125 |
| PASS | 70 |
| FAIL | 9 |

### Samples

- npx playwright test scripts/omega_gen6_v23_10_pyreblade_flamberge_core_only_screenshot.spec.ts --project=chromium --workers=1
- npx playwright test scripts/omega_gen6_v23_9_pyreblade_flamberge_core_only_screenshot.spec.ts --project=chromium --workers=1
- npx playwright test scripts/omega_gen6_v23_9_pyreblade_flamberge_screenshot.spec.ts --project=chromium --workers=1
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

## Tripwires (from hot blackboard; TOOL_TRIPWIRE FAIL)

### Fails by tool

| tool | fail_count |
|---|---|
| tavily | 770 |
| openrouter | 770 |
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

- Set tavily credentials/env vars (tripwire FAIL x770).
- Set openrouter credentials/env vars (tripwire FAIL x770).
- Set duckdb credentials/env vars (tripwire FAIL x72).
