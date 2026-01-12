#!/usr/bin/env python3
# Medallion: Gold | Mutation: 95% | HIVE: V
# Port 5: DEFEND | Blackboard Purity & Immutability Sentinel

import os
import json
import hashlib
import sys
from datetime import datetime

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
QUARANTINE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/blackboard_quarantine.jsonl"
MANIFEST_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/blackboard_manifest.json"
SECRET_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/.hfo_secret"

def get_secret():
    if os.path.exists(SECRET_PATH):
        with open(SECRET_PATH, "r") as f:
            return f.read().strip()
    return "HFO_DEFAULT_SECRET"

def verify_and_quarantine():
    if not os.path.exists(BLACKBOARD_PATH):
        return True

    secret = get_secret()
    valid_lines = []
    quarantined_count = 0
    immutability_breach = False
    
    with open(BLACKBOARD_PATH, 'r') as f:
        lines = f.readlines()

    last_sig = "ROOT"
    last_timestamp = None
    seal_found = False

    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        
        try:
            entry = json.loads(line)
            
            # --- SEAL RECOGNITION ---
            # A SEAL signal resets the validation chain to allow proceeding after documented breaches.
            if entry.get("phase") == "SIGNAL" and entry.get("query") == "RED_TRUTH_SEAL":
                print(f"⚓ [PURITY]: RED_TRUTH_SEAL found at line {i+1}. Restarting chain validation.")
                last_sig = entry.get("signature")
                last_timestamp = None # Reset chronology check for new epoch? Optional.
                seal_found = True
                immutability_breach = False # Reset breach for this run if we found a seal
                continue

            # Skip validation if we haven't found a seal and there was a prior breach? 
            # No, we validate everything, but the SEAL acts as the new anchor.
            
            # Check for Immutability Breach (Signatures/Chain)
            sig = entry.get("signature")
            if not sig:
                print(f"❌ [PURITY]: Unsigned entry at line {i+1}")
                # We don't quarantine yet, just mark as breach
                immutability_breach = True
            else:
                # Verify HMAC Chain
                temp_entry = entry.copy()
                temp_entry.pop("signature")
                entry_str = json.dumps(temp_entry, sort_keys=True)
                # Try both possible 'prev' signals if this is the first line
                prev = last_sig if last_sig != "ROOT" else "LEGACY"
                expected = hashlib.sha256(f"{secret}:{prev}:{entry_str}".encode()).hexdigest()
                
                # Check against LEGACY as well for root entry
                if sig != expected and last_sig == "ROOT":
                    expected_legacy = hashlib.sha256(f"{secret}:LEGACY:{entry_str}".encode()).hexdigest()
                    if sig == expected_legacy:
                        expected = expected_legacy

                if sig != expected:
                    print(f"❌ [PURITY]: Chain fracture at line {i+1}. TAMPER DETECTION.")
                    immutability_breach = True
                
                last_sig = sig

            # Check Chronology
            ts_str = entry.get("timestamp")
            if ts_str:
                try:
                    # Handle Z suffix
                    clean_ts = ts_str.replace('Z', '')
                    current_ts = datetime.fromisoformat(clean_ts)
                    if last_timestamp and current_ts < last_timestamp:
                        print(f"❌ [PURITY]: Chronological breach at line {i+1} ({ts_str} < {last_timestamp.isoformat()})")
                        immutability_breach = True
                    last_timestamp = current_ts
                except ValueError:
                    pass

            valid_lines.append(line)

        except json.JSONDecodeError:
            print(f"⚠️ [PURITY]: Malformed JSON at line {i+1}. Quarantining...")
            with open(QUARANTINE_PATH, 'a') as qf:
                qentry = {
                    "quarantine_ts": datetime.utcnow().isoformat() + "Z",
                    "original_line_index": i + 1,
                    "raw_content": line
                }
                qf.write(json.dumps(qentry) + "\n")
            quarantined_count += 1
            continue

    # Rewrite blackboard if entries were quarantined
    if quarantined_count > 0:
        with open(BLACKBOARD_PATH, 'w') as f:
            for vline in valid_lines:
                f.write(vline + "\n")
        print(f"✅ [PURITY]: {quarantined_count} malformed entries moved to quarantine.")

    # Generate Master Hash for Git Ops
    with open(BLACKBOARD_PATH, 'rb') as f:
        master_hash = hashlib.sha256(f.read()).hexdigest()
    
    manifest = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "blackboard_sha256": master_hash,
        "line_count": len(valid_lines),
        "quarantined_last_run": quarantined_count,
        "status": "PASS" if not immutability_breach else "BREACH"
    }
    
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=4)
    
    # Block Git commit if there's an immutability breach
    if immutability_breach:
        print("🚨 [PURITY]: Immutability breach detected. Blackboard has been edited or tampered with.")
        print("💡 [PURITY]: To resume the chain, you must log a 'SIGNAL: RED_TRUTH_ANCHOR' via the Hub.")
        return False
        
    return True

if __name__ == "__main__":
    if not verify_and_quarantine():
        sys.exit(1)
    print("✅ [PURITY]: Blackboard Integrity Verified. Manifest updated.")
    sys.exit(0)
