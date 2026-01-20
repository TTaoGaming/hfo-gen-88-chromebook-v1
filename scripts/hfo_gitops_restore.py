#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

# Medallion: Bronze | Mutation: 0% | HIVE: I
# PORT-6-ARCHIVE: HFO GitOps Restorer
# Restores all missing receipts in Cold Bronze by running freeze_to_cold.py on all Hot Bronze files.

REPO_ROOT = Path(__file__).resolve().parents[1]
HOT_ROOT = REPO_ROOT / "hfo_hot_obsidian" / "bronze"

def _resolve_freeze_tool() -> Path:
    env_path = os.environ.get("HFO_FREEZE_TOOL")
    if env_path:
        return Path(env_path).expanduser().resolve()

    matches = list(HOT_ROOT.rglob("freeze_to_cold.py"))
    if len(matches) == 1:
        return matches[0]
    if len(matches) == 0:
        raise FileNotFoundError(
            f"freeze_to_cold.py not found under {HOT_ROOT}. Set HFO_FREEZE_TOOL to the script path."
        )

    # Fail-closed: ambiguous tooling is unsafe for GitOps.
    sample = "\n".join(str(p) for p in matches[:10])
    raise RuntimeError(
        f"Multiple freeze_to_cold.py matches found ({len(matches)}). Set HFO_FREEZE_TOOL explicitly. Sample:\n{sample}"
    )

def restore_receipts():
    freeze_tool = _resolve_freeze_tool()
    if not freeze_tool.exists():
        raise FileNotFoundError(f"Freeze tool missing: {freeze_tool}")

    print("🚀 [PORT-6-ARCHIVE]: Restoring receipts via GitOps Batch Freeze...")
    print(f"🔧 Using freeze tool: {freeze_tool}")

    count = 0
    failures = 0
    for root, dirs, files in os.walk(HOT_ROOT):
        for file in files:
            if file.endswith((".py", ".html", ".md", ".json", ".yaml", ".ts")):
                hot_path = os.path.join(root, file)
                proc = subprocess.run([
                    sys.executable,
                    str(freeze_tool),
                    hot_path,
                ], capture_output=True, text=True)
                if proc.returncode != 0:
                    failures += 1
                    print(f"❌ Freeze failed ({proc.returncode}) for: {hot_path}")
                    if proc.stderr:
                        print(proc.stderr.strip()[:2000])
                count += 1

    if failures:
        raise RuntimeError(f"GitOps restore completed with failures: {failures}/{count}")

    print(f"✅ [PORT-6-ARCHIVE]: Batch Freeze complete. {count} files processed.")

if __name__ == "__main__":
    try:
        restore_receipts()
    except Exception as e:
        print(f"🛑 [PORT-6-ARCHIVE]: GitOps restore failed: {e}")
        raise
