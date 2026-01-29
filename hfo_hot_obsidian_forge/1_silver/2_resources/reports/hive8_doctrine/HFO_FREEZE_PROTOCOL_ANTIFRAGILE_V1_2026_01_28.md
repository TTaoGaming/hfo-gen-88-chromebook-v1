<!--
Medallion: Silver | Mutation: 0% | HIVE: V
Provenance: Operator prompt (2026-01-28). Consolidates existing repo freeze + receipt patterns into an antifragile loop.
-->

# HFO Freeze Protocol (Antifragile) — Silver v1 (2026-01-28)

## Why freezing increases antifragility

Freezing is not “stop changing.” Freezing is **controlled crystallization**:

- **You create a replayable, receipted snapshot** at a known boundary.
- **You keep iterating in Hot**, but you can always roll back to a stable artifact.
- **Failures become fuel**: each failure yields a new constraint (gate), and the next freeze captures the repaired invariant.

In HFO terms: freezing is an **anti-drift primitive** that turns churn into hardened checkpoints.

## Scope boundaries (when to freeze)

Freeze on **interfaces and externally-visible behavior**, not on internal experimentation.

Recommended freeze triggers:

- A port interface changes (contracts, pointer schemas, adapter manifests).
- A “golden path” test becomes stable and meaningful.
- A new entrypoint / runtime boot path is validated.
- A mitigation for a real incident is completed (OOM, crash loop, sync fragility).

## What to freeze (the minimal set)

Freeze the smallest set that makes the system replayable:

1) **Entrypoints**
- `active_hfo_omega_entrypoint.html`
- `active_hfo_omega_entrypoint.json`

2) **Pointers / routing**
- `hfo_pointers.json`

3) **Contracts / schemas**
- `contracts/` (especially anything used cross-port)

4) **Operational gates**
- `scripts/hfo_flight.sh` (and any scripts used by gates)
- the specific Playwright tests that define your “golden” invariants

5) **Receipts**
- A `.receipt.json` (sha256 + timestamp + source/target) for each frozen artifact

## Where to freeze (cold, receipted)

Use the cold layer for hardened snapshots.

Existing pattern example:

- `scripts/hfo_freeze_v24.py` copies mission-thread artifacts Hot → Cold and writes `.receipt.json` alongside the frozen target.

Key invariant:

- Frozen artifacts must be **content-addressed by receipt** (sha256) and treated as immutable.

## The antifragile loop: freeze → test → receipt → replay

### Step 0: Preflight (capsule)

Run a preflight to capture a capsule of current state.

- `bash scripts/hfo_flight.sh preflight --scope HFO --note "freeze boundary" --out artifacts/flight/preflight_HFO_freeze.json`

### Step 1: Verify invariants

Run the smallest set of tests that prove the boundary is stable.

- Keep this small and specific (port-level smoke / golden path).

### Step 2: Freeze

Freeze the minimal set of replay-critical files (entrypoints, pointers, contracts, gates).

- Copy Hot → Cold
- Generate `.receipt.json` for each frozen file

### Step 3: Postflight (receipt)

Write a postflight receipt referencing the frozen artifacts.

- `bash scripts/hfo_flight.sh postflight --scope HFO --preflight-receipt-id <id> --summary "freeze snapshot" --sources <paths> --changes <bullets> --out artifacts/flight/postflight_HFO_freeze.json`

### Step 4: Replay check (optional, strong)

Pick one replayable proof:

- Re-run the same tests against the frozen entrypoint.
- Or run a deterministic “golden master” replay if available.

## Governance / safety rules

- **SSOT memory write-path** remains doobidoo sqlite_vec only.
- Shodh is a derived view: treat it as rebuildable cache, not something you “freeze.”
- Do not expand root pollution; freeze artifacts into the appropriate cold hierarchy.

## Practical “do this next”

1) Choose a single boundary to freeze (e.g., Omega entrypoint + pointer contract).
2) Define 2–5 concrete invariants (tests or checks).
3) Freeze + receipt.
4) Record the freeze in SSOT as a `status_update` with links to receipts.
