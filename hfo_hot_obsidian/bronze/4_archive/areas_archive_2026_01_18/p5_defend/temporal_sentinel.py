#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

from pathlib import Path

# Medallion: Bronze | Mutation: 0% | HIVE: V
# PORT-5-IMMUNIZE: AI Theater & Workflow Sentinel

REPO_ROOT = Path(__file__).resolve()
for _ in range(8):
    REPO_ROOT = REPO_ROOT.parent
    if (REPO_ROOT / "AGENTS.md").exists():
        break

BLACKBOARD_PATH = str(REPO_ROOT / "hfo_hot_obsidian" / "hot_obsidian_blackboard.jsonl")
GRUDGE_PATH = str(
    REPO_ROOT
    / "hfo_hot_obsidian"
    / "bronze"
    / "2_areas"
    / "p5_immunize"
    / "BOOK_OF_BLOOD_GRUDGES.jsonl"
)


def _parse_ts(value: str) -> datetime | None:
    if not value:
        return None
    try:
        # Support both Z and explicit offsets.
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None

def log_grudge(scream_id, message):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "port": "P4",
        "scream": f"SCREAM_{scream_id}",
        "severity": "CRITICAL",
        "msg": message
    }
    with open(GRUDGE_PATH, 'a') as f:
        f.write(json.dumps(entry) + "\n")

def check_blackboard():
    if not os.path.exists(BLACKBOARD_PATH):
        return True

    with open(BLACKBOARD_PATH, 'r') as f:
        lines = f.readlines()
        if not lines: return True

        logs = []
        for line in lines:
            try:
                logs.append(json.loads(line))
            except:
                continue

        # 1. Temporal Integrity (compare parsed datetimes; fall back to string if unparseable)
        last_raw = None
        last_dt = None
        for i, entry in enumerate(logs):
            raw = entry.get("timestamp")
            dt = _parse_ts(raw) if isinstance(raw, str) else None

            if last_raw is not None:
                if dt is not None and last_dt is not None:
                    if dt < last_dt:
                        print("❌ [P4 SCREAM_6: AMNESIA]: Non-chronological log sequence detected.")
                        print(f"   prev[{i-1}]={last_raw}")
                        print(f"   curr[{i}]={raw}")
                        return False
                elif isinstance(raw, str) and isinstance(last_raw, str):
                    if raw < last_raw:
                        print("❌ [P4 SCREAM_6: AMNESIA]: Non-chronological log sequence detected (string-compare fallback).")
                        print(f"   prev[{i-1}]={last_raw}")
                        print(f"   curr[{i}]={raw}")
                        return False

            last_raw = raw
            last_dt = dt

    return True

if __name__ == "__main__":
    if not check_blackboard():
        sys.exit(1)
    print("✅ [PORT-5-IMMUNIZE]: Temporal Integrity Verified.")
