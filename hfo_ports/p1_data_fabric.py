#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

P1_DATA_FABRIC_VERSION = "0.1.0"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _run_cmd(argv: list[str], timeout_sec: int = 2) -> tuple[int, str]:
    try:
        p = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        out = (p.stdout or "") + (p.stderr or "")
        return int(p.returncode), out.strip()
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"
    except FileNotFoundError:
        return 127, "NOT_FOUND"
    except Exception as e:
        return 1, f"ERROR {type(e).__name__}: {e}"


def _read_text(path: Path, max_bytes: int = 200_000) -> str:
    try:
        if not path.exists() or not path.is_file():
            return ""
        data = path.read_bytes()
        if len(data) > max_bytes:
            data = data[-max_bytes:]
        return data.decode("utf-8", errors="replace")
    except Exception:
        return ""


def _safe_size_bytes(path: Path) -> int:
    try:
        if not path.exists():
            return 0
        if path.is_file():
            return int(path.stat().st_size)
        total = 0
        for p in path.rglob("*"):
            try:
                if p.is_file():
                    total += int(p.stat().st_size)
            except Exception:
                pass
        return int(total)
    except Exception:
        return 0


def _collect_ide_snapshot(repo_root: Path) -> dict:
    snapshot: dict = {
        "type": "ide_data_fabric_snapshot",
        "version": P1_DATA_FABRIC_VERSION,
        "timestamp": _utc_now(),
        "repo_root": str(repo_root),
        "port": "p1",
        "fabric": "ide",
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        # Legacy compatibility: keep the prior type marker so existing tooling can still match.
        "legacy": {
            "type": "ide_tracer_venom_snapshot",
        },
    }

    try:
        snapshot["loadavg"] = os.getloadavg()
    except Exception:
        snapshot["loadavg"] = None

    meminfo = _read_text(Path("/proc/meminfo"), max_bytes=50_000)
    if meminfo:
        snapshot["proc_meminfo_tail"] = meminfo.splitlines()[:40]

    try:
        du = shutil.disk_usage(repo_root)
        snapshot["disk_usage_bytes"] = {
            "total": int(du.total),
            "used": int(du.used),
            "free": int(du.free),
        }
    except Exception:
        snapshot["disk_usage_bytes"] = None

    _rc, ps_cpu = _run_cmd(
        ["bash", "-lc", "ps -eo pid,ppid,comm,%cpu,%mem,rss,args --sort=-%cpu | head -n 25"],
        timeout_sec=3,
    )
    _rc, ps_rss = _run_cmd(
        ["bash", "-lc", "ps -eo pid,ppid,comm,%cpu,%mem,rss,args --sort=-rss | head -n 25"],
        timeout_sec=3,
    )
    snapshot["ps_top_cpu"] = ps_cpu.splitlines()
    snapshot["ps_top_rss"] = ps_rss.splitlines()

    _rc, code_ps = _run_cmd(
        [
            "bash",
            "-lc",
            "pgrep -af '/usr/share/code/code|/proc/self/exe --type=utility|node .*vscode|code --type' || true",
        ],
        timeout_sec=2,
    )
    snapshot["vscode_processes"] = [ln for ln in code_ps.splitlines() if ln.strip()]

    _rc, hfo_daemons = _run_cmd(
        [
            "bash",
            "-lc",
            "pgrep -af 'scripts/p5_sentinel_daemon.py|scripts/hfo_stigmergy_anchor.py|scripts/hfo_resource_shepherd_daemon.py|scripts/hfo_gitops_batcher.py' || true",
        ],
        timeout_sec=2,
    )
    snapshot["hfo_daemons"] = [ln for ln in hfo_daemons.splitlines() if ln.strip()]

    git_dir = repo_root / ".git"
    snapshot["git"] = {
        "objects_bytes_est": _safe_size_bytes(git_dir / "objects"),
        "pack_bytes_est": _safe_size_bytes(git_dir / "objects" / "pack"),
    }
    _rc, git_cfg = _run_cmd(
        [
            "bash",
            "-lc",
            "git config --local --get gc.auto || true; git config --local --get maintenance.auto || true; git config --local --get maintenance.strategy || true",
        ],
        timeout_sec=2,
    )
    snapshot["git"]["local_maintenance_config"] = git_cfg.splitlines()

    _rc, git_gc = _run_cmd(
        ["bash", "-lc", "pgrep -af '/usr/lib/git-core/git (gc|pack-objects)' || true"],
        timeout_sec=2,
    )
    snapshot["git"]["active_gc"] = [ln for ln in git_gc.splitlines() if ln.strip()]

    blackboard = repo_root / "hfo_hot_obsidian" / "hot_obsidian_blackboard.jsonl"
    mcp_mem = repo_root / "hfo_hot_obsidian" / "bronze" / "3_resources" / "memory" / "mcp_memory.jsonl"
    snapshot["logs"] = {
        "hot_blackboard_size_bytes": _safe_size_bytes(blackboard),
        "mcp_memory_size_bytes": _safe_size_bytes(mcp_mem),
    }

    _rc, dmesg_tail = _run_cmd(["bash", "-lc", "dmesg -T 2>/dev/null | tail -n 40 || true"], timeout_sec=2)
    if dmesg_tail and dmesg_tail != "NOT_FOUND":
        snapshot["dmesg_tail"] = dmesg_tail.splitlines()

    return snapshot


def _emit_ide_snapshot(repo_root: Path) -> tuple[dict, Path]:
    snap = _collect_ide_snapshot(repo_root)
    out_dir = repo_root / "hfo_hot_obsidian" / "bronze" / "3_resources" / "telemetry"
    out_dir.mkdir(parents=True, exist_ok=True)
    # Keep the legacy filename for continuity across tools and reports.
    out_path = out_dir / "ide_tracer_venom.jsonl"
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(snap, ensure_ascii=False) + "\n")
    return snap, out_path


def run(argv: list[str], repo_root: Path) -> int:
    sub = argv[0].lower() if argv else ""
    if sub not in {"data_fabric", "fabric"}:
        print("Usage: python3 hfo_hub.py p1 data_fabric ide")
        return 2

    mode = argv[1].lower() if len(argv) > 1 else ""
    if mode in {"ide", "ide_fabric", "vscode", "chromebook"}:
        snap, out_path = _emit_ide_snapshot(repo_root)
        print("[HFO HUB] P1 data_fabric: IDE snapshot written")
        print(f"  path: {out_path}")
        print("  headline:")
        loadavg = snap.get("loadavg")
        if loadavg:
            print(f"    loadavg: {loadavg}")
        logs = snap.get("logs", {})
        if isinstance(logs, dict):
            print(
                "    logs: hot_blackboard=%sB mcp_memory=%sB"
                % (logs.get("hot_blackboard_size_bytes"), logs.get("mcp_memory_size_bytes"))
            )
        git = snap.get("git", {})
        if isinstance(git, dict):
            print(
                "    git: objects≈%sB pack≈%sB active_gc=%s"
                % (git.get("objects_bytes_est"), git.get("pack_bytes_est"), len(git.get("active_gc") or []))
            )
        daemons = snap.get("hfo_daemons") or []
        if isinstance(daemons, list):
            print(f"    hfo_daemons: {len(daemons)}")
        return 0

    print("Usage: python3 hfo_hub.py p1 data_fabric ide")
    return 2
