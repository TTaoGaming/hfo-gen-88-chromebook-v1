<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# Handoff — Omega Gen6 v17.x → v18 (Keybar + P3 Diagnostics)

Timestamp (UTC): 2026-01-23T16:39:50Z

## What’s true right now (grounded)

- Gen6 v17.x entrypoints are present and were validated earlier with Playwright + P3 diagnostic probes.
- Gen6 v18 entrypoint exists and includes:
  - A deny-by-default **P2 Knuckle Keybar Thread** hook (`window.hfoP2KnuckleKeybarThread?.tick?.(...)`).
  - A deny-by-default **P3 Knuckle Key Injector** (`window.hfoP3KnuckleKeyInjector`, gated by `p3-knuckle-key-injector`).
- Playwright can appear “frozen” when the local server at `http://localhost:8889/` is down/unreachable.

## Primary blocker

- If `http://localhost:8889/` is not reachable, `page.goto(...)` waits and tests look hung.

Grounding:

- Server entrypoint script: [scripts/hfo_threaded_server.py](../../../../../../scripts/hfo_threaded_server.py)
- Active Omega pointers (Gen5): [active_hfo_omega_entrypoint.html](../../../../../../active_hfo_omega_entrypoint.html)

## Tests & diagnostics already run (from session context)

- Gen6 v17.* suite:
  - `npx playwright test scripts/omega_gen6_v17_*.spec.ts --project=chromium --workers=1 --reporter=line`
- P3 diagnostic battery probes:
  - `npx playwright test scripts/omega_gen6_v17_4_p3_diagnostic_battery_probe.spec.ts --project=chromium --workers=1`
  - `npx playwright test scripts/omega_gen6_p3_diagnostic_battery_cross_version.spec.ts --project=chromium --workers=1`

Key finding from probes:

- On the LIGHT URL (injector disabled), `keyboard_packet` can fail while `synthetic_canary` still reports PASS; enabling `flag-p3-injector=true` makes `keyboard_packet` and `trace_span_chain` succeed.

Relevant files:

- v18 entrypoint: [hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v18.html](omega_gen6_v18.html)
- Test guard helpers: [scripts/omega_gen6_test_guards.ts](../../../../../../scripts/omega_gen6_test_guards.ts)
- P3 diagnostic battery library: [hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/lib/js/hfo_p3_diagnostic_battery_v1.js](lib/js/hfo_p3_diagnostic_battery_v1.js)

## What’s been added for handoff (hub memory path)

A hub-level CLI now exists to append a `status_update` line into MCP memory JSONL (pointer-resolved via `hfo_pointers.json -> paths.mcp_memory`).

- Hub file: [hfo_hub.py](../../../../../../hfo_hub.py)
- Pointer SSOT: [hfo_pointers.json](../../../../../../hfo_pointers.json)

Example:

- `python3 hfo_hub.py memory append --topic my_topic --change "did X" --source "some/path.md"`

## Next steps (recommended)

1. Restore server availability. Ensure [scripts/hfo_threaded_server.py](../../../../../../scripts/hfo_threaded_server.py) is running and `curl -m 2 http://localhost:8889/` returns.

1. Add fail-fast Playwright guard (preflight). Add a quick server-up check in [scripts/omega_gen6_test_guards.ts](../../../../../../scripts/omega_gen6_test_guards.ts) so tests error quickly with a clear message when `:8889` is down.

1. v18 stabilization path. Keep v18 knuckle/keybar features deny-by-default; add one v18-specific RED→GREEN spec asserting: visualization loads, crossings emit deterministic metadata, and the COMMIT-only injector emits a P3 effect only when the flag is enabled.
