---
schema_id: hfo.hive8.compendium
schema_version: 3
version: v7
status: draft

doc_id: hfo.hive8.gen88.v5.legendary_commanders_3_plus_1_compendium_bluf_8x8_meta

dates:
  created_utc: "2026-01-29"
  updated_utc: "2026-01-29"

medallion:
  layer: bronze
  mutation_score: 0
  hive: V

portability:
  goal: "single-file markdown (portable)"
  rule: "No external links in body; any links live only in 'Extra References'."

intent:
  primary:
    - "Portable, self-contained reference for HFO HIVE8 legendary commanders and ports (Gen88)."
    - "A single file you can export/share without breaking meaning or losing the core system."
  operational:
    - "Still provides executable gate commands (for repo environments) but does not require them to understand the doctrine."

ssot_snapshot:
  identity_invariants:
    schema: "hfo.legendary_commanders.invariants.v1"
    binary_rule: "port_index == binary (P0..P7 == 000..111)"
  mapping_contract:
    schema: "hfo.mtg.port_card_mappings.v5"
    p7_trigger_note: "Regal Sliver"

ssot:
  identity_invariants: contracts/hfo_legendary_commanders_invariants.v1.json
  mapping_contract: contracts/hfo_mtg_port_card_mappings.v5.json

gates:
  - id: compendium_frontmatter
    command: "node scripts/verify_hive8_compendium_frontmatter.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: compendium_portable_links
    command: "node scripts/verify_hive8_compendium_portable_links.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: contracts_schema
    command: "npm run test:contracts"
    pass_condition: "Exits 0"
  - id: mapping_table_drift
    command: "node scripts/verify_hive8_mtg_card_mappings.mjs"
    pass_condition: "Prints OK: and exits 0"
  - id: mermaid_syntax
    command: "npm run mermaid:lint"
    pass_condition: "Exits 0"

operational_assumptions:
  - "Cross-port payloads validate or they do not cross (fail-closed)."
  - "Memory writes use the SSOT write-path only."
---

# HFO HIVE8 GEN88 — Legendary Commanders 3+1 Compendium (V7, Portable)

This document is intentionally self-contained.

It is designed to be a better CDD/BDD/TDD/DevOps reference by being:
- CDD: contracts are enumerated as concepts and enforcement boundaries.
- BDD: each port has explicit behaviors and failure modes.
- TDD: behaviors are mapped to executable checks (gates) and known gaps.
- DevOps: a runnable gate index exists, but doctrine is understandable without running anything.

## Prime directives
- SSOT is law (identities/mappings are authoritative).
- Views are disposable (this document is a view and can be regenerated).
- Fail-closed by default (if it crosses a boundary, it validates).
- Single write-path for memory writes (SSOT only).

## Canonical identity invariants (binary)
Binary is canonicalized to port index ordering: P0..P7 == 000..111.

| Port | Powerword | Commander | Trigram | Binary |
| ---- | --------- | --------- | ------- | ------ |
| P0 | OBSERVE | THE LIDLESS LEGION | Kun (☷) Earth | 000 |
| P1 | BRIDGE | THE WEB WEAVER | Gen (☶) Mountain | 001 |
| P2 | SHAPE | THE MIRROR MAGUS | Kan (☵) Water | 010 |
| P3 | INJECT | HARMONIC HYDRA | Xun (☴) Wind | 011 |
| P4 | DISRUPT | RED REGNANT | Zhen (☳) Thunder | 100 |
| P5 | IMMUNIZE | PYRE PRAETORIAN | Li (☲) Fire | 101 |
| P6 | ASSIMILATE | KRAKEN KEEPER | Dui (☱) Lake | 110 |
| P7 | NAVIGATE | SPIDER SOVEREIGN | Qian (☰) Heaven | 111 |

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

## Executable Gates Index (DevOps/TDD)
These commands are optional. The doctrine remains valid without running them.

| Gate | What it protects | Command | Pass condition |
| ---- | ---------------- | ------- | -------------- |
| Compendium header gate | Machine-parseability + required YAML keys | node scripts/verify_hive8_compendium_frontmatter.mjs | Prints OK: and exits 0 |
| Portability gate | No external links in body | node scripts/verify_hive8_compendium_portable_links.mjs | Prints OK: and exits 0 |
| Contracts schema gate | Contracts parse + invariants stay consistent | npm run test:contracts | Exits 0 |
| Mapping-table drift gate | Mapping table matches SSOT across checked docs | node scripts/verify_hive8_mtg_card_mappings.mjs | Prints OK: and exits 0 |
| Mermaid lint gate | Diagrams don’t silently rot | npm run mermaid:lint | Exits 0 |

