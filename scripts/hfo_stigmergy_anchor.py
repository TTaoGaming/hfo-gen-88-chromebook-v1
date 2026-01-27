#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: E
"""
⚓ HFO STIGMERGY ANCHOR
Pattern: Automated Safety Guard / State Archiver
Mission: Scheduled Backup and Architectural Cleanup
"""

import time
import shutil
import os
import sys
import datetime
import json
import subprocess
from subprocess import TimeoutExpired
from pathlib import Path

try:
    from hfo_env import load_repo_env

    load_repo_env()
except Exception:
    # Fail-open: anchor should still perform backups even if env parsing breaks.
    pass

# Paths
ROOT_DIR = str(Path(__file__).resolve().parents[1])
HOT_DIR = os.path.join(ROOT_DIR, "hfo_hot_obsidian")
BACKUP_DIR = os.path.join(ROOT_DIR, "hfo_hot_obsidian/4_archive/stigmergy_anchors")
BLACKBOARD_PATH = os.path.join(HOT_DIR, "hot_obsidian_blackboard.jsonl")
CONFIG_PATH = os.path.join(ROOT_DIR, "scripts/hfo_config.json")
P5_HUB_PATH = os.path.join(
    HOT_DIR,
    "bronze/4_archive/areas_archive_2026_01_18/architecture/ports/hfo_orchestration_hub.py",
)
P5_AUDIT_CONTEXT = os.path.join(HOT_DIR, "bronze/__anchor_fast_gate__.txt")

def perform_backup():
    """Performs a timestamped backup of critical files."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    anchor_path = os.path.join(BACKUP_DIR, f"anchor_{timestamp}")
    os.makedirs(anchor_path, exist_ok=True)

    print(f"⚓ [ANCHOR]: Initiating Backup Anchor [{timestamp}]...")

    # 1. Backup Blackboard
    if os.path.exists(BLACKBOARD_PATH):
        shutil.copy2(BLACKBOARD_PATH, os.path.join(anchor_path, "hot_obsidian_blackboard.jsonl"))

    # 2. Backup AGENTS.md
    agents_path = os.path.join(ROOT_DIR, "AGENTS.md")
    if os.path.exists(agents_path):
        shutil.copy2(agents_path, os.path.join(anchor_path, "AGENTS.md"))

    # 3. Backup Active Workspace HTML
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                cfg = json.load(f)
                active_version = cfg.get("activeVersion", "unknown")
                # Look for the file in Gen 4 directory
                gen4_dir = os.path.join(HOT_DIR, "bronze/2_areas/mission_thread_omega_gen_4")
                active_file = os.path.join(gen4_dir, f"omega_gen4_v{active_version}.html")
                if os.path.exists(active_file):
                    shutil.copy2(active_file, os.path.join(anchor_path, os.path.basename(active_file)))
    except Exception as e:
        print(f"⚠️ [ANCHOR]: HTML backup failed: {e}")

    print(f"✅ [ANCHOR]: Backup complete: {anchor_path}")

def architectural_cleanup():
    """Placeholder for architectural cleanup tasks."""
    print("🧹 [ANCHOR]: Initiating Architectural Cleanup...")

    # 1. Run P5 Audit and log summary
    try:
        result = subprocess.run(
            [sys.executable, P5_HUB_PATH, "p5", P5_AUDIT_CONTEXT],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            print("✅ [ANCHOR]: P5 Audit PASS.")
        else:
            print("⚠️ [ANCHOR]: P5 Audit FAIL. Drift detected.")
    except TimeoutExpired:
        print("⚠️ [ANCHOR]: P5 Audit TIMEOUT. Treating as drift.")
    except Exception as e:
        print(f"❌ [ANCHOR]: Cleanup failed: {e}")

def main_loop(interval_minutes=10):
    """Main loop for the Stigmergy Anchor."""
    print(f"⚓ [ANCHOR]: Stigmergy Anchor Active. Interval: {interval_minutes}m")
    os.makedirs(BACKUP_DIR, exist_ok=True)

    while True:
        try:
            perform_backup()
            architectural_cleanup()
        except Exception as e:
            print(f"🚨 [ANCHOR]: Error in main loop: {e}")

        print(f"💤 [ANCHOR]: Sleeping for {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    interval = 10
    if len(sys.argv) > 1:
        try:
            interval = int(sys.argv[1])
        except: pass
    main_loop(interval)
