# Medallion: Silver | Mutation: 0% | HIVE: V

# Phoenix protocol (freeze-and-restart) for Gen88

Date: 2026-01-26

This is a **nondestructive** runbook to “freeze everything here” and start fresh, while keeping this workspace as a stable archive.

## Principle

- Treat the current workspace as **Cold Bronze + receipts**.
- Create a new workspace for **Hot Bronze only**.
- Promotion into Silver happens only via frozen batches with receipts.

This separates:
- write-heavy ingestion (where agents can be reckless)
from
- archive/query (which must remain stable and small).

## Phase 0 — Stabilize (already mostly done)

- Keep always-on processes OFF by default (MCP/Playwright/Ollama).
- Use feature flags for intentional enabling.
- Keep VS Code watchers/search excludes for massive data.

Reference: `RESOURCE_LIFECYCLE.md`.

## Phase 1 — Freeze this repo as archive-only

Goal: Stop new churn, keep it browsable.

Operational rules:
- No daemons.
- No appenders.
- No “open giant jsonl/duckdb in the editor”.

Proof snapshots:
- `./scripts/disk_audit_light.sh`
- `./scripts/ledger_audit_light.sh`

These logs become your “pre-freeze proof”.

## Phase 2 — Create receipts (no compression required yet)

For each batch directory you consider frozen:
- Create a small receipt file with:
  - file list
  - total bytes
  - sha256 per file (or per segment)
  - record counts if applicable

(We can implement a receipt generator next, but this doc keeps the protocol safe-first.)

## Phase 3 — Optional compression / dedupe (only after freeze)

Important: this phase is *safe if and only if data is frozen*.

Options (in increasing complexity):

1) Compress frozen segments (recommended)
- Compress jsonl segments only after rotation.
- Keep both the compressed file and a receipt.

2) Hardlink-based dedupe (advanced; still nondestructive but changes inodes)
- Only do this on immutable cold copies.
- Always do a dry-run first.

3) btrfs reflink/dedupe (advanced; may not be available in Crostini)
- Use only if you can prove it works and doesn’t require risky privileges.

## Phase 4 — Start fresh workspace (Hot Bronze only)

Create a new folder/workspace that contains ONLY:
- minimal code
- minimal hot bronze working set

Rules for agents:
- They write into Hot Bronze only.
- When a batch is complete, they “handoff” to this archive repo as a frozen cold bronze drop.
- Promotion to Silver is only from frozen batches with receipts.

## Guardrails to keep agents honest

- Manual preflight before running heavy workflows:
  - disk free threshold
  - memory pressure threshold
  - offender processes check (MCP/Playwright)

We can encode this as a script (`scripts/agent_preflight.sh`) so you can require it operationally.

## What I recommend you do next

1) Run the two audits to capture baseline proof logs.
2) Confirm you want Phoenix to be:
   - “new workspace folder” (recommended), or
   - “new Crostini container” (heavier).
3) Implement receipts + rotation for the biggest ledgers (most leverage, minimal risk).
