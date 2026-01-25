# Medallion: Bronze | Mutation: 0% | HIVE: V

import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hfo_system_budget import get_throttle_profile, should_force_low_ram_for_playwright

_bb_child_span = None
_bb_emit = None
_bb_new_trace = None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def _read_meminfo_kb() -> dict[str, int]:
    out: dict[str, int] = {}
    try:
        for line in Path('/proc/meminfo').read_text(encoding='utf-8').splitlines():
            if ':' not in line:
                continue
            k, rest = line.split(':', 1)
            rest = rest.strip()
            parts = rest.split()
            if not parts:
                continue
            try:
                out[k] = int(parts[0])
            except ValueError:
                continue
    except Exception:
        pass
    return out


def _venv_python(repo_root: Path) -> str:
    candidate = repo_root / '.venv' / 'bin' / 'python'
    if candidate.exists():
        return str(candidate)
    return sys.executable


def _run_cmd(cmd: list[str], *, cwd: Path, env: dict[str, str], log_path: Path) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open('w', encoding='utf-8') as f:
        f.write(f"# cmd: {shlex.join(cmd)}\n")
        f.write(f"# cwd: {cwd}\n")
        f.write(f"# ts_start_utc: {_now_iso()}\n")
        f.flush()
        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            env=env,
            stdout=f,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return proc.wait()


