# Medallion: Bronze | Mutation: 0% | HIVE: E
import json
import hashlib
import os

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

with open(SECRET_PATH, "r") as f: secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

def check_sig(prev_sig, entry):
    sig = entry.pop("signature", None)
    entry_str = json.dumps(entry, sort_keys=True)
    expected = hashlib.sha256(f"{secret}:{prev_sig}:{entry_str}".encode()).hexdigest()
    return expected, sig

# Line 1
e1 = json.loads(lines[0])
exp1, got1 = check_sig("LEGACY", e1)
print(f"Line 1: Expected {exp1}, Got {got1}")

# Line 2
e2 = json.loads(lines[1])
exp2, got2 = check_sig(got1, e2)
print(f"Line 2: Expected {exp2}, Got {got2}")

# Line 3
e3 = json.loads(lines[2])
exp3, got3 = check_sig(got2, e3)
print(f"Line 3: Expected {exp3}, Got {got3}")
