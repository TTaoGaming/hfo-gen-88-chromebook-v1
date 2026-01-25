#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Port 0 Shard Health Tracer (Baton) contract.

Goal:
- Deterministic, hallucination-adverse health check.
- Must output exactly one JSON baton on stdout (no raw logs).
- Must fail closed with explicit failures when keys are missing.

Run:
  python3 scripts/p0_port0_shard_health_tracer_contract_test.py -v
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


def _run_hub_baton(args: list[str], *, timeout_sec: float = 6.0, env_overrides: dict | None = None) -> tuple[int, str, str]:
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["HFO_BATON_BUDGET_CHARS"] = "2500"
    if env_overrides:
        for k, v in env_overrides.items():
            if v is None:
                env.pop(str(k), None)
            else:
                env[str(k)] = str(v)

    proc = subprocess.run(
        [sys.executable, str(HUB), "--baton", "--baton-budget-chars", "2500", *args],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestP0ShardHealthTracerContract(unittest.TestCase):
    def test_fail_closed_when_keys_missing(self) -> None:
        rc, out, err = _run_hub_baton(
            ["p0", "tracer", "--query", "health-check", "--time-budget-ms", "1200"],
            env_overrides={
                "BRAVE_API_KEY": "",
                "TAVILY_API_KEY": "",
                "OPENROUTER_API_KEY": "",
            },
        )

        self.assertNotEqual(rc, 0)
        self.assertTrue(out.strip().startswith("{"))
        self.assertEqual(err.strip(), "")

        baton = json.loads(out)
        self.assertEqual(baton.get("schema"), "hfo.baton.v1")
        self.assertEqual(baton.get("port"), "p0")
        self.assertEqual(baton.get("action"), "tracer")
        self.assertEqual(baton.get("status"), "FAIL")

        tools = baton.get("tool_results")
        self.assertIsInstance(tools, list)
        tool_names = [t.get("tool") for t in tools if isinstance(t, dict)]
        self.assertIn("mcp_inventory", tool_names)
        self.assertIn("pointers", tool_names)
        self.assertIn("env:BRAVE_API_KEY", tool_names)
        self.assertIn("env:TAVILY_API_KEY", tool_names)
        self.assertIn("env:OPENROUTER_API_KEY", tool_names)

        failures = baton.get("failures")
        self.assertIsInstance(failures, list)
        self.assertGreaterEqual(len(failures), 1)

        # Explicit missing keys must be represented as failures.
        failure_tools = [f.get("tool") for f in failures if isinstance(f, dict)]
        self.assertIn("env:BRAVE_API_KEY", failure_tools)
        self.assertIn("env:TAVILY_API_KEY", failure_tools)
        self.assertIn("env:OPENROUTER_API_KEY", failure_tools)


if __name__ == "__main__":
    unittest.main()