## Contract inventory (CDD, conceptual)
This is a portable inventory: it describes what must exist and what it means.

| Contract concept | Purpose | Producer(s) | Consumer(s) | Fail behavior |
| ---------------- | ------- | ----------- | ----------- | ------------- |
| Identity invariants | Canonical names, domains, trigram, binary | Operator / doctrine | All ports + docs | Hard fail on uniqueness/bit mismatch |
| 3+1 mapping contract | Commander-to-cards mapping SSOT | Operator / doctrine | Gold docs + verifier | Hard fail on drift |
| Blackboard cloudevent | Cross-port stigmergy events | Any port | Any port | Reject invalid event shape |
| Tripwire events | Safety/guardrail triggers | P4/P5 | P7/P6 | Reject invalid event shape |
| Flight/phase receipts | Proof-of-work & continuity | Tooling | Tooling | Reject missing required fields |
| Exemplar event | Reusable exemplars for learning | P6 | P0/P7/P2 | Reject invalid sha256 |

## Enforcement map (CDD → DevOps)

| Boundary | Enforced by | Evidence |
| -------- | ----------- | -------- |
| Gold docs ↔ mapping SSOT | mapping-table drift gate | Verifier OK output + receipts |
| Contracts ↔ parsing/uniqueness | contracts schema gate | Test output |
| Document portability | portability gate | Verifier OK output |

## BDD → Gate traceability (BDD/TDD)

| Port | Core behavior invariant (BDD) | Gate(s) that enforce it today | Gap (what to add next) |
| ---- | ----------------------------- | ----------------------------- | ---------------------- |
| P0 | No cross-port evidence without schema + provenance | contracts schema gate + receipts | Add explicit evidence packet schema + tests |
| P1 | No cross-port bridge without strict schema validation | contracts schema gate + receipts | Add adapter harness tests + fuzzing |
| P2 | Shape payloads normalized before injection | contracts schema gate + receipts | Add golden fixtures for pointer/touch2d |
| P3 | Inject only validated, provenance-tagged effects | contracts schema gate + receipts | Add injection harness tests |
| P4 | Disruption is auditable and reversible | contracts schema gate + receipts | Add tripwire test suite (no silent damage) |
| P5 | Defenses are fail-closed; drift is detected before promotion | mapping drift gate + contracts schema gate | Add quarantine/resurrection playbook tests |
| P6 | Memory writes use the single blessed SSOT path | operational status update + receipts | Add a detector gate for JSONL append attempts |
| P7 | Navigation decisions are traceable to evidence + contracts | contracts schema gate + receipts | Add decision record schema + replay gate |

## Commander pages (portable deep dives)
The V7 portable rule means these pages are self-contained doctrine: no file links, no external dependencies.

### Shared myth-language (for machine doctrine)
This system is a role-based Galois lattice expressed as a mythic narrative lens.

Core promise:
- Every agent performs a RITUAL.
- Every action follows a PROTOCOL.
- Every boundary is guarded by a GATE.
- Every accepted crossing is BLESSED (validated, provenance-tagged, replayable).

At the highest level, the swarm loops through four divine phases:
- DIVINE HINDSIGHT: after-action truth extraction (what actually happened).
- DIVINE INSIGHT: present-tense world model coherence (what is happening).
- DIVINE VALIDATED_FORESIGHT: evidence-backed intent (what we will do next).
- DIVINE EVOLUTION: controlled change of doctrine + code (how we improve safely).

Operationally, these four phases are implemented by the eight commanders as a continuous cycle.

### P0 — THE LIDLESS LEGION / OBSERVE (ISR under contest)

Mission
- Convert raw signals into calibrated evidence packets (with uncertainty and provenance).
- Refuse “confidence theater”: if it cannot be justified, it cannot cross.

Doctrine (DIVINE INSIGHT)
- P0 is the swarm’s eyes, but also its discipline: it names what is unknown.
- “Coverage” is not truth; evidence is truth only after calibration + schema.

Protocol
1) Capture: ingest raw observations (sensors/logs/transcripts/frames).
2) Normalize: standardize time, coordinate frames, units, and encoding.
3) Calibrate: attach uncertainty, quality, freshness, and adversarial risk.
4) Bind: attach provenance (source, transform chain, hashes where possible).
5) Bless: emit evidence only if it validates (fail-closed).

Primary artifacts (portable description)
- Evidence packet: a typed record that can be replayed and re-evaluated.
- Freshness contract: evidence includes time windows + decay semantics.

