#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Root hub shim for HFO.

This shim provides a stable root entrypoint that forwards to the current
Hub implementation. Change the target path via HFO_HUB_TARGET to swap
versions without changing callers.
"""

import os
import runpy
import sys
from pathlib import Path

BASE = "/home/tommytai3/active/hfo_gen_88_chromebook_v_1"
DEFAULT_TARGET = os.path.join(
    BASE,
    "hfo_hot_obsidian/bronze/1_projects/alpha_mcp_gateway_hub/hfo_mcp_gateway_hub.py",
)

try:
    from hfo_pointers import resolve_target

    TARGET = resolve_target(
        env_var="HFO_HUB_TARGET",
        dotted_key="targets.mcp_gateway_impl",
        default=DEFAULT_TARGET,
    )
except Exception:
    TARGET = os.environ.get("HFO_HUB_TARGET", DEFAULT_TARGET)


def _print_vision() -> None:
    spec = "hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/GEN5_V10_HEX_MODULAR_MONOLITH_SPEC_2026_01_20.yaml"
    html = "hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v11.html"
    active = "active_hfo_omega_entrypoint.html"
    legacy = "active_omega.html"
    smoke = "scripts/hfo_gen5_version_smoke.sh"
    print(
        "\n".join(
            [
                "HFO / Active Omega — App Vision (Mission Thread OMEGA)",
                "",
                "North Star:",
                "  Total Tool Virtualization — gestures + multimodal intent manifest virtual tools,",
                "  with evaluation harness feedback and archive-backed curricula to mastery.",
                "",
                "Architecture Contract:",
                "  - Single HTML artifact (avoid dual-authority / duplicated identifiers).",
                "  - Exactly 8 ports (P0–P7) with strict responsibilities.",
                "  - New adapters are chunked by domain and registered behind tokens.",
                "  - Cross-port data is schema-enforced (Zod contracts).",
                "",
                "8 Ports (Hex):",
                "  P0 SENSE     — raw observations (camera/mediapipe or mock)",
                "  P1 FUSE      — universal DataFabric + envelope (single authority)",
                "  P2 SHAPE     — physics + rendering substrates",
                "  P3 DELIVER   — W3C-ish pointer injection",
                "  P4 DISRUPT   — suppression/feedback/stability heuristics",
                "  P5 DEFEND    — integrity checks + stable eval harness surface",
                "  P6 STORE     — telemetry export/sinks",
                "  P7 NAVIGATE  — mission orchestration + parameter hot-swap + intent manifests",
                "",
                "Source of truth:",
                f"  - Spec: {spec}",
                f"  - Active HFO Omega Entrypoint: {active}",
                f"  - Legacy pointer (compat): {legacy}",
                f"  - Baseline artifact: {html}",
                f"  - Smoke harness: {smoke}",
                "",
                "Manual test (local):",
                "  1) Start server:",
                "     python3 scripts/hfo_threaded_server.py",
                "  2) Open Active Omega (stable pointer; forwards to current baseline):",
                "     http://localhost:8889/" + active,
                "     (legacy) http://localhost:8889/" + legacy,
                "  3) Or open baseline Gen5 v11 directly (headless-safe flags):",
                "     http://localhost:8889/" + html + "?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true",
                "  3) Optional: Excalidraw overlay:",
                "     ...&flag-ui-excalidraw=true",
                "  4) Optional: P1 ports path (DataFabric+envelope):",
                "     ...&flag-p1-ports=true",
                "  5) Console helpers:",
                "     - window.hfoStartMockReplay()  (runs without camera)",
                "     - window.hfoPorts.p7.navigate.getMissionVision()",
            ]
        )
    )


try:
    from dotenv import load_dotenv

    load_dotenv(Path(BASE) / ".env", override=False)
except Exception:
    pass

if __name__ == "__main__":
    # Single blessed entryway (CLI dispatch) for Port 7 rituals.
    # Default behavior remains: forward to the active hub implementation.
    if len(sys.argv) >= 2 and sys.argv[1] in {
        "ssot",
        "SSOT",
        "memory:ssot",
        "ssot:frontdoor",
    }:
        # Single blessed entryway (SSOT facade) for memory operations.
        sys.argv[0] = "scripts/hfo_ssot.py"
        sys.argv.pop(1)
        runpy.run_path(str(Path(BASE) / "scripts/hfo_ssot.py"), run_name="__main__")
        raise SystemExit(0)

    # Compact HFO ritual recitation (non-destructive): lattice + invariants + grudges tail.
    if len(sys.argv) >= 2 and sys.argv[1] in {"ritual", "p7:ritual", "hfo:ritual"}:
        sys.argv[0] = "scripts/hfo_ritual.py"
        sys.argv.pop(1)
        runpy.run_path(str(Path(BASE) / "scripts/hfo_ritual.py"), run_name="__main__")
        raise SystemExit(0)

    if len(sys.argv) >= 2 and sys.argv[1] in {"p7:s3-turn", "p7:turn", "p7:s3"}:
        sys.argv[0] = "scripts/p7_s3_turn.py"
        sys.argv.pop(1)
        runpy.run_path(str(Path(BASE) / "scripts/p7_s3_turn.py"), run_name="__main__")
        raise SystemExit(0)

    # Quick, antifragile health check (non-destructive).
    if len(sys.argv) >= 2 and sys.argv[1] in {
        "health",
        "health:memory",
        "memory:health",
    }:
        sys.argv[0] = "scripts/hfo_memory_healthcheck.py"
        sys.argv.pop(1)
        runpy.run_path(
            str(Path(BASE) / "scripts/hfo_memory_healthcheck.py"), run_name="__main__"
        )
        raise SystemExit(0)

    # SSOT-only health (Shodh treated as optional/derived).
    if len(sys.argv) >= 2 and sys.argv[1] in {
        "health:ssot",
        "memory:health:ssot",
        "health:memory:ssot",
    }:
        sys.argv[0] = "scripts/hfo_memory_healthcheck.py"
        sys.argv.pop(1)
        sys.argv.insert(1, "--ssot-only")
        runpy.run_path(
            str(Path(BASE) / "scripts/hfo_memory_healthcheck.py"), run_name="__main__"
        )
        raise SystemExit(0)

    # Memory overview (operator-friendly): SSOT vs derived vs legacy, with guidance.
    if len(sys.argv) >= 2 and sys.argv[1] in {
        "memory:overview",
        "overview:memory",
        "memory:stores",
        "memory:list",
    }:
        sys.argv[0] = "scripts/hfo_memory_overview.py"
        sys.argv.pop(1)
        runpy.run_path(
            str(Path(BASE) / "scripts/hfo_memory_overview.py"), run_name="__main__"
        )
        raise SystemExit(0)

    # Deep SSOT-only health (includes sqlite quick_check).
    if len(sys.argv) >= 2 and sys.argv[1] in {
        "health:ssot:deep",
        "memory:health:ssot:deep",
    }:
        sys.argv[0] = "scripts/hfo_memory_healthcheck.py"
        sys.argv.pop(1)
        sys.argv.insert(1, "--deep-sqlite")
        sys.argv.insert(1, "--ssot-only")
        runpy.run_path(
            str(Path(BASE) / "scripts/hfo_memory_healthcheck.py"), run_name="__main__"
        )
        raise SystemExit(0)

    # Fail-closed memory guardrails (non-destructive).
    if len(sys.argv) >= 2 and sys.argv[1] in {
        "guardrails",
        "guardrails:memory",
        "guard:memory",
        "memory:guard",
        "memory:guardrails",
    }:
        sys.argv[0] = "scripts/hfo_memory_guardrails.py"
        sys.argv.pop(1)
        runpy.run_path(
            str(Path(BASE) / "scripts/hfo_memory_guardrails.py"), run_name="__main__"
        )
        raise SystemExit(0)

    if len(sys.argv) >= 2 and sys.argv[1] in {"p7:s3-validate", "p7:validate", "p7:s3_validate"}:
        sys.argv[0] = "scripts/s3_v2_1_validate.py"
        sys.argv.pop(1)
        runpy.run_path(str(Path(BASE) / "scripts/s3_v2_1_validate.py"), run_name="__main__")
        raise SystemExit(0)

    if len(sys.argv) >= 2 and sys.argv[1] in {"vision", "omega:vision", "gen5:v10_1:vision"}:
        _print_vision()
        raise SystemExit(0)

    # Port 6 (Kraken Keeper) — Bronze-level progressive rollup (non-destructive).
    if len(sys.argv) >= 2 and sys.argv[1] in {"p6:bronze-rollup", "p6:rollup:bronze", "p6:bronze"}:
        sys.argv[0] = "scripts/p6_bronze_progressive_rollup.py"
        sys.argv.pop(1)
        runpy.run_path(str(Path(BASE) / "scripts/p6_bronze_progressive_rollup.py"), run_name="__main__")
        raise SystemExit(0)

    # Stigmergy facade (blackboard read/write) — agent-friendly entryway.
    if len(sys.argv) >= 2 and sys.argv[1] in {
        "stigmergy",
        "stigmergy:emit",
        "stigmergy:tail",
        "stigmergy:query",
        "stigmergy:resolve",
    }:
        sys.argv[0] = "scripts/hfo_stigmergy.py"
        cmd = sys.argv.pop(1)
        # Allow both `stigmergy emit` and `stigmergy:emit` styles.
        if cmd.startswith("stigmergy:"):
            sys.argv.insert(1, cmd.split(":", 1)[1])
        runpy.run_path(
            str(Path(BASE) / "scripts/hfo_stigmergy.py"), run_name="__main__"
        )
        raise SystemExit(0)

    sys.argv[0] = TARGET
    runpy.run_path(TARGET, run_name="__main__")
