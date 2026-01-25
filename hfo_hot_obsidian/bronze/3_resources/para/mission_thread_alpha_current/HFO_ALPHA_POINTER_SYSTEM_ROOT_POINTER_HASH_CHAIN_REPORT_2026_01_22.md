# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO Mission Thread Alpha — Pointer System Formalization (Root Pointer + Hash Chain)

**Authority:** Port 1 (Bridger / Web Weaver) — Shared Data Fabric

**Date:** 2026-01-22

## Executive Summary

You already *have* the “one stable pointer” concept implemented: [hfo_pointers.json](../../../../../../hfo_pointers.json) + the resolver [hfo_pointers.py](../../../../../../hfo_pointers.py) feed the root shims [hfo_hub.py](../../../../../../hfo_hub.py) and [hfo_mcp_gateway_hub.py](../../../../../../hfo_mcp_gateway_hub.py) and the Alpha gateway implementation uses it for SSOT DB paths.

What’s missing is the cryptographic *verification* layer and (more importantly) a trustworthy *anchor* for the expected hash/signature.

**My assessment:** your mental model is ~**65% correct / 35% wrong**.

- You’re correct that a single pointer file is a powerful hot-swap seam.
- You’re correct that cryptographic hashing enables tamper-*detection*.
- You’re **partly wrong** equating “hashing” with “tight security”: hashing gives integrity evidence *only if* you have a trusted expected value; it does not by itself provide authenticity, freshness, or rollback protection.

This report proposes a Port‑1 “Root Pointer v1” pattern that keeps **one human-edited pointer artifact** while using GitOps to supply the trust anchor (signed commits/tags), with optional detached signatures for stronger guarantees.

---

## Evidence: current pointer system (what exists today)

### Root pointer file (single artifact)

- [hfo_pointers.json](../../../../../../hfo_pointers.json) defines:
  - `targets.mcp_gateway_impl` (the active Alpha MCP gateway implementation)
  - `paths.*` for shared SSOT resources (blackboard, mcp_memory, duckdb)

### Resolver + hot-swap seam

- [hfo_pointers.py](../../../../../../hfo_pointers.py) resolves dotted keys and supports **env overrides** (`HFO_*`) and **defaults**.

### Active call-sites (Alpha + P5)

- Root hub shim uses the pointer target:
  - [hfo_hub.py](../../../../../../hfo_hub.py)
- Root MCP shim uses the pointer target:
  - [hfo_mcp_gateway_hub.py](../../../../../../hfo_mcp_gateway_hub.py)
- Alpha implementation uses pointer paths for DuckDB:
  - [hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py](../../../1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py)
- P5 Sentinel uses pointer paths for DuckDB:
  - [scripts/p5_sentinel_daemon.py](../../../../../../scripts/p5_sentinel_daemon.py)

So: the “single pointer seam” is already real and valuable.

---

## Why it still feels brittle (root causes)

### 1) No cryptographic verification step

Right now, nothing *verifies* that [hfo_pointers.json](../../../../../../hfo_pointers.json) (or the target files it points at) matches any expected hash.

A change will be noticed by Git diff and maybe by humans, but it is not cryptographically enforced at runtime.

### 2) Hashes alone don’t yield authenticity

Even if we add a SHA‑256 field somewhere:

- If an attacker can modify both the pointer and the “expected hash” source, the system can still be fooled.
- A hash proves **integrity** of bytes relative to an expected value; it does **not** prove:
  - **Who** authored it (authenticity)
  - **When** it was minted (freshness)
  - That it isn’t an **old** known-good pointer (rollback)

### 3) Env overrides are a deliberate bypass (useful, but security-relevant)

[ hfo_pointers.py](../../../../../../hfo_pointers.py) intentionally allows environment variables to override the pointer values.

This is great for CI and emergency ops, but it means “the pointer file is authoritative” is **not universally true** unless you enforce policies like:

- In production/mission runs, forbid `HFO_*` overrides (or log + fail-closed when present).

### 4) Silent fallback behaviors can hide drift

On parse errors or missing files, the resolver returns `{}` / defaults.

This helps survivability, but it can mask accidental corruption.

**Alpha posture choice:** for Mission Thread Alpha infrastructure, a stricter fail-closed mode is often preferable (Port 5 can enforce).

---

## Your understanding: what % wrong and why (learning scaffold)

I’m scoring this by claims (weights sum to 100). This is a teaching rubric, not a “math truth”.

