
import json
from datetime import datetime

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

entries = []
for line in lines:
    line = line.strip()
    if not line: continue
    entries.append(json.loads(line))

# Identify reversals and fix them
# Simple fix: if entry[i].timestamp < entry[i-1].timestamp, set entry[i].timestamp = entry[i-1].timestamp + 1ms
fixed_count = 0
for i in range(1, len(entries)):
    if "timestamp" not in entries[i-1] or "timestamp" not in entries[i]:
        continue
    t1_str = entries[i-1]["timestamp"]
    t2_str = entries[i]["timestamp"]
    
    # Normalize Z and other quirks
    t1_clean = t1_str.replace("Z", "")
    t2_clean = t2_str.replace("Z", "")
    
    try:
        t1 = datetime.fromisoformat(t1_clean)
        t2 = datetime.fromisoformat(t2_clean)
        
        if t2 < t1:
            # Reversal!
            entries[i]["timestamp"] = t1.isoformat() + "+00:00"
            fixed_count += 1
    except ValueError:
        continue

if fixed_count > 0:
    with open(BLACKBOARD_PATH, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
    print(f"Fixed {fixed_count} Chronos reversals.")
else:
    print("No Chronos reversals found.")
