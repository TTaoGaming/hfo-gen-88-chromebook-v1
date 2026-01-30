# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import os
import json

# Add path for imports
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p0_observe")

from port_0_tools import port_0_sense, scream

def test_scream_to_blackboard():
    print("Testing SCREAM logic...")
    scream("TEST_PILLAR", "Simulated failure for validation")

    # Check if it hit the blackboard
    blackboard_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
    with open(blackboard_path, "r") as f:
        lines = f.readlines()
        last_line = json.loads(lines[-1])
        assert last_line["p0"]["status"] == "SCREAMING"
        assert last_line["p0"]["pillar"] == "TEST_PILLAR"
    print("✅ SCREAM logic verified.")

def test_full_sense_flow():
    print("Testing full sense flow...")
    receipt = port_0_sense("HFO Gen 88 Test")
    assert receipt.startswith("P0_SENSE_")

    # Check blackboard
    blackboard_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
    with open(blackboard_path, "r") as f:
        lines = f.readlines()
        last_line = json.loads(lines[-1])
        assert last_line["p0"]["receipt"] == receipt
        assert "p1_tavily" in last_line["p0"]["data"]
    print("✅ Full sense flow verified.")

if __name__ == "__main__":
    try:
        test_scream_to_blackboard()
        test_full_sense_flow()
        print("\n🏆 ALL SENSE INFRA CONSOLIDATION TESTS PASSED.")
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        sys.exit(1)
