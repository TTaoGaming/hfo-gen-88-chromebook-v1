# Medallion: Bronze | Mutation: 0% | HIVE: V
"""
P7 PRAETORIAN: Port 7 Cognitive Integrity Guard
Enforces Thinking Octet schema and detects AI drift in the blackboard.
"""

import json
import os
import re
import yaml
import hashlib

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
OCTREE_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p7_navigate/P7_FRACTAL_OCTREE.yaml"

def load_limits():
    with open(OCTREE_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config['octant_navigator']['shards'], config['degradation_thresholds']

def check_p7_integrity():
    print("--- P5 PRAETORIAN: Port 7 Audit ---")
    shard_limits, thresholds = load_limits()

    if not os.path.exists(BLACKBOARD_PATH):
        print("FAIL: Blackboard missing.")
        return False

    violations = 0
    drift_warnings = 0

    with open(BLACKBOARD_PATH, "r") as f:
        for i, line in enumerate(f):
            try:
                data = json.loads(line)
                tool = data.get("tool", "")

                # Only audit Port 7 Thinking Octet tools
                if re.match(r"T[0-7]", tool):
                    # Find specific shard limit
                    tool_key = None
                    for k in shard_limits.keys():
                        if tool in k:
                            tool_key = k
                            break

                    limit = shard_limits.get(tool_key, 1024) if tool_key else 1024

                    # 1. Schema Check
                    required = ["timestamp", "thought_hash", "tokens_used", "token_cap"]
                    if not all(k in data for k in required):
                        print(f"VIOLATION [Line {i+1}]: Missing keys in {tool}")
                        violations += 1
                        continue

                    # 2. Shard Check
                    used = data["tokens_used"]
                    if used > limit:
                        print(f"VIOLATION [Line {i+1}]: {tool} overflow ({used}/{limit})")
                        violations += 1

                    # 3. Hash Integrity Check
                    payload_summary = data.get("payload", {}).get("summary", "")
                    expected_hash = hashlib.sha256(payload_summary.encode()).hexdigest()
                    if data["thought_hash"] != expected_hash:
                        # Allow short hashes for backward compatibility if they match the start
                        if not expected_hash.startswith(data["thought_hash"]):
                            print(f"VIOLATION [Line {i+1}]: {tool} HASH MISMATCH. (Corrupt or Mutated entry)")
                            violations += 1

                    # 4. Drift Check (Redlining against octree floors)
                    if used < thresholds['hard_floor']:
                        print(f"LOSS WARNING [Line {i+1}]: {tool} is in the DEATH ZONE ({used} tokens). Information is too lossy.")
                        drift_warnings += 1
                    elif used > limit * 0.9:
                        print(f"DRIFT WARNING [Line {i+1}]: {tool} is redlining.")
                        drift_warnings += 1

            except json.JSONDecodeError:
                # Ignore non-JSON for this specific tool, but P5-CHRONOS might care.
                pass

    print(f"Audit Complete. Violations: {violations}, Drift Warnings: {drift_warnings}")
    return violations == 0

if __name__ == "__main__":
    success = check_p7_integrity()
    if not success:
        exit(1)
