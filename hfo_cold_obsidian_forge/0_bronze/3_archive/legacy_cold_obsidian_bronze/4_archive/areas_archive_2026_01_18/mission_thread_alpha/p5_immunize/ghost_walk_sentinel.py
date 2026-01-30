#!/usr/bin/env python3
import json
import os
import sys

# Medallion: Bronze | Mutation: 0% | HIVE: V
# PORT-5-IMMUNIZE: GHOST-SHIELD (Stigmergy Orphan Detection)
# Attack Vector: ORPHAN_LOGIC
# Logic: Any new file must be preceded or accompanied by a blackboard entry.

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
WORKSPACE_ROOT = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze"

def check_orphans():
    print("🛡️ [P5 GHOST-SHIELD]: Scanning for orphaned logic...")

    with open(BLACKBOARD_PATH, "r") as f:
        blackboard = f.read()

    orphans = []
    # Scan for python, ts, html files
    for root, dirs, files in os.walk(WORKSPACE_ROOT):
        for f in files:
            if f.endswith(('.py', '.ts', '.html', '.yaml')):
                # Check if filename is mentioned in blackboard
                if f not in blackboard:
                    # Ignore specific generic files
                    if f in ['__init__.py', 'p5_praetorian.py']:
                        continue
                    orphans.append(os.path.join(root, f))

    if orphans:
        print(f"❌ [P5 GHOST-SHIELD]: BREACH: Orphaned files detected (no blackboard trace):")
        for o in orphans:
            print(f"   - {o}")
        # Soft warning for now to allow initialization
        print("⚠️ [P5 GHOST-SHIELD]: WARNING: Ensure all new files are logged in stigmergy blackboard.")
    else:
        print("✅ [P5 GHOST-SHIELD]: All active logic tracks in stigmergy.")

    return True

if __name__ == "__main__":
    check_orphans()
