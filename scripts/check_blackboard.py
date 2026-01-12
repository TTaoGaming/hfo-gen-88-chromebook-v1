import json
from datetime import datetime

file_path = '/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl'

def parse_ts(ts_str):
    # Standardize to ISO format that datetime.fromisoformat can handle
    ts_str = ts_str.replace('Z', '+00:00')
    if ts_str.count('+00:00') > 1:
        ts_str = ts_str.replace('+00:00+00:00', '+00:00')
    return datetime.fromisoformat(ts_str)

with open(file_path, 'r') as f:
    last_ts = None
    for i, line in enumerate(f):
        try:
            data = json.loads(line)
            ts = parse_ts(data['timestamp'])
            if last_ts and ts < last_ts:
                print(f"Fracture at line {i+1}: {ts} < {last_ts}")
                print(f"Current: {line.strip()}")
            last_ts = ts
        except Exception as e:
            print(f"Error at line {i+1}: {e}")
