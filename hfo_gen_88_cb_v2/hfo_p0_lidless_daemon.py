# Medallion: Bronze | Mutation: 0% | HIVE: V
import os
import psutil
import time
import json
from pathlib import Path

# --- THRIFT CONFIG (P0) ---
THRIFT_RAM_CEILING = 50 * 1024 * 1024  # 50MB
HEARTBEAT_INTERVAL = 60  # 1 minute tick
REPORT_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/MISSION_CONTROL/HIVE_VITALITY.json"

def get_hive_vitality():
    """Gathers hardware and process telemetry."""
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    load = os.getloadavg()
    
    # Identify Active Commanders
    daemons = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = " ".join(proc.info['cmdline'] or [])
            if "hfo_p" in cmd and ".py" in cmd:
                daemons.append({
                    "pid": proc.info['pid'],
                    "cmd": cmd.split("/")[-1],
                    "mem_mb": proc.memory_info().rss / (1024 * 1024)
                })
        except:
            continue

    return {
        "timestamp": time.ctime(),
        "hardware": {
            "ram_used_gb": round(mem.used / (1024**3), 2),
            "ram_avail_gb": round(mem.available / (1024**3), 2),
            "cpu_load_1m": load[0],
            "disk_free_gb": round(disk.free / (1024**3), 2)
        },
        "active_commanders": daemons,
        "status": "GREEN" if mem.available > (500 * 1024 * 1024) else "AMBER"
    }

def run_p0_singleton():
    print("🦅 P0 Lidless Singleton Activated (Thrift Mode)")
    while True:
        try:
            vitality = get_hive_vitality()
            with open(REPORT_PATH, "w") as f:
                json.dump(vitality, f, indent=4)
            
            # Pulse to terminal or log if needed
            print(f"📡 [P0] Heartbeat: RAM {vitality['hardware']['ram_avail_gb']}GB Avail | Cmdrs: {len(vitality['active_commanders'])}")
            
            time.sleep(HEARTBEAT_INTERVAL)
        except Exception as e:
            print(f"⚠️ P0 Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_p0_singleton()
