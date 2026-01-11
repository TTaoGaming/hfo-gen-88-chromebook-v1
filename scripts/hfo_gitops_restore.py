#!/usr/bin/env python3
import os
import subprocess

# Medallion: Bronze | Mutation: 0% | HIVE: I
# PORT-6-ARCHIVE: HFO GitOps Restorer
# Restores all missing receipts in Cold Bronze by running freeze_to_cold.py on all Hot Bronze files.

HOT_ROOT = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze"
FREEZE_TOOL = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p5_immunize/freeze_to_cold.py"

def restore_receipts():
    print("🚀 [PORT-6-ARCHIVE]: Restoring receipts via GitOps Batch Freeze...")
    
    count = 0
    for root, dirs, files in os.walk(HOT_ROOT):
        for file in files:
            if file.endswith((".py", ".html", ".md", ".json", ".yaml", ".ts")):
                hot_path = os.path.join(root, file)
                subprocess.run(["python3", FREEZE_TOOL, hot_path])
                count += 1
    
    print(f"✅ [PORT-6-ARCHIVE]: Batch Freeze complete. {count} receipts regenerated.")

if __name__ == "__main__":
    restore_receipts()
