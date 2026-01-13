# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import os
import json

# Add hub path to sys.path
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/ports")

from versions.base import Port7Navigate, Port5Immunize

def test_p7_shards():
    print("--- HFO Thread Alpha: Port 7 Navigator Audit ---")
    query = "HFO Phoenix Reconstruction"
    context = "System is in LOCKDOWN mode. Previous mission Omega Gen 4 V5.0 successfully archived."
    
    shards = {
        "N0_MAP": Port7Navigate.port7_shard0_observe,
        "N1_SINAFIN": Port7Navigate.port7_shard1_bridge,
        "N2_SYNC": Port7Navigate.port7_shard2_shape,
        "N3_LOGIC": Port7Navigate.port7_shard3_inject,
        "N4_WARP": Port7Navigate.port7_shard4_disrupt,
        "N5_VOTE": lambda q, c: Port7Navigate.port7_shard5_immunize({"p0": "READY"}, c),
        "N6_MEMO": Port7Navigate.port7_shard6_assimilate,
        "N7_BMC2": Port7Navigate.port7_shard7_navigate
    }
    
    results = {}
    for name, shard_func in shards.items():
        print(f"Testing {name}...")
        try:
            res = shard_func(query, context)
            status = "PASS" if isinstance(res, dict) and res.get("status") != "DEGRADED" else "FAIL"
            if res.get("status") == "STUB": status = "STUB"
            
            results[name] = {"status": status, "data_type": type(res).__name__, "message": res.get("message", "N/A")}
            if status == "FAIL":
                 print(f"  ❌ {name} failed: {res}")
            elif status == "STUB":
                 print(f"  🟡 {name} is a STUB.")
            else:
                 print(f"  ✅ {name} passed.")
        except Exception as e:
            print(f"  ❌ {name} error: {e}")
            results[name] = {"status": "ERROR", "message": str(e)}
            
    print("\n--- Summary ---")
    print(json.dumps(results, indent=2))
    
    # Port 5 Audit
    audit = Port5Immunize.shard0_hardgate(__file__)
    print(f"\nP5 Hardgate: {audit.get('status')} - {audit.get('message')}")

if __name__ == "__main__":
    test_p7_shards()
