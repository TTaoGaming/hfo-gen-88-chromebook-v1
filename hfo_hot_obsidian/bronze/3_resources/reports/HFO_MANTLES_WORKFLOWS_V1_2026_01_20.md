# Medallion: Bronze | Mutation: 0% | HIVE: I

# HFO Mantles: 8 Commander Workflows (V1)

**Timestamp**: 2026-01-20
**Canon**:

- There are **8 commanders (P0–P7)**.
- Each commander has **exactly one Mantle**.
- Mantles are **workflows** (state machines / doctrine), not “extra legendary artifacts”.
- Artifact canon remains restricted to the 3 canonical artifacts (names may also be used as Mantle names):
  - P3: Nematocyst Needles
  - P4: Book of Blood Grudges
  - P7: Obsidian Hourglass

## Research Anchors (repo-grounded; no invention)

This section exists to keep the Mantle definitions **evidence-backed** and to clearly separate:

- **Grounded repo sources** (preferred)
- **Archived / AI-memory sources** (allowed, but explicitly lower trust)
- **Missing evidence** (must be flagged, not filled with invention)

### Exemplar composition ("0 invention")

- Repo doctrine explicitly encodes exemplar-first composition and rejects bespoke invention:
  - `.github/agents/HFO-Hive8.agent.md`
  - `hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/architecture/HUB_V9_GALOIS_LATTICE_SPEC.yaml`
  - `hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/architecture/ports/hfo_orchestration_hub.py`

### Map-Elites / mission-fit / evaluation harness

- "Map-Elites Archive" and explicit "Mission Fitness Score" are described in:
  - `hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/reports/PARETO_FRONTIER_EVAL_HARNESS.md`
- Mission-fit framing (Mosaic/JADC2 grounding) is described in:
  - `hfo_hot_obsidian/bronze/3_resources/hfo_mission_fit_research.md`
  - `hfo_cold_obsidian/bronze/3_resources/hfo_mission_fit_research.md`

### Spike factory (candidate generation)

- "Spike Factory" appears as a named SHAPING concept in the archive vault:
  - `hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/sprawl_cleanup_2026_01_14/ttao-notes-2026-1-12.md`
  - `hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/hfo_mtg_commanders/MASTER_HFO_COMMANDER_VAULT.md`

### Mission completion / Definition-of-Done (hard gates)

- A concrete "MISSION_COMPLETE" event exists in the Alpha trial state machine:
  - `scripts/hfo_alpha_trial.py`
- Port-specific "Definition of Done" sections exist in the W3C pointer archive:
  - `hfo_hot_obsidian/bronze/3_resources/projects_archive_2026_01_18/ai-chat-w3c-pointer-2026-1-9.md`

### Evidence quality note (archived AI memory)

- Some Map‑Elites/hourglass-variant language exists in archived chat-memory JSON. Treat as **non-authoritative** unless corroborated elsewhere:
  - `hfo_hot_obsidian/bronze/4_archive/areas_archive_2026_01_18/root_cleanup_staging_2026_01_18/reports/chat-gpt-memory-2026-1-18.json`

### Missing external research (tooling degraded)

- External search is currently **not available** in this workspace (observed TOOL_TRIPWIRE failures):
  - `hfo_hot_obsidian/hot_obsidian_blackboard.jsonl`

## 4-part Mantle schema (used for all 8)

1) **Trigger** — when the mantle runs
2) **Inputs** — data/resources it consumes
3) **Invariants** — rules it must never violate (fail-closed)
4) **Outputs** — artifacts/state it produces

---

## P7 — Mantle of the Obsidian Hourglass (HIVE/8 Prescience Engine)

This is the flagship example. It is **powerful at full capacity**, but currently a **shadow**: the mantle exists as doctrine and partial surfaces, not yet as a fully-automated prescience engine.

### 1) Trigger

- A mission-cycle boundary (start-of-task, end-of-task, or explicit “turn the hourglass”).
- A detected drift event (contradiction, regression, schema break, trust failure).
- A request for **prescience**: “what should we do next” with evidence constraints.

### 2) Inputs

- **Hindsight**: immutable logs + receipts + blackboards + prior gate results (past web).
- **Insight**: current swarm state (active tasks, active ports, current constraints/budgets).
- **Validated Foresight**: candidate futures from simulation/search (spike factory), evaluation harness results, and validated predictions.
- **Evolution**: mutation operators / genetic programming proposals for MapElite-style exploration + selection.

### 3) Invariants

- **Fail-closed**: if evidence is missing, mark uncertainty explicitly; do not fabricate.
- **Provenance first**: every conclusion points to sources (logs/docs/contracts) or is labeled hypothesis.
- **Bounded budgets**: time/compute caps per cycle; degrade gracefully.
- **Strange Loop durability**: always returns to Hindsight with a new index ($n\!+\!1$), never “forgets” the last validated state.
- **No silent cross-boundary injection**: injection workflows are explicit (delegated to P3 mantle).

### 4) Outputs

