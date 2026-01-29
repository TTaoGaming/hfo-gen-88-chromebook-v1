#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Memory guardrails (fail-closed) for Gen88.

Purpose:
- Enforce single blessed write path: Doobidoo sqlite_vec SSOT.
- Block accidental activation of legacy JSONL memory backends.
- Keep configuration anchored to `hfo_pointers.json`.

UX principle:
- Guide, don't punish: failures should include the blessed entryways and exact
    commands/tasks to self-correct.

Notes:
- This is a preflight-style check; it does not mutate state.
- Exit codes: 0=ok, 2=guardrails violated.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from hfo_memory_guardrails import (  # noqa: E402
    check_guardrails,
    format_entryways_text,
    format_guardrails_human,
    get_blessed_entryways,
)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="HFO memory guardrails (SSOT-only)")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    ap.add_argument(
        "--entryways",
        action="store_true",
        help="Print blessed entryways (how to do it right) and exit",
    )
    ap.add_argument(
        "--allow-shodh-mcp",
        action="store_true",
        help="Allow HFO_MCP_ENABLE_SHODH_MEMORY=1 (normally blocked to avoid multi-backend confusion)",
    )
    args = ap.parse_args(argv)

    repo_root = _REPO_ROOT

    if args.entryways:
        entryways = get_blessed_entryways(repo_root=repo_root, environ=os.environ)
        print(format_entryways_text(entryways))
        return 0

    payload = check_guardrails(
        repo_root=repo_root,
        allow_shodh_mcp=bool(args.allow_shodh_mcp),
        environ=os.environ,
    )

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(format_guardrails_human(payload))

    return 0 if payload.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv[1:]))
