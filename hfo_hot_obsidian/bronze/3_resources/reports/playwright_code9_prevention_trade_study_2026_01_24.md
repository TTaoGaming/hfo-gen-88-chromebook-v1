# Medallion: Bronze | Mutation: 0% | HIVE: V

# Playwright Code 9 Prevention — 4 Options + Trade Study (2026-01-24)

Context: “exit code 9” events correlated with Playwright screenshot runs under a low-RAM VM/container (no swap) and large baseline VS Code RSS.

## Option A — Budget-Enforced Defaults (Auto Low-RAM Mode)

**What**

- Make Playwright automatically choose safe settings on low-memory machines.
- Enforce `workers=1`, disable `fullyParallel`, and disable `trace` when total RAM is below a threshold.

**Automation mechanism**

- Detect RAM from `/proc/meminfo` in `playwright.config.ts` and auto-enable low-RAM mode.
- Hard-fail if a run tries to use more than 1 worker in low-RAM mode.

**Prevents**

- Accidental high concurrency and trace artifacts that inflate memory.

## Option B — Preflight Wrapper + Proof Bundle (Fail-Closed Gate)

**What**

- A wrapper script becomes the only blessed way to run Playwright locally.

**Automation mechanism**

- Wrapper does:
  1) Snapshot “before” (Port 3 IDE tracer) into telemetry JSONL.
  2) Validates `/dev/shm`, free memory, and ensures no stray Playwright/Chromium from prior runs.
  3) Forces low-RAM mode flags (or refuses to run).
  4) Runs Playwright.
  5) Snapshot “after” + on-failure snapshot.

**Prevents**

- “Silent” operator errors; creates durable proof for every failure.

## Option C — Runtime Watchdog (Tripwire + Graceful Abort)

**What**

- A small watchdog monitors RSS and kills/aborts the Playwright run before the kernel/host SIGKILLs random processes.

**Automation mechanism**

- Launch Playwright as a child process.
- Every N seconds:
  - sample process RSS totals for `node`, `chrome`/`chromium`, `code` and overall `MemAvailable`.
  - if thresholds exceed a policy → send SIGTERM to Playwright and write a “tripwire exceeded” proof snapshot.

**Prevents**

- Cascading crashes that also take down VS Code.

## Option D — Isolation / Offload (Dedicated Runner With Swap)

**What**

- Move the screenshot pipeline off the fragile dev VM.

**Automation mechanism**

- Run the snapshot suite on:
  - a dedicated Linux machine / desktop, or
  - a self-hosted CI runner, or
  - a container/VM configured with swap/zram.

**Prevents**

- Local dev environment instability; isolates heavy GPU/ReadPixels + Chromium workloads.

---

## Trade Study Matrix (1–5; higher is better)

Criteria:

- **Stability** = prevents code 9 / SIGKILL
- **Effort** = implementation effort (5 = easiest)
- **Overhead** = ongoing runtime overhead (5 = lowest)
- **Fidelity** = preserves screenshot fidelity/throughput (5 = best)
- **Proof** = quality of diagnostic artifacts (5 = best)

| Option | Stability | Effort | Overhead | Fidelity | Proof | Notes |
|---|---:|---:|---:|---:|---:|---|
| A Budget defaults | 4 | 5 | 5 | 3 | 2 | Best baseline guard; doesn’t capture failure context by itself. |
| B Preflight + proof | 4 | 3 | 4 | 3 | 5 | Turns every run into a reproducible evidence bundle. |
| C Watchdog tripwire | 5 | 2 | 3 | 3 | 5 | Highest stability; may abort runs early to save IDE. |
| D Offload/Isolation | 5 | 2 | 5 | 5 | 4 | Best long-term; requires extra machine/runner plumbing. |

## Recommended adoption path

- **Phase 1 (today): A + B**
  - Stop accidental “wrong settings” runs and always generate proof.

- **Phase 2 (if still unstable): add C**
  - Make crashes impossible by aborting before OOM.

- **Phase 3 (for heavy batch work): D**
  - Screenshot pipeline runs off-machine with swap/zram.
