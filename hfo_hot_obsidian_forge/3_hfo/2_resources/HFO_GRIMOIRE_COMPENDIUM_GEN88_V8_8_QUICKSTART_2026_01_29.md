---
medallion_layer: bronze
mutation_score: 0
hive: V
schema_id: hfo.gen88.grimoire_quickstart
doc_family: hfo.grimoire.compedium.gen88.v8_8
generated_utc: 2026-01-29T00:00:00Z
---

# HFO Grimoire Compendium — Gen88 v8.8 (Quickstart)

Purpose: a one-page operator guide for using the Gen88 v5 Hive8 Grimoire in day-to-day work (especially inside VS Code).

## What this Grimoire is

- A **portable, self-contained doctrine kernel** for HFO HIVE8 (P0–P7) with “3+1” commander mnemonics.
- A **translation ladder**: identity → analogies → JADC2 tiles → BDD (Gherkin) + Mermaid → red-team → invariants → tags/metadata → Meadows.
- A **gated artifact**: the canonical compendium is checked by repo verifiers (manifest/frontmatter/portability/drift).

Primary doc(s):
- Canonical (portable, gate-checked): `hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_8_2026_01_29.md`
- Grimoire (operator copy): `hfo_hot_obsidian_forge/3_hfo/2_resources/HFO_GRIMOIRE_COMPENDIUM_GEN88_V8_8_2026_01_29.md`
- Hot resources mirror (tooling target): `hfo_hot_obsidian_forge/hfo/resources/HFO_GRIMOIRE_COMPENDIUM_GEN88_V8_8_2026_01_29.md`

## How to use it (fast)

1) Read the **BLUF** first. It sets the invariants: ports are bounded, SSOT is law, drift is detected.
2) Pick the port you’re in (P0–P7) and use the **Part ladder** as your checklist.
3) For any work that can change state, run the **P4 4-beat** ritual:
   - Preflight → Payload → Postflight → Payoff (handoff)
4) Close the loop with an **SSOT status_update** so the next turn starts from truth.

## HIVE/8 = PDCA (with a swarm twist)

These are **aliases**: two names for the same loop.

- **Plan**: HFO Hindsight = Hunting Hyper-heuristics
- **Do**: HFO Insight = interlocking interfaces
- **Check**: HFO Validated Foresight = validation vanguard
- **Act**: HFO Evolve = evolving engines

Practical meaning: swarms can split the loop across ports/roles, but the loop must still close.

## IDE / Copilot workflow (recommended)

When you ask Copilot to do work in this repo, the best prompts explicitly bind it to:

- The **canonical anchors** (AGENTS + Grimoire + pointers)
- The **port** you’re operating as (P0–P7)
- The **beat** you want (Preflight/Payload/Postflight/Payoff)
- The **gate** you expect to pass (e.g. Hive8 compendium verifiers)

Example prompt template:

"Operate as Gen88v5 P4. Use the Grimoire v8.8 BLUF + port ladder. Make the smallest safe change. Produce a P4 4-beat proof bundle. End with an SSOT status_update. Run `npm run verify:hive8:compendium` if the compendium changes."

## Commands that matter

- Hive8 compendium gates: `npm run verify:hive8:compendium`
- P4 4-beat wrapper (proof + signals): `bash scripts/hfo_p4_basic_4beat.sh --note "..." --slug "..." --title "..." --summary "..." --outcome ok|partial|error`
- SSOT overview: `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_hub.py memory:overview`
- SSOT status update: `bash scripts/mcp_env_wrap.sh ./.venv/bin/python hfo_ssot_status_update.py --topic <topic> --payload-json '{...}'`

## “What do I do next?” (operator checklist)

- If you’re changing doctrine: update canonical → run gates → mirror to Grimoire paths → refresh receipts if required → commit.
- If you’re changing code: pick a port → enforce contracts → produce proof payload → write SSOT update.
- If you’re debugging drift: start at SSOT (contracts) → confirm derived docs → run drift verifiers.
