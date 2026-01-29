<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->

---

medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
protocol: hive_pdca_double_diamond_fractal_scatter_gather
version: v1
created_utc: 2026-01-27
consolidation_target: github_copilot_hive8_gen88v4_agent_mode
---

# HFO HIVE/8 — H‑I‑V‑E PDCA Double Diamond (Fractal Scatter/Gather) (V1)

## Intent

Lock the **canonical zoom levels** for the HIVE/8 Gen88v4 architecture:

- **Zoomed-out (macro):** H‑I‑V‑E is a 4‑phase loop that aligns to PDCA and reads as a double diamond.
- **Zoomed-in (phase):** each phase is a **paired port micro-diamond** (scatter ↔ gather).
- **Zoomed-in (port):** each port internally runs **scatter → gather → scatter → gather** (a mini double diamond).

This document is **Gold**: it is meant to be stable, simple enough to teach, and precise enough to implement.

## Canonical phase names (HIVE)

| Letter | Phase | Meaning |
|---|---|---|
| H | phase_0_hindsight | look back; sense reality; establish evidence |
| I | phase_1_insight | interface/bridge; bind evidence into constraints |
| V | phase_2_validated_foresight | prove/validate; quantify confidence |
| E | phase_3_evolution | deliver/change; apply feedback and red-team |

Pair order (anti-diagonal): `(P0+P7) → (P1+P6) → (P2+P5) → (P3+P4)`.

## PDCA overlay (strange loop)

HIVE also labels a PDCA loop:

- **H = Plan** (discover/define the problem from evidence)
- **I = Do** (bridge into an executable contract / plan-of-record)
- **V = Check** (validate claims: bounds, audits, invariants)
- **E = Act** (ship, disrupt weak points, evolve the next cycle)

## Diagram 1 — Zoomed-out: 4-phase loop (double diamond + PDCA)

This is the “one slide” view.

```mermaid
flowchart LR
  %% Macro: H-I-V-E loop with double-diamond cadence.
  H["H: Hindsight<br/>(Plan)"] --> I["I: Insight<br/>(Do)"] --> V["V: Validated Foresight<br/>(Check)"] --> E["E: Evolution<br/>(Act)"] --> H

  %% Double diamond annotation (conceptual):
  %% Diamond 1: H (scatter) -> I (gather)
  %% Diamond 2: V (scatter) -> E (gather)
  H --- DD1[[Diamond 1<br/>Scatter→Gather]]
  V --- DD2[[Diamond 2<br/>Scatter→Gather]]
```

## Diagram 2 — Zoomed-in: each HIVE phase is a paired micro-diamond

Each phase runs a **scatter port** adjacent to a **gather port**.

```mermaid
flowchart TD
  subgraph H[H: phase_0_hindsight]
    P0[P0 OBSERVE<br/>SCATTER] --> P7[P7 NAVIGATE<br/>GATHER]
  end

  subgraph I[I: phase_1_insight]
    P1[P1 BRIDGE<br/>SCATTER] --> P6[P6 ASSIMILATE<br/>GATHER]
  end

  subgraph V[V: phase_2_validated_foresight]
    P2[P2 SHAPE<br/>SCATTER] --> P5[P5 IMMUNIZE<br/>GATHER]
  end

  subgraph E[E: phase_3_evolution]
    P3[P3 INJECT<br/>SCATTER] --> P4[P4 DISRUPT<br/>GATHER]
  end

  H --> I --> V --> E
  E --> H
```

## Diagram 3 — Zoomed-in: each port runs a mini double diamond (SGSG)

Within any single port, enforce an internal rhythm:

1) **Scatter**: generate candidate hypotheses/options.
2) **Gather**: select a dominant path and tighten constraints.
3) **Scatter**: draft the 8‑item artifact surface.
4) **Gather**: validate, finalize, and (if strict PASS) publish stigmergy.

```mermaid
flowchart LR
  S1[Scatter 1<br/>Hypotheses/options] --> G1[Gather 1<br/>Select + constrain]
  G1 --> S2[Scatter 2<br/>Draft 8 artifact items]
  S2 --> G2[Gather 2<br/>Strict validate + finalize]
  G2 -->|PASS| SIG[INJECT<br/>Stigmergy append]
  G2 -->|FAIL| STOP[Fail-closed<br/>No stigmergy]
```

## Diagram 4 — Nested diamonds (zoom rule: 2 at a time; 4 when doubled)

This diagram is intentionally “structural” (not geometric): it shows how a **big double diamond** contains a **smaller diamond**, which itself contains a **micro double diamond**.

Zoom rule:

- When you zoom in one level, a “piece” becomes **2** (scatter → gather).
- When you zoom in one more level, that becomes **4** (scatter → gather → scatter → gather).

```mermaid
flowchart TD
  %% BIG DOUBLE DIAMOND (two diamonds chained) in a strange loop.
  subgraph BIG["Big Double Diamond (HIVE Turn) — Strange Loop"]
    direction LR
    D1S[Diamond A: Scatter] --> D1G[Diamond A: Gather]
    D1G --> D2S[Diamond B: Scatter]
    D2S --> D2G[Diamond B: Gather]
  end

  D2G --> LOOP["Loop Closure<br/>(next turn)"]
  LOOP --> D1S

  %% Inside Diamond A (a smaller diamond).
  subgraph A_INNER[Inside Diamond A: Smaller Diamond]
    direction LR
    A_S[Scatter] --> A_G[Gather]
  end

  %% Inside A_G (a micro double diamond).
  subgraph MICRO[Inside Smaller Diamond: Micro Double Diamond]
    direction LR
    M_S1[Scatter 1] --> M_G1[Gather 1] --> M_S2[Scatter 2] --> M_G2[Gather 2]
  end

  %% Visual anchoring links (conceptual containment)
  D1S -. zoom in .-> A_S
  A_G -. zoom in .-> M_S1
```

## Fractal rule (what “nested diamonds” means)

- **Macro:** the whole turn is a double diamond (H→I, V→E) inside a PDCA strange loop.
- **Meso:** each HIVE phase contains a pair (scatter→gather).
- **Micro:** each port repeats scatter→gather→scatter→gather and then emits stigmergy only on PASS.

In practice: every “completed object” becomes the next cycle’s environment.

- Baton artifacts become the next port’s observed substrate.
- Stigmergy events become the next turn’s observed substrate.

## Hard constraints (Gen88v4 invariants)

- Ports 0–3 are SCATTER; ports 4–7 are GATHER.
- Each port publishes exactly **8** artifact items.
- Meta promotion counts are fixed (scatter=2, gather=1).
- Stigmergy is **append-only** and must be **strict-gated**.

## References

- Silver: [hfo_hot_obsidian_forge/1_silver/2_resources/reports/hive8_doctrine/HFO_HIVE8_SCATTER_GATHER_DOUBLE_DIAMOND_PDCA_PROTOCOL_V1_2026_01_26.md](hfo_hot_obsidian_forge/1_silver/2_resources/reports/hive8_doctrine/HFO_HIVE8_SCATTER_GATHER_DOUBLE_DIAMOND_PDCA_PROTOCOL_V1_2026_01_26.md)
- Gold vocabulary: [hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_OBSIDIAN_POWERWORDS_JADC2_DOMAIN_MAP_V1_2026_01_26.md](hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_OBSIDIAN_POWERWORDS_JADC2_DOMAIN_MAP_V1_2026_01_26.md)
