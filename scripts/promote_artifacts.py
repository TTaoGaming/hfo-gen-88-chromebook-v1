import os
import json
import hashlib
import datetime

FILES_TO_PROMOTE = [
    {
        "src": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_2/omega_gen2_v2.html",
        "dest": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_omega_gen_2/omega_gen2_v2.html"
    },
    {
        "src": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega_gen_2/omega_gen2_v3.html",
        "dest": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_omega_gen_2/omega_gen2_v3.html"
    },
    {
        "src": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/strange_loop_intervener.py",
        "dest": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/2_areas/mission_thread_alpha/strange_loop_intervener.py"
    },
    {
        "src": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/reports/FORENSIC_REPORT_V55_CHRONOS.md",
        "dest": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/4_archive/FORENSIC_REPORT_V55_CHRONOS.md"
    },
    {
        "src": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/reports/FORENSIC_ROOT_CAUSE_INTROSPECTION.md",
        "dest": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/4_archive/FORENSIC_ROOT_CAUSE_INTROSPECTION.md"
    },
    {
        "src": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/reports/AI_SLOP_DEFENSE_REPORT.md",
        "dest": "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_cold_obsidian/bronze/4_archive/AI_SLOP_DEFENSE_REPORT.md"
    }
]

def promote():
    for f in FILES_TO_PROMOTE:
        src = f["src"]
        dest = f["dest"]
        
        if not os.path.exists(src):
            print(f"Skipping {src} (not found)")
            continue
            
        # Ensure dest dir exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        # Read content
        with open(src, "rb") as sf:
            content = sf.read()
            
        # Write to dest
        with open(dest, "wb") as df:
            df.write(content)
            
        # Calculate hash
        file_hash = hashlib.sha256(content).hexdigest()
        
        # Create receipt
        receipt = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": src,
            "target": dest,
            "hash": file_hash,
            "medallion": "Bronze",
            "state": "Frozen"
        }
        
        with open(dest + ".receipt.json", "w") as rf:
            json.dump(receipt, rf, indent=4)
            
        print(f"Promoted {src} -> {dest}")

if __name__ == "__main__":
    promote()
