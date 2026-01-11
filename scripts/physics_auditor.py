#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
import sys
import re
import os

def audit_physics(file_path):
    print(f"🕵️  Auditing Physics in {file_path}...")
    errors = []
    
    if not os.path.exists(file_path):
        return False, ["File not found"]

    with open(file_path, "r") as f:
        content = f.read()

    # 1. Check for Physics Engine Initialization
    if "Matter.Engine.create()" not in content and "Rapier.init()" not in content:
        errors.append("❌ Missing Physics Engine Initialization (Matter or Rapier)")

    # 2. Check for One Euro Filter (Required for canalization smoothing)
    if "class OneEuroFilter" not in content:
        errors.append("❌ Missing OneEuroFilter implementation")

    # 3. Check for 1eurofilter dependency (if external) or internal math
    if "Math.PI" not in content and "OneEuroFilter" in content:
        errors.append("❌ OneEuroFilter implementation seems broken/partial (Missing Math.PI)")

    # 4. Check for hfoState integration
    if "hfoState.physics" not in content:
        errors.append("❌ hfoState.physics configuration not found")

    # 5. Check for P0 Observe logic
    if "port0Observe" not in content:
         errors.append("❌ Missing Formalized P0 Observe (port0Observe)")

    # 6. Check for P1 Bridge logic
    if "port1Bridge" not in content:
         errors.append("❌ Missing Formalized P1 Bridge (port1Bridge)")

    # 7. Check for P2 Shape logic
    if "port2Shape" not in content:
         errors.append("❌ Missing Formalized P2 Shape (port2Shape)")

    # 8. Check for P3 Inject logic
    if "port3Inject" not in content:
        errors.append("❌ Missing Formalized P3 Inject (port3Inject)")

    if not errors:
        print("✅ Physics Integrity Verified.")
        return True, []
    else:
        for err in errors:
            print(err)
        return False, errors

if __name__ == "__main__":
    config_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/scripts/hfo_config.json"
    target = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v39.html"
    
    if os.path.exists(config_path):
        import json
        with open(config_path, "r") as f:
            cfg = json.load(f)
            target = f"/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v{cfg['activeVersion']}.html"

    success, errs = audit_physics(target)
    if not success:
        sys.exit(1)
    sys.exit(0)
