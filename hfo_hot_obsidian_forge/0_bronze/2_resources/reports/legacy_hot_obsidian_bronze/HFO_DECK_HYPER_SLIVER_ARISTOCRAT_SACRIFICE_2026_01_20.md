# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Deck (Half-Deck Spec): Hyper Sliver Aristocrat Sacrifice

**Timestamp**: 2026-01-20
**Keywords (user-provided)**: hyper, sliver, aristocrat, sacrifice
**Scope**: “Half the deck” = **32 cards total** = **8 core** + **24 supplements**.

This document is an evidence-backed reconstruction of the **HFO deck-as-architecture metaphor** from repo sources.

## What is known (grounded)

- HFO is an **8-port system (P0–P7)** with roles/verbs aligned to **JADC2 Mosaic** domains and expressed via “legendary commanders”.
  - Source: [hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl](../../3_resources/memory/mcp_memory.jsonl)
- You already have an explicit **triple-sided card format**:
  - **Side A**: MTG narrative/mechanics
  - **Side B**: Gherkin declarative scenario
  - **Side C**: JADC2 Mosaic tile (doctrinal grounding)
  - Source: [hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_TRIPLE_SIDED.md](../../4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_TRIPLE_SIDED.md)
- The “sliver manifold” exists as a canonical mapping from ports → sliver archetypes (two per port).
  - Source: [hfo_hot_obsidian/bronze/3_resources/mtg_slivers/16_SLIVER_SYNERGY_MANIFOLD.md](../mtg_slivers/16_SLIVER_SYNERGY_MANIFOLD.md)
- “Aristocrat logic” is explicitly used as a metaphor for **sacrificing transient units** to sustain **immutable, persisted knowledge**.
  - Source: [hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/hfo_mtg_commanders/KRAKEN_KEEPER_ASSIMILATION_PROTOCOL.md](../projects_archive_2026_01_18/hfo_mtg_commanders/KRAKEN_KEEPER_ASSIMILATION_PROTOCOL.md)

## The 3-sided card isomorphism (MTG = Declarative = Mosaic Tile)

You’ve defined a three-view equivalence class:

- **MTG side (mechanics)** = a compact, symbolic “API surface” for the port (costs, triggers, sacrifice/exile loops).
- **Gherkin side (declarative)** = the port’s executable intention contract (Given/When/Then invariants).
- **JADC2 Mosaic side (tile)** = the doctrinal role + domain placement (Sense/Fuse/Shape/Deliver/Disrupt/Defend/Store/Navigate).

In other words: the same capability is rendered three times for three audiences:

- **Human mythic builder** (MTG)
- **Engineering contract** (Gherkin)
- **Operational doctrine** (JADC2 Mosaic)

## Deck structure (32-card half-deck)

### A) 8 core cards = the 8 Port Commander Tiles

These are the “core cards” because they each correspond to one port and carry the primary verb + domain identity.

Grounding sources:

- Commander identity + JADC2 mapping: [hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl](../../3_resources/memory/mcp_memory.jsonl)
- Triple-sided template (A/B/C sides): [hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_TRIPLE_SIDED.md](../../4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_TRIPLE_SIDED.md)
- Newer binary/octality variant: [hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/hfo_mtg_commanders/mtg_card_manifest_v13.md](../projects_archive_2026_01_18/hfo_mtg_commanders/mtg_card_manifest_v13.md)

| Port | Core Card (Commander Tile) | Verb | JADC2 Domain | Signature mechanic (theme)
|---:|---|---|---|---|
| P0 | The Lidless Legion | OBSERVE | ISR | Sacrifice-for-telemetry / draw
| P1 | The Web Weaver | BRIDGE | Data Fabric | Schema weaving / fusion
| P2 | The Mirror Magus | SHAPE | Digital Twin | Copy/morph / simulation
| P3 | Harmonic Hydra / Spore Storm (variant names exist) | INJECT | Effect Delivery | Cascade / event delivery
| P4 | The Red Regnant | DISRUPT | Coev. Red Team | Sacrifice & cull / attrition engine
| P5 | The Pyre Praetorian | IMMUNIZE | Force Protection | Rebirth loop / hard gates
| P6 | The Kraken Keeper | ASSIMILATE | AAR | Exile-as-datalake / assimilation
| P7 | The Spider Sovereign | NAVIGATE | BMC2 | Search/control / orchestration