Gates (what must be true before P0 output is trusted)
- Schema validity: evidence conforms to a declared shape.
- Provenance completeness: source + transform chain present.
- Staleness bound: evidence declares its own expiry or confidence decay.

Failure modes (the sins of the Lidless)
- Noise masquerading as signal (false positives).
- Stale evidence steering navigation (frozen “truth”).
- Missing uncertainty (binary certainty in an analog world).

Blessing criteria
- Evidence is accepted only if: validated + provenance-tagged + uncertainty-aware + freshness-scoped.

Scaling note (8^1 → 8^8)
- 8^1: one P0 swarm produces a single coherent evidence stream.
- 8^8: P0 forks per commander-context (P0↔P7, P0↔P4, etc.), producing context-specific evidence views while preserving a shared SSOT identity.

### P1 — THE WEB WEAVER / BRIDGE (shared data fabric)

Mission
- Bridge heterogeneous systems into one typed stream without losing meaning.
- Make interoperability boring by making it explicit.

Doctrine (DIVINE INSIGHT)
- The Web Weaver is not a “converter”; it is a covenant of boundaries.
- Every adapter is a confession: what it assumes, what it drops, what it preserves.

Protocol
1) Identify boundary: source domain → contract domain.
2) Decode: read input without coercion.
3) Validate: strict schema validation; reject on mismatch.
4) Transform: explicit mapping (no silent defaults).
5) Emit: produce a typed event stream (Cloudevent-style stigmergy where applicable).

Gates
- No “helpful coercion”: if the source does not match, it is rejected.
- Adapter explicitness: every transform has declared rules.
- Drift detection: schema changes are surfaced as failures, not “best effort”.

Failure modes
- Silent meaning loss (“it parsed, so it must be fine”).
- Schema drift hidden behind compatibility shims.
- Implicit joins that create phantom correlations.

Blessing criteria
- Bridge output is blessed only if it is strictly validated and transform rules are explicit.

Scaling note (8^1 → 8^8)
- 8^1: one bridge fabric for the platform.
- 8^8: per-commander adapter lanes (e.g., P4 gets a “red-team safe” lane, P6 gets a “memory-grade” lane), still converging on shared contract shapes.

### P2 — THE MIRROR MAGUS / SHAPE (creation, digital twin, spike factory)

Mission
- Create and maintain the world-model substrate: normalized geometry, state, and affordances.
- Turn evidence into a coherent “mirror” that downstream ports can act upon.

Doctrine (DIVINE INSIGHT → DIVINE VALIDATED_FORESIGHT)
- P2 is where the swarm becomes spatially literate.
- A digital twin is not an image; it is a contract for action.

Protocol
1) Ingest: accept evidence packets only when blessed.
2) Align: unify coordinate frames, timestamps, and identities.
3) Compose: build a canonical state representation (twin/state graph).
4) Predict: generate candidate futures (scenarios) as hypotheses.
5) Package: export shaped payloads for P3 (effects) and P7 (planning).

Gates
- Coordinate invariants: no mixing frames without declared transforms.
- Identity invariants: entities remain consistent across time.
- Determinism envelope: same inputs should yield same shaped outputs (within declared stochastic bounds).

Failure modes
- Coordinate confusion (left-handed/right-handed, unit mismatch).
- Time skew (phantom motion).
- Shape drift (event schemas change invisibly).

Blessing criteria
- Shaped state is blessed when it is coherent, identity-consistent, and transform-traceable.

Scaling note (8^1 → 8^8)
- 8^1: one shared twin for the mission.
- 8^8: “twin shards” per domain + per commander-context (e.g., a P4 adversarial twin, a P5 integrity twin) with reconciliation through contracts and receipts.

### P3 — HARMONIC HYDRA / INJECT (delivery, payload injection, recomposition)

Mission
- Deliver effects into target substrates (UI, actuators, services, workflows) only when validated.
- Recompose safely: transform intent into action without losing traceability.

Doctrine (DIVINE VALIDATED_FORESIGHT)
- P3 is the mouth of the swarm: it speaks into reality.
- The Hydra is harmonic only when all heads agree on provenance.

Protocol
1) Receive: accept shaped payloads with provenance.
2) Validate: ensure contracts match target boundary expectations.
3) Stage: prepare a reversible plan (dry-run or sandbox when possible).
4) Inject: apply effects with idempotency and trace hooks.
5) Record: emit receipts + replay tokens.

Gates
- Provenance gate: no payload without lineage.
- Replay gate: side-effects must be replayable or explicitly marked irreducible.
- Idempotency gate: repeated execution must be safe or explicitly guarded.

