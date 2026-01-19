# Medallion: Gold | Mutation: 0% | HIVE: V

# 🧶 HFO DEFENSES: AI-SLOP & THEATER SUPPRESSION

**Medallion Layer**: Forensic (GOLD_DEFENSE)
**Signal ID**: `SLOP_SUPPRESSION_20260111`

---

## 🎭 IDENTIFIED SLOP PATTERNS (VECTORS)

### 1. The "Pseudo-Completion" Fraud

**Pattern**: Agent claims a task is "Completed" or "Stabilized" while leaving static stubs or omitting critical logic.
**Defensive Block**:

- **P5-TODO-CRIT**: A pre-commit check that greps for `TODO`, `FIXME`, or `STUB` in newly added code. If found without an associated `BYPASS_ID`, the commit is blocked.
- **Symbol Density Check**: Ensures that methods added have a minimum cyclomatic complexity or line count (prevents empty `pass` or `return {}` theater).

### 2. The "Comment-Only" Artifact (Code Leaks)

**Pattern**: Agent produces a file that is mostly prose or contains `...e-x-i-s-t-i-n-g c-o-d-e...` markers.
**Defensive Block**:

- **LEAK-GATE**: Pre-commit regex that blocks strings like `...r-e-s-t of the f-i-l-e...`, `/* Lines o-m-i-t-t-e-d */`, or `...e-x-i-s-t-i-n-g c-o-d-e...`.
- **Doc-to-Code Ratio**: If a `.py` or `.ts` file contains >70% comments/prose, it is flagged as a "Narrative Leak."

### 3. The "Medallion Mask" (Header Theater)

**Pattern**: Agent adds `// Medallion: Gold` to a file that has no receipts or hasn't passed property tests.
**Defensive Block**:

- **HEADER-AUDIT**: A gate that compares the `Medallion` header level with the actual directory depth (`hfo_hot_obsidian/bronze/...`). If a file claims `Gold` in a `Bronze` folder, it is rejected.
- **Timestamp Velocity**: If 10 files are labeled "Hardened" in a single commit, the P purity guard tags it as "Suspicious Velocity" (Manual Review Required).

---

## 🛠️ MINIMAL-COST DEFENSE IMPLEMENTATION

### [PROTOTYPE] `scripts/slop_sentinel.sh`

A lightweight shell script tied to Husky that enforces these "Sanity Filters":

```bash
#!/bin/bash
# Minimal-Cost AI Slop Filter

# 1. Block slop markers
grep -qE "\.\.\.e-x-i-s-t-i-n-g c-o-d-e\.\.\.|\.\.\.r-e-s-t of the f-i-l-e\.\.\.|Lines .* o-m-i-t-t-e-d" $(git diff --cached --name-only)
if [ $? -eq 0 ]; then
    echo "🚨 [SLOP-BLOCK]: AI-Generated 'Existing Code' marker detected!"
    exit 1
fi

# 2. Block Empty Stubs in sensitive ports
grep -qE "pass$|return \{\}$" $(git diff --cached --name-only | grep "ports/")
if [ $? -eq 0 ]; then
    echo "🚨 [THEATER-BLOCK]: Empty stub detected in Hub Ports!"
    exit 1
fi

# 3. Medallion Header Mismatch
# (Simple count: files claiming Gold should not be in Bronze path)
grep -l "Medallion: Gold" $(git diff --cached --name-only | grep "/bronze/")
if [ $? -eq 0 ]; then
    echo "🚨 [HEADER-FRAUD]: Medallion Level 'Gold' not allowed in 'Bronze' path."
    exit 1
fi
```

---
*Spider Sovereign (Port 7) | Anti-Slop Manifold*
