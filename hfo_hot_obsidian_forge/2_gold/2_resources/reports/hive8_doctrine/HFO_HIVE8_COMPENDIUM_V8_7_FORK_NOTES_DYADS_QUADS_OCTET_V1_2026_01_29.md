---
medallion_layer: gold
mutation_score: 0
hive: V
schema_id: hfo.hive8.compact_notes
schema_version: 1
created_utc: "2026-01-29"
authority_port: P4
intent:
  - "Notes to fork/evolve Hive8 compendium v8.7 from v8.6."
  - "Integrate a consistent mechanics-as-behavioral-pointers lens for 3+1 packages, plus dyad/quad/octet composition semantics."
constraints:
  - "Merge-ready for portable body: no http(s) URLs, no Markdown links."
  - "Keep SSOT drift-gated tables unchanged (identity, envelope, P3 policy, MTG mapping)."
---

# v8.7 Fork/Evolve Notes — Solo/Dyad/Quad/Octet Semantics (merge-ready)

## Why this addition (what your discussion adds)
Your writeup adds a missing translation layer between:
- the SSOT 3+1 mapping table (static truth), and
- the per-commander 8-part ladder (doctrine),
by giving an explicit composition grammar:
1) solo package behavior
2) canonical dyads
3) preferred quads (pairs-of-pairs)
4) octet state (all 8 online)

In v8.7, I’d treat this as a **doctrinal “composition layer”**: a concise, testable summary of how ports combine into mission-thread behavior.

## Non-negotiable safety note (how to frame MTG mechanics)
Recommend a short disclaimer block (portable) that separates:
- **Mechanics-as-pointer** (metaphor and behavioral mnemonic), vs
- **Rules-true win line** (deterministic, step-based, assumption-complete)

Reason: some lines in the discussion are intentionally metaphorical (useful), but would be misread as rules-true if embedded verbatim.

Proposed portable wording:
- “The 3+1 cards are mnemonic behavioral pointers. When the doc states a ‘win line’, it must explicitly list assumptions and steps; otherwise treat it as metaphorical doctrine.”

## Recommended placement in the compendium
Add a new section between the BLUF and the Commander Pages, or between Commander Pages and Meta Synthesis:

Option A (preferred):
- BLUF
- NEW: “Composition Layer: Solo → Dyads → Quads → Octet (portable)”
- Commander Pages (8 parts each)
- Meta Synthesis

Option B (minimal disruption):
- Keep v8.6 ordering, but add a short “Composition Layer” inside Meta Synthesis as a first subsection.

## Proposed “Composition Layer” structure (portable)

### 1) Solo package template (applies to each port)
For each port, add a compact block:
- “Solo resolution goal”
- “Failure mode (solo)”
- “Tripwire (solo)”
- “Output artifact (solo)”

This makes the solo paragraph operationally comparable across ports.

### 2) Canonical dyads (must match anti-diagonal)
Use the lattice as the primary grouping:
- (P0 + P7) ISR ↔ C2
- (P1 + P6) Data Fabric ↔ AAR
- (P2 + P5) Spike Factory ↔ Blue Team
- (P3 + P4) Delivery ↔ Red Team

For each dyad, recommend a standard 4-line schema:
- “Joint capability” (what becomes possible)
- “Joint risk” (new failure mode)
- “Guardrail” (what must be fail-closed)
- “Evidence artifact” (what to log or gate)

### 3) Non-canonical but useful dyads (explicitly marked)
Keep a short list of “useful but non-canonical” dyads, but mark them as overlays rather than lattice defaults.
Example overlays from your discussion:
- (P4 + P5) Contestation ↔ Recovery (GATHER axis)
- (P3 + P6) Deploy ↔ Assimilate (sorties and rebuild)

### 4) Preferred quads (pairs-of-pairs)
Recommend defining quads explicitly as:
- “Which dyads are being composed”
- “What the quad optimizes”
- “What the quad risks”

Your draft quads map cleanly:
- Quad A (P0, P1, P6, P7): sensemaking + C2 spine
- Quad B (P2, P5, P0, P1): macro-engine
- Quad C (P3, P4, P5, P6): attrition blender
- Quad D (P2, P3, P7, P1): factory + delivery + command + fabric

### 5) Octet state (all 8 online)
Recommend rewriting this as an explicit “multiple win axes” section:
- “Speed axis” (tempo)
- “Fuel axis” (mana and resources)
- “Inevitability axis” (recursion + adaptation)
- “Denial axis” (removal, disruption, rollback)

And add a single sentence: “Octet state is not a single combo; it’s a capability envelope with multiple converging finish lines.”

## Rules-true vs pointer-true: fixes to embed before promoting
These are small correctness adjustments that make the doctrine safer.

### A) Summoning sickness nuance (important for ‘infinite any’ claims)
- Sacrifice abilities do not require haste. Tokens can be sacrificed immediately.
- Tapping for mana (Gemhide-style) does require haste if the token just entered.

Recommendation: when describing “infinite any” or “tap then sac” loops, always specify whether haste is assumed for newly created tokens.

### B) “Myriad causes endless cascades” should be reframed
Cascade triggers on casting, not on token copies entering.
Recommendation: phrase this as a metaphorical throughput pointer unless a rules-true cast loop is explicitly specified.

### C) Win lines should use a standard recipe format
Add a compact recipe format so the doc stays audit-friendly:
- Inputs (board state)
- Assumptions (haste? activation doubler? mana conversion?)
- Steps (numbered)
- Outputs (what becomes infinite / what is guaranteed)
- Failure points (what breaks it)

## Suggested v8.7 content edits (surgical)

### 1) Add a new portable subsection: “Mechanics-as-Pointers Contract”
A short block near the BLUF:
- states pointer-true vs rules-true distinction
- commits that any explicit “infinite/win line” must be a recipe

### 2) Enrich each commander page (without adding a 9th part)
Within Part 1 (analogies) add a consistent mini-block:
- “Behavioral pointer: why these 3+1 mechanics cue the port’s Mosaic tendencies”

Within Part 4 (red team) add:
- “How this port’s package fails if overextended”

### 3) Add one cross-port “Composition Layer” section
Keep it short, and treat it as doctrine, not SSOT.

### 4) Add an “Assumption Ledger” table (portable)
A small table listing any assumptions used by win lines (e.g., haste for newly created tokens) so future edits don’t drift implicitly.

## Suggested v8.7 annex (non-portable, optional)
If you want maximum detail without bloating portable:
- Annex: “Win Lines Cookbook” (recipes only)
- Annex: “Rules citations and card rulings” (external references live here, not in portable)

End state goal for v8.7:
- v8.6 stays the SSOT-gated portable backbone.
- v8.7 adds the composition semantics layer and makes combo claims audit-friendly.
