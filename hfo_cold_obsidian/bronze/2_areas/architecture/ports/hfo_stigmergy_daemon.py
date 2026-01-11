#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
"""
🐝 HFO STIGMERGY DAEMON
Pattern: Auto-Scheduler / Blackboard Monitor
Mission: Fire-and-Forget Research Tasks
"""

import time
import json
import os
import sys
import datetime

# Add current port directory to path for relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from versions.base import BLACKBOARD_PATH, log_to_blackboard, load_env
from versions.hub_v5 import HubV5

def watch_blackboard():
    """Watches for 'SIGNAL' with status 'QUEUED'."""
    print("🐝 [HFO DAEMON]: Stigmergy Daemon Active. Watching blackboard...")
    load_env()

    processed_signals = set()
    
    # Pre-scan to find everything already processed
    if os.path.exists(BLACKBOARD_PATH):
        with open(BLACKBOARD_PATH, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    sid = entry.get("signal_id")
                    if sid and (entry.get("phase") in ["SIGNAL_COMPLETE", "SIGNAL_STATUS"]):
                        processed_signals.add(sid)
                except: continue

    last_line_offset = 0

    while True:
        if os.path.exists(BLACKBOARD_PATH):
            current_size = os.path.getsize(BLACKBOARD_PATH)
            if current_size > last_line_offset:
                with open(BLACKBOARD_PATH, "r") as f:
                    f.seek(last_line_offset)
                    lines = f.readlines()
                    last_line_offset = f.tell()

                    for line in lines:
                        if not line.strip(): continue
                        try:
                            entry = json.loads(line)
                            if entry.get("phase") == "SIGNAL" and entry.get("status") == "QUEUED":
                                signal_id = entry.get("signal_id")
                                if signal_id in processed_signals:
                                    continue
                                
                                query = entry.get("query")
                                print(f"🚀 [HFO DAEMON]: Detected Signal [{signal_id}]: {query}")
                                processed_signals.add(signal_id)
                                
                                # Update blackboard: IN_PROGRESS
                                log_to_blackboard({
                                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                                    "phase": "SIGNAL_STATUS",
                                    "signal_id": signal_id,
                                    "status": "PROCESSING"
                                })

                                # Run the Hub (This creates the Baton via HubV5)
                                try:
                                    baton = HubV5.run(query)
                                    
                                    # Final log: SIGNAL_COMPLETE
                                    log_to_blackboard({
                                        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                                        "phase": "SIGNAL_COMPLETE",
                                        "signal_id": signal_id,
                                        "query": query,
                                        "baton": baton
                                    })
                                    print(f"✅ [HFO DAEMON]: Signal [{signal_id}] Completed. Baton Created.")
                                except Exception as hub_err:
                                    print(f"❌ [HFO DAEMON]: Hub Execution Failed for [{signal_id}]: {hub_err}")
                                    log_to_blackboard({
                                        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                                        "phase": "SIGNAL_STATUS",
                                        "signal_id": signal_id,
                                        "status": "FAILED",
                                        "error": str(hub_err)
                                    })
                                    
                        except json.JSONDecodeError:
                            pass # Skip partial writes
                        except Exception as e:
                            print(f"⚠️ [HFO DAEMON]: Error processing line: {e}")
        
        else:
            # Table doesn't exist yet, wait
            pass
            
        time.sleep(2) # 2-second pulse to avoid CPU spinning

if __name__ == "__main__":
    try:
        watch_blackboard()
    except KeyboardInterrupt:
        print("\n🛑 [HFO DAEMON]: Shutting down.")
