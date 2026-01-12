#!/bin/bash
# HFO-GOLD-INTEGRITY | AI Slop Sentinel

echo "🛡️ [P5-SLOP]: Scanning for AI Theater and Slop Patterns..."

# 1. Block "Existing Code" markers
# Using char classes to avoid self-triggering during pre-commit audit
MARKERS=$(git diff --cached --name-only | xargs -I {} grep -HE "\.\.\.[e]xisting [c]ode\.\.\.|\.\.\.[r]est of the [c]ode\.\.\.|Lines .* [o]mitted" {} 2>/dev/null)
if [ ! -z "$MARKERS" ]; then
    echo "🚨 [SLOP-BLOCK]: AI-Generated 'Existing Code' marker detected!"
    echo "$MARKERS"
    exit 1
fi

# 2. Block Empty Stubs in sensitive ports
STUBS=$(git diff --cached --name-only | grep "hfo_hot_obsidian/" | xargs -I {} grep -HE "pass$|return \{\}$" {} 2>/dev/null)
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
exit 0
