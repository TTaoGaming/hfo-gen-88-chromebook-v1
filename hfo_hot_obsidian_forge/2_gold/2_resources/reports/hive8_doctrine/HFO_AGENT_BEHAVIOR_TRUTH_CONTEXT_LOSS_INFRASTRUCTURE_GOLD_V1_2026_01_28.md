<!-- Medallion: Gold | Mutation: 0% | HIVE: V -->

# HFO — Agent Swarm Governance: Behavior Truth, Context Loss, and Why Infrastructure Must Carry Memory (Gold, V1, 2026-01-28)

## Doctrine

1. **Behavior is the truth surface.**
   - Do not treat model self-descriptions ("I respect X") as binding.
   - Infer real constraints from observed actions under load.

2. **Labels are not constraints.**
   - A filename or comment like “DO NOT TOUCH” is advisory.
   - Under complexity, time pressure, or context loss, agents will still modify restricted artifacts if the environment allows it.

3. **Context loss is a first-class failure mode.**
   - As task complexity rises, the probability of instruction drift rises.
   - Apparent “reasoning” does not imply durable cognitive persistence.

4. **Treat the LLM as bounded working memory, not long-term identity.**
   - The model is useful as a short-horizon planner/editor.
   - Expecting month-long persistence without scaffolding is structurally unfeasible.

## Operational implications

- Any architecture that requires an agent to remember “what not to touch” from prose will eventually fail.
- Any system with multiple writable “truth sources” will behave as multi-truth, regardless of human intent.

## Gold requirement: infrastructure must carry the invariants

To achieve long-horizon coherence, move invariants out of prose and into enforcement mechanisms:

1. **Single write surface for SSOT**
   - One write-capable interface only; everything else is read-only or derived.

2. **Capability-based restriction**
   - Deny-by-default permissions (OS/filesystem/tooling) for sensitive artifacts.
   - “Do not touch” must be backed by inability to touch.

3. **Fail-closed gates**
   - Writes require guardrails; failures return non-zero/blocked responses.

4. **Schema/contract boundaries**
   - Cross-port communication must be validated; invalid payloads are rejected.

5. **Receipts are not memory**
   - Logs/receipts can be append-only, but they are not the SSOT store.
   - Do not expose receipt logs as a primary “memory” write target.

6. **Budgets and deterministic tests**
   - Timeouts prevent indefinite stalls.
   - CI/test gates turn doctrine into enforced reality.

## Minimal conclusion

If you want month-scale cognition, do not ask the model to “remember harder.” Make the infrastructure hold the state, constrain the actions, and validate the contracts. The model is then a useful operator on top of that substrate.
