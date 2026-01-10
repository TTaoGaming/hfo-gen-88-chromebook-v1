#!/usr/bin/env python3
import sys
import os
import shutil
import json
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: V
# P5 DEFEND: Automated Quarantine & Demotion Manager

GRUDGE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/p5_defend/BOOK_OF_BLOOD_GRUDGES.jsonl"

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
    # Rules:
    # 1. Any file in hfo_cold_obsidian must have [file].receipt.json in the SAME directory.
    # 2. Any file in hfo_hot_obsidian/silver must have [file].receipt.json in silver/3_resources/receipts.

    filename = os.path.basename(filepath)

    if "hfo_cold_obsidian" in filepath:
        receipt_path = f"{filepath}.receipt.json"
        if not os.path.exists(receipt_path):
            return False, f"Cold File lacks freeze receipt: {receipt_path}"
        return True, "Valid"

    if "hfo_hot_obsidian/silver" in filepath:
        # Avoid checking receipts against themselves
        if "3_resources/receipts" in filepath: return True, "Valid"

        parts = filepath.split('/')
        silver_root = ""
        for i, part in enumerate(parts):
            if part == "silver":
                silver_root = "/".join(parts[:i+1])
                break

        receipt_path = os.path.join(silver_root, "3_resources", "receipts", f"{filename}.receipt.json")
        if not os.path.exists(receipt_path):
            return False, f"Silver File lacks mutation receipt: {receipt_path}"

        with open(receipt_path, 'r') as r:
            data = json.load(r)
            score = data.get("mutation_score", 0)
            if not (88 <= score <= 98):
                return False, f"Silver Receipt failed Goldilocks check: {score}%"

        return True, "Valid"

    return True, "Valid"

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
