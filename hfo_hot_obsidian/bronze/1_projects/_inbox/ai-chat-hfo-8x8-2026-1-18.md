# Medallion: Bronze | Mutation: 0% | HIVE: V

## 1-page executive summary: Alpha vs Omega

### Mission Thread Alpha (HFO infra / swarm OS)

**Short-term (ship-next):**

* Turn HFO into a *durable mission-engineering platform* where every action has **contracts + receipts + replayable evidence**.
* Standardize the **8 ports / roles** so specialists can operate with minimal cross-talk (ports/adapters, fail-closed gates, mutation/property testing, observability).
* Make “Phoenix rebuilds” safe: rebirths must reconverge on **SSOT + manifests + baton handoffs**.

**Long-term (end-state):**

* A verified, composable “swarm OS” that can:

  * Run AoA/DSE at scale (Pareto frontiers, MAP-Elites diversity archive).
  * Maintain a tri-temporal loop (Past/Present/Future) with auditability.
  * Enforce governance against reward-hacking (“green-but-meaningless”) via gates, receipts, and adversarial testing.

### Mission Thread Omega (gesture → pointer / Total Tool Virtualization)

**Short-term (ship-next):**

* A production-grade **gesture→pointer control plane**:

  * Hand tracking → shaping (smoothing/prediction) → **hard-gated anti-Midas FSM** → W3C Pointer Events → per-target injection adapters.
  * Measured SLOs (p95 latency/jitter, false activations, occlusion recovery), with record/replay harness.

**Long-term (end-state):**

* “Universal pointer ABI” for controlling *any* UI reliably, evolving to multi-sensor fusion (RGB/thermal/etc.) while preserving ports/adapters and fail-closed behavior.

---

## Does your summary match my memory?

Yes on the core: **Alpha = governance/orchestration backbone**, **Omega = gesture→pointer product/control plane**, and the stabilizers are **SSOT + baton handoff + receipts/replay**.

One correction/lock-in based on what you just specified:

* The **anti-diagonal dyads** are the HIVE/8 geometry you described:
  **P0+P7 = Hindsight/Hunt**, **P1+P6 = Insight/Interlock**, **P2+P5 = Validated Foresight/Validate**, **P3+P4 = Evolve/Evolve** — and you want an **alias system** so these are facets of one invariant truth (not separate frameworks). (Saved.)

---

## Research-grounded MCP selection rules for HFO

### “Best MCP” in practice means “most trustworthy + easiest to govern”

1. **Prefer official/vendor MCP servers** (Notion, Slack, Stripe, Atlassian, Figma) over random community servers when credentials or write-access are involved. ([Notion Developers][1])
2. **Treat MCP servers as code execution / data-exfiltration risk**; require Workspace Trust and explicit allowlists. VS Code explicitly warns that MCP servers can run arbitrary code and should only be used from trusted publishers. ([Visual Studio Code][2])
3. **Identity/credential governance matters more than the protocol** (avoid static over-privileged secrets; prefer OAuth/JIT/least privilege). ([TechRadar][3])

---

## Your 8 legendary commanders (P0 → P7) and what they should do

| Port | Commander        | Power word     | JADC2 domain           | “Eventually able to do” (capability end-state)                                                         |
| ---- | ---------------- | -------------- | ---------------------- | ------------------------------------------------------------------------------------------------------ |
| P0   | Lidless Legion   | **OBSERVE**    | ISR                    | Instrument everything; produce high-integrity sensor/telemetry streams + anomaly flags.                |
| P1   | Web Weaver       | **BRIDGE**     | Data Fabric            | Move data/contracts/events safely across boundaries; standardize envelopes, routing, provenance.       |
| P2   | Mirror Magus     | **SHAPE**      | Digital Twin           | Create/modify artifacts (prototypes, spikes, edits), mint variants/tokens, manage environment shaping. |
| P3   | Spore Storm      | **INJECT**     | Effect Delivery        | Deliver actions into targets via adapters; keep injection deterministic, app-specific, fail-closed.    |
| P4   | Harmonic Hydra   | **DISRUPT**    | Coevolution / Red Team | Adversarial testing + “venom payloads” (fuzz/mutation/chaos) to break weak assumptions safely.         |
| P5   | Pyre Praetorian  | **IMMUNIZE**   | Force Protection       | Safety governor: policy-as-code, permissioning, tripwires, rollback/kill-switch discipline.            |
| P6   | Kraken Keeper    | **ASSIMILATE** | AAR                    | Distill results into durable knowledge: receipts, rollups, evidence, frontier updates.                 |
| P7   | Spider Sovereign | **NAVIGATE**   | C2/BMC2                | Choose what to do next (AoA/DSE), allocate budget, manage WIP, prevent drift.                          |

