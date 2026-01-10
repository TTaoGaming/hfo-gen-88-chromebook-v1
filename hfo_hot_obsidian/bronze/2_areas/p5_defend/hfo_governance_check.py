#!/usr/bin/env python3
import sys
import re
import os

# Medallion: Bronze | Mutation: 0% | HIVE: V
# PORT-5-IMMUNIZE: ROE Enforcement Script

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

            # Find provenance line
            prov_line = None
            for line in lines:
                match = re.match(PROVENANCE_REGEX, line)
                if match:
                    prov_line = match
                    break

            # Scream 5: Pollution (Missing Provenance)
            if not prov_line:
                print(f"❌ [P4 SCREAM_5: POLLUTION]: Missing or invalid Provenance Header in {filepath}")
                return False

            # Reward Hacking / Spoofing Check
            claimed_layer = prov_line.group(2).lower()
            actual_layer = "bronze"
            if "/silver/" in filepath: actual_layer = "silver"
            elif "/gold/" in filepath: actual_layer = "gold"
            elif "hfo_cold_obsidian" in filepath:
                # Cold files can be Bronze/Silver/Gold but must match their internal PARA
                if "/bronze/" in filepath: actual_layer = "bronze"
                elif "/silver/" in filepath: actual_layer = "silver"
                elif "/gold/" in filepath: actual_layer = "gold"

            if claimed_layer != actual_layer:
                print(f"❌ [P4 SCREAM_3: PHANTOM]: Layer Spoofing Detected! {filepath} claims {claimed_layer} but is in {actual_layer}.")
                return False

            # Scream 2: AI Theater (Lazy code markers)
            if re.search(LAZY_AI_REGEX, content):
                print(f"❌ [P4 SCREAM_2: THEATER]: Lazy AI markers detected in {filepath}")
                return False

            return True
    except Exception as e:
        print(f"❌ [PORT-5-IMMUNIZE]: Error reading surface {filepath}: {e}")
        return False
        print(f"❌ [PORT-5-IMMUNIZE]: Error reading surface {filepath}: {e}")
        return False

def main():
    files = sys.argv[1:]
    exit_needed = False
    for f in files:
        if not os.path.isfile(f): continue

        is_bronze = "hfo_hot_obsidian/bronze" in f
        success = check_file(f)

        if not success:
            if is_bronze:
                print(f"⚠️ [P5 WARNING]: Header violation in Bronze file {f}. Please fix before freezing.")
            else:
                print(f"❌ [P5 BLOCK]: Header violation in hardened layer file {f}.")
                exit_needed = True

    if exit_needed:
        sys.exit(1)

if __name__ == "__main__":
    main()
