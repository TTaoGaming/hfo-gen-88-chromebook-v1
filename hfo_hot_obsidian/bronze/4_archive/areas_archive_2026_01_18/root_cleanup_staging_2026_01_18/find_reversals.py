# Medallion: Bronze | Mutation: 0% | HIVE: V
import json
from datetime import datetime

file_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

reversals = []
prev_dt = None
prev_line = ""

with open(file_path, "r") as f:
    for i, line in enumerate(f, 1):
        try:
            entry = json.loads(line)
            ts = entry.get("timestamp")
            if not ts:
                continue
            
            # Normalize timestamp to naive datetime
            ts_str = ts.replace("Z", "").replace(" ", "T")
            if "+" in ts_str:
                ts_str = ts_str.split("+")[0]
            if "." not in ts_str:
                ts_str += ".000000"
            
            try:
                current_dt = datetime.fromisoformat(ts_str)
            except ValueError:
                current_dt = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%f")
            
            if prev_dt and current_dt < prev_dt:
                reversals.append({
                    "line": i,
                    "prev_ts": prev_dt.isoformat(),
                    "curr_ts": current_dt.isoformat(),
                    "diff": (prev_dt - current_dt).total_seconds()
                })
            
            prev_dt = current_dt
            prev_line = line
        except Exception as e:
            print(f"Error at line {i}: {e}")

if reversals:
    print(f"Found {len(reversals)} reversals:")
    for r in reversals:
        print(f"Line {r['line']}: {r['prev_ts']} -> {r['curr_ts']} (Diff: {r['diff']}s)")
else:
    print("No timestamp reversals found.")
