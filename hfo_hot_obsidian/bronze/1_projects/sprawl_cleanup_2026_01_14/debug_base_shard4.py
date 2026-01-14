# Medallion: Bronze | Mutation: 0% | HIVE: E

import sys
import os
import json
import hmac
import hashlib

# Add hub path
hub_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/ports"
if hub_path not in sys.path: sys.path.append(hub_path)

from versions.base import BLACKBOARD_PATH

SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"
with open(SECRET_PATH, "r") as f: secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

last_sig = "ROOT"
for i, line in enumerate(lines):
    line = line.strip()
    if not line: continue
    entry = json.loads(line)
    
    # Seal check
    if entry.get("phase") == "SIGNAL" and entry.get("query") == "RED_TRUTH_SEAL":
        last_sig = entry.get("signature")
        continue

    sig = entry.pop("signature")
    prev = last_sig if last_sig != "ROOT" else "LEGACY"
    entry_str = json.dumps(entry, sort_keys=True)
    data_to_hash = prev + entry_str
    expected = hmac.new(secret.encode(), data_to_hash.encode(), hashlib.sha256).hexdigest()
    
    if i == 2: # Line 3
        print(f"DEBUG LINE 3:")
        print(f"  PREV: {prev}")
        print(f"  STR:  {entry_str}")
        print(f"  EXP:  {expected}")
        print(f"  GOT:  {sig}")
    
    if sig != expected:
        print(f"FRACTURE AT LINE {i+1}")
        break
    last_sig = sig
