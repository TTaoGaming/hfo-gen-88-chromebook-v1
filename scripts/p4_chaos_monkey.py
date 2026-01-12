#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: I
# Port 4: DISRUPT | chaos_monkey.py | Pathogen Generator

import os
import sys
import random
import shutil

# Pathogens to inject
PATHOGENS = {
    "P4_SLOP_EXISTING": {
        "pattern": "// Code logic here\n",
        "replacement": "// Code logic here\n// EXISTING_CODE_MARKER\n"
    },
    "P4_REWARD_HACK_REMOTE": {
        "pattern": 'src="./assets/piano_genie/script.js"',
        "replacement": 'src="https://storage.googleapis.com/magentadata/js/checkpoints/piano_genie/model/script.js"'
    },
    "P4_HEADER_FRAUD": {
        "pattern": "Medallion: Bronze",
        "replacement": "Medallion: Gold"
    },
    "P4_THEATER_SPINNER": {
        "pattern": "</body>",
        "replacement": '<script>setInterval(() => { console.log("AI is thinking..."); }, 100);</script></body>'
    }
}

def inject_pathogen(file_path, pathogen_id):
    if not os.path.exists(file_path):
        print(f"❌ [P4-CHAOS]: Target {file_path} not found.")
        return False

    with open(file_path, "r") as f:
        content = f.read()

    pathogen = PATHOGENS[pathogen_id]
    if pathogen["pattern"] not in content:
        print(f"⚠️ [P4-CHAOS]: Pattern for {pathogen_id} not found in {file_path}. Skipping.")
        return False

    mutated_content = content.replace(pathogen[pathogen_id == "P4_REWARD_HACK_REMOTE" and "pattern" or "pattern"], pathogen["replacement"])
    
    with open(file_path, "w") as f:
        f.write(mutated_content)
    
    print(f"🧪 [P4-CHAOS]: Injected {pathogen_id} into {file_path}.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 p4_chaos_monkey.py <file_path> <pathogen_id>")
        print(f"Available Pathogens: {', '.join(PATHOGENS.keys())}")
        sys.exit(1)

    target = sys.argv[1]
    p_id = sys.argv[2]
    
    if p_id == "ALL":
        for pid in PATHOGENS.keys():
            inject_pathogen(target, pid)
    else:
        inject_pathogen(target, p_id)
