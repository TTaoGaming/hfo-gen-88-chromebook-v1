#!/usr/bin/env python3
import sys
import os
import json
import hashlib
import shutil
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: E
# P5 DEFEND: Freeze Tool (Hot Bronze -> Cold Bronze)

COLD_ROOT = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian"
HOT_ROOT = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian"

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def freeze_file(hot_path):
    if not hot_path.startswith(HOT_ROOT):
        print(f"❌ Error: {hot_path} is not in Hot Obsidian.")
        return False

    if "bronze" not in hot_path:
        print(f"❌ Error: Only Bronze files can be frozen to Cold Bronze via this tool.")
        return False

    # Calculate target path in Cold Bronze
    rel_path = os.path.relpath(hot_path, HOT_ROOT)
    cold_path = os.path.join(COLD_ROOT, rel_path)

    # Ensure directory exists
    os.makedirs(os.path.dirname(cold_path), exist_ok=True)

    # Generate Receipt
    file_hash = get_file_hash(hot_path)
    receipt = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": hot_path,
        "target": cold_path,
        "hash": file_hash,
        "medallion": "Bronze",
        "state": "Frozen"
    }

    # Write receipt
    receipt_path = f"{cold_path}.receipt.json"

    print(f"❄️ [P5 FREEZE]: Freezing {os.path.basename(hot_path)}...")
    shutil.copy2(hot_path, cold_path)
    with open(receipt_path, 'w') as f:
        json.dump(receipt, f, indent=4)

    print(f"✅ [P5 FREEZE]: Success. {cold_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: freeze_to_cold.py <hot_file_path>")
        sys.exit(1)

    for arg in sys.argv[1:]:
        freeze_file(os.path.abspath(arg))
