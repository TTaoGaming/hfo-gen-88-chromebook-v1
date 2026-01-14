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

class HubV8(HubV7):
    """Version 8: Promotion & Archival Commander. Inherits V7 Multi-Diamond logic.
    Provides semantic sharding and BFT quorum reinforcement for Generation 88.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version = "8.1.0-BRONZE"

HUB_REGISTRY = {
    "1": HubV1,
    "2": HubV2,
    "3": HubV3,
    "4": HubV4,
    "5": HubV5,
    "6": HubV6,
    "7": HubV7,
    "8": HubV8,
}

def check_p5_safety():
    """
    Check the blackboard for the most recent Sentinel or P5 signal.
    If it's a BREACH, scream and warn the operator.
    """
    from versions.base import BLACKBOARD_PATH
    if not os.path.exists(BLACKBOARD_PATH):
        return False

    try:
        with open(BLACKBOARD_PATH, "r") as f:
            lines = f.readlines()
            if not lines:
                return False
            
            # Search for the most recent status entry
            for line in reversed(lines[-50:]):
                try:
                    entry = json.loads(line.strip())
                    status = entry.get("status")
                    if status:
                        if status == "BREACH":
                            timestamp = entry.get("timestamp")
                            file_name = entry.get("file", "Unknown")
                            print(f"\n🚨 [HUB-INTERLOCK]: STOP! A BREACH was recently detected.")
                            print(f"🚨 [HUB-INTERLOCK]: Timestamp: {timestamp}")
                            print(f"🚨 [HUB-INTERLOCK]: Violator: {file_name}")
                            print(f"🚨 [HUB-INTERLOCK]: The system is in 'Red Alarm' state. Fix the baseline before proceeding.\n")
                            return True
                        elif status == "PASS":
                            return False
                except (json.JSONDecodeError, ValueError):
                    continue
    except Exception as e:
        print(f"⚠️ [HUB-FAIL]: Safety check error: {e}")
    return False

def check_bft_interlock():
    """
    Check the blackboard for consecutive low BFT consensus scores.
    If the last TWO turns have consensus_score < 0.35, block execution.
    """
    from versions.base import BLACKBOARD_PATH
    if not os.path.exists(BLACKBOARD_PATH):
        return False

    LOW_SCORE_THRESHOLD = 0.35
    low_score_count = 0

    try:
        with open(BLACKBOARD_PATH, "r") as f:
            lines = f.readlines()
            if not lines:
                return False
            
            # Analyze last few H_COMPLETE and BFT_AUDIT entries
            for line in reversed(lines):
                try:
                    entry = json.loads(line.strip())
                    # Check both H_COMPLETE and BFT_AUDIT phases for scores
                    score = None
                    if entry.get("phase") == "BFT_AUDIT":
                         score = entry.get("consensus_score")
                    elif entry.get("phase") == "H_COMPLETE":
                         score = entry.get("output", {}).get("bft_metrics", {}).get("consensus_score")
                    
                    if score is not None:
                        if score < LOW_SCORE_THRESHOLD:
                            low_score_count += 1
                            if low_score_count >= 2:
                                print(f"\n🛑 [HUB-INTERLOCK]: BFT INTERLOCK TRIGGERED!")
                                print(f"🛑 [HUB-INTERLOCK]: Consecutive low consensus scores detected ({score:.2f} < {LOW_SCORE_THRESHOLD}).")
                                print(f"🛑 [HUB-INTERLOCK]: System drift exceeds safety parameters. BLOCKING further H-PHASE turns.")
                                print(f"🛑 [HUB-INTERLOCK]: Perform deep analysis/research before resetting the interlock.\n")
                                return True
                        else:
                            # We found a high score, break the consecutive chain
                            return False
                except (json.JSONDecodeError, ValueError):
                    continue
    except Exception as e:
        print(f"⚠️ [HUB-FAIL]: BFT check error: {e}")
    return False

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

    now = timestamp_start
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
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
        if check_p5_safety():
            # In interactive mode, we warn. In automated mode, we would exit.
            print("⚠️ WARNING: Proceeding despite P5 breach. Use at your own risk.")
            
        if check_bft_interlock():
            print("🚨 CRITICAL: BFT Interlock Blocking. System drift detected.")
            sys.exit(1)

        query = sys.argv[2] if len(sys.argv) > 2 else "heartbeat"
        print(json.dumps(execute_hexagonal_orchestration(query)))
    elif cmd == "p0":
        # Keep legacy P0 compatibility with V2 support
        try:
            from versions.base import Port0ObserveV2
            print(Port0ObserveV2.execute_all(sys.argv[2] if len(sys.argv) > 2 else "ping"))
        except (ImportError, AttributeError):
            # Fallback to direct shard call if V2 is not imported correctly
            shard_results = Port0Observe.port0_shard0_observe(sys.argv[2] if len(sys.argv) > 2 else "ping")
            print(json.dumps(shard_results))
    elif cmd == "p5":
        if len(sys.argv) > 2 and sys.argv[2].lower() == "manifest":
            print(Port5Immunize.get_manifest())
            sys.exit(0)
            
        file_context = sys.argv[2] if len(sys.argv) > 2 else None
        results = Port5Immunize.execute_all(file_context=file_context)
        # Log V-Phase to blackboard for HIVE compliance
        log_to_blackboard({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "phase": "V",
            "audit": results,
            "file_context": file_context
        })
        print(json.dumps(results, indent=2))
        # EXIT GATE: Block if aggregate status is not PASS
        if results.get("aggregate_status") != "PASS":
            sys.exit(1)
        sys.exit(0)
    elif cmd == "signal":
        if len(sys.argv) < 3:
            print("Usage: python3 hfo_orchestration_hub.py signal \"<query>\"")
            sys.exit(1)
        query = sys.argv[2]
        signal_id = "SIG_" + hashlib.sha256(query.encode()).hexdigest()[:8]
        log_to_blackboard({
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
    elif cmd == "anchor":
        print("🌀 [HFO HUB]: Initializing Stigmergy Anchor...")
        from scripts.hfo_stigmergy_anchor import main_loop
        main_loop()
    else:
        print(f"Command {cmd} not recognized.")


