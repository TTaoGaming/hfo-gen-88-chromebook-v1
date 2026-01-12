# ⚖️ FORENSIC ANALYSIS: CONNECTIVITY REGRESSION [V52]

**Medallion Layer**: Hot Bronze
**Incident Date**: 2026-01-11
**Incident ID**: `CONN_REFUSED_V52_8890_5500`
**Status**: 🔴 RED (RECOVERY MODE ACTIVE)

---

## 🕵️ Executive Summary

The project has entered a "Connectivity Death Spiral" on the Chromebook V-1 host. Despite the internal Linux container (Crostini) successfully spawning both **Python P0-Server (8889)** and **VS Code Live Server (5500)**, the ChromeOS Host browser is returning `ERR_CONNECTION_REFUSED`. This signifies a failure in the **Host-to-Container Network Bridge**, likely triggered by port-switching collisions during the V52 promotion.

## 🎭 The Anatomy of the Failure

### 1. The Port Conflict (Collision)

Initial V52 setup attempted to use port `8889` for two separate processes (Python and Live Server). This created a "Zombie Socket" scenario where the Linux kernel reported the port as open, but the application layer (Live Server) was unable to bind cleanly to the existing listener, leading to the `ERR_SOCKET_NOT_CONNECTED` state.

### 2. The Host-Bridge Block (The "Wall")

After reverting to the standard port `5500`, the error shifted to `ERR_CONNECTION_REFUSED`.

- **Evidence**: `netstat -tulpn` shows `31404/exe` (VS Code) is listening on `0.0.0.0:5500`.
- **Evidence**: Internal `curl` from within Linux returns `HTTP/1.1 200 OK`.
- **Deduction**: The Linux firewall or the ChromeOS Crostini bridge has "blacklisted" or failed to propagate the port forwarding for `127.0.0.1`.

### 3. The Playwright Proof (The "Mirror")

A headless Playwright capture (`hfo:shot:headless`) was executed.

- **Result**: **SUCCESS**.
- **Implication**: The system is 100% functional *inside* the Linux environment. The failure is strictly **External Visibility**.

## 🛰️ 8 Critical Signals (CS) Status

- **CS-1 (Server Integrity)**: 🟢 **GREEN**. Python server on 8889 is robustly serving V52.
- **CS-2 (Path Resolution)**: 🟢 **GREEN**. Workspace root configured to `/`. `Cannot GET` resolved.
- **CS-3 (Bridge Stability)**: 🔴 **CRITICAL**. Host Chrome cannot reach Container Linux.
- **CS-4 (Socket State)**: 🟡 **AMBER**. Zombie sockets detected on 8890 but cleared.

## 🛡️ Remediation Strategy (To Hot Bronze)

The system must be stabilized in **Hot Bronze** before any further feature work (Mission Omega) proceeds.

1. **Protocol Shift**: Abandon `127.0.0.1` in favor of `localhost` or the direct Container IP `100.115.92.204`.
2. **Persistence**: The Python server at `8889` is the only verified stable bridge at this time.
3. **Hard Gate**: No more configuration changes to `settings.json` without a P5 Forensic clearing the bridge.

---
*Spider Sovereign (Port 7) | Forensic Audit Complete | Symbiotic Canalization Secured*
