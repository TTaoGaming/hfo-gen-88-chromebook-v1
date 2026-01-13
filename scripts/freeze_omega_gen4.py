import os
import json
import hashlib
import datetime

BASE_DIR = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
FILES_TO_FREEZE = [
    "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v1.html",
    "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v2.html",
    "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v3.html",
    "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v4.html",
    "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_v5.html",
    "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_4/omega_gen4_manifest.yaml",
    "reports/AI_STRUGGLE_REPORT_2026_01_12.md",
]

def freeze():
    for rel_path in FILES_TO_FREEZE:
        src = os.path.join(BASE_DIR, rel_path)
        # Determine dest path
        if rel_path.startswith("reports/"):
            dest = os.path.join(BASE_DIR, "hfo_cold_obsidian/bronze/4_archive", os.path.basename(rel_path))
        else:
            dest = os.path.join(BASE_DIR, "hfo_cold_obsidian", rel_path.replace("hfo_hot_obsidian/", ""))
            
        if not os.path.exists(src):
            print(f"Skipping {src} (not found)")
            continue
            
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        with open(src, "rb") as sf:
            content = sf.read()
            
        with open(dest, "wb") as df:
            df.write(content)
            
        file_hash = hashlib.sha256(content).hexdigest()
        
        receipt = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": rel_path,
            "target": dest.replace(BASE_DIR + "/", ""),
            "hash": file_hash,
            "medallion": "Bronze",
            "state": "Frozen",
            "hive": "V"
        }
        
        with open(dest + ".receipt.json", "w") as rf:
            json.dump(receipt, rf, indent=4)
            
        print(f"Frozen: {rel_path} -> {receipt['target']}")

if __name__ == "__main__":
    freeze()
