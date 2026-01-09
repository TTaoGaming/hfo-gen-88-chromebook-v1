#!/usr/bin/env python3
import sys
import os
import shutil
import json
from datetime import datetime

# Medallion: Bronze | Mutation: 95% | HIVE: V
# P5 DEFEND: Automated Quarantine & Demotion Manager

GRUDGE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/bootstrapping_hfo/defenses/BOOK_OF_BLOOD_GRUDGES.jsonl"

def log_grudge(scream_id, filename, message):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "port": "P4",
        "scream": f"SCREAM_{scream_id}",
        "file": filename,
        "severity": "CRITICAL",
        "msg": message
    }
    with open(GRUDGE_PATH, 'a') as f:
        f.write(json.dumps(entry) + "\n")

def get_medallion_layer(path):
    if "hfo_hot_obsidian/silver" in path: return "silver"
    if "hfo_hot_obsidian/gold" in path: return "gold"
    if "hfo_hot_obsidian/hfo" in path: return "hfo"
    return "bronze"

def check_receipt(filepath):
    # Receipts are located in the 3_resources/receipts of the target layer
    # Format: filename.receipt.json
    parts = filepath.split('/')
    try:
        medallion_index = -1
        for i, part in enumerate(parts):
            if part in ["bronze", "silver", "gold", "hfo"]:
                medallion_index = i
                break

        if medallion_index == -1: return True # Not in medallion

        layer = parts[medallion_index]
        if layer == "bronze": return True # Bronze doesn't need receipt yet (it IS the input)

        filename = os.path.basename(filepath)
        receipt_name = f"{filename}.receipt.json"
        # Receipt must be in the target layer's 3_resources/receipts
        receipt_path = os.path.join("/".join(parts[:medallion_index+1]), "3_resources", "receipts", receipt_name)

        if not os.path.exists(receipt_path):
            return False, f"Missing Tamper-Evident Receipt: {receipt_path}"

        # Basic validation of receipt content
        with open(receipt_path, 'r') as r:
            data = json.load(r)
            if data.get("mutation_score", 0) < 88:
                return False, f"Receipt failed Goldilocks check: {data.get('mutation_score')}% < 88%"

        return True, "Valid"
    except Exception as e:
        return False, f"Receipt Error: {str(e)}"

def quarantine(filepath, reason):
    filename = os.path.basename(filepath)
    # Move to the archive of the current layer
    parts = filepath.split('/')
    for i, part in enumerate(parts):
        if part in ["bronze", "silver", "gold", "hfo"]:
            archive_dir = os.path.join("/".join(parts[:i+1]), "4_archive")
            os.makedirs(archive_dir, exist_ok=True)
            target = os.path.join(archive_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
            print(f"🚨 [P5 DEFEND]: QUARANTINE TRIGGERED. Demoting {filepath} to {target}")
            shutil.move(filepath, target)
            log_grudge(1, filename, f"Quarantined: {reason}") # Scream 1: Breach
            return

def main():
    files = sys.argv[1:]
    for f in files:
        if not os.path.isfile(f): continue

        # Check if moving to higher layer
        layer = get_medallion_layer(f)
        if layer in ["silver", "gold", "hfo"]:
            valid, reason = check_receipt(f)
            if not valid:
                quarantine(f, reason)
                sys.exit(1) # Block the commit

if __name__ == "__main__":
    main()
