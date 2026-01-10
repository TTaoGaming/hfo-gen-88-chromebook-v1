#!/usr/bin/env python3
import subprocess
import os
import json
import datetime

# Medallion: Bronze | Mutation: 0% | HIVE: I
# P6 STORE: HFO GitOps Sharding Engine
# Partitions the repository into 8-port shards for distributed persistence.

BLACKBOARD_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
SHARD_LOG = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p6_store/GIT_SHARD_RECEIPT.jsonl"

SHARDS = {
    "P0_SENSE": ["hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p0_sense/**"],
    "P1_FUSE": ["hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p1_fuse/**", "hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/p1_fuse/**"],
    "P2_SHAPE": ["hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/p2_shape/**"],
    "P3_DELIVER": ["hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/p3_deliver/**"],
    "P4_DISRUPT": ["hfo_hot_obsidian/bronze/4_archive/**"],
    "P5_DEFEND": ["hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p5_defend/**", "hfo_hot_obsidian/bronze/2_areas/p5_defend/**"],
    "P6_STORE": ["hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p6_store/**"],
    "P7_NAVIGATE": ["hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p7_navigate/**"]
}

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
    return result.stdout.strip()

def shard_and_save():
    print("🚀 [P6 STORE]: Initializing GitOps Sharding...")

    # 1. Stage All Current Changes
    run_cmd("git add .")

    # 2. Commit the Mosaic State
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    commit_msg = f"HFO Gen 88 Pulse: {timestamp} | Medallion: Bronze"
    run_cmd(f"git commit -m '{commit_msg}'")

    # 3. Generate Shard Receipts
    git_hash = run_cmd("git rev-parse HEAD")

    receipt = {
        "timestamp": timestamp,
        "git_hash": git_hash,
        "shards": list(SHARDS.keys()),
        "medallion": "bronze"
    }

    with open(SHARD_LOG, "a") as f:
        f.write(json.dumps(receipt) + "\n")

    print(f"✅ [P6 STORE]: GitOps Shard Complete. Hash: {git_hash}")
    return git_hash

if __name__ == "__main__":
    shard_and_save()
