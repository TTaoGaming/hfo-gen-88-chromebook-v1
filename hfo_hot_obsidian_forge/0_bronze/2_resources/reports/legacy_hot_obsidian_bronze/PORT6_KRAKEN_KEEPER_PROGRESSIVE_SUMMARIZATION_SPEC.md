# Medallion: Bronze | Mutation: 0% | HIVE: V

# Port 6 (Kraken Keeper) — Progressive Summarization + Medallion Freeze Schedule

Version (Z): 2026-01-25T00:00:00Z

## Objective

Make HFO memory **antifragile** by turning raw Hot logs into:
- **tamper-evident Cold snapshots** (hash receipts)
- **non-destructive progressive summaries** promoted upward (Hot Silver/Gold/HFO)

Port 6 Kraken Keeper owns this lifecycle:
- bounded hydration (prevent OOM)
- deterministic rollups
- freeze receipts
- schedule governance (powers of 8)

## Single Blessed Entryway (SSOT) + duplicates

### SSOT blessed entryway
- Root shim: [hfo_mcp_gateway_hub.py](hfo_mcp_gateway_hub.py)
  - This is the stable launcher; it forwards to the active implementation via `hfo_pointers.json` / env overrides.
- Root hub shim (general): [hfo_hub.py](hfo_hub.py)
  - Also forwards to the same active gateway implementation.

### Expected duplicate (by design, not a bug)
- Implementation: [hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py](hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py)
  - This is the actual server implementation; the root shim delegates to it.

Rule: operators should invoke the **root shim** entrypoints; do not hardcode the Alpha path in external scripts.

## Data Lake Lanes (Hot vs Cold) and what each lane means

### Hot lanes (mutable, operational)
- Hot Bronze: raw working artifacts (JSONL logs, operator notes, active specs)
- Hot Silver: daily/weekly rollups and curated summaries meant for re-use
- Hot Gold: higher-order summaries built from batches of Silver
- Hot HFO: epoch-level summaries and stable mission engineering notes

### Cold lanes (immutable, tamper-evident)
Cold is **copy + receipt** (append-only). Cold never overwrites; it archives.

- Cold Bronze: frozen snapshots of Hot Bronze artifacts + `.receipt.json` hashes
- Cold Silver: frozen snapshots of Hot Silver rollups + receipts
- Cold Gold: frozen snapshots of Hot Gold summaries + receipts
- Cold HFO: frozen snapshots of Hot HFO epoch summaries + receipts

Existing freeze tool (Hot Bronze → Cold Bronze):
- [hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_alpha/p5_immunize/freeze_to_cold.py](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_alpha/p5_immunize/freeze_to_cold.py)

Existing GitOps restorer (bulk freeze of Hot Bronze files, fail-closed on ambiguity):
- [scripts/hfo_gitops_restore.py](scripts/hfo_gitops_restore.py)

## Progressive summarization schedule (powers of 8)

Use a powers-of-8 cadence (days):
- Bronze cadence: $8^0 = 1$ day
- Silver cadence: $8^1 = 8$ days
- Gold cadence: $8^2 = 64$ days
- HFO cadence: $8^3 = 512$ days

Interpretation:
- Every day: summarize + freeze Bronze
- Every 8 days: summarize Silver from daily rollups, then freeze Silver
- Every 64 days: summarize Gold from Silver bundles, then freeze Gold
- Every 512 days: summarize HFO epoch from Gold bundles, then freeze HFO

## Canonical inputs (today)

### Working memory + stigmergy
- Working memory ledger (large; must be read bounded): [hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl](hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl)
- Hot blackboard (stigmergy): [hfo_hot_obsidian/hot_obsidian_blackboard.jsonl](hfo_hot_obsidian/hot_obsidian_blackboard.jsonl)

### Kraken Keeper turn discipline
- Agent mode contract (authority + fail-closed ritual): [.github/agents/hfo-port6-kraken-keeper.agent.md](.github/agents/hfo-port6-kraken-keeper.agent.md)
- Turn driver (preflight → answer → postflight): [scripts/kraken_keeper_turn.py](scripts/kraken_keeper_turn.py)

### Rollup generator (already exists)
- Daily rollups → Hot Silver path: [scripts/hfo_rollup_generate.py](scripts/hfo_rollup_generate.py)

## Required invariants (non-destructive)

1) **No destructive edits** to primary ledgers
   - `mcp_memory.jsonl` and `hot_obsidian_blackboard.jsonl` are append-only.
2) **Cold is immutable**
   - copy artifact → hash receipt → never overwrite.
3) **Bounded hydration**
   - Port 6 must read tails / bounded windows only.
   - The gateway hub tail reader was updated to avoid reading entire JSONL into RAM.
4) **Every rollup has provenance**
   - timestamp (Z)
   - input pointers
   - receipt ids / sources

## Pipeline: Hot Bronze → Cold Bronze → Hot Silver → Cold Silver → Hot Gold → Cold Gold → Hot HFO → Cold HFO

### Stage A (daily) — Bronze
- A1. Generate daily rollup (Hot Silver)
  - Use [scripts/hfo_rollup_generate.py](scripts/hfo_rollup_generate.py)
  - Output goes under `hfo_hot_obsidian/silver/3_resources/reports/rollups/daily/`
- A2. Freeze Hot Bronze artifacts to Cold Bronze
  - Use `freeze_to_cold.py` (or GitOps restore for batch)
  - Receipt: `.receipt.json` alongside the frozen file

### Stage B (every 8 days) — Silver
- B1. Produce a Silver bundle summary (Hot Gold input later)
  - Input: 8 daily rollups + key receipts
  - Output: curated Hot Silver summary markdowns
- B2. Freeze Silver to Cold Silver
  - Same copy+receipt model as Bronze

### Stage C (every 64 days) — Gold
- C1. Produce Gold summary from Silver bundles
- C2. Freeze Gold to Cold Gold

### Stage D (every 512 days) — HFO
- D1. Produce epoch (HFO) summary from Gold bundles
- D2. Freeze HFO to Cold HFO

## Scheduling (recommended mechanisms)

Because Crostini/systemd availability varies, support multiple schedulers:

1) Cron (inside Linux container)
- Daily: run rollup + freeze
- Every 8/64/512 days: run promotion scripts

2) VS Code tasks
- For manual “operator push-button” execution when cron isn’t reliable.

3) Repo daemons (only if bounded)
- If you add a daemon, it must obey [scripts/hfo_system_budget.py](scripts/hfo_system_budget.py) backoff under low RAM.

## Port 6 governance notes (OOM responsibility)

Kraken Keeper authority includes:
- enforcing bounded hydration tails
- turning “large log growth” into scheduled compactions/archives
- ensuring daily rollups exist so the operator can safely ignore raw ledgers

When OOM risk is detected (low MemAvailable, no swap), Port 6 should:
- reduce tail sizes
- skip expensive scans
- prioritize freeze + rollup proofs

---

## Next implementation step (not in this document)

To fully operationalize this spec, add:
- a Port 6 “progressive summarization runner” script that:
  - computes due windows (1/8/64/512)
  - runs rollup generation
  - freezes the resulting artifacts into Cold lanes
  - emits receipts + `status_update` into `mcp_memory.jsonl`
- optional cron/task definitions
