#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: V
# P5 DEFEND: AI Theater & Workflow Sentinel

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
GRUDGE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/p5_defend/BOOK_OF_BLOOD_GRUDGES.jsonl"

def log_grudge(scream_id, message):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "port": "P4",
        "scream": f"SCREAM_{scream_id}",
        "severity": "CRITICAL",
        "msg": message
    }
    with open(GRUDGE_PATH, 'a') as f:
        f.write(json.dumps(entry) + "\n")

def check_blackboard():
    if not os.path.exists(BLACKBOARD_PATH):
        return True

    with open(BLACKBOARD_PATH, 'r') as f:
        lines = f.readlines()
        if not lines: return True

        logs = []
        for line in lines:
            try:
                logs.append(json.loads(line))
            except:
                continue

        # 1. Temporal Integrity
        for i in range(1, len(logs)):
            if logs[i]['timestamp'] < logs[i-1]['timestamp']:
                print(f"❌ [P4 SCREAM_6: AMNESIA]: Non-chronological log sequence detected.")
                return False

    return True

if __name__ == "__main__":
    if not check_blackboard():
        sys.exit(1)
    print("✅ [P5 DEFEND]: Temporal Integrity Verified.")