| Claim | Your statement | Correct? | Weight | Wrong % inside claim | Why wrong / missing piece |
|---|---|---:|---:|---:|---|
| A | “1 pointer… easy to hotswap” | Mostly | 25 | 10 | Already true: root shim reads [hfo_pointers.json](../../../../../../hfo_pointers.json). Remaining gap is governance + verification. |
| B | “cryptographic hashing… tight security” | Partly | 30 | 55 | Hashing ≠ security. Hashing gives integrity checks but needs a trusted anchor; doesn’t prove author, freshness, or prevent rollback. |
| C | “tamper evident when something has changed” | Partly | 25 | 35 | Tamper-evidence requires a trusted expected hash/signature. If attacker can change both, tamper-evidence collapses. |
| D | “GitOps gives version/tracking/durability built in” | Mostly | 15 | 25 | Git gives versioning; durability depends on remotes, branch protections, and signature policies. |
| E | “Port 1 authority; shared data fabric” | Yes | 5 | 0 | Correct: P1 should own the cross-port pointer/manifest envelope boundaries. |

Weighted wrongness:

$$
0.25\cdot0.10 + 0.30\cdot0.55 + 0.25\cdot0.35 + 0.15\cdot0.25 + 0.05\cdot0.00 \approx 0.35
$$

**Result:** ~**35% wrong** (and the “wrong” is primarily the *security model*, not the architecture seam).

---

## Proposed design: Port‑1 “Root Pointer v1” (single pointer artifact + verifiable chain)

### Design goal

Keep one human-edited pointer file, but make it **tamper-evident and operationally hot-swappable** with GitOps durability.

### Core idea

- **One pointer artifact (human-edited):** `hfo_pointers.json`
- **One trust anchor (machine-enforced):** Git commit/tag signature policy (or detached signature stored in repo)
- **One verification step (Port‑1 responsibility):** verify pointer + referenced artifacts before use

### Minimal schema extension (conceptual)

Add fields to `hfo_pointers.json` (or a separate manifest, if you prefer) that bind it to an expected state:

- `pointers_version`: semantic version for the pointer schema
- `expected_repo_commit`: the commit SHA this pointer is meant to run under
- `expected_repo_tree_sha256`: optional stronger commit/tree binding
- `artifact_hashes`: map of important target paths → sha256

Example (illustrative only):

```json
{
  "pointers_version": "1",
  "expected_repo_commit": "<git sha>",
  "targets": { "mcp_gateway_impl": "..." },
  "paths": { "duckdb_unified": "..." },
  "artifact_hashes": {
    "hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py": "sha256:...",
    "hfo_gen_88_cb_v2/hfo_unified_v88.duckdb": "sha256:..."
  }
}
```

### Verification contract (Port 1 owns this)

Port‑1 “pointer verification” should answer:

1) Is the pointer JSON schema-valid? (fail-closed)
2) Do the pointed-to files exist?
3) Do the bytes hash to the expected sha256?
4) Is the Git anchor acceptable?
   - signed commit/tag required (policy)
   - branch protections / fast-forward only
5) If anything fails: emit a Port‑5 compatible violation signal and fail-closed.

### Why Git signing matters

To get from “tamper evident” to “tight security”, you need **authenticity**.

Practical anchor options:

- **Preferred:** signed commits (`git commit -S`) and/or signed tags (`git tag -s`) with protected branches.
- **Optional extra-hard:** detached signatures for the pointer blob (e.g., minisign/cosign) stored alongside.

---

## Operational workflow (GitOps-friendly)

1) Edit [hfo_pointers.json](../../../../../../hfo_pointers.json) (the only human touchpoint)
2) GitOps pipeline:
   - runs a pointer verification script
   - computes required hashes
   - enforces signed commit/tag policy
3) P5 sentinel / hub preflight:
   - re-validates pointer chain before mission execution

This keeps hot-swaps cheap (edit one file), while still making drift measurable and gateable.

---

## Learning exercises (quick scaffolding)

1) **Integrity vs authenticity:** write one sentence for each.
2) **Attack simulation:** imagine attacker can edit the repo but not the remote protected branch — what breaks?
3) **Rollback test:** check out an old commit and see why “hash valid” doesn’t imply “fresh”.
4) **Policy drill:** list which env vars should be forbidden in “mission run” mode.
5) **One-page threat model:** insider vs outsider; local vs CI; rewrite-history vs append-only.

---

## Next concrete step (implementation-ready)

- Add a Port‑1 pointer verification gate (script or module) that:
  - loads `hfo_pointers.json`
  - validates schema
  - hashes and checks `targets` and critical `paths`
  - emits a single pass/fail receipt entry

Then wire it into `npm run p5:preflight` (or an Alpha-specific preflight) as a fail-closed step.