---

## MCP “shards” for each commander (8 tools each)

Constraint applied:

* **4 shared Hive tools (max overlap = 4):**
  **Filesystem (internal), Git (internal), Fetch (external), GitHub (external)** ([GitHub][4])
* Each role gets **+4 specialized tools** (2 internal, 2 external) aligned to its domain.

### P0 — OBSERVE (ISR) | Lidless Legion

**Shared (2 internal / 2 external):** Filesystem, Git, Fetch, GitHub ([GitHub][4])
**Specialized internal:**

* **Playwright MCP** (instrument/verify UIs; capture evidence) ([Visual Studio Code][2])
* **Passage-of-time MCP** (time windows, cadence, “when did X happen”) ([GitHub][5])
  **Specialized external:**
* **Sentry MCP** (error/trace context as “ISR for software”) ([Model Context Protocol][6])
* **Brave Search MCP** (web ISR / current intel) ([GitHub][7])

### P1 — BRIDGE (Data Fabric) | Web Weaver

**Shared:** Filesystem, Git, Fetch, GitHub
**Specialized internal:**

* **NATS MCP** (event bus / stigmergy surface) ([GitHub][8])
* **PostgreSQL MCP** (ledger/contract store access) ([Reddit][9])
  **Specialized external:**
* **AWS Labs OpenAPI MCP** (bridge to arbitrary APIs via specs) ([GitHub][10])
* **Vercel MCP** (deploy/preview surface for web artifacts) ([PulseMCP][11])

### P2 — SHAPE (Digital Twin) | Mirror Magus

**Shared:** Filesystem, Git, Fetch, GitHub
**Specialized internal:**

* **DuckDB MCP** (local OLAP + “what changed” analytics) ([GitHub][12])
* **Temporal MCP** (durable workflows; replayable orchestration) ([npm][13])
  **Specialized external:**
* **Figma MCP** (design→code context for shaping UI artifacts) ([Figma][14])
* **Notion MCP** (shape specs/SSOT pages with controlled access) ([Notion Developers][1])

### P3 — INJECT (Effect Delivery) | Spore Storm

**Shared:** Filesystem, Git, Fetch, GitHub
**Specialized internal:**

* **Playwright MCP** (high-fidelity injection + E2E action evidence) ([Visual Studio Code][2])
* **Docker MCP toolkit/catalog** (standardize execution environment for injectors) ([Docker Documentation][15])
  **Specialized external:**
* **Stripe MCP** (payments/monetization actions without bespoke glue) ([Stripe Docs][16])
* **Slack MCP** (operational dispatch + notifications + human-in-the-loop) ([Slack Developer Docs][17])

### P4 — DISRUPT (Red Team) | Harmonic Hydra

**Shared:** Filesystem, Git, Fetch, GitHub
**Specialized internal:**

* **Playwright MCP** (break flows, detect regressions, collect repros) ([Visual Studio Code][2])
* **Grep MCP** (rapid codebase attack-surface search) ([Grep][18])
  **Specialized external:**
* **Sentry MCP** (incident-driven adversarial focus) ([Model Context Protocol][6])
* **Atlassian Rovo MCP** (target the real work graph: Jira/Confluence/Compass) ([Atlassian Support][19])

### P5 — IMMUNIZE (Force Protection) | Pyre Praetorian

**Shared:** Filesystem, Git, Fetch, GitHub
**Specialized internal:**

* **Temporal MCP** (policy gates as durable workflows; enforced approvals) ([npm][13])
* **PostgreSQL MCP** (policy/audit ledger, allowlists, receipts) ([Reddit][9])
  **Specialized external:**
* **Atlassian Rovo MCP** (audit logs + controlled client access in enterprise graph) ([Atlassian Support][19])
* **Slack MCP** (secure escalation + approvals in the comms plane) ([Slack Developer Docs][17])

### P6 — ASSIMILATE (AAR) | Kraken Keeper

**Shared:** Filesystem, Git, Fetch, GitHub
**Specialized internal:**

* **DuckDB MCP** (rollups, evidence queries, monthly/weekly digests) ([GitHub][12])
* **PostgreSQL MCP** (durable canonical facts + indices) ([Reddit][9])
  **Specialized external:**
