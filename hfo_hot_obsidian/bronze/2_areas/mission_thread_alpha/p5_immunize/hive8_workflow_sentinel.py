#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: V
# PORT-5-IMMUNIZE: Hive 8 Workflow Sentinel
# Enforces Dual Search and 8-Step Sequential Thinking requirements.

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

def check_workflow():
    if not os.path.exists(BLACKBOARD_PATH):
        print("❌ [P5 HIVE8_SENTINEL]: Blackboard not found.")
        return False

    with open(BLACKBOARD_PATH, "r") as f:
        lines = f.readlines()

    if not lines:
        print("❌ [P5 HIVE8_SENTINEL]: Blackboard is empty.")
        return False

    # Reversing to find the most recent interaction block
    current_thoughts = set()
    found_recent_h = False
    quad_search_found = False

    for line in reversed(lines):
        try:
            entry = json.loads(line)
            phase = entry.get("phase")

            if phase == "H":
                found_recent_h = True
                p0 = entry.get("p0", {})
                receipt = p0.get("receipt", "")
                # Accept both legacy and new OBSERVE prefixes during migration
                valid_prefixes = ["QUAD_SEARCH", "DUAL_SEARCH", "P0_SENSE_SEARCH", "OBSERVE_SEARCH", "QUAD_OBSERVE"]
                if any(x in receipt for x in valid_prefixes):
                    quad_search_found = True

                # Violation detection for generic web_fetch bypass
                if p0.get("status") == "breached":
                    print(f"🚨 [P5 HIVE8_SENTINEL]: Breach detected in blackboard: {p0.get('violation')}")
                    return False

            if phase == "I":
                details = entry.get("details", {})
                step = details.get("step")
                if step:
                    current_thoughts.add(int(step))

            # Stop once we hit a dispatch from a PREVIOUS session
            if found_recent_h and phase == "E":
                break

        except Exception:
            continue

    # Validation Logic:
    # 1. H-Phase MUST have a valid search receipt.
    if not found_recent_h:
         print("⚠️ [P5 WARNING]: No H-Phase detected in recent blackboard history.")
    elif not quad_search_found:
        print("❌ [P5 HIVE8_SENTINEL]: BREACH: H-Phase detected without QUAD/P0_SENSE_SEARCH receipt.")
        return False

    # 2. Sequential Thinking Enforcement (HIVE/8)
    # Required steps for a 'Valid' interaction. Step 8 is 'Audit for Reward Hacking'.
    required_steps = {1, 2, 3, 4, 5, 6, 7}
    missing = required_steps - current_thoughts
    if found_recent_h and missing:
        print(f"❌ [P5 HIVE8_SENTINEL]: BREACH: Missing sequential thinking steps: {missing}")
        return False

    # 3. Time-Entropy / Reward Hacking Audit
    # Genuine sequential thinking requires temporal spacing.
    # We only check the most recent session block (post-last 'E' phase).
    recent_i_timestamps = []
    found_e = False
    for line in reversed(lines):
        try:
            entry = json.loads(line)
            if entry.get("phase") == "E":
                found_e = True
                break
            if entry.get("phase") == "I":
                 ts_str = entry.get("timestamp")
                 if ts_str.endswith("Z"):
                     ts_str = ts_str[:-1]
                 # Ensure we have a naive datetime for comparison
                 dt = datetime.fromisoformat(ts_str)
                 if dt.tzinfo is not None:
                     dt = dt.replace(tzinfo=None)
                 recent_i_timestamps.append(dt)
        except: continue
    
    # Sort reversed list to get chronological order for delta calc
    recent_i_timestamps.sort()

    if len(recent_i_timestamps) > 1:
        deltas = [(recent_i_timestamps[i] - recent_i_timestamps[i-1]).total_seconds() for i in range(1, len(recent_i_timestamps))]
        # Threshold: Thinking < 0.2s is physically impossible for a genuine agent cycle.
        fast_thoughts = [d for d in deltas if d < 0.2]
        if len(fast_thoughts) >= 3: 
            print(f"🚨 [P5 HIVE8_SENTINEL]: BREACH (REWARD_HACKING): Synthetic thought burst detected in recent session ({len(fast_thoughts)} steps < 0.2s). Stop lazy slop generation.")
            return False

    if quad_search_found:
        print("✅ [P5 HIVE8_SENTINEL]: Hive/8 Protocol Validated.")
        return True

    return True # Allow if no H-phase started yet

if __name__ == "__main__":
    if not check_workflow():
        sys.exit(1)
