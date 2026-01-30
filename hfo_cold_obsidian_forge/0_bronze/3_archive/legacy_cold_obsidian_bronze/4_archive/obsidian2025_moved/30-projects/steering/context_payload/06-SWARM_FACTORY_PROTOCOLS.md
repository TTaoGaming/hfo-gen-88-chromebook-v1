# Swarm Factory Protocols (PREY₈ • Quorum • Cleanroom)

This page is a **bridge doc**: it ties together the operational loop (PREY₈), the reliability layer (Byzantine quorum), the regeneration layer (Genesis/Phoenix), and the navigation layer (Obsidian Hourglass + HNSW) as one **swarm factory**.

If you only read one thing to understand “how HFO stays sane under chaos,” read this.

## PREY₈ as the base-8 workflow dial

- **Notation**: `PREY₈:XXXX` where each digit is a power-of-8 intensity for a phase.
- **Phases**: **P**erceive → **R**eact → **E**xecute → **Y**ield.
- **Meaning**: each digit chooses worker-count scale: $8^0, 8^1, 8^2, 8^3$.

Primary spec:
- [_archive/archive_dev_2025/HFO_buds/generation_80/GEN_80.3_PREY8_OBSIDIAN.md](/_archive/archive_dev_2025/HFO_buds/generation_80/GEN_80.3_PREY8_OBSIDIAN.md)

Gen81 reality constraint worth repeating:
- **DuckDB single-writer** tends to clamp **Execute/Yield** concurrency (keep writes serialized).

## The Heartbeat (my heartbeat for HFO)

Heartbeat is the “minimum viable life signal” for the swarm: it proves **the octet can still coordinate**.

- **1181 pattern**: $1 \rightarrow 1 \rightarrow 8 \rightarrow 1$ (intent → orchestrate → octet report → synthesis)
- Think of it as a small, repeatable PREY slice you can schedule (cron) or fire on demand.

Source:
- [_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_66/brain/grimoire/card_11_heartbeat.md](/_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_66/brain/grimoire/card_11_heartbeat.md)

## Byzantine quorum swarms (L1 hardened consensus)

When truth matters, you don’t trust a single generator.

- **Principle**: “No output without quorum.”
- **Practical shape**: **scatter** to a roster → **gather** into a consensus level → **validate** with guards → emit artifacts.
- **Why**: this is how HFO turns model brittleness into *system robustness*.

Canonical implementation notes (bug history, thresholds, timeouts, and the scatter/gather mental model):
- [_archive/Dev_2025_12_11/HiveFleetObsidian_2025_11_16_byzantine_quorum_tools_buggy/hfo_todo/2025-11-15-byzantine-sdk-formalization.md](/_archive/Dev_2025_12_11/HiveFleetObsidian_2025_11_16_byzantine_quorum_tools_buggy/hfo_todo/2025-11-15-byzantine-sdk-formalization.md)
- [_archive/Dev_2025_12_11/HiveFleetObsidian_2025_11_16_byzantine_quorum_tools_buggy/hfo_sdk/README.md](/_archive/Dev_2025_12_11/HiveFleetObsidian_2025_11_16_byzantine_quorum_tools_buggy/hfo_sdk/README.md)

Design framing (zero-trust loop as architecture, not just a trick):
- [_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_67/dreaming/HFO_BYZANTINE_GUARDRAIL.md](/_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_67/dreaming/HFO_BYZANTINE_GUARDRAIL.md)

## Antifragile coevolution: red-team / blue-team as a living immune system

HFO treats adversarial pressure as a *feature*, not a bug:

- **Red team pressure** (Disruptor / adversarial agent): attempts to subvert, mislead, or break consensus.
- **Blue team hardening** (Immunizer + Navigator): audits reality (tools, files, tests) and enforces intent/architecture.
- **Coevolution loop**: adversarial probes generate failures → failures become new tests/guards/features → the swarm grows stronger.

One-pager that explicitly names the system as “antifragile evolutionary swarm” and calls out an intentional Disruptor trying to subvert BFT:
- [_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_63/07_navigator_brain/ai-chat-hfo-archetecture-rpg-2025-12-02.md](/_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_63/07_navigator_brain/ai-chat-hfo-archetecture-rpg-2025-12-02.md)

## HNSW: how the spider walks the semantic manifold

When the swarm says “navigate memory,” HNSW is one of the key traversal primitives:

- **HNSW** (Hierarchical Navigable Small World) is the fast approximate-nearest-neighbor graph used to move through vector space neighborhoods.
- In HFO language: it’s how you find the “nearby” memories in the **Karmic Web** (past) quickly enough to keep the loop alive.

HFO sources that connect **Hourglass ⇄ HNSW ⇄ memory traversal**:
- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_hourglass.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_hourglass.md)
- [_archive/Dev_2025_12_11/hfo_gem_gen_71/brain/sota_orchestration_report.md](/_archive/Dev_2025_12_11/hfo_gem_gen_71/brain/sota_orchestration_report.md)

## Declarative Grimoire + Gherkin Cleanroom + Genesis/Phoenix

This is the “clean room genesis phoenix” spine: **spec first, then ports, then adapters, then audits**; and when corruption accumulates, burn-and-regenerate.

### Cleanroom (no code without Gherkin)
- Intent is written as a **Gherkin Feature**.
- Code is treated as a *derived artifact*.

Source:
- [_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_67/dreaming/HFO_ENGINEERING_PROTOCOLS.md](/_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_67/dreaming/HFO_ENGINEERING_PROTOCOLS.md)

### Genesis (abstract factory for swarm creation)
Genesis is the creation law: the “swarm factory interface” that spawns the standard roles/components.

Source:
- [_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_64/archive/dream_slop/grimoire/archive/mirrors/genesis_protocols.md](/_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_64/archive/dream_slop/grimoire/archive/mirrors/genesis_protocols.md)

### Phoenix (controlled burn + regeneration)
Phoenix is the system-level “escape hatch” when theater and complexity exceed recovery.

Source:
- [_archive/archive_dev_2025/HFO_buds/generation_73/hfo_grimoire/silver/card_03_phoenix_protocol_v2.md](/_archive/archive_dev_2025/HFO_buds/generation_73/hfo_grimoire/silver/card_03_phoenix_protocol_v2.md)

## Obsidian hourglass strange loop (hindsight → insight → foresight)

The hourglass is the tri-web triangulation engine:

- **Hindsight**: Karmic Web (Past) — what happened.
- **Insight**: Present Web (Present) — what’s happening.
- **Foresight**: Simulation Web (Future) — what could happen next.

Read:
- [_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_hourglass.md](/_archive/Dev_2025_12_11/hfo_gem_gen_63_1/grimoire/cards/obsidian_hourglass.md)
- [_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_67/dreaming/HFO_OBSIDIAN_MATRIX_v10_CANON.md](/_archive/Dev_2025_12_11/Historical_Buds_gem_gen_53_to_gen_67/Historical_Buds/hfo_gem_gen_67/dreaming/HFO_OBSIDIAN_MATRIX_v10_CANON.md)

## Minimal “swarm factory” recipe (Gen81-friendly)

- Start at `PREY₈:0000` (serial) until the heartbeat is green.
- Use Heartbeat 1181 to prove the octet wiring.
- Escalate with **Byzantine quorum** only for high-risk or truth-critical outputs.
- Keep **writes** serialized; push concurrency to read/think phases.
- When corruption accumulates: **Phoenix** → regenerate from the Grimoire DNA.
