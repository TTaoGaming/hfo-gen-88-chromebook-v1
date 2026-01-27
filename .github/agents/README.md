# HFO Agent Modes (Index)

This folder defines the available GitHub agent modes for the HFO workspace.

## Modes

- **Baseline (MCP grounded):** [hfo-basic-mcp.agent.md](hfo-basic-mcp.agent.md)
- **Port 6 (Assimilation / STORE / AAR):** [hfo-port6-kraken-keeper.agent.md](hfo-port6-kraken-keeper.agent.md)
- **Port 7 (Navigation / Sensemaking / S3 Protocol):** [hfo-port7-spider-sovereign.agent.md](hfo-port7-spider-sovereign.agent.md)
- **HIVE8 doctrine:** [HFO-Hive8.agent.md](HFO-Hive8.agent.md)

## Port 6: Kraken Keeper (automatic, vendor-agnostic)

The Port 6 mode is designed to be fail-closed and auditable.

- **Automatic per-turn ritual:** `scripts/kraken_keeper_turn.py`
  - Always runs `P6` preflight → requires JSON response → runs postflight.
  - Works vendor-agnostically in `--provider manual` mode (paste into any model).
  - Optional `--provider openrouter` mode for API automation.

- **VS Code task:** “Kraken Keeper: Turn (Auto Preflight+Postflight)” (see `.vscode/tasks.json`).

Artifacts:

- `artifacts/kraken_keeper/` (packets, preflight/postflight raw JSON, turn receipts)

Contracts:

- `contracts/hfo_kraken_keeper_turn_receipt.zod.ts` (+ tests under `contracts/__tests__/`)
