# Gen81 Scope (Keep Kiro Context Small)

This workspace is the **Gen81 active write-zone**.

## Rules

- Only write under `active/kiro_dev_2025/**`.
- Treat `_archive/**` as **read-only** (historical bronze).
- Do not scan or ingest the full archive by default; query it surgically.
- Prefer `data_lake/gold/**` and `.kiro/specs/**` for always-on context.
