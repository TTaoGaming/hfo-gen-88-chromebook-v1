# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Gen6 — UI Shell Microkernel + Hexagonal 8 Ports (GoldenLayout + lil-gui) Report

Date: 2026-01-22
Scope: Omega Gen6 UI composition and the coupling between GoldenLayout/lil-gui panels and the HFO 8-port hexagonal core.

## Executive Summary

You’re already very close to exemplar composition on the *core* side (ports-first semantics + contract thinking + deterministic replay posture). Where you’re paying the “bespoke glue tax” is the **UI shell boundary**:

- GoldenLayout panels, lil-gui folders, and per-frame UI updates are currently coupled to runtime globals and lifecycle timing.
- This produces fragile panel behavior (subscribe ordering, missing/duplicated DOM roots, resize/activation mismatches, stale listeners).

Recommendation (Pareto-optimal):

- Keep **Hexagonal Architecture (Ports & Adapters)** as the core organizing principle for the 8 ports.
- Adopt a **Microkernel (Plug-in) Architecture** *only* for the UI shell: GoldenLayout becomes the shell; panels + lil-gui folders become plugins.
- Standardize one manifest-driven boundary (LayerManifest / CompositionManifest / AdapterManifest + a new UIShellPluginManifest) so the shell is a thin host and plugins never “reach into” port internals.

## Grounding (Evidence in this repo)

These files are the evidence anchor points for this report:

- Gen6 v16 entrypoint includes GoldenLayout + lil-gui importmap/flags and per-frame `updateVisualPanels`:
  - [omega_gen6_v16.html](omega_gen6_v16.html)
- Gen6 v16 initializes the dev effects bus before GoldenLayout loads (lifecycle coupling hot spot):
  - [omega_gen6_v16.html](omega_gen6_v16.html)
- Gen6 v1 composition spec explicitly defines LayerManifest/CompositionManifest/AdapterManifest and “Touch2D never chooses DOM; emits envelopes only”:
  - [GEN6_V1_TACTICAL_VIEW_COMPOSITION_SPEC_2026_01_21.yaml](GEN6_V1_TACTICAL_VIEW_COMPOSITION_SPEC_2026_01_21.yaml)
- Gen6 multi-app readiness synthesis calls out contract drift + capability-driven manifests + fail-closed routing:
  - [OMEGA_GEN6_MULTIAPP_READINESS_SYNTHESIS_2026_01_21.md](OMEGA_GEN6_MULTIAPP_READINESS_SYNTHESIS_2026_01_21.md)

## What’s going wrong (Observed symptoms)

If you feel “panels are often broken / haunted”, these are the recurring classes of failure in a GoldenLayout+lil-gui environment:

1) **Lifecycle ordering bugs**

- Panels subscribe before the bus exists, or after the relevant events already happened.
- Panels mount before their DOM container is sized, then never recover.

1) **Resize + activation drift**

- GoldenLayout changes tab visibility and container sizes; canvas-based views need explicit resize handling.
- Some panels keep rendering while hidden, consuming resources and producing stale state.

1) **Global state coupling**

- Panels reach into `window.*` objects, which encourages implicit dependencies and hidden contracts.
- It becomes easy to “fix a panel” by directly calling a port function instead of flowing through the port boundary.

1) **Per-frame UI work**

- Updating many GUI elements each animation frame causes jank and amplifies flakiness.
- It also increases the chance of race conditions between shell updates and plugin rendering.

## Root cause (Where you are weakest, and why)

You are weakest at the **composition boundary** (shell ↔ plugins ↔ ports). Not because you lack architecture—because you have **too many overlapping integration mechanisms**:

- OpenFeature flags (feature toggles)
- GoldenLayout layout tree (composition)
- lil-gui controllers/folders (configuration + debug)
- `window.hfoPortsEffects` (observability bus)
- `window.hfoRegistry` (runtime registry)
- `window.hfoState` (test transparency surface)

These are all individually useful. The weakness is that they aren’t yet unified under *one* contract-driven “UI shell API” that plugins use.

Result: when a panel breaks, the easiest local fix is bespoke glue (special cases, conditional initialization, ad-hoc event listeners), and those accumulate.

## Target architecture: Hexagonal core + Microkernel UI shell

### Pattern names (exemplar patterns)

- **Hexagonal Architecture** (Ports & Adapters): your HFO P0–P7 ports are the stable seams.
- **Microkernel / Plug-in Architecture**: a minimal shell provides services; plugins provide features.
- **Modular Monolith**: one deployable artifact where modules/plugins are still cleanly isolated.

### Responsibility split (crisp boundaries)

**Core (Hex, ports-first)**

- Defines contracts and invariants.
- Emits events through a stable bus.
- Does not import GoldenLayout, lil-gui, or any panel code.

**UI Shell (Microkernel host)**

- Owns GoldenLayout and the DOM container.
- Owns plugin lifecycle: install → activate → deactivate → dispose.
- Provides services to plugins:
  - event subscription (ports effects)
  - settings storage
  - logging/telemetry
  - theming tokens

**UI Plugins (adapters)**

- Panels (GoldenLayout components)
- lil-gui folders (debug/config surfaces)
- Optional overlays (HUDs)

Plugins may:

- subscribe to port events
- render derived state
- publish “commands” to the shell (not directly to ports)

Plugins may NOT:

- call into port internals directly
- patch global runtime objects
- own routing policy

### The “one seam” rule (Pareto)

Make the shell expose exactly one seam:

- `window.hfoUiShell` (or registry token) that implements a small API.

