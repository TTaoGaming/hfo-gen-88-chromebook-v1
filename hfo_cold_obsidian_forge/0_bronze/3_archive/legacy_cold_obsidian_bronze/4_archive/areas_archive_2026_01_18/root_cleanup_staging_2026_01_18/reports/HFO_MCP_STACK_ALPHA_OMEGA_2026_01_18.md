# Medallion: Bronze | Mutation: 0% | HIVE: V

# HFO MCP Stack (Alpha/Omega) — 2026-01-18

## Scope

This document defines the **tool stack** for Mission Thread Alpha and Omega, plus MCP servers required to reach maximum operational potential while keeping the stack minimal and grounded.

---

## Mission Thread Alpha (Port 6: Kraken Keeper — Monthly Rollups)

### Core tool stack (minimum viable)

- **filesystem**: SSOT file access, reports, manifests, and anchor discovery.
- **memory**: store monthly rollups as graph nodes with evidence links.
- **sequential-thinking**: enforce multi-step, grounded reasoning.
- **time**: timestamps for receipts and rollups.
- **tavily**: external evidence search and cross‑validation.
- **brave-search**: redundant external search source for verification.

### Optional (situational)

- **microsoft/playwright-mcp**: UI testing (not needed for rollups).
- **web fetch**: only if Tavily/Brave are unavailable.

### What this enables

- Deterministic monthly rollups from SSOT.
- Audit‑grade evidence chains for Alpha governance.
- Reduced drift through anchored memory writes.

---

## Mission Thread Omega (Port 2/3/4 — Interaction + Visual Fidelity)

### Core tool stack (minimum viable)

- **filesystem**: substrate inspection and change tracking.
- **memory**: capture rollup outputs and Omega state snapshots.
- **sequential-thinking**: enforce multi‑step diagnostics.
- **time**: timestamped evidence.
- **tavily + brave-search**: asset and behavior research.

### Optional (high‑value for Omega)

- **microsoft/playwright-mcp**: UI/interaction parity tests and regression checks.

### What this enables

- Faster interaction debugging with evidence.
- Repeatable parity checks and handoff stability.

---

## MCP Servers to Reach MAX Potential (Pinned Stack)

**Keep/Enable:**

- filesystem
- memory
- sequential-thinking
- time
- tavily
- brave-search

**Add only if needed:**

- microsoft/playwright-mcp

**Disable for rollup focus:**

- context7
- microsoft/markitdown
- DBCode – Database Management
- Jupyter
- Copilot Container Tools

---

## Notes

- This stack is aligned to **HIVE/8:1010** with evidence-first rollups.
- Keep SSOT read‑only; all writes should be memory rollups and reports.
