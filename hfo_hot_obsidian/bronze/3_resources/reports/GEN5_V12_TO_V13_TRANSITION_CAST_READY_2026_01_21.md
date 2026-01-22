# Medallion: Bronze | Mutation: 0% | HIVE: V

# Gen5 v12 → v13 Transition (Cast/Projector-Ready Gesture Substrate)

Date: 2026-01-21

## Scope

This is a transition document (spec/report) for evolving Gen5 from **v12 multi-app shared substrate** into **v13 hot-swap hardened**, with an explicit product framing:

- **Controller device**: mobile phone or laptop running the gesture substrate (camera + FSM + injection)
- **Display surface**: projector / cast target showing the active adapter(s)

Primary goal: make “swap consumer software live” reliable without breaking the single-authority substrate ports.

## Executive Summary (grounded)

What v12 already asserts (contract-level):

- HERO is the substrate; apps are adapters mounted into HERO overlays.
- One camera capture authority; multiple views are mirrors (no multi-capture).
- P3 routes pointer injection deterministically according to policy, ideally through AppHost.

Evidence:

- v12 spec: multi-app shared substrate + single camera invariant.
  - See hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V12_MULTIAPP_SHARED_SUBSTRATE_SPEC_2026_01_20.yaml

What v13 tightens (hot-swap level):

- Activation is idempotent, centralized, and **waits for iframe readiness** before becoming “active”.
- Hot-swap surfaces (dropdown + GoldenLayout tabs) delegate to AppHost only.
- Optional dual-HERO experiment introduces a `heroSlotId` concept.

Evidence:

- v13 spec: strict hot-swap semantics + readiness gating + optional dual-HERO.
  - See hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V13_ADAPTER_HOTSWAP_SPEC_2026_01_21.yaml

Observed “roots” impacting demo feel (not just symptoms):

- The active harness defaults currently disable camera capture.
  - active_hfo_omega_entrypoint.json sets `flag-disable-camera: "true"`.
  - This makes any “video background” / camera-derived gesture pipeline appear missing/inert by default.

Evidence:

- active_hfo_omega_entrypoint.json

## Reality Check: v12 Readiness vs v12 Spec

There is a deliberate tension between the readiness report and the v12 spec:

- The readiness report (2026-01-20) describes v11 as “substrate + one app” and calls out missing AppHost + routing contracts.
- The v12 spec (2026-01-20) declares the intended target state (multi-app, shared substrate, AppHost/TargetRouter).

Interpretation:

- v12 is the **desired consolidation**, not necessarily fully promoted/hardened everywhere in the harness.
- v13 is a **targeted hardening pass** focused on hot-swap correctness, not a rewrite.

Evidence:

- Readiness report: hfo_hot_obsidian/bronze/3_resources/reports/GEN5_MULTIAPP_V12_READINESS_2026_01_20.md
- v12 spec: hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V12_MULTIAPP_SHARED_SUBSTRATE_SPEC_2026_01_20.yaml

## Root Invariants to Preserve (v12 → v13)

These invariants are the “roots” to protect so casting and hot-swap don’t regress into whack-a-mole fixes.

### 1) Single authority per service

- Camera capture: exactly one authority (P0).
- DataFabric: exactly one authority (P1).
- Injection routing/delivery: exactly one authority (P3).
- App lifecycle / overlay visibility: exactly one authority (P7 AppHost).

Evidence:

- v12 spec: invariants/single_authority and shared_substrate.

### 2) Same-origin adapters for deterministic targeting

- Deterministic `elementFromPoint` probing and injection into iframe documents requires same-origin.
- Cross-origin demos are not baseline; vendor locally or build minimal internal demo.

Evidence:

- v12 spec: “No cross-origin apps in v12 baseline”.
- v13 spec: “same_origin_only: true”.

### 3) Active-target routing policy is explicit

- ACTIVE_APP_ONLY is a first-class policy.
- TargetRouter must ask AppHost for the active target root when enabled.

Evidence:

- v12 spec: target_routing policies.
- v13 spec: hotswap requirements for ACTIVE_APP_ONLY.

## Why “Video Background is Gone” (grounded, harness-level)

The default harness flags currently disable camera capture.

- active_hfo_omega_entrypoint.json has `flag-disable-camera: "true"`.
- This is consistent with seeing no webcam feed / no camera-driven overlays.

This is not a “bug in rendering”; it is a **boot-time configuration**.

Evidence:

- active_hfo_omega_entrypoint.json

