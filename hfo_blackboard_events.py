#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V
"""Blackboard event emission helpers.

Goal: append-only, audit-friendly events into the hot Obsidian blackboard JSONL
while preserving the existing chained-signature + chronology invariants enforced
by `scripts/blackboard_purity.py`.

This module intentionally has no external dependencies.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

DEFAULT_BLACKBOARD_REL = "hfo_hot_obsidian/hot_obsidian_blackboard.jsonl"
DEFAULT_SECRET_REL = ".hfo_secret"
DEFAULT_SECRET_FALLBACK = "HFO_DEFAULT_SECRET"


def _repo_root() -> Path:
    return Path(__file__).resolve().parent


def _blackboard_path() -> Path:
    return _repo_root() / DEFAULT_BLACKBOARD_REL


def _secret_path() -> Path:
    return _repo_root() / DEFAULT_SECRET_REL


def _iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _iso_utc_now() -> str:
    return _iso_utc(datetime.now(timezone.utc))


def _parse_ts(ts: str) -> datetime | None:
    if not ts:
        return None
    s = str(ts).strip()
    # Some historical lines have "+00:00Z" (invalid); normalize.
    if s.endswith("Z") and ("+" in s[10:] or "-" in s[10:]):
        # Strip trailing Z; offset already present.
        s = s[:-1]
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except Exception:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _read_last_json_line(fh) -> dict[str, Any] | None:
    # Caller must hold an exclusive lock.
    try:
        fh.seek(0, os.SEEK_END)
        size = fh.tell()
        if size <= 0:
            return None

        # Read a tail chunk; expand a bit vs old 4096 to be safer.
        seek_pos = max(0, size - 16384)
        fh.seek(seek_pos)
        chunk = fh.read()
        if isinstance(chunk, bytes):
            chunk = chunk.decode("utf-8", errors="ignore")

        lines = [ln for ln in str(chunk).splitlines() if ln.strip()]
        if not lines:
            return None

        # If we started mid-line, the first split may be partial; prefer last.
        last = lines[-1].strip()
        return json.loads(last)
    except Exception:
        return None


def _read_secret() -> str:
    env_secret = os.environ.get("HFO_BLACKBOARD_SECRET")
    if env_secret and str(env_secret).strip():
        return str(env_secret).strip()
    try:
        sp = _secret_path()
        if sp.exists():
            return sp.read_text(encoding="utf-8").strip() or DEFAULT_SECRET_FALLBACK
    except Exception:
        pass
    return DEFAULT_SECRET_FALLBACK


def append_signed_entry(entry: dict[str, Any], *, blackboard_path: Path | None = None) -> dict[str, Any]:
    """Append a JSON object to the blackboard with a chained signature.

    This is atomic w.r.t. signature chaining: we lock the file, read last signature,
    compute signature, and append under the same lock.

    Returns the final entry (including signature) that was appended.
    """

    path = blackboard_path or _blackboard_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    secret = _read_secret()

    try:
        import fcntl
    except Exception as e:  # pragma: no cover
        raise RuntimeError("fcntl unavailable; cannot safely append") from e

    # Open in a+ so we can read tail under the same handle.
    with path.open("a+", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            last = _read_last_json_line(fh)
            last_sig = (last or {}).get("signature") or "LEGACY"
            last_ts = _parse_ts((last or {}).get("timestamp") or "")

            out = dict(entry)

            # Preserve chronology: ensure timestamp is monotonic.
            ts = _parse_ts(str(out.get("timestamp") or ""))
            if ts is None:
                ts = datetime.now(timezone.utc)
            if last_ts is not None and ts < last_ts:
                ts = last_ts + timedelta(microseconds=1)
            out["timestamp"] = _iso_utc(ts)

            # Signature computed over entry without signature.
            entry_str = json.dumps(out, sort_keys=True)
            sig = hashlib.sha256(f"{secret}:{last_sig}:{entry_str}".encode()).hexdigest()
            out["signature"] = sig

            fh.seek(0, os.SEEK_END)
            fh.write(json.dumps(out, sort_keys=True) + "\n")
            fh.flush()
            return out
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


@dataclass(frozen=True)
class TraceContext:
    trace_id: str
    span_id: str
    parent_span_id: str | None = None

    @property
    def traceparent(self) -> str:
        # W3C traceparent: version-traceid-spanid-flags
        flags = "01"
        return f"00-{self.trace_id}-{self.span_id}-{flags}"


def new_trace(*, parent: TraceContext | None = None) -> TraceContext:
    trace_id = uuid.uuid4().hex  # 32 hex chars
    span_id = uuid.uuid4().hex[:16]  # 8 bytes / 16 hex chars
    parent_span_id = parent.span_id if parent else None
    return TraceContext(trace_id=trace_id, span_id=span_id, parent_span_id=parent_span_id)


def child_span(parent: TraceContext) -> TraceContext:
    """Create a child span under the same trace id."""

    span_id = uuid.uuid4().hex[:16]
    return TraceContext(trace_id=parent.trace_id, span_id=span_id, parent_span_id=parent.span_id)


def make_cloudevent(
    *,
    event_type: str,
    source: str,
    data: dict[str, Any] | list[Any] | str | int | float | bool | None,
    subject: str | None = None,
    trace: TraceContext | None = None,
    time_utc: str | None = None,
    extensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a CloudEvents-ish envelope compatible with the HFO blackboard.

    - Uses CloudEvents 1.0 core fields.
    - Adds W3C traceparent + lightweight OpenTelemetry-ish trace ids.
    - Also includes `timestamp` for existing Chronos/purity scripts.
    """

    t = time_utc or _iso_utc_now()
    tr = trace or new_trace()

    evt: dict[str, Any] = {
        "phase": "CLOUDEVENT",
        "specversion": "1.0",
        "id": uuid.uuid4().hex,
        "source": source,
        "type": event_type,
        "time": t,
        "timestamp": t,
        "datacontenttype": "application/json",
        "subject": subject,
        "traceparent": tr.traceparent,
        "trace_id": tr.trace_id,
        "span_id": tr.span_id,
        "parent_span_id": tr.parent_span_id,
        "data": data,
    }

    # Avoid serializing None for optional CloudEvents fields.
    if evt.get("subject") is None:
        evt.pop("subject", None)

    if extensions:
        for k, v in extensions.items():
            # CloudEvents allows extension attributes.
            evt[k] = v

    return evt


def emit_cloudevent_to_blackboard(
    *,
    event_type: str,
    source: str,
    data: dict[str, Any] | list[Any] | str | int | float | bool | None,
    subject: str | None = None,
    trace: TraceContext | None = None,
    time_utc: str | None = None,
    extensions: dict[str, Any] | None = None,
    blackboard_path: Path | None = None,
) -> dict[str, Any]:
    evt = make_cloudevent(
        event_type=event_type,
        source=source,
        data=data,
        subject=subject,
        trace=trace,
        time_utc=time_utc,
        extensions=extensions,
    )
    return append_signed_entry(evt, blackboard_path=blackboard_path)
