<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
deliverable: legendary_commanders_3_plus_1_compendium
version: v1
created_utc: 2026-01-29
provenance:
  identity_ssot: contracts/hfo_legendary_commanders_invariants.v1.json
  mapping_ssot: contracts/hfo_mtg_port_card_mappings.v5.json
  fail_closed_verifier: scripts/verify_hive8_mtg_card_mappings.mjs
  gold_sources:
    front_door: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_HIVE8_LEGENDARY_COMMANDERS_3_PLUS_1_MTG_JADC2_FRONT_DOOR_V1_2026_01_29.md
    meta_synthesis: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_LEGENDARY_COMMANDERS_META_SYNTHESIS_V1_2026_01_29.md
    meadows_synthesis: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_JADC2_MOSAIC_MEADOWS_COMMANDERS_3_PLUS_1_SYNTHESIS_V1_2026_01_29.md
---

# HFO HIVE8 — Gen88 v5: 8 Legendary Commanders (3 Slivers + 1 Equipment) — 18-page Compendium (V1)

## BLUF (Executive Summary)
HFO HIVE8 is an **8-tile, safety-coupled control lattice** for agentic work: each Port (P0–P7) is a system role with explicit boundaries, and every “forward push” is paired with an opposing stabilizer (anti-diagonal) to prevent drift, reward hacking, and brittle scaling.

This compendium promotes one practical behavior: **treat SSOT as law (contracts), treat Gold docs as derived views, and keep the whole system fail-closed**.

- **Authoritative identity SSOT**: `contracts/hfo_legendary_commanders_invariants.v1.json`
- **Authoritative 3+1 mapping SSOT (Gen88 v5)**: `contracts/hfo_mtg_port_card_mappings.v5.json`
- **Fail-closed enforcement**: `scripts/verify_hive8_mtg_card_mappings.mjs`

### What changed in v5 (so you can sanity-check quickly)
Only one mapping change vs prior mapping generations: **P7 trigger is Regal Sliver** (C2 legitimacy/coordination cue), not Brood.

---

## Mapping Table (SSOT-locked)

| Port | Commander        | Mosaic Domain                                 | Sliver (Static)      | Sliver (Trigger)   | Sliver (Activated) | Equipment (Non-creature)  |
| ---- | ---------------- | --------------------------------------------- | -------------------- | ------------------ | ------------------ | ------------------------- |
| P0   | Lidless Legion   | ISR / sensing under contest                   | Cloudshredder Sliver | Synapse Sliver     | Telekinetic Sliver | Infiltration Lens         |
| P1   | Web Weaver       | Shared data fabric / interoperability         | Quick Sliver         | Diffusion Sliver   | Gemhide Sliver     | Goldvein Pick             |
| P2   | Mirror Magus     | Creation / digital twin / spike factory       | Mirror Entity        | Hatchery Sliver    | Sliver Queen       | Illusionist's Bracers     |
| P3   | Harmonic Hydra   | Delivery / payload injection / recomposition  | The First Sliver     | Harmonic Sliver    | Hibernation Sliver | Blade of Selves           |
| P4   | Red Regnant      | Red team / contestation / destructive probing | Venom Sliver         | Thorncaster Sliver | Necrotic Sliver    | Blade of the Bloodchief   |
| P5   | Pyre Praetorian  | Blue team / defense-in-depth / recovery       | Sliver Hivelord      | Pulmonic Sliver    | Basal Sliver       | Sword of Light and Shadow |
| P6   | Kraken Keeper    | AAR / learning / assimilation                 | Dregscape Sliver     | Lazotep Sliver     | Homing Sliver      | Sword of Fire and Ice     |
| P7   | Spider Sovereign | C2 / navigate / hunt heuristics               | Sliver Legion        | Regal Sliver       | Sliver Overlord    | Lightning Greaves         |

---

## How to read each commander section (the “2 pages”)
Each commander section is written as an operational two-page: it includes (1) intent + boundaries, (2) the 3+1 mnemonic, (3) Meadows stocks/flows/loops/delays, (4) invariants + failure modes, and (5) the anti-diagonal coupling.

Deep dives are linked, but this compendium is designed to be **reviewable as a standalone promotion candidate**.

---

