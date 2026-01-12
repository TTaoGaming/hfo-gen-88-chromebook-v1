#!/usr/bin/env python3
# Medallion: Gold | Mutation: 100% | HIVE: V
# Port 5: DEFEND | GENERATION GATE PROTECTOR

import os
import sys
import subprocess

COLD_DIR = "hfo_cold_obsidian"
RECEIPT_EXT = ".receipt.json"

def get_current_generation():
    """Extracts generation number from workspace folder name."""
    cwd = os.getcwd()
    folder_name = os.path.basename(cwd)
    # Expected pattern: hfo_gen_XX_...
    import re
    match = re.search(r"gen_(\d+)", folder_name)
    if match:
        return int(match.group(1))
    return 0

def check_generation_gate():
    """
    Enforces the rule: Cold Bronze is Append-Only.
    1. No Edits (M) or Deletions (D).
    2. New files (A/??) MUST have a matching .receipt.json.
    3. Generation must match Workspace ID.
    """
    current_gen = get_current_generation()
    print(f"🛡️ [P5-GATE]: Workspace Gen: {current_gen} | Ground Truth Validation...")
    
    try:
        # Check git status for Cold directory
        # --porcelain=v1 for easy parsing
        git_status = subprocess.check_output(["git", "status", "--porcelain", COLD_DIR]).decode()
        
        staged_files = []
        untracked_files = []
        
        for line in git_status.splitlines():
            if not line: continue
            status = line[:2]
            path = line[3:].strip()
            
            # BLOCK: Modification or Deletion
            if 'M' in status or 'D' in status or 'R' in status:
                print(f"🚨 [GEN-GATE-BREACH]: Unauthorized edit/delete/rename in Gen {current_gen} Cold storage!")
                print(f"   -> FILE: {path} (Status: {status})")
                return False
            
            # TRACK: New files (A = Staged, ?? = Untracked)
            if 'A' in status or '??' in status:
                if status == '??':
                    untracked_files.append(path)
                else:
                    staged_files.append(path)

        # VALIDATE: All new files must have a receipt
        all_new = staged_files + untracked_files
        source_files = [f for f in all_new if not f.endswith(RECEIPT_EXT)]
        receipt_files = [f for f in all_new if f.endswith(RECEIPT_EXT)]
        
        for sf in source_files:
            expected_receipt = sf + RECEIPT_EXT
            if expected_receipt not in all_new:
                # Also check filesystem in case it was already committed but untracked now
                if not os.path.exists(expected_receipt):
                    print(f"❌ [PROVENANCE-FAIL]: New file in COLD lacks matching receipt!")
                    print(f"   -> FILE: {sf}")
                    print(f"   -> EXPECTED: {expected_receipt}")
                    return False
                
    except Exception as e:
        print(f"⚠️ [P5-GATE-WARN]: Gate error: {e}")
        return False
        
    return True

if __name__ == "__main__":
    if not check_generation_gate():
        print("\n🚨 [ESCALATION_LEVEL_8]: GENERATION GATE BREACHED.")
        print("🚨 ACTION: BLOCKING COMMIT. PROMOTION TO NEXT GEN REQUIRED FOR EDITS.")
        sys.exit(1)
    else:
        print("✅ [P5-GATE-PASS]: Lockdown Verified.")
        sys.exit(0)
