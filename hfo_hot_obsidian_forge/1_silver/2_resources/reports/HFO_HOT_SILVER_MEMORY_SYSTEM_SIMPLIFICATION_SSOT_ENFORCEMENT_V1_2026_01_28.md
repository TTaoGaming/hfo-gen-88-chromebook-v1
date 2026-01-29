<!-- Medallion: Silver | Mutation: 0% (not measured) | HIVE: V -->

---

title: "Hot/Silver Report — Make Memory Easy: SSOT + Machine Enforcement"
date: "2026-01-28"
layer: "silver"
mutation_score: "0% (not measured)"
scope: ["memory", "ssot", "doobidoo", "guardrails", "contracts", "operator_ux"]
status: "proposal"

---

# Hot/Silver — Memory System Simplification (SSOT + Enforcement)

## Executive summary

The system is already *close* to “easy mode” in policy, but the *operator surface* is not yet a single obvious entrypoint.

From the latest storage manifest:

- Blessed write path is **doobidoo sqlite_vec SSOT** (`doobidoo_sqlite_vec_ssot`).
- Shodh is explicitly a **derived mirror** (rebuildable).
- Legacy JSONL ledgers and legacy sqlite_vec DBs exist and should be **no-write**.

This report proposes a small set of machine-enforced changes so that:

1) “What’s in my memory?” is always answered by *one command*.
2) Only one substrate is allowed to accept writes (SSOT), enforced by code + CI.
3) Every other store is either derived (rebuildable) or telemetry (append-only) with explicit policy.

## Evidence snapshot (SSOT policy as-is)

Source of truth used for this report: `artifacts/memory_manifest/latest.json`.

Key facts:

- `policy.blessed_write_path = doobidoo_sqlite_vec_ssot`
- SSOT path: `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`
- Deprecated write paths include:
  - `legacy_mcp_memory_jsonl`
  - `doobidoo_sqlite_vec_legacy_db`
  - `blackboard_hot_forge_legacy`

Implication: the SSOT stance is correct; the missing part is **uniform enforcement + a single overview UX**.

## Problem statement (why it feels like a maze)

Even with a blessed SSOT, a system feels spaghetti when:

- There is no single “overview command/report” everyone uses.
- Multiple stores look similar (jsonl, sqlite, duckdb), but aren’t clearly labeled as **SSOT vs derived vs telemetry** in machine-readable form.
- Write pathways are “policy by convention” (names/labels) rather than *gates by code*.

## Design goals (make it easy for agents + humans)

- **Goal A — One-liner overview:** A single command answers:
  - which store is SSOT, its file path, size, last modified, and record count
  - which stores are derived and safe-to-rebuild
  - which stores are deprecated and must not be written
- **Goal B — Fail-closed writes:** Any attempt to write to a non-SSOT store fails with a clear error.
- **Goal C — Machine-readable policy:** The “blessed write path” and store registry is a contract, not a wiki page.
- **Goal D — Rebuildability:** Derived views (Shodh, DuckDB exports) are reproducible from SSOT.

## Proposed architecture tightening (minimal change set)

### 1) Promote the storage manifest into a contract

You already generate `hfo.memory_storage_manifest.v1`.

Proposed tightening:

- Add a Zod contract (or Python schema) for `hfo.memory_storage_manifest.v1` and validate in CI.
- Add a “required fields” set for each store kind:
  - SSOT must specify `authoritative=true`, `engine=sqlite_vec`, `write_policy=blessed_write_path`, and a stable pointer-resolved path.
  - Derived stores must specify `write_policy=derived_rebuildable` and an explicit `derived_from` reference.
  - Deprecated stores must specify `write_policy=deprecated` or `deprecated_no_write`.

Outcome: the policy becomes machine-enforced, not label-enforced.

### 2) Add a single overview command (and make it the default)

Add a new operator command:

- `hfo_hub.py memory:overview --json`

It should:

- Read `artifacts/memory_manifest/latest.json`.
- Resolve SSOT path.
- Query SSOT for record counts (and optionally min/max timestamps if available).
- Print a compact overview (JSON + human-readable).

Then wire a VS Code task:

- `Memory: Overview (SSOT + Derived + Legacy)`

Outcome: “What’s in memory?” becomes one click / one command.

### 3) Enforce write-path gating in code, not docs

Current manifest states deprecated write paths exist.

Proposed enforcement:

- Centralize a single guard function used by all ingest/sync scripts:
  - refuses writes unless target store id == `policy.blessed_write_path`
  - refuses writes if store id is `deprecated*`
- Require all ingest scripts to call the guard.
- Add a CI test that intentionally tries to write to a deprecated store and expects failure.

Outcome: even if a human makes a mistake, the system prevents drift.

### 4) Make pointers the only path authority

The manifest already stores a path to SSOT.

Proposed:

- Store the SSOT DB path in `hfo_pointers.json` (already practiced in other subsystems).
- Manifest generation should prefer pointer-resolved paths and include the pointer key used.

Outcome: file moves don’t break agents; pointers are the stable API.

## Operational UX (what “easy mode” looks like)

### What an agent needs to know (and nothing more)

- “Write memory” → only one operation exists: doobidoo SSOT ingest/store.
- “Search memory” → either query SSOT directly or query Shodh (derived index) knowing it’s rebuildable.
- “Telemetry” → blackboards are append-only and are not the memory SSOT.

### Default operator runbook (3 commands)

1) Overview:
   - `hfo_hub.py memory:overview`
2) Ingest (dry-run first):
   - `scripts/hfo_memory_ingest_text_dir.py --dir <path> --max-files 10 --max-bytes 2000000 (dry-run)`
3) Rebuild derived search index:
   - `Memory: Sync SSOT → Shodh`

## Acceptance criteria (machine-checkable)

- A single command/task produces a JSON summary containing:
  - SSOT store id + path + size + mtime
  - SSOT record count
  - list of derived stores + their paths
  - list of deprecated stores + their paths
- Any script that supports `--write` fails if the target store is not SSOT.
- CI validates `artifacts/memory_manifest/latest.json` against the contract.
- CI includes a “drift check” that fails if more than one store is marked `authoritative=true`.

## Migration plan (no drama)

Phase 0 (today):
- Implement `memory:overview` and its VS Code task.
- Add contract validation for the storage manifest.

Phase 1:
- Audit ingest/sync scripts for guard usage.
- Add a single `memory_guard.py` (or equivalent) used everywhere.

Phase 2:
- Add “SSOT-only write gate” to CI.
- Optionally: auto-generate a short markdown “Memory Overview” report artifact each day.

## Appendix: Grounded store map (from latest manifest)

- SSOT (blessed): `artifacts/mcp_memory_service/gen88_v4/hfo_gen88_v4_ssot_sqlite_vec_2026_01_26.db`
- Legacy sqlite (deprecated): `artifacts/mcp_memory_service/sqlite_vec.db`
- Legacy MCP ledger (deprecated): `hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl`
- Derived Shodh index dir: `artifacts/shodh_memory`
- Derived sync state: `artifacts/shodh_memory/sync_state_doobidoo_gen88_v4.json`
- Telemetry blackboard (forge v4): `hfo_hot_obsidian_forge/0_bronze/2_resources/blackboards/hot_obsidian_blackboard_v4.jsonl`