- A **Cycle Record** (H→I→V→E) with:
  - what was observed (H),
  - what is currently true (I),
  - what was tested/validated (V),
  - what changed/evolved (E).
- A prioritized **next-intent manifest** for the swarm (what to do next, with budgets).
- Updated **anti-drift guardrails** (new checks, new contracts, new invariants).

### Internal phase loop (HIVE/8)

- **H — Hindsight / Hunt**: query past web + receipts to frame the problem.
- **I — Insight / Interlock**: fuse current state across swarm; ensure shared envelope.
- **V — Validated Foresight / Validate**: spike factory + harness; reject non-validated futures.
- **E — Evolution / Evolve**: genetic programming / MapElite exploration of improvements.
- **Strange Loop**: commit back to Hindsight as $n\!+\!1$ (durable recursion).

---

## P3 — Mantle of the Nematocyst Needles (Injector Arsenal)

### 1) Trigger

- A delivery intent is approved (“inject this effect/payload into the active app surface”).

### 2) Inputs

- Target policy (what is allowed to be touched/injected).
- Active app context (currently same-origin iframe/app; later generalized boundaries).
- Payload library: **ALL needles** — each nematocyst is a distinct targeted payload.

### 3) Invariants

- **Explicit targeting**: never inject into unspecified targets.
- **Escalation as saturation**: if one payload fails, branch to $8^N$ payload variants (bounded by budgets).
- **Auditability**: each injection attempt is logged with a reason + outcome.

### 4) Outputs

- One or more delivered effects (pointer/event/app injections).
- A replayable injection trace (what needle(s) were used, success/failure).

---

## P4 — Mantle of the Book of Blood Grudges (Hashed Pain Ledger)

### 1) Trigger

- Any integrity breach, contradiction, betrayal signal, or quorum failure.

### 2) Inputs

- Failure events, red-truth signals, and any evidence of tampering.

### 3) Invariants

- **Cryptographic hashing**: ledger is tamper-evident (chain-linked entries).
- **Pain is signal**: do not discard; compress, index, and make actionable.
- **Non-forgetfulness**: grudges decay only by explicit policy, never silently.

### 4) Outputs

- A hashed ledger entry (“grudge counter”) with provenance.
- Escalation hints to P5 (defend) and P7 (hourglass) when thresholds are crossed.

---

## P2 — Mantle of the Mirror Mask of Many (Perspective Rotation)

### 1) Trigger

- A modeling decision is requested (COA selection, hypothesis testing, reframing).

### 2) Inputs

- Fused signal envelopes (from P1), plus current constraints.

### 3) Invariants

- **Perspective rotation is mandatory**: at least 8 frames/faces considered.
- **No single-face dominance** without validation (handshake with P5/Validate).

### 4) Outputs

- A ranked set of COAs/hypotheses with stated assumptions.
- A “why we chose this face” explanation trail.

---

## P5 — Mantle of the Embercloak / Blue Phoenix (Resurrection-as-Integrity)

### 1) Trigger

- Integrity checks fail, contamination is detected, or recovery is required.

### 2) Inputs

- Grudge ledger escalations (from P4), validated policies, and current threat model.

### 3) Invariants

- **Zero-trust posture**: refuse unsafe resurrection.
- **Become flame to become pure**: cleanse → reforge → resurrect only when rules pass.

### 4) Outputs

- A hardened restored state (revived system with stronger invariants).
- New/updated guard checks to prevent recurrence.

---

## P0 — Mantle of the Lidless Aperture (Sensing Fanout)

### 1) Trigger

- New signal sources appear, or an observation sweep is requested.

### 2) Inputs

- Sensor streams / telemetry shards.

### 3) Invariants

- **Wide capture, narrow commit**: many signals observed; few promoted with justification.

### 4) Outputs

- Promoted observations (ranked) and raw context snapshots.

---

## P1 — Mantle of the Loomed Fabric (Envelope Weaving)

### 1) Trigger

- Cross-port coordination needs a shared shape (schema/envelope).

### 2) Inputs

- Observations + intent + provenance.

### 3) Invariants

- **Single authority for envelope semantics** (P1 owns the shared shape).
- **Compatibility**: reject data that cannot be placed into the fabric.

### 4) Outputs

- Canonical envelopes/threads for downstream ports.

---

## P6 — Mantle of the Abyssal Ledger (Assimilation)

### 1) Trigger

- End-of-cycle, loss events, or explicit “assimilate” request.

### 2) Inputs

- Logs, traces, receipts, blackboard entries.

### 3) Invariants

- **Nothing is lost**: everything is indexed; compression is allowed but not deletion.

### 4) Outputs

- Retrieved lessons and durable indexed memory ready for future Hindsight.

---

## Notes: shadow → full capacity roadmap (Hourglass)

- **Shadow (now)**: doctrine + partial surfaces; manual invocation; incomplete spike factory + MapElite loops.
- **Full capacity (target)**: automated H→I→V→E cycles with bounded budgets; spike factory generating candidate tools; validated foresight via harness; evolutionary genetic programming / MapElite exploration; Strange Loop commit back to Hindsight $n\!+\!1$.
