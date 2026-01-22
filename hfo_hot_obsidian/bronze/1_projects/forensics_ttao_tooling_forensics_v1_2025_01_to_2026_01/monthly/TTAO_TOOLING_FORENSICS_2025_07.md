# Medallion: Bronze | Mutation: 0% | HIVE: V

# TTao Tooling Forensics v1: 2025-07

## Provenance
- Generated (UTC): 2026-01-22T02:17:52.842625Z
- DuckDB: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
- MCP memory: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
- Hot blackboard: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl
- Window (DuckDB modified_at): 2025-07-01T00:00:00 .. 2025-08-01T00:00:00 (start inclusive, end exclusive)
- Window (UTC): 2025-07-01T00:00:00Z .. 2025-08-01T00:00:00Z (start inclusive, end exclusive)
- High-signal mode: True

## Summary
- DuckDB path records: total=6495 used=6495
- MCP memory entries in month: 0
- Blackboard entries in month: 0
- Inferred stacks: node, python, eslint, python-code

## Manifests/configs (top)
| signal | n |
|---|---|
| python/requirements | 1 |
| build/make | 1 |
| node/eslint | 1 |
| node/package.json | 1 |

## Extensions (top; post-filter)
| ext | n |
|---|---|
|  | 5473 |
| h | 246 |
| py | 169 |
| json | 114 |
| wav | 69 |
| cfg | 30 |
| yaml | 27 |
| md | 23 |
| 6 | 22 |
| 5 | 22 |
| a | 22 |
| so | 20 |
| txt | 17 |
| js | 12 |
| sh | 11 |
| 0 | 10 |
| html | 10 |
| typed | 8 |
| pc | 7 |
| template | 7 |

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
- Node project touched without a lockfile change; consider ensuring lockfile is committed to stabilize installs.
