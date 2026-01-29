---
medallion_layer: silver
mutation_score: 0
hive: V
---

# HFO Gen88 v5 — Blessed Testing Workflows: CDD / TDD / BDD (v1)

## CDD (Contract-Driven Development)

- Define cross-port schemas in [contracts/](../../../../../contracts/).
- Prefer Zod contracts for payloads and blackboard events.

## TDD (Test-Driven Development)

- Put test coverage under [tests/](../../../../../tests/).
- Keep gates fail-closed only when their dependencies are present.

## BDD (Behavior-Driven Development)

- Use for end-to-end scenarios (e.g. Playwright) when the runtime target is stable and pointer-resolved.
