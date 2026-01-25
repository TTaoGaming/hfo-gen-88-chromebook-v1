<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

# Gen6 Architecture Guardrail + v18 Knuckle Keybar (COMMIT-only)

Date: 2026-01-22

## 1) What version is currently “active”?

**Evidence:** the stable Omega launcher points to **Gen5**, not Gen6.

- Config SSOT: [active_hfo_omega_entrypoint.json](../../../../../../active_hfo_omega_entrypoint.json)
  - `active.gen = "gen5"`
  - `active.baseline.path = "/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html"`
- Secondary/legacy pointer: [active_omega.json](../../../../../../active_omega.json)
  - `active.gen = "gen5"`
  - baseline `omega_gen5_v11.html`
- Launcher fallback behavior: [active_hfo_omega_entrypoint.html](../../../../../../active_hfo_omega_entrypoint.html)
  - `DEFAULT_TARGET_PATH = '/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v11.html'`

**Conclusion:** your “active” Omega surface is **Gen5 (v12 via JSON; v11 fallback)**. So editing Gen6 v16 “because it’s active” is indeed a code smell.

## 2) Architecture violation (why this matters)

If we patch older Gen6 pages (e.g., v16) while the system’s launcher is Gen5, we risk:

- **Stealth coupling**: “active behavior” appears changed but the launcher does not actually serve that version.
- **False confidence**: tests or manual runs might target a Gen6 URL while production points elsewhere.
- **Medallion flow break**: mixing experimental mutations into “baseline” pages without an explicit v18 artifact makes provenance ambiguous.

### Guardrail

- Treat Gen6 v16/v17 as **immutable baselines** unless explicitly cloned into a new evolution artifact.
- All new behavior should land in a **new Gen6 v18 entrypoint file** and be **deny-by-default behind flags**.

## 3) v18 target: “Knuckle Keybar in COMMIT”

### Doctrine

- **Knuckle keybar sensing may run at P2**, but **effects (key injection) must be COMMIT-only**.
- COMMIT-only must be enforced at the **effect boundary** (P3 injector) using **DataFabric cursor state**, not just “raw” sensor signals.

### v18 Minimum Surfaces (TDD: existing RED specs)

These are already expressed by the v18 RED tests:

- [scripts/omega_gen6_v18_p2_knuckle_keybar_thread_presence_red.spec.ts](../../../../../../scripts/omega_gen6_v18_p2_knuckle_keybar_thread_presence_red.spec.ts)
  - When `flag-p2-knuckle-keybar=true`, runtime must expose `window.hfoP2KnuckleKeybarThread.tick({now,dt,dataFabric})`.
- [scripts/omega_gen6_v18_p3_knuckle_key_inject_emits_space_red.spec.ts](../../../../../../scripts/omega_gen6_v18_p3_knuckle_key_inject_emits_space_red.spec.ts)
  - When `flag-p3-knuckle-key-injector=true`, emitting `p2/knuckle_keypress` with `phase:'begin'` in **COMMIT** must produce `p3/knuckle_key_inject` that targets Dino (`Space`).

## 4) Implementation plan (safe, architecture-aligned)

### 4.1 Create a Gen6 v18 artifact (don’t edit v16)

- Add: `hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v18.html`
- Source: clone from the latest known-good Gen6 v17.x page (e.g., `omega_gen6_v17_4.html`) and then add v18 modules.

### 4.2 Flags (deny-by-default)

Add new OpenFeature keys with default `false`:

- `p2-knuckle-keybar`
- `p3-knuckle-key-injector`
- (optional) `ui-knuckle-keybar-overlay`

### 4.3 P2: KnuckleKeybarThread (sensing + Port2 emit)

Expose `window.hfoP2KnuckleKeybarThread` with:

- `tick({ now, dt, dataFabric })`
- It inspects `dataFabric.cursors[]` and (when enabled) emits `p2/knuckle_keypress` begin/end.

**Important:** this thread must NOT change readiness or FSM; it only emits sensor events.

### 4.4 P3: KnuckleKey injector (COMMIT-only effect boundary)

When enabled:

- Subscribe to `hfoPortsEffects` events.
- On `p2/knuckle_keypress` with `phase:'begin'`:
  - Find matching cursor in `systemState.dataFabric.cursors` (by `pointerId`/`handIndex`).
  - **Hard gate:** only proceed if `cursor.fsmState === 'COMMIT'`.
  - Emit `p3/knuckle_key_inject` with payload mapping to Dino `Space`.

Fail-closed behavior:

- If cursor not found / not COMMIT: do nothing (or emit a `p3/knuckle_key_suppressed` telemetry event).

## 5) Revert policy

Given the launcher is Gen5, Gen6 pages should be treated as versioned artifacts.

- Any previous edits to Gen6 v16 should be reverted (you already undid `omega_gen6_v16.html`).
- v18 work should be additive: new `omega_gen6_v18.html` only.

## 6) “Ready for v18” acceptance criteria

- v18 page exists and boots under the local server.
- Both v18 RED specs flip GREEN against v18:
  - thread presence test
  - COMMIT-only injector test

## 7) Next concrete actions

1) Create `omega_gen6_v18.html` (clone v17.x)
2) Add flag plumbing + P2 thread + P3 injector
3) Update v18 specs to target v18 URL (not v16) and run:
   - `npx playwright test scripts/omega_gen6_v18_p2_knuckle_keybar_thread_presence_red.spec.ts`
   - `npx playwright test scripts/omega_gen6_v18_p3_knuckle_key_inject_emits_space_red.spec.ts`
