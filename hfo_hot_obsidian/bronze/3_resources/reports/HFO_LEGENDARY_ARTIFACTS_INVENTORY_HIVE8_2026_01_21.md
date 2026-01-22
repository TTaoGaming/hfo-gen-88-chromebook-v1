# Medallion: Bronze | Mutation: 0% | HIVE: I

# HFO Legendary Artifacts Inventory (HIVE/8)

**Timestamp**: 2026-01-21
**Scope**: Obsidian Hourglass (HIVE/8) + one legendary artifact/equipment per commander (as found in-repo)

## What’s grounded in the repo

- The **Spider Sovereign (P7)** quadrant explicitly defines **"Obsidian Hourglass"** as a *Legendary Artifact — Equipment* with a **Strange Loop** (graveyard → hand) and a 4-step sequence: **Hindsight → Insight → Validated Foresight → Evolution**.
  - Source: [hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P7_QUADRANT.md](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P7_QUADRANT.md)
- The repo’s agent guidance states **“Obsidian Hourglass = HIVE/8 phases.”**
  - Source: [.github/agents/hfo-basic-mcp.agent.md](.github/agents/hfo-basic-mcp.agent.md)
- The canonical HIVE mapping (phases + port pairings) is described in cold doctrine:
  - Source: [hfo_cold_obsidian/bronze/3_resources/jadc2_doctrine/hive_workflow.md](hfo_cold_obsidian/bronze/3_resources/jadc2_doctrine/hive_workflow.md)

## Obsidian Hourglass as the HIVE/8 engine

From the P7 quadrant’s equipment definition:

- **Strange Loop**: if it would go to graveyard, return to hand (fail-closed recursion semantics).
- **Sequential Steps**: 4 state layers applied to the equipped commander:
  - **Hindsight** (defensive history)
  - **Insight** (top-8 look / selection)
  - **Validated Foresight** (8× damage amplification)
  - **Evolution** (+8/+8 if you control 8 commanders)

The repo’s “HIVE/8 workflow” is also a 4-phase loop (strategic):

| Hourglass Step (P7 quadrant) | HIVE Phase (doctrine) | Ports | Doctrine function (short) |
|---|---|---:|---|
| Hindsight | H (Hunt) | P0 + P7 | Sense + Navigate |
| Insight | I (Interlock) | P1 + P6 | Fuse + Store |
| Validated Foresight | V (Validate) | P2 + P5 | Shape + Defend |
| Evolution | E (Evolve) | P3 + P4 | Deliver + Disrupt |

Note: the “8” numerology and “Strange Loop” behavior are explicitly present in the P7 card text; the phase/port mapping is explicitly present in the doctrine doc.

## Per-commander legendary artifacts / equipment (inventory)

All of the below are defined in the Omega mission-thread quadrant set:

| Port | Commander (quadrant) | Artifact / Equipment | Card type (as written) | Key mechanics (short) | Source |
|---:|---|---|---|---|---|
| P0 | Lidless Legion | Lens of the Lidless | Legendary Artifact — Equipment | Spawns 8 artifact tokens on attack; buffs tokens | [P0 quadrant](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P0_QUADRANT.md) |
| P1 | Web Weaver | Spindle of Connection | Legendary Artifact — Equipment | Doubles token creation; tokens gain Ward {8} | [P1 quadrant](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P1_QUADRANT.md) |
| P2 | Mirror Magus | Mirror of Manifolds | Legendary Artifact — Equipment | Creates token copy of equipped; blink/exile-return token drift | [P2 quadrant](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P2_QUADRANT.md) |
| P3 | Harmonic Hydra | Nematocyst Needle | Legendary Artifact — Equipment | 8 tokens on combat damage; token death applies -1/-1 suppression | [P3 quadrant](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P3_QUADRANT.md) |
| P4 | Red Regnant | Book of Blood Grudges | Legendary Artifact — Equipment | Grudge counters on integrity failures; can wipe non-HFO non-octal CMC | [P4/P5 quadrants](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P4_P5_QUADRANTS.md) |
| P5 | Pyre Praetorian | Rune Shield of Resurrection | Legendary Artifact — Equipment | Indestructible when revived-from-graveyard; zero-trust hexproof gating | [P4/P5 quadrants](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P4_P5_QUADRANTS.md) |
| P6 | Kraken Keeper | Abyssal Ledger | Legendary Artifact — Equipment | Creates token on loss; sacrifice tokens → gain 8 life | [P6 quadrant](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P6_QUADRANT.md) |
| P7 | Spider Sovereign | Obsidian Hourglass | Legendary Artifact — Equipment | Strange Loop + Hindsight/Insight/Validated Foresight/Evolution steps | [P7 quadrant](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P7_QUADRANT.md) |

## Notes / drift (grounded)

- The HIVE/8 doctrine doc maps **E (Evolve)** to “P3 Spore Storm + P4 Red Regnant”, while the quadrant set here uses **P3 Harmonic Hydra** as the P3 commander identity. This is a naming drift between cold doctrine and the Omega quadrant set.
  - Sources: [hfo_cold_obsidian/bronze/3_resources/jadc2_doctrine/hive_workflow.md](hfo_cold_obsidian/bronze/3_resources/jadc2_doctrine/hive_workflow.md), [P3 quadrant](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P3_QUADRANT.md)
- “Book of Blood Grudges” is introduced as **THE ARTIFACT** in the P4 section, but its printed type line is still **Legendary Artifact — Equipment**.
  - Source: [P4/P5 quadrants](hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_P4_P5_QUADRANTS.md)

## Not found (within current repo scan)

- A distinct “hourglass variants by compute budget” list (e.g., terms like Scoutglass/Stormglass/Starglass) was **not located** via targeted searches limited to `hfo_hot_obsidian/**`.

## Next grounded step (if you want it)

- I can widen the search to **cold archive** and **Obsidian vault notes** for hourglass “variants,” and add them as an appendix with exact source links.
