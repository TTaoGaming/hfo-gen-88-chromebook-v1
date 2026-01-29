<!-- Medallion: Silver | Mutation: 0% | HIVE: V -->
---

medallion_layer: silver
mutation_score_target: 0.88
hfo_scope: hive8
protocol: meta_promoted_deliverables_contract
version: v1
created_utc: 2026-01-27
---

# HFO HIVE8 — Meta-Promoted Deliverables Contract (V1)

## Objective

Freeze the **meta-promoted deliverables** contract so a single HIVE8 turn is auditable:

- 8 port artifacts (each publishes **8^1** items)
- 1 meta synthesis artifact (promotes a strict subset)
- 1 stigmergy signal (gated on strict PASS)

This contract is designed for Mosaic Warfare / Galois Lattice invariants and powers-of-two readability.

## Operator Phrasing (Exact)

- “ports 0-3 are all scatter patterns and ports 4-7 are gather patterns”
- “ports 0-3 always gives 8^1 in their artifact and presents to the user 2^1 answers”
- “ports 4-7 it should always be 8^1 in their artifact and 8^0 in the meta synthesis”
- “Port 0 … two observations … then … Port 7 … one … Port one … two … Port 6 … one iridescent Pearl … Port 2 … two reflections … Port 5 … one firewall … Port 3 … 2 injections … Port 4 … one song”
- “this is mathematically important in the MOSAIC WARFARE GALOIS LATTICE”

## Canonical Shape

### Port artifact cardinality

- All ports P0–P7 must publish exactly **8** artifact items (8^1).
- The artifact items are indexed with powers-of-two IDs: 1, 2, 4, 8, 16, 32, 64, 128.

### Meta-promoted cardinality

- SCATTER ports (P0–P3): promote exactly **2** items (2^1), with IDs 1 and 2.
- GATHER ports (P4–P7): promote exactly **1** item (8^0), with ID 1.

## Meta-Promoted Deliverables (Required Labels)

These labels are the *type contract* for meta-promoted items.

| Port | Persona | Mode | Meta-promoted count | Required label(s) |
|---|---|---|---:|---|
| P0 | THE LIDLESS LEGION | SCATTER | 2 | Observation, Observation |
| P1 | THE WEB WEAVER (Swarm Lord of Webs) | SCATTER | 2 | Top Color, Top Color |
| P2 | THE MIRROR MAGUS | SCATTER | 2 | Reflection, Reflection |
| P3 | HARMONIC HYDRA | SCATTER | 2 | Injection (Battery), Injection (Battery) |
| P4 | RED REGNANT | GATHER | 1 | Song |
| P5 | PYRE PRAETORIAN | GATHER | 1 | Firewall |
| P6 | KRAKEN KEEPER | GATHER | 1 | Iridescent Pearl (UML Mermaid) |
| P7 | SPIDER SOVEREIGN | GATHER | 1 | Alignment (S3 Handoff) |

## Wiring Requirement

- Each port artifact must contain a **Meta-Promoted Items** block with those labeled placeholders.
- Meta synthesis must show:
  - Page 1: per-port briefings
  - A dedicated section enumerating **Meta-Promoted Deliverables** (P0 → P7)
  - Cardinality PASS/FAIL validators

## Notes

- This contract does **not** constrain content beyond label + cardinality; the system must still answer arbitrary prompts (e.g., “best API integration with MediaPipe tasks”).
