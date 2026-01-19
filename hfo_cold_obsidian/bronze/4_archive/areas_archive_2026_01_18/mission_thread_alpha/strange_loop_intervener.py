#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: I
"""
🌀 STRANGE LOOP INTERVENER (P4 <-> P5)
Formalizes the feedback loop between the Red Regnant's Grudges and the Pyre Praetorian's Rebirths.
"""

import os
import json
import datetime

# Paths
P4_GRUDGES = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p4_disrupt/BOOK_OF_BLOOD_GRUDGES.jsonl"
P5_REBIRTHS = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p5_defend/DANCE_OF_DEATH_AND_REBIRTH.jsonl"

def get_last_entry(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        lines = f.readlines()
        if not lines:
            return None
        try:
            return json.loads(lines[-1])
        except json.JSONDecodeError:
            return None

def main():
    print("🌀 [HFO]: Initializing Strange Loop Intervention...")
    
    last_grudge = get_last_entry(P4_GRUDGES)
    last_rebirth = get_last_entry(P5_REBIRTHS)
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Intervention Logic: If a grudge exists and hasn't been "Immunized" or "Hardened"
    if last_grudge and last_grudge.get("severity") == "CRITICAL":
        msg = last_grudge.get("msg") or last_grudge.get("description")
        
        # Check if the last rebirth already addressed this
        if last_rebirth and msg in last_rebirth.get("msg", ""):
            print("✅ [HFO]: No new intervention required. Last grudge already addressed.")
        else:
            print(f"🚨 [P5 INTERVENE]: Critical Grudge detected: {msg}")
            
            # Record Death (Detection of the breach)
            death_entry = {
                "timestamp": timestamp,
                "port": "P5",
                "phase": "V",
                "type": "DEATH",
                "msg": f"Breach detected via P4 Grudge: {msg}. Initiating Pyre Cycle."
            }
            
            # Record Rebirth (Proposed Hardening)
            rebirth_entry = {
                "timestamp": timestamp,
                "port": "P5",
                "phase": "E",
                "type": "REBIRTH",
                "msg": f"Hardening system against: {msg}. Synchronizing Praetorian gates."
            }
            
            with open(P5_REBIRTHS, "a") as f:
                f.write(json.dumps(death_entry) + "\n")
                f.write(json.dumps(rebirth_entry) + "\n")
            
            print("🔥 [P5]: Death and Rebirth cycle logged.")

    elif last_rebirth and last_rebirth.get("type") == "REBIRTH":
        print("🕯️ [P4 INTERVENE]: System hardened. Red Regnant observing for next drift...")
        # (Later: Logic for P4 to acknowledge the rebirth and reduce disruption pressure)

if __name__ == "__main__":
    main()
