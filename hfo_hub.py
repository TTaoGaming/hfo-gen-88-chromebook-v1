#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Root hub shim for HFO.

This shim provides a stable root entrypoint that forwards to the current
Hub implementation. Change the target path via HFO_HUB_TARGET to swap
versions without changing callers.
"""

import os
import sys
import runpy
from pathlib import Path

BASE = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
DEFAULT_TARGET = os.path.join(
    BASE,
    "hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py",
)
TARGET = os.environ.get("HFO_HUB_TARGET", DEFAULT_TARGET)

try:
    from dotenv import load_dotenv

    load_dotenv(Path(BASE) / ".env", override=False)
except Exception:
    pass

if __name__ == "__main__":
    sys.argv[0] = TARGET
    runpy.run_path(TARGET, run_name="__main__")
