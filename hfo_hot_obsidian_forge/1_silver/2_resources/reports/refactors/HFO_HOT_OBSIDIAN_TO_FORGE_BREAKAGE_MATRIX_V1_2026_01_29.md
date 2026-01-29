# Medallion: Silver | Mutation: 0% | HIVE: V

# HFO Hot Obsidian → Forge Move: Breakage Matrix (V1)

Date: 2026-01-29 (UTC)

## Scope
This report enumerates what will break (and why) if `hfo_hot_obsidian/` is moved into the canonical Forge layout:

- `hfo_hot_obsidian_forge/{0_bronze,1_silver,2_gold,3_hfo}/{0_projects,1_areas,2_resources,3_archive}/`

Assumption: you are willing to **demote** anything currently in Hot Gold into Hot Silver/Bronze if it reduces operational risk.

## Executive Summary (TL;DR)
If you “just move the folders”, breakage will be immediate in **three load-bearing places**:

1) **Pointer targets** in `hfo_pointers.json` (gateway hub + infra specs + payload root)
2) **Blackboard path defaults** hardcoded across scripts (`hfo_hot_obsidian/hot_obsidian_blackboard.jsonl`)
3) **Static URL/file path references** used by Playwright/TS configs and VS Code tasks

The safest pattern is a **two-phase migration**:

- Phase A (compat mode): move content into Forge, but leave **symlink stubs** (or “compat mirrors”) in legacy locations to preserve old paths.
- Phase B (cutover): update pointers + code to be Forge-native, then retire legacy stubs once nothing depends on them.

## Breakage Matrix

### A. Runtime-critical (will break automation)

#### A1. `hfo_pointers.json` targets (gateway + specs + payload)
**What breaks**
- `mcp_gateway_impl` points into `hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/...`.
- `p3s_payload_root` points into `hfo_hot_obsidian/bronze/3_resources/p3s_payloads`.
- Multiple other pointers target Hot Obsidian file paths.

**Why**
- These are treated as contracts by tooling (hub runners, flight wrappers, etc.). A path move without pointer updates yields immediate file-not-found.

**Evidence**
- `hfo_pointers.json` contains multiple `hfo_hot_obsidian/...` targets.
- `scripts/hfo_gen88_p3s_strangeloop.sh` prints payload root via pointers but defaults to Hot Bronze:
  - `(paths.get('p3s_payload_root') or 'hfo_hot_obsidian/bronze/3_resources/p3s_payloads')`

**Mitigation**
- Preferred: update pointer targets to Forge-native paths *after* the destination exists.
- Safer initial cut: keep legacy paths as symlinks pointing into Forge (so pointers don’t need to change immediately).

**Notes on “demote gold”**
- If you demote Hot Gold resources into Forge Silver/Bronze, you must also update any pointer/docs referencing gold paths.

#### A2. Hot blackboard default path (`hfo_hot_obsidian/hot_obsidian_blackboard.jsonl`)
**What breaks**
- Many scripts and agent docs assume the hot blackboard lives at `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl`.

**Why**
- The value is hardcoded as a default in multiple places (including some absolute paths).

**Evidence (examples)**
- `hfo_blackboard_events.py`: `DEFAULT_BLACKBOARD_REL = "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"`
- `scripts/p5_sentinel_daemon.py`: `BLACKBOARD_PATH = "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"`
- `scripts/kraken_keeper_turn.py`: returns `Path('hfo_hot_obsidian/hot_obsidian_blackboard.jsonl')`
- `scripts/p6_bronze_progressive_rollup.py`: default `--blackboard` uses that path
- Several scripts use **absolute** `/home/.../hfo_hot_obsidian/hot_obsidian_blackboard.jsonl`

**Mitigation**
- Best compat: keep a symlink file at `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl` pointing to the pointer-blessed blackboard path (today that is the storehouse canonicalized JSONL under the legacy/telemetry folder).
- Best long-term: refactor scripts to read blackboard path from `hfo_pointers.json` (fail-closed if missing).

**Risk**
- If you move `hfo_hot_obsidian/` wholesale into Forge and remove the legacy root, these scripts will silently stop logging or crash.

#### A3. VS Code tasks calling Python entrypoints under Hot Obsidian
**What breaks**
- Tasks that run Python scripts by direct path into `hfo_hot_obsidian/...` will fail.

**Evidence (example)**
- `.vscode/tasks.json` has commands invoking:
  - `hfo_hot_obsidian/bronze/4_archive/.../hfo_orchestration_hub.py`

**Mitigation**
- Keep those paths alive via symlinks until tasks are updated.

### B. Build/test/dev UX (will break tests, local URLs, docs)

#### B1. Playwright tests and hardcoded local URLs
**What breaks**
- Specs that navigate to URLs containing `hfo_hot_obsidian/...` will fail after moves.

**Evidence (examples)**
- `scripts/v33_sticky_drag.spec.ts` uses:
  - `http://localhost:8080/hfo_hot_obsidian/bronze/2_areas/...`
- `scripts/v40_standard_e2e.spec.ts` similar pattern

**Mitigation**
- Either:
  - Preserve legacy paths via symlinks (so the static server still serves the same URL paths), or
  - Update tests to use Forge paths and ensure your server exposes them.

#### B2. TypeScript project includes
**What breaks**
- `tsconfig.json` includes files under `hfo_hot_obsidian/bronze/2_areas/...`. Moving those breaks compile/lint tasks.

**Evidence**
- `tsconfig.json` has include entries pointing at hot obsidian mission-thread sources.

**Mitigation**
- Move the referenced TS files *and* update `tsconfig.json`, or keep compat symlinks.

#### B3. Docs and reports that link to Hot Obsidian paths
**What breaks**
- Internal markdown links (especially in `artifacts/flight/*` and doctrine reports) won’t resolve if paths move.

**Mitigation**
- Accept doc-link rot temporarily (if you don’t care), or do a scripted search+replace later.

### C. Low-risk / informational (annoying, but not fatal)

#### C1. Contracts / JSON manifests listing file paths
**What breaks**
- Any contract or JSON list that encodes file paths may become stale.

**Evidence**
- `contracts/hfo_legendary_commanders_invariants.v1.json` enumerates several `hfo_hot_obsidian/...` file paths.

**Mitigation**
- Decide if those are “identity paths” (must remain stable via alias) or “location paths” (ok to update).

## Recommended Migration Strategy (Fail-Closed)

### Phase A — Compat Mode (minimize breakage)
1) Move content into Forge medallion+PARA.
2) Leave behind:
   - `hfo_hot_obsidian/` directory as a **compat shim** (symlinks into Forge)
   - `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl` as a **symlink** to the pointer-blessed blackboard
3) Do **not** update pointers until the Forge targets are proven present.

### Phase B — Cutover
1) Update `hfo_pointers.json` to Forge-native targets (gateway impl, payload root, etc.).
2) Update hardcoded scripts to consume pointer paths.
3) Update VS Code tasks, TS config, and Playwright specs.
4) Only then, deprecate/remove legacy stubs.

## “Demote any gold” guidance
- Anything currently under `hfo_hot_obsidian/gold/` that is actively referenced by tooling should be treated as **Silver operational doctrine** or **Bronze working notes**, unless it is truly hardened and stable.
- Practically: plan to migrate `gold/3_resources` into Forge Silver resources by default, and reserve Forge Gold for artifacts you *never want to move again*.

## Next Actions
- If you want, I can produce a companion “compat shim spec” that enumerates exactly which symlinks must exist to avoid breakage (gateway + blackboard + payload root + served HTML paths).

