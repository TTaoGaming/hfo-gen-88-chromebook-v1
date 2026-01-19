# Medallion: Bronze | Mutation: 0% | HIVE: I
"""
🕷️ HFO SPIDER SOVEREIGN DAEMON
Pattern: 24/7 Orchestration Engine
Role: Lord of Webs (Port 7)

This daemon incarnates the HFO commanders on a regular interval,
facilitating autonomous mission progress and state synchronization.
"""

import sys
import os
import time
import argparse

# Add the actors directory to path
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/akka_actors")
try:
    from spider_sovereign import SpiderSovereign
except ImportError as e:
    print(f"❌ Failed to import SpiderSovereign: {e}")
    sys.exit(1)

def run_daemon(interval: int):
    print(f"🕸️ HFO Spider Sovereign Daemon Starting...")
    print(f"📡 Frequency: Every {interval} seconds.")
    
    sovereign = SpiderSovereign()
    
    # 24/7 Loop
    try:
        while True:
            sovereign.cycle()
            print(f"💤 Sleeping for {interval}s...")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Daemon shutting down. Hibernating Lord of Webs.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HFO Spider Sovereign 24/7 Daemon")
    parser.add_argument("--interval", type=int, default=60, help="Cycle interval in seconds (default: 60)")
    args = parser.parse_args()
    
    run_daemon(args.interval)
