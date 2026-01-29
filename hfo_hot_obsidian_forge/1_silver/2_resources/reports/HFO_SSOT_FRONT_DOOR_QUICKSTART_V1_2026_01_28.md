# Medallion: Silver | Mutation: 0% | HIVE: V

# HFO SSOT Front Door (Quickstart) — V1 (2026-01-28)

## Goal

Make memory easy for humans and agents by providing a single blessed entryway:

- **SSOT (Doobidoo sqlite_vec)** is the only **write** store.
- **Shodh** is a **derived / on-demand** index fed from SSOT.
- JSONL ledgers are **receipts/telemetry**, not the brain.

## The One Command You Should Use

Use the SSOT facade via the root hub shim:

- `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py ssot <subcommand> ...`

If an agent is confused, tell it:

- "Use `hfo_hub.py ssot` only. Do not write anywhere else."

## Blessed Subcommands

- `hfo_hub.py ssot entryways`
- `hfo_hub.py ssot guard`
- `hfo_hub.py ssot health --json`
- `hfo_hub.py ssot ingest-md --dir <DIR> --tags gen88_v4 ssot --write`
- `hfo_hub.py ssot ingest-text --dir <DIR> --tags gen88_v4 ssot --write`
- `hfo_hub.py ssot export --out artifacts/exports/doobidoo_export.jsonl --limit 0`
- `hfo_hub.py ssot import --in artifacts/exports/doobidoo_export.jsonl --write`
- `hfo_hub.py ssot sync-shodh --dry-run`
- `hfo_hub.py ssot recall-shodh --query "..." --limit 8`

## Guardrails (Why Writes Sometimes Fail)

Write operations intentionally fail-closed if configuration violates SSOT rules.
Run:

- `hfo_hub.py ssot guard`

…and follow the printed "blessed entryways" next steps.

## VS Code Tasks

Use the existing Memory tasks in `.vscode/tasks.json` — they now call the SSOT facade.

## Source

- scripts/hfo_ssot.py
- hfo_hub.py
- scripts/hfo_memory_guardrails.py
- scripts/hfo_memory_healthcheck.py
