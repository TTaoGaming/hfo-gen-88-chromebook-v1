# Medallion: Bronze | Mutation: 0% | HIVE: E
import hashlib
import json
import datetime
import os
import shutil

def generate_receipt(source_path, target_path, medallion="Bronze"):
    if not os.path.exists(target_path):
        print(f"Error: Target path {target_path} does not exist. Copy the file first.")
        return

    with open(target_path, "rb") as f:
        content = f.read()
        sha256_hash = hashlib.sha256(content).hexdigest()
    
    receipt = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "source": source_path,
        "target": target_path,
        "hash": sha256_hash,
        "medallion": medallion,
        "state": "Frozen"
    }
    
    receipt_path = target_path + ".receipt.json"
    with open(receipt_path, "w") as f:
        json.dump(receipt, f, indent=4)
    print(f"Generated receipt for {os.path.basename(target_path)}")

def freeze_file(source_dir, target_dir, filename, medallion="Bronze"):
    source_path = os.path.join(source_dir, filename)
    target_path = os.path.join(target_dir, filename)
    
    if not os.path.exists(source_path):
        print(f"Skipping {filename}: Source does not exist.")
        return

    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Copy file
    shutil.copy2(source_path, target_path)
    print(f"Copied {filename} to Cold Bronze")
    
    # Generate receipt
    generate_receipt(source_path, target_path, medallion)

if __name__ == "__main__":
    hot_dir = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/"
    cold_dir = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_omega_gen_4/"
    
    # Auto-discover all omega files in the hot directory
    for f in os.listdir(hot_dir):
        if f.startswith("omega_gen4_v") or f in ["OMEGA_EVOLUTION_HISTORY.md", "OMEGA_GEN4_DELTA_REPORT.md", "SUCCESSFUL_PATTERNS_OMEGA.md", "omega_gen4_manifest.yaml"]:
            freeze_file(hot_dir, cold_dir, f)

    # Freeze the freshly tracked user notes as well?
    notes_hot = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/1_projects/sprawl_cleanup_2026_01_14/"
    notes_cold = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/1_projects/sprawl_cleanup_2026_01_14/"
    
    if os.path.exists(notes_hot):
        for note in os.listdir(notes_hot):
            if note.endswith(".md"):
                freeze_file(notes_hot, notes_cold, note)

    # Freeze the current note if possible?
    # root_dir = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/"
    # freeze_file(root_dir, os.path.join(cold_dir, "../../4_archive/"), "ttao-notes-2025-1-14.md")
