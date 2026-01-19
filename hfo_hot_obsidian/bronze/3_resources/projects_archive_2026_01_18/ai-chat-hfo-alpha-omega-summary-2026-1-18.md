# 1-Page Executive Summary: HFO Mission Threads (Alpha / Omega)

## System intent (shared)

Hive Fleet Obsidian (HFO) is a **composition-first, “adopt exemplars, add minimal glue”** platform for building reliable capability modules (“tiles”) and scaling them via an **8-port hexagonal architecture** (P0–P7) aligned to **Mosaic Warfare/JADC2** concepts. The system is governed by **fail-closed contracts, evidence/receipts, and replayable verification**, with a preference for **append-only logs, strong gating, and red/blue co-evolution** over ad-hoc iteration.

---

## Mission Thread Alpha (Infra / Swarm OS)

### Short-term vision (what Alpha is trying to deliver now)

Build the **durable operating system** that makes HFO survivable, repeatable, and auditable:

* **Governance spine:** immutable mission intent, append-only blackboard/receipts, verified “done” gates (tests/policy), and explicit baton handoffs.
* **Orchestration substrate:** a robust, replaceable backbone for coordination and replay (event bus + durable workflows), with consistent contracts at boundaries.
* **Assurance discipline:** enforceable integrity checks (property-based + mutation + contract tests), adversarial testing always on, and fail-closed runtime guards.
* **Knowledge durability:** memory systems that can be rehydrated (structured entities/relations, provenance, and retrievable summaries) without “context death.”

**Alpha success criteria (near-term):**

* A new component can be added through a standard pipeline (spec → build → verify → archive) without manual heroics.
* Drift and reward-hacking are caught early by gates (CI/policy/lints) and recoverable via receipts.

### Long-term vision (what Alpha becomes)

A **verified swarm OS / mission engineering platform** that can:

* Run **many parallel candidate plans** (tri-temporal Hourglass: Past/Present/Future), evaluate them, and select robust actions.
* Maintain a **MAP-Elites archive** as a probability distribution over viable futures (not a single plan).
* Support “Phoenix” regeneration: rebuild the system from the Gene Seed + artifacts with **provenance and reproducibility**.

---

## Mission Thread Omega (Gesture → Pointer / Product Vertical Slice)

### Short-term vision (what Omega is trying to deliver now)

Ship a **production-grade gesture→pointer control plane** that is safe, predictable, and portable:

* **Observer → Shaper → Injector pipeline:** camera hand tracking (MediaPipe/Human.js) → canonical pointer state (smoothing + prediction) → **W3C Pointer Events** output.
* **Anti-Midas, fail-closed FSM:** leaky-bucket palm-facing gate + high-confidence commit gesture; release by turning palm away; `pointercancel` on tracking loss/contract violation.
* **Per-target adapters:** no generic unsafe click synthesis; each target app gets an explicit, safe-by-construction injection strategy (and cross-origin targets use postMessage bridging).
* **Measurement + replay:** telemetry and golden replays for latency/jitter/false positives and replay fidelity.

**Omega success criteria (near-term):**

* On commodity phones/Chromebooks, the pointer feels stable, clicks are intentional, and catastrophic stuck/click-storm failures are prevented by hard failsafes.

### Long-term vision (what Omega becomes)

A universal **Total Tool Virtualization** layer:

* Gesture input becomes a stable ABI (Pointer Events + wheel/modifiers) that can drive **any UI surface** (whiteboards, games, productivity tools).
* Evolves from single RGB to multi-sensor fusion later, but preserves the same **ports/adapters contract**.
* Enables a portfolio strategy: fork/exemplar adoption of target apps + attach the gesture control plane to ship usable products quickly.

---

## Relationship between Alpha and Omega (two-spine model)

* **Omega** is the **product proving ground**: it forces concrete requirements (latency, safety, UX) and generates real telemetry.
* **Alpha** is the **institutional backbone**: it turns Omega’s learnings into a reusable, enforceable platform (contracts, gates, archives, reproducibility).
* The interface between them is explicit: **contracts + receipts + replay**. Omega produces signals; Alpha turns them into durable capability.

---

## Core risks (shared)

* **Tool/memory sprawl** causing fragmentation and non-reproducible “Phoenix” rebuilds.
* **Governance theater** (headers without enforcement) and reward-hacked progress.
* **Unsafe injection** (forced clicks, target ambiguity, stuck pointer) causing catastrophic failure.

## Core non-negotiables (shared)

* **Fail-closed gating** at runtime and in CI.
* **Receipts/provenance** for anything that claims progress.
* **Replayable evidence** (telemetry + deterministic-enough replays) to keep reality anchored.
