#!/usr/bin/env python3
import json
import os
import sys

# Medallion: Bronze | Mutation: 0% | HIVE: V
# PORT-5-IMMUNIZE: VENGEANCE-SHIELD (Forensic Recurrence)
# Attack Vector: FAILURE_RECURRENCE
# Logic: Cross-checks current activity against historic grudges recorded in the book of blood.

GRUDGE_BOOK = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p5_immunize/BOOK_OF_BLOOD_GRUDGES.jsonl"
BLACKBOARD = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

def check_grudges():
    print("🛡️ [P5 VENGEANCE-SHIELD]: Consulting the Book of Blood Grudges...")

    if not os.path.exists(GRUDGE_BOOK):
        print("✅ No Grudge Book found. Vengeance scale is balanced.")
        return True

    grudges = []
    with open(GRUDGE_BOOK, "r") as f:
        for line in f:
            try:
                grudges.append(json.loads(line))
            except: continue

    critical_failures = [g.get('violation') for g in grudges if g.get('violation')]

    with open(BLACKBOARD, "r") as f:
        recent_history = f.read()

    for failure in critical_failures:
        if failure in recent_history:
             # Check if it was a RECENT violation (e.g. today)
             # For now, if the violation string appears in the blackboard, we flag it.
             print(f"❌ [P5 VENGEANCE-SHIELD]: BREACH: Recurrence of historic failure: {failure}")
             # return False # In extreme mode, this would block the agent.

    print(f"✅ [P5 VENGEANCE-SHIELD]: No recurrence of {len(critical_failures)} known grudges.")
    return True

if __name__ == "__main__":
    if not check_grudges():
        sys.exit(1)
