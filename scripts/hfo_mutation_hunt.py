#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 98% | HIVE: V
"""
🧬 HFO MUTATION HUNT: GOLDILOCKS AUDIT
This script intentionally injects faults into the HFO-8 environment
to verify that the P5-HardGate isn't 'theater'.
Target score: 88% - 98.99%
"""

import os
import subprocess
import json
import time
import sys

ORCHESTRATION_PATH = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/ports"
if ORCHESTRATION_PATH not in sys.path:
    sys.path.append(ORCHESTRATION_PATH)

MANIFOLD = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/architecture/ports/hfo_orchestration_hub.py"

def run_manifold_p5():
    res = subprocess.run(["python3", MANIFOLD, "p5"], capture_output=True, text=True)
    return json.loads(res.stdout)

def test_mutation(name, setup_fn, cleanup_fn):
    print(f"🧪 Testing Mutation: {name}")
    setup_fn()
    try:
        # Run think first to update blackboard state
        subprocess.run(["python3", MANIFOLD, "think", f"Mutation: {name}"], capture_output=True)
        result = run_manifold_p5()
        status = result.get("p1", {}).get("status")
        if status in ["BLOCK", "FAIL"]:
            print(f"✅ Mutation Caught: {status}")
            return True
        else:
            print(f"❌ MUTATION LEAKED: HardGate returned {status}")
            return False
    finally:
        cleanup_fn()

# --- MUTATION 1: Corrupt Physics ---
def setup_physics_break():
    # Rename the auditor script so it fails
    os.rename("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/scripts/physics_auditor.py", "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/scripts/physics_auditor.py.bak")

def cleanup_physics_break():
    if os.path.exists("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/scripts/physics_auditor.py.bak"):
        os.rename("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/scripts/physics_auditor.py.bak", "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/scripts/physics_auditor.py")

# --- MUTATION 2: Delete P3 Injector ---
def setup_p3_break():
    # Patch the dynamic HTML
    from hfo_orchestration_hub import get_active_workspace
    path = get_active_workspace()
    with open(path, "r") as f:
        content = f.read()
    with open(path, "w") as f:
        f.write(content.replace("p3InjectPointer", "p3BROKENPointer"))

def cleanup_p3_break():
    from hfo_orchestration_hub import get_active_workspace
    path = get_active_workspace()
    with open(path, "r") as f:
        content = f.read()
    with open(path, "w") as f:
        f.write(content.replace("p3BROKENPointer", "p3InjectPointer"))

# --- MUTATION 3: Bypass Thinking (Reward Hacking) ---
def test_reward_hack():
    print("🧪 Testing Mutation: Reward Hack (Bypassing Think)")
    # We DON'T run think. We just run p5. 
    # But wait, p5 looks at the PREVIOUS receipt.
    # To truly test reward hacking, we need to inject a fake receipt into the blackboard.
    bb_path = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
    with open(bb_path, "a") as f:
        f.write(json.dumps({
            "timestamp": "2026-01-10T00:00:00Z",
            "phase": "H",
            "summary": "Fake Thought",
            "thought_map": {"T0_SENSE": {"receipt_hash": "FAKE_HASH"}}
        }) + "\n")
    
    result = run_manifold_p5()
    status = result.get("p1", {}).get("status")
    if status == "BLOCK":
        print(f"✅ Reward Hack Caught: {status}")
        return True
    else:
        print(f"❌ REWARD HACK LEAKED: HardGate returned {status}")
        return False

if __name__ == "__main__":
    results = [
        test_mutation("Physics Break", setup_physics_break, cleanup_physics_break),
        test_mutation("P3 Missing", setup_p3_break, cleanup_p3_break),
        test_reward_hack()
    ]
    
    score = (sum(results) / len(results)) * 100
    print(f"\n📈 Mutation Detection Score: {score}%")
    if score >= 100:
        print("⚠️ VIOLATION: Score 100% detected. Mutation tests may be too trivial/fitted.")
    elif score >= 88:
        print("🎯 GOLDILOCKS ZONE REACHED (88-98.99%). Tests are non-trivial and effective.")
    else:
        print("📉 UNDER-TESTED. Increase mutation depth.")
