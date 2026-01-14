# Medallion: Bronze | Mutation: 0% | HIVE: E
import json
import hashlib
import hmac
import os

SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"
BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

with open(SECRET_PATH, "r") as f:
    secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

def test_line(i, prev_sig):
    line_str = lines[i].strip()
    entry = json.loads(line_str)
    sig_found = entry.pop("signature")
    entry_str = json.dumps(entry, sort_keys=True)
    print(f"Entry String {i+1}: {entry_str}")
    
    # Check HMAC
    data_hmac = prev_sig + entry_str
    sig_hmac = hmac.new(secret.encode(), data_hmac.encode(), hashlib.sha256).hexdigest()
    
    # Check SHA
    data_sha = f"{secret}:{prev_sig}:{entry_str}"
    sig_sha = hashlib.sha256(data_sha.encode()).hexdigest()
    
    print(f"Line {i+1}:")
    print(f"  Found: {sig_found}")
    print(f"  HMAC:  {sig_hmac}")
    print(f"  SHA:   {sig_sha}")
    if sig_found == sig_hmac: print("  MATCH: HMAC")
    if sig_found == sig_sha: print("  MATCH: SHA")
    return sig_found

# Line 1 (root) - let's see what it matches
line1 = json.loads(lines[0].strip())
sig1 = line1.pop("signature")
entry_str1 = json.dumps(line1, sort_keys=True)

for prev in ["LEGACY", "ROOT", "NONE", ""]:
    data_hmac = prev + entry_str1
    sig_hmac = hmac.new(secret.encode(), data_hmac.encode(), hashlib.sha256).hexdigest()
    if sig_hmac == sig1: print(f"Line 1 matches HMAC with prev='{prev}'")
    
    data_sha = f"{secret}:{prev}:{entry_str1}"
    sig_sha = hashlib.sha256(data_sha.encode()).hexdigest()
    if sig_sha == sig1: print(f"Line 1 matches SHA with prev='{prev}'")

print("\nVerifying Line 2 (prev=sig1):")
test_line(1, sig1)

print("\nVerifying Line 3 (prev=sig2):")
sig2 = json.loads(lines[1].strip()).get("signature")
test_line(2, sig2)
