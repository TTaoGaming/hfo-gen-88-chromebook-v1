# Medallion: Gold | Mutation: 0% | HIVE: V

# 🧠 Playbook: MITRE ATLAS (Adversarial ML Behaviors)

**Intent:** Use MITRE ATLAS as a behavioral map for attacks against ML systems (data, training, inference, supply chain) and map mitigations into HFO Ports.

---

## External Source (Authoritative)

- MITRE ATLAS (official): <https://atlas.mitre.org/>

## Minimal Threat Surface Checklist

- Data, training pipeline, model artifacts, inference, deployment.

## Port Mapping

- P0 Observe: drift/anomaly signals
- P1 Bridge: contracts for inputs/outputs
- P4 Disrupt: adversarial evals
- P5 Immunize: provenance + gates + rollback
- P6 Assimilate: store evidence + eval results
- P7 Navigate: orchestrate secure ML loop

## Guardrails

- Link to ATLAS technique pages; do not replicate large corpora.

---
*Spider Sovereign | Playbook-ATLAS-01*
