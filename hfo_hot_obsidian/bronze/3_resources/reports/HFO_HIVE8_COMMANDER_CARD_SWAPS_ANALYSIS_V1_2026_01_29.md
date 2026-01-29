# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO HIVE8 — Commander Card Swaps (Analysis)

Date: 2026-01-29
Scope: Recommendations only (no SSOT changes applied)
Source of current mapping: `contracts/hfo_mtg_port_card_mappings.v5.json`

## Why swaps at all?
The current 3-slivers + 1-equipment mapping is already internally consistent, but a few slots can be made more “capability-complete” across the lattice by:
- increasing *governance + legitimacy* in C2 (P7)
- increasing *memory/consolidation semantics* in AAR/learning (P6)
- increasing *secure boundary/transport semantics* in interoperability (P1)
- increasing *pure reconnaissance/scouting semantics* in sensing (P0)

Constraints I’m using:
- Keep the port identity (commander + port role) unchanged.
- Prefer swaps that increase “explainability” (the metaphor should be obvious).
- Prefer swaps that introduce missing capability coverage across the 8 without duplicating too much.

## Proposed swaps (4)

### Swap 1 — P7 (NAVIGATE / C2): Brood Sliver → Regal Sliver
- Current slot: P7 `trigger` = Brood Sliver
- Proposed: P7 `trigger` = Regal Sliver
- Why this rounds out P7:
  - Brood Sliver reads as “success spawns capacity,” which is a tempting C2 metaphor but (in HFO) risks pulling P7 into “more bodies” instead of “better authority + coordination.”
  - Regal Sliver reads as “legitimacy + distributed mandate” — a clearer C2 metaphor: a *recognized authority state* that lowers coordination costs and improves convergence.
- Systems-thinking effect:
  - Shifts P7’s dominant positive feedback loop from “more bodies → more bodies” to “recognized authority → better information → better decisions → sustained authority.”
- Tradeoffs / red-team notes:
  - Regal introduces a higher governance narrative; if the project wants P7 to stay “pure hunt/heuristics,” it may feel too political.
  - If you rely on P7 being the “scale engine,” you may miss Brood’s explicit growth cue.

### Swap 2 — P6 (STORE / AAR & learning): Sword of Fire and Ice → Mask of Memory
- Current equipment: P6 = Sword of Fire and Ice
- Proposed equipment: P6 = Mask of Memory
- Why this rounds out P6:
  - P6’s job is assimilation, summarization, and distillation. “Mask of Memory” is *literal* and matches the behavior we want: capture signal, discard noise, keep the distilled artifact.
  - The Sword reads as “damage + burst value” (strong card, weaker metaphor). Mask reads as “structured remembering.”
- Systems-thinking effect:
  - Better aligns with the SSOT doctrine: ingest → compress → retrieve → revise (a negative-feedback stabilizer on mission drift).
- Tradeoffs / red-team notes:
  - Mask is less “powerful” as a generic fantasy artifact than a Sword; if the aesthetic goal is “mythic weapon,” this is a tone change.
  - This creates some metaphor overlap with P0’s Synapse (draw) semantics, but that overlap is acceptable: P0 *acquires*, P6 *consolidates*.

### Swap 3 — P1 (FUSE / interoperability): Goldvein Pick → Whispersilk Cloak
- Current equipment: P1 = Goldvein Pick
- Proposed equipment: P1 = Whispersilk Cloak
- Why this rounds out P1:
  - Goldvein Pick reads as “extract value / treasure.” That’s a decent bridge metaphor (adapters create usable value), but it underplays the *secure boundary + encapsulation* requirement.
  - Whispersilk Cloak reads as “protected transit” — a clean metaphor for contract-wrapped payloads moving across system boundaries without being mutated mid-flight.
- Systems-thinking effect:
  - Reinforces fail-closed boundaries: interoperability should reduce coupling and increase safety.
- Tradeoffs / red-team notes:
  - Cloak is more “stealth” than “schema.” If you prefer P1 to stay explicitly about “common language,” consider a more “tooling/utility” equipment later.

### Swap 4 — P0 (SENSE / observe under contest): Infiltration Lens → Explorer’s Scope
- Current equipment: P0 = Infiltration Lens
- Proposed equipment: P0 = Explorer’s Scope
- Why this rounds out P0:
  - Infiltration Lens reads as “force interaction to draw info.” That’s closer to active probing/infiltration, which P4 already owns.
  - Explorer’s Scope reads as “scouting + looking ahead,” which is a clearer “SENSE” metaphor: gather raw observations, map the unknown, reduce uncertainty.
- Systems-thinking effect:
  - Moves P0 slightly toward *measurement* and away from *provocation*, keeping “contestation” centered in P4.
- Tradeoffs / red-team notes:
  - If your doctrine intentionally wants P0 to include “ISR under contest” (hostile environment), the Lens is defensible; Scope may feel too “peaceful reconnaissance.”

## If you decide to adopt any of these
These are SSOT-impacting changes. The correct path is:
1) Update the authoritative mapping in `contracts/hfo_mtg_port_card_mappings.v5.json`
2) Re-run the existing doc generator so all Gold ladder docs + meta synthesis stay fail-closed consistent
3) Let precommit fail-closed enforcement catch any drift

## Quick recommendation order
If you only take 1–2 swaps:
1) P6 equipment swap (Sword → Mask) for thematic correctness
2) P7 Brood → Regal for governance/legitimacy framing
