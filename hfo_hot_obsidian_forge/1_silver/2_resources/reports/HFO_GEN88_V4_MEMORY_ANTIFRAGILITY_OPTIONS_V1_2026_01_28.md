# Medallion: Silver | Mutation: 0% | HIVE: V

# Gen88 v4 Memory System — 4 Antifragility Options (2026-01-28)

## TL;DR Recommendation

If your system is freezing and agents keep “writing to the wrong place”, the highest-leverage move is to **shrink the writable surface area**.

Recommended order:

1) **Option 1 (SSOT-only + Shodh on-demand)** — immediate stabilization, simplest mental model.
2) **Option 2 (Batched ingest/sync + backpressure)** — removes the freeze vectors and makes operations resumable.
3) **Option 3 (Single gateway API + contracts)** — prevents multi-backend drift across the swarm.
4) **Option 4 (Disaster recovery + rebuildability drills)** — makes failure a routine, safe event.

---

## Current State (Repo Evidence)

### What’s already good

- **Single write-path SSOT exists:** Doobidoo `sqlite_vec` SSOT (pointer-resolved).
  - Guide: `hfo_hot_obsidian_forge/1_silver/2_resources/reports/HFO_GEN88_V4_BLESSED_MEMORY_SYSTEM.md`
  - Pointer: `paths.mcp_memory_ssot_sqlite` in `hfo_pointers.json`
- **Fail-closed guardrails exist:** `scripts/hfo_memory_guardrails.py` verifies env flags + SSOT path alignment.
- **Fast health checks exist:** `scripts/hfo_memory_healthcheck.py` checks SSOT + Shodh, and supports `--ssot-only` + `--deep-sqlite`.
- **Stable CLI dispatch exists:** `hfo_hub.py` exposes `health`, `health:ssot`, `health:ssot:deep`, and `memory:guard`.

### What’s brittle

- **Too many “memory-shaped things” look writable** (JSONL ledgers, Shodh MCP adapter, SSOT ingest scripts, blackboards).
- **Derived index (Shodh) can consume CPU in the background** (index commits/GC) and trigger perceived “freezes”, even if SSOT is healthy.
- **Bulk ingest/sync is operationally unsafe** when run without batching/cursors/time limits.

---

## Option 1 — SSOT-Only + Shodh On-Demand (Simplest/Most Stabilizing)

**Goal:** one mental model: **SSOT is the only write path**; derived views are optional and can be stopped anytime.

### What changes

- Treat Shodh as **on-demand** (start only for recall / demos / audits; stop otherwise).
- Keep Shodh **out of the MCP tool surface by default** (avoid multi-server confusion).
- Keep “legacy JSONL MCP memory server” disabled permanently.

### Concrete implementation

1) Enforce default flags via guardrails:
   - `HFO_MCP_ENABLE_MEMORY=0`
   - `HFO_MCP_ENABLE_MCP_MEMORY_SERVICE=1`
   - `HFO_MCP_ENABLE_SHODH_MEMORY=0` (allow only for special runs)
   - Script: `scripts/hfo_memory_guardrails.py`

2) Use SSOT-only checks as your “safe mode”:
   - `hfo_hub.py health:ssot`
   - `hfo_hub.py health:ssot:deep`

3) Stop Shodh when not needed:
   - `scripts/shodh_memory_stop.sh`

### Pros

- Biggest reduction in brittleness per unit effort.
- Stops the “agents are confused” problem at the source (fewer choices).
- Shodh becomes a tool, not a dependency.

### Cons / risks

- Any workflow that expects Shodh via MCP tools must switch to HTTP recall scripts.
- Requires discipline: Shodh stays “derived”, not promoted to SSOT.

### Antifragility win

Failures of Shodh no longer block memory writes or SSOT verification; Shodh outages become routine, safe events.

---

## Option 2 — Make Ingest/Sync Resumable (Batching + Backpressure)

**Goal:** eliminate freeze vectors by making operations bounded and restartable.

### What changes

- Every bulk write operation gets:
  - a **cursor** (resume point)
  - a **time budget** (`--max-seconds`)
  - **batch size limits**
  - **rate limiting/backoff**

### Concrete implementation

