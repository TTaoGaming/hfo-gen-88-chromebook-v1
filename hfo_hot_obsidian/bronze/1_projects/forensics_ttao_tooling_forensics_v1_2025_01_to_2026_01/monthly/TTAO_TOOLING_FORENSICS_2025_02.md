# Medallion: Bronze | Mutation: 0% | HIVE: V

# TTao Tooling Forensics v1: 2025-02

## Provenance
- Generated (UTC): 2026-01-22T02:17:52.053910Z
- DuckDB: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/hfo_unified_v88_merged.duckdb
- MCP memory: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl
- Hot blackboard: /home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl
- Window (DuckDB modified_at): 2025-02-01T00:00:00 .. 2025-03-01T00:00:00 (start inclusive, end exclusive)
- Window (UTC): 2025-02-01T00:00:00Z .. 2025-03-01T00:00:00Z (start inclusive, end exclusive)
- High-signal mode: True

## Summary
- DuckDB path records: total=3687 used=3687
- MCP memory entries in month: 0
- Blackboard entries in month: 0
- Inferred stacks: node, python-code

## Manifests/configs (top)
| signal | n |
|---|---|
| node/package.json | 1 |

## Extensions (top; post-filter)
| ext | n |
|---|---|
| dat | 2136 |
| js | 623 |
| py | 318 |
|  | 155 |
| txt | 92 |
| json | 67 |
| html | 66 |
| h | 46 |
| css | 31 |
| yaml | 23 |
| cmake | 16 |
| sh | 11 |
| md | 10 |
| typed | 8 |
| template | 8 |
| code-workspace | 7 |
| 14 | 6 |
| yml | 6 |
| png | 5 |
| so | 5 |

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
