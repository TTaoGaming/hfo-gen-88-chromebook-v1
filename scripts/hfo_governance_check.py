#!/usr/bin/env python3
import sys
import re
import os

# Medallion: Bronze | Mutation: 95% | HIVE: V
# P5 DEFEND: ROE Enforcement Script

PROVENANCE_REGEX = r"(//|#) Medallion: (Bronze|Silver|Gold) \| Mutation: \d+% \| HIVE: (H|I|V|E)"
LAZY_AI_REGEX = r"\.\.\.existing code\.\.\.|\.\.\.remaining code\.\.\.|// \.\.\."

SCREAMS = {
    0: "BLINDSPOT",
    1: "BREACH",
    2: "THEATER",
    3: "PHANTOM",
    4: "MUTATION",
    5: "POLLUTION",
    6: "AMNESIA",
    7: "LATTICE"
}

def check_file(filepath):
    if not filepath.endswith(('.py', '.ts', '.js', '.v', '.md')):
        return True

    try:
        with open(filepath, 'r') as f:
            content = f.read()
            lines = content.splitlines()[:10]

            # Scream 5: Pollution (Missing Provenance)
            if not any(re.match(PROVENANCE_REGEX, line) for line in lines):
                print(f"❌ [P4 SCREAM_5: POLLUTION]: Missing or invalid Provenance Header in {filepath}")
                return False

            # Scream 2: AI Theater (Lazy code markers)
            if re.search(LAZY_AI_REGEX, content):
                print(f"❌ [P4 SCREAM_2: THEATER]: Lazy AI markers detected in {filepath}")
                return False

            return True
    except Exception as e:
        print(f"❌ [P5 DEFEND]: Error reading surface {filepath}: {e}")
        return False
        print(f"❌ [P5 DEFEND]: Error reading surface {filepath}: {e}")
        return False

def main():
    files = sys.argv[1:]
    failed = False
    for f in files:
        if os.path.isfile(f) and not check_file(f):
            failed = True

    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