# P0 — Lidless Legion (OBSERVE) — SENSE / ISR under contest
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P0_SENSE_OBSERVE_LIDLESS_LEGION_LADDER_8PART_V1_2026_01_28.md`

## Role (one sentence)
Convert the world into calibrated evidence: observations that can survive contest, drift, and adversarial noise.

## 3+1 anchor (mnemonic)
- Static: Cloudshredder Sliver → default posture: fast acquisition / high cadence capture
- Trigger: Synapse Sliver → convert engagements into “insight increments” (information gain)
- Activated: Telekinetic Sliver → deliberate control of attention / fixation / occlusion handling
- Equipment: Infiltration Lens → turn resistance into observable signal (forced disclosure)

## Boundaries (what P0 owns vs does not)
- Owns: sampling, normalization, provenance tagging, and “candidate truth” packaging.
- Does not own: cross-boundary typing contracts (P1), dispatch (P3), suppression policy (P4), or SSOT writes (P6).

## Meadows frame (stocks / flows / loops / delays)
- Stocks: raw observation buffer, calibration state, confidence mass, sensor debt.
- Flows: ingest → normalize → tag → emit exemplar.
- Reinforcing loop $R_{cal}$: better calibration → better observations → better calibration.
- Balancing loop $B_{noise}$: anomaly detection → attenuation → reduced false positives.
- Delays: sensor lag, preprocessing latency, model-update cadence.

## Invariants (fail-closed intent)
- Observations must carry provenance sufficient for later rejection (not “pretty dashboards”).
- If the observation can influence action, it must be reproducible or explicitly flagged as non-reproducible.

## Failure modes + tripwires
- Reward hack: “optimize for easy-to-measure signals” → tripwire on mismatch between observed improvements and downstream action quality.
- Drift: quietly changing feature extraction → tripwire on calibration deltas + exemplar regression.

## Anti-diagonal coupling (P0 ↔ P7)
P0 produces evidence; P7 turns that evidence into bounded intent. The pair prevents “observe everything” and “decide everything” pathologies.

---

# P1 — Web Weaver (BRIDGE) — FUSE / Data fabric interoperability
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P1_FUSE_BRIDGE_THE_WEB_WEAVER_LADDER_8PART_V1_2026_01_28.md`

## Role (one sentence)
Make boundaries explicit: schema-validate what crosses ports so drift cannot silently propagate.

## 3+1 anchor (mnemonic)
- Static: Quick Sliver → “bridge readiness” (low-latency interop posture)
- Trigger: Diffusion Sliver → event-driven friction against hostile/invalid integration
- Activated: Gemhide Sliver → paid-cost resource enabling (turn compatibility into energy)
- Equipment: Goldvein Pick → turn work into portable value units (accounting for integration)

## Boundaries
- Owns: contracts/schemas, parsing, validation, IR transformation.
- Does not own: deciding priorities (P7), storing truth (P6), or applying suppression (P4).

## Meadows frame
- Stocks: schema library health, validation backlog, interface trust.
- Flows: parse → validate → transform → publish typed IR.
- $R_{contract}$: clearer schemas → fewer errors → more stable schemas.
- $B_{drift}$: reject invalid payloads → invariants preserved.
- Delays: version negotiation and downstream discovery.

## Invariants
- Cross-port payloads must be schema-validated; failures must fail-closed.
- “Views” (docs, dashboards) must not overwrite SSOT.

## Failure modes
- Over-permissive parsing becomes a covert coupling → tripwire on untyped fields and schema bypass.

## Anti-diagonal coupling (P1 ↔ P6)
P1 makes safe shapes; P6 makes those shapes durable and recallable.

---

