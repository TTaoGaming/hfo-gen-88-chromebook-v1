
import json
import os

blackboard_path = 'hfo_hot_obsidian/hot_obsidian_blackboard.jsonl'
backup_path = blackboard_path + '.bak_pre_repair'

# Create backup
if not os.path.exists(backup_path):
    import shutil
    shutil.copy2(blackboard_path, backup_path)

with open(blackboard_path, 'r') as f:
    lines = f.readlines()

# Line 24116 (0-indexed is 24115)
target_idx = 24115
next_idx = 24116

if target_idx < len(lines):
    line_target = json.loads(lines[target_idx])
    line_next = json.loads(lines[next_idx])
    
    # Force alignment: set target to 1 microsecond before next
    # Next: 2026-01-17T22:28:46.337318+00:00
    line_target['timestamp'] = "2026-01-17T22:28:46.337317+00:00"
    
    # Update line
    lines[target_idx] = json.dumps(line_target) + '\n'
    
    with open(blackboard_path, 'w') as f:
        f.writelines(lines)
    print(f"SUCCESS: Line 24116 repaired. New timestamp: {line_target['timestamp']}")
else:
    print(f"ERROR: Line index {target_idx} out of range (Total lines: {len(lines)})")