Recommended diagnostic lever (not promoted change):

- Run the active entrypoint with `?flag-disable-camera=false` and verify whether the video substrate returns.

## Why “COMMIT Does Nothing” (root-cause map)

COMMIT is a downstream effect. If any upstream invariant is disabled, COMMIT can appear inert.

Minimum pipeline for “COMMIT causes visible effect”:

1) Controller produces a commit intent (FSM state transition exists)
2) P3 injector receives a pointer envelope
3) TargetRouter selects an active target root (ACTIVE_APP_ONLY)
4) Adapter overlay is visible + ready (iframe loaded)
5) Adapter has a concrete binding (e.g., click synthesis or keypress bridge)

The most common “root breaks” in this chain are:

- App activation marks active before iframe is ready (hotswap race)
- Active routing has no valid root (misconfigured active adapter)
- Upstream sensing is disabled (camera off), so FSM never emits commit

v13 explicitly addresses the race by requiring “activation waits for iframe readiness signal”.

Evidence:

- v13 spec: AppHost required behaviors (activation waits for iframe readiness).

## v13: What Changes (delta list)

v13 is a minimal clone of v12 with stricter hot-swap semantics.

### Required v13 deltas

- AppHost activation is:
  - idempotent
  - centralized for overlay visibility toggles
  - readiness-gated (iframe loaded + ready signal)

- UI surfaces:
  - dropdown lists AppHost registry
  - GoldenLayout tab changes delegate to AppHost only

- P3 routing:
  - ACTIVE_APP_ONLY must always query AppHost for active target root
  - injector behavior selected by adapter metadata, not hardcoded app IDs

Evidence:

- v13 spec: apphost + hotswap_surface + p3_target_routing.

### Optional v13 experiment

- Dual-HERO tabs with `heroSlotId` to allow A/B substrate views.

Evidence:

- v13 spec: optional_experiment_dual_hero_tabs.

## Casting/Product Framing: Controller vs Display

To make Gen5 “cast/projector-ready” without architectural drift, treat casting as a transport boundary around the display surface.

### Recommended model (v13 framing)

- Controller runs the substrate ports (P0/P1/P3/P7) and produces:
  - typed FSM events
  - pointer envelopes
  - adapter switch events

- Display runs a thin viewer shell that:
  - renders the active adapter iframe(s)
  - accepts injected pointer envelopes and applies them to the active adapter root

Key requirement: all cross-device messages must be schema-validated (P1-owned contracts).

This keeps “gesture sensing” independent from “render/display”, and aligns with v12’s shared substrate principle.

### Contract additions implied

v13 already proposes:

- `HeroSlotId`
- `AdapterSwitchEvent`
- `ActiveAdapterState`

For casting, extend with:

- `PointerEnvelope` (if not already a stable contract)
- `FsmEvent`
- `ControllerHeartbeat` (timing/latency/ready state)

Evidence:

- v12 spec: contracts list includes FsmEvent.
- v13 spec: contracts v13_additions.

## Concrete Migration Steps (v12 → v13)

1) Clone v12 artifact → v13 artifact (rename only).
2) Register at least 2 adapters (Excalidraw + one non-Excalidraw, same-origin).
3) Add readiness gating:
   - AppHost.activate waits for iframe load + adapter-ready signal.
4) Enforce ACTIVE_APP_ONLY routing through AppHost.
5) Add Playwright gates focused on hot-swap (dropdown and tab).

Evidence:

- v13 spec: migration_plan and acceptance_tests.

## Acceptance Gates (minimum)

- Switch adapter A → B via dropdown (no reload) and verify target routing resolves inside B.
- Switch B → A and verify adapter-specific behavior is selected via metadata only.

Evidence:

- v13 spec: acceptance_tests.

## Risks / Failure Modes (casting-aware)

- UI timing races: options populate before registration.
  - Mitigation: AppHost list + delayed refresh.

- Iframe readiness races: routing before load.
  - Mitigation: activation waits on ready signal.

- Cross-origin adapters: non-deterministic targeting.
  - Mitigation: vendor locally; same-origin only.

Evidence:

- v13 spec: risks.

## Next Grounded Step

If the immediate objective is to validate “cast-ready substrate” rather than patch symptoms:

- First confirm camera flag state (active harness defaults disable camera).
- Then promote v13 readiness gating and hot-swap Playwright gates.

Evidence:

- active_hfo_omega_entrypoint.json
- v13 spec: activation readiness + hot-swap tests
