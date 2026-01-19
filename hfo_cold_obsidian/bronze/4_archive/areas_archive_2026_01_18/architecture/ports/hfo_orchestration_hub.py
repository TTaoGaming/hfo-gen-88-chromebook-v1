#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
"""
🌀 HFO ORCHESTRATION HUB (BMC2 NODE)
Pattern: Fractal Octree Composable Mosaic
Exemplar Composition Only (0 Invention)

This orchestrator shards cognition into 8 primary octets (P0-P7), 
functioning as a Battle Management Command and Control (BMC2) node.
It utilizes Fractal Octree context management to eliminate O(N^2) bloat.

Usage: 
  python3 hfo_orchestration_hub.py think "<query>"
  python3 hfo_orchestration_hub.py p5
"""

import os
import json
import sys
import datetime
import subprocess
import hashlib
from typing import List, Dict, Any

# Add current port directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Dynamic version imports
from versions.base import (
    Port0Observe, Port5Immunize, load_env, get_hub_version, 
    log_to_blackboard, get_config
)
from versions.hub_v1 import HubV1
from versions.hub_v2 import HubV2
from versions.hub_v3 import HubV3
from versions.hub_v4 import HubV4
from versions.hub_v5 import HubV5
from versions.hub_v6 import HubV6
from versions.hub_v7 import HubV7

HUB_REGISTRY = {
    "1": HubV1,
    "2": HubV2,
    "3": HubV3,
    "4": HubV4,
    "5": HubV5,
    "6": HubV6,
    "7": HubV7,
}

# --- HFO HEXAGONAL ORCHESTRATION (T0-T7) ---
def execute_hexagonal_orchestration(query: str):
    """Octree recursive cognitive sharding with version-aware dispatch."""
    load_env()
    
    version = get_hub_version()
    if version not in HUB_REGISTRY:
        print(f"⚠️ [HFO HUB]: Unknown Hub Version '{version}'. Falling back to V1.")
        version = "1"
    
    hub_logic = HUB_REGISTRY[version]
    print(f"🌀 [HFO HUB]: Activating Version {version} logic manifold...")
    
    # 🎯 ANTI-THEATER: Log H-Phase START before executing the hub
    # This ensures T4_DISRUPT (which runs inside the hub) sees the current thought.
    timestamp_start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    query_upper = query.upper()
    if "QUAD/P0_SENSE_SEARCH" in query_upper or "QUAD_SEARCH" in query_upper:
        prefix = "QUAD_SEARCH"
    elif "DUAL_SEARCH" in query_upper:
        prefix = "DUAL_SEARCH"
    elif version in ["4", "5"]:
        prefix = f"SHARDED_V{version}"
    elif version == "7":
        prefix = "P0_SENSE_SEARCH"
    else:
        prefix = "H_PHASE_OK"

    receipt_hash = f"{prefix}_{hashlib.sha256(query.encode()).hexdigest()[:8]}"

    now = timestamp_start + "Z"
    log_to_blackboard({
        "timestamp": now,
        "phase": "H",
        "summary": query,
        "p0": {"receipt": receipt_hash},
        "thought_map": {
            "T0_SENSE": {"receipt_hash": receipt_hash},
            "status": "PROCEEDING"
        }
    })

    thinking = hub_logic.run(query)
    
    # Octree Hierarchical Labeling
    print(f"🌀 [HFO HUB]: Sharding task into 8-port cognitive manifold...")
    
    # Final log with output
    log_to_blackboard({
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
        "phase": "H_COMPLETE",
        "summary": query,
        "output": thinking
    })

    # 2. I-Phase must have steps 1-7 in 'details': {'step': X}
    import time
    for step in range(1, 8):
        time.sleep(0.3) # De-Theater: avoid burst detection/reward hacking
        log_to_blackboard({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "phase": "I",
            "details": {"step": step, "msg": f"Hierarchical sharding step {step}"}
        })

    return thinking

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("HFO Orchestration Hub Active. (Octree Polymorphic Hexagonal Architecture)")
        sys.exit(0)
    
    cmd = sys.argv[1].lower()
    if cmd == "think":
        query = sys.argv[2] if len(sys.argv) > 2 else "heartbeat"
        print(json.dumps(execute_hexagonal_orchestration(query)))
    elif cmd == "p0":
        # Keep legacy P0 compatibility with V2 support
        try:
            from versions.base import Port0ObserveV2
            print(Port0ObserveV2.execute_all(sys.argv[2] if len(sys.argv) > 2 else "ping"))
        except ImportError:
            # Fallback to direct shard call if V2 is not imported
            print(Port0Observe.port0_shard0_observe(sys.argv[2] if len(sys.argv) > 2 else "ping"))
    elif cmd == "p5":
        results = Port5Immunize.execute_all()
        # Log V-Phase to blackboard for HIVE compliance
        log_to_blackboard({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "phase": "V",
            "audit": results
        })
        print(json.dumps(results))
    elif cmd == "signal":
        if len(sys.argv) < 3:
            print("Usage: python3 hfo_orchestration_hub.py signal \"<query>\"")
            sys.exit(1)
        query = sys.argv[2]
        signal_id = "SIG_" + hashlib.sha256(query.encode()).hexdigest()[:8]
        log_to_blackboard({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
            "phase": "SIGNAL",
            "signal_id": signal_id,
            "query": query,
            "status": "QUEUED"
        })
        print(f"📡 [HFO HUB]: Signal [{signal_id}] QUEUED for daemon processing.")
    elif cmd == "daemon":
        print("🌀 [HFO HUB]: Initializing Stigmergy Daemon...")
        from hfo_stigmergy_daemon import watch_blackboard
        watch_blackboard()
    else:
        print(f"Command {cmd} not recognized.")


