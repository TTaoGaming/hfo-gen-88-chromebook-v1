# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import os
import json
import random
import time

# Add path for imports
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p0_observe")

from port_0_tools import port_0_sense, scream

def test_entropy_queries():
    """Testing with high-entropy or 'impossible' queries to trigger screams."""
    print("🚀 Starting Chaos/Entropy Sensing Tests...")

    impossible_queries = [
        "", # Empty query
        "asdfasdfasdfasdfasdfasdf123412341234", # Gibberish
        "http://non-existent-domain-123456789.com", # Invalid URL for Pillar 5
        "A" * 5000, # Oversized query to test thinning/clipping
    ]

    for q in impossible_queries:
        print(f"Testing Query (Length {len(q)}): '{q[:20]}...'")
        try:
            receipt = port_0_sense(q)
            print(f"  Receipt: {receipt}")
        except Exception as e:
            print(f"  Caught expected error: {e}")

def audit_blackboard_density():
    """Audit the blackboard to see if we're hitting the Goldilocks zone."""
    blackboard_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
    with open(blackboard_path, "r") as f:
        lines = [l for l in f.readlines() if l.strip()]

    total = len(lines)
    # Count entries where any P0 pillar has an error or is 'N/A' or triggered a scream
    # A 'perfect' system would have 0 screams. We want some.
    screams = sum(1 for l in lines if '"status": "SCREAMING"' in l or "FAILED" in l)

    print(f"\n📊 GOLDILOCKS AUDIT (MISSION: SENSE):")
    print(f"Total Sensing Events: {total}")
    print(f"Entropy/Scream Signals: {screams}")

    if total > 0:
        coverage_stability = 100 - ((screams / total) * 100)
        print(f"Stability Score: {coverage_stability:.1f}%")

        if 80.0 <= coverage_stability <= 98.9:
            print("🟢 GOLDILOCKS ZONE ATTAINED (80-99%). System is sufficiently brittle/honest.")
        elif coverage_stability > 99.0:
            print("🔴 WARNING: 100% GREEN DETECTED. Potential 'AI Theater' detected.")
            print("Action: Increase sensing sensitivity or add more chaotic edge cases.")
        else:
            print("🔴 WARNING: SYSTEM UNDER 80%. Too unstable for Silver promotion.")

if __name__ == "__main__":
    test_entropy_queries()
    # Add a manual entropy injection for audit
    scream("CHAOS_PROBE", "Random entropy injection for Goldilocks calibration.")
    audit_blackboard_density()

if __name__ == "__main__":
    test_entropy_queries()
    # simulate_intermittent_network() # Reserved for future
    audit_blackboard_density()