Note: P3 naming differs across artifacts (e.g., “Spore Storm” vs “Harmonic Hydra”). That variance is visible in the sources above.

### B) 24 supplements = (16 Slivers) + (8 MTG Anchors)

This matches your stated arithmetic: 8 core + 24 supplements = 32.

#### B1) The 16 Sliver supplements (2 per port)

These are the “hyper sliver” substrate: slivers represent **distributed abilities** (shared affordances) across the swarm.

Source: [hfo_hot_obsidian/bronze/3_resources/mtg_slivers/16_SLIVER_SYNERGY_MANIFOLD.md](../mtg_slivers/16_SLIVER_SYNERGY_MANIFOLD.md)

| Port | Sliver (Primary) | Sliver (Secondary) | Semantic vector
|---:|---|---|---|
| P0 | Cloudshredder | Synapse | High-velocity recon
| P1 | Mirror Entity | Gemhide | Universal interop
| P2 | Sliver Queen | Homing | Multi-agent propagation
| P3 | The First Sliver | Bonescythe | Cascade event delivery
| P4 | Necrotic | Harmonic | Kinetic neutralization
| P5 | Hivelord | Crystalline | Hardened integrity
| P6 | Dregscape | Pulmonic | Temporal resilience
| P7 | Overlord | Legion | Strategic orchestration

#### B2) The 8 MTG “anchor” supplements (1 per port)

These are the “real MTG reference anchors” paired to each port’s identity.

Source: [hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/HFO_LEGENDARY_COMMANDERS_V1.md](../../4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/HFO_LEGENDARY_COMMANDERS_V1.md)

| Port | MTG Anchor Card
|---:|---|
| P0 | Urza, Lord High Artificer
| P1 | Breya, Etherium Shaper
| P2 | Sakashima of a Thousand Faces
| P3 | Ghave, Guru of Spores
| P4 | Elesh Norn, Mother of Machines
| P5 | Syrix, Carrier of the Flame
| P6 | Arixmethes, Slumbering Isle
| P7 | Kenrith, the Returned King

## Why “Aristocrat Sacrifice” is a core architectural keyword

In your repo’s semantics, **sacrifice** is not just flavor; it is a design primitive:

- **Culling / mutation pressure (P4)**: sacrifice removes weak/low-signal agents and forces evolution.
  - Source: [hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/hfo_mtg_commanders/STABILIZED_HFO_SLIVER_MOSAIC_V3.md](../projects_archive_2026_01_18/hfo_mtg_commanders/STABILIZED_HFO_SLIVER_MOSAIC_V3.md)
- **Rebirth / hardening loops (P5)**: sacrifice fuels resets/resurrection into a stronger state (fail-closed governance).
  - Source: [hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/hfo_mtg_commanders/LEGENDARY_HFO_COMMANDERS_V5_OBSIDIAN_GHERKIN.md](../projects_archive_2026_01_18/hfo_mtg_commanders/LEGENDARY_HFO_COMMANDERS_V5_OBSIDIAN_GHERKIN.md)
- **Assimilation economics (P6)**: sacrifice transient files/agents to sustain immutable, indexed stores (“aristocrat batches”).
  - Source: [hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/hfo_mtg_commanders/KRAKEN_KEEPER_ASSIMILATION_PROTOCOL.md](../projects_archive_2026_01_18/hfo_mtg_commanders/KRAKEN_KEEPER_ASSIMILATION_PROTOCOL.md)

A concise statement:

> **Aristocrats** = many cheap, disposable workers (agents/files) that convert “death” into advantage (telemetry, energy, persistence).

## Open gaps / drift flags

- I did **not** find a literal decklist named exactly “hyper sliver aristocrat sacrifice” or a file explicitly enumerating “8 core + 24 supplements” as a deck object.
- The 32-card half-deck above is therefore a **grounded reconstruction** using existing port/commander/sliver/anchor sources, not a verbatim list copied from a single canonical deck file.

If you want, I can:

1) create a dedicated SSOT deck file (e.g., `HFO_DECK_V1.yaml`) that pins this 32-card half-deck explicitly, and
2) add a guard script that asserts it stays 8+24 with unique names.
