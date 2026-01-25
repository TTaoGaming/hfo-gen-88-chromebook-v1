#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""RED TDD: Port 0 Context Facade (Baton) contract.

Goal:
- An agent calls the hub once (Port 0), waits up to a time budget, and receives exactly
  one compact JSON baton that is grounded (tool evidence included) and fail-closed.

This test is intentionally RED until Port 0 exposes an `observe` (or similar) action
that produces a structured baton matching the assertions below.

Run:
  python3 scripts/p0_port0_context_facade_baton_red_test.py
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
    env["HFO_BATON_BUDGET_CHARS"] = "1500"
    if env_overrides:
        for k, v in env_overrides.items():
            if v is None:
                env.pop(str(k), None)
            else:
                env[str(k)] = str(v)

    proc = subprocess.run(
        [sys.executable, str(HUB), "--baton", "--baton-budget-chars", "1500", *args],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestP0ContextFacadeBatonContract(unittest.TestCase):
    def test_p0_observe_returns_grounded_single_baton(self) -> None:
        """Contract: `p0 observe` returns a single JSON baton with grounded evidence.

        Desired CLI (future):
          python3 hfo_hub.py --baton p0 observe --query "..." --time-budget-ms 2500 --free-first

        Required baton fields (future):
          - schema == "hfo.baton.v1" (or compatible)
          - port == "p0"
          - action == "observe"
          - status in {"OK","FAIL"}
          - time_budget_ms == 2500
          - request.query echoed
          - tool_results[] with explicit ok/fail and evidence URLs/paths
          - failures[] populated if any tool failed (no silent partial success)
          - stdout MUST be ONLY the baton JSON (no raw logs)
        """

        time_budget_ms = 2500
        rc, out, err = _run_hub_baton(
            [
                "p0",
                "observe",
                "--query",
                "ping",
                "--time-budget-ms",
                str(time_budget_ms),
                "--free-first",
                "--stub-tools",
            ],
            timeout_sec=6.0,
        )

        # This is a RED test: once implemented, Port 0 should succeed.
        self.assertEqual(
            rc,
            0,
            msg=(
                "Expected Port 0 observe to succeed (RED until implemented).\n"
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
        self.assertEqual(baton.get("port"), "p0")
        self.assertEqual(baton.get("action"), "observe")
        self.assertIn(baton.get("status"), {"OK", "FAIL"})

        # Time budget is part of the façade contract.
        self.assertEqual(baton.get("time_budget_ms"), time_budget_ms)
        self.assertIsInstance(baton.get("duration_ms"), int)
        self.assertLessEqual(
            baton.get("duration_ms"),
            time_budget_ms,
            "Port 0 must respect the time budget (fail-closed if exceeded)",
        )

        # Request echo prevents hallucinated scope.
        req = baton.get("request")
        self.assertIsInstance(req, dict)
        self.assertEqual(req.get("query"), "ping")
        self.assertEqual(req.get("mode"), "free-first")

        # Grounded tool evidence.
        tool_results = baton.get("tool_results")
        self.assertIsInstance(tool_results, list)
        self.assertGreaterEqual(len(tool_results), 2)

        for tr in tool_results:
            self.assertIsInstance(tr, dict)
            self.assertIn(tr.get("tool"), {"brave-search", "tavily", "filesystem", "time"})
            self.assertIn(tr.get("ok"), {True, False})
            evidence = tr.get("evidence")
            self.assertIsInstance(evidence, list)
            # At least one evidence anchor per tool result.
            self.assertGreaterEqual(len(evidence), 1)

        # Failures must be explicit.
        failures = baton.get("failures")
        self.assertIsInstance(failures, list)

    def test_p0_observe_fail_closed_no_phantom_tools_when_keys_missing(self) -> None:
        """Contract: if keys are missing, Port 0 must FAIL with explicit failures.

        - Must not claim Tavily was used when TAVILY_API_KEY is missing.
        - Must include a brave-search tool_result with ok=false and a failure explaining missing key.
        - Must still output exactly one baton JSON (no raw logs).
        """

        rc, out, err = _run_hub_baton(
            [
                "p0",
                "observe",
                "--query",
                "ping",
                "--time-budget-ms",
                "1500",
                "--free-first",
                "--no-paid",
            ],
            timeout_sec=6.0,
            env_overrides={
                "BRAVE_API_KEY": "",
                "TAVILY_API_KEY": "",
            },
        )

        self.assertNotEqual(rc, 0, "Expected FAIL when keys are missing")
        self.assertTrue(out.strip().startswith("{"), "stdout must be JSON baton")
        self.assertEqual(err.strip(), "", "stderr must be empty for a clean baton contract")

        baton = json.loads(out)
        self.assertEqual(baton.get("schema"), "hfo.baton.v1")
        self.assertEqual(baton.get("port"), "p0")
        self.assertEqual(baton.get("action"), "observe")
        self.assertEqual(baton.get("status"), "FAIL")

        failures = baton.get("failures")
        self.assertIsInstance(failures, list)
        self.assertGreaterEqual(len(failures), 1)

        tools = baton.get("tool_results")
        self.assertIsInstance(tools, list)
        tool_names = [t.get("tool") for t in tools if isinstance(t, dict)]
        self.assertIn("brave-search", tool_names)
        self.assertNotIn("tavily", tool_names, "No-paid + missing key must not claim Tavily usage")

        brave_entries = [t for t in tools if isinstance(t, dict) and t.get("tool") == "brave-search"]
        self.assertGreaterEqual(len(brave_entries), 1)
        self.assertEqual(brave_entries[0].get("ok"), False)


if __name__ == "__main__":
    unittest.main()
