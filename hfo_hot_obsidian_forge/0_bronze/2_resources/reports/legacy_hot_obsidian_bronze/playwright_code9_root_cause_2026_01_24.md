# Medallion: Bronze | Mutation: 0% | HIVE: V

# Playwright exit code 9 (SIGKILL) — Root Cause Report (2026-01-24)

## What is known (proof)

### 1) Kernel is under sustained memory pressure

The kernel repeatedly reports:

- `virtio_balloon ... Out of puff! Can't get 1 pages`

This is consistent with a VM/container that cannot satisfy page allocations or reclaim memory. Under this condition, large processes (Chromium/Node/VS Code) are frequently killed by the host or kernel, which commonly surfaces as **exit code 9** (SIGKILL).

Source proof: kernel `dmesg` tail captured during diagnostics (see MCP memory entry for excerpt timestamps).

### 2) Baseline VS Code memory footprint is already huge before tests

Latest IDE tracer proof snapshot (UTC `2026-01-24T18:01:33Z`) shows:

- VS Code NodeService utility: ~1.28GB RSS
- VS Code zygote: ~783MB RSS
- Pylance server: ~412MB RSS

This means Playwright does not start from “empty RAM”; it is competing with an already-large Chromium process tree plus language servers.

Source proof: [.hfo_runtime/ide_tracer_latest_summary.json](../../../../.hfo_runtime/ide_tracer_latest_summary.json)

### 3) Your v23.11 variants spec amplifies load (retries + full-page screenshots)

In [scripts/omega_gen6_v23_11_pyreblade_solid_flamberge_variants_screenshot.spec.ts](../../../../scripts/omega_gen6_v23_11_pyreblade_solid_flamberge_variants_screenshot.spec.ts):

- It loops 4 variants, each doing multiple render ticks + a screenshot.
- It previously used **full-page** screenshot, which is heavier than **canvas-only**.
- It previously had `retries: 1`, which doubles attempts when flakes happen under pressure.

## Root causes (ranked)

### RC1 — Memory pressure + no swap + VM ballooning → SIGKILL (exit code 9)

- Your environment shows ~6.3GiB RAM and **0 swap**.
- `virtio_balloon` spam indicates the VM is being squeezed.
- Chromium under screenshot load is a classic victim → SIGKILL → exit code 9.

This is the primary root cause.

### RC2 — Concurrency defaults can silently multiply Chromium processes

Even if you *intend* to run `--workers=1`, any run without that flag can spawn multiple workers by default, multiplying browser processes.

Mitigation included here: an explicit low-RAM mode guard (`HFO_LOW_RAM=1`) that forces `workers=1` and disables `fullyParallel` and trace capture.

### RC3 — Screenshot pipeline cost (ReadPixels / software GL) increases CPU+RAM spikes

Repeated screenshots (especially full-page) can cause large transient allocations and slow readbacks.

Mitigation included here: switch to **canvas-only** screenshots and reduce viewport.

## Implemented guards (changes made)

1) Lower crash amplification in v23.11 specs:

- v23.11 variants spec: retries disabled; canvas-only screenshots; smaller viewport.
- v23.11 real flamberge core spec: retries disabled.

1) Playwright governance guard:

- `HFO_LOW_RAM=1` forces `workers: 1`, disables `fullyParallel`, and disables trace capture.

## How to run safely (recommended)

- Use low-RAM mode:
  - `HFO_LOW_RAM=1 npx playwright test scripts/omega_gen6_v23_11_pyreblade_solid_flamberge_variants_screenshot.spec.ts --project=chromium --reporter=line`

- When doing heavy snapshot batches: close extra VS Code windows and avoid running other Node/Playwright tasks simultaneously.

## What is missing (next proof to collect)

- Playwright `test-results/` / `playwright-report/` artifacts from the failing runs were not found in the repo at the time of this report.
  - If crashes continue, the next step is to force writing artifacts to a known folder and capture the exact failure text (`Target closed`, `browser has disconnected`, etc.) alongside an IDE tracer snapshot.
