<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->
<!-- markdownlint-disable MD041 MD003 MD022 -->
---
medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
deliverable: legendary_commanders_3_plus_1_compendium_bluf_8x8_meta
version: v3
created_utc: 2026-01-29
provenance:
  identity_ssot: contracts/hfo_legendary_commanders_invariants.v1.json
  mapping_ssot: contracts/hfo_mtg_port_card_mappings.v5.json
  fail_closed_verifier: scripts/verify_hive8_mtg_card_mappings.mjs
  gold_sources:
    front_door: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_HIVE8_LEGENDARY_COMMANDERS_3_PLUS_1_MTG_JADC2_FRONT_DOOR_V1_2026_01_29.md
    ladder_docs:
      - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P0_SENSE_OBSERVE_LIDLESS_LEGION_LADDER_8PART_V1_2026_01_28.md
      - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P1_FUSE_BRIDGE_THE_WEB_WEAVER_LADDER_8PART_V1_2026_01_28.md
      - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P2_SHAPE_SHAPE_MIRROR_MAGUS_LADDER_8PART_V1_2026_01_28.md
      - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P3_DELIVER_INJECT_HARMONIC_HYDRA_LADDER_8PART_V1_2026_01_28.md
      - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P4_DISRUPT_DISRUPT_RED_REGNANT_LADDER_8PART_V1_2026_01_28.md
      - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P5_DEFEND_IMMUNIZE_PYRE_PRAETORIAN_LADDER_8PART_V1_2026_01_28.md
      - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P6_STORE_ASSIMILATE_KRAKEN_KEEPER_LADDER_8PART_V1_2026_01_28.md
      - hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P7_NAVIGATE_NAVIGATE_SPIDER_SOVEREIGN_LADDER_8PART_V1_2026_01_28.md
---

# HFO HIVE8 — Gen88 v5: Compendium (BLUF + 8×8 Ladder Parts + Meta Synthesis) (V3)

## BLUF (Executive Summary)
HFO HIVE8 is a safety-coupled 8-port lattice for agentic work.

- Each **Port (P0–P7)** is a commander-role with strict boundaries.
- Each role is anchored by a **Gen88 v5 “3+1” mnemonic** (3 slivers by tier + 1 equipment) to make intent memorable.
- The whole system is drift-resistant because **SSOT is law** (contracts) and Gold docs are derived views.

Authoritative SSOT:
- `contracts/hfo_legendary_commanders_invariants.v1.json`
- `contracts/hfo_mtg_port_card_mappings.v5.json`

Fail-closed verifier:
- `scripts/verify_hive8_mtg_card_mappings.mjs`

### Sanity check (Gen88 v5)
P7 trigger must be **Regal Sliver** (C2 legitimacy/coordination), not Brood.

---

## Audit goals (this revision)
This compendium is optimized for three traits:

1) **Simplicity**
  - One SSOT mapping table.
  - One 8-part ladder template repeated across ports.
  - Minimal “new doctrine” invented here; this file is a promotion-ready view.

2) **Extendability**
  - Versioned document (V3) with a stable table that can be verifier-checked.
  - Clear, mechanical steps for future Gen88 v6+ mapping bumps.

3) **Antifragile behavior**
  - Every port includes: a boundary rule, a failure mode, and a tripwire/guardrail.
  - Anti-diagonal coupling is treated as a safety mechanism, not decoration.

---

## Operating rules (apply to all ports)
- **SSOT is law**: identities and mappings are authoritative in `contracts/`.
- **Views are disposable**: if a Gold view drifts, it is corrected or regenerated (never treated as truth).
- **Fail-closed by default**: cross-boundary payloads either validate or they do not cross.
- **Single write-path**: “memory writes” go to the SSOT (sqlite_vec) write-path only.
- **Anti-diagonal safety**: every forward capability is paired with an opposing stabilizer (sum-to-7 coupling).

### Extension protocol (how to change safely)
If you want to change a 3+1 mapping:
1) Create a new mapping contract (e.g., `contracts/hfo_mtg_port_card_mappings.v6.json`).
2) Update `scripts/verify_hive8_mtg_card_mappings.mjs` to point at the new contract.
3) Update the mapping tables in the checked Gold docs (including this compendium).
4) Run `node scripts/verify_hive8_mtg_card_mappings.mjs` and require green before promotion.

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