* **Notion MCP** (publish “Gold” summaries to living docs) ([Notion Developers][1])
* **Linear MCP** (turn AAR into tracked work items; close the loop) ([Linear][20])

### P7 — NAVIGATE (C2/BMC2) | Spider Sovereign

**Shared:** Filesystem, Git, Fetch, GitHub
**Specialized internal:**

* **Temporal MCP** (mission cadence + durable decision workflows) ([npm][13])
* **Passage-of-time MCP** (timeboxed planning + horizon control) ([GitHub][5])
  **Specialized external:**
* **Linear MCP** (WIP control + roadmap steering) ([Linear][20])
* **Atlassian Rovo MCP** (portfolio view across Jira/Confluence/Compass) ([Atlassian Support][19])

---

## Two critical governance notes (non-optional for HFO)

1. **VS Code MCP trust gate:** only enable MCP servers from publishers you trust; MCP servers can execute code. ([Visual Studio Code][2])
2. **Avoid credential sprawl:** prefer OAuth/least-privilege; treat identity fragmentation as the primary systemic risk. ([TechRadar][3])

If you want the next step, I can convert the shard plan into:

* a **single JSON config shape** (client-agnostic) and
* a **rollout order** (P1 Bridge → P5 Immunize → P0 Observe → P6 Assimilate …) to keep blast radius low.

[1]: https://developers.notion.com/docs/get-started-with-mcp?utm_source=chatgpt.com "Connecting to Notion MCP"
[2]: https://code.visualstudio.com/docs/copilot/customization/mcp-servers "Use MCP servers in VS Code"
[3]: https://www.techradar.com/pro/mcps-biggest-security-loophole-is-identity-fragmentation?utm_source=chatgpt.com "MCP's biggest security loophole is identity fragmentation"
[4]: https://github.com/upstash/context7?utm_source=chatgpt.com "Context7 MCP Server -- Up-to-date code documentation for ..."
[5]: https://github.com/jlumbroso/passage-of-time-mcp?utm_source=chatgpt.com "\"Passage of Time\" Model Context Protocol (MCP) Server"
[6]: https://modelcontextprotocol.io/examples?utm_source=chatgpt.com "Example Servers"
[7]: https://github.com/brave/brave-search-mcp-server?utm_source=chatgpt.com "Brave Search MCP Server"
[8]: https://github.com/modelcontextprotocol/servers/tree/main/src/time?utm_source=chatgpt.com "Time MCP Servers"
[9]: https://www.reddit.com/r/mcp/comments/1jgw10w/knowledge_graph_memory_server_a_persistent_memory/?utm_source=chatgpt.com "Knowledge Graph Memory Server – A persistent ..."
[10]: https://github.com/getsentry/sentry-mcp-stdio?utm_source=chatgpt.com "Model Context Protocol (MCP) server for Sentry"
[11]: https://www.pulsemcp.com/servers/modelcontextprotocol-knowledge-graph-memory?utm_source=chatgpt.com "Knowledge Graph Memory MCP Server by Anthropic"
[12]: https://github.com/awslabs/mcp?utm_source=chatgpt.com "awslabs/mcp: AWS MCP Servers"
[13]: https://www.npmjs.com/package/%40modelcontextprotocol/server-memory?utm_source=chatgpt.com "@modelcontextprotocol/server-memory"
[14]: https://www.figma.com/blog/introducing-figma-mcp-server/?utm_source=chatgpt.com "Introducing our MCP server: Bringing Figma into your ..."
[15]: https://docs.docker.com/ai/mcp-catalog-and-toolkit/?utm_source=chatgpt.com "Docker MCP Catalog and Toolkit"
[16]: https://docs.stripe.com/mcp?utm_source=chatgpt.com "Model Context Protocol (MCP)"
[17]: https://docs.slack.dev/ai/mcp-server/?utm_source=chatgpt.com "Slack MCP server overview | Slack Developer Docs"
[18]: https://grep.app/?utm_source=chatgpt.com "Code Search | Grep by Vercel"
[19]: https://support.atlassian.com/atlassian-rovo-mcp-server/docs/use-atlassian-rovo-mcp-server/?utm_source=chatgpt.com "Use Atlassian Rovo MCP Server"
[20]: https://linear.app/docs/mcp?utm_source=chatgpt.com "MCP server – Linear Docs"
---

## What you’re aiming for (8 shards = an “apex, pareto” tile-stack)

A **JADC2 / Mosaic Warfare** software-engineering “complete team” with 8 specialist commanders should cover, with minimal bespoke glue:

