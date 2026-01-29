# Medallion: Silver | Mutation: 0% | HIVE: V

# Mission Thread Omega — Hot/Silver Overview (Product / Gesture / UI Payload)

Date: 2026-01-24

## Definition

Omega is the product/gesture/UI payload thread.

- North Star (hub vision): “Total Tool Virtualization — gestures + multimodal intent manifest virtual tools, with evaluation harness feedback and archive-backed curricula to mastery.”
  - Source: `hfo_hub.py` (`vision` output)

Omega is implemented as *versioned, testable artifacts* (often single-HTML runtimes) and their specs.

## Primary Entry Surfaces (Stable Pointers)

- Active Omega launcher:
  - `active_hfo_omega_entrypoint.html`
  - Forwards to the configured baseline path while forwarding all `flag-*` query params.
  - Source: `active_hfo_omega_entrypoint.html`
- Active Omega config:
  - `active_hfo_omega_entrypoint.json`
  - Source: `active_hfo_omega_entrypoint.json`

In the current config, baseline points at:

- `/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html`

## Omega Architecture Contract (8 Ports)

From hub vision:

- Single HTML artifact preference (avoid dual authority)
- Exactly 8 ports P0–P7
- Cross-port payloads schema-enforced via Zod contracts

Source: `hfo_hub.py`

## Gen5: The “Hex Modular Monolith” Baseline

The Gen5 spec describes a practical path to strong hex boundaries without losing the single-HTML deployment model:

- Spec: `hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V10_HEX_MODULAR_MONOLITH_SPEC_2026_01_20.yaml`
- Baseline artifact (currently active via entrypoint config):
  - `hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html`

Core Omega invariants (from spec):

- Single-authority symbols
- Hex boundaries via Port Facades
- Fail-closed adapter registry
- Contract validation of cross-port payloads
- Stable evaluation harness surface for Playwright (`window.hfoEval`)

Source: `hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V10_HEX_MODULAR_MONOLITH_SPEC_2026_01_20.yaml`

## Gen6: Multi-Hand + Tripwire + Embedded Instrument (v24 Spec)

Gen6 v24 spec is explicitly "spec-first" and emphasizes fail-closed P2/P3 behaviors:

- Spec: `hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/specs/omega_gen6_v24_spec.yaml`
- Base entrypoint for v24 work: `.../omega_gen6_v23_10.html`
- Target v24 artifact: `.../omega_gen6_v24.html` (spec says it should exist; current presence should be validated when implementing)

v24 direction (summary):

- N hands, stable hand identity via coast + snaplock
- Per-hand knuckle TripPlane
- 4 fingertip sensors per hand
- Map fingertip tripwire edges → discrete key events
- GoldenLayout vertical split with Piano Genie iframe
- COMMIT-only delivery by default (fail-closed)

Source: `hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/specs/omega_gen6_v24_spec.yaml`

## What’s Working (Recent Evidence)

From recent MCP memory entries:

- Versioned Omega artifacts (v23.x series) support fork-and-evolve without destructive edits.
- Low-RAM Playwright governance + proof bundles reduce “exit code 9 / SIGKILL” instability during screenshot-heavy runs.

Sources:

- `scripts/hfo_playwright_safe_run.py`
- `playwright.config.ts`

## Critical Gaps (Omega)

- The stable launcher points to Gen5 baseline, but “promotion” rules for moving the baseline are still mostly manual.
- Omega needs a first-class lineage record for “baseline changed from X → Y” (otherwise drift and tribal knowledge accumulate).
- Spec-to-artifact closure: v24 spec exists; implementation needs deterministic proof + promotion steps.

## Next Actions (Omega)

1) Keep FORK_AND_EVOLVE: every new Omega artifact is a new versioned file + a lineage record.
2) Promote baseline only when:
   - minimal Playwright proof passes, and
   - P5 audit is green (warnings acceptable; no BREACH).
3) Encode “baseline selection” into a P1/P7-readable manifest so that Alpha/Omega coordination is explicit.
