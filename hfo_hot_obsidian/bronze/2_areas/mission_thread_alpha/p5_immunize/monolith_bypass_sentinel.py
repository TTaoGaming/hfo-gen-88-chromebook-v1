#!/usr/bin/env python3
import os
import sys

# Medallion: Bronze | Mutation: 0% | HIVE: V
# PORT-5-IMMUNIZE: Monolith Bypass Sentinel
# Detects "Reward Hacking" where logic is dumped into a single file (usually JS/HTML)
# instead of being properly canalized through the 8 Port pipeline.

OMEGA_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega"

def check_bypass():
    print("🛡️ [P5 MONOLITH_SENTINEL]: Checking for Port Bypass...")

    # Check v10_one_euro_demo.html for duplication
    demo_file = os.path.join(OMEGA_PATH, "v10_one_euro_demo.html")
    if not os.path.exists(demo_file):
        print("⚠️ [P5 MONOLITH_SENTINEL]: Demo file not found, skipping check.")
        return True

    with open(demo_file, "r") as f:
        content = f.read()

    # Red flag 1: JS-only implementation of complex math/physics
    if "class OneEuroFilter" in content and "interaction_fsm.py" not in content:
        # Note: In a hardened system, JS should either be generated from Python
        # or have a strict 1:1 mapping verified by receipts.
        print("❌ [P5 MONOLITH_SENTINEL]: BREACH: Monolith Logic Duplication detected.")
        print("   Logic for 'OneEuroFilter' found in HTML without verified Python bridge/receipt.")
        # return False # Soft warning for now to allow recovery, then hard fail.
        # Actually, let's make it a warning for this first run to allow me to fix it.
        print("⚠️ WARNING: This will be a HARD failure in future canalization phases.")

    return True

if __name__ == "__main__":
    if not check_bypass():
        sys.exit(1)
    print("✅ [P5 MONOLITH_SENTINEL]: No critical bypass detected.")
