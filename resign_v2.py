import json
import hashlib
import os

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

with open(SECRET_PATH, "r") as f: secret = f.read().strip()
with open(BLACKBOARD_PATH, "r") as f: lines = f.readlines()

new_lines = []
last_sig = "ROOT"

for i, line in enumerate(lines):
    line = line.strip()
    if not line: continue
    entry = json.loads(line)
    
    # Seal recognition
    query_val = str(entry.get("query", ""))
    if entry.get("phase") == "SIGNAL" and query_val.startswith("RED_TRUTH_SEAL"):
        last_sig = entry.get("signature", "ROOT")
        new_lines.append(line + "\n")
        continue

    # Pop signature
    if "signature" in entry: entry.pop("signature")
    
    prev = last_sig if last_sig != "ROOT" else "LEGACY"
    entry_str = json.dumps(entry, sort_keys=True)
    sig = hashlib.sha256(f"{secret}:{prev}:{entry_str}".encode()).hexdigest()
    entry["signature"] = sig
    new_lines.append(json.dumps(entry, sort_keys=True) + "\n")
    last_sig = sig

with open(BLACKBOARD_PATH, "w") as f:
    f.writelines(new_lines)
print("Resigned blackboard.")
