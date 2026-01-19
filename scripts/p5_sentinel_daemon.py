#!/usr/bin/env python3
# Medallion: Gold | Mutation: 95% | HIVE: V
# Port 5: DEFEND | P5 Sentinel Daemon (Watchdog)

import time
import subprocess
import os
import json
import datetime
import sys
import urllib.request
import urllib.error

# HFO: Add port path to sys.path for base imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../hfo_hot_obsidian/bronze/2_areas/architecture/ports"))
from versions.base import log_to_blackboard

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("❌ [SENTINEL]: 'watchdog' package missing. Please run 'pip install watchdog'.")
    sys.exit(1)

# Configuration
BLACKBOARD_PATH = "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
HUB_PATH = "hfo_hot_obsidian/bronze/2_areas/architecture/ports/hfo_orchestration_hub.py"
WATCH_EXTENSIONS = {".py", ".ts", ".js", ".html", ".yaml", ".md"}
IGNORE_SUBSTRINGS = {"blackboard", ".receipt.json", ".git", ".venv", "node_modules", "__pycache__"}
TRIPWIRE_INTERVAL_SECONDS = 300
DUCKDB_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_gen_88_cb_v2/hfo_unified_v88.duckdb"
GATEWAY_RECEIPTS_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/3_resources/receipts/hfo_mcp_gateway_receipts.jsonl"


def log_tripwire(status: str, tool: str, details: str):
    log_to_blackboard({
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
        "phase": "TOOL_TRIPWIRE",
        "status": status,
        "tool": tool,
        "details": details,
    })


def check_tavily():
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        log_tripwire("FAIL", "tavily", "TAVILY_API_KEY missing")
        return
    payload = {
        "api_key": api_key,
        "query": "healthcheck",
        "search_depth": "basic",
        "max_results": 1,
    }
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                log_tripwire("FAIL", "tavily", f"HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        log_tripwire("FAIL", "tavily", f"HTTPError {e.code}")
    except Exception as e:
        log_tripwire("FAIL", "tavily", f"Request failed: {e}")


def check_openrouter():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        log_tripwire("FAIL", "openrouter", "OPENROUTER_API_KEY missing")
        return
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                log_tripwire("FAIL", "openrouter", f"HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        log_tripwire("FAIL", "openrouter", f"HTTPError {e.code}")
    except Exception as e:
        log_tripwire("FAIL", "openrouter", f"Request failed: {e}")


def check_duckdb():
    if not os.path.exists(DUCKDB_PATH):
        log_tripwire("FAIL", "duckdb", "DuckDB file missing")
        return
    try:
        size = os.path.getsize(DUCKDB_PATH)
        if size <= 0:
            log_tripwire("FAIL", "duckdb", "DuckDB file size is 0")
    except Exception as e:
        log_tripwire("FAIL", "duckdb", f"DuckDB stat failed: {e}")


def check_gateway_receipts():
    if not os.path.exists(GATEWAY_RECEIPTS_PATH):
        log_tripwire("FAIL", "mcp_gateway", "Gateway receipts log missing")


def run_tripwires():
    check_tavily()
    check_openrouter()
    check_duckdb()
    check_gateway_receipts()

class P5SentinelHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_triggered = {}
        self.cooldown = 1.0  # seconds to prevent rapid double-triggers

    def on_modified(self, event):
        if event.is_directory:
            return
        
        path = event.src_path
        ext = os.path.splitext(path)[1]
        
        if ext in WATCH_EXTENSIONS and not any(sub in path for sub in IGNORE_SUBSTRINGS):
            now = time.time()
            if path in self.last_triggered and (now - self.last_triggered[path]) < self.cooldown:
                return
            
            self.last_triggered[path] = now
            print(f"🛡️ [SENTINEL]: Change detected: {path}")
            self.run_p5_audit(path)

    def run_p5_audit(self, file_path):
        try:
            # Hub P5 command executes all registered Port 5 tools with file context
            result = subprocess.run(
                ["python3", HUB_PATH, "p5", file_path],
                capture_output=True,
                text=True
            )
            
            # Use return code 0 as success, others as breach
            is_breach = result.returncode != 0
            status = "BREACH" if is_breach else "PASS"
            
            log_entry = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
                "phase": "WATCH_SENTINEL",
                "file": file_path,
                "status": status,
                "msg": "Real-time integrity audit triggered by filesystem event."
            }
            
            if is_breach:
                log_entry["details"] = result.stdout.strip()
                print(f"🚨 [SENTINEL]: BREACH DETECTED in {file_path}!")
                # Terminal visual scream
                print("-" * 40)
                print(result.stdout.strip())
                print("-" * 40)
            else:
                print(f"✅ [SENTINEL]: {file_path} integrity verified.")

            # HFO: Use signed log_to_blackboard instead of raw write
            log_to_blackboard(log_entry)
                
        except Exception as e:
            print(f"❌ [SENTINEL]: Internal error during audit: {e}")

if __name__ == "__main__":
    if not os.path.exists(HUB_PATH):
        print(f"❌ [SENTINEL]: Hub path not found at {HUB_PATH}")
        sys.exit(1)

    event_handler = P5SentinelHandler()
    observer = Observer()
    
    # Watch HFO domains
    observer.schedule(event_handler, path="hfo_hot_obsidian", recursive=True)
    observer.schedule(event_handler, path=".", recursive=False)
    
    print("🌀 [SENTINEL]: P5 Sentinel Daemon active. Mode: Real-time Defense.")
    print(f"📝 [SENTINEL]: Logging to {BLACKBOARD_PATH}")
    observer.start()
    
    try:
        last_tripwire = 0.0
        while True:
            now = time.time()
            if now - last_tripwire >= TRIPWIRE_INTERVAL_SECONDS:
                run_tripwires()
                last_tripwire = now
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 [SENTINEL]: Powering down...")
        observer.stop()
    observer.join()