# Commander Pages (8 parts each)
Each commander section follows the same 8-part ladder:
0) identity+3+1 (SSOT) → 1) analogies → 2) JADC2 tile → 3) Gherkin+2 Mermaid → 4) red-team → 5) invariants → 6) tags/metadata+Mermaid → 7) Meadows.

---

## P0 — THE LIDLESS LEGION / OBSERVE (SENSE)
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P0_SENSE_OBSERVE_LIDLESS_LEGION_LADDER_8PART_V1_2026_01_28.md`

### Part 0 — Galois lattice + identity + 3+1 cards (SSOT)
- port_id: P0 | powerword: OBSERVE | tile: SENSE | jadc2_domain: ISR (Observer)
- trigram: Kun (☷) Earth | octree bits: 000
- partner (sum-to-7): P7 | stage 0: Hindsight → Alignment
- 3+1: Cloudshredder / Synapse / Telekinetic / Infiltration Lens

### Part 1 — Plain-language analogies + cognitive scaffolding
- Static: acquire early evidence fast enough to steer.
- Trigger: “contact with reality” yields more context (information gain).
- Activated: pay attention to freeze variables (throttle/gate).
- Equipment: resistance reveals structure (high-signal diagnostics under friction).

### Part 2 — JADC2 MOSAIC tiles
- Produces: ranked evidence packets + anomaly candidates.
- Rejects: speculation without provenance/uncertainty.
- Handoff: P0 → P7 evidence; P7 → P0 priority/ignore constraints.

### Part 3 — Declarative Gherkin + 2 Mermaid diagrams
Gherkin invariant:
- Given an observation crosses a boundary
- Then it must be provenance-tagged, uncertainty-labeled, schema-valid, or fail-closed

~~~mermaid
flowchart TD
  S["Raw signals"] --> P0["P0 OBSERVE\ncalibrate + detect"]
  P7["P7 constraints"] --> P0
  P0 --> E["Evidence packets\n(rank + uncertainty)"]
  E --> P7
~~~

~~~mermaid
flowchart LR
  P0["P0"] <--> P7["P7"]
  P0 --> L["Stage 0: Hindsight → Alignment"]
~~~

### Part 4 — Devil’s advocate / red teaming weaknesses
- Reward-hack risk: maximize volume over quality.
- Drift risk: optionalize provenance fields.
- Latency risk: stale evidence steers into the past.

### Part 5 — Invariants list
- No cross-port evidence without provenance + uncertainty + schema validity.
- Preserve last known-good calibration snapshot.

### Part 6 — Key tags + metadata summaries + 1 Mermaid diagram
Tags: hive8, P0, OBSERVE, SENSE, ISR

~~~mermaid
sequenceDiagram
  participant P7 as P7
  participant P0 as P0
  P7-->>P0: priority + ignore list
  P0-->>P7: evidence packet
~~~

### Part 7 — Systems engineering (Donna Meadows vocabulary)
- Stocks: evidence reservoir, attention budget, sensor trust.
- Delays: sensor→evidence latency; truth→action latency.
- Leverage: information flows + rules for “contact events.”

---

## P1 — THE WEB WEAVER / BRIDGE (FUSE)
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P1_FUSE_BRIDGE_THE_WEB_WEAVER_LADDER_8PART_V1_2026_01_28.md`

### Part 0 — Galois lattice + identity + 3+1 cards (SSOT)
- port_id: P1 | powerword: BRIDGE | tile: FUSE | jadc2_domain: Fusion / Joint Data Fabric (Bridger)
- trigram: Gen (☶) Mountain | octree bits: 100
- partner: P6 | stage 1: Insight → Memory
- 3+1: Quick / Diffusion / Gemhide / Goldvein Pick

### Part 1 — Plain-language analogies + cognitive scaffolding
- Static: interop readiness (low-latency boundary-crossing, but disciplined).
- Trigger: friction against invalid/hostile interactions.
- Activated: convert capability into energy (resource enablement).
- Equipment: turn integration work into portable value (accounting).

### Part 2 — JADC2 MOSAIC tiles
- Produces: typed IR, validated payloads, contract-stamped artifacts.
- Rejects: untyped cross-port coupling.

### Part 3 — Declarative Gherkin + 2 Mermaid diagrams
Gherkin invariant:
- Given a payload crosses ports
- Then it must validate against a versioned schema or be rejected

~~~mermaid
flowchart TD
  P0["P0 evidence"] --> P1["P1 BRIDGE\nparse+validate"]
  P1 --> OK["Typed IR"]
  P1 --> NO["Fail-closed reject"]
