"""Medallion: Bronze | Mutation: 0% | HIVE: V

Safe normalizer for MCP working-memory ledger.

Why:
- `hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl` is treated like JSONL, but in practice
  it can contain embedded newlines and concatenated JSON objects.

What this does:
- Reads the ledger as a *JSON value stream* (concatenated JSON objects separated by arbitrary
  whitespace/newlines).
- Emits a strict JSONL shadow file (one JSON object per line) WITHOUT modifying the original.
- Emits a small receipt JSON with counts, parse errors, and sha256 hashes.

This is designed to be fail-soft: it will skip non-JSON spans and continue scanning.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Tuple


@dataclass
class ParseIssue:
    offset: int
    message: str
    context: str


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _extract_json_objects(text: str) -> Tuple[List[Any], List[ParseIssue]]:
    decoder = json.JSONDecoder()
    index = 0
    length = len(text)

    objects: List[Any] = []
    issues: List[ParseIssue] = []

    while index < length:
        # Skip whitespace
        while index < length and text[index].isspace():
            index += 1
        if index >= length:
            break

        try:
            obj, next_index = decoder.raw_decode(text, idx=index)
            objects.append(obj)
            index = next_index
            continue
        except json.JSONDecodeError as exc:
            # Fail-soft: move forward until we find a plausible start of JSON.
            context_start = max(0, index - 80)
            context_end = min(length, index + 160)
            issues.append(
                ParseIssue(
                    offset=index,
                    message=str(exc),
                    context=text[context_start:context_end].replace("\n", "\\n"),
                )
            )

            # Heuristic: advance to next '{' or '['
            next_curly = text.find("{", index + 1)
            next_square = text.find("[", index + 1)
            candidates = [c for c in [next_curly, next_square] if c != -1]
            if not candidates:
                break
            index = min(candidates)

    return objects, issues


def _write_jsonl(path: Path, objects: List[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for obj in objects:
            if not isinstance(obj, dict):
                # Preserve non-dict JSON values too, but wrap them for JSONL discipline.
                obj = {"type": "_non_object_json_value", "value": obj}
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _write_receipt(
    path: Path,
    *,
    input_path: Path,
    output_path: Path,
    input_sha256: str,
    output_sha256: str,
    objects_count: int,
    issues: List[ParseIssue],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    receipt = {
        "type": "ledger_normalization_receipt",
        "input": {
            "path": str(input_path),
            "sha256": input_sha256,
            "bytes": input_path.stat().st_size if input_path.exists() else None,
        },
        "output": {
            "path": str(output_path),
            "sha256": output_sha256,
            "bytes": output_path.stat().st_size if output_path.exists() else None,
            "objects": objects_count,
        },
        "parse_issues": [
            {"offset": i.offset, "message": i.message, "context": i.context} for i in issues[:50]
        ],
        "parse_issues_total": len(issues),
        "note": "Output is a strict JSONL shadow file. Original ledger left untouched.",
    }
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize MCP memory ledger to strict JSONL (shadow file).")
    parser.add_argument(
        "--in",
        dest="input_path",
        default="hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl",
        help="Input ledger path.",
    )
    parser.add_argument(
        "--out",
        dest="output_path",
        default="artifacts/ledger_normalization/mcp_memory.normalized.jsonl",
        help="Output strict JSONL path (shadow file).",
    )
    parser.add_argument(
        "--receipt",
        dest="receipt_path",
        default="artifacts/ledger_normalization/mcp_memory.normalized.receipt.json",
        help="Receipt JSON path.",
    )
    parser.add_argument(
        "--allow-jsonl-write",
        action="store_true",
        help=(
            "Allow writing JSONL outputs. Default is deny-by-default to enforce sqlite-only memory policy; "
            "use Doobidoo SSOT for durable writes."
        ),
    )
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    receipt_path = Path(args.receipt_path)

    if not args.allow_jsonl_write:
        raise SystemExit(
            "Refusing to write JSONL output by default (sqlite-only memory policy). "
            "Re-run with --allow-jsonl-write if you explicitly want a derived JSONL shadow file."
        )

    raw = _read_bytes(input_path)
    input_sha256 = _sha256_bytes(raw)

    text = raw.decode("utf-8", errors="replace")
    objects, issues = _extract_json_objects(text)

    _write_jsonl(output_path, objects)

    out_bytes = _read_bytes(output_path)
    output_sha256 = _sha256_bytes(out_bytes)

    _write_receipt(
        receipt_path,
        input_path=input_path,
        output_path=output_path,
        input_sha256=input_sha256,
        output_sha256=output_sha256,
        objects_count=len(objects),
        issues=issues,
    )

    print(
        json.dumps(
            {
                "input": str(input_path),
                "output": str(output_path),
                "receipt": str(receipt_path),
                "objects": len(objects),
                "parse_issues_total": len(issues),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
