# Medallion: Silver | Mutation: 0% | HIVE: V

## HFO Magic Number Normalization (v0.1)

**Date**: 2026-01-25
**Intent**: reduce configuration drift and catch obvious mistakes by constraining “magic numbers” to a small, legible set.

---

## Rule (current)

In HFO configuration, settings, thresholds, and any “chosen constants” should use ONLY one of:

1) **Powers of 2**: $2^n$ (e.g., 1, 2, 4, 8, 16, 32, 64, …)
2) **Powers of 8**: $8^n$ (e.g., 1, 8, 64, 512, 4096, …)
3) **Multiples of 8**: $8k$ (e.g., 8, 16, 24, 32, 40, …)

If a value is not in one of these buckets, it is presumed suspect and should trigger review.

---

## Examples (heuristic)

- **Count-like knobs** (e.g., max active windows, buffer sizes): prefer **powers of 2**.
- **HFO/HIVE alignment knobs** (port counts, shard widths, fractal steps): prefer **powers of 8**.
- **Percent-ish or step thresholds** (hysteresis steps, debounce windows expressed as “ticks”): prefer **multiples of 8**.

---

## Rationale

- Constrains degrees of freedom, making drift and errors visible.
- Forces explicit justification when a number is “special”.
- Aligns with the existing HFO motif of octrees / 8-port holonarchy.

---

## Roadmap

- **Near-term**: allow all three categories (power-of-2, power-of-8, multiple-of-8) to minimize churn while standardizing.
- **Future**: converge toward **powers of 8** as the dominant system.
- **Automation target**: add a **pre-commit check** that scans settings/config/contracts for numeric literals and flags non-conforming “magic numbers”, with allowlist + justification mechanism.

---

## Open Questions / Needed Specs

- What file classes are “settings” (YAML, JSON, TS contracts, Python configs, etc.)?
- What is the canonical allowlist mechanism (inline annotation vs external allowlist file)?
- How do we treat floats (e.g., 0.8), percentages (80), and units (ms, frames)?

