# Medallion: Bronze | Mutation: 0% | HIVE: V

# P0 Lidless Legion (ISR) — Port-by-Port Status Report (2026-01-23T17:11:26Z)

**Version:** 2026-01-23T17:11:26Z (timestamp-versioned)

## Executive Summary (Verified)

- **External observation is online:** Tavily + Brave + OpenRouter endpoints are reachable (HTTP 200) per `p3 tracer_venom`.
- **Internal observation is partially online:** repo filesystem access + MCP memory + DuckDB file-index exist; **offline wiki is missing** and gateway health marks `ok=false`.
- **Strict “exactly 8 tools” invariant is currently violated:** optional MCP servers are enabled (`context7`, `omnisearch`). `p3 tracer_venom` fails-closed unless `HFO_ALLOW_OPTIONAL_MCP=1`.

## Ground Truth Inputs (Evidence Links)

- P0/P1/P2/P3/P4/P5/P6/P7 JADC2/Mosaic doctrine: [hfo_hot_obsidian/silver/3_resources/reports/HFO_GEN88_CANALIZATION_SUMMARY.md](hfo_hot_obsidian/silver/3_resources/reports/HFO_GEN88_CANALIZATION_SUMMARY.md)
- P0 “Lidless Legion” commander doctrine: [hfo_hot_obsidian/silver/3_resources/reports/HFO_GRIMOIRE_8_COMMANDERS_TRIPLE_SIDED_HYPER_SLIVER_ARISTOCRATS_2026_01_22.md](hfo_hot_obsidian/silver/3_resources/reports/HFO_GRIMOIRE_8_COMMANDERS_TRIPLE_SIDED_HYPER_SLIVER_ARISTOCRATS_2026_01_22.md)
- Pointer SSOT (targets/ports/versions): [hfo_pointers.json](hfo_pointers.json)
- Tracer implementation (swappable microkernel): [hfo_ports/p3_tracer_venom.py](hfo_ports/p3_tracer_venom.py)

## Canonical “8 Tools” Observation Stack (What P0 should have)

In current repo reality, your “8 tools” for P0 observation can be made concrete as:

1) **filesystem (internal)** — reads workspace artifacts for signals.
2) **memory (internal)** — writes/reads MCP working memory JSONL.
3) **time (internal)** — timestamps evidence.
4) **sequential-thinking (internal)** — controlled reasoning (not observation, but governs it).
5) **tavily (external)** — web evidence.
6) **brave-search (external)** — redundant web evidence.
7) **hfo_mcp_gateway_hub (internal)** — aggregates health + provides tools like DuckDB search.
8) **playwright (internal/external-ish)** — runtime observation of the UI/entrypoint surfaces.

**Important:** in strict mode, having more than these 8 active MCP servers is treated as drift.

## Port-by-Port Walkthrough (JADC2 Mosaic Tile Roles + Repo Reality)

### P0 — SENSE / OBSERVE / ISR ("The Lidless Legion")

**Doctrine:** P0 is the pervasive eye: ISR [0,0].

**What’s good right now (verified):**

- You *do* have dual observation channels:
  - External ISR via Tavily + Brave.
  - Internal ISR via DuckDB file-index + filesystem + blackboard/memory.

**What’s missing (verified):**

- Gateway health still reports `ok=false` because:
  - `context7_key=false`
  - `offline_wiki_path=false`

**Assessment:** P0’s ISR capability is **functionally strong on external/internal evidence**, but the **health contract is not “GREEN”** until you either:

- Provide offline wiki path and Context7 key, **or**
- Explicitly downgrade gateway `ok` semantics to “core-only” vs “optional”.

### P1 — FUSE / ROUTE / Data Fabric

**Doctrine:** schema bridge + fabric; transforms raw P0 telemetry into contracts.

**Repo reality (verified):**

- Cross-port schema work exists (contracts in `contracts/`), but P1 is not yet pinned as a hub action in `ports.*`.

**Operational recommendation:** pin a `ports.p1.preflight` action that validates Zod contracts compile + schema invariants.

### P2 — SHAPE / SYNTH+MODEL / Digital Twin

**Doctrine:** physics twin / simulation [3,2].

**Repo reality:**

- P2 is present in Omega Gen6 work (READY gate, physics semantics) but not wired into hub port runner as a deterministic action.

**Recommendation:** create a `ports.p2.gate` that runs the P2-focused Playwright specs that are already GREEN in MCP memory.

### P3 — DELIVER / MODEL / Effect Delivery

**Doctrine:** inject pointer events; effect delivery [3,3].

**Repo reality (verified):**

- You now have **P3 tracer_venom**, wired as a swappable microkernel plugin and pointer-gated via `ports.p3.tracer_venom`.
- This is an *infrastructure* P3 capability (sanity checking toolchain health), not UI event injection.

### P4 — DISRUPT / DISRUPT / Red Team

**Doctrine:** adversarial pressure (“Scream” tile).

**Repo reality:**

- P4 has pinned test actions in pointers, but runtime expectations may be failing (prior infra notes).

### P5 — DEFEND / AUDIT / Blue Team HardGate

**Doctrine:** integrity checks, governance gates.

**Repo reality:**

- P5 is pinned in pointers (`preflight`, `gate`).

### P6 — STORE / PERSIST / Kraken Keeper

**Doctrine:** telemetry archive; long-term SSOT.

**Repo reality:**

- Memory + DuckDB exist and are referenced by pointers.
- `port6_assimilate` exists in gateway hub.

### P7 — NAVIGATE / PLAN / BMC2

**Doctrine:** orchestration + mission routing.

**Repo reality:**

- Orchestration exists conceptually; not yet pinned as a deterministic hub action.

## Tracer Venom Findings (Current)

- `python3 hfo_hub.py p3 tracer`:
  - **FAILS** because `context7` and `omnisearch` are enabled (drift from strict 8).
- `HFO_ALLOW_OPTIONAL_MCP=1 python3 hfo_hub.py p3 tracer`:
  - **OK** and proves:
    - `TAVILY_API_KEY` present; Tavily search returns HTTP 200
    - `OPENROUTER_API_KEY` present; OpenRouter models endpoint returns HTTP 200
    - `BRAVE_API_KEY` present; Brave web search endpoint returns HTTP 200

## Actionable Next Steps (to make P0 “fully GREEN”)

1) Decide whether `context7` + `omnisearch` are part of your canonical 8.
   - If **no**, remove/disable them in MCP config to restore strict invariant GREEN.
   - If **yes**, promote them into the canonical set and update tracer semantics.
2) Decide whether gateway `tool_health.ok` should be “core-only” (Tavily+OpenRouter+DuckDB+rg) or “all optional integrations present”.
3) Pin P0-specific hub action (e.g. `ports.p0.observe_compile`) that runs `p0_observe_compile` with a model you know is available in OpenRouter.
