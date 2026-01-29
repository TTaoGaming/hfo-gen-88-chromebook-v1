#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

"""Shodh recall CLI (derived memory view).

This is a lightweight smoke-test + operator tool to query Shodh directly over HTTP.
It complements:
- Shodh server: scripts/shodh_memory_server.sh
- SSOT → Shodh sync: scripts/shodh_sync_from_doobidoo_ssot.py

Example:
  bash scripts/mcp_env_wrap.sh ./.venv/bin/python scripts/hfo_shodh_recall.py \
    --query "timeline of 2025" --limit 8
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import requests


def _shodh_base_url() -> str:
    host = os.getenv("SHODH_HOST", "127.0.0.1").strip() or "127.0.0.1"
    port = os.getenv("SHODH_PORT", "3030").strip() or "3030"
    return f"http://{host}:{port}"


def _extract_header(content: str) -> dict[str, Any] | None:
    lines = content.splitlines()
    if len(lines) < 2:
        return None
    if lines[0].strip() != "[HFO_DERIVED_VIEW]":
        return None
    try:
        header = json.loads(lines[1])
        return header if isinstance(header, dict) else None
    except Exception:
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Query Shodh /api/recall")
    ap.add_argument("--query", required=True, help="Natural language query")
    ap.add_argument("--limit", type=int, default=8, help="Max results")
    ap.add_argument(
        "--mode",
        default="hybrid",
        choices=["semantic", "associative", "hybrid"],
        help="Retrieval mode",
    )
    ap.add_argument(
        "--user-id",
        default=os.getenv("SHODH_USER_ID", "hfo_gen88_v4"),
        help="Shodh user_id namespace",
    )
    ap.add_argument("--timeout-sec", type=float, default=60.0)
    ap.add_argument(
        "--max-preview-chars",
        type=int,
        default=240,
        help="Preview chars from the content body (0 disables)",
    )

    args = ap.parse_args(argv)

    base = _shodh_base_url()
    dotenv_path = Path(__file__).resolve().parent.parent / ".env"
    dotenv_text = ""
    if dotenv_path.exists():
        dotenv_text = dotenv_path.read_text(encoding="utf-8", errors="ignore")

    def _dotenv_get(key: str) -> str:
        for raw in dotenv_text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == key:
                return v.strip().strip('"').strip("'")
        return ""

    api_key = (
        os.getenv("SHODH_API_KEY", "").strip()
        or os.getenv("SHODH_DEV_API_KEY", "").strip()
        or _dotenv_get("SHODH_API_KEY").strip()
        or _dotenv_get("SHODH_DEV_API_KEY").strip()
    )

    url = f"{base.rstrip('/')}/api/recall"
    payload = {
        "user_id": str(args.user_id),
        "query": str(args.query),
        "limit": int(args.limit),
        "mode": str(args.mode),
    }

    headers = {"X-API-Key": api_key} if api_key else {}
    resp = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=max(1.0, float(args.timeout_sec)),
    )
    if resp.status_code in (401, 403) and not api_key:
        print(
            "ERROR: Shodh rejected the request (401/403). This Shodh server appears to require an API key; set SHODH_API_KEY (or SHODH_DEV_API_KEY) or reconfigure Shodh to allow unauthenticated local access.",
            flush=True,
        )
        return 2
    resp.raise_for_status()

    obj = resp.json()
    memories = obj.get("memories", [])

    print(
        json.dumps(
            {"query": args.query, "hits": len(memories), "shodh_url": base}, indent=2
        )
    )

    for i, mem in enumerate(memories, start=1):
        content = (mem.get("experience") or {}).get("content") or ""
        header = _extract_header(str(content)) or {}
        source_path = (
            (header.get("metadata") or {})
            if isinstance(header.get("metadata"), dict)
            else {}
        ).get("source_path")
        content_hash = header.get("content_hash")

        body = str(content)
        if header:
            # Skip header (first 2 lines) for preview.
            body = "\n".join(body.splitlines()[2:]).strip()

        preview = ""
        if int(args.max_preview_chars) > 0:
            preview = body[: int(args.max_preview_chars)].replace("\n", " ").strip()

        print(f"\n[{i}] source_path={source_path}")
        print(f"    content_hash={content_hash}")
        if preview:
            print(f"    preview={preview}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
