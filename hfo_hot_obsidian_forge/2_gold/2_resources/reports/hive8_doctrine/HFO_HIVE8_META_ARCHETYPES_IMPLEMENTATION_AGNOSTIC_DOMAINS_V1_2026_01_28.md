<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->

## <!-- markdownlint-disable MD041 MD003 MD022 -->

medallion_layer: gold
mutation_score_target: 0.88
hfo_scope: hive8
protocol: meta_archetypes_implementation_agnostic_domains
version: v1
created_utc: 2026-01-28
consolidation_target: github_copilot_hive8_gen88v4_agent_mode

---

# HFO HIVE/8 — Meta-archetypes HFO Should Adopt (Implementation-Agnostic Domains) (V1)

## Intent

Define the **implementation-agnostic domains** ("meta-archetypes") that HFO should consistently adopt, independent of language/runtime/UI.

These are written as **Gold**: stable, teachable, and usable as a scoring rubric during design reviews and port execution.

## Canonical dyad mapping (HIVE anti-diagonal)

The dyad rule is anti-diagonal symmetry: **P(i) ↔ P(7−i)**.

| Dyad    | HIVE phase | Alias                          | Primary mode                       |
| ------- | ---------- | ------------------------------ | ---------------------------------- |
| P0 + P7 | H          | Hunt / Hindsight               | evidence → intent / constraints    |
| P1 + P6 | I          | Interlock / Insight            | interface contracts → assimilation |
| P2 + P5 | V          | Validate / Validated Foresight | shaping → audit / hard gates       |
| P3 + P4 | E          | Evolve / Evolution             | inject → disrupt / feedback        |

## The 11 meta-archetypes (domains)

Each archetype names a domain, then assigns a **primary dyad owner** (who must defend it) and a **secondary dyad** (who stress-tests it).

|   # | Meta-archetype                              | Domain statement                                                                   | Primary dyad | Secondary dyad | Notes (operator signals)                                                                         |
| --: | ------------------------------------------- | ---------------------------------------------------------------------------------- | ------------ | -------------- | ------------------------------------------------------------------------------------------------ |
|   1 | Contested intelligence                      | Operate as if all sensing is adversarial: deception, noise, partial observability. | P0+P7        | P3+P4          | Confidence-scored observations; “unknown” is allowed; avoid narrative certainty.                 |
|   2 | Mosaic composability                        | Every tile/port can be swapped without killing the system.                         | P1+P6        | P2+P5          | Strict contracts; adapter manifests; “hot swap” readiness is a first-class acceptance criterion. |
|   3 | Interoperability via strict contracts       | Cross-port data must pass explicit schemas; fail-closed boundaries.                | P1+P6        | P2+P5          | Zod contracts; versioned manifests; compatibility checks; schema evolution is deliberate.        |
|   4 | Immutable provenance + receipts             | Every claim/action has lineage: inputs, outputs, hashes, receipts.                 | P1+P6        | P2+P5          | Append-only receipts; SSOT write-path; dedupe-safe ingestion; traceable artifacts.               |
|   5 | Temporal integrity                          | Ordering matters: resist desync and preserve the chain-of-evidence.                | P1+P6        | P0+P7          | Lamport/monotonic clocks; re-signing; deterministic replay manifests.                            |
|   6 | Resilient networking + graceful degradation | When dependencies fail, degrade instead of crashing.                               | P2+P5        | P3+P4          | Fallback modes; feature flags; isolate failure domains; keep core loop alive.                    |
|   7 | Zero trust posture                          | Assume compromised inputs/agents; enforce least privilege and explicit allowlists. | P2+P5        | P0+P7          | Tripwires; deny-by-default; quarantine paths; “no theater” audits.                               |
|   8 | Adversarial co-evolution                    | Red/blue co-adaptation is continuous; the attacker evolves too.                    | P3+P4        | P2+P5          | Chaos/fuzz harness; exploit playbooks; regression tests as scars.                                |
|   9 | Stigmergic memory / disk-first persistence  | The system’s memory survives context loss: blackboards + SSOT.                     | P1+P6        | P0+P7          | One write-path SSOT; derived views rebuildable; coordination via JSONL signals.                  |
|  10 | Byzantine finality lane                     | Decisions reach finality via quorum/verification, not vibes.                       | P2+P5        | P0+P7          | Quorum checks; conflict analysis; “abort on disagreement”; explicit stop rules.                  |
|  11 | Training + evaluation pipeline              | Model/tool changes are governed by evals, artifacts, and rollout gates.            | P2+P5        | P3+P4          | Dataset + model artifact provenance; eval gates; staged rollouts; rollback drills.               |

## Notes

- This list is intentionally **mechanical**: each archetype should be testable via artifacts, receipts, validators, and replay.
- Dyad mapping is a **responsibility assignment**, not exclusivity: all ports participate, but one dyad is accountable.

## Sources

- Dyads + aliases: hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/\_inbox/ai-chat-hfo-galois-lattice-2026-1-18.md
- Dyad order (anti-diagonal) and PDCA/HIVE mapping: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_HIVE_PDCA_DOUBLE_DIAMOND_FRACTAL_SCATTER_GATHER_V1_2026_01_27.md
- Mosaic composability, graceful degradation, temporal desync, anti-theater: hfo_hot_obsidian/bronze/3_resources/reports/JADC2_MOSAIC_VULNERABILITY_ASSESSMENT_V28_2.md
- Contested ISR framing (P0 domain text): hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_cards/HFO_CARD_SET_HIVE8_LEGENDARY_COMMANDERS_V1_2026_01_27.md
- Training pipeline / model artifacts (MITRE ATLAS playbook): hfo_cold_obsidian/gold/3_resources/playbooks/MITRE_ATLAS_PLAYBOOK.md
