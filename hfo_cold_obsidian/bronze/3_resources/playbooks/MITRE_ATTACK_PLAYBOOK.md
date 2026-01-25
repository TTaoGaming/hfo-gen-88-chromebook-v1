# Medallion: Bronze | Mutation: 0% | HIVE: V

# 🛡️ Playbook: MITRE ATT&CK (Threat Behavior Mapping)

**Intent:** Use MITRE ATT&CK as a *labeling and reasoning scaffold* for adversary behaviors without importing or duplicating the full ATT&CK corpus.

---

## What This Playbook Covers

- How to use ATT&CK as a tagging taxonomy for incidents, detections, and hardening work.
- A lightweight mapping approach: HFO Port/Commander → ATT&CK-style thinking.
- How to keep this repo clean: links + local summaries, not copied data.

## External Source (Authoritative)

- ATT&CK knowledge base (official): <https://attack.mitre.org/>

## Usage Pattern

### 1) Choose a “behavioral unit”

Examples:

- A suspicious workflow
- A compromised credential event
- An unusual process tree

### 2) Tag in ATT&CK terms

- Use ATT&CK tactic/technique IDs when you have them.
- If you don’t have IDs, use plain-language tags (e.g., “credential access”, “lateral movement”), then refine later.

### 3) Connect to HFO Ports

- **P0 Observe:** evidence acquisition (telemetry, artifacts)
- **P1 Bridge:** normalize into a schema/contract
- **P6 Assimilate:** store + index (DuckDB/blackboard)
- **P5 Immunize:** harden and add gates/guards
- **P4 Disrupt:** red-team / adversarial testing loops

### 4) Record outcomes as a mini playbook entry

Minimum fields:

- Scenario name
- Observables
- Hypothesis
- Candidate ATT&CK tags
- Controls to add (P5)
- Tests to add (P4)

## Repo Integration Suggestions

- Put your local notes under `hfo_cold_obsidian/**/playbooks/`.
- Keep ATT&CK content as *references* (URLs + paraphrased summaries).

## Guardrails

- Do not copy large tables/lists from ATT&CK into this repo.
- Prefer linking the technique page and writing your own HFO-specific “what to do” steps.

---
*Spider Sovereign | Playbook-ATTACK-01*
