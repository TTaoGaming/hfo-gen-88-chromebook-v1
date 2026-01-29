# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO HIVE8 — P2 (SHAPE): Hibernation vs Brood for “Fork/Evolve” (not just more bodies)

Date: 2026-01-29
Status: Analysis-only (no SSOT change implied)
Baseline SSOT (Gen88 v5): `contracts/hfo_mtg_port_card_mappings.v5.json`

## Why this decision matters (P2 semantics)
If P2 is *“fork simulation / mutated digital twins / evolve-then-select”* then the mnemonic should cue:
- **branching** (multiple candidate trajectories)
- **mutation** (not identical clones)
- **selection pressure** (cull/rollback bad branches)
- **reversibility** (return-to-safe-state)

If the card mostly cues **replication**, it tends to mis-train the intuition toward “just spawn more bodies.”

## Current Gen88 v5 reality check
In Gen88 v5, P2 is currently:
- Tier A (static): **Mirror Entity**
- Tier B (trigger): **Hatchery Sliver**
- Tier C (activated): **Sliver Queen**

Both **Hatchery** and **Queen** are (very) “more bodies” cards. So if your intent is “mutated different forks,” you likely want to revise **more than one** P2 slot.

## Hibernation Sliver vs Brood Sliver (what they *train*)
### Option 1 — Hibernation Sliver (activated: pay life → return to hand)
Best when you want P2 to mean:
- **rollback / revert / retreat** as a first-class move
- **branch safety**: try something; if it destabilizes, pull it back
- **iterative mutation**: re-cast with different context → “same template, different outcome”

Main drawback:
- It’s not inherently “mutation”; it’s “reversibility.” Mutation must be expressed by the *process* around it (e.g., different parameters, different environment, different constraints).

### Option 2 — Brood Sliver (trigger: combat damage → create a token copy)
Best when you want P2 to mean:
- **validated design spawns instances** (factory/replication)
- **scale-out** from success signals

Main drawback (your stated concern):
- It strongly reads as **“more bodies”** and the copies are **not different**. It’s great for “scale,” weak for “mutate.”

## If the goal is truly “fork/evolve,” my recommendation
- Prefer **Hibernation-style semantics** (rollback/branch safety) over Brood-style semantics (replication).
- If you still want “forks,” make them **stochastic / selection-driven**, not “identical token on success.”

### Stronger fork/evolve mnemonic (if you’re open to a third candidate)
- **Frenetic Sliver** (activated: coin-flip phase out vs sacrifice) is a cleaner *evolutionary* cue:
  - many branches attempted
  - selection pressure (some branches die)
  - survivorship becomes “the plan”

## Suggested next step (only if you want to change SSOT)
If you decide P2 should be “mutated forks” rather than “factory scale,” the clean move is a **single-version bump** (v6) that revises P2 Tier B/C together so the metaphor is coherent.

I can propose 1–2 concrete v6 variants (minimal-change) that keep the rest of Gen88 v5 untouched.
