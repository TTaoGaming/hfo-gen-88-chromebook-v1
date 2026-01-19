# Medallion: Bronze | Mutation: 0% | HIVE: V
import json
import hashlib
import os

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

def verify_root():
    if not os.path.exists(BLACKBOARD_PATH) or not os.path.exists(SECRET_PATH):
        print("Missing files")
        return

    with open(SECRET_PATH, "r") as f:
        secret = f.read().strip()

    with open(BLACKBOARD_PATH, "r") as f:
        line1 = f.readline().strip()
        if not line1:
            print("Empty file")
            return
        
        entry = json.loads(line1)
        sig = entry.pop("signature")
        entry_str = json.dumps(entry, sort_keys=True)
        
        # Check LEGACY path (Hub base.py logic)
        expected_legacy = hashlib.sha256(f"{secret}:LEGACY:{entry_str}".encode()).hexdigest()
        
        print(f"Line 1 Signature: {sig}")
        print(f"Expected Legacy:  {expected_legacy}")
        
        if sig == expected_legacy:
            print("MATCH")
        else:
            print("MISMATCH")

if __name__ == "__main__":
    verify_root()
# Test trigger
