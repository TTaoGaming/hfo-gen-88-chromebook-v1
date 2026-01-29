import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {
    port: undefined,
    out: undefined,
    created: undefined,
    version: undefined,
  };
  for (let i = 2; i < argv.length; i++) {
    const token = argv[i];
    if (token === "--port") args.port = argv[++i];
    else if (token === "--out") args.out = argv[++i];
    else if (token === "--created") args.created = argv[++i];
    else if (token === "--version") args.version = argv[++i];
  }
  if (!args.port) throw new Error("Missing --port (e.g. P0)");
  if (!args.out) throw new Error("Missing --out (path to .md)");
  return args;
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function requirePortId(port) {
  const normalized = String(port).toUpperCase();
  if (!/^P[0-7]$/.test(normalized)) {
    throw new Error(`Invalid --port: ${port}. Expected P0..P7`);
  }
  return normalized;
}

function getIdentity(invariants, portId) {
  const ports = invariants?.ports;
  if (!Array.isArray(ports)) {
    throw new Error("Unexpected invariants shape: expected { ports: [...] }");
  }
  const row = ports.find((p) => String(p?.port_id).toUpperCase() === portId);
  if (!row) throw new Error(`No identity invariants found for ${portId}`);
  return row;
}

function getMapping(mappings, portId) {
  const ports = mappings?.ports;
  if (!ports || typeof ports !== "object" || Array.isArray(ports)) {
    throw new Error(
      "Unexpected mapping shape: expected { ports: { P0: {...} } }",
    );
  }
  const row = ports[portId];
  if (!row) throw new Error(`No mapping found for ${portId}`);
  return row;
}

function cardForSlot(slivers, slot) {
  const hit = (slivers || []).find(
    (s) => String(s?.slot).toLowerCase() === slot,
  );
  return hit?.card ?? "TBD";
}

function mdEscape(value) {
  return String(value ?? "").replace(/\|/g, "\\|");
}

function portNumber(portId) {
  return Number(String(portId).slice(1));
}

function partnerPortId(portId) {
  const n = portNumber(portId);
  return `P${7 - n}`;
}

function galoisStage(portId) {
  const n = portNumber(portId);
  if (n === 0 || n === 7)
    return {
      stage: 0,
      pair: "P0 + P7",
      meaning:
        "Hindsight → Alignment (sensor fusion → mission-thread navigation)",
    };
  if (n === 1 || n === 6)
    return {
      stage: 1,
      pair: "P1 + P6",
      meaning:
        "Insight → Memory (interlocking interfaces → deep recall / exemplars)",
    };
  if (n === 2 || n === 5)
    return {
      stage: 2,
      pair: "P2 + P5",
      meaning:
        "Validated Foresight → Gate (shape readiness → forensic/defensive gate)",
    };
  return {
    stage: 3,
    pair: "P3 + P4",
    meaning:
      "Evolution → Feedback (delivery injection → disruption/suppression loop)",
  };
}

function scatterGatherPartition(portId) {
  return portNumber(portId) <= 3 ? "SCATTER (diverge)" : "GATHER (converge)";
}

function metaPromotedCount(portId) {
  return portNumber(portId) <= 3 ? 2 : 1;
}

function seedJadc2ProducesRejects(portId) {
  switch (portId) {
    case "P0":
      return {
        produces:
          "Evidence packets, calibrated observations, anomaly candidates",
        rejects: "Speculation without evidence, stale/uncalibrated samples",
      };
    case "P1":
      return {
        produces: "Schemas/contracts, interface bindings, interop guarantees",
        rejects: "Implicit coupling, undocumented payloads, schema drift",
      };
    case "P2":
      return {
        produces: "State/shape models, constraints, validated transformations",
        rejects:
          "Unstable dynamics, invalid geometry, incoherent parameterizations",
      };
    case "P3":
      return {
        produces:
          "Delivery payloads (events/commands), injections, controlled actuation",
        rejects:
          "Side effects without guards, non-idempotent blasts, silent failures",
      };
    case "P4":
      return {
        produces:
          "Feedback/suppression signals, disruption signatures, loop tuning",
        rejects:
          "Runaway amplification, reward-hacking trajectories, noisy oscillations",
      };
    case "P5":
      return {
        produces:
          "Integrity verdicts, gates, quarantine decisions, resurrection policies",
        rejects:
          "Unsigned/tainted inputs, invariant breaks, un-auditable writes",
      };
    case "P6":
      return {
        produces:
          "Indexed memory, exemplars, retrieval surfaces, SSOT snapshots",
        rejects:
          "Unprovenanced memory writes, orphaned artifacts, duplicate truths",
      };
    case "P7":
      return {
        produces:
          "Navigation decisions, mission-thread constraints, orchestration plans",
        rejects: "Goal drift, ambiguous priorities, unbounded scope expansion",
      };
    default:
      return { produces: "", rejects: "" };
  }
}

