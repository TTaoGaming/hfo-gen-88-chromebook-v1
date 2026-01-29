<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->

---

medallion_layer: bronze
mutation_score_target: 0.88
hfo_scope: hive8
protocol: fractal_0123_microturn_powerwords
version: v1
created_utc: 2026-01-27
status: draft

---

# HFO — Fractal 0→1→2→3 Microturn (Powerwords / Domains) (Draft V1)

## Intent

Define the **canonical 4-step microcycle** that composes fractally across:

- a single port’s execution
- the 8-port baton chain
- multi-stage paired flows
- multi-turn runs

This microcycle is expressed using the existing OBSIDIAN powerwords, where ports P0–P3 correspond to the 0→1→2→3 domains.

## The microturn (0→1→2→3)

| Phase | Port | Powerword | Domain synonym set | Output (artifact class) |
|---:|---|---|---|---|
| 0 | P0 | OBSERVE | sense / context / ISR / tools | evidence bundle (tool receipts, snippets, constraints) |
| 1 | P1 | BRIDGE | connect / fuse / data-fabric / synthesize | interface + contract decisions |
| 2 | P2 | SHAPE | transform / materialize / normalize | durable baton artifact (strict schema) |
| 3 | P3 | INJECT | deliver / broadcast / dispatch | stigmergy signal (append-only event) |

### Crucial clarity

- **BRIDGE (P1)** is not “just summarization”; it’s the *schema-level and interface-level* binding step that makes later materialization deterministic.
- **SHAPE (P2)** is “make it real”: artifact writes, SSOT updates, and verifiable transformations.
- **INJECT (P3)** is “broadcast”: producing the *environmental* coordination signal (stigmergy) once the materialized object is strict-valid.

## Fractal composition rule

Treat **any completed artifact** as the next loop’s “environment”. Then:

- Within one port: `observe → bridge → shape → inject`
- Across ports: the baton artifact from one port becomes observed evidence for the next port.
- Across turns: stigmergy lines become observed context for later turns.

## Gating rule (anti-theater)

- “Inject” (stigmergy) is only allowed after **strict PASS** for the port-level artifact.
- Meta-level publish is only allowed after **global strict PASS**.

## Promotion path

- Candidate Gold ratification target: update the Gold vocabulary map with an explicit **0→1→2→3 microturn section**.
- Source of truth for the 8-port mapping remains the Gold OBSIDIAN vocabulary document.

## References

- Gold mapping (target to update): `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_OBSIDIAN_POWERWORDS_JADC2_DOMAIN_MAP_V1_2026_01_26.md`
