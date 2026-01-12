import json
import hashlib
import os

SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"
BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

with open(SECRET_PATH, "r") as f:
    secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

line1 = json.loads(lines[0].strip())
sig1 = line1.pop("signature")

line2 = json.loads(lines[1].strip())
sig2_found = line2.pop("signature")

prevs = [sig1, "LEGACY", "ROOT", "MALFORMED", "ERROR", ""]
seps = [None, (',', ':'), (', ', ': ')]

for prev in prevs:
    for sep in seps:
        if sep:
            entry_str = json.dumps(line2, sort_keys=True, separators=sep)
        else:
            entry_str = json.dumps(line2, sort_keys=True)
        
        h = hashlib.sha256(f"{secret}:{prev}:{entry_str}".encode()).hexdigest()
        if h == sig2_found:
            print(f"MATCH FOUND!")
            print(f"Prev: {prev}")
            print(f"Separators: {sep}")
            exit(0)

print("No match found with simple permutations.")
