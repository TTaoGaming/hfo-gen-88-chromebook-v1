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
    if len(sys.argv) >= 2 and sys.argv[1] in {"vision", "omega:vision", "gen5:v10_1:vision"}:
        _print_vision()
        raise SystemExit(0)

    sys.argv[0] = TARGET
    runpy.run_path(TARGET, run_name="__main__")
