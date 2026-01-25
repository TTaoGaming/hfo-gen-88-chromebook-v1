# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Pareto Frontier — Next Actions for Mission Threads (Alpha / Omega)

**Date:** 2026-01-22

## Ground Truth: current state (evidence)

- Preflight currently fails at the healthcheck step (`p5:preflight` runs `hfo:health:strict`): see [package.json](../../../../../package.json).
- Healthcheck defines FAIL conditions including `pending_signatures` and reports WARN on missing env keys: [scripts/hfo_healthcheck.py](../../../../../scripts/hfo_healthcheck.py).
- Observed preflight output earlier in this session indicates:
  - missing env: `TAVILY_API_KEY`, `OPENROUTER_API_KEY`
  - FAIL reasons: `pending_signatures` (plus earlier `jsonl_parse_errors` in output)
- Pointer hot-swap seam exists already: [hfo_pointers.json](../../../../../hfo_pointers.json) + [hfo_pointers.py](../../../../../hfo_pointers.py) feeding [hfo_hub.py](../../../../../hfo_hub.py) and [hfo_mcp_gateway_hub.py](../../../../../hfo_mcp_gateway_hub.py).

## The Pareto goal

Maximize “system survivability per unit effort” (Alpha), and “product correctness per unit effort” (Omega), while keeping fail‑closed posture.

Below are **4 frontier options**: each is a coherent 0.5–2 day push with a clear payoff and measurable success criteria.

---

## Option 1 — Alpha: Make the Root Pointer *Verifiable* (Port‑1 owned)

**Theme:** fix brittleness at the top seam.

- **Impact:** High
- **Effort:** Medium (0.5–1.5 days)
- **Risk:** Low (localized changes)

**What you do:** implement a Port‑1 pointer verification gate that makes the existing single-pointer seam cryptographically meaningful.

**Why now:** today the seam exists, but it is not verified (so it’s “easy to change”, not “tamper-evident”).

**Concrete deliverables:**

1) A pointer verification script/module that:
   - schema-validates [hfo_pointers.json](../../../../../hfo_pointers.json)
   - hashes critical targets and paths
   - emits a pass/fail receipt entry
2) A GitOps policy anchor (minimum viable): signed commits/tags on the branch where pointer changes land.
3) Integration into preflight (fail-closed) after healthcheck is made actionable (see Option 2).

**Success criteria:**

- A deliberate pointer tamper causes a deterministic FAIL before mission execution.
- A legitimate pointer update becomes “one file edit + one green gate”.

**Best next command after implementation:**

- `python3 scripts/p5_preflight_audit.py` (or add a new Alpha preflight script)

---

## Option 2 — Alpha: Make P5 Preflight *Actionable* (reduce false FAILs)

**Theme:** your gate is currently noisy; reduce “gate fatigue”.

- **Impact:** Very High (unblocks daily work)
- **Effort:** Low (2–6 hours)
- **Risk:** Medium (risk of weakening fail-closed if done carelessly)

**What you do:** keep fail-closed intent, but split “hard fail” vs “warn” so offline/degraded deps don’t prevent all progress.

**Why now:** `p5:preflight` currently fails because healthcheck flags:

- missing env vars (WARN): `TAVILY_API_KEY`, `OPENROUTER_API_KEY`
- `pending_signatures` (FAIL): blackboard entries with `signature == "pending"` as defined in [scripts/hfo_healthcheck.py](../../../../../scripts/hfo_healthcheck.py)

**Two Pareto sub-variants (pick one):**

A) **Two-lane gate:**
- “Mission run” lane (hard): requires no pending signatures.
- “Dev offline” lane (soft): warns but does not block on pending signatures.

B) **Auto-repair lane:**
- Add a deterministic repair step that resolves `pending_signatures` before the healthcheck runs.
- Candidate tools already exist in repo (example): [scripts/fix_blackboard_signatures.py](../../../../../scripts/fix_blackboard_signatures.py).

**Success criteria:**

- `npm run -s p5:preflight` reliably passes in the intended lane.
- Healthcheck output becomes a short checklist, not a wall of red.

---

## Option 3 — Omega: Stop the Bleed — Make Playwright Determinism the Default

**Theme:** if tests are flaky, velocity collapses.

- **Impact:** Medium-High
- **Effort:** Low-Medium (0.5–1 day)
- **Risk:** Low

**What you do:** pick the currently failing/unstable spec and make it “boringly green”.

**Primary candidate:**

- [scripts/omega_gen6_v17_3_tripwire_lookahead_knob_lead_time_monotonic.spec.ts](../../../../../scripts/omega_gen6_v17_3_tripwire_lookahead_knob_lead_time_monotonic.spec.ts)

**Payoff:** once determinism is strong, you can safely refactor P2/P3 timing logic without regressions.

**Concrete deliverables:**

- Make monotonic assertions robust to minor timing drift (or explicitly assert on deterministic `now`/`ts` payload semantics only).
- Add a “single source of truth” for expected lead-time in fixtures (not derived from runtime wall time).
- Promote the test to run under a consistent task target (one command).

**Success criteria:**

- The spec passes 10 consecutive runs with `--workers=1`.

---

## Option 4 — Alpha↔Omega: Silverize the Shared Data Fabric Boundary (Contracts + Replay)

**Theme:** the interface is the product.

- **Impact:** High (long-term compounding)
- **Effort:** Medium-High (1–2 days)
- **Risk:** Medium (touches shared schemas)

**What you do:** choose 1–2 contracts that are truly “shared data fabric” and lock them down with contract tests + replay validation.

**Candidates already in place:**

- Data fabric schema: [contracts/hfo_data_fabric.zod.ts](../../../../../contracts/hfo_data_fabric.zod.ts)
- Replay manifest: [contracts/hfo_replay_manifest.zod.ts](../../../../../contracts/hfo_replay_manifest.zod.ts)
- Pointer command transport: [contracts/hfo_pointer_command.zod.ts](../../../../../contracts/hfo_pointer_command.zod.ts)
- Adapter manifest: [contracts/hfo_adapter_manifest.zod.ts](../../../../../contracts/hfo_adapter_manifest.zod.ts)

**Concrete deliverables:**

- Add a small battery of contract tests that parse real JSONL fixtures (already used in Playwright) through Zod in Node.
- Add one “fail-closed drift” test: reject unknown fields where required, accept only known versions.

**Success criteria:**

- Any accidental schema drift breaks fast (before runtime).
- You can replay old fixtures without hand-editing (backward compatibility is explicit, not accidental).

---

## Recommendation: what to do *right now*

If the objective is maximum forward motion with minimal regret:

1) **Option 2** (make preflight actionable) — unlocks everything else.
2) **Option 1** (verifiable root pointer) — fixes the Alpha brittleness you called out.
3) Choose **Option 3** *or* **Option 4** based on the next 48h focus:
   - shipping UX correctness → Option 3
   - hardening shared interface → Option 4

---

## Notes (why this is Pareto)

- Option 2 has the best impact/effort ratio because it turns the whole system back into a usable machine.
- Option 1 is the highest-leverage Alpha integrity upgrade because it secures the top-level “what is active?” seam.
- Options 3–4 are the compounding Omega upgrades: deterministic tests and stable contracts.
