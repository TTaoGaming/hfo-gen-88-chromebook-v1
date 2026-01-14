# Medallion: Bronze | Mutation: 0% | HIVE: E
import json
import hashlib
import os
import datetime

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

with open(SECRET_PATH, "r") as f: secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

last_sig = "ROOT"
for i, line in enumerate(lines):
    line = line.strip()
    if not line: continue
    try:
        entry = json.loads(line)
        query_val = str(entry.get("query", ""))
        if entry.get("phase") == "SIGNAL" and query_val.startswith("RED_TRUTH_SEAL"):
            last_sig = entry.get("signature", "ROOT")
            print(f"SEAL at line {i+1}, resetting last_sig to {last_sig}")
            continue

        if "signature" not in entry:
            print(f"Unsigned at line {i+1}")
            break
        
        sig = entry.pop("signature")
        prev = last_sig if last_sig != "ROOT" else "LEGACY"
        entry_str = json.dumps(entry, sort_keys=True)
        expected = hashlib.sha256(f"{secret}:{prev}:{entry_str}".encode()).hexdigest()
        
        if sig != expected and last_sig == "ROOT":
            expected_legacy = hashlib.sha256(f"{secret}:LEGACY:{entry_str}".encode()).hexdigest()
            if sig == expected_legacy: expected = expected_legacy

        if sig != expected:
            print(f"FRACTURE at line {i+1}")
            print(f"  Entry: {entry_str}")
            print(f"  Prev Sig: {prev}")
            print(f"  Expected: {expected}")
            print(f"  Got: {sig}")
            break
        
        last_sig = sig
    except Exception as e:
        print(f"Error at line {i+1}: {e}")
        break
print("Finished audit.")
