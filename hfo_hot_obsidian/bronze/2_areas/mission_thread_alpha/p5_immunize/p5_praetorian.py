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
    failures = []

    def run_check(name, script, args=None):
        if not run_sentinel(name, os.path.join(base_path, script), args):
            failures.append(name)
            return False
        return True

    # 1. P5-CHRONOS (Temporal)
    run_check("P5-CHRONOS", "temporal_sentinel.py")

    # 2. PORT-0-OBSERVE (Workflow)
    run_check("PORT-0-OBSERVE", "hive8_workflow_sentinel.py")

    # 3. P1-MONOLITH (Architectural)
    run_check("P1-MONOLITH", "monolith_bypass_sentinel.py")

    # 4. P5-MEDALLION (Integrity)
    # Check core project files
    hot_bronze = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze"
    files_to_check = []
    for root, dirs, files in os.walk(hot_bronze):
        for f in files:
            if f.endswith(('.py', '.ts', '.html')):
                # Filter out the chaos files themselves
                if "chaos_injector" in f: continue
                files_to_check.append(os.path.join(root, f))

    run_check("P5-MEDALLION", "integrity_sentinel.py", files_to_check)

    # 5. P6-GHOST (Stigmergy)
    run_check("P6-GHOST", "ghost_walk_sentinel.py")

    # 6. P1-ZOD (Contract)
    run_check("P1-ZOD", "zod_gate_sentinel.py")

    # 7. P7-VENGEANCE (Forensic)
    run_check("P7-VENGEANCE", "blood_grudge_sentinel.py")

    # 8. P5-PRECOMMIT (Gatekeeper)
    run_check("P5-PRECOMMIT", "pre_commit_shield.py")

    if failures:
        print(f"\n🚨 [P5 PRAETORIAN]: IMMUNIZER BREACHED! Fails: {', '.join(failures)}")
        sys.exit(1)

    print("🛡️ [P5 PRAETORIAN]: 8 SHIELDS ACTIVE. System Integrity Fully Immunized.")

if __name__ == "__main__":
    main()
