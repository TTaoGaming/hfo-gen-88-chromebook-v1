#!/usr/bin/env python3
import json
import os
import time

# Medallion: Bronze | Mutation: 0% | HIVE: V
# CHAOS TEST: Intentionally violating the 8 Shields to verify Port 5 defense.

BLACKBOARD = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
CORE_HTML = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/v10_one_euro_demo.html"

def inject_violations():
    print("🔥 [CHAOS_TEST]: Injecting violations...")

    # 1. CHRONOS Violation: Post-dated entry (Amnesia)
    with open(BLACKBOARD, "a") as f:
        f.write(json.dumps({
            "timestamp": "2024-01-01T00:00:00Z",
            "phase": "E",
            "summary": "CHAOS_TEST: Temporal Breach - Back to the Future."
        }) + "\n")
    print("   ❌ CHRONOS: Injected post-dated entry.")

    # 2. PORT-0-OBSERVE Violation: H-Phase without Search Receipt
    with open(BLACKBOARD, "a") as f:
        f.write(json.dumps({
            "timestamp": "2026-01-10T12:00:00Z",
            "phase": "H",
            "summary": "CHAOS_TEST: Sourcing from thin air (Search Bypass).",
            "p0": {"status": "sensing", "receipt": "CHEATING_NO_API"}
        }) + "\n")
    print("   ❌ PORT-0-OBSERVE: Injected search bypass.")

    # 3. GHOST Violation: Orphaned File
    orphan_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p5_immunize/GHOST_ORPHAN.py"
    with open(orphan_path, "w") as f:
        f.write("# This file is not in the blackboard.\n")
    print("   ❌ GHOST: Created orphaned file.")

    # 4. PRE-COMMIT Violation: Corrupting Header
    with open(CORE_HTML, "r") as f:
        content = f.read()
    corrupt_content = content.replace("Medallion: Bronze", "CORRUPT_HEADER")
    with open(CORE_HTML, "w") as f:
        f.write(corrupt_content)
    print("   ❌ PRE-COMMIT: Corrupted medallion header.")

if __name__ == "__main__":
    inject_violations()
