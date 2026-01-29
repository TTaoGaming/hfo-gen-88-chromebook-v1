#!/bin/bash
# HFO-GOLD-INTEGRITY | AI Slop Sentinel

echo "🛡️ [P5-SLOP]: Scanning for AI Theater and Slop Patterns..."

# 1. Block "Evasive AI Theater" markers (Narrative Evasion Vector)
# We target phrases used to skip implementation or hide stubs.
EVASION_PATTERNS=(
    "\.\.\.[e]xisting [c]ode\.\.\."
    "\.\.\.[r]est of the [c]ode\.\.\."
    "Lines .* [o]mitted"
    "[r]emainder of .* [b]revity"
    "[p]reviously [p]rovided"
    "[s]ame as [b]efore"
    "[n]o [c]hanges [n]eeded"
)

for pattern in "${EVASION_PATTERNS[@]}"; do
    MARKERS=$(git diff --cached --name-only | grep -vE "reports/|manifest|BOOK_OF_BLOOD_GRUDGES|blackboard" | xargs -I {} grep -HiE "$pattern" {} 2>/dev/null)
    if [ ! -z "$MARKERS" ]; then
        echo "🚨 [SLOP-BLOCK]: Narrative Evasion detected ($pattern)!"
        echo "$MARKERS"
        exit 1
    fi
done

# 2. Block Empty Stubs in sensitive ports
# Using [[:space:]] to avoid false positives like "bypass"
STUBS=$(git diff --cached --name-only | grep "hfo_hot_obsidian/" | xargs -I {} grep -HE "[[:space:]]pass$|return \{\}$" {} 2>/dev/null)
if [ ! -z "$STUBS" ]; then
    echo "🚨 [THEATER-BLOCK]: Empty stub detected in Hub Ports!"
    echo "$STUBS"
    exit 1
fi

# 3. Medallion Header Mismatch
# (Files claiming Gold should not be in Bronze path)
FRAUD=$(git diff --cached --name-only | grep "/bronze/" | xargs -I {} grep -l "Medallion: Gold" {} 2>/dev/null)
if [ ! -z "$FRAUD" ]; then
    echo "🚨 [HEADER-FRAUD]: Medallion Level 'Gold' not allowed in 'Bronze' path."
    echo "$FRAUD"
    exit 1
fi

echo "✅ [P5-SLOP-PASS]: No slop patterns detected."

# 4. Hallucinated Gestures (Emoji Slop)
# 🤚 is a confirmed hallucination. Correct language: 🖐️ (SENSE), ☝️ (AIM), 🫷 (RELEASE)
HALLUCINATION_EMOJIS=(
    "🤚"
)

for emoji in "${HALLUCINATION_EMOJIS[@]}"; do
    # Scan tracked files only (avoid OOM from large derived artifacts / storehouse JSONLs).
    H_FLAGS=$(git grep -l "$emoji" -- \
        ":(exclude)node_modules/**" \
        ":(exclude).git/**" \
        ":(exclude).venv/**" \
        ":(exclude).stryker/**" \
        ":(exclude)artifacts/**" \
        ":(exclude)hfo_hot_obsidian/bronze/3_resources/memory_fragments_collection/**" \
        ":(exclude)hfo_hot_obsidian/bronze/3_resources/memory_fragments_storehouse/**" \
        "*.html" "*.py" "*.js" "*.md" "*.jsonl" 2>/dev/null || true)
    if [ ! -z "$H_FLAGS" ]; then
        echo "🚨 [GESTURE-HALLUCINATION]: Forbidden emoji '$emoji' detected in the following files:"
        echo "$H_FLAGS"
        echo "Please use the correct sequence: 🖐️ (SENSE), ☝️ (AIM), 🫷 (RELEASE)."
    fi
done

exit 0
