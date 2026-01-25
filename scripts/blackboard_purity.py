#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 95% | HIVE: V
# Port 5: DEFEND | Blackboard Purity & Immutability Sentinel

import os
import json
import hashlib
import sys
import argparse
from datetime import datetime

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

BLACKBOARD_PATH = str(REPO_ROOT / "hfo_hot_obsidian" / "hot_obsidian_blackboard.jsonl")
QUARANTINE_PATH = str(
    REPO_ROOT / "hfo_hot_obsidian" / "bronze" / "1_projects" / "blackboard_quarantine.jsonl"
)
MANIFEST_PATH = str(REPO_ROOT / "hfo_hot_obsidian" / "blackboard_manifest.json")
SECRET_PATH = str(REPO_ROOT / ".hfo_secret")


def _compute_sha256(path: str):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def _read_manifest(path: str):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

def get_secret():
    if os.path.exists(SECRET_PATH):
        with open(SECRET_PATH, "r") as f:
            return f.read().strip()
    return "HFO_DEFAULT_SECRET"

def verify_and_quarantine(*, quiet: bool = False, check_only: bool = False):
    if not os.path.exists(BLACKBOARD_PATH):
        return True

    if check_only:
        blackboard_sha256 = _compute_sha256(BLACKBOARD_PATH)
        manifest = _read_manifest(MANIFEST_PATH)
        if manifest is None:
            if not quiet:
                print("❌ [PURITY]: Manifest missing/unreadable; run scripts/blackboard_purity.py to regenerate.")
            return False

        status = manifest.get("status")
        if status != "PASS":
            if not quiet:
                print(f"❌ [PURITY]: Manifest status is {status!r}; refusing push.")
            return False

        if manifest.get("blackboard_sha256") != blackboard_sha256:
            if not quiet:
                print("❌ [PURITY]: Blackboard changed since last manifest generation.")
                print("💡 [PURITY]: Stop blackboard writers, then run: python3 scripts/blackboard_purity.py")
            return False

        if not quiet:
            print("✅ [PURITY]: Blackboard matches manifest (check-only).")
        return True

    secret = get_secret()
    valid_lines = []
    quarantined_count = 0
    immutability_breach = False

    with open(BLACKBOARD_PATH, 'r') as f:
        lines = f.readlines()

    last_sig = "ROOT"
    last_timestamp = None
    seal_found = False

    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue

        try:
            entry = json.loads(line)

            # --- SEAL RECOGNITION ---
            # A SEAL signal resets the validation chain to allow proceeding after documented breaches.
            if entry.get("phase") == "SIGNAL" and entry.get("query") == "RED_TRUTH_SEAL":
                if not quiet:
                    print(f"⚓ [PURITY]: RED_TRUTH_SEAL found at line {i+1}. Restarting chain validation.")
                last_sig = entry.get("signature")
                last_timestamp = None # Reset chronology check for new epoch? Optional.
                seal_found = True
                immutability_breach = False # Reset breach for this run if we found a seal
                continue

            # Skip validation if we haven't found a seal and there was a prior breach?
            # No, we validate everything, but the SEAL acts as the new anchor.

            # Check for Immutability Breach (Signatures/Chain)
            sig = entry.get("signature")
            if not sig:
                if not quiet:
                    print(f"❌ [PURITY]: Unsigned entry at line {i+1}")
                # We don't quarantine yet, just mark as breach
                immutability_breach = True
            else:
                # Verify HMAC Chain
                temp_entry = entry.copy()
                temp_entry.pop("signature")
                entry_str = json.dumps(temp_entry, sort_keys=True)
                # Try both possible 'prev' signals if this is the first line
                prev = last_sig if last_sig != "ROOT" else "LEGACY"
                expected = hashlib.sha256(f"{secret}:{prev}:{entry_str}".encode()).hexdigest()

                # Check against LEGACY as well for root entry
                if sig != expected and last_sig == "ROOT":
                    expected_legacy = hashlib.sha256(f"{secret}:LEGACY:{entry_str}".encode()).hexdigest()
                    if sig == expected_legacy:
                        expected = expected_legacy

                if sig != expected:
                    if not quiet:
                        print(f"❌ [PURITY]: Chain fracture at line {i+1}. TAMPER DETECTION.")
                    immutability_breach = True

                last_sig = sig

            # Check Chronology
            ts_str = entry.get("timestamp")
            if ts_str:
                try:
                    # Handle Z suffix
                    clean_ts = ts_str.replace('Z', '')
                    current_ts = datetime.fromisoformat(clean_ts)
                    if last_timestamp and current_ts < last_timestamp:
                        if not quiet:
                            print(f"❌ [PURITY]: Chronological breach at line {i+1} ({ts_str} < {last_timestamp.isoformat()})")
                        immutability_breach = True
                    last_timestamp = current_ts
                except ValueError:
                    pass

            valid_lines.append(line)

        except json.JSONDecodeError:
            if not quiet:
                print(f"⚠️ [PURITY]: Malformed JSON at line {i+1}. Quarantining...")
            with open(QUARANTINE_PATH, 'a') as qf:
                qentry = {
                    "quarantine_ts": datetime.utcnow().isoformat() + "Z",
                    "original_line_index": i + 1,
                    "raw_content": line
                }
                qf.write(json.dumps(qentry) + "\n")
            quarantined_count += 1
            continue

    # Rewrite blackboard if entries were quarantined
    if quarantined_count > 0:
        with open(BLACKBOARD_PATH, 'w') as f:
            for vline in valid_lines:
                f.write(vline + "\n")
        if not quiet:
            print(f"✅ [PURITY]: {quarantined_count} malformed entries moved to quarantine.")

    # Generate Master Hash for Git Ops
    with open(BLACKBOARD_PATH, 'rb') as f:
        master_hash = hashlib.sha256(f.read()).hexdigest()

    next_manifest = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "blackboard_sha256": master_hash,
        "line_count": len(valid_lines),
        "quarantined_last_run": quarantined_count,
        "status": "PASS" if not immutability_breach else "BREACH"
    }

    # Pre-push hook safety: avoid rewriting a tracked file every run just due to timestamp.
    # Only update the manifest on meaningful changes.
    try:
        if os.path.exists(MANIFEST_PATH):
            with open(MANIFEST_PATH, 'r') as f:
                current_manifest = json.load(f)
            comparable_keys = ["blackboard_sha256", "line_count", "quarantined_last_run", "status"]
            if all(current_manifest.get(k) == next_manifest.get(k) for k in comparable_keys):
                next_manifest["timestamp"] = current_manifest.get("timestamp", next_manifest["timestamp"])
                next_manifest = current_manifest
    except Exception:
        pass

    with open(MANIFEST_PATH, 'w') as f:
        json.dump(next_manifest, f, indent=4)

    # Block Git commit if there's an immutability breach
    if immutability_breach:
        if not quiet:
            print("🚨 [PURITY]: Immutability breach detected. Blackboard has been edited or tampered with.")
            print("💡 [PURITY]: To resume the chain, you must log a 'SIGNAL: RED_TRUTH_ANCHOR' via the Hub.")
        return False

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HFO Blackboard Purity & Immutability Sentinel")
    parser.add_argument("--check-only", action="store_true", help="Verify manifest matches blackboard; do not rewrite files")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-line diagnostics")
    args = parser.parse_args()

    if not verify_and_quarantine(quiet=args.quiet, check_only=args.check_only):
        sys.exit(1)

    if not args.quiet:
        if args.check_only:
            print("✅ [PURITY]: Blackboard Integrity Verified (check-only).")
        else:
            print("✅ [PURITY]: Blackboard Integrity Verified. Manifest updated.")
    sys.exit(0)
