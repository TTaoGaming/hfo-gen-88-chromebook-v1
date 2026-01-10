#!/usr/bin/env python3
import sys
import os
import json
import hashlib
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: I
# P1 FUSE: Receipt Generation Utility

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def generate_receipt(filepath, layer, phase):
    file_hash = get_file_hash(filepath)
    receipt = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "file": os.path.basename(filepath),
        "hash": file_hash,
        "medallion_layer": layer,
        "hive_phase": phase,
        "origin": "Phoenix Chromebook V-1"
    }

    receipt_path = f"{filepath}.receipt.json"
    with open(receipt_path, 'w') as f:
        json.dump(receipt, f, indent=4)
    print(f"✅ [P1 FUSE]: Receipt generated for {filepath} -> {os.path.basename(receipt_path)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_receipt.py <file_path> [layer] [phase]")
        sys.exit(1)

    path = sys.argv[1]
    layer = sys.argv[2] if len(sys.argv) > 2 else "Bronze"
    phase = sys.argv[3] if len(sys.argv) > 3 else "V"

    if os.path.isfile(path):
        generate_receipt(path, layer, phase)
    else:
        print(f"❌ Error: File {path} not found.")
