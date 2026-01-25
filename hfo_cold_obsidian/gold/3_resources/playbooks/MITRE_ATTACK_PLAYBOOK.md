# Medallion: Gold | Mutation: 0% | HIVE: V

# 🛡️ Playbook: MITRE ATT&CK (Threat Behavior Mapping)

**Intent:** Use MITRE ATT&CK as a *labeling and reasoning scaffold* for adversary behaviors without importing or duplicating the full ATT&CK corpus.

---

## External Source (Authoritative)

- ATT&CK knowledge base (official): <https://attack.mitre.org/>

## Workflow

1) Identify the behavior/event.
2) Tag with ATT&CK tactic/technique IDs when known.
3) Map actions across HFO ports:
   - P0 evidence → P1 normalization → P6 storage → P4 red-team probes → P5 guards.
4) Record a compact local entry (scenario, observables, hypothesis, tags, mitigations, tests).

## Guardrails

- Link to ATT&CK technique pages; do not copy large ATT&CK tables/lists into this repo.
- Keep mitigations written in HFO terms (ports, gates, receipts, tests).

---
*Spider Sovereign | Playbook-ATTACK-01*
