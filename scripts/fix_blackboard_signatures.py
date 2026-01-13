import json
import hashlib
import os

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

if not os.path.exists(SECRET_PATH):
    print("Secret not found")
    exit(1)

with open(SECRET_PATH, "r") as f: secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

new_lines = []
last_sig = "ROOT"

for i, line in enumerate(lines):
    line = line.strip()
    if not line: continue
    try:
        entry = json.loads(line)
        
        # Check for seal
        query_val = str(entry.get("query", ""))
        if entry.get("phase") == "SIGNAL" and query_val.startswith("RED_TRUTH_SEAL"):
            # Resets the chain
            last_sig = entry.get("signature", "ROOT")
            new_lines.append(line + "\n")
            continue

        # Remove old signature
        if "signature" in entry:
            old_sig = entry.pop("signature")
        
        prev = last_sig if last_sig != "ROOT" else "LEGACY"
        # Ensure we use the exact same serialization as the hub (sort_keys=True)
        entry_str = json.dumps(entry, sort_keys=True)
        new_sig = hashlib.sha256(f"{secret}:{prev}:{entry_str}".encode()).hexdigest()
        
        entry["signature"] = new_sig
        new_lines.append(json.dumps(entry) + "\n")
        last_sig = new_sig
    except json.JSONDecodeError:
        print(f"Skipping malformed line {i+1}")

with open(BLACKBOARD_PATH, "w") as f:
    f.writelines(new_lines)
print("Blackboard signatures recalculated.")
