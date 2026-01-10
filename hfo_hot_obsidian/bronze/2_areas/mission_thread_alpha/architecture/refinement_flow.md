# Medallion: Bronze | Mutation: 0% | HIVE: I
# 🏗️ Refinement Flow: 1-Way Medallion Transition

This document defines the mandatory 1-way refinement flow for code promotion within the HFO Gen 88 ecosystem.

## 🌊 The Flow (High-Level)
1.  **HOT BRONZE** (`hfo_hot_obsidian/bronze/`): Kinetic development, prototyping, and raw logic.
2.  **COLD BRONZE** (`hfo_cold_obsidian/bronze/`): Hardened logic. Requires a **Freeze Receipt**.
3.  **HOT SILVER** (`hfo_hot_obsidian/silver/`): Integration-ready code. Requires a **Mutation Receipt** (Stryker 88%+).

---

## 🛠️ Layer Transitions

### 1. HOT BRONZE ➔ COLD BRONZE (Freeze)
- **Constraint**: Code is finalized but not yet mutation-tested.
- **Artifact**: `[filename].receipt.json`
- **Utility**: `p5_defend/freeze_to_cold.py`
- **Requirements**:
    - Provenance Header (Bronze).
    - No syntax errors (Pylance).
    - File hash recorded in receipt.

### 2. COLD BRONZE ➔ HOT SILVER (Mutation)
- **Constraint**: Code must be proven resilient against regression.
- **Artifact**: `[filename].mutation.json`
- **Utility**: `p5_defend/promote_to_silver.py`
- **Requirements**:
    - Stryker/Mutation score: **88% - 98% (Goldilocks Zone)**.
    - Property-based tests passed.

---

## 🛡️ Enforcement (P5 DEFEND)
The [P5 MEDALLION GUARD](hfo_hot_obsidian/bronze/2_areas/p5_defend/medallion_guard.py) enforces these transitions at commit-time.
- Any file in `hfo_cold_obsidian` WITHOUT a valid receipt will be **Quarantined**.
- Any file in `hfo_hot_obsidian/silver` WITHOUT a valid Goldilocks mutation receipt will be **Quarantined**.

---
*Spider Sovereign (Port 7) | Gen 88 Refinement*