1) Refactor ingest scripts (markdown/text dir) to support:
   - `--cursor-file artifacts/...json`
   - `--max-seconds 30`
   - `--max-new-memories 200`
   - `--sleep-ms 25` between writes

2) Refactor Shodh sync to support:
   - `--max-upserts 200`
   - `--max-seconds 30`
   - `--sleep-ms 10`
   - commit cursor **only after confirmed upserts**

3) Add “safe default” VS Code tasks:
   - “Ingest (Write, Safe Batch)”
   - “Sync SSOT → Shodh (Safe Batch)”

### Pros

- Makes the system operationally safe even under low resources.
- Turns big jobs into small, predictable steps.
- Dramatically reduces the chance of hanging or thrashing.

### Cons / risks

- Requires some engineering work and light state management.

### Antifragility win

A crash/restart becomes normal: you rerun the same command and it continues from cursor; failure becomes a controlled input to the system.

---

## Option 3 — One Gateway API for Memory (Contracts + “No Direct Writes” Policy)

**Goal:** prevent swarm confusion by ensuring every agent uses the same entrypoint and schemas.

### What changes

- Agents never call random scripts directly for “memory”. They call **one gateway**.
- All cross-port memory messages are schema-validated (Zod contracts) and fail-closed.

### Concrete implementation

1) Add a single memory CLI surface in `hfo_hub.py`:
   - `hfo_hub.py memory:store` (SSOT write)
   - `hfo_hub.py memory:recall` (SSOT recall)
   - `hfo_hub.py memory:sync:shodh` (derived)

2) Define a Zod contract for “memory command” payloads:
   - `contracts/hfo_pointer_command.zod.ts` style
   - New: `contracts/hfo_memory_command.zod.ts`

3) Make tools “hard to misuse”:
   - Keep legacy JSONL MCP server disabled.
   - Keep Shodh MCP adapter disabled by default.
   - Require pointer-resolved paths for any storage.

### Pros

- Maximum reduction in “agent did the wrong thing”.
- Extensible: new stores/indexes become backends behind one API.

### Cons / risks

- Moderate engineering work (contracts + integration).
- Requires migrating existing docs/scripts to the gateway surface.

### Antifragility win

The system becomes resistant to operator/agent mistakes: invalid commands fail before writes happen.

---

## Option 4 — Treat Failure as Normal (Backups + Rebuild Drills + Kill-Switches)

**Goal:** operational antifragility: corruption/outages become routine drills, not emergencies.

### What changes

- Scheduled SSOT exports + integrity checks.
- Standard rebuild steps:
  - “Rebuild Shodh from SSOT”
  - “Rebuild derived analytics from SSOT”
- Kill-switches / resource governors for background services.

### Concrete implementation

1) Backup policy:
   - nightly `scripts/hfo_memory_export_doobidoo_ssot.py --out artifacts/exports/...jsonl`
   - periodic `hfo_hub.py health:ssot:deep`

2) Rebuild policy:
   - `scripts/shodh_memory_stop.sh`
   - delete/rotate derived Shodh data dir
   - rerun `scripts/shodh_sync_from_doobidoo_ssot.py` in batches (Option 2)

3) Kill-switches:
   - Add a small “resource governor” that stops Shodh if CPU > X% for Y minutes.
   - Integrate into an existing daemon (e.g., sentinel) if desired.

### Pros

- Most “anti fragile” operational posture: you gain confidence by exercising failure.

### Cons / risks

- Requires some discipline/automation.

### Antifragility win

A broken derived index is no longer scary; you rebuild it routinely. Backups ensure SSOT is portable.

---

## Decision Matrix

| Option | Best for | Effort | Risk | Antifragility impact |
|---|---|---:|---:|---:|
| 1. SSOT-only + Shodh on-demand | immediate stabilization | low | low | high |
| 2. Batched/resumable ops | preventing freezes | medium | low | very high |
| 3. Gateway API + contracts | stopping agent confusion | medium-high | medium | very high |
| 4. Backups + rebuild drills | long-term resilience | medium | low | high |

---

## Next Smallest Step

Pick one:

A) If you want stability now: adopt **Option 1** as default policy and run only SSOT checks during instability.

B) If you want “no more freezes”: implement **Option 2** first (bounded ingest/sync with cursors).

C) If you want “no more wrong writes”: implement **Option 3** (single gateway + contracts) after Option 1.