1. **Truth/SSOT** (code + data)
2. **Change execution** (build/test/deploy + browser/E2E)
3. **Observability + incident response**
4. **Work/knowledge flow** (tickets/docs/chat)
5. **Governance / safety gates** (fail-closed constraints)
6. **Planning / reasoning discipline** (structured decomposition)

MCP is the transport: VS Code (Copilot) can run MCP servers as tool backends in a standard client/server setup. ([Visual Studio Code][1])

---

## The “core 4” shared across *all* shards (high ROI, low regret)

These are the minimum common substrate; everything else is role specialization.

1. **Filesystem MCP** (controlled local read/write with access controls/roots) ([Awesome MCP Servers][2])
2. **Git MCP** (local repo introspection / diffs / history) ([playbooks][3])
3. **DuckDB ↔ MCP** (your SSOT analytics spine; can expose/query data via MCP) ([DuckDB][4])
4. **Sequential Thinking MCP** (forces structured stepwise reasoning, useful for all roles) ([npm][5])

This keeps overlap intentionally capped while still giving every commander the same “ground truth + disciplined reasoning” foundation.

---

## The 8 commanders as “shards” (each leads a swarm)

Below: **4 internal + 4 external** per shard. Internal = local/SSOT tools; External = network/SaaS tools. I’m using **first-party** MCPs where available (GitHub, Atlassian, Notion, Sentry, Microsoft Playwright). ([GitHub][6])

### P0 — Lidless Legion (OBSERVE | ISR)

**Purpose:** instrument reality; gather signals; detect drift early.

* **Internal (add to core 4):**

  * DuckDB MCP queries for telemetry rollups (SSOT evidence)
  * Filesystem “evidence locker” (append-only logs/receipts)
  * Git history mining (when did it change?)
  * Memory KG MCP (optional, if you want entity/relations) ([npm][7])
* **External (role-unique):**

  * **Playwright MCP** for “what the UI actually does” probes ([GitHub][8])
  * **Sentry MCP** for errors/traces/issues as ground truth ([Sentry Documentation][9])
  * **GitHub MCP** for repo/PR/issue reality (hosted option exists) ([GitHub][6])
  * Slack MCP (only if you treat chat as an ISR channel) ([GitHub][10])

### P1 — Web Weaver (BRIDGE | Data Fabric)

**Purpose:** connect systems; standardize envelopes; make data flow reliable.

* **Internal:**

  * DuckDB MCP (schemas, lineage tables, medallion rollups)
  * Filesystem MCP (schema registry + contract files)
  * Git MCP (contract diffs / versioning)
  * Memory MCP (entity graph for contracts/services) ([npm][7])
* **External (role-unique):**

  * **Atlassian Rovo MCP** (Jira/Confluence as the “fabric” surface) ([GitHub][11])
  * **Notion MCP** (lightweight knowledge transport / specs) ([Notion Developers][12])
  * GitHub MCP (issues/PRs as integration endpoints) ([GitHub Docs][13])
  * Slack MCP (broadcast/subscribe operational comms) ([GitHub][14])

### P2 — Mirror Magus (SHAPE | Digital Twin)

**Purpose:** prototypes/spikes/edits; mint tokens/variants; maintain the “twin” of system state.

* **Internal:**

  * Git MCP (branching, diffs, reversible edits)
  * Filesystem MCP (scaffolds, golden fixtures, receipts)
  * DuckDB MCP (digital twin state tables, replay indexes)
  * Sequential Thinking MCP (design decomposition discipline) ([npm][5])
* **External (role-unique):**

  * GitHub MCP (PR automation + review workflows) ([GitHub][6])
  * Notion MCP (design docs you can regenerate from SSOT) ([Notion Developers][12])
  * Playwright MCP (validate the twin against real UI) ([GitHub][8])
  * Sentry MCP (shape fixes from live failure signals) ([Sentry Documentation][9])

### P3 — Spore Storm (INJECT | Effect Delivery)

**Purpose:** deliver actions into targets (your per-target adapters, pointer ABI, etc.).

* **Internal:**

  * Filesystem MCP (adapter configs + target surface contracts)
  * Git MCP (versioned injection strategies; rollback)
  * DuckDB MCP (effect logs + replay evidence)
  * Sequential Thinking MCP (safe execution checklists) ([npm][5])
* **External (role-unique):**

  * Playwright MCP (E2E action delivery + assertions) ([GitHub][8])
  * GitHub MCP (CI triggers, PR merges gated by evidence) ([GitHub Docs][13])
  * Atlassian MCP (deployment tasks tied to tickets/runbooks) ([GitHub][11])
  * Slack MCP (operator notifications / human-in-loop gates) ([GitHub][10])

