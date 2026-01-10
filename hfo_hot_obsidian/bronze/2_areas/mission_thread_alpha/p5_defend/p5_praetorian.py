#!/usr/bin/env python3
import sys
import subprocess
import os

# Medallion: Bronze | Mutation: 0% | HIVE: V
# P5 PYRE PRAETORIAN: The Immunizer
# Consolidates all defense and governance sentinels under Port 5.

def run_sentinel(name, path, args=None):
    print(f"🛡️ [P5 PRAETORIAN]: Running {name}...")
    cmd = [sys.executable, path]
    if args:
        cmd.extend(args)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"🚨 [P5 PRAETORIAN]: {name} FAILED!")
        print(result.stdout)
        print(result.stderr)
        return False

    print(f"✅ [P5 PRAETORIAN]: {name} Passed.")
    return True

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))

    # 1. Temporal/Behavioral Sentinel
    if not run_sentinel("Temporal Sentinel", os.path.join(base_path, "temporal_sentinel.py")):
        sys.exit(1)

    # 2. Hive 8 Workflow Sentinel (Dual Search & 8-Step Thinking)
    if not run_sentinel("Hive 8 Sentinel", os.path.join(base_path, "hive8_workflow_sentinel.py")):
        sys.exit(1)

    # 3. Integrity Sentinel (Refinement Flow)
    # We run it across hot_obsidian/silver and cold_obsidian
    files_to_check = []
    for root, dirs, files in os.walk("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian"):
        for f in files:
            if not f.endswith(".receipt.json"):
                files_to_check.append(os.path.join(root, f))

    for root, dirs, files in os.walk("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/silver"):
        for f in files:
            if not f.endswith(".receipt.json") and "3_resources/receipts" not in root:
                files_to_check.append(os.path.join(root, f))

    if files_to_check:
        if not run_sentinel("Integrity Sentinel", os.path.join(base_path, "integrity_sentinel.py"), files_to_check):
            sys.exit(1)

    print("🛡️ [P5 PRAETORIAN]: Immunizer Sequence Complete. System Integrity Verified.")

if __name__ == "__main__":
    main()
