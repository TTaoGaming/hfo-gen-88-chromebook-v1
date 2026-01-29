#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Sync doobidoo sqlite SSOT memories into Shodh (derived Hebbian view).

Design
- doobidoo (mcp-memory-service) sqlite_vec is the single write-path SSOT.
- Shodh is a derived, rebuildable index to support Hebbian-style retrieval/strengthening.
- Sync uses Shodh `/api/upsert` with `external_id` = `doobidoo:<content_hash>` for idempotency.

Usage
- Dry-run (no HTTP writes):
    ./.venv/bin/python scripts/shodh_sync_from_doobidoo_ssot.py --dry-run

- Sync with defaults from .env:
    ./.venv/bin/python scripts/shodh_sync_from_doobidoo_ssot.py

Env (defaults)
- MCP_MEMORY_SQLITE_PATH: doobidoo SSOT sqlite path
- SHODH_HOST / SHODH_PORT: Shodh HTTP server location
- SHODH_API_KEY: API key for `X-API-Key` header

Notes
- This script never mutates the doobidoo SSOT.
- If Shodh is wiped, re-run this sync to rebuild the derived view.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sqlite3
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import requests

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


@dataclass(frozen=True)
class DoobidooMemoryRow:
    doobidoo_id: str
    content_hash: str
    content: str
    tags_raw: Any
    memory_type: str | None
    metadata_raw: Any
    created_at_iso: str | None
    updated_at_iso: str | None
    deleted_at: Any


def _default_sqlite_path() -> str:
    env = os.getenv("MCP_MEMORY_SQLITE_PATH", "").strip()
    if env:
        return env
    try:
        from hfo_pointers import resolve_path

        return resolve_path("paths.mcp_memory_ssot_sqlite", default="")
    except Exception:
        return ""


def _default_state_path() -> str:
    env = os.getenv("HFO_SHODH_SYNC_STATE", "").strip()
    if env:
        return env
    try:
        from hfo_pointers import resolve_path

        return resolve_path("paths.shodh_sync_state_gen88_v4", default="")
    except Exception:
        return "artifacts/shodh_memory/sync_state_doobidoo_gen88_v4.json"


def _parse_iso8601(s: str) -> dt.datetime | None:
    if not s:
        return None
    s = s.strip()
    # sqlite stores both `...Z` and `...+00:00` in various implementations.
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return dt.datetime.fromisoformat(s)
    except ValueError:
        return None


def _safe_json_loads(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, (bytes, bytearray)):
        try:
            value = value.decode("utf-8")
        except Exception:
            return None
    if not isinstance(value, str):
        return None
    s = value.strip()
    if not s:
        return None
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None


def _parse_tags(tags_raw: Any) -> list[str]:
    parsed = _safe_json_loads(tags_raw)
    if isinstance(parsed, list):
        return [str(x) for x in parsed if str(x).strip()]
    if isinstance(tags_raw, str):
        # fallback: comma-separated string
        parts = [p.strip() for p in tags_raw.split(",")]
        return [p for p in parts if p]
    return []


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (bytes, bytearray)):
        try:
            return value.decode("utf-8", errors="replace")
        except Exception:
            return str(value)
    return str(value)


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    # PRAGMA table_info returns: cid, name, type, notnull, dflt_value, pk
    return {r[1] for r in rows}


def _iter_doobidoo_memories(sqlite_path: Path) -> Iterable[DoobidooMemoryRow]:
    conn = sqlite3.connect(str(sqlite_path))
    conn.row_factory = sqlite3.Row

    cols = _table_columns(conn, "memories")

    select_cols = [
        "id",
        "content_hash",
        "content",
        "tags",
        "memory_type",
        "metadata",
    ]
    if "created_at_iso" in cols:
        select_cols.append("created_at_iso")
    else:
        select_cols.append("NULL as created_at_iso")

    if "updated_at_iso" in cols:
        select_cols.append("updated_at_iso")
    else:
        select_cols.append("NULL as updated_at_iso")

    if "deleted_at" in cols:
        select_cols.append("deleted_at")
    else:
        select_cols.append("NULL as deleted_at")

    query = f"SELECT {', '.join(select_cols)} FROM memories"

    for row in conn.execute(query):
        yield DoobidooMemoryRow(
            doobidoo_id=_coerce_str(row["id"]),
            content_hash=_coerce_str(row["content_hash"]) or _coerce_str(row["id"]),
            content=_coerce_str(row["content"]),
            tags_raw=row["tags"],
            memory_type=(
                _coerce_str(row["memory_type"])
                if row["memory_type"] is not None
                else None
            ),
            metadata_raw=row["metadata"],
            created_at_iso=(
                _coerce_str(row["created_at_iso"])
                if row["created_at_iso"] is not None
                else None
            ),
            updated_at_iso=(
                _coerce_str(row["updated_at_iso"])
                if row["updated_at_iso"] is not None
                else None
            ),
            deleted_at=row["deleted_at"],
        )


