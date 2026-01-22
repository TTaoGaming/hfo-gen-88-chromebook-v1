#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""
Root shim for the MCP Gateway Hub.

Purpose:
- Keep a stable root entrypoint for versioned/aliased gateway hub layers.
- Delegate execution to the current Alpha project implementation.
"""

import os
import runpy
from pathlib import Path

BASE_PATH = Path("/home/tommytai3/active/hfo_gen_88_chromebook_v_1")

DEFAULT_TARGET = BASE_PATH / "hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py"

try:
    from hfo_pointers import resolve_target

    TARGET = Path(
        resolve_target(
            env_var="HFO_MCP_GATEWAY_TARGET",
            dotted_key="targets.mcp_gateway_impl",
            default=str(DEFAULT_TARGET),
        )
    )
except Exception:
    TARGET = Path(os.environ.get("HFO_MCP_GATEWAY_TARGET", str(DEFAULT_TARGET)))

try:
    from dotenv import load_dotenv

    load_dotenv(BASE_PATH / ".env", override=False)
except Exception:
    pass

if __name__ == "__main__":
    runpy.run_path(str(TARGET), run_name="__main__")
