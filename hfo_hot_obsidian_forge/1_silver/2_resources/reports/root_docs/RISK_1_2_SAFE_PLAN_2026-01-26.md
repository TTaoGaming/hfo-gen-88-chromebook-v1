# Medallion: Silver | Mutation: 0% | HIVE: V

# Safe plan for Risk #1 and Risk #2 (Gen88)

Date: 2026-01-26

This plan is explicitly **safe and nondestructive**:
- No deletes.
- No moves unless you explicitly choose to do them.
- Default actions are **audit / proof / quarantine-by-exclusion**.

## Definitions (match your architecture)

- **Hot Bronze**: write-heavy, active ingestion/work area (high churn; unsafe to index).
- **Cold Bronze**: frozen snapshots of Hot Bronze batches (immutable; eligible for dedupe + compression + receipts).
- **Hot Silver**: promoted, curated, query-friendly subset (small; indexed; safe).
- **Receipts**: machine-checkable manifests (hashes, counts, provenance) proving what a batch contains.

The operational goal is:

$$\text{Hot Bronze (active)} \to \text{Cold Bronze (frozen)} \to \text{Dedupe + Compress + Receipt} \to \text{Promote to Hot Silver}$$

---

## Risk #1: Disk pressure (and disk-full mounts)

### Why it hurts Gen88
- On a ~6GB RAM Chromebook with no swap, disk pressure amplifies stalls:
  - VS Code indexing + Node spawns + large file churn can create IO storms.
  - Near-full filesystems can degrade btrfs performance.

### Safe actions (no deletes)

1) **Prove current disk state (bounded, low-impact)**
- Run: `./scripts/disk_audit_light.sh`
- Output log goes to `artifacts/forensics/disk_audit_light_<timestamp>.log`.

2) **Keep the IDE from touching cold data** (already mostly in place)
- Confirm workspace settings keep watchers/search out of:
  - `**/hfo_hot_obsidian/bronze/**`
  - `**/hfo_hot_obsidian/4_archive/**`
  - `**/hfo_cold_obsidian/bronze/**`
  - `**/*.jsonl`, `**/*.duckdb`, `**/*.parquet`, `**/*.zim`

3) **Classify “what can be compressed safely”**
Safe to compress (when frozen):
- `.jsonl` ledgers (append-only logs)
- `.ndjson` (if present)
- old screenshots / artifacts
- old batch directories that are no longer being written

Not safe to compress in-place while active:
- active DB files (`*.duckdb`) while the writer is running
- directories currently ingesting/appending

4) **Quarantine strategy (no delete, no move)**
- Freeze by policy:
  - Only Hot Bronze is writable.
  - Everything else becomes read-only by convention.
- Enforcement is operational: keep daemons OFF by default; only enable flags for intentional work.

5) **Optional: Phoenix “fresh container” without losing archives**
If you want a clean start, the safest nondestructive move is:
- Keep this workspace as **archives-only** (Cold Bronze / receipts).
- Start a new clean workspace for Hot Bronze only.
- Promote into this archive workspace via controlled batches.

(Details are in `PHOENIX_PROTOCOL_2026-01-26.md`.)

---

## Risk #2: Huge ledgers / big DB files causing indexing and IO storms

### Why it hurts Gen88
- `*.jsonl` and `*.duckdb` are large, frequently touched, and expensive for:
  - file watchers
  - search indexers
  - language tooling
  - backup/sync tooling

Even if CPU looks fine, IO churn can freeze the session.

### Safe actions (no deletes)

1) **Prove ledger footprint (bounded, low-impact)**
- Run: `./scripts/ledger_audit_light.sh`
- Output log goes to `artifacts/forensics/ledger_audit_light_<timestamp>.log`.

2) **Keep ledgers out of VS Code**
Already in place via `.vscode/settings.json`, but the operational rule is:
- Don’t open giant `.jsonl` / `.duckdb` directly in the editor.

3) **Introduce “rotation” at the file boundary (future apply step)**
Rotation is the single biggest win that’s still nondestructive:
- Keep one small “head” file for active writes.
- Periodically roll to a new segment (e.g., daily or at 64–256MB).
- Freeze old segments to Cold Bronze.

4) **Compression only on frozen segments**
- For jsonl: `zstd -T0 -19` or `gzip -9` (zstd usually better).
- Keep receipts alongside archives so promotion can be proven.

5) **Receipts as the promotion gate**
Every frozen batch should have:
- counts (lines/records)
- hash(s) (sha256)
- time window
- source pointer(s)

Only batches with receipts are eligible to promote to Silver.

---

## What “safe” looks like this week

- Run the two audits and keep the proof logs.
- Do not delete anything.
- Do not attempt deep dedupe tools inside Crostini yet.
- Start enforcing the lifecycle boundaries: Hot Bronze only = active; everything else = cold.
- If you want Phoenix: freeze this repo as archive workspace and start a fresh hot workspace.
