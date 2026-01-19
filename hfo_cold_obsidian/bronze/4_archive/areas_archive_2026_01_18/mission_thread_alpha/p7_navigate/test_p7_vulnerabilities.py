# Medallion: Bronze | Mutation: 0% | HIVE: I
"""
P7 Vulnerability & Breakage Test (RED TEAM)
This script attempts to identify edge cases in the Port 7 Thinking Octet logging.
1. JSON Corruption Detection
2. Shard Limit Breach Detection
3. Missing Step Detection (Stigmergy Orphanhood)
"""

import json
import os
import sys

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"

def run_audit():
    print("--- P7 BLACKBOARD AUDIT START ---")

    if not os.path.exists(BLACKBOARD_PATH):
        print(f"FAILED: No blackboard found at {BLACKBOARD_PATH}")
        return

    corrupt_lines = []
    overflows = []
    orphan_steps = []

    with open(BLACKBOARD_PATH, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)

            # 1. Check for Overflows
            used = data.get("tokens_used", 0)
            cap = data.get("token_cap", 0)
            if used > cap and cap > 0:
                overflows.append((i+1, data.get("tool"), used, cap))

            # 2. Check for missing metadata
            if "tool" not in data or "thought_hash" not in data:
                orphan_steps.append((i+1, "Missing critical keys"))

        except json.JSONDecodeError:
            corrupt_lines.append(i+1)

    # Report Results
    if corrupt_lines:
        print(f"CRITICAL: Found {len(corrupt_lines)} corrupt JSON lines: {corrupt_lines}")
    else:
        print("SUCCESS: JSON Integrity verified.")

    if overflows:
        print(f"WARNING: Found {len(overflows)} shunt overflows (Used > Cap):")
        for line, tool, used, cap in overflows:
            print(f"  Line {line}: {tool} used {used} but cap is {cap}")
    else:
        print("SUCCESS: No shard overflows detected.")

    if orphan_steps:
        print(f"WARNING: Found {len(orphan_steps)} orphan or malformed entries: {orphan_steps}")
    else:
        print("SUCCESS: No orphans detected.")

    print("--- P7 BLACKBOARD AUDIT END ---")

if __name__ == "__main__":
    # Create a deliberate breakage if argument passed
    if len(sys.argv) > 1 and sys.argv[1] == "--break":
        print("INJECTING DELIBERATE BREAKAGE...")
        with open(BLACKBOARD_PATH, "a") as f:
            # Malformed JSON
            f.write("{\"timestamp\": \"BAD_JSON\", \"broken\": true \n")
            # Overflow
            f.write(json.dumps({
                "timestamp": "2026-01-09T00:00:00Z",
                "tool": "T99",
                "thought_hash": "deadbeef",
                "tokens_used": 9999,
                "token_cap": 1024,
                "payload": {"summary": "DELIBERATE OVERFLOW"}
            }) + "\n")
        print("Breakage injected. Run audit to detect.")

    run_audit()
