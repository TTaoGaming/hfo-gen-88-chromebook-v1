# Medallion: Bronze | Mutation: 0% | HIVE: E
import json
import hashlib
import os

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

with open(SECRET_PATH, "r") as f: secret = f.read().strip()
with open(BLACKBOARD_PATH, "r") as f: lines = f.readlines()

line1 = lines[0].strip()
line2 = lines[1].strip()
line3 = lines[2].strip()

# Sig 1
e1 = json.loads(line1)
sig1 = e1.pop("signature")
entry_str1 = json.dumps(e1, sort_keys=True)
exp1 = hashlib.sha256(f"{secret}:LEGACY:{entry_str1}".encode()).hexdigest()
print(f"Line 1: Exp {exp1} Got {sig1}")

# Sig 2
e2 = json.loads(line2)
sig2 = e2.pop("signature")
entry_str2 = json.dumps(e2, sort_keys=True)
exp2 = hashlib.sha256(f"{secret}:{sig1}:{entry_str2}".encode()).hexdigest()
print(f"Line 2: Exp {exp2} Got {sig2}")

# Sig 3
e3 = json.loads(line3)
sig3 = e3.pop("signature")
entry_str3 = json.dumps(e3, sort_keys=True)
exp3 = hashlib.sha256(f"{secret}:{sig2}:{entry_str3}".encode()).hexdigest()
print(f"Line 3: Exp {exp3} Got {sig3}")
