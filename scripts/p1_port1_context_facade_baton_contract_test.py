#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Port 1 Context Facade (Baton) contract.

Goal:
- An agent calls the hub once (Port 1), waits up to a time budget, and receives exactly
  one compact JSON baton (no raw logs on stdout/stderr).

Run:
  python3 scripts/p1_port1_context_facade_baton_contract_test.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HUB = REPO_ROOT / "hfo_hub.py"


def _run_hub_baton(args: list[str], *, timeout_sec: float = 6.0) -> tuple[int, str, str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["HFO_BATON_BUDGET_CHARS"] = "1500"

    proc = subprocess.run(
        [sys.executable, str(HUB), "--baton", "--baton-budget-chars", "1500", *args],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestP1ContextFacadeBatonContract(unittest.TestCase):
    def test_p1_fuse_returns_single_baton(self) -> None:
        time_budget_ms = 1200
        rc, out, err = _run_hub_baton(
            [
                "p1",
                "fuse",
                "--query",
                "zod",
                "--time-budget-ms",
                str(time_budget_ms),
            ],
            timeout_sec=6.0,
        )

        self.assertEqual(
            rc,
            0,
            msg=(
                "Expected Port 1 fuse to succeed.\n"
                f"returncode={rc}\n"
                f"stdout={out[:500]}\n"
                f"stderr={err[:500]}\n"
            ),
        )

        # stdout must be only the baton JSON.
        self.assertTrue(out.strip().startswith("{"), "stdout must be JSON baton")
        self.assertEqual(err.strip(), "", "stderr must be empty for a clean baton contract")

        baton = json.loads(out)
        self.assertEqual(baton.get("schema"), "hfo.baton.v1")
        self.assertEqual(baton.get("port"), "p1")
        self.assertEqual(baton.get("action"), "fuse")
        self.assertEqual(baton.get("status"), "OK")

        self.assertEqual(baton.get("time_budget_ms"), time_budget_ms)
        self.assertIsInstance(baton.get("duration_ms"), int)
        self.assertLessEqual(baton.get("duration_ms"), time_budget_ms)

        req = baton.get("request")
        self.assertIsInstance(req, dict)
        self.assertEqual(req.get("query"), "zod")

        tool_results = baton.get("tool_results")
        self.assertIsInstance(tool_results, list)
        self.assertGreaterEqual(len(tool_results), 1)

        contracts = [t for t in tool_results if isinstance(t, dict) and t.get("tool") == "contracts"]
        self.assertEqual(len(contracts), 1)
        self.assertIn(contracts[0].get("ok"), {True, False})

        failures = baton.get("failures")
        self.assertIsInstance(failures, list)
        self.assertEqual(len(failures), 0)


if __name__ == "__main__":
    unittest.main()
