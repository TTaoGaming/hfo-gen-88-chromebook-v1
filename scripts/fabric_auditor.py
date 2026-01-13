# Medallion: Bronze | Mutation: 0% | HIVE: I

#!/usr/bin/env python3
"""
HFO FABRIC AUDITOR v1.0
Industry Standard Data Lineage Verification for Omega Gen 4.

This tool scans HTML/JS files to ensure 'Medallion Purity':
- Port 1 (Fusion) is the only place raw sensor data is processed.
- All Visualization and Dispatch (Ports 2-7) must consume the Shared Data Fabric.
"""

import sys
import re
import os

def audit_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return False

    with open(file_path, 'r') as f:
        content = f.read()

    print(f"\n🔍 AUDITING DATA FABRIC LINEAGE: {os.path.basename(file_path)}")
    print("-" * 60)

    # Patterns indicating Bypass (Whack-a-Mole targets)
    bypass_patterns = [
        {
            "id": "RAW_LANDMARK_BYPASS",
            "regex": r"(?<!P1Bridger\.)results\.landmarks",
            "msg": "Found raw landmark access outside of P1Bridger. Use systemState.dataFabric instead.",
            "severity": "CRITICAL"
        },
        {
            "id": "LOCAL_COORDINATE_MATH",
            "regex": r"\* (?:width|height)(?!.*P1Bridger)(?!.*this\.app\.renderer)",
            "msg": "Scale-to-screen math detected outside of Port 1 Bridge. Port 1 should handle all coordinate fusion.",
            "severity": "WARNING"
        },
        {
            "id": "UNPROTECTED_SENSE_LOOP",
            "regex": r"results\.landmarks\.forEach\(",
            "msg": "Direct loop over raw results. Sensor data must be mapped through Port 1 first.",
            "severity": "CRITICAL"
        }
    ]

    violations = 0
    lines = content.split('\n')
    
    # 📜 Purity Scan
    for pattern in bypass_patterns:
        matches = list(re.finditer(pattern["regex"], content))
        if matches:
            for match in matches:
                # Find line number
                line_no = content.count('\n', 0, match.start()) + 1
                snippet = lines[line_no-1].strip()
                
                # Check for P1Bridger scope (simple class/method detection)
                # If we are inside P1Bridger block, landmarks access is allowed.
                # This is a heuristic: check if P1Bridger appeared recently in the file
                # or if the current method contains P1-related keywords.
                
                # Exclusion for legitimate skeletal overlay in drawResults
                if "drawResults" in snippet and "rawResults" in snippet and pattern["id"] != "UNPROTECTED_SENSE_LOOP":
                    continue
                if "utils.draw" in snippet: # MP drawings often need raw data
                    continue
                
                # Check for P1Bridger scope (wider range for monoliths)
                context_range = lines[max(0, line_no-150):line_no]
                is_in_p1 = any("class P1Bridger" in l or "static fuse" in l for l in context_range)
                if is_in_p1:
                    continue
                
                # Legalizing P2/P3/P7 domain scaling (e.g. PixiJS or specific viewport)
                domain_scaling = any("this.app.renderer" in l or "canvas.width" in l for l in context_range)
                if domain_scaling and pattern["id"] == "LOCAL_COORDINATE_MATH":
                    continue

                violations += 1
                color = "\033[91m" if pattern["severity"] == "CRITICAL" else "\033[93m"
                reset = "\033[0m"
                print(f"{color}[{pattern['severity']}]{reset} {pattern['id']} at Line {line_no}")
                print(f"   Context: {snippet}")
                print(f"   Guide:   {pattern['msg']}\n")

    print("-" * 60)
    if violations == 0:
        print("✅ LINEAGE AUDIT PASS: All consumers are consuming the Fabric.")
        return True
    else:
        print(f"❌ LINEAGE AUDIT FAIL: Found {violations} bypass(es).")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fabric_auditor.py <file_path>")
        sys.exit(1)
    
    success = audit_file(sys.argv[1])
    sys.exit(0 if success else 1)
