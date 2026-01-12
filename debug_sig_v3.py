
import json
import hmac
import hashlib
import os

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

with open(SECRET_PATH, "r") as f:
    secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

def verify(line_idx, prev_sig):
    line = lines[line_idx].strip()
    entry = json.loads(line)
    found_sig = entry.pop("signature")
    
    # Try with spaces (default)
    entry_str_spaces = json.dumps(entry, sort_keys=True)
    h_spaces = hmac.new(secret.encode(), (prev_sig + entry_str_spaces).encode(), hashlib.sha256).hexdigest()
    
    # Try without spaces
    entry_str_no_spaces = json.dumps(entry, sort_keys=True, separators=(',', ':'))
    h_no_spaces = hmac.new(secret.encode(), (prev_sig + entry_str_no_spaces).encode(), hashlib.sha256).hexdigest()
    
    print(f"Line {line_idx+1}:")
    print(f"  Found: {found_sig}")
    print(f"  Calculated (spaces):   {h_spaces}")
    print(f"  Calculated (no-space): {h_no_spaces}")
    
    if found_sig == h_spaces: print("  MATCH: SPACES")
    if found_sig == h_no_spaces: print("  MATCH: NO-SPACES")
    return found_sig

last = "LEGACY"
for i in range(5):
    last = verify(i, last)
