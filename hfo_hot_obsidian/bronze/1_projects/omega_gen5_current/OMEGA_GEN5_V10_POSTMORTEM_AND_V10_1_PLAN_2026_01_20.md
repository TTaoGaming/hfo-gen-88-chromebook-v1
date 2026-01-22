<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# OMEGA GEN5 v10 Postmortem + v10.1 Modular-Monolith Plan (2026-01-20)

## TL;DR

Gen5 v10 attempted to modularize the Gen5 monolith by introducing import-mapped ES modules for contracts/utilities/Port-1/Port-2, but the migration was **partial**: the same symbols were imported **and** still defined inline in the HTML. That produces a hard revealed failure:

- `Identifier 'ConfigSchema' has already been declared`

Because the script errors during evaluation, downstream runtime objects like `window.hfoEval` never get defined, breaking existing Playwright harnesses.

The recommended move is to **clone v9 into v10.1** as a *modular monolith* and refactor incrementally behind the 8-port (P0–P7) hex architecture, with **single-authority** invariants and per-version smoke gates.

---

## Anchors (Source of Truth)

- Gen5 v9 HTML: [omega_gen5_v9.html](omega_gen5_v9.html)
- Gen5 v10 HTML: [omega_gen5_v10.html](omega_gen5_v10.html)
- Extracted module candidates (used by v10 importmap):
  - Contracts: [lib/js/hfo_contracts.js](lib/js/hfo_contracts.js)
  - Utilities: [lib/js/hfo_utils.js](lib/js/hfo_utils.js)
  - Port 1 Bridger: [lib/js/hfo_p1_bridger.js](lib/js/hfo_p1_bridger.js)
  - Port 2 Physics: [lib/js/hfo_p2_physics.js](lib/js/hfo_p2_physics.js)
  - Port 2 Shape (Babylon): [lib/js/hfo_p2_babylon.js](lib/js/hfo_p2_babylon.js)

---

## What v10 changed (the intended direction)

### 1) Introduced module boundaries via importmap

In v10, the HTML adds importmap aliases for port modules:

- `hfo-contracts` → `./lib/js/hfo_contracts.js`
- `hfo-utils` → `./lib/js/hfo_utils.js`
- `hfo-p1` → `./lib/js/hfo_p1_bridger.js`
- `hfo-p2-physics` → `./lib/js/hfo_p2_physics.js`
- `hfo-p2-babylon` → `./lib/js/hfo_p2_babylon.js`

This is directionally correct for a modular monolith: you keep a single artifact (`omega_gen5_v10.html`) but organize code behind explicit port modules.

### 2) Started extracting Port ownership

The extracted modules clearly map to the port model:

- **P1 (FUSE)**: `P1Bridger` in [lib/js/hfo_p1_bridger.js](lib/js/hfo_p1_bridger.js)
- **P2 (SHAPE / PHYSICS manifold)**:
  - `PlanckPhysicsAdapter` in [lib/js/hfo_p2_physics.js](lib/js/hfo_p2_physics.js)
  - `BabylonJuiceSubstrate` + `HAND_CONNECTIONS` in [lib/js/hfo_p2_babylon.js](lib/js/hfo_p2_babylon.js)
- **Cross-port contracts**: Zod schemas in [lib/js/hfo_contracts.js](lib/js/hfo_contracts.js)
- **Utilities**: filters/physics helpers in [lib/js/hfo_utils.js](lib/js/hfo_utils.js)

This is consistent with hex architecture: ports expose stable interfaces/data; adapters implement tech specifics.

---

## How v10 was broken (the failure mode)

### The root break: “dual authority” for the same symbol

v10 does BOTH of these in the same `type="module"` script:

1) **Imports** `ConfigSchema`, `FusionSchema`, `LandmarkSchema`, `DataFabricSchema` from `hfo-contracts`.
2) **Re-declares** `const FusionSchema = ...`, `const LandmarkSchema = ...`, `const DataFabricSchema = ...` inline in the HTML.

That violates the most important refactor invariant:

> A symbol must have exactly one authority in a build unit.

In JavaScript modules, importing `ConfigSchema` and then later declaring `const ConfigSchema = ...` (or equivalently, declaring `FusionSchema`, etc.) yields a hard parse/runtime error:

- `Identifier 'ConfigSchema' has already been declared`

### Why the break cascades

Once the module throws, the rest of v10 initialization is never executed. Practically that means:

- `window.hfoEval` may not be assigned
- test harness hooks fail
- “it looks like refactor broke everything” even though 80% of code is intact

This is exactly the “agents refactored too much at once” smell: extraction + inline leftovers + scope collision.

---

## Patterns that work (keep these)

### Pattern A — Single-authority invariants (the #1 rule)

For each port-owned concept, pick **one**:

- **Option 1 (modular)**: defined in `lib/js/...` and imported into HTML.
- **Option 2 (inline)**: defined in the HTML and **not** imported.

Never both.

### Pattern B — Modular monolith (not microservices)

Keep one runtime artifact (`omega_gen5_v10_1.html`) but structure the implementation behind modules.

Benefits:

- still easy to open in a browser
- still deterministic for Playwright harness
- code is organized by port boundaries

### Pattern C — Ports are stable, adapters swap

Treat ports as stable contracts + functions:

- P0 emits *observations* (raw results)
- P1 fuses to a **DataFabric** (validated contract)
- P2 takes DataFabric and produces physics/rendering
- P3 injects events (adapter boundary)
- P4–P7 can evolve independently behind the contract

### Pattern D — Tests gate the version you’re editing

The default fast test targets `omega_gen5_v4.html` today, so it can “pass” while v10 is broken.

Preferred: add per-version smoke gates:

- v9 smoke
- v10.1 smoke

and require them before promoting a refactor.

---

## Anti-patterns (avoid these)

### Anti-pattern 1 — Partial extraction with leftover inline definitions

This is what broke v10. Imported symbol + inline redeclare = hard failure.

### Anti-pattern 2 — Refactoring multiple ports in one change

If a change touches P1 + P2 + P3 simultaneously, it becomes impossible to localize breakage.

Rule of thumb:

- one port boundary change per PR/commit
- keep adapters stable while ports move (or vice versa)

### Anti-pattern 3 — “Contracts” duplicated in multiple places

Zod schemas must be SSOT. If contracts exist in both HTML and `hfo_contracts.js`, drift is guaranteed.

### Anti-pattern 4 — Tests that don’t target the active artifact

If the test suite targets v4 while refactoring v10, failures will escape.

---

## v10.1 plan: clone v9 → modular monolith (8-port architecture)

### Goal

Create `omega_gen5_v10_1.html` by cloning v9, then refactor **incrementally** so the monolith remains coherent while becoming modular.

### Step 0 — Clone baseline

- Start from [omega_gen5_v9.html](omega_gen5_v9.html)
- Create `omega_gen5_v10_1.html`

Acceptance criteria:

- boots with `?flag-disable-camera=true`
- preserves `window.hfoEval` for harness
- passes readiness drain smoke

### Step 1 — Extract only contracts (P1 SSOT)

- Move **only** `LandmarkSchema`, `FusionSchema`, `DataFabricSchema` (and a real `ConfigSchema`) into [lib/js/hfo_contracts.js](lib/js/hfo_contracts.js)
- In HTML: import them; delete inline duplicates.

Acceptance criteria:

- zero duplicate identifiers
- data fabric parse still works

### Step 2 — Extract P1 bridger (FUSE)

- Move `P1Bridger` into [lib/js/hfo_p1_bridger.js](lib/js/hfo_p1_bridger.js)
- In HTML: import it; delete inline definition.

Acceptance criteria:

- only one `P1Bridger` symbol exists
- Playwright readiness tests still pass

### Step 3 — Extract P2 physics + P2 shape

- Physics adapters in [lib/js/hfo_p2_physics.js](lib/js/hfo_p2_physics.js)
- Babylon visuals in [lib/js/hfo_p2_babylon.js](lib/js/hfo_p2_babylon.js)

Acceptance criteria:

- no global BABYLON lifecycle regressions
- rendering still matches parity expectations

### Step 4 — Make “ports” explicit in the monolith

Within the modular monolith, enforce an explicit port index:

- **P0 SENSE**: capture/recognize (MediaPipe)
- **P1 FUSE**: contract validation + coordinate fusion + readiness
- **P2 SHAPE**: physics + geometry + rendering substrates
- **P3 DELIVER**: W3C pointer injection + UI adapters
- **P4 DISRUPT**: feedback loops/suppression (optional gating)
- **P5 DEFEND**: integrity checks / fail-closed
- **P6 STORE**: telemetry export + replay ingestion
- **P7 NAVIGATE**: GUI + config shell

Even if a port is “thin”, it should still exist as a named module or named section.

---

## Practical guardrails for AI-assisted refactors

- Always do a **smoke boot** after any extraction (open with camera disabled).
- Never land a commit where the version under edit is not covered by at least one Playwright spec.
- Prefer “copy then refactor” over “mutate the only copy”.
- Ban “dual authority”: if it’s imported, it must not be redefined inline.

---

## Known v10-specific issue list (actionable)

1) Duplicate symbol declarations: contracts + bridger + babylon classes exist both imported and inline.
2) Test suite does not gate v10 by default; fast suite still targets v4.

---

## Recommended next action

Create `omega_gen5_v10_1.html` from v9 and make extraction changes one-port-at-a-time with per-version smoke tests.
