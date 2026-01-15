# 🥉 BRONZE HUB: Single Source of Truth (SSOT)

**Operational Mode**: 8-Port High-Level Concurrency  
**Medallion Level**: L2 (Cold Bronze)  
**System Target**: 6.3Gi RAM Hardware Optimization (TSP)

---

> [!CAUTION]
> ### 🚨 RED WARNING: DAEMON INTEGRITY MANDATE
> Every Port (P0-P7) **MUST** have at least one active background Daemon online at all times to maintain Hive Coherence. Even if a Port's logic is "Simplified" or in "Stub Mode," the thread must exist to preserve the 8x Concurrency Pattern. **Zero Dead Ports Allowed.**

---

## 🛸 The 8-Port Concurrency Grid
The HFO Manifold operates via **8 Legendary Commander Singletons** (P0-P7) running on the **Thrift Shard Protocol (TSP)**.

| Port | Commander | Mission | Daemon Path | Status |
| :--- | :--- | :--- | :--- | :--- |
| **P0** | **Lidless Legion** | ISR / System Vitality | `hfo_p0_lidless_daemon.py` | **🟢 ACTIVE** |
| **P1** | **Blight Bringer** | Schema / AI-Slot | `hfo_p1_blight_daemon.py` | 🟡 PENDING |
| **P2** | **Crystalline Hive**| Storage / Vector | `hfo_p2_crystal_daemon.py` | 🌑 STUB |
| **P3** | **Spore Storm** | Prototyping | `hfo_p3_spore_daemon.py` | 🌑 STUB |
| **P4** | **Red Regnant** | Governance / Policy | `hfo_p4_regnant_daemon.py` | 🌑 STUB |
| **P5** | **Shadow Sliver** | Security / Stealth | `hfo_p5_shadow_daemon.py` | 🌑 STUB |
| **P6** | **Kraken Keeper** | **Assimilation / SSOT** | `hfo_p6_kraken_daemon.py` | **🔥 ACTIVE** |
| **P7** | **Prime Sliver** | Replication / Quine | `hfo_p7_prime_daemon.py` | 🌑 STUB |

---

## 🏛️ Commander Singleton Architecture
### Core Hierarchy
1.  **Commander (The Singleton)**: The P{N} logic core and unique identity.
2.  **Daemons (The Kinetic Arms)**: Persistent background processes (using `nohup` or `isBackground=true`). 
3.  **Shards (The Workers)**: Individual execution units (LLM calls, DuckDB commits, File I/O) managed by the Daemon.

### Orchestration ROE (Bronze)
- **Non-Blocking**: All heavy I/O (Ingestion, Hashing, FTS) must run in the background.
- **Transactional**: Atomic commits (DuckDB `BEGIN/COMMIT`) are mandatory to prevent state corruption.
- **Boot Order**: P0 Sentinel (First) -> P6 Kraken (Second) -> Others (Concurrent).

---

## 🪶 Thrift Shard Protocol (TSP)
Strict resource boundaries to ensure 8-fold concurrency on constrained hardware.

### Guardrails
- **RAM Caps (RSS)**:
    - **P0 Daemon**: < 50MB RAM (Telemetry).
    - **General Daemons**: < 150MB RAM.
    - **P6 (Kraken)**: < 500MB (Heavy Payload Exception).
- **Adaptive Tick-Rate**: Daemons must use a **Sleep-and-Pulse** loop (e.g., wake every 60s or 600s) to keep CPU low.
- **Graceful Degeneracy**: If **P0 Lidless Legion** signals `MEMORY_CRITICAL`, all Thrift Shards must checkpoint and hibernate within 5 seconds.

---

*Verified for Gen 88 | Medallion: Bronze | 2026-01-15*
*Contact: Mission Control [v1.0.ssot]*
