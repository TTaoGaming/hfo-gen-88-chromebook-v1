# Medallion: Gold | Mutation: 100% | HIVE: V
# 🧊 HFO Cold Start Protocol: Chromebook V-1

**Mission**: Phoenix Project Resurrection
**Source Truth**: `hfo_cold_obsidian/`
**Target Substrate**: `hfo_hot_obsidian/`

---

## 🛠️ The Procedure

### 1. Initialization
- Verify `git` status and `pre-commit` hooks.
- Validate local `.venv` and Python dependencies.
- Read `hot_obsidian_blackboard.jsonl` for the last known state.

### 2. Warming the Bronze
- Moving code from `hfo_cold_obsidian/bronze` to the active workspace.
- **Rules**:
    - Never copy "Silver" or "Gold" directly into a cold environment without a Bronze "cooling" test phase.
    - All logic must pass **Zod 6.0** contract validation upon ingestion.
    - If a component has < 88% mutation score, it MUST be hardened in the local environment before integration.

### 3. HIVE Sync
- Every major logic ingestion must be logged to the blackboard.
- Format: `{"timestamp": "...", "phase": "H", ..., "pX": {"status": "warming", "component": "xyz"}}`

---

## 🗺️ Commander Mapping (Medallion Compliance)

| Commander | Medallion Layer  | Cold Source Path | Hot Destination Path             |
| :-------- | :--------------- | :--------------- | :------------------------------- |
| P0 SENSE  | Bronze           | `bronze/p0/...`  | `hfo_hot_obsidian/bronze/p0/...` |
| P1 FUSE   | Silver-to-Bronze | `bronze/p1/...`  | `hfo_hot_obsidian/bronze/p1/...` |

---
*Spider Sovereign (Port 7) | Protocol V1.0*
