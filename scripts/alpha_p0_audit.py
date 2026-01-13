# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import os
import json

# Add hub path to sys.path
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/ports")

from versions.base import Port0Observe, Port0ObserveV2, Port5Immunize

def test_p0_shards():
    print("--- HFO Thread Alpha: Port 0 Shard Audit ---")
    query = "HFO Phoenix Reconstruction"
    
    shards = {
        "O0_TAVILY": Port0Observe.port0_shard0_observe,
        "O1_ARXIV": Port0Observe.port0_shard1_bridge,
        "O2_DDG": Port0Observe.port0_shard2_shape,
        "O3_GITHUB": Port0Observe.port0_shard3_inject,
        "O4_REPO": Port0Observe.port0_shard4_disrupt,
        "O5_BLACKBOARD": Port0Observe.port0_shard5_immunize,
        "O6_WIKI": Port0ObserveV2.port0_shard6_assimilate_v2,
        "O7_AGENTS": Port0Observe.port0_shard7_navigate
    }
    
    results = {}
    for name, shard_func in shards.items():
        print(f"Testing {name}...")
        try:
            res = shard_func(query)
            status = "PASS" if isinstance(res, dict) and res.get("status") != "FAIL" else "FAIL"
            results[name] = {"status": status, "data_type": type(res).__name__}
            if status == "FAIL":
                 print(f"  ❌ {name} failed: {res}")
            else:
                 print(f"  ✅ {name} passed.")
        except Exception as e:
            print(f"  ❌ {name} error: {e}")
            results[name] = {"status": "ERROR", "message": str(e)}
            
    print("\n--- Summary ---")
    print(json.dumps(results, indent=2))
    
    # Port 5 Audit of the test script itself
    audit = Port5Immunize.shard0_hardgate(__file__)
    print(f"\nP5 Hardgate: {audit.get('status')} - {audit.get('message')}")

if __name__ == "__main__":
    test_p0_shards()
