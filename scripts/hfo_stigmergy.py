#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""HFO Stigmergy facade.

Purpose
- Provide a small, stable, agent-friendly CLI surface for blackboard (stigmergy)
  read/write operations.
- Enforce pointer-blessed paths + fail-closed behavior.
- Centralize auto-metadata enrichment so wrappers/scripts stay simple.

This tool intentionally avoids external dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import subprocess
import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import hfo_blackboard_events as bb

REPO_ROOT = Path(__file__).resolve().parent.parent
POINTERS_PATH = REPO_ROOT / "hfo_pointers.json"


def _die(msg: str, code: int = 2) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_pointers() -> dict[str, Any]:
    try:
        return json.loads(POINTERS_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        raise RuntimeError(f"cannot read pointers: {POINTERS_PATH}") from e


def resolve_blackboard_path() -> Path:
    data = _read_pointers()
    paths = data.get("paths") or {}
    out = str(
        paths.get("blackboard_hot_forge") or paths.get("blackboard") or ""
    ).strip()
    if not out:
        raise RuntimeError(
            "FAIL-CLOSED: cannot resolve pointer-blessed blackboard path (blackboard_hot_forge|blackboard)"
        )
    p = (REPO_ROOT / out) if not out.startswith("/") else Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("", encoding="utf-8")
    if not os.access(p, os.W_OK):
        raise RuntimeError(f"FAIL-CLOSED: blackboard not writable: {p}")
    return p


def _git(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(
            cmd, cwd=str(REPO_ROOT), stderr=subprocess.DEVNULL, text=True
        )
        return out.strip()
    except Exception:
        return ""


def _safe_env(k: str) -> str:
    return str(os.environ.get(k) or "").strip()


@dataclass(frozen=True)
class AutoMeta:
    agent_name: str
    agent_model: str
    agent_mode_id: str
    platform_os: str
    platform_arch: str
    platform_hostname: str
    repo_sha: str
    repo_branch: str
    ts_utc: str


def build_auto_meta(*, mode_id: str) -> AutoMeta:
    agent_name = _safe_env("HFO_AGENT_NAME") or _safe_env("COPILOT_AGENT") or "unknown"
    agent_model = _safe_env("HFO_AGENT_MODEL") or "unknown"

    # Best-effort host/runtime tags.
    plat_os = platform.system().lower() or "unknown"
    plat_arch = platform.machine().lower() or "unknown"

    # Hostname can be sensitive; allow explicit opt-out.
    if _safe_env("HFO_EVENT_REDACT") == "1":
        hostname = "redacted"
    else:
        hostname = socket.gethostname() or "unknown"

    sha = _git(["git", "rev-parse", "HEAD"])
    branch = _git(["git", "rev-parse", "--abbrev-ref", "HEAD"])

    return AutoMeta(
        agent_name=agent_name,
        agent_model=agent_model,
        agent_mode_id=mode_id,
        platform_os=plat_os,
        platform_arch=plat_arch,
        platform_hostname=hostname,
        repo_sha=sha,
        repo_branch=branch,
        ts_utc=_iso_utc_now(),
    )


def enrich_data(data: Any, *, meta: AutoMeta) -> Any:
    if _safe_env("HFO_EVENT_META_DISABLE") == "1":
        return data

    meta_dict = {
        "agent": {
            "name": meta.agent_name,
            "model": meta.agent_model,
            "mode_id": meta.agent_mode_id,
        },
        "platform": {
            "os": meta.platform_os,
            "arch": meta.platform_arch,
            "hostname": meta.platform_hostname,
        },
        "repo": {
            "sha": meta.repo_sha,
            "branch": meta.repo_branch,
        },
        "ts_utc": meta.ts_utc,
    }

    # Convention: if data is a dict, attach under data.meta.
    if isinstance(data, dict):
        out = dict(data)
        existing = out.get("meta")
        if isinstance(existing, dict):
            # Preserve explicit fields; meta only fills gaps.
            merged = dict(meta_dict)
            merged.update(existing)
            out["meta"] = merged
        else:
            out["meta"] = meta_dict
        return out

    # Otherwise wrap it.
    return {"value": data, "meta": meta_dict}


def _iter_last_lines(path: Path, limit: int) -> Iterable[str]:
    if limit <= 0:
        return []
    buf: deque[str] = deque(maxlen=limit)
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                buf.append(ln)
    return list(buf)


def cmd_resolve(_: argparse.Namespace) -> int:
    bb_path = resolve_blackboard_path()
    print(str(bb_path))
    return 0


def cmd_emit(args: argparse.Namespace) -> int:
    bb_path = resolve_blackboard_path()

    event_type = args.type.strip()
    source = args.source.strip()
    subject = (args.subject or "").strip() or None

    if not event_type:
        _die("Error: --type is required")
    if not source:
        _die("Error: --source is required")

    if args.data_json:
        try:
            data: Any = json.loads(args.data_json)
        except Exception as e:
            raise RuntimeError("Error: --data-json must be valid JSON") from e
    else:
        data = {}

    # Agent-friendly optional fields.
    if args.scope:
        if isinstance(data, dict):
            data.setdefault("scope", args.scope)
    if args.turn_id:
        if isinstance(data, dict):
            data.setdefault("turn_id", args.turn_id)

    meta = build_auto_meta(mode_id=args.mode_id)
    data = enrich_data(data, meta=meta)

    evt = bb.emit_cloudevent_to_blackboard(
        event_type=event_type,
        source=source,
        subject=subject,
        data=data,
        blackboard_path=bb_path,
    )

    print(json.dumps(evt, ensure_ascii=False))
    return 0


def _parse_json_line(line: str) -> dict[str, Any] | None:
    try:
        obj = json.loads(line)
    except Exception:
        return None
    if not isinstance(obj, dict):
        return None
    return obj


def cmd_tail(args: argparse.Namespace) -> int:
    bb_path = resolve_blackboard_path()
    lines = _iter_last_lines(bb_path, args.limit)

    out: list[dict[str, Any]] = []
    for ln in lines:
        obj = _parse_json_line(ln)
        if not obj:
            continue
        if args.type and str(obj.get("type") or "") != args.type:
            continue
        if args.type_prefix and not str(obj.get("type") or "").startswith(
            args.type_prefix
        ):
            continue
        if args.subject and str(obj.get("subject") or "") != args.subject:
            continue
        out.append(obj)

    if args.format == "json":
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for obj in out:
            print(json.dumps(obj, ensure_ascii=False))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    bb_path = resolve_blackboard_path()

    # Stream scan; keep bounded matches.
    matches: deque[dict[str, Any]] = deque(
        maxlen=args.limit if args.limit > 0 else None
    )

    with bb_path.open("r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            obj = _parse_json_line(ln)
            if not obj:
                continue
            if args.type and str(obj.get("type") or "") != args.type:
                continue
            if args.type_prefix and not str(obj.get("type") or "").startswith(
                args.type_prefix
            ):
                continue
            if args.subject and str(obj.get("subject") or "") != args.subject:
                continue
            matches.append(obj)

    out = list(matches)
    if args.format == "json":
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for obj in out:
            print(json.dumps(obj, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="hfo_stigmergy.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("resolve", help="Print pointer-blessed blackboard path")
    sp.set_defaults(func=cmd_resolve)

    sp = sub.add_parser(
        "emit", help="Emit a signed CloudEvent to the pointer-blessed blackboard"
    )
    sp.add_argument("--type", required=True, help="CloudEvents type")
    sp.add_argument("--source", required=True, help="CloudEvents source")
    sp.add_argument("--subject", default="", help="CloudEvents subject")
    sp.add_argument("--data-json", default="", help="Event data JSON")
    sp.add_argument(
        "--mode-id",
        default=_safe_env("HFO_MODE_ID") or "hfo-hub-stigmergy",
        help="Logical mode id",
    )
    sp.add_argument("--scope", default="", help="Optional scope field for data")
    sp.add_argument("--turn-id", default="", help="Optional turn_id field for data")
    sp.set_defaults(func=cmd_emit)

    sp = sub.add_parser(
        "tail", help="Tail N events from the blackboard (with optional filters)"
    )
    sp.add_argument("--limit", type=int, default=20)
    sp.add_argument("--type", default="")
    sp.add_argument("--type-prefix", default="")
    sp.add_argument("--subject", default="")
    sp.add_argument("--format", choices=["jsonl", "json"], default="jsonl")
    sp.set_defaults(func=cmd_tail)

    sp = sub.add_parser(
        "query", help="Query events from the blackboard (stream scan; bounded output)"
    )
    sp.add_argument("--limit", type=int, default=50)
    sp.add_argument("--type", default="")
    sp.add_argument("--type-prefix", default="")
    sp.add_argument("--subject", default="")
    sp.add_argument("--format", choices=["jsonl", "json"], default="json")
    sp.set_defaults(func=cmd_query)

    return p


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
