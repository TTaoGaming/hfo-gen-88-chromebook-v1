# Medallion: Bronze | Mutation: 0% | HIVE: V

# TTao Tooling Forensics v1: 2025-11

## Provenance
- Generated (UTC): 2026-01-22T02:17:55.570261Z
- DuckDB: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
- MCP memory: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
- Hot blackboard: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl
- Window (DuckDB modified_at): 2025-11-01T00:00:00 .. 2025-12-01T00:00:00 (start inclusive, end exclusive)
- Window (UTC): 2025-11-01T00:00:00Z .. 2025-12-01T00:00:00Z (start inclusive, end exclusive)
- High-signal mode: True

## Summary
- DuckDB path records: total=79318 used=78135
- MCP memory entries in month: 0
- Blackboard entries in month: 0
- Inferred stacks: node, python, docker, python-code

## Manifests/configs (top)
| signal | n |
|---|---|
| build/make | 103 |
| ci/github-actions | 49 |
| node/package.json | 38 |
| go/go.mod | 27 |
| go/go.sum | 22 |
| rust/cargo.toml | 11 |
| python/setup.py | 9 |
| docker/dockerfile | 5 |
| python/pyproject | 5 |
| docker/compose | 3 |
| python/requirements | 3 |
| rust/cargo.lock | 1 |
| node/package-lock | 1 |
| build/taskfile | 1 |
| node/webpack | 1 |
| node/yarn.lock | 1 |

## Extensions (top; post-filter)
| ext | n |
|---|---|
| py | 21530 |
| h | 10378 |
| manifest | 8587 |
| txn | 8587 |
| lance | 8582 |
| md | 5591 |
| go | 4590 |
|  | 1667 |
| zip | 1218 |
| pyi | 919 |
| json | 684 |
| so | 455 |
| proto | 431 |
| txt | 337 |
| feature | 196 |
| pc | 195 |
| rs | 171 |
| hpp | 164 |
| pyx | 154 |
| js | 152 |

## Tests/commands (from MCP memory; heuristic)
### Tool counts
(none)

### Status counts
(none)

### Samples
(none)

## Tripwires (from hot blackboard; TOOL_TRIPWIRE FAIL)
### Fails by tool
(none)

### Samples
(none)

## Patterns (heuristic)
- High-signal mode enabled (derived artifact substrings filtered).

## Anti-patterns / risks (heuristic)
(none)

## Suggested friction fixes (actionable)
(none)