~~~

~~~mermaid
flowchart LR
  P1["P1"] <--> P6["P6"]
  P1 --> L["Stage 1: Insight → Memory"]
~~~

### Part 4 — Devil’s advocate / red teaming weaknesses
- Over-permissive parsing becomes covert coupling.

### Part 5 — Invariants list
- Contracts are law; views are derived.

### Part 6 — Key tags + metadata + Mermaid
Tags: hive8, P1, BRIDGE, FUSE, Data Fabric

~~~mermaid
sequenceDiagram
  participant Up as Upstream
  participant P1 as P1
  participant Down as Downstream
  Up->>P1: raw payload
  P1-->>Down: typed payload (or reject)
~~~

### Part 7 — Meadows
- Leverage: rules + information flows (schemas).

---

## P2 — THE MIRROR MAGUS / SHAPE (SHAPE)
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P2_SHAPE_SHAPE_MIRROR_MAGUS_LADDER_8PART_V1_2026_01_28.md`

### Part 0 — Identity + 3+1 (SSOT)
- port_id: P2 | powerword: SHAPE | tile: SHAPE | jadc2_domain: Modeling / Digital Twin / COA Development (Shaper)
- trigram: Kan (☵) Water | octree bits: 010
- partner: P5 | stage 2: Validated Foresight → Gate
- 3+1: Mirror Entity / Hatchery / Sliver Queen / Illusionist's Bracers

### Part 1 — Analogies
- Static: one substrate, many candidate forms.
- Trigger: validated conditions create more candidate capacity.
- Activated: pay to instantiate.
- Equipment: copy activated shaping (amplify deliberate transformation).

### Part 2 — JADC2
- Produces: admissible shapes (cursor frames, bounded dynamics, twins).
- Rejects: unbounded geometry/physics claims.

### Part 3 — Gherkin + Mermaid
Invariant:
- Given a SHAPE payload is produced
- Then it must conform to SHAPE-layer formats (Touch2D / PointerEvent-shape) or fail-closed

~~~mermaid
flowchart TD
  Raw["Raw coords"] --> P2["P2 SHAPE\nnormalize + constrain"]
  P2 --> Out["Touch2D / pointer-shaped"]
  P2 --> Guard["Bounds + constraints"]
~~~

~~~mermaid
flowchart LR
  P2["P2"] <--> P5["P5"]
  P2 --> L["Stage 2: Validated Foresight → Gate"]
~~~

### Part 4 — Red team
- Failure: too many candidates without selection pressure.

### Part 5 — Invariants
- SHAPE outputs must be stable, bounded, and typed.

### Part 6 — Tags/metadata + Mermaid
Tags: hive8, P2, SHAPE, Digital Twin

~~~mermaid
sequenceDiagram
  participant P2 as P2
  participant P3 as P3
  P2-->>P3: normalized SHAPE payload
~~~

### Part 7 — Meadows
- Leverage: tune delays (timesteps) and bounds to prevent oscillation.

---

## P3 — HARMONIC HYDRA / INJECT (DELIVER)
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P3_DELIVER_INJECT_HARMONIC_HYDRA_LADDER_8PART_V1_2026_01_28.md`

### Part 0 — Identity + 3+1 (SSOT)
- port_id: P3 | powerword: INJECT | tile: DELIVER | jadc2_domain: Effect Delivery / Precision Strike (Injector)
- trigram: Xun (☴) Wind | octree bits: 110
- partner: P4 | stage 3: Evolution → Feedback
- 3+1: The First / Harmonic / Hibernation / Blade of Selves

### Part 1 — Analogies
- Static: controlled cascade/recomposition.
- Trigger: contact delivers effect.
- Activated: pay to retreat/rollback.
- Equipment: bounded forked delivery.

### Part 2 — JADC2
- Produces: dispatched effects with receipts.
- Rejects: untraceable actions.

### Part 3 — Gherkin + Mermaid
Invariant:
- Given an effect is dispatched
- Then it must be receipt-driven/idempotent and linked to validated intent

~~~mermaid
flowchart TD
  P7["P7 intent"] --> P3["P3 INJECT\ndispatch"]
  P3 --> Env["Target substrate"]
  P3 --> Receipt["Receipts"]
~~~

~~~mermaid
flowchart LR
  P3["P3"] <--> P4["P4"]
  P3 --> L["Stage 3: Evolution → Feedback"]
~~~

### Part 4 — Red team
- Fanout without bounds becomes fragility.

