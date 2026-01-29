<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
# P6 Day Reconstruction (Markdown Example) — V0.1 (2026-01-25)

## Goal

Ask Port 6 (Kraken Keeper) a date-scoped question like:

- “What did I do on YYYY-MM-DD?”

…but force the answer to be grounded in evidence (git + DuckDB), with auditable outputs.

## Reality Check (Current Wiring)

- OpenRouter provider is **not** wired in this workspace (`OPENROUTER_API_KEY=missing`).
- Kraken Keeper **is wired** to produce a fail-closed, auditable turn with receipts.
- With `--day YYYY-MM-DD`, the turn driver now generates a **day snapshot** artifact and links it via the existing `artifact_linkage` blackboard event.

This means:

- The pipeline can **collect** day-scoped evidence automatically.
- The “advisor answer” can be generated in **manual mode** (paste packet into any model), and still be audited.

## Command (Operator)

```bash
bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/kraken_keeper_turn.py \
  --scope P6 \
  --provider manual \
  --mode chat \
  --day 2025-07-15 \
  --write-memory false \
  --write-exemplar false \
  --prompt "DAY RECON: Tell me what I did on 2025-07-15. Use only evidence in the day snapshot + capsule; if missing, say so."
```

## What You Get (Proof-of-Result Artifacts)

A successful run yields:

- Preflight + postflight receipts (JSON)
- Operator-facing 1-page Markdown reports (Hot/Bronze)
- A packet JSON for the model
- A day snapshot JSON (git + DuckDB evidence)
- A single `artifact_linkage` blackboard event referencing all of the above

## Proof Run (Example: 2025-07-15)

Evidence from this repo run:

- preflight_receipt_id: `30ad9974082a`
- postflight_receipt_id: `52c7fdf75f42`
- day snapshot:
  - `artifacts/kraken_keeper/day_snapshots/P6_20250715_30ad9974082a_day_snapshot.json`

Observed evidence inside the day snapshot:

- `git log` lines: **0** (no commits captured in git for that UTC day)
- DuckDB `mission_journal` events: **0** rows

Interpretation:

- Kraken Keeper **cannot** truthfully tell you “what you did” for that day beyond “no captured activity in these stores,” because the evidence is empty.

## Suggested Answer Shape (Markdown)

### Day Reconstruction: 2025-07-15 (UTC)

**Evidence**

- Git activity: none captured (0 commits)
- DuckDB mission_journal: none captured (0 events)
- Other sources: not queried (calendar/email/OS activity)

**What you likely did (STRICT MODE)**

- Unproven. There is insufficient captured evidence in git or mission_journal for this day.

**Gaps**

- Uncommitted work is invisible to git-based reconstruction.
- Work not journaled into DuckDB is invisible.

**Next steps**

- Add a daily rollup ingest (writes a summary event into DuckDB per day).
- Expand the day snapshot to include file-path histograms (git diff stats) and blackboard filtering by date.

## Source Anchors

- scripts/kraken_keeper_turn.py
- artifacts/kraken_keeper/day_snapshots/P6_20250715_30ad9974082a_day_snapshot.json
- hfo_hot_obsidian/hot_obsidian_blackboard.jsonl
- hfo_gen_88_cb_v2/hfo_unified_v88.duckdb
