#!/usr/bin/env python3
# Medallion: Bronze | Mutation: 0% | HIVE: V

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

P0_CONTEXT_FACADE_VERSION = "2026-01-23T18:00:00Z"


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _emit(obj: dict) -> None:
    # Strict: Port 0 facade prints exactly one JSON object (the baton) and nothing else.
    print(json.dumps(obj, ensure_ascii=False))


def _deadline_from_budget_ms(budget_ms: int) -> float:
    return time.perf_counter() + max(0, budget_ms) / 1000.0


def _check_deadline(deadline: float) -> bool:
    return time.perf_counter() <= deadline


def _http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict | None = None,
    timeout_sec: float = 12.0,
) -> tuple[bool, dict | None, str]:
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
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                return True, json.loads(raw), f"HTTP {resp.status}"
            except Exception:
                return False, None, "Invalid JSON"
    except urllib.error.HTTPError as e:
        return False, None, f"HTTP {e.code}"
    except Exception as e:
        return False, None, f"Error: {type(e).__name__}: {e}"


def _extract_urls_from_brave(payload: dict | None) -> list[str]:
    if not isinstance(payload, dict):
        return []
    web = payload.get("web")
    if not isinstance(web, dict):
        return []
    results = web.get("results")
    if not isinstance(results, list):
        return []
    urls: list[str] = []
    for r in results:
        if not isinstance(r, dict):
            continue
        u = r.get("url")
        if isinstance(u, str) and u:
            urls.append(u)
    return urls


def _extract_urls_from_tavily(payload: dict | None) -> list[str]:
    if not isinstance(payload, dict):
        return []
    results = payload.get("results")
    if not isinstance(results, list):
        return []
    urls: list[str] = []
    for r in results:
        if not isinstance(r, dict):
            continue
        u = r.get("url")
        if isinstance(u, str) and u:
            urls.append(u)
    return urls


@dataclass(frozen=True)
class ToolResult:
    tool: str
    ok: bool
    duration_ms: int
    evidence: list[str]
    note: str


def _tool_result_dict(tr: ToolResult) -> dict:
    return {
        "tool": tr.tool,
        "ok": tr.ok,
        "duration_ms": tr.duration_ms,
        "evidence": tr.evidence,
        "note": tr.note,
    }


def run(argv: list[str], repo_root: Path) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("observe", nargs="?")
    parser.add_argument("--query", required=True)
    parser.add_argument("--time-budget-ms", type=int, default=2500)
    parser.add_argument("--free-first", action="store_true")
    parser.add_argument("--max-results", type=int, default=5)

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        baton = {
            "schema": "hfo.baton.v1",
            "port": "p0",
            "action": "observe",
            "status": "FAIL",
            "exit_code": 2,
            "started_utc": _iso_utc_now(),
            "duration_ms": 0,
            "time_budget_ms": None,
            "request": None,
            "tool_results": [],
            "failures": [
                {
                    "tool": "p0-context-facade",
                    "error": "Usage: python3 hfo_hub.py p0 observe --query <text> [--time-budget-ms N] [--free-first]",
                }
            ],
        }
        _emit(baton)
        return 2

    started_utc = _iso_utc_now()
    t0 = time.perf_counter()

    budget_ms = int(args.time_budget_ms)
    deadline = _deadline_from_budget_ms(budget_ms)

    tool_results: list[ToolResult] = []
    failures: list[dict] = []

    query = str(args.query)
    mode = "free-first" if bool(args.free_first) else "direct"

    def add_failure(tool: str, error: str) -> None:
        failures.append({"tool": tool, "error": error})

    def exceeded() -> bool:
        return not _check_deadline(deadline)

    # Shard: time
    if exceeded():
        add_failure("time", "Time budget exceeded before any tool call")

    # Shard: brave-search (free)
    brave_urls: list[str] = []
    if not failures and (args.free_first or True):
        if exceeded():
            add_failure("time", "Time budget exceeded before brave-search")
        else:
            brave_key = os.environ.get("BRAVE_API_KEY")
            if not brave_key:
                add_failure("brave-search", "Missing BRAVE_API_KEY")
                tool_results.append(ToolResult("brave-search", False, 0, [], "missing key"))
            else:
                t1 = time.perf_counter()
                q = urllib.parse.quote(query)
                url = f"https://api.search.brave.com/res/v1/web/search?q={q}&count={max(1, min(int(args.max_results), 10))}"
                ok, payload, note = _http_json(
                    url,
                    method="GET",
                    headers={"X-Subscription-Token": brave_key},
                    timeout_sec=12.0,
                )
                dt = int((time.perf_counter() - t1) * 1000)
                brave_urls = _extract_urls_from_brave(payload)
                tool_results.append(
                    ToolResult(
                        "brave-search",
                        bool(ok and brave_urls),
                        dt,
                        brave_urls[: int(args.max_results)],
                        note,
                    )
                )
                if not ok:
                    add_failure("brave-search", note)

    # Shard: tavily (paid fallback)
    tavily_urls: list[str] = []
    should_try_tavily = (not brave_urls) and (os.environ.get("TAVILY_API_KEY") is not None)
    if not failures and should_try_tavily:
        if exceeded():
            add_failure("time", "Time budget exceeded before tavily")
        else:
            tavily_key = os.environ.get("TAVILY_API_KEY")
            if not tavily_key:
                add_failure("tavily", "Missing TAVILY_API_KEY")
                tool_results.append(ToolResult("tavily", False, 0, [], "missing key"))
            else:
                t2 = time.perf_counter()
                ok, payload, note = _http_json(
                    "https://api.tavily.com/search",
                    method="POST",
                    body={"api_key": tavily_key, "query": query, "max_results": int(args.max_results)},
                    timeout_sec=12.0,
                )
                dt = int((time.perf_counter() - t2) * 1000)
                tavily_urls = _extract_urls_from_tavily(payload)
                tool_results.append(
                    ToolResult(
                        "tavily",
                        bool(ok and tavily_urls),
                        dt,
                        tavily_urls[: int(args.max_results)],
                        note,
                    )
                )
                if not ok:
                    add_failure("tavily", note)

    # Shard: filesystem (grounding anchor: repo root)
    try:
        tool_results.append(
            ToolResult(
                "filesystem",
                True,
                0,
                [str(repo_root)],
                "repo_root",
            )
        )
    except Exception as e:
        add_failure("filesystem", f"Error: {type(e).__name__}: {e}")
        tool_results.append(ToolResult("filesystem", False, 0, [], "exception"))

    duration_ms = int((time.perf_counter() - t0) * 1000)
    if duration_ms > budget_ms and not any(f.get("tool") == "time" for f in failures):
        add_failure("time", f"Time budget exceeded (duration_ms={duration_ms} > budget_ms={budget_ms})")

    ok = (len(failures) == 0) and (bool(brave_urls) or bool(tavily_urls))

    baton = {
        "schema": "hfo.baton.v1",
        "port": "p0",
        "action": "observe",
        "status": "OK" if ok else "FAIL",
        "exit_code": 0 if ok else 3,
        "started_utc": started_utc,
        "duration_ms": duration_ms,
        "time_budget_ms": budget_ms,
        "request": {
            "query": query,
            "mode": mode,
        },
        "tool_results": [_tool_result_dict(tr) for tr in tool_results],
        "failures": failures,
        "version": P0_CONTEXT_FACADE_VERSION,
    }

    _emit(baton)
    return 0 if ok else 3


if __name__ == "__main__":
    raise SystemExit(run(os.sys.argv[1:], Path(__file__).resolve().parents[1]))
