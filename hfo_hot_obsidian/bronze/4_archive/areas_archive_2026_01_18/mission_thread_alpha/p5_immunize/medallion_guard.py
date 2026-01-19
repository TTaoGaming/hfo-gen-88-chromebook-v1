#!/usr/bin/env python3
import sys
import os
import json
import hashlib

# Medallion: Bronze | Mutation: 0% | HIVE: V
# PORT-5-IMMUNIZE: Medallion Transition Guard (Tamper-Evident Receipts)

def get_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def check_transition(filepath):
    # Only protect Cold layers and Silver/Gold layers
    if not ("hfo_cold_obsidian" in filepath or "silver" in filepath or "gold" in filepath):
        return True

    receipt_path = f"{filepath}.receipt.json"

    if not os.path.exists(receipt_path):
        print(f"❌ [P5 ERROR]: Transition Blocked. No receipt found for {filepath}")
        print(f"   Required: {os.path.basename(receipt_path)}")
        return False

    try:
        with open(receipt_path, 'r') as f:
            receipt = json.load(f)
            expected_hash = receipt.get("hash")
            current_hash = get_file_hash(filepath)

            if current_hash != expected_hash:
                print(f"❌ [P4 SCREAM_1: BREACH]: Tamper detected in {filepath}")
                print(f"   Receipt Hash: {expected_hash[:8]}...")
                print(f"   Current Hash: {current_hash[:8]}...")
                return False

            return True
    except Exception as e:
        print(f"❌ [P5 ERROR]: Failed to validate receipt for {filepath}: {e}")
        return False

def main():
    files = sys.argv[1:]
    failed = False
    for f in files:
        if os.path.isfile(f) and not f.endswith(".receipt.json"):
            if not check_transition(f):
                failed = True

    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()
