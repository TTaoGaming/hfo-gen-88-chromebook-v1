#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
import urllib.request
import urllib.error

P3_TRACER_VENOM_VERSION = "0.1.0"


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
        "type": "ide_tracer_venom_snapshot",
        "version": P3_TRACER_VENOM_VERSION,
        "timestamp": _utc_now(),
        "repo_root": str(repo_root),
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
    }

    # Load/memory basics (best-effort).
    try:
        snapshot["loadavg"] = os.getloadavg()
    except Exception:
        snapshot["loadavg"] = None

    meminfo = _read_text(Path("/proc/meminfo"), max_bytes=50_000)
    if meminfo:
        snapshot["proc_meminfo_tail"] = meminfo.splitlines()[:40]

    # Disk usage.
    try:
        du = shutil.disk_usage(repo_root)
        snapshot["disk_usage_bytes"] = {
            "total": int(du.total),
            "used": int(du.used),
            "free": int(du.free),
        }
    except Exception:
        snapshot["disk_usage_bytes"] = None

    # Top processes (proof).
    _rc, ps_cpu = _run_cmd(["bash", "-lc", "ps -eo pid,ppid,comm,%cpu,%mem,rss,args --sort=-%cpu | head -n 25"], timeout_sec=3)
    _rc, ps_rss = _run_cmd(["bash", "-lc", "ps -eo pid,ppid,comm,%cpu,%mem,rss,args --sort=-rss | head -n 25"], timeout_sec=3)
    snapshot["ps_top_cpu"] = ps_cpu.splitlines()
    snapshot["ps_top_rss"] = ps_rss.splitlines()

    # VS Code + HFO daemons.
    _rc, code_ps = _run_cmd(["bash", "-lc", "pgrep -af '/usr/share/code/code|/proc/self/exe --type=utility|node .*vscode|code --type' || true"], timeout_sec=2)
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

    # Git maintenance pressure.
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

    # Use a strict pattern to avoid pgrep matching its own argv.
    _rc, git_gc = _run_cmd(
        ["bash", "-lc", "pgrep -af '/usr/lib/git-core/git (gc|pack-objects)' || true"],
        timeout_sec=2,
    )
    snapshot["git"]["active_gc"] = [ln for ln in git_gc.splitlines() if ln.strip()]

    # Log growth pressure indicators.
    blackboard = repo_root / "hfo_hot_obsidian" / "hot_obsidian_blackboard.jsonl"
    mcp_mem = repo_root / "hfo_hot_obsidian" / "bronze" / "3_resources" / "memory" / "mcp_memory.jsonl"
    snapshot["logs"] = {
        "hot_blackboard_size_bytes": _safe_size_bytes(blackboard),
        "mcp_memory_size_bytes": _safe_size_bytes(mcp_mem),
    }

    # OOM / kernel signal (best-effort; often blocked in containers).
    _rc, dmesg_tail = _run_cmd(["bash", "-lc", "dmesg -T 2>/dev/null | tail -n 40 || true"], timeout_sec=2)
    if dmesg_tail and dmesg_tail != "NOT_FOUND":
        snapshot["dmesg_tail"] = dmesg_tail.splitlines()

    return snapshot


def _emit_ide_snapshot(repo_root: Path) -> tuple[dict, Path]:
    snap = _collect_ide_snapshot(repo_root)
    out_dir = repo_root / "hfo_hot_obsidian" / "bronze" / "3_resources" / "telemetry"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ide_tracer_venom.jsonl"
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(snap, ensure_ascii=False) + "\n")
    return snap, out_path


def _read_mcp_servers(repo_root: Path) -> tuple[dict, str | None]:
    mcp_path = repo_root / ".vscode/mcp.json"
    if not mcp_path.exists():
        return {}, f"Missing MCP config: {mcp_path}"
    try:
        data = json.loads(mcp_path.read_text(encoding="utf-8"))
        servers = data.get("servers", {})
        if not isinstance(servers, dict):
            return {}, "Invalid MCP config: servers must be an object"
        return servers, None
    except Exception as e:
        return {}, f"Failed to parse MCP config: {e}"


def _http_json(url: str, method: str = "GET", headers: dict | None = None, body: dict | None = None, timeout_sec: int = 15) -> tuple[bool, str]:
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    data_bytes = None
    if body is not None:
        data_bytes = json.dumps(body).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data_bytes, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            return True, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"Error: {type(e).__name__}: {e}"


