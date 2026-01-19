# Medallion: Bronze | Mutation: 0% | HIVE: I

# 🏗️ HFO Gen 88: Hybrid Memory Substrate Integration Plan (V1.0)

**Date**: 2026-01-17
**Mission Thread**: Alpha (Orchestration & Bootstrapping)
**System Components**: MCP v2.1 + Akka Agentic v1.5 + DuckDB v1.2

---

## 🎯 Executive Summary

Transition the current Python-based stubs into a hardened, reactive actor system (Akka) that utilizes a universal sensor/tool bridge (MCP) and maintains local analytical persistence (DuckDB). This satisfies the JADC2 requirement for **Persistent Sense-MakeSense-Act** loops.

---

## 🏗️ 1. Architecture: The 8-Port Hybrid Stack

### Port 0-1 (SENSE/BRIDGE) -> **MCP (Model Context Protocol)**

- **Role**: Standardized adapter for MediaPipe landmarks, system telemetry, and external tool calls.
- **Integration**: Deploy an MCP Server using the Python SDK.
- **Benefit**: Decouples sensor logic from orchestration. MediaPipe becomes a "Tool" in the MCP registry.

### Port 7 (NAVIGATE) -> **Akka Agentic Platform**

- **Role**: State management and durable orchestration.
- **Integration**: Replace the `hfo_spider_sovereign_daemon.py` loop with an **ActorSystem**.
- **Actors**:
  - `NavigatorActor` (P7): Primary mission lead.
  - `SenseActor` (P0/P1): Polls the MCP bridge.
  - `DefenseActor` (P5): Monitors invariants and executes Pyre cycles.
- **State**: Actors use Akka Persistence to store state snapshots between cycles.

### Port 6 (STORE) -> **DuckDB Local Substrate**

- **Role**: Forensics, telemetry retrieval, and cold-starts.
- **Integration**: Actors pipe their event streams (`CHANT`) into `.parquet` files or the unified `hfo_unified_v88.duckdb`.
- **Retrieval**: P7 `NavigatorActor` queries DuckDB via SQL to determine historical context ("What was the hand velocity 30s ago?").

---

## 🚀 2. Implementation Roadmap

### Phase 1: The MCP Bridge (P0/P1)

1. **Initialize MCP Server**: Create `hfo_mcp_sensor_server.py`.
2. **Tool Registration**: Register MediaPipe-to-UPE projection as an MCP Tool.
3. **Connection**: Enable the VS Code MCP interface to "see" the Python landmarks.

### Phase 2: Akka Actor Manifest (P7)

1. **Define Protobufs**: Create `hfo_gen88_messages.proto` for actor communication.
2. **Core Actor Implementation**: Implement `HardenedBaseActor` in `hfo_gen_88_cb_v2/actors/`.
3. **Durable State**: Configure the DuckDB event journal.

### Phase 3: DuckDB Analytics (P6)

1. **Schema Hardening**: Finalize `FusionSchema` in SQL.
2. **Forensic Dashboard**: Connect the Hub Port 5 to query DuckDB for "slop" detection (Detecting non-deterministic jitter).

---

## 🛡️ 3. Port 5 (DEFEND) Policy

- **BFT Interlock**: Akka clusters must reach 3/3 consensus for Port 7 "COMMIT" missions.
- **Chronos Integrity**: Every DuckDB entry must be signed by the `ValidatorActor`.
- **Slop Sentinel**: Automated rejection of any non-actor background processes.

---
*Spider Sovereign (Port 7) | Gen 88 Integration Plan*
