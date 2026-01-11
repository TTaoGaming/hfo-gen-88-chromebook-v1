#!/usr/bin/env python3
import subprocess
import os
import sys
import json
from datetime import datetime

def run_step(name, command, shell=False):
    print(f"--- [STEP] {name} ---")
    try:
        result = subprocess.run(command, shell=shell, text=True, capture_output=True)
        if result.returncode == 0:
            print(f"✅ {name} Passed")
            return True, result.stdout
        else:
            print(f"❌ {name} Failed")
            print(result.stderr)
            return False, result.stderr
    except Exception as e:
        print(f"💥 {name} Errored: {e}")
        return False, str(e)

def generate_report(results):
    report_path = f"reports/forensic_v33_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    os.makedirs("reports", exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write("# 🛡️ HFO P5 Forensic Analysis Report\n\n")
        f.write(f"**Date**: {datetime.now().isoformat()}\n")
        f.write(f"**Target**: Mission Thread Omega (V33)\n\n")
        
        for name, success, output in results:
            status = "✅ PASS" if success else "❌ FAIL"
            f.write(f"## {name}: {status}\n")
            f.write("```\n")
            f.write(output[-2000:]) # Last 2000 chars
            f.write("\n```\n\n")
            
    print(f"\n📊 Report generated: {report_path}")
    return report_path

if __name__ == "__main__":
    # Load Abstraction Layer
    config_path = "scripts/hfo_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    
    version = config["activeVersion"]
    target_file = f"hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v{version}.html"
    
    steps = [
        ("P5 Syntax Gate", ["python3", "scripts/p5_syntax_gate.py", target_file]),
        ("Active E2E Test", ["npx", "playwright", "test", "scripts/omega_active_e2e.spec.ts"]),
        ("Active Sticky Drag Test", ["npx", "playwright", "test", f"scripts/omega_v{version}_sticky_drag.spec.ts"])
    ]
    
    final_results = []
    overall_success = True
    
    for name, cmd in steps:
        success, output = run_step(name, cmd)
        final_results.append((name, success, output))
        if not success:
            overall_success = False
            
    report_file = generate_report(final_results)
    
    if not overall_success:
        print(f"\n🛑 TROUBLESHOOTING DETECTED ERRORS. SEE {report_file}")
        sys.exit(1)
    else:
        print("\n🚀 ALL SYSTEMS NOMINAL.")