# P2 — Mirror Magus (SHAPE) — SHAPE / Digital twin and constrainted creation
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P2_SHAPE_SHAPE_MIRROR_MAGUS_LADDER_8PART_V1_2026_01_28.md`

## Role (one sentence)
Generate admissible candidate structures (COAs, twins, simulations) under explicit constraints.

## 3+1 anchor (mnemonic)
- Static: Mirror Entity → shape-shift the same substrate into many candidate forms
- Trigger: Hatchery Sliver → successful conditions produce additional candidate capacity
- Activated: Sliver Queen → deliberate creation of instances when you pay the cost
- Equipment: Illusionist's Bracers → copy an activated capability (amplify deliberate shaping)

## Boundaries
- Owns: constraint definition, admissibility checks for generated candidates, and stability envelopes.
- Does not own: final promotion gate (P5) or mission routing (P7).

## Meadows frame
- Stocks: constraint satisfaction margin, model inventory, simulation debt.
- Flows: propose → constrain → simulate → score.
- $B_{constraint}$: violations → resolution → reduced violations.
- $R_{coherence}$: coherent state → predictable interaction → stronger coherence.
- Delays: timestep, stabilization iterations, evaluation latency.

## Invariants
- Candidate generation must not bypass the P5 gate for promotion.
- Model quality must be expressed as constraints + evidence, not vibes.

## Failure modes
- “More candidates” without selection pressure becomes noise → tripwire on candidate count vs accepted utility.

## Anti-diagonal coupling (P2 ↔ P5)
P2 creates; P5 gates. Together they prevent “factory spam” and enforce survivable promotion.

---

# P3 — Harmonic Hydra (INJECT) — DELIVER / Payload injection and recomposition
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P3_DELIVER_INJECT_HARMONIC_HYDRA_LADDER_8PART_V1_2026_01_28.md`

## Role (one sentence)
Deliver controlled effects into the environment with legible sequencing and reversible semantics.

## 3+1 anchor (mnemonic)
- Static: The First Sliver → recomposition/cascade: small inputs unfold into structured outputs
- Trigger: Harmonic Sliver → contact effects: deliver value by interacting with the surface
- Activated: Hibernation Sliver → deliberate retreat/rollback: pay to pull back
- Equipment: Blade of Selves → “forked delivery” under a disciplined copy rule (bounded parallelism)

## Meadows frame
- Stocks: event queue depth, state coherence, retry debt.
- Flows: schedule → dispatch → acknowledge → advance.
- $R_{throughput}$: clean FSM → fewer retries → higher throughput.
- $B_{backpressure}$: queue growth → throttle → queue shrink.
- Delays: propagation latency and ack latency.

## Invariants
- Actions must be idempotent or receipt-driven.
- Every dispatch must be attributable to a validated intent.

## Failure modes
- Unbounded fanout becomes fragility → tripwire on queue growth and duplicate effects.

## Anti-diagonal coupling (P3 ↔ P4)
P3 pushes effects; P4 applies contestation to keep the system honest.

---

# P4 — Red Regnant (DISRUPT) — DISRUPT / Red team suppression and antifragile correction
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P4_DISRUPT_DISRUPT_RED_REGNANT_LADDER_8PART_V1_2026_01_28.md`

## Role (one sentence)
Detect instability and reward hacking; apply suppression so learning stays within safety margins.

## 3+1 anchor (mnemonic)
- Static: Venom Sliver → default posture: make unsafe contact costly
- Trigger: Thorncaster Sliver → reflexive counterpressure on engagement
- Activated: Necrotic Sliver → paid-cost targeted excision (remove the corrupt component)
- Equipment: Blade of the Bloodchief → convert confirmed failures into hardening power

## Meadows frame
- Stocks: suppression budget, anomaly ledger, resilience margin.
- Flows: detect → damp → observe recovery.
- $B_{safety}$: drift → suppression → drift reduction.
- $R_{antifragile}$: postmortem → guardrail improvements → fewer incidents.
- Delays: detection delay dominates (you can’t suppress what you can’t see).

## Invariants
- Suppression must be policy-bound; avoid destabilizing over-correction.
- Tripwires must be deterministic enough to stop “AI theater.”

## Anti-diagonal coupling (P4 ↔ P3)
P4 makes P3 safe by forcing feedback and preventing silent runaway loops.

---

# P5 — Pyre Praetorian (IMMUNIZE) — DEFEND / Integrity and resurrection
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P5_DEFEND_IMMUNIZE_PYRE_PRAETORIAN_LADDER_8PART_V1_2026_01_28.md`

## Role (one sentence)
Gate promotion, quarantine taint, and resurrect from known-good so failures are survivable.

## 3+1 anchor (mnemonic)
- Static: Sliver Hivelord → invariants are hard to destroy (resilience posture)
- Trigger: Pulmonic Sliver → when things die, recovery triggers (bounce-back semantics)
- Activated: Basal Sliver → paid-cost resource conversion (power emergency maneuvers)
- Equipment: Sword of Light and Shadow → recover key assets while maintaining continuity

