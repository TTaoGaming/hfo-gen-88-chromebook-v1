# Medallion: Bronze | Mutation: 0% | HIVE: E
import json
import os
import datetime

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

new_lines = []
last_ts = None

for i, line in enumerate(lines):
    line = line.strip()
    if not line: continue
    entry = json.loads(line)
    
    ts_str = entry.get("timestamp")
    if ts_str:
        try:
            clean_ts = ts_str.replace('Z', '+00:00')
            current_ts = datetime.datetime.fromisoformat(clean_ts)
            if last_ts and current_ts < last_ts:
                print(f"Fixing temporal reversal at line {i+1}: {ts_str} -> {last_ts}")
                # Set to 1 millisecond after last_ts
                current_ts = last_ts + datetime.timedelta(milliseconds=1)
                entry["timestamp"] = current_ts.isoformat()
            last_ts = current_ts
        except Exception as e:
            print(f"Skip TS line {i+1}: {e}")
    
    new_lines.append(json.dumps(entry, sort_keys=True) + "\n")

with open(BLACKBOARD_PATH, "w") as f:
    f.writelines(new_lines)
print("Fixed temporal reversals.")
