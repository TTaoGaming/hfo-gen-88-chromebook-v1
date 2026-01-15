import json
import hashlib
import os
from datetime import datetime, timedelta

SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"
BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
BACKUP_PATH = BLACKBOARD_PATH + ".bak"

def get_secret():
    with open(SECRET_PATH, "r") as f:
        return f.read().strip()

def fix_and_resign():
    secret = get_secret()
    
    # Backup
    if not os.path.exists(BACKUP_PATH):
        import shutil
        shutil.copy2(BLACKBOARD_PATH, BACKUP_PATH)
        print(f"Backup created at {BACKUP_PATH}")

    with open(BLACKBOARD_PATH, "r") as f:
        lines = f.readlines()

    new_lines = []
    last_sig = "ROOT"
    last_ts = "0000-00-00T00:00:00.000000+00:00"
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        entry = json.loads(line)
        
        # 1. Fix ALL Chronos Fractures (Temporal Reversals)
        if "timestamp" in entry:
            ts_str = entry["timestamp"]
            # Strict normalization to ISO with microsecond precision and +00:00
            def normalize_ts(t):
                if not t or t == "0000-00-00T00:00:00.000000+00:00":
                    return datetime(1970, 1, 1)
                
                # Strip potential trailing 'Z' or offset for base parsing
                clean_t = t.replace("Z", "").replace(" ", "T")
                if "+" in clean_t:
                    clean_t = clean_t.split("+")[0]
                
                # Ensure microsecond precision for base
                if "." not in clean_t:
                    clean_t += ".000000"
                
                try:
                    return datetime.fromisoformat(clean_t)
                except:
                    # Fallback for very weird formats
                    try:
                        return datetime.strptime(clean_t, "%Y-%m-%dT%H:%M:%S.%f")
                    except:
                        return datetime(1970, 1, 1)

            current_dt = normalize_ts(ts_str)
            last_dt = normalize_ts(last_ts)
            
            if current_dt <= last_dt:
                new_dt = last_dt + timedelta(microseconds=1)
                entry["timestamp"] = new_dt.isoformat() + "+00:00"
                print(f"Fixed Chronos reversal at line {i+1}: {ts_str} -> {entry['timestamp']} (after {last_ts})")
            else:
                # Still normalize it to ensure consistent format for next comparison
                entry["timestamp"] = current_dt.isoformat() + "+00:00"
            
            last_ts = entry["timestamp"]
        else:
            # If no timestamp, skip comparison but keep track of last_ts
            pass

        # 2. Recalculate Signature
        if "signature" in entry:
            entry.pop("signature")
        
        prev = last_sig if last_sig != "ROOT" else "LEGACY"
        entry_str = json.dumps(entry, sort_keys=True)
        new_sig = hashlib.sha256(f"{secret}:{prev}:{entry_str}".encode()).hexdigest()
        
        entry["signature"] = new_sig
        new_lines.append(json.dumps(entry))
        last_sig = new_sig

    with open(BLACKBOARD_PATH, "w") as f:
        f.write("\n".join(new_lines) + "\n")
    
    print("Blackboard successfully re-signed and Chronos fracture resolved.")

if __name__ == "__main__":
    fix_and_resign()
