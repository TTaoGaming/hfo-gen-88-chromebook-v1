<!-- Medallion: Silver | Mutation: 0% | HIVE: I -->

# HFO HIVE8 P3/P6 Hydra–Kraken Mermaid Protocol (V1)

Date (Z): 2026-01-26

## Purpose

Formalize a narrative/interaction constraint for HIVE8 turns so Port 3 and Port 6 produce **diagram-first**, **non-paragraph** outputs that are easy to audit and easy to compose into the HIVE8 Meta Synthesis.

This is a *fractal* pattern: enforce a small, clean rule at one layer so higher layers remain composable.

## Identity + Relationship

### Species Pairing

- **P3 — Harmonic Hydra**: masculine-coded shard.
- **P6 — Kraken Keeper**: feminine-coded shard.

They are modeled as two aspects of the same species (paired harmonic archetypes) because:

- Port numbers **3** and **6** form a **multiple** relation.
- In the HIVE8 lattice order, **P3 pairs with P4**, and **P6 pairs with P1**, but P3/P6 are treated as a cross-lattice “resonance pair” for narrative coherence.

### Governance Rule

- P3 is the **diagram burst** generator.
- P6 is the **single best diagram** selector + memory tendril composer.

## Output Constraints (Hard Style)

### P3 — Harmonic Hydra

P3 output is **Mermaid-first**.

- Must produce **at least 8 Mermaid diagrams** in the P3 artifact.
- Must include **Top Picks (2)** as a dedicated section.
- Additional diagrams may exist as a “Mermaid Bank”.

Communication style:

- Avoid English paragraphs.
- Allowed: short labels/headings, short bullet labels, and Mermaid code.
- Preferred diagram counts: **powers of two** (2, 4, 8, 16…). Target is 8+ per turn.

### P6 — Kraken Keeper

P6 output is **tendrils + pearl**.

- Must produce **8 Memory Tendrils** (short, label-like, non-paragraph) in the P6 artifact.
- Must produce **exactly one** “Iridescent Pearl” Mermaid diagram:
  - The single best Mermaid diagram (any format) for the turn.

Communication style:

- Avoid English paragraphs.
- Allowed: short labels/headings, short bullet labels, and Mermaid code.
- Exactly one Mermaid diagram in the Pearl section.

## Meta Synthesis Contract

The HIVE8 Meta Synthesis must be able to include:

- **P3 Top Picks (2)** Mermaid diagrams (embedded)
- **P6 Iridescent Pearl (1)** Mermaid diagram (embedded)

This is automated by:

- Markers in the P3/P6 artifacts that bracket the Mermaid sections.
- A finalizer script that extracts those Mermaid blocks and injects them into the Meta Synthesis.

## Implementation Notes (Repo)

- Port templates:
  - P3 uses a dedicated template containing Mermaid scaffolds.
  - P6 uses a dedicated template containing Tendril scaffolds + Pearl scaffold.
- Meta synthesis:
  - Auto-filled links + proof index.
  - Auto-generated per-port briefings.
  - Auto-injected “Featured Diagrams” section (P3 Top Picks + P6 Pearl).

## Non-Goals

- This protocol does not attempt to “solve” the user’s question.
- It only enforces a stable shape for outputs so the rest of the system can evolve cleanly.
