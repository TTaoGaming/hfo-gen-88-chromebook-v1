import json
import hashlib
import os
import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: E

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

def reinit_blackboard():
    secret = "HFO_DEFAULT_SECRET"
    if os.path.exists(SECRET_PATH):
        with open(SECRET_PATH, "r") as f:
            secret = f.read().strip()

    # Move current to quarantine if it exists and has content
    if os.path.exists(BLACKBOARD_PATH) and os.path.getsize(BLACKBOARD_PATH) > 0:
        quarantine_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/blackboard_quarantine.jsonl"
        os.rename(BLACKBOARD_PATH, quarantine_path)
        print(f"📦 Existing blackboard moved to {quarantine_path}")

    # Create fresh REINIT entry
    reinit_entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "phase": "THEATER_BREACH",
        "summary": "REINIT: Resetting Cryptographic Blackboard Chain for Armored Gen 88.",
        "p0": {"receipt": "REINIT_AUTO_STABILIZE"}
    }
    
    # Sign it as LEGACY (start of chain)
    entry_str = json.dumps(reinit_entry, sort_keys=True)
    signature = hashlib.sha256(f"{secret}:LEGACY:{entry_str}".encode()).hexdigest()
    reinit_entry["signature"] = signature
    
    with open(BLACKBOARD_PATH, "w") as f:
        f.write(json.dumps(reinit_entry, sort_keys=True) + "\n")
    
    print("✅ Blackboard REINIT successful. Chain started.")

if __name__ == "__main__":
    reinit_blackboard()
