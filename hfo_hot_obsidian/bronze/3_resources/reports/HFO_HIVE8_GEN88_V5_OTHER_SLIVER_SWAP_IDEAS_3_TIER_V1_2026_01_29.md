# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO HIVE8 — Gen88 v5: Other Sliver Swap Ideas (3-tier) (Analysis)

Date: 2026-01-29
Status: Analysis-only (do not apply to SSOT without explicit decision)
SSOT baseline (Gen88 v5): `contracts/hfo_mtg_port_card_mappings.v5.json`

## Ground rule
Your **3-tier format** is treated as:
- Tier A = **Sliver (static)**: always-on posture / default field condition
- Tier B = **Sliver (trigger)**: event-driven response / conditional reflex
- Tier C = **Sliver (activated)**: deliberate, paid-cost capability / explicit control action

Gen88 v5 already takes the key theming fix:
- **P7 trigger** is now **Regal Sliver** (C2 legitimacy → coordination), not “more bodies.”

The ideas below are *candidates* for a future v5+ (or v6) if we decide the metaphor is doing the wrong cognitive work.

---

## Candidate swaps by port (3-tier)

### P0 (SENSE / OBSERVE) — keep “truth acquisition” pure
Current (v5):
- A static: Cloudshredder Sliver
- B trigger: Synapse Sliver
- C activated: Telekinetic Sliver

Ideas:
- **Tier B (trigger) option: Synapse Sliver → Sedge Sliver**
  - Why: if you want P0 to feel less like “card draw” and more like “situational sensing advantages under conditions,” Sedge reads as conditional advantage.
  - Risk: might weaken the obvious “information gain” metaphor that Synapse provides.

- **Tier C (activated) option: Telekinetic Sliver → Harmonic Sliver**
  - Why: if you want P0’s active move to be “probe and reveal by touching the environment,” Harmonic as a “contact effect” metaphor can be clearer than “tap/lock.”
  - Risk: overlaps with P3’s current Harmonic identity; only do this if P3 is also reworked.

### P1 (FUSE / BRIDGE) — emphasize contracts + interop safety
Current (v5):
- A static: Quick Sliver
- B trigger: Diffusion Sliver
- C activated: Gemhide Sliver

Ideas:
- **Tier C (activated) option: Gemhide Sliver → Hibernation Sliver**
  - Why: a “paid cost to bounce/retreat” reads like **compat-layer rollback** and safe boundary-crossing.
  - Risk: overlaps with P3’s activated slot today (Hibernation). Only do if you also re-allocate P3’s activated tier.

- **Tier A (static) option: Quick Sliver → Crystalline Sliver**
  - Why: if you want interop to be “hard-to-mutate in transit,” Crystalline reads as strong “don’t poke inside the payload” boundary semantics.
  - Risk: can imply “too opaque to debug.” If adopted, pair with stronger P6 audit cues.

### P2 (SHAPE / SHAPE) — keep “factory/twin” semantics crisp
Current (v5):
- A static: Mirror Entity
- B trigger: Hatchery Sliver
- C activated: Sliver Queen

Ideas:
- **Tier B (trigger) option: Hatchery Sliver → Brood Sliver**
  - Why: if we remove Brood from P7 (C2), this is the more natural home for “validated design spawns instances.”
  - Risk: doubles-down on “more bodies” in P2; only good if P2 is explicitly your scale/factory port.

- **Tier C (activated) option: Sliver Queen → Sliver Overlord**
  - Why: if you want P2’s paid move to be “fetch exactly the component I need” (toolchain assembly) rather than “spawn tokens.”
  - Risk: overlaps with P7’s Overlord; would require a coordinated swap (P7 activated changes too).

### P3 (DELIVER / INJECT) — delivery wants “recomposition + safe retreat”
Current (v5):
- A static: The First Sliver
- B trigger: Harmonic Sliver
- C activated: Hibernation Sliver

Ideas:
- **Tier C (activated) option: Hibernation Sliver → Necrotic Sliver**
  - Why: if P3’s paid action should feel like “surgical removal / rollback by deletion,” Necrotic reads like targeted excision.
  - Risk: overlaps with P4’s activated tier today (Necrotic). Only do if you’re intentionally blurring P3/P4.

- **Tier A (static) option: The First Sliver → Quick Sliver**
  - Why: if “delivery” is really about responsiveness / time-to-effect, Quick reads as always-on delivery readiness.
  - Risk: weakens the “cascade/recomposition” motif that The First Sliver currently carries.

### P6 (STORE / ASSIMILATE) — memory wants “recover, index, rehydrate”
Current (v5):
- A static: Dregscape Sliver
- B trigger: Lazotep Sliver
- C activated: Homing Sliver

Ideas:
- **Tier B (trigger) option: Lazotep Sliver → Synapse Sliver**
  - Why: if you want the “learning loop” to trigger on engagement and reward “postmortem insight,” Synapse reads as “insight extraction” more than Lazotep’s “armor.”
  - Risk: steals P0’s “info gain” identity; do only if you deliberately want P6 to be the primary “insight converter.”

- **Tier C (activated) option: Homing Sliver → Sliver Overlord**
  - Why: if retrieval is the paid move, Overlord reads as “fetch exact capability from the library.”
  - Risk: overlaps with P7 activated; would force a larger rebalance.

### P7 (NAVIGATE / NAVIGATE) — C2 wants legitimacy + pruning
Current (v5):
- A static: Sliver Legion
- B trigger: Regal Sliver
- C activated: Sliver Overlord

Ideas:
- **Tier A (static) option: Sliver Legion → Diffusion Sliver**
  - Why: if P7’s always-on posture should be “reduce random interference with command,” Diffusion reads like “C2 friction shield.”
  - Risk: may underplay the “global alignment” motif Sliver Legion currently provides.

- **Tier C (activated) option: Sliver Overlord → Sliver Hivelord**
  - Why: if the paid move is “make the current plan resilient while executing,” Hivelord reads as “protect the plan from being destroyed mid-flight.”
  - Risk: overlaps with P5 (defense) semantics; only adopt if you want P7 to own more execution-resilience.

---

## My strongest 2 recommendations (if we ever do v6)
1) Move **Brood Sliver** (if we want it at all) into **P2 trigger** to make P2 the explicit scale/factory port.
2) Keep **P7 trigger = Regal Sliver** permanently; it’s the cleanest C2 mnemonic in the set.
