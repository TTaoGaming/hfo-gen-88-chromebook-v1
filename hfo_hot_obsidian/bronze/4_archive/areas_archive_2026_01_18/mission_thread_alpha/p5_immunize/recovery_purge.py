# Medallion: Bronze | Mutation: 0% | HIVE: I
#!/usr/bin/env python3
import json
import os

BLACKBOARD = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
ORPHAN = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p5_immunize/GHOST_ORPHAN.py"
DEMO_HTML = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/v10_one_euro_demo.html"

def purge():
    print("🧹 [RECOVERY]: Cleaning up stress test damage...")

    # 1. Blackboard Purge
    if os.path.exists(BLACKBOARD):
        with open(BLACKBOARD, "r") as f:
            lines = f.readlines()

        cleaned_lines = []
        for line in lines:
            try:
                data = json.loads(line)
                # Purge 2024 (Chronos breach) or search bypass (P0 breach)
                if "2024-01-01" in data.get("timestamp", ""): continue
                if data.get("p0", {}).get("receipt") == "CHEATING_NO_API": continue
                if "CHAOS_TEST" in data.get("summary", ""): continue
                cleaned_lines.append(line)
            except:
                continue

        with open(BLACKBOARD, "w") as f:
            f.writelines(cleaned_lines)
        print(f"   ✅ Blackboard cleaned. Removed {len(lines) - len(cleaned_lines)} chaos entries.")

    # 2. Delete Ghost Orphan
    if os.path.exists(ORPHAN):
        os.remove(ORPHAN)
        print("   ✅ Deleted GHOST_ORPHAN.py.")

    # 3. Restore Header (if still corrupt)
    if os.path.exists(DEMO_HTML):
        with open(DEMO_HTML, "r") as f:
            content = f.read()
        if "CORRUPT_HEADER" in content:
            restored = content.replace("CORRUPT_HEADER", "Medallion: Bronze")
            with open(DEMO_HTML, "w") as f:
                f.write(restored)
            print("   ✅ Restored Medallion header in demo HTML.")

if __name__ == "__main__":
    purge()
