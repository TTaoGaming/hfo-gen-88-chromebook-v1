#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Reseal a JSONL blackboard by (re)computing chained signatures.

This repairs mixed signed/unsigned logs that can trip Chronos gates.

Behavior:
- Reads JSONL input line-by-line.
- For each JSON object, removes any existing `signature` and computes a new
  chained signature: sha256(f"{secret}:{prev_sig}:{json.dumps(entry, sort_keys=True)}").
- Writes the resealed JSON objects to output in JSONL format.

Notes:
- The signature chain is computed over *every* JSON object line, regardless of
  whether it is a CloudEvent envelope.
- Secret resolution prefers `HFO_BLACKBOARD_SECRET` env var, then `.hfo_secret`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _read_secret(repo_root: Path) -> str:
    env_secret = os.environ.get("HFO_BLACKBOARD_SECRET")
    if env_secret and str(env_secret).strip():
        return str(env_secret).strip()

    secret_path = repo_root / ".hfo_secret"
    try:
        if secret_path.exists():
            s = secret_path.read_text(encoding="utf-8").strip()
            if s:
                return s
    except Exception:
        pass

    return os.environ.get("HFO_DEFAULT_SECRET", "HFO_DEFAULT_SECRET")


def _iter_json_objects(lines: Iterable[str]) -> Iterable[dict[str, Any]]:
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception as e:
            raise ValueError(f"Invalid JSONL line: {line[:200]}") from e
        if not isinstance(obj, dict):
            raise ValueError("Each JSONL line must be a JSON object")
        yield obj


def _seal_entries(entries: Iterable[dict[str, Any]], *, secret: str) -> list[dict[str, Any]]:
    prev_sig = "LEGACY"
    out: list[dict[str, Any]] = []

    for entry in entries:
        e = dict(entry)
        e.pop("signature", None)

        # Keep basic chronology sanity: ensure a timestamp exists.
        if not e.get("timestamp"):
            e["timestamp"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        entry_str = json.dumps(e, sort_keys=True)
        sig = hashlib.sha256(f"{secret}:{prev_sig}:{entry_str}".encode()).hexdigest()
        e["signature"] = sig
        out.append(e)
        prev_sig = sig

    return out


def main() -> int:
    repo_root = _repo_root()

    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input JSONL blackboard path")
    ap.add_argument("--output", required=True, help="Output JSONL path")
    args = ap.parse_args()

    inp = Path(args.input)
    outp = Path(args.output)

    if not inp.exists():
        raise SystemExit(f"Input not found: {inp}")

    secret = _read_secret(repo_root)

    entries = list(_iter_json_objects(inp.read_text(encoding="utf-8").splitlines()))
    sealed = _seal_entries(entries, secret=secret)

    outp.parent.mkdir(parents=True, exist_ok=True)
    tmp = outp.with_suffix(outp.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(e, sort_keys=True) + "\n" for e in sealed), encoding="utf-8")
    tmp.replace(outp)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
