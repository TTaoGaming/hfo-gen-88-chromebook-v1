
import json
import os

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()

# Line 12087 (1-based) is index 12086
target_idx = 12086
if len(lines) > target_idx:
    entry = json.loads(lines[target_idx])
    # Set to something after 12086's 06:35:21.136004
    entry["timestamp"] = "2026-01-15T06:35:21.200000+00:00"
    lines[target_idx] = json.dumps(entry) + "\n"
    
    with open(BLACKBOARD_PATH, "w") as f:
        f.writelines(lines)
    print(f"Fixed Chronos reversal at line {target_idx + 1}")
else:
    print("Line not found")
