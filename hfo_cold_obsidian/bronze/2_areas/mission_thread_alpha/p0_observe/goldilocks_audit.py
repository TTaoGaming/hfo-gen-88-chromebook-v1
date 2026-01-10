# Medallion: Bronze | Mutation: 0% | HIVE: V
import json
import os
import sys
from datetime import datetime

# Provenance: Port 0 Goldilocks Auditor

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

def run_audit():
    if not os.path.exists(BLACKBOARD_PATH):
        print(f"❌ Blackboard not found at {BLACKBOARD_PATH}")
        return

    screams = []
    completes = []

    with open(BLACKBOARD_PATH, "r") as f:
        for line in f:
            if not line.strip(): continue
            try:
                entry = json.loads(line)
                if "p0" in entry:
                    if entry["p0"].get("status") == "SCREAMING":
                        screams.append(entry)
                    elif entry["p0"].get("status") == "complete":
                        completes.append(entry)
            except:
                continue

    total_p0 = len(screams) + len(completes)
    if total_p0 == 0:
        print("⚪ No Port 0 data found for audit.")
        return

    stability_score = (len(completes) / total_p0) * 100

    print(f"📊 --- GOLDILOCKS SENSE AUDIT ({datetime.now().isoformat()}) ---")
    print(f"Total Sensing Events: {total_p0}")
    print(f"Success/Complete:     {len(completes)}")
    print(f"Scream/Entropy:       {len(screams)}")
    print(f"Stability Score:      {stability_score:.1f}%")

    # Goldilocks Zone Check
    if stability_score > 99.0:
        print("🟥 CRITICAL: AI THEATER DETECTED (Stability > 99%).")
        print("   Promotion to Silver BLOCKED until entropy is injected.")
    elif stability_score < 80.0:
        print("🟨 WARNING: SYSTEM FRAGILE (Stability < 80%).")
        print("   Acceptable for Bronze experimentation. Fix required for Silver.")
    elif 80.0 <= stability_score <= 99.0:
        print("✅ GOLDILOCKS ZONE ATTAINED (80-99%).")
        print("   System is honest and resilient. Silver promotion READY.")
    else:
        print("❓ Score unusual.")

if __name__ == "__main__":
    run_audit()