### P4 — Harmonic Hydra (DISRUPT | Coev Red Team “durable venom”)

**Purpose:** adversarial testing, chaos, exploit finding; durable nematocyst payloads.

* **Internal:**

  * Git MCP (fault injection branches, mutation diffs)
  * Filesystem MCP (fuzz corpora, chaos knobs, failure artifacts)
  * DuckDB MCP (failure clustering, exploit taxonomy)
  * Sequential Thinking MCP (threat modeling / pre-mortems) ([npm][5])
* **External (role-unique):**

  * Playwright MCP (adversarial UI exploration) ([GitHub][8])
  * Sentry MCP (verify failures are real + measurable) ([Sentry Documentation][9])
  * GitHub MCP (security/CI integration points) ([GitHub][6])
  * Slack MCP (red-team incident drills / comms) ([GitHub][14])

### P5 — Pyre Praetorian (IMMUNIZE | Force Protection)

**Purpose:** guardrails; least privilege; fail-closed constraints; policy enforcement.

* **Internal:**

  * Filesystem MCP with strict roots (deny-by-default) ([Awesome MCP Servers][2])
  * Git MCP (policy-as-code diffs, attestations)
  * DuckDB MCP (compliance evidence, audit trails)
  * Memory MCP (store invariants / “never again” rules) ([npm][7])
* **External (role-unique):**

  * Sentry MCP (monitor regressions / safety incidents) ([Sentry Documentation][9])
  * GitHub MCP (branch protection / workflow enforcement surface) ([GitHub Docs][13])
  * Atlassian MCP (security runbooks / approvals) ([GitHub][11])
  * Notion MCP (policy manuals / controlled playbooks) ([Notion Developers][12])

### P6 — Kraken Keeper (ASSIMILATE | AAR)

**Purpose:** after-action review; convert raw traces into lessons; keep the medallion lake coherent.

* **Internal:**

  * DuckDB MCP (primary assimilation engine) ([DuckDB][4])
  * Filesystem MCP (ingest receipts, logs, artifacts)
  * Git MCP (map lessons to commits/releases)
  * Memory MCP (entity graph of incidents/lessons) ([npm][7])
* **External (role-unique):**

  * Sentry MCP (incident source of truth) ([Sentry Documentation][9])
  * GitHub MCP (link incidents ↔ PRs ↔ releases) ([GitHub][6])
  * Atlassian MCP (AAR tickets + knowledge capture) ([GitHub][11])
  * Notion MCP (publish “gold” summaries) ([Notion Developers][12])

### P7 — Spider Sovereign (NAVIGATE | BMC2/C2)

**Purpose:** orchestration, prioritization, resource allocation; keep Alpha/Omega aligned and reversible.

* **Internal:**

  * DuckDB MCP (portfolio state, queues, metrics)
  * Git MCP (rollbacks, release coordination)
  * Filesystem MCP (mission intents, SOPs, runbooks)
  * Sequential Thinking MCP (planning + trade studies) ([npm][5])
* **External (role-unique):**

  * GitHub MCP (coordination across repos/projects) ([GitHub][6])
  * Atlassian MCP (program-level C2: epics, dependencies) ([GitHub][11])
  * Slack MCP (C2 broadcast + command acknowledgments) ([GitHub][10])
  * Notion MCP (high-level doctrine / strategy pages) ([Notion Developers][12])

---

## Why this is “pareto” (in your terms)

* **Low bespoke glue:** everything is a standard MCP tool boundary; VS Code supports MCP as a unified tool interface. ([Visual Studio Code][1])
* **SSOT-first:** DuckDB is the spine; DuckDB MCP exists as an integration surface. ([DuckDB][4])
* **Truth via execution:** Playwright MCP gives you “what happened” evidence, not just reasoning. ([GitHub][8])
* **Production-grade feedback loop:** Sentry MCP makes failures first-class inputs. ([Sentry Documentation][9])
* **Enterprise knowledge flow:** Atlassian + Notion MCP cover tickets/docs with OAuth-oriented remote servers. ([GitHub][11])
* **Reversibility + governance:** GitHub MCP supports repo/PR/issue workflows, including hosted configuration routes. ([GitHub][6])

If you want the next step, the right “geometry move” is: **freeze the shared core-4**, then pick **exactly 2 external SaaS surfaces to start** (usually GitHub + Playwright), and add the others only when the role’s KPIs demand them.

---