### Part 5 — Invariants
- No action without provenance, schema, and receipt.

### Part 6 — Tags/metadata + Mermaid
Tags: hive8, P3, INJECT, DELIVER

~~~mermaid
sequenceDiagram
  participant P3 as P3
  participant P4 as P4
  P3->>P4: effect trace
  P4-->>P3: suppression/backoff
~~~

### Part 7 — Meadows
- Leverage: backpressure + delays (ack latency) to avoid overshoot.

---

## P4 — RED REGNANT / DISRUPT (DISRUPT)
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P4_DISRUPT_DISRUPT_RED_REGNANT_LADDER_8PART_V1_2026_01_28.md`

### Part 0 — Identity + 3+1 (SSOT)
- port_id: P4 | powerword: DISRUPT | tile: DISRUPT | jadc2_domain: Multi-Domain Operations / EW / Cyber (Disruptor)
- trigram: Zhen (☳) Thunder | octree bits: 001
- partner: P3 | stage 3
- 3+1: Venom / Thorncaster / Necrotic / Blade of the Bloodchief

### Part 1 — Analogies
- Static: unsafe contact is costly.
- Trigger: reflexive counterpressure.
- Activated: paid excision (remove corrupt component).
- Equipment: convert confirmed failures into hardening power.

### Part 2 — JADC2
- Produces: suppression signals + drift detection.

### Part 3 — Gherkin + Mermaid
Invariant:
- Given instability is detected
- Then suppression must be policy-bound and observable

~~~mermaid
flowchart TD
  Obs["Signals"] --> P4["P4 DISRUPT\ndetect + suppress"]
  P4 --> Policy["Policy"]
  P4 --> Guard["Tripwires"]
~~~

~~~mermaid
flowchart LR
  P4["P4"] <--> P3["P3"]
  P4 --> L["Stage 3"]
~~~

### Part 4 — Red team
- Over-suppression can stall the lattice.

### Part 5 — Invariants
- Tripwires are deterministic enough to stop theater.

### Part 6 — Tags/metadata + Mermaid
Tags: hive8, P4, DISRUPT

~~~mermaid
sequenceDiagram
  participant P4 as P4
  participant P5 as P5
  P4-->>P5: anomaly candidates
  P5-->>P4: quarantine verdict
~~~

### Part 7 — Meadows
- Leverage: shorten detection delay; tune suppression budget.

---

## P5 — PYRE PRAETORIAN / IMMUNIZE (DEFEND)
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P5_DEFEND_IMMUNIZE_PYRE_PRAETORIAN_LADDER_8PART_V1_2026_01_28.md`

### Part 0 — Identity + 3+1 (SSOT)
- port_id: P5 | powerword: IMMUNIZE | tile: DEFEND | jadc2_domain: Cyber Defense / Zero Trust / Resurrection (Immunizer)
- trigram: Li (☲) Fire | octree bits: 101
- partner: P2 | stage 2
- 3+1: Hivelord / Pulmonic / Basal / Sword of Light and Shadow

### Part 1 — Analogies
- Static: invariants resist destruction.
- Trigger: recovery triggers on failure.
- Activated: paid resource conversion.
- Equipment: recover key assets while maintaining continuity.

### Part 2 — JADC2
- Produces: gate decisions, quarantine, resurrection.

### Part 3 — Gherkin + Mermaid
Invariant:
- Given an artifact is promoted
- Then it must pass deterministic integrity checks

~~~mermaid
flowchart TD
  Cand["Candidate"] --> P5["P5 IMMUNIZE\nverify"]
  P5 --> Pass["Promote"]
  P5 --> Fail["Quarantine/restore"]
~~~

~~~mermaid
flowchart LR
  P5["P5"] <--> P2["P2"]
  P5 --> L["Stage 2"]
~~~

### Part 4 — Red team
- Gate bypass is the core exploit.

### Part 5 — Invariants
- Fail-closed on mismatch.

### Part 6 — Tags/metadata + Mermaid
Tags: hive8, P5, IMMUNIZE

~~~mermaid
sequenceDiagram
  participant P5 as P5
  participant P6 as P6
  P5-->>P6: approved artifact
  P6-->>P5: recall proof
~~~

### Part 7 — Meadows
- Leverage: rules (gates) > throughput.

---

