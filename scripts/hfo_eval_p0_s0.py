#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""
HFO EVALUATION HARNESS: PORT 0 SHARD 0 (TAVILY SENSE)
Checks connectivity, latency, and relevance for ISR sharding.
"""

import sys
import os
import time
import json
import datetime

# Setup paths
BASE_DIR = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
PORTS_DIR = os.path.join(BASE_DIR, "hfo_hot_obsidian/bronze/2_areas/architecture/ports")
sys.path.append(PORTS_DIR)

try:
    from versions.base import Port0Observe, load_env, log_to_blackboard
except ImportError as e:
    print(f"❌ [EVAL-FAIL]: Failed to import Port0Observe: {e}")
    sys.exit(1)

def run_eval():
    print("🚀 [HFO-EVAL]: Starting Port 0 Shard 0 (Tavily) Audit...")
    
    # Check Env
    load_env()
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("❌ [EVAL-FAIL]: TAVILY_API_KEY missing from environment.")
        return False

    test_queries = [
        "Hyper-Fractal Obsidian Orchestration",
        "JADC2 Mosaic Warfare DARPA",
        "Medallion Framework Mutation Scoring Stryker"
    ]
    
    results = []
    
    for query in test_queries:
        print(f"📡 [EVAL-SENSE]: Querying: '{query}'...")
        start_time = time.time()
        
        try:
            output = Port0Observe.port0_shard0_observe(query)
            latency = (time.time() - start_time) * 1000
            
            error = output.get("error")
            if error:
                print(f"❌ [EVAL-ERROR]: {error}")
                results.append({"query": query, "status": "FAIL", "error": error, "latency_ms": latency})
                continue
                
            res_count = len(output.get("results", []))
            print(f"✅ [EVAL-PASS]: {res_count} nodes retrieved in {latency:.2f}ms")
            
            results.append({
                "query": query,
                "status": "PASS",
                "latency_ms": latency,
                "count": res_count,
                "top_title": output.get("results", [{}])[0].get("title") if res_count > 0 else "N/A"
            })
            
        except Exception as e:
            print(f"❌ [EVAL-CRASH]: {e}")
            results.append({"query": query, "status": "CRASH", "error": str(e)})

    # Summary
    success_count = sum(1 for r in results if r["status"] == "PASS")
    avg_latency = sum(r.get("latency_ms", 0) for r in results if r["status"] == "PASS") / max(1, success_count)
    
    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "port_shard": "P0.0",
        "status": "GREEN" if success_count == len(test_queries) else "YELLOW" if success_count > 0 else "RED",
        "metrics": {
            "success_rate": f"{success_count}/{len(test_queries)}",
            "avg_latency_ms": f"{avg_latency:.2f}"
        },
        "results": results
    }

    print("\n📊 [EVAL-REPORT]:")
    print(json.dumps(report, indent=2))
    
    # Log to blackboard
    log_to_blackboard({
        "phase": "V",
        "event": "PORT_SHARD_EVAL",
        "port": 0,
        "shard": 0,
        "report": report
    })
    
    return success_count == len(test_queries)

if __name__ == "__main__":
    run_eval()
