# Medallion: Bronze | Mutation: 0% | HIVE: E
import json
import hashlib
import os

SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"
BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

with open(SECRET_PATH, "r") as f:
    secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

line1_str = lines[0].strip()
line1 = json.loads(line1_str)
sig1 = line1.pop("signature")

line2_str = lines[1].strip()
line2 = json.loads(line2_str)
sig2_found = line2.pop("signature")

# Try to replicate sig2 calculation
# Case A: last_signature was sig1
prev = sig1
entry_str2 = json.dumps(line2, sort_keys=True)
expected_sig2 = hashlib.sha256(f"{secret}:{prev}:{entry_str2}".encode()).hexdigest()

print(f"Sig1: {sig1}")
print(f"Line 2 JSON: {entry_str2}")
print(f"Sig2 Found: {sig2_found}")
print(f"Sig2 Expected: {expected_sig2}")

if sig2_found == expected_sig2:
    print("SUCCESS: Match found!")
else:
    print("FAIL: No match.")
    # Try alternate: last_signature was "LEGACY" (maybe it didn't find line 1?)
    alternate = hashlib.sha256(f"{secret}:LEGACY:{entry_str2}".encode()).hexdigest()
    print(f"Sig2 Expected (LEGACY): {alternate}")
    
    # Try alternate: last_signature was "MALFORMED"
    alternate2 = hashlib.sha256(f"{secret}:MALFORMED:{entry_str2}".encode()).hexdigest()
    print(f"Sig2 Expected (MALFORMED): {alternate2}")

    # Try alternate: last_signature was "ROOT"
    alternate3 = hashlib.sha256(f"{secret}:ROOT:{entry_str2}".encode()).hexdigest()
    print(f"Sig2 Expected (ROOT): {alternate3}")