## P6 — KRAKEN KEEPER / ASSIMILATE (STORE)
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P6_STORE_ASSIMILATE_KRAKEN_KEEPER_LADDER_8PART_V1_2026_01_28.md`

### Part 0 — Identity + 3+1 (SSOT)
- port_id: P6 | powerword: ASSIMILATE | tile: STORE | jadc2_domain: Post-Mission Analysis / Data Repository (Assimilator)
- trigram: Dui (☱) Lake | octree bits: 011
- partner: P1 | stage 1
- 3+1: Dregscape / Lazotep / Homing / Sword of Fire and Ice

### Part 1 — Analogies
- Static: rehydrate value.
- Trigger: persist under attack.
- Activated: fetch exact component.
- Equipment: convert engagement into durable advantage.

### Part 2 — JADC2
- Produces: SSOT truth, recall, rebuildable views.

### Part 3 — Gherkin + Mermaid
Invariant:
- Given a memory write occurs
- Then it must go through the SSOT write-path

~~~mermaid
flowchart TD
  Art["Artifacts"] --> P6["P6 ASSIMILATE\nwrite+index"]
  P6 --> SSOT["SSOT (sqlite_vec)"]
  SSOT --> Recall["Recall"]
~~~

~~~mermaid
flowchart LR
  P6["P6"] <--> P1["P1"]
  P6 --> L["Stage 1"]
~~~

### Part 4 — Red team
- Multiple write-paths cause truth drift.

### Part 5 — Invariants
- SSOT is the only write-path.

### Part 6 — Tags/metadata + Mermaid
Tags: hive8, P6, ASSIMILATE

~~~mermaid
sequenceDiagram
  participant P6 as P6
  participant P7 as P7
  P6-->>P7: recall results
  P7-->>P6: query focus
~~~

### Part 7 — Meadows
- Leverage: information flows + pruning policies.

---

## P7 — SPIDER SOVEREIGN / NAVIGATE (NAVIGATE)
Deep dive ladder: `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_P7_NAVIGATE_NAVIGATE_SPIDER_SOVEREIGN_LADDER_8PART_V1_2026_01_28.md`

### Part 0 — Identity + 3+1 (SSOT)
- port_id: P7 | powerword: NAVIGATE | tile: NAVIGATE | jadc2_domain: Battle Management Command and Control (Navigator)
- trigram: Qian (☰) Heaven | octree bits: 111
- partner: P0 | stage 0
- 3+1: Sliver Legion / Regal Sliver / Sliver Overlord / Lightning Greaves

### Part 1 — Analogies
- Static: global alignment posture.
- Trigger: legitimacy signal triggers coordination (C2 cue).
- Activated: deliberate routing/fetch capability.
- Equipment: reduce execution friction without changing intent.

### Part 2 — JADC2
- Produces: bounded intent, priorities, plan constraints.
- Rejects: invented truth.

### Part 3 — Gherkin + Mermaid
Invariant:
- Given P7 selects work
- Then it must cite SSOT + receipts and remain within constraints

~~~mermaid
flowchart TD
  SSOT["SSOT"] --> P7["P7 NAVIGATE\nprioritize + route"]
  P7 --> Work["Next actions"]
  Work --> P6["P6 receipts"]
~~~

~~~mermaid
flowchart LR
  P7["P7"] <--> P0["P0"]
  P7 --> L["Stage 0"]
~~~

### Part 4 — Red team
- Speed-over-truth causes orphaned work.

### Part 5 — Invariants
- No truth invention; cite SSOT.

### Part 6 — Tags/metadata + Mermaid
Tags: hive8, P7, NAVIGATE

~~~mermaid
sequenceDiagram
  participant P7 as P7
  participant P0 as P0
  P7-->>P0: priorities
  P0-->>P7: calibrated evidence
~~~

### Part 7 — Meadows
- Leverage: paradigms (mission thread) + rules (constraints) + info flows.

---

# Meta Synthesis (1 section)

## The lattice is the safety mechanism
The anti-diagonal pairing (sum-to-7) creates four control couples:
- P0↔P7 evidence↔intent
- P1↔P6 contract↔memory
- P2↔P5 creation↔gate
- P3↔P4 delivery↔suppression

## Unifying law
- If it crosses a boundary, it must be schema-validated.
- If it becomes truth, it must be SSOT-written.
- If it becomes action, it must be gated + receipt-driven.

## Promotion checklist
- Mapping table matches `contracts/hfo_mtg_port_card_mappings.v5.json`.
- P7 trigger is **Regal Sliver**.
- Each commander is expressed in the full 8-part ladder form.
