#!/usr/bin/env python3
import os
import sys
import json
import psutil
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: H
# PORT-0-OBSERVE: Hardware Sensor (CPU/RAM/Backoffs)
# Enforces resource-aware mission engineering on Chromebook V-1 hardware.

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

def sense_hardware():
    cpu_count = psutil.cpu_count(logical=True)
    # Get 1-minute load average
    try:
        cpu_load = os.getloadavg()[0]
    except AttributeError:
        # Fallback if os.getloadavg() is not available (Windows/etc)
        cpu_load = psutil.cpu_percent(interval=1) / 100 * cpu_count
    
    mem = psutil.virtual_memory()
    
    # Heuristic for backoff:
    # If load per core > 0.8 OR available memory < 512MB
    load_per_core = cpu_load / cpu_count if cpu_count > 0 else 0
    backoff_required = load_per_core > 0.8 or mem.available < (512 * 1024 * 1024)
    
    # Check for GPU (Intel Integrated usually)
    gpu_available = os.path.exists("/dev/dri/renderD128")
    gpu_info = "Intel/Integrated (renderD128 detected)" if gpu_available else "None detected"
    
    return {
        "cpu": {
            "count": cpu_count,
            "load_1m": cpu_load,
            "load_per_core": load_per_core,
            "percent": psutil.cpu_percent(interval=0.1)
        },
        "memory": {
            "total": mem.total,
            "available": mem.available,
            "percent": mem.percent
        },
        "backoff": {
            "required": backoff_required,
            "suggested_concurrency": 1 if backoff_required else max(1, cpu_count // 2),
            "reason": "High Load" if load_per_core > 0.8 else "Low Memory" if mem.available < (512 * 1024 * 1024) else "Optimal"
        },
        "gpu": gpu_info
    }

def log_to_blackboard(hardware_data):
    receipt_id = f"HARDWARE_SENSE_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "phase": "H",
        "summary": "P0-Sense Hardware Audit: Resource limits detected.",
        "p0": {
            "status": "sensing",
            "hardware": hardware_data,
            "receipt": receipt_id
        },
        "p7": {"status": "routing"}
    }

    with open(BLACKBOARD_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return receipt_id

def main():
    print("🔍 [PORT-0-OBSERVE]: Sensing Host Hardware...")
    try:
        data = sense_hardware()
        receipt = log_to_blackboard(data)
        
        # Output for terminal consumption
        print(json.dumps(data, indent=2))
        print(f"✅ [PORT-0-OBSERVE]: Hardware Sense Complete. Receipt: {receipt}")
        
        if data["backoff"]["required"]:
            print(f"⚠️ [P0 WARNING]: BACKOFF REQUIRED. Suggested Concurrency: {data['backoff']['suggested_concurrency']}")
        else:
            print(f"🟢 [P0 INFO]: Resources Optimal. Suggested Concurrency: {data['backoff']['suggested_concurrency']}")
            
    except Exception as e:
        print(f"❌ [P0 ERROR]: Hardware sensing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
