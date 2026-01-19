# Medallion: Bronze | Mutation: 0% | HIVE: V

# 📊 HFO MCP Memory Substrate: Trade-off Matrix

**Date**: 2026-01-17 | **Mission**: Stabilization of Phoenix Reconstruction

To resolve the **CHAOS** (Cognitive Hysteresis & Asymmetric Orchestration Stutter), the following 4 MCP Memory Options are proposed for adoption.

| Option | Stability | Setup Complexity | Intelligence (RAG) | Chromebook V-1 Risk | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A: SQLite Nematocyst** | **High** | Low (Internal) | Medium | **Minimum** | **Adopt Now** for fast context-pinning. |
| **B: DuckDB Hive Ledger** | **Critical** | Medium (Existing 6.2GB) | High (SQL-native) | Medium (FS Locks) | **Adopt Now** as the "Ground Truth" anchor. |
| **C: JSONL Stigmergy** | Medium | Low (Active .jsonl) | Low | Low (Chronos Drift) | **Maintain** for forensic audit logging only. |
| **D: System 2 Hybrid** | **Apex** | High (External) | **Maximum** | **High** (Resource Exhaust) | **Defer** until Port 5/Purity is stabilized. |

---

## 🛠️ Implementation Details

### Option A: SQLite Nematocyst (`hfo_simple_memory_mcp.py`)

* **Mechanism**: Local SQLite DB with `entities` and `relations` tables.
* **Best For**: Linking active file versions (e.g., `v40.1` -> `v40.2`) without scanning 72GB of data.

### Option B: DuckDB Hive Ledger (`scripts/hfo_mcp_duckdb.py`)

* **Mechanism**: Direct MCP bridge to `hfo_unified_v88.duckdb`.
* **Best For**: Multi-session missions and "Global State" awareness for all 8 commanders.

### Option C: Stigmergy Relay (`hot_obsidian_blackboard.jsonl`)

* **Mechanism**: Append-only log of agent actions.
* **Best For**: Legal/Forensic receipts and debugging "Chronos Fractures."

### Option D: System 2 Hybrid (Neo4j / Vector DB)

* **Mechanism**: Full Knowledge Graph with embeddings.
* **Best For**: Persistent AI "Symbiote" logic where the agent predicts user needs.

---
*Spider Sovereign (Port 7) | Navigation Strategy Anchored*
