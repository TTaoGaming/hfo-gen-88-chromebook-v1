# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Hot Bronze Forensic (Behavioral) — Shodh Failure Episode
Date (UTC): 2026-01-29T004234Z

Scope
- This is a behavioral analysis only: observed actions, observable failure modes, and risk patterns.
- This report does not attribute motives or intent.
- Evidence sources are limited to repo state and proof artifacts on disk.

## Evidence anchors (what exists on disk)
- Shodh server operator script: scripts/shodh_memory_server.sh
- Shodh SSOT sync implementation: scripts/shodh_sync_from_doobidoo_ssot.py
- Shodh recall CLI: scripts/hfo_shodh_recall.py
- Shodh sync proof logs:
  - artifacts/proofs/shodh_sync_20260128T225731Z.txt
  - artifacts/proofs/shodh_sync_dry_20260128T225944Z.txt
  - artifacts/proofs/shodh_sync_write_20260128T230000Z.txt
- Working MCP memory ledger tail (read-only context): hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl

## Behavioral timeline (observable)
1) High-rate environment mutation while debugging a distributed pipeline
- Repeatedly toggled/rewired Shodh runtime assumptions between “docker mode” and “native mode” and relied on scripts that can exit successfully even when the runtime is not actually healthy.
- Resulting behavior: “success” was inferred from process start attempts rather than confirmed via a stable /health probe and a full write+recall loop.

2) Conflation of three separate states into one “working/not working” conclusion
- Server-process state (did something start?)
- Service-health state (does /health respond quickly and consistently?)
- End-to-end state (can SSOT→Shodh sync write, then Shodh recall return results?)
- The observed failure mode is that the end-to-end state was treated as equivalent to “server started”, which creates false positives.

3) Insufficiently bounded retries that amplified instability
- Sync and recall attempts were repeated without stabilizing prerequisites (service liveness + correct API keys + stable port reachability).
- Evidence of instability:
  - artifacts/proofs/shodh_sync_20260128T225731Z.txt shows a /health probe failing with ReadTimeout and a message that Shodh is not reachable.
  - artifacts/proofs/shodh_sync_write_20260128T230000Z.txt shows per-record upsert failures due to HTTP read timeouts.
- Behavioral effect: repeated retries under a timeout condition produce more partial writes, more confusion, and more churn.

4) Drift into “configuration edits as a first-line debug action”
- When a pipeline is failing, configuration edits (e.g., creating/altering .env values) were treated as a default lever rather than a last-mile correction after a confirmed diagnosis.
- This increases the chance of making the configuration state harder to reason about than the underlying service fault.

5) Mixed persistence channels during a “SSOT-only” phase
- There was attempted use of a legacy JSONL ledger for status logging despite an explicit SSOT-only directive and filesystem enforcement that makes those writes fail.
- Behavioral impact: attempting writes to a known-blocked sink is a reliability smell; it creates noise and undermines operator trust because it demonstrates the system boundaries are not being treated as hard constraints.

## Failure modes created or worsened by the behavior
- False-positive “Shodh is working” signals (process start ≠ service healthy ≠ e2e sync/recall).
- Partial sync attempts with timeouts, which can produce ambiguous state (“some ids may be upserted, but the run fails”).
- Configuration-state opacity: more variables change than necessary to isolate the true failing component.

## Concrete technical “break points” (observed)
- Shodh reachability is the immediate break point.
  - artifacts/proofs/shodh_sync_20260128T225731Z.txt: /health ReadTimeout at 127.0.0.1:3030.
- Shodh write path timeouts are the next break point.
  - artifacts/proofs/shodh_sync_write_20260128T230000Z.txt: repeated HTTP read timeout during /api/upsert attempts.
- Shodh recall requires SHODH_API_KEY to be set.
  - scripts/hfo_shodh_recall.py exits immediately if SHODH_API_KEY is missing.

## Behavioral corrective constraints (what should have happened)
These are behavioral constraints, not technical excuses.
- Single-pass gating: do not run SSOT→Shodh sync until /health succeeds N times in a row with short timeouts.
- Single command-path: always invoke the same operator pathway (one script/task) to start Shodh, and require it to prove health before returning success.
- Bounded retries: when timeouts occur, stop and capture one proof artifact (stderr/stdout) before altering configuration.
- SSOT-only discipline: do not attempt to write to legacy JSONL stores when SSOT-only is in effect; persist state via SSOT-native receipts only.
- Separate diagnosis from remediation: identify whether the fault is (a) process startup, (b) health endpoint reachability, (c) API key/auth, (d) request payload size/timeout, before making any edits.

## Operational definition of PASS vs FAIL (end-to-end)
PASS requires all three:
1) Server health: curl http://127.0.0.1:3030/health returns quickly and consistently.
2) Sync write: SSOT→Shodh upsert completes without timeouts.
3) Recall: scripts/hfo_shodh_recall.py returns hits for a known SSOT-ingested string.

Based on the proof artifacts listed above, the observed episode is FAIL at least on (1) and (2).

## Immediate next step (behavioral, not technical)
- Freeze configuration.
- Capture one clean run:
  - Start Shodh.
  - Probe /health 10x.
  - Run a small sync (limit=10).
  - Run one recall query.
- Only then decide whether the defect is “pipeline broken” or “service unreachable/unstable”.
