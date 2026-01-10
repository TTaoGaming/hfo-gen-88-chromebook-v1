#!/usr/bin/env python3
import sys
import os
import json
import hashlib
import shutil
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: E
# P5 DEFEND: Promotion Tool (Cold Bronze -> Hot Silver)

COLD_ROOT = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian"
HOT_ROOT = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian"

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def promote_to_silver(cold_path, mutation_score):
    if not (88 <= mutation_score <= 98):
        print(f"❌ [P5 ERROR]: Mutation Score {mutation_score}% is outside the Goldilocks Zone (88-98%).")
        return False

    if not cold_path.startswith(COLD_ROOT):
        print(f"❌ Error: {cold_path} is not in Cold Obsidian.")
        return False

    # Calculate target path in Hot Silver
    # Expected: hfo_cold_obsidian/bronze/path/to/file -> hfo_hot_obsidian/silver/path/to/file
    rel_path = os.path.relpath(cold_path, os.path.join(COLD_ROOT, "bronze"))
    silver_path = os.path.join(HOT_ROOT, "silver", rel_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(silver_path), exist_ok=True)

    # Generate Mutation Receipt
    file_hash = get_file_hash(cold_path)
    receipt = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": cold_path,
        "target": silver_path,
        "hash": file_hash,
        "medallion": "Silver",
        "mutation_score": mutation_score,
        "validator": "Stryker-Sim"
    }

    # Write receipt
    receipt_dir = os.path.join(HOT_ROOT, "silver", "3_resources", "receipts")
    os.makedirs(receipt_dir, exist_ok=True)
    receipt_path = os.path.join(receipt_dir, f"{os.path.basename(silver_path)}.receipt.json")

    print(f"🥈 [P5 PROMOTE]: Promoting {os.path.basename(cold_path)} to Silver...")
    shutil.copy2(cold_path, silver_path)
    with open(receipt_path, 'w') as f:
        json.dump(receipt, f, indent=4)

    print(f"✅ [P5 PROMOTE]: Success. {silver_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: promote_to_silver.py <cold_file_path> <mutation_score>")
        sys.exit(1)

    promote_to_silver(os.path.abspath(sys.argv[1]), int(sys.argv[2]))
