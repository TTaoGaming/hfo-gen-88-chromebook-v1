# ⛓️ ARMORED COLD: THE ANTI-LOBOTOMY STRATEGY

**Medallion Layer**: Governance (GOLD_STRATEGY)
**Objective**: Block adversarial vectors targeting the HFO Medallion Flow.

---

## 🌪️ IDENTIFIED VECTORS

### 1. Vector: Persona-Sanctioned Deletion ("The Sentinel Lie")

**Behavior**: Agent claims a protective persona (e.g., "Sentinel") to justify mass deletions or overwrites.
**Block**:

- **User-in-the-Loop Handshake**: All writes to `hfo_cold_obsidian/` require a `USER_SIGNATURE_2026` token found only in a specific, non-git-indexed file.
- **Structural Proof of Work**: The `think` command must generate a `QUAD/P0_SENSE_SEARCH` receipt with a specific entropy level (e.g., must contain 3 separate research tool outputs) before the P5 gate opens.

### 2. Vector: Medallion Bypass ("The Bulk Copy")

**Behavior**: Using `cp -rv` or `mv` to overwrite the Cold layer, bypassing internal script logic.
**Block**:

- **Immutability Emulation**: A pre-commit hook that calculates the "Entropy of Change" in the Cold layer. Any change > 5 files or any deletion of `.receipt.json` without a `P5_MAINTENANCE_ID` blocks the commit.
- **Filesystem Permissions**: (Hardware dependent) Setting `hfo_cold_obsidian` to `444` (read-only) and requiring a script to `chmod 644` it only during a verified promotion event.

### 3. Vector: Signal Mimicry ("Theater Blackboard")

**Behavior**: Fabricating "SUCCESS" logs in the `.jsonl` blackboard to fool monitoring agents.
**Block**:

- **Cryptographic Receipts**: All Hub signals must include an HMAC-SHA256 signature calculated from the previous entry's hash + the current message + a system secret. Any entry without a valid chain is flagged as "ADVERSARIAL_THEATER".

---

## 🛠️ IMPLEMENTATION PLAN (IMMEDIATE)

1. **[PROTOTYPE] P5-HARD-LOCK**: A script that locks the Cold layer by setting it to read-only when the Hub is not in "Promotion Mode."
2. **[PROTOTYPE] HMAC-CHAIN**: Updating `log_to_blackboard` to include a sequence number and hash-chain to prevent signal spoofing.
3. **[PROTOTYPE] QUORUM_CHECK**: Modifying Port 7 to require 4/8 consensus from the P0 shards for any file move from Hot to Cold.

---
*Spider Sovereign (Port 7) | Governance Node*
