# Medallion: Bronze | Mutation: 0% | HIVE: I
# 🧠 HFO 8-Step Sequential Thinking Framework (Hardened Trace)
# This script enforces the mandatory 8-step reasoning process for HFO agents,
# with HFO verbs and BDD receipt generation for behavior tracing.

import json
import datetime
import os
import sys
import hashlib

HFO_VERB_MAP = {
    1: "OBSERVE",   # PORT-0-OBSERVE
    2: "BRIDGE",    # PORT-1-BRIDGE
    3: "SHAPE",     # P2 SHAPE
    4: "INJECT",    # PORT-3-INJECT
    5: "DISRUPT",   # P4 DISRUPT
    6: "IMMUNIZE",  # PORT-5-IMMUNIZE
    7: "ARCHIVE",   # PORT-6-ARCHIVE
    8: "NAVIGATE"   # P7 NAVIGATE
}

class SequentialThinker:
    def __init__(self, blackboard_path):
        self.blackboard_path = blackboard_path
        self.total_steps = 8

    def _generate_receipt(self, step, thought):
        salt = datetime.datetime.utcnow().isoformat()
        raw = f"{step}-{thought}-{salt}"
        return f"THOUGHT_{step}_{hashlib.sha256(raw.encode()).hexdigest()[:8].upper()}"

    def add_thought(self, thought, step, is_revision=False):
        if step > self.total_steps:
             print(f"❌ [P7 ERROR]: Thought step {step} exceeds mandatory limit of {self.total_steps}")
             return None

        verb = HFO_VERB_MAP.get(step, "UNKNOWN")
        receipt = self._generate_receipt(step, thought)
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"

        entry = {
            "timestamp": timestamp,
            "phase": "I",
            "summary": f"[{verb}] Thought {step}/{self.total_steps}: {thought[:50]}...",
            "details": {
                "thought": thought,
                "step": step,
                "verb": verb,
                "total_steps": self.total_steps,
                "is_revision": is_revision,
                "thought_receipt": receipt,
                "expected_behavior": f"hfo_{verb.lower()}_logic"
            },
            "p7": {"status": "thinking", "receipt": receipt}
        }

        self._log_to_blackboard(entry)
        return entry

    def _log_to_blackboard(self, entry):
        with open(self.blackboard_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')

def main():
    if len(sys.argv) < 3:
        print("Usage: sequential_thinking.py <step> '<thought>'")
        sys.exit(1)

    try:
        step = int(sys.argv[1])
        thought = sys.argv[2]

        thinker = SequentialThinker("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/hot_obsidian_blackboard.jsonl")
        thinker.add_thought(thought, step)
    except Exception as e:
        print(f"❌ [P7 ERROR]: Failed to log thought: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