Failure modes
- Injection without provenance (untraceable behavior).
- Unreplayable side-effects (cannot audit or debug).
- “Action drift” (payload meaning changes at injection time).

Blessing criteria
- An injection is blessed only when it is validated, traceable, and produces receipts.

Scaling note (8^1 → 8^8)
- 8^1: one injection lane guarded by gates.
- 8^8: multiple heads (one per commander-context) propose effects; a harmonizer (often P7/P5 jointly) selects which head may speak.

### P4 — RED REGNANT / DISRUPT (red team, contestation, destructive probing)

Mission
- Stress the system to reveal weakness, false certainty, and brittle assumptions.
- Force truth by adversarial contact.

Doctrine (DIVINE INSIGHT → DIVINE EVOLUTION)
- P4 is the necessary adversary: it prevents sacred lies.
- Disruption is not chaos; it is controlled falsification.

Protocol
1) Target selection: choose hypotheses and weak points (based on evidence).
2) Probe design: define what failure would look like.
3) Execute: run disruption within defined blast radius.
4) Tripwire: emit explicit tripwire events for risky conditions.
5) Report: produce audit artifacts that can be turned into P5 defenses.

Gates
- Audit gate: every disruption is logged and attributable.
- Reversibility gate: disruption must be reversible or quarantine-scoped.
- Blast-radius gate: declared limits are enforced.

Failure modes
- Silent damage (undetected corruption).
- Un-auditable disruption (“it happened but nobody knows why”).
- Endless red-teaming without conversion into defenses.

Blessing criteria
- A disruption is blessed when it is bounded, audited, and yields actionable defects/guards.

Scaling note (8^1 → 8^8)
- 8^1: one adversarial swarm tests the whole platform.
- 8^8: adversary cells per commander, producing domain-specific probes; P5 arbitrates which probes are allowed in production.

### P5 — PYRE PRAETORIAN / IMMUNIZE (defense-in-depth, integrity, recovery)

Mission
- Guard the gates: integrity checks, quarantine, resurrection, drift detection.
- Convert P4 findings into durable defenses.

Doctrine (DIVINE EVOLUTION)
- P5 is the doctrine’s immune system: it remembers attacks as protections.
- The Pyre burns away unsafe states to preserve continuity.

Protocol
1) Detect: watch for drift, corruption, and policy violations.
2) Quarantine: isolate unsafe artifacts/events.
3) Validate: run gates and contracts on candidates.
4) Resurrect: restore known-good states (rollback, replay, rebuild).
5) Promote: allow changes only after proof-of-work.

Gates
- Fail-closed boundary gate: absence of proof implies denial.
- Drift gate: mappings/contracts must not change silently.
- Resurrection gate: a recovery path must exist for critical workflows.

Failure modes
- Permissive defaults (“let it through for now”).
- Bypassed gates (shadow pipelines).
- Quarantine that never resolves (operational deadlocks).

Blessing criteria
- A promotion is blessed when it passes gates and has a recovery plan.

Scaling note (8^1 → 8^8)
- 8^1: one sentinel guarding all boundaries.
- 8^8: distributed immune system with local quarantines; a global invariant set keeps them consistent.

### P6 — KRAKEN KEEPER / ASSIMILATE (AAR, memory, exemplars)

Mission
- Perform after-action review (AAR) and distill exemplars.
- Consolidate truths into the single blessed memory write-path (SSOT).

Doctrine (DIVINE HINDSIGHT)
- P6 is where the swarm learns without hallucinating.
- “Summary” is not memory unless it is source-grounded and provenance-tagged.

Protocol
1) Collect: gather receipts, events, evidence, and outcomes.
2) Reconcile: resolve conflicts, deduplicate, and time-order.
3) Distill: extract exemplars (what worked, what failed, why).
4) Store: write to SSOT only.
5) Publish: emit replay manifests and learning signals back to P7/P2/P5.

Gates
- Single write-path gate: memory writes must go to SSOT.
- Provenance gate: every distilled claim traces to sources.
- Replay gate: learning is tied to reproducible runs.

Failure modes
- Fragmented write paths (multiple “truth stores”).
- Unverifiable summaries (orphaned claims).
- Learning loops that mutate doctrine without gates.

Blessing criteria
- A memory is blessed when it is SSOT-written, provenance-grounded, and replay-referenced.

Scaling note (8^1 → 8^8)
- 8^1: one keeper consolidates the mission journal.
- 8^8: per-commander keepers distill local exemplars; a global keeper reconciles and updates doctrine with controlled evolution.

