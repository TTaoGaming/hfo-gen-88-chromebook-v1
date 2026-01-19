# Medallion: Bronze | Mutation: 0% | HIVE: V

## 4 best improvements (and why)

1. **Make observations structured (KV + status + confidence + provenance)**

* **Why:** Free-text observations drift, can’t be reliably queried, diffed, or linted. Adding `k/v`, `status` (`confirmed|unconfirmed|deprecated`), `confidence`, and `src` lets you enforce “zero trust” and run integrity checks.

2. **Explicit aliasing + canonicalization for names**

* **Why:** You already have a live collision (`Commander_P3`: “Spore Storm” vs “Harmonic Hydra”). Without an alias model, retrieval fragments, and Copilot will hallucinate whichever is most salient. Canonical name + alias edges + provenance prevents semantic split-brain.

3. **Graph integrity rules + CI lint (hard gates)**

* **Why:** Your schema implies invariants (each port must have one power word, one commander, one JADC2 mapping; Litany must be 8 lines). Encode those as DuckDB queries that fail CI so drift is caught immediately.

4. **Evidence objects become first-class with typed fields**

* **Why:** Your month evidence nodes are strong, but still text blobs. Converting to typed fields (`count`, `method`, `sample_paths[]`, `source_doc`) makes them auditable, comparable across runs, and usable for trend dashboards.

---

## Matrix trade study (4 improvements)

**Scoring:** 1 (worst) → 5 (best)

| Improvement                                      | What changes                                                                       | Value to you (zero-trust) | Implementation cost | Risk of breaking existing data | Ongoing maintenance | DuckDB queryability | Key downside                                                      |
| ------------------------------------------------ | ---------------------------------------------------------------------------------- | ------------------------: | ------------------: | -----------------------------: | ------------------: | ------------------: | ----------------------------------------------------------------- |
| **A. Structured observations (KV + provenance)** | `observations: ["text"]` → `observations: [{"k","v","src","status","confidence"}]` |                     **5** |                   3 |                              3 |                   2 |               **5** | Requires migration/backfill or dual-format support                |
| **B. Canonical name + alias model**              | Add `canonical_name` + `alias_of` edges or alias list w/ sources                   |                     **5** |                   2 |                              2 |                   2 |               **4** | Requires discipline to avoid adding new “near-duplicate” entities |
| **C. Graph integrity rules + CI lint**           | Add DuckDB “lint queries” and fail build on violations                             |                     **5** |                   2 |                          **1** |               **1** |               **4** | Needs clear invariants; too strict early can annoy you            |
| **D. Typed evidence records**                    | Convert month evidence blobs → fields (`count`, `method`, `samples`, `run_id`)     |                     **4** |                   3 |                              2 |                   2 |               **5** | More schema to maintain; must version evidence runs               |

---

## Recommendation (Pareto pick)

If you do only **two** first:

1. **C. Integrity rules + CI lint** (highest value, lowest risk, cheap)
2. **B. Canonical + alias model** (stops immediate split-brain)

Then:
3) **A. Structured observations** (big long-term payoff, moderate migration cost)
4) **D. Typed evidence** (turns your forensics into real analytics)

---

## Minimal acceptance criteria for each (so it’s enforceable)

* **A:** At least 80% of observations are KV objects; any plain-text observation must include `status="unstructured"` and `src`.
* **B:** Any entity with multiple names must have one canonical and all others as aliases with `src` and `status`.
* **C:** CI fails if any `Port_*` lacks exactly one commander/power word, or if any commander lacks a JADC2 mapping; Litany must include P0–P7.
* **D:** Every evidence node must include `method`, `count`, and at least 1 `sample_path`, plus `run_id`.

If you want, I can output the exact DuckDB lint SQL and a JSONL “v2 schema” example for one port/commander/evidence node.