## Meadows frame
- Stocks: integrity score, quarantine volume, recovery playbooks.
- Flows: verify → quarantine → restore → re-verify.
- $B_{integrity}$: corruption → quarantine → integrity restored.
- $R_{hardening}$: incidents → new checks → fewer incidents.
- Delays: forensics and restore time.

## Invariants
- No promotion without passing deterministic checks.
- Quarantine must be reversible and auditable.

## Anti-diagonal coupling (P5 ↔ P2)
P5 prevents P2’s creativity from becoming unbounded mutation.

---

# P6 — Kraken Keeper (ASSIMILATE) — STORE / SSOT persistence and recall
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P6_STORE_ASSIMILATE_KRAKEN_KEEPER_LADDER_8PART_V1_2026_01_28.md`

## Role (one sentence)
Make truth durable: a single write-path SSOT that can rebuild everything else.

## 3+1 anchor (mnemonic)
- Static: Dregscape Sliver → default posture: rehydrate value from the graveyard
- Trigger: Lazotep Sliver → when attacked, persist (telemetry hardening)
- Activated: Homing Sliver → paid-cost retrieval: fetch the exact component you need
- Equipment: Sword of Fire and Ice → convert engagement into durable advantage (read/write power)

## Meadows frame
- Stocks: SSOT corpus, index quality, lineage integrity.
- Flows: ingest → embed/index → recall → rebuild derived views.
- $R_{memory}$: better recall → better ops → better capture.
- $B_{bloat}$: growth → pruning policies → stable performance.
- Delays: embedding latency, sync latency.

## Invariants
- SSOT is the only blessed write-path.
- Derived views are rebuildable; if they drift, they are discarded.

## Anti-diagonal coupling (P6 ↔ P1)
P6 operationalizes P1’s contracts by making validated artifacts retrievable.

---

# P7 — Spider Sovereign (NAVIGATE) — NAVIGATE / C2 orchestration and mission continuity
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P7_NAVIGATE_NAVIGATE_SPIDER_SOVEREIGN_LADDER_8PART_V1_2026_01_28.md`

## Role (one sentence)
Provide C2 legitimacy and coordination: pick the next action under constraints, and keep the mission thread coherent.

## 3+1 anchor (mnemonic)
- Static: Sliver Legion → global alignment posture (whole-system direction)
- Trigger: Regal Sliver → legitimacy signal triggers coordination (C2 authority cue)
- Activated: Sliver Overlord → deliberate routing: fetch the needed capability on demand
- Equipment: Lightning Greaves → reduce execution friction while preserving intent

## Meadows frame
- Stocks: mission graph, attention budget, plan stability.
- Flows: prioritize → route → measure → update.
- $R_{alignment}$: clear priorities → efficient execution → clearer priorities.
- $B_{overreach}$: scope creep → constraint → scope reduction.
- Delays: human review and planning cadence.

## Invariants
- P7 must not “invent truth”; it consumes SSOT + verified artifacts.
- Authority must be expressed as constraints and receipts, not vibes.

## Failure modes
- Over-optimization for speed (“just do more”) → tripwire on broken invariants and orphaned work.

## Anti-diagonal coupling (P7 ↔ P0)
P7 bounds what gets observed; P0 provides evidence to update navigation without hallucination.

---

# Meta Synthesis — The 8 Commanders as a safety-coupled lattice

## The four control couples (anti-diagonal)
- P0 ↔ P7: evidence ↔ bounded intent
- P1 ↔ P6: contracts ↔ durable memory
- P2 ↔ P5: creation ↔ gate/resurrection
- P3 ↔ P4: delivery ↔ suppression/contest

## One shared law
If it crosses a boundary, it must be schema-validated. If it becomes “truth,” it must be SSOT-written. If it becomes action, it must be gated and receipt-driven.

## Promotion checklist (what makes this doc promotable)
- Mapping table matches `contracts/hfo_mtg_port_card_mappings.v5.json` exactly.
- P7 trigger is **Regal Sliver**.
- The system is described as fail-closed, with explicit couplings and failure modes.

## Related syntheses
- Commander meta synthesis: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_LEGENDARY_COMMANDERS_META_SYNTHESIS_V1_2026_01_29.md`
- Meadows/JADC2 synthesis: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_JADC2_MOSAIC_MEADOWS_COMMANDERS_3_PLUS_1_SYNTHESIS_V1_2026_01_29.md`
