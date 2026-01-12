import os
import hashlib
import json
import shutil
from datetime import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: I

SOURCE_DIR_CODE = "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/piano_genie_official"
TARGET_DIR_CODE = "hfo_cold_obsidian/bronze/2_areas/mission_thread_omega/piano_genie_official"

SOURCE_DIR_ASSETS = "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/assets/piano_genie"
TARGET_DIR_ASSETS = "hfo_cold_obsidian/bronze/2_areas/mission_thread_omega/assets/piano_genie"

TIMESTAMP = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_receipt(relative_path, file_hash):
    receipt = {
        "artifact": relative_path,
        "hash": file_hash,
        "timestamp": TIMESTAMP,
        "medallion": "BRONZE",
        "mutation_score": 0.0,
        "status": "RED_TRUTH",
        "hive": "I"
    }
    return receipt

def freeze_directory(source, target):
    if not os.path.exists(target):
        os.makedirs(target)
    
    for root, dirs, files in os.walk(source):
        # Calculate relative path for target directory structure
        rel_dir = os.path.relpath(root, source)
        dest_dir = os.path.join(target, rel_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        for file in files:
            if file.endswith(".receipt.json"):
                continue
                
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            
            # 1. Calculate Hash
            file_hash = calculate_hash(src_file)
            
            # 2. Copy File
            shutil.copy2(src_file, dest_file)
            print(f"✅ Copied: {src_file} -> {dest_file}")
            
            # 3. Create Receipt
            # Use the formal repo path for artifact ID
            repo_path = os.path.relpath(dest_file, "/home/tommytai3/active/hfo_gen_88_chromebook_v_1")
            receipt = create_receipt(repo_path, file_hash)
            receipt_file = dest_file + ".receipt.json"
            
            with open(receipt_file, "w") as f:
                json.dump(receipt, f, indent=2)
            print(f"📜 Receipt generated: {receipt_file}")

if __name__ == "__main__":
    print("🧊 Initiating HFO Cold Bronze Freeze...")
    freeze_directory(SOURCE_DIR_CODE, TARGET_DIR_CODE)
    freeze_directory(SOURCE_DIR_ASSETS, TARGET_DIR_ASSETS)
    print("🚀 Freeze Complete.")