def _emit_safe_run_event(event_type: str, *, trace: Any, payload: dict[str, Any]) -> None:
    """Best-effort emitter to hot blackboard (never blocks the runner)."""
    if not callable(_bb_emit):
        return
    try:
        _bb_emit(
            event_type=event_type,
            source="scripts/hfo_playwright_safe_run.py",
            subject="playwright",
            data=payload,
            trace=trace,
        )
    except Exception:
        return


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    # Make repo-root modules importable when executing as a script from ./scripts.
    rr = str(repo_root)
    if rr not in sys.path:
        sys.path.insert(0, rr)

    global _bb_child_span, _bb_emit, _bb_new_trace
    if _bb_emit is None:
        try:
            from hfo_blackboard_events import child_span as _bb_child_span  # type: ignore
            from hfo_blackboard_events import emit_cloudevent_to_blackboard as _bb_emit  # type: ignore
            from hfo_blackboard_events import new_trace as _bb_new_trace  # type: ignore
        except Exception:
            _bb_child_span = None
            _bb_emit = None
            _bb_new_trace = None

    trace = _bb_new_trace() if callable(_bb_new_trace) else None
    _emit_safe_run_event(
        "hfo.playwright.invoke",
        trace=trace,
        payload={"argv": sys.argv[1:], "pid": os.getpid(), "cwd": str(repo_root)},
    )

    parser = argparse.ArgumentParser(
        description=(
            'Safe Playwright runner: enforces low-RAM governance and captures proof snapshots (P1 IDE data fabric) '
            'before/after to prevent untracked exit-code-9 events.'
        )
    )
    parser.add_argument(
        '--force-low-ram',
        action='store_true',
        help='Force low-RAM mode regardless of detected total memory.',
    )
    parser.add_argument(
        '--mem-threshold-gib',
        type=float,
        default=8.0,
        help='Enable low-RAM mode when MemTotal is below this threshold (GiB). Default: 8.0',
    )
    parser.add_argument(
        '--no-tracer',
        action='store_true',
        help='Skip P1 IDE data fabric snapshots (not recommended).',
    )
    parser.add_argument(
        'playwright_args',
        nargs=argparse.REMAINDER,
        help=(
            'Arguments to pass to Playwright. If the first arg is "--", it is ignored. '
            'Example: scripts/spec.ts --project=chromium --reporter=line'
        ),
    )

    try:
        args = parser.parse_args()
    except SystemExit as e:
        code = 0
        try:
            if e.code is None:
                code = 0
            elif isinstance(e.code, int):
                code = int(e.code)
            else:
                code = int(str(e.code))
        except Exception:
            code = 1

        result_trace = _bb_child_span(trace) if trace is not None and callable(_bb_child_span) else trace
        _emit_safe_run_event(
            "hfo.playwright.result",
            trace=result_trace,
            payload={"argv": sys.argv[1:], "pid": os.getpid(), "exit_code": code, "ok": bool(code == 0)},
        )
        raise

    pw_args = list(args.playwright_args)
    if pw_args and pw_args[0] == '--':
        pw_args = pw_args[1:]

    if not pw_args:
        print('ERROR: No Playwright args provided.', file=sys.stderr)
        print('Example: python scripts/hfo_playwright_safe_run.py scripts/my.spec.ts --project=chromium', file=sys.stderr)

        result_trace = _bb_child_span(trace) if trace is not None and callable(_bb_child_span) else trace
        _emit_safe_run_event(
            "hfo.playwright.result",
            trace=result_trace,
            payload={"argv": sys.argv[1:], "pid": os.getpid(), "exit_code": 2, "ok": False},
        )
        return 2

    meminfo = _read_meminfo_kb()
    mem_total_kb = meminfo.get('MemTotal', 0)
    mem_available_kb = meminfo.get('MemAvailable', 0)

    prof = get_throttle_profile(ttl_sec=2.0)

    threshold_kb = int(args.mem_threshold_gib * 1024 * 1024)
    low_ram = bool(
        args.force_low_ram
        or should_force_low_ram_for_playwright()
        or (mem_total_kb > 0 and mem_total_kb < threshold_kb)
    )

    # Emit a richer invoke payload once decisions are known.
    invoke_trace = _bb_child_span(trace) if trace is not None and callable(_bb_child_span) else trace
    _emit_safe_run_event(
        "hfo.playwright.invoke",
        trace=invoke_trace,
        payload={
            "argv": sys.argv[1:],
            "pid": os.getpid(),
            "cwd": str(repo_root),
            "mem_total_kb": mem_total_kb,
            "mem_available_kb": mem_available_kb,
            "mem_threshold_gib": float(args.mem_threshold_gib),
            "mem_threshold_kb": threshold_kb,
            "force_low_ram_flag": bool(args.force_low_ram),
            "policy_force_low_ram": bool(should_force_low_ram_for_playwright()),
            "low_ram": bool(low_ram),
            "pareto_enabled": bool(prof.pareto_enabled),
            "throttle_level": str(prof.level),
            "sleep_multiplier": float(prof.sleep_multiplier),
            "throttle_reason": str(prof.reason),
            "cpu_count": int(prof.cpu_count),
            "loadavg": [float(prof.load1), float(prof.load5), float(prof.load15)],
            "no_tracer": bool(args.no_tracer),
            "playwright_args": pw_args,
        },
    )

    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir = repo_root / '.hfo_runtime' / 'playwright_safe_runs' / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    if low_ram:
        env['HFO_LOW_RAM'] = '1'

    vpy = _venv_python(repo_root)
    tracer_cmd = [vpy, str(repo_root / 'hfo_hub.py'), 'p1', 'data_fabric', 'ide']

    proof: dict[str, Any] = {
        'type': 'playwright_safe_run',
        'run_id': run_id,
        'ts_start_utc': _now_iso(),
        'cwd': str(repo_root),
        'mem_total_kb': mem_total_kb,
        'mem_available_kb_start': mem_available_kb,
        'pareto_enabled': prof.pareto_enabled,
        'throttle_level': prof.level,
        'sleep_multiplier': prof.sleep_multiplier,
        'throttle_reason': prof.reason,
        'cpu_count': prof.cpu_count,
        'loadavg_1': prof.load1,
        'low_ram_mode': low_ram,
        'env_overrides': {'HFO_LOW_RAM': env.get('HFO_LOW_RAM')} if low_ram else {},
        'playwright_cmd': ['npx', 'playwright', 'test', *pw_args],
        'logs': {},
    }

    if not args.no_tracer:
        pre_log = run_dir / 'p1_data_fabric_before.log'
        proof['logs']['p1_data_fabric_before'] = str(pre_log.relative_to(repo_root))
        _run_cmd(tracer_cmd, cwd=repo_root, env=env, log_path=pre_log)

    pw_log = run_dir / 'playwright.log'
    proof['logs']['playwright'] = str(pw_log.relative_to(repo_root))
    exit_code = _run_cmd(['npx', 'playwright', 'test', *pw_args], cwd=repo_root, env=env, log_path=pw_log)
    proof['exit_code'] = exit_code

    meminfo_after = _read_meminfo_kb()
    proof['mem_available_kb_end'] = meminfo_after.get('MemAvailable', 0)
    proof['ts_end_utc'] = _now_iso()

    if not args.no_tracer:
        post_log = run_dir / 'p1_data_fabric_after.log'
        proof['logs']['p1_data_fabric_after'] = str(post_log.relative_to(repo_root))
        _run_cmd(tracer_cmd, cwd=repo_root, env=env, log_path=post_log)

    telemetry_dir = repo_root / 'hfo_hot_obsidian' / 'bronze' / '3_resources' / 'telemetry'
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = telemetry_dir / 'playwright_safe_runs.jsonl'
    with jsonl_path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(proof, sort_keys=True) + '\n')

    summary_path = run_dir / 'run_summary.json'
    summary_path.write_text(json.dumps(proof, indent=2, sort_keys=True), encoding='utf-8')

    headline = f"safe_run={run_id} low_ram={int(low_ram)} exit_code={exit_code} memAvailKB_end={proof.get('mem_available_kb_end', 0)}"
    print(headline)
    print(f"telemetry: {jsonl_path}")
    print(f"run_dir: {run_dir}")

    result_trace = _bb_child_span(trace) if trace is not None and callable(_bb_child_span) else trace
    _emit_safe_run_event(
        "hfo.playwright.result",
        trace=result_trace,
        payload={
            "run_id": run_id,
            "exit_code": int(exit_code),
            "ok": bool(exit_code == 0),
            "low_ram": bool(low_ram),
            "mem_available_kb_end": int(proof.get('mem_available_kb_end', 0) or 0),
            "run_dir": str(run_dir),
            "telemetry_jsonl": str(jsonl_path),
            "summary_json": str(summary_path),
            "logs": dict(proof.get('logs') or {}),
        },
    )

    return exit_code



if __name__ == '__main__':
    raise SystemExit(main())