def _default_shodh_url() -> str:
    host = os.getenv("SHODH_HOST", "127.0.0.1")
    port = os.getenv("SHODH_PORT", "3030")
    return f"http://{host}:{port}"


def _default_shodh_api_key() -> str:
    api_key = (
        os.getenv("SHODH_API_KEY", "").strip()
        or os.getenv("SHODH_DEV_API_KEY", "").strip()
    )
    if api_key:
        return api_key

    dotenv_path = _REPO_ROOT / ".env"
    if not dotenv_path.exists():
        return ""
    try:
        text = dotenv_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

    def get_line_value(key: str) -> str:
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == key:
                return v.strip().strip('"').strip("'")
        return ""

    return get_line_value("SHODH_API_KEY") or get_line_value("SHODH_DEV_API_KEY")


def _load_state(state_path: Path) -> dict[str, Any]:
    if not state_path.exists():
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_state(state_path: Path, state: dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _format_shodh_content(mem: DoobidooMemoryRow, *, max_content_chars: int) -> str:
    tags = _parse_tags(mem.tags_raw)
    metadata = _safe_json_loads(mem.metadata_raw)

    header = {
        "ssot": "doobidoo_sqlite_vec",
        "ssot_version": "gen88_v4",
        "doobidoo_id": mem.doobidoo_id,
        "content_hash": mem.content_hash,
        "created_at_iso": mem.created_at_iso,
        "updated_at_iso": mem.updated_at_iso,
        "memory_type": mem.memory_type,
        "tags": tags,
        "metadata": metadata,
    }

    header_json = json.dumps(header, ensure_ascii=False, sort_keys=True)
    # Keep the raw content intact after the header block, but optionally truncate
    # for Shodh (derived view) to avoid huge payloads/timeouts.
    rendered = f"[HFO_DERIVED_VIEW]\n{header_json}\n\n{mem.content}".strip() + "\n"

    if max_content_chars <= 0:
        return rendered

    if len(rendered) <= max_content_chars:
        return rendered

    kept = rendered[:max_content_chars]
    kept = kept.rstrip() + "\n\n[HFO_TRUNCATED] "
    kept += f"original_chars={len(rendered)} kept_chars={max_content_chars}\n"
    return kept


def _post_upsert(
    *,
    session: requests.Session,
    shodh_url: str,
    api_key: str,
    user_id: str,
    mem: DoobidooMemoryRow,
    changed_by: str,
    timeout_sec: float,
    max_content_chars: int,
) -> dict[str, Any]:
    tags = _parse_tags(mem.tags_raw)

    # Add stable provenance tags.
    tags = [*tags, "ssot_doobidoo", "gen88_v4", "derived_shodh"]

    payload = {
        "user_id": user_id,
        "external_id": f"doobidoo:{mem.content_hash}",
        "content": _format_shodh_content(mem, max_content_chars=max_content_chars),
        "tags": tags,
        "memory_type": mem.memory_type,
        "change_type": "content_updated",
        "changed_by": changed_by,
        "change_reason": "sync_from_doobidoo_sqlite_ssot",
    }

    headers = {"X-API-Key": api_key} if str(api_key or "").strip() else {}
    resp = session.post(
        f"{shodh_url.rstrip('/')}/api/upsert",
        headers=headers,
        json=payload,
        timeout=timeout_sec,
    )
    resp.raise_for_status()
    return resp.json()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Sync doobidoo sqlite SSOT into Shodh derived view via /api/upsert"
    )
    parser.add_argument(
        "--sqlite-path",
        default=_default_sqlite_path(),
        help="Path to doobidoo sqlite SSOT (default: MCP_MEMORY_SQLITE_PATH)",
    )
    parser.add_argument(
        "--shodh-url",
        default=_default_shodh_url(),
        help="Shodh base URL (default: http://$SHODH_HOST:$SHODH_PORT)",
    )
    parser.add_argument(
        "--shodh-api-key",
        default=_default_shodh_api_key(),
        help="Shodh API key for X-API-Key header (default: SHODH_API_KEY/SHODH_DEV_API_KEY, else .env)",
    )
    parser.add_argument(
        "--shodh-user-id",
        default=os.getenv("SHODH_USER_ID", "hfo_gen88_v4"),
        help="Shodh user_id namespace (default: SHODH_USER_ID or hfo_gen88_v4)",
    )
    parser.add_argument(
        "--state-path",
        default=_default_state_path(),
        help="Path to local sync state JSON (default: artifacts/shodh_memory/...) ",
    )
    parser.add_argument(
        "--since-iso",
        default=None,
        help="Only sync rows with updated_at_iso >= this ISO timestamp (best-effort)",
    )
    parser.add_argument("--include-deleted", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument(
        "--require-tag",
        action="append",
        default=[],
        help="Only sync memories whose tags contain this value (repeatable; all must match).",
    )
    parser.add_argument(
        "--timeout-sec",
        type=float,
        default=300.0,
        help="HTTP timeout for each /api/upsert request (default: 300)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=0,
        help="Retry count for transient HTTP failures (connection/timeouts/5xx). Default: 0",
    )
    parser.add_argument(
        "--retry-backoff-sec",
        type=float,
        default=1.0,
        help="Backoff seconds between retries (default: 1.0)",
    )
    parser.add_argument(
        "--max-content-chars",
        type=int,
        default=12000,
        help="Max chars sent to Shodh per memory (<=0 disables; default: 12000)",
    )
    parser.add_argument(
        "--sleep-ms",
        type=int,
        default=0,
        help="Sleep between upserts (ms) to reduce server load (default: 0)",
    )
    parser.add_argument(
        "--max-runtime-sec",
        type=float,
        default=0.0,
        help="Max wall-clock seconds to spend in this run (0 means no limit)",
    )
    parser.add_argument(
        "--changed-by",
        default="hfo_ssot_sync",
        help="Auditing string stored in Shodh change log",
    )

    args = parser.parse_args(argv)

    sqlite_path = Path(args.sqlite_path) if args.sqlite_path else None
    if not sqlite_path:
        print(
            "ERROR: missing --sqlite-path (or MCP_MEMORY_SQLITE_PATH)", file=sys.stderr
        )
        return 2
    if not sqlite_path.exists():
        print(f"ERROR: sqlite path does not exist: {sqlite_path}", file=sys.stderr)
        return 2

    if not args.dry_run:
        # Fail-fast: if Shodh is down, don't churn through rows with repeated connection errors.
        probe_timeout = float(args.timeout_sec)
        probe_timeout = max(5.0, min(30.0, probe_timeout))

        last_health_exc: Exception | None = None
        for attempt in range(max(0, int(args.retries)) + 1):
            try:
                health = requests.get(
                    f"{str(args.shodh_url).rstrip('/')}/health",
                    timeout=probe_timeout,
                )
                health.raise_for_status()
                last_health_exc = None
                break
            except Exception as e:
                last_health_exc = e
                if attempt >= int(args.retries):
                    break
                time.sleep(max(0.0, float(args.retry_backoff_sec)))

        if last_health_exc is not None:
            print(
                "ERROR: Shodh is not reachable. Start the 'Shodh Memory: Server (3030)' task (or check SHODH_HOST/SHODH_PORT) and retry.",
                file=sys.stderr,
            )
            print(f"ERROR: /health probe failed: {last_health_exc}", file=sys.stderr)
            return 3

    since_iso = args.since_iso
    since_dt = _parse_iso8601(since_iso) if since_iso else None

    state_path = Path(args.state_path)
    state = _load_state(state_path)
    last_synced_iso = state.get("max_updated_at_iso")
    last_synced_dt = (
        _parse_iso8601(last_synced_iso) if isinstance(last_synced_iso, str) else None
    )

    effective_since_dt = since_dt or last_synced_dt

    rows = list(_iter_doobidoo_memories(sqlite_path))

    def row_dt(r: DoobidooMemoryRow) -> dt.datetime | None:
        return _parse_iso8601(r.updated_at_iso or "") or _parse_iso8601(
            r.created_at_iso or ""
        )

    # Deterministic order: timestamp then doobidoo id.
    rows.sort(
        key=lambda r: (
            (row_dt(r) or dt.datetime.min.replace(tzinfo=dt.timezone.utc)),
            r.doobidoo_id,
        )
    )

    if not args.include_deleted:
        rows = [r for r in rows if r.deleted_at is None]

    if effective_since_dt:
        filtered: list[DoobidooMemoryRow] = []
        for r in rows:
            rdt = row_dt(r)
            if rdt is None:
                # No timestamps; conservative include.
                filtered.append(r)
                continue
            if rdt >= effective_since_dt:
                filtered.append(r)
        rows = filtered

    if args.require_tag:
        required = [t.strip() for t in args.require_tag if str(t).strip()]
        if required:
            rows = [
                r
                for r in rows
                if all(req in _parse_tags(r.tags_raw) for req in required)
            ]

    if args.limit and args.limit > 0:
        rows = rows[: args.limit]

    print(
        json.dumps(
            {
                "sqlite_path": str(sqlite_path),
                "shodh_url": args.shodh_url,
                "shodh_user_id": args.shodh_user_id,
                "dry_run": bool(args.dry_run),
                "timeout_sec": float(args.timeout_sec),
                "max_content_chars": int(args.max_content_chars),
                "rows_selected": len(rows),
                "since": (
                    effective_since_dt.isoformat() if effective_since_dt else None
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )

    if args.dry_run:
        for r in rows[: min(3, len(rows))]:
            print(
                f"DRY_RUN would upsert external_id=doobidoo:{r.content_hash} id={r.doobidoo_id}"
            )
        return 0

    session = requests.Session()

    created = 0
    updated = 0
    failed = 0
    max_dt: dt.datetime | None = last_synced_dt

    started = time.time()
    processed = 0
    stopped_early = False

    for i, r in enumerate(rows, start=1):
        if float(args.max_runtime_sec) > 0:
            elapsed = time.time() - started
            if elapsed >= float(args.max_runtime_sec):
                stopped_early = True
                break
        try:
            resp: dict[str, Any] | None = None
            last_exc: Exception | None = None

            for attempt in range(max(0, int(args.retries)) + 1):
                try:
                    resp = _post_upsert(
                        session=session,
                        shodh_url=args.shodh_url,
                        api_key=args.shodh_api_key,
                        user_id=args.shodh_user_id,
                        mem=r,
                        changed_by=args.changed_by,
                        timeout_sec=args.timeout_sec,
                        max_content_chars=args.max_content_chars,
                    )
                    last_exc = None
                    break
                except requests.exceptions.HTTPError as e:
                    last_exc = e
                    status = getattr(getattr(e, "response", None), "status_code", None)
                    if (
                        status in (401, 403)
                        and not str(args.shodh_api_key or "").strip()
                    ):
                        print(
                            "ERROR: Shodh rejected /api/upsert (401/403) and no API key was provided. Set SHODH_API_KEY (or SHODH_DEV_API_KEY) / --shodh-api-key, or reconfigure Shodh to allow unauthenticated local writes.",
                            file=sys.stderr,
                        )
                        return 2
                    is_retryable = isinstance(status, int) and status >= 500
                    if attempt >= int(args.retries) or not is_retryable:
                        break
                    time.sleep(max(0.0, float(args.retry_backoff_sec)))
                except requests.exceptions.RequestException as e:
                    last_exc = e
                    if attempt >= int(args.retries):
                        break
                    time.sleep(max(0.0, float(args.retry_backoff_sec)))

            if resp is None and last_exc is not None:
                raise last_exc

            assert resp is not None

            was_update = bool(resp.get("was_update"))
            if was_update:
                updated += 1
            else:
                created += 1

            processed += 1

            rdt = row_dt(r)
            if rdt and (max_dt is None or rdt > max_dt):
                max_dt = rdt

            if i % 25 == 0 or i == len(rows):
                print(
                    f"progress {i}/{len(rows)} created={created} updated={updated} failed={failed}",
                    file=sys.stderr,
                )
        except Exception as e:
            failed += 1
            print(
                f"ERROR upsert failed id={r.doobidoo_id} hash={r.content_hash}: {e}",
                file=sys.stderr,
            )

        if int(args.sleep_ms) > 0:
            time.sleep(int(args.sleep_ms) / 1000.0)

    # Fail-closed: only advance the incremental sync cursor when the run had no failures.
    # Otherwise we risk skipping older rows that failed earlier in the sorted stream.
    if failed == 0 and max_dt:
        state["max_updated_at_iso"] = max_dt.isoformat()
    state["last_run_at"] = dt.datetime.now(tz=dt.timezone.utc).isoformat()
    state["sqlite_path"] = str(sqlite_path)
    state["shodh_url"] = args.shodh_url
    state["shodh_user_id"] = args.shodh_user_id

    _save_state(state_path, state)

    elapsed_sec = time.time() - started

    print(
        json.dumps(
            {
                "created": created,
                "updated": updated,
                "failed": failed,
                "processed": processed,
                "stopped_early": stopped_early,
                "elapsed_sec": round(elapsed_sec, 3),
                "state_path": str(state_path),
                "max_updated_at_iso": state.get("max_updated_at_iso"),
            },
            indent=2,
            sort_keys=True,
        )
    )

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
