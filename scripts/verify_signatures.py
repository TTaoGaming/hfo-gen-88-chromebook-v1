import json
import hashlib

SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"
BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

with open(SECRET_PATH, "r") as f:
    secret = f.read().strip()

with open(BLACKBOARD_PATH, "r") as f:
    lines = f.readlines()
    last_sig = "ROOT"
    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        try:
            entry = json.loads(line)
            sig = entry.pop("signature")
            prev = last_sig if last_sig != "ROOT" else "LEGACY"
            entry_str = json.dumps(entry, sort_keys=True)
            expected = hashlib.sha256(f"{secret}:{prev}:{entry_str}".encode()).hexdigest()
            
            # Root entry check
            if sig != expected and last_sig == "ROOT":
                expected_legacy = hashlib.sha256(f"{secret}:LEGACY:{entry_str}".encode()).hexdigest()
                if sig == expected_legacy: expected = expected_legacy

            if sig != expected:
                print(f"Fracture at line {i+1}!")
                print(f"  Prev Sig: {prev}")
                print(f"  Found:    {sig}")
                print(f"  Expected: {expected}")
                print(f"  Entry:    {entry_str}")
            
            last_sig = sig
        except Exception as e:
            print(f"Error at line {i+1}: {e}")
