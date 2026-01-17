#!/usr/bin/env python3
import os
import subprocess
import time
import psutil

# Medallion: Bronze | Mutation: 0% | HIVE: I
# Role: Resource-Aware Stryker Background Orchestrator
# Mission: Phoenix Project Thread Omega

def check_resources():
    cpu_load = psutil.cpu_percent(interval=1)
    # Memory check
    mem = psutil.virtual_memory()
    return cpu_load, mem.percent

def run_stryker():
    print("🚀 [HFO-STRYKER]: Initializing background mutation run...")
    
    # Path to config
    config_path = "stryker.small.config.json"
    
    # Command with 'nice' to lower priority
    # Using 'ionice' if possible for disk priority as well
    cmd = ["nice", "-n", "19", "npx", "stryker", "run", config_path]
    
    try:
        process = subprocess.Popen(cmd, stdout=open("stryker_background.log", "w"), stderr=subprocess.STDOUT)
        print(f"🛰️ [HFO-STRYKER]: Stryker PID {process.pid} running in background.")
        
        while process.poll() is None:
            cpu, mem = check_resources()
            if cpu > 85:
                print(f"⚠️ [HFO-STRYKER]: High CPU detected ({cpu}%). Background process is niced, but monitoring...")
            time.sleep(30)
            
        print(f"✅ [HFO-STRYKER]: Mutation run finished with exit code {process.returncode}")
    except Exception as e:
        print(f"❌ [HFO-STRYKER]: Error during execution: {e}")

if __name__ == "__main__":
    run_stryker()
