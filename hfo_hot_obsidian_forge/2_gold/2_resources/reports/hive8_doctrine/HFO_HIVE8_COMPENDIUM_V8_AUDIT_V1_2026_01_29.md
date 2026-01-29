<!-- Medallion: Bronze | Mutation: 0% | HIVE: V -->
---
schema_id: hfo.hive8.audit
schema_version: 1
version: v1
status: draft

doc_id: hfo.hive8.compendium.v8.audit

dates:
  created_utc: "2026-01-29"
  updated_utc: "2026-01-29"

subject:
  compendium_version: v8
  compendium_doc:
    path: hfo_hot_obsidian_forge/2_gold/2_resources/reports/hive8_doctrine/HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V8_2026_01_29.md
    sha256: 4f943b8b6766a2ea5fb16141f65ddb5cde6b15306f7663860cfb94d0fe9ef4ce

proof:
  gate_capture_dir: artifacts/proofs/hive8_compendium_v8_audit_2026_01_29T170526Z
  p4_4beat:
    turn_id: ad5f77991cfe43e39d2154a5aa11d6c6
    preflight_receipt_id: c19695d31197
    postflight_receipt_id: 561079fb79b1
    payload_md: hfo_hot_obsidian/bronze/3_resources/p3s_payloads/2026_01_29T170602Z__P4__hive8_compendium_v8_s4_state_machine__ad5f77991cfe43e39d2154a5aa11d6c6.md
    payload_json: hfo_hot_obsidian/bronze/3_resources/p3s_payloads/2026_01_29T170602Z__P4__hive8_compendium_v8_s4_state_machine__ad5f77991cfe43e39d2154a5aa11d6c6.json
    payload_md_sha256: c1e0567ca289cce860123abe7bac34a914babd6b35b25ba6b285e51307fd77cd
    payload_json_sha256: a88167a1ffa47293345f5de8617f91f953ceafe3b68daef71096cb938586eb57

scores:
  scale: "0-10"
  devops: 8.0
  cdd: 8.5
  bdd: 7.5
  tdd: 5.5
---

# HFO HIVE8 Compendium V8 — 1-page Audit

## Executive summary
V8 is strong on CDD/DevOps foundations (SSOT + fail-closed verifiers + repeatable proof ritual). BDD is now explicit and machine-readable in doctrine (including S4 as a state machine), but TDD is the limiting factor: most port behaviors are not yet enforced by harness-level tests (beyond contract parsing and mapping drift checks).

## Proof of results (what ran, what passed)
All proof artifacts are local files (portable doctrine does not depend on links).

### Gate results (captured)
Captured gate run output:
- artifacts/proofs/hive8_compendium_v8_audit_2026_01_29T170526Z/gates_output.txt

Key pass lines (excerpted):
- OK: compendium front matter parsed (…V8…)
- OK: portable link policy satisfied (…V8…)
- OK: HIVE8 3+1 mappings match contracts/hfo_mtg_port_card_mappings.v5.json across 5 docs.
- 15 passing (contracts)
- OK: mermaid lint skipped (no files provided)

Compendium SHA256 (captured):
- artifacts/proofs/hive8_compendium_v8_audit_2026_01_29T170526Z/compendium_v8.sha256

### P4 4-beat ritual proof
This change is sealed with the P4 ritual (preflight→payload→postflight→payoff) and hashed payloads:
- turn_id: ad5f77991cfe43e39d2154a5aa11d6c6
- payload_md_sha256: c1e0567ca289cce860123abe7bac34a914babd6b35b25ba6b285e51307fd77cd
- payload_json_sha256: a88167a1ffa47293345f5de8617f91f953ceafe3b68daef71096cb938586eb57

## Audit scorecard (0–10)

### DevOps — 8.0
Strengths:
- Repeatable gates exist and run cleanly (frontmatter, portability, contract tests, mapping drift).
- Proof ritual produces receipts + sha256 payloads.
- Mapping drift is fail-closed and SSOT-locked across multiple docs.

Gaps to reach 9–10:
- Add a single “one-command” CI-like script that runs the whole gate suite + writes a proof directory consistently.
- Add a guardrail gate for “no legacy JSONL memory writes” (detector mentioned in doctrine, not enforced yet).

### CDD — 8.5
Strengths:
- SSOT contracts exist and are validated; invariants are explicit.
- Cross-boundary shapes are treated as first-class and fail-closed.
- Mapping contract is mechanically verified against docs.

Gaps to reach 9–10:
- Introduce a small set of additional “decision record” and “evidence packet” schemas and validate them in tests.

### BDD — 7.5
Strengths:
- Port behaviors and failure modes are explicit.
- S4 protocol is now a state machine with allowed transitions and blessed exit criteria.
- Doctrine includes explicit coupling rules and invariants.

Gaps to reach 9–10:
- Convert the highest-value behaviors into executable specs (even a small set) so BDD is not only narrative.

### TDD — 5.5
Strengths:
- Contract tests exist and pass.
- Mapping drift is tested.

Primary gap:
- Most behaviors are not yet covered by harness tests per port (P0 evidence packets, P1 adapters, P7 decision records, P5 quarantine/resurrection).

Fastest upgrades:
- Add golden fixtures + property tests for one port at a time (start with P1 adapters and P7 decision record + replay).

## Recommended next steps (Pareto)
1) Add a minimal “decision record” contract (P7) + a replay verifier gate.
2) Add a minimal “evidence packet” contract (P0) + a freshness/provenance test.
3) Add a “memory write-path guardrail” gate to fail builds if non-SSOT writes are attempted.