def run(argv: list[str], repo_root: Path) -> int:
    sub = argv[0].lower() if argv else ""
    if sub not in {"tracer", "tracer_venom", "venom"}:
        print("Usage: python3 hfo_hub.py p3 tracer [ide]")
        return 2

    # IDE/Chromebook tracer mode: proof snapshots for resource truth.
    mode = argv[1].lower() if len(argv) > 1 else ""
    if mode in {"ide", "ide_tracer", "vscode", "chromebook"}:
        print("[HFO HUB] P3 tracer: IDE snapshot is now Port 1 DataFabric (alias)")
        try:
            from hfo_ports import p1_data_fabric

            return p1_data_fabric.run(["data_fabric", "ide"], repo_root)
        except Exception as e:
            print(f"[HFO HUB] P3 tracer alias failed: {type(e).__name__}: {e}")
            # Fall back to legacy behavior.
            snap, out_path = _emit_ide_snapshot(repo_root)
            print("[HFO HUB] P3 tracer: IDE/VSCODE snapshot written (legacy)")
            print(f"  path: {out_path}")
            return 0

    servers, err = _read_mcp_servers(repo_root)
    if err:
        print(f"[HFO HUB] P3 tracer: {err}")
        return 3

    canonical_8 = [
        "filesystem",
        "memory",
        "sequential-thinking",
        "time",
        "tavily",
        "brave-search",
        "playwright",
        "hfo_mcp_gateway_hub",
    ]
    optional = ["context7", "omnisearch"]

    present = set(servers.keys())
    missing = [name for name in canonical_8 if name not in present]
    extra = sorted([name for name in present if name not in set(canonical_8) and name not in set(optional)])
    enabled_optional = sorted([name for name in optional if name in present])

    print("[HFO HUB] P3 tracer: MCP server inventory")
    print(f"  canonical_expected=8 present={len([x for x in canonical_8 if x in present])} missing={len(missing)}")
    if missing:
        print("  missing: " + ", ".join(missing))
    if enabled_optional:
        print("  optional_enabled: " + ", ".join(enabled_optional))
    if extra:
        print("  extra_enabled: " + ", ".join(extra))

    allow_optional = os.environ.get("HFO_ALLOW_OPTIONAL_MCP", "0") in {"1", "true", "TRUE"}
    drift_optional = bool(enabled_optional or extra)
    if drift_optional and not allow_optional:
        print("[HFO HUB] P3 tracer: drift detected (optional/extra MCP servers enabled)")
        print("[HFO HUB] Set HFO_ALLOW_OPTIONAL_MCP=1 to allow >8 (not recommended).")

    key_status = {
        "TAVILY_API_KEY": bool(os.environ.get("TAVILY_API_KEY")),
        "OPENROUTER_API_KEY": bool(os.environ.get("OPENROUTER_API_KEY")),
        "BRAVE_API_KEY": bool(os.environ.get("BRAVE_API_KEY")),
    }
    print("[HFO HUB] P3 tracer: key presence")
    for k in ["TAVILY_API_KEY", "OPENROUTER_API_KEY", "BRAVE_API_KEY"]:
        print(f"  {k}={'OK' if key_status[k] else 'MISSING'}")

    probe_ok = True
    print("[HFO HUB] P3 tracer: live probes")

    if key_status["TAVILY_API_KEY"]:
        ok, msg = _http_json(
            "https://api.tavily.com/search",
            method="POST",
            body={"api_key": os.environ.get("TAVILY_API_KEY"), "query": "ping", "max_results": 1},
        )
        print(f"  tavily: {'OK' if ok else 'FAIL'} ({msg})")
        probe_ok = probe_ok and ok
    else:
        print("  tavily: SKIP (missing key)")

    if key_status["OPENROUTER_API_KEY"]:
        ok, msg = _http_json(
            "https://openrouter.ai/api/v1/models",
            method="GET",
            headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
        )
        print(f"  openrouter: {'OK' if ok else 'FAIL'} ({msg})")
        probe_ok = probe_ok and ok
    else:
        print("  openrouter: SKIP (missing key)")

    if key_status["BRAVE_API_KEY"]:
        ok, msg = _http_json(
            "https://api.search.brave.com/res/v1/web/search?q=ping&count=1",
            method="GET",
            headers={"X-Subscription-Token": os.environ.get("BRAVE_API_KEY")},
        )
        print(f"  brave-search: {'OK' if ok else 'FAIL'} ({msg})")
        probe_ok = probe_ok and ok
    else:
        print("  brave-search: SKIP (missing key)")

    if missing or (drift_optional and not allow_optional) or (not all(key_status.values())) or (not probe_ok):
        print("[HFO HUB] P3 tracer: FAIL")
        return 3

    print(f"[HFO HUB] P3 tracer: OK (venom={P3_TRACER_VENOM_VERSION})")
    return 0



if __name__ == "__main__":
    raise SystemExit(run(os.sys.argv[1:], Path(__file__).resolve().parents[1]))
