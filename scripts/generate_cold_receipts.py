# Medallion: Bronze | Mutation: 0% | HIVE: E
import hashlib
import json
import datetime
import os

def generate_receipt(source_path, target_path, medallion="Bronze"):
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
    print(f"Generated receipt for {target_path}")

# HFO_ARCHETYPE_ANALYSIS_V1.md
generate_receipt(
    "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/reports/HFO_ARCHETYPE_ANALYSIS_V1.md",
    "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_alpha/HFO_ARCHETYPE_ANALYSIS_V1.md"
)

# LEGENDARY_HFO_COMMANDERS_THE_OCTAL_MANIFEST.md
generate_receipt(
    "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_THE_OCTAL_MANIFEST.md",
    "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_omega/LEGENDARY_HFO_COMMANDERS_THE_OCTAL_MANIFEST.md"
)