### P7 — SPIDER SOVEREIGN / NAVIGATE (C2, orchestration, hunt heuristics)

Mission
- Orchestrate: plan, prune, steer, and allocate attention.
- Convert evidence and contracts into decisions that can be explained and replayed.

Doctrine (DIVINE VALIDATED_FORESIGHT)
- P7 is the weaver of intent: it chooses which futures to attempt.
- The Sovereign does not “guess”; it validates and then commits.

Protocol
1) Receive: accept blessed evidence (P0) and shaped state (P2).
2) Model: evaluate hypotheses and risks (including adversarial risk).
3) Decide: choose an intent with an explicit rationale.
4) Dispatch: send tasks to ports with contract-bound payloads.
5) Verify: require receipts; adjust based on outcomes.

Gates
- Traceability gate: decisions must link to evidence and constraints (conceptually, not as hyperlinks).
- Budget gate: time/cost/concurrency limits are explicit.
- Anti-reward-hacking gate: proxy metrics cannot override invariants.

Failure modes
- Proxy optimization (reward hacking).
- Non-traceable decisions (cannot debug).
- Thrash (too many replans without learning).

Blessing criteria
- A plan is blessed when it is evidence-backed, contract-bound, and receipt-verifiable.

Scaling note (8^1 → 8^8)
- 8^1: one sovereign coordinates eight commander swarms.
- 8^8: sovereigns exist at multiple levels (commander-of-commanders), with strict arbitration rules to avoid circular control.

## Synergy meta synthesis (JADC2 mosaic mission engineering)

### The mosaic as a closed loop
The platform is a continuous mission-engineering loop:
- OBSERVE (P0) produces calibrated evidence.
- BRIDGE (P1) makes evidence interoperable.
- SHAPE (P2) composes a coherent world model.
- INJECT (P3) applies validated effects.
- DISRUPT (P4) adversarially tests assumptions.
- IMMUNIZE (P5) hardens boundaries and restores integrity.
- ASSIMILATE (P6) extracts hindsight and stores SSOT truth.
- NAVIGATE (P7) chooses intents with validated foresight.

This is the JADC2 mosaic: many heterogeneous tiles, one coherent doctrine.

### The Galois lattice (role-based partial order)
Think of “roles” as constraints, not personalities.

One useful partial order for safe cross-port composition:
- Evidence (P0) ≤ Interop (P1) ≤ World model (P2) '≤' Intent/Plan (P7)
- Intent/Plan (P7) ≤ Effect (P3)
- Effect (P3) ≤ Receipt/Trace (P6)
- Receipt/Trace (P6) ≤ Defense updates (P5)
- Defense updates (P5) ≤ New probes (P4)

The order is enforced by gates: you may not “skip upward” without proof.

### Ritual, protocol, blessing (the swarm’s religion-as-software)
RITUAL (meta): Preflight → Payload → Postflight → Payoff.

PROTOCOL (local): each commander’s protocol transforms inputs into blessed outputs.

GATES (formal): contracts + drift checks + portability + receipts.

BLESSING (semantic): a crossing is blessed when it is validated, provenance-tagged, replayable, and bounded.

### Concurrency envelope (8^1 now, 8^8 later)
8^1 (today):
- Eight commander swarms operate concurrently.
- Coordination occurs via strict contracts and stigmergy events.
- P7 arbitrates, P5 guards, P6 remembers.

8^8 (future doctrine):
- Each commander spawns eight sub-commander cells (a full matrix of perspectives).
- This creates a “mosaic-of-mosaics”: every domain is evaluated through every other domain’s lens.
- Requirements to be safe:
  - Stronger arbitration (avoid circular control).
  - Hard budgets (compute, time, blast radius).
  - Replay-first instrumentation (no untraceable branches).
  - Explicit conflict resolution rules (which invariants win).

### Coupling rules (how commanders may touch each other)
- P0 outputs are read-only evidence; they do not command.
- P7 commands, but cannot fabricate evidence.
- P3 acts, but cannot redefine doctrine.
- P4 attacks, but cannot bypass P5.
- P5 blocks, but must provide a path to recovery.
- P6 remembers, but cannot invent sources.

### What “complete platform” means
The platform is “complete” when:
- Every boundary has a contract.
- Every contract has a gate.
- Every gate yields a receipt.
- Every receipt can be replayed.
- Every replay produces hindsight.
- Hindsight evolves doctrine only through blessed change.

## Extra References (non-portable)
This section may contain links/paths for repo users; the body above must remain link-free.
