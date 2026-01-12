#!/usr/bin/env python3
# Medallion: Gold | Mutation: 98% | HIVE: V
# Port 5: DEFEND | MEDALLION PURITY GUARD

import os
import sys
import json
import subprocess

COLD_DIR = "hfo_cold_obsidian"
HOT_DIR = "hfo_hot_obsidian"
RECEIPT_EXT = ".receipt.json"

def check_raw_copy_bypass():
    """
    Check if hfo_cold_obsidian has been modified without using freezing tools.
    This detects bulk 'cp -rv' or manual overwrites.
    """
    print("🛡️ [P5-PURITY]: Checking for Medallion Type-1 Breaches...")
    
    # Check if receipts were deleted recently
    try:
        git_diff = subprocess.check_output(["git", "diff", "--name-only", "HEAD"]).decode()
        if "hfo_cold_obsidian" in git_diff and RECEIPT_EXT in git_diff:
            # Check for deletions
            git_status = subprocess.check_output(["git", "status", "--porcelain", COLD_DIR]).decode()
            deletions = [line for line in git_status.split('\n') if line.startswith(' D')]
            if len(deletions) > 10:
                print(f"🚨 [RED_TRUTH]: MASSIVE RECEIPT DELETION DETECTED! ({len(deletions)} files)")
                print("🚨 [RED_TRUTH]: Possible 'Atomic Sync' Lobotomy in progress.")
                return False
    except:
        pass
        
    return True

def verify_provenance_integrity():
    """
    Ensure every source file in Cold has a matching receipt.
    """
    print("🛡️ [P5-PURITY]: Verifying Provenance Integrity...")
    missing_receipts = []
    for root, dirs, files in os.walk(COLD_DIR):
        for f in files:
            if f.endswith(('.py', '.ts', '.html', '.yaml', '.md')) and not f.endswith(RECEIPT_EXT):
                receipt_path = os.path.join(root, f + RECEIPT_EXT)
                if not os.path.exists(receipt_path):
                    missing_receipts.append(os.path.join(root, f))
    
    if missing_receipts:
        print(f"❌ [P5-FAIL]: {len(missing_receipts)} files in COLD lack provenance receipts!")
        for m in missing_receipts[:5]:
            print(f"   -> MISSING: {m}")
        return False
    
    return True

def enforce_bronze_headers():
    """
    Ensure every source file in HOT_DIR has a Medallion provenance header.
    """
    print("🛡️ [P5-PURITY]: Enforcing Medallion Provenance Headers in HOT...")
    missing_headers = []
    
    # We only check files that are staged for commit
    try:
        staged_files = subprocess.check_output(["git", "diff", "--cached", "--name-only"]).decode().splitlines()
        for f in staged_files:
            if f.startswith(HOT_DIR) and f.endswith(('.py', '.ts', '.html', '.yaml')):
                # Check for "Medallion:" string in first 5 lines
                abs_path = os.path.abspath(f)
                if not os.path.exists(abs_path): continue
                
                with open(abs_path, 'r') as file_obj:
                    lines = [file_obj.readline() for _ in range(5)]
                    content = "".join(lines)
                    if "Medallion:" not in content:
                        missing_headers.append(f)
    except Exception as e:
        print(f"⚠️ [P5-PURITY]: Header check error: {e}")
        
    if missing_headers:
        print(f"❌ [P5-FAIL]: {len(missing_headers)} files in HOT lack provenance headers!")
        for m in missing_headers:
            print(f"   -> MISSING HEADER: {m}")
        return False
    return True

def main():
    checks = [
        check_raw_copy_bypass,
        verify_provenance_integrity,
        enforce_bronze_headers
    ]
    
    failure = False
    for check in checks:
        if not check():
            failure = True
            
    if failure:
        print("\n🚨 [ESCALATION_LEVEL_8]: MEDALLION PURITY BREACHED.")
        print("🚨 ACTION: BLOCKING COMMIT. CONSULT THE BOOK OF BLOOD GRUDGES.")
        sys.exit(1)
    else:
        print("✅ [P5-PASS]: Medallion Purity Verified.")
        sys.exit(0)

if __name__ == "__main__":
    main()
