# Medallion: Bronze | Mutation: 0% | HIVE: V

# System Snapshot — 2026-01-26

## Summary

- Environment observed: Linux container (Crostini/penguin) running VS Code
- CPU: 8 cores visible
- Memory (container): 6.3 GiB total, 0 swap visible
- Disk: 301G total, 99G free on `/`

## Current risk posture

- Primary crash risk is *RAM spikes with no swap* (large-file reads, indexing, and extension host growth).
- Biggest repo hazard: very large ledger/artifact files exist in workspace and must remain excluded/streamed.

## Snapshot (container)

- Timestamp: 2026-01-26T12:18:07-07:00

### Memory

- Total: 6.3 GiB
- Used: ~2.7 GiB
- Available: ~3.6 GiB
- Swap: 0B

### Top memory processes (high-level)

- VS Code utility process: ~846 MB RSS
- VS Code zygote: ~563 MB RSS
- Pylance: ~461 MB RSS
- TypeScript server(s): capped to `--max-old-space-size=1024`

### Largest workspace files (must stay excluded)

- ~7242 MB: `hfo_hot_obsidian/bronze/4_archive/.../hfo_unified_v88_merged.duckdb`
- ~903 MB: `**/wikipedia_simple.zim` (hot + cold copies)
- ~407 MB: `hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl`
- ~401 MB: `**/wiki_rag/*.parquet` (hot + cold copies)

## Guardrails already applied

- VS Code exclude hygiene and watcher limits: see [.vscode/settings.json](../../../../.vscode/settings.json)
- Large-file guardrails:
  - `files.maxMemoryForLargeFilesMB = 64`
  - `editor.largeFileOptimizations = true`
- Language server pressure reduction:
  - `typescript.disableAutomaticTypeAcquisition = true`
  - `typescript.tsserver.maxTsServerMemory = 1024`
  - `python.analysis.diagnosticMode = openFilesOnly`
  - `python.analysis.indexing = false`

## Next best guard moves

- Disable unused extensions (e.g. KiloCode/RooCode) per-workspace.
- Stop background servers you’re not using (Playwright test server, daemons).
- Move very large archives out of the repo workspace (or keep them excluded) to reduce background churn.
- Continue with progressive rollups: [scripts/p6_bronze_progressive_rollup.py](../../../../scripts/p6_bronze_progressive_rollup.py)
