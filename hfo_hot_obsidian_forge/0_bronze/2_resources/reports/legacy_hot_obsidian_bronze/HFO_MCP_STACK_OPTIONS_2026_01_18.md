# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO MCP Stack Options — 2026-01-18

## Goal

Improve **cognitive persistence** (memory system) while keeping tooling standardized and low‑drift.

---

## Option Matrix (4 paths)

| Option | Stack | Speed | Evidence Quality | Drift Risk | Best For |
|---|---|---:|---:|---:|---|
| A — Minimal Core | filesystem + memory + sequential-thinking + time | ✅ Fast | ✅ Medium | ✅ Low | Pure rollups & memory stabilization |
| B — Evidence Core | A + tavily + brave-search | ⚠️ Medium | ✅ High | ⚠️ Medium | Monthly rollups with external validation |
| C — Evidence + UI | B + playwright | ❌ Slower | ✅ High | ⚠️ Medium | Omega parity + regression tests |
| D — Max Context | C + context7 + omnisearch | ❌ Slowest | ⚠️ Mixed | ❌ Higher | Broad research, non‑rollup work |

---

## Pareto Frontier (recommended)

- **A** for fastest stabilization of memory system.
- **B** for best evidence/effort balance.
- **C** only when Omega UI validation is required.

**D is dominated** for monthly rollups (more noise and setup without proportional gain).

---

## Standardization Guidance

- **Freeze** to Option A or B for Port 6 monthly rollups.
- **Promote** to C only for Omega parity work.
- **Avoid** D during rollups to reduce drift.

---

## Next Step

Pick A/B/C as the active stack for the next 30 days and pin versions in `.vscode/mcp.json`.

*HFO Hot Bronze — Port 6 Kraken Keeper / Stack Options*