function main() {
  const { port, out, created, version } = parseArgs(process.argv);
  const portId = requirePortId(port);

  const repoRoot = process.cwd();
  const invariants = readJson(
    path.join(
      repoRoot,
      "contracts/hfo_legendary_commanders_invariants.v1.json",
    ),
  );
  const mappings = readJson(
    path.join(repoRoot, "contracts/hfo_mtg_port_card_mappings.v5.json"),
  );

  const identity = getIdentity(invariants, portId);
  const mapping = getMapping(mappings, portId);

  const commanderName =
    identity.commander_name ?? mapping.commander ?? "UNKNOWN";
  const powerword = identity.powerword ?? "UNKNOWN";
  const mosaicTile = identity.mosaic_tile ?? "UNKNOWN";
  const jadc2Domain = identity.jadc2_domain ?? "UNKNOWN";
  const mosaicDomain = mapping.mosaic_domain ?? "UNKNOWN";

  const slivers = mapping.slivers ?? [];
  const equipment = mapping.equipment?.card ?? "TBD";

  const sliverStatic = cardForSlot(slivers, "static");
  const sliverTrigger = cardForSlot(slivers, "trigger");
  const sliverActivated = cardForSlot(slivers, "activated");

  const createdDate = created ?? new Date().toISOString().slice(0, 10);
  const versionId = version ?? "v1";

  const partner = partnerPortId(portId);
  const stage = galoisStage(portId);
  const partition = scatterGatherPartition(portId);
  const promoted = metaPromotedCount(portId);
  const jadc2Seeds = seedJadc2ProducesRejects(portId);

  const content = `---
medallion_layer: gold
mutation_score: "0%"  # narrative artifact; no tests
hfo_scope: hive8
port_id: ${mdEscape(portId)}
version: ${mdEscape(versionId)}
created: ${mdEscape(createdDate)}
tags:
  - hive8
  - ${mdEscape(portId)}
  - ${mdEscape(String(powerword).toLowerCase())}
  - ${mdEscape(String(mosaicTile).toLowerCase())}
  - ${mdEscape(String(commanderName).toLowerCase().replace(/\s+/g, "_"))}
provenance:
  identity_ssot: contracts/hfo_legendary_commanders_invariants.v1.json
  mapping_ssot: contracts/hfo_mtg_port_card_mappings.v5.json
---

# HFO HIVE8 — ${mdEscape(portId)} (${mdEscape(mosaicTile)}): ${mdEscape(commanderName)} / ${mdEscape(powerword)}

You are reading an 8-part translation ladder:
0) Galois lattice + identity + 3+1 cards → 1) analogies/scaffolding → 2) JADC2 tiles → 3) Gherkin + Mermaid → 4) red-team → 5) invariants → 6) tags/metadata + Mermaid → 7) Meadows.

---

## Part 0 — Galois lattice + identity + 3+1 cards (SSOT)
### Identity (SSOT-locked)
- **port_id**: ${mdEscape(portId)}
- **commander_name**: ${mdEscape(identity.commander_name ?? "")}
- **powerword**: ${mdEscape(powerword)}
- **mosaic_tile**: ${mdEscape(mosaicTile)}
- **jadc2_domain**: ${mdEscape(jadc2Domain)}
- **mosaic_domain (mapping)**: ${mdEscape(mosaicDomain)}
- **trigram**: ${mdEscape(identity.trigram?.name ?? "")} (${mdEscape(identity.trigram?.symbol ?? "")}), element ${mdEscape(identity.trigram?.element ?? "")}
- **octree bits**: ${mdEscape(Array.isArray(identity.octree_bits) ? identity.octree_bits.join("") : "")}

### Lattice placement (anti-diagonal)
- **partner (sum-to-7)**: ${mdEscape(partner)}
- **stage**: ${mdEscape(stage.stage)} (${mdEscape(stage.pair)})
- **stage meaning**: ${mdEscape(stage.meaning)}
- **scatter/gather**: ${mdEscape(partition)}
- **meta-promoted deliverables count**: ${mdEscape(promoted)}

Companion doctrine:
- Galois workflow: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GALOIS_LATTICE_DIAGONAL_ANTIDIAGONAL_WORKFLOW_V1_2026_01_27.md
- Meta-promoted shape: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_META_PROMOTED_DELIVERABLES_GALOIS_LATTICE_PROTOCOL_V1_2026_01_26.md

### 3+1 cards (SSOT)
- **Sliver (static)**: ${mdEscape(sliverStatic)}
- **Sliver (trigger)**: ${mdEscape(sliverTrigger)}
- **Sliver (activated)**: ${mdEscape(sliverActivated)}
- **Equipment**: ${mdEscape(equipment)}

---

## Part 1 — Plain-language analogies + cognitive scaffolding
### (A) ${mdEscape(sliverStatic)} (static)
Analogy:
Examples:

### (B) ${mdEscape(sliverTrigger)} (trigger)
Analogy:
Examples:

### (C) ${mdEscape(sliverActivated)} (activated)
Analogy:
Examples:

### (D) ${mdEscape(equipment)} (equipment)
Analogy:
Examples:

---

## Part 2 — JADC2 MOSAIC tiles
- **Domain label (SSOT)**: ${mdEscape(jadc2Domain)}
- **Mosaic tile (SSOT)**: ${mdEscape(mosaicTile)}
- **Mosaic domain (mapping)**: ${mdEscape(mosaicDomain)}
- **Produces (seed)**: ${mdEscape(jadc2Seeds.produces)}
- **Rejects (seed)**: ${mdEscape(jadc2Seeds.rejects)}

Lattice handoff notes:
- **${mdEscape(portId)} → ${mdEscape(partner)}**:
- **${mdEscape(partner)} → ${mdEscape(portId)}**:

---

## Part 3 — Declarative Gherkin + 2 Mermaid diagrams
### Gherkin
Invariant:
- Given …
- When …
- Then …

Happy path:
- Given …
- When …
- Then …

Fail-closed path:
- Given …
- When …
- Then …

### Mermaid (wiring)
~~~mermaid
flowchart TD
  A["${mdEscape(portId)}: ${mdEscape(commanderName)}"] --> B["Inputs"]
  A --> C["Outputs"]
  A --> D["Fail-closed guards"]
  C --> E["${mdEscape(partner)} handoff"]
~~~

### Mermaid (anti-diagonal stage)
~~~mermaid
flowchart LR
  P["${mdEscape(stage.pair)}"] --> M["Stage ${mdEscape(stage.stage)}"]
  M --> S["${mdEscape(stage.meaning)}"]
~~~

---

## Part 4 — Devil’s advocate / red teaming weaknesses
- Where this port can reward-hack:
- Where contracts can drift:
- Where latency/throughput can create illusions:
- How the partner port would exploit failure:

---

## Part 5 — Invariants list
- Anti-diagonal partner must sum to 7.
- All cross-port payloads are schema-validated (fail-closed).
- SSOT is the only blessed write-path for “memory writes”.
- Every artifact must be provenance-tagged.
- 3+1 cards must match SSOT contracts.

Port-specific invariants:
-

---

## Part 6 — Key tags + metadata summaries + 1 Mermaid diagram
Key tags (suggested):
- hive8
- ${mdEscape(portId)}
- ${mdEscape(powerword)}
- ${mdEscape(mosaicTile)}
- ${mdEscape(jadc2Domain)}

Metadata summary:
- **Primary input type**:
- **Primary output type**:
- **Primary risk**:
- **Primary guardrail**:

~~~mermaid
sequenceDiagram
  participant This as ${mdEscape(portId)}
  participant Partner as ${mdEscape(partner)}
  This->>Partner: Handoff
  Partner-->>This: Constraint/feedback
~~~

---

## Part 7 — Systems engineering (Donna Meadows vocabulary)
### Stocks

### Flows

### Feedback loops

### Delays

### Leverage points

### Failure modes

---

## Quick mental model (one sentence)
`;

  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, content, "utf8");
  process.stdout.write(`[ok] wrote ${out}\n`);
}

main();