Everything UI-side goes through that API:

- GoldenLayout panel creation
- lil-gui creation
- plugin registration
- plugin settings
- port event subscription

This is how you stop bespoke glue from spreading.

## Contracts & manifests (stop the drift)

You already have manifest thinking in Gen6 docs. Extend it one level:

### Keep (already in your Gen6 posture)

- **LayerManifest**: what a GoldenLayout layer is.
- **CompositionManifest**: which layers are active + GoldenLayout tree.
- **AdapterManifest**: iframe tool adapters and capabilities.

(See the contract list in [GEN6_V1_TACTICAL_VIEW_COMPOSITION_SPEC_2026_01_21.yaml](GEN6_V1_TACTICAL_VIEW_COMPOSITION_SPEC_2026_01_21.yaml))

### Add (UIShellPluginManifest)

Define a small plugin manifest that declares what the plugin contributes:

- `id`, `title`
- `contributes.panels[]` (GoldenLayout components)
- `contributes.guiFolders[]` (lil-gui folders)
- `consumes.events[]` (port event types it subscribes to)
- `publishes.commands[]` (shell commands it can emit)

This manifest should be validated (Zod) at registration time and **fail-closed**.

## Why GoldenLayout panels break (and how microkernel fixes it)

GoldenLayout assumes *component lifecycle* discipline.

A microkernel solves this by providing a single place to enforce:

- Mount once, dispose once.
- Subscribe/unsubscribe symmetry.
- Resize handling for canvases.
- Activation handling (tab selected vs hidden).
- Optionality (plugin can be disabled without side effects).

Practically:

- Shell installs a panel plugin.
- Shell creates the GoldenLayout component.
- Plugin gets a `PanelContext` with:
  - container element
  - `onResize`, `onShow`, `onHide`, `dispose`
  - `events.subscribe(...)` handle

If a panel can’t meet the contract, it does not load.

## Apple HIG + Material 3 alignment (practical guidance for this stack)

This repo is not a native iOS/Android app, but you can still follow the *spirit* of both systems.

### 1) One navigation model

GoldenLayout can easily become “everything everywhere”. Pick one primary mode:

- **Task-first**: each main tab = a task (Sense / Navigate / Deliver), with secondary debug panels optional.

Rule:

- Core task panels are always present.
- Debug panels are plugins, off by default.

### 2) Design tokens (stop per-panel styling drift)

Define shared tokens at the shell level:

- color roles: surface, surfaceVariant, primary, error, warning, success
- typography scale: body, label, title
- spacing scale: 4/8/12/16/24

Then plugins consume tokens; they do not invent palettes.

### 3) Density + hit targets

GoldenLayout tends to encourage dense UI. Borrow the HIG/M3 constraint:

- Minimum interactive target size (mouse): “comfortable” targets.
- For touch overlays: targets must be larger.

Operationally:

- Default panel controls are “comfortable density”.
- Add a `density` token (comfortable/compact) for power users.

### 4) Feedback and states

Your ports already emit lots of states (IDLE/READY/COMMIT/COAST).

Map them consistently:

- Neutral/idle → gray
- Ready/armed → amber
- Commit/active → primary
- Error/breach → red

Do not let each plugin decide colors.

### 5) Progressive disclosure (key Pareto lever)

HIG and M3 both reward progressive disclosure:

- Show only what’s needed for the current task.
- Hide advanced debug controls behind an “Advanced” section.

For lil-gui:

- Default: minimal folders.
- Advanced: deep tuning knobs.

## Concrete refactor proposal (Bronze → Silver path)

### Bronze (now): reduce glue without rewrites

1) Create a “UI Shell” module inside the Gen6 HTML that:
   - initializes GoldenLayout
   - registers plugins
   - exposes a small API
2) Convert your top 2–3 flaky panels into plugins first.
3) Move lil-gui folder creation into plugins (no global scattered folder creation).
4) Ensure every plugin cleans up:
   - event listeners
   - subscriptions
   - intervals/raf loops

### Silver (integration): validate and gate

1) Add Zod schema for UIShellPluginManifest.
2) Add a small deterministic test that:
   - loads Gen6
   - registers one plugin
   - asserts panel mounts and disposes cleanly
3) Validate that disabling plugins yields the “light URL” stable baseline.

### Gold (hardened): fail-closed composition

1) Treat composition as data:
   - CompositionManifest drives which plugins are active.
2) Deny-by-default:
   - a plugin can’t subscribe/publish outside its manifest.
3) Add mutation-scored tests around plugin lifecycle invariants.

## Checklist: where bespoke glue is most likely accumulating

Use this checklist to locate the hotspots:

- Any panel that reads or writes `window.hfo*` directly.
- Any panel that has its own copy of “routing” or “active tool selection”.
- Any panel that updates UI every frame instead of reacting to events.
- Any panel that does not have explicit `dispose()` cleanup.
- Any panel that hardcodes adapter IDs instead of reading capabilities.

The manifest-driven posture in [OMEGA_GEN6_MULTIAPP_READINESS_SYNTHESIS_2026_01_21.md](OMEGA_GEN6_MULTIAPP_READINESS_SYNTHESIS_2026_01_21.md) is the right direction; extend the same discipline to UI panels.

## Bottom line

You don’t need “more architecture.” You need **one authoritative UI shell seam**.

- Hexagonal ports remain the stable engine.
- GoldenLayout becomes the microkernel host.
- Panels + lil-gui become plugins with a validated manifest.

That’s the cleanest path to exemplar composition with minimal bespoke glue.
