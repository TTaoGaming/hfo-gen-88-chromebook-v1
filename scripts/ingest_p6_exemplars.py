#!/usr/bin/env python3

# Medallion: Bronze | Mutation: 0% | HIVE: V
# P6 Exemplars → DuckDB ingestion (Bronze→Silver bridge)
# - Reads exemplar JSON artifacts written by `scripts/kraken_keeper_turn.py`
# - Upserts them into the unified DuckDB SSOT for later querying/assimilation.

from __future__ import annotations

import argparse
import glob
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb


def utc_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class IngestResult:
    processed: int
    succeeded: int
    failed: int
    errors: list[dict[str, Any]]


def _require_str(obj: dict[str, Any], key: str) -> str:
    v = obj.get(key)
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f'missing/invalid {key}')
    return v


def ensure_schema(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS p6_exemplar_events (
            exemplar_id TEXT PRIMARY KEY,
            ts TIMESTAMP,
            scope TEXT,
            preflight_receipt_id TEXT,
            postflight_receipt_id TEXT,
            outcome TEXT,
            prompt_sha256 TEXT,
            answer_sha256 TEXT,
            tags JSON,
            keywords JSON,
            sources JSON,
            artifact_path TEXT,
            payload JSON
        )
        """
    )


def upsert_exemplar(con: duckdb.DuckDBPyConnection, event: dict[str, Any], artifact_path: str) -> None:
    exemplar_id = f"{event.get('scope','')}_{event.get('preflight_receipt_id','')}"
    con.execute(
        """
        INSERT INTO p6_exemplar_events (
            exemplar_id, ts, scope, preflight_receipt_id, postflight_receipt_id,
            outcome, prompt_sha256, answer_sha256, tags, keywords, sources,
            artifact_path, payload
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(exemplar_id) DO UPDATE SET
            ts=excluded.ts,
            scope=excluded.scope,
            preflight_receipt_id=excluded.preflight_receipt_id,
            postflight_receipt_id=excluded.postflight_receipt_id,
            outcome=excluded.outcome,
            prompt_sha256=excluded.prompt_sha256,
            answer_sha256=excluded.answer_sha256,
            tags=excluded.tags,
            keywords=excluded.keywords,
            sources=excluded.sources,
            artifact_path=excluded.artifact_path,
            payload=excluded.payload
        """,
        [
            exemplar_id,
            event.get('ts'),
            event.get('scope'),
            event.get('preflight_receipt_id'),
            event.get('postflight_receipt_id'),
            event.get('outcome'),
            event.get('prompt_sha256'),
            event.get('answer_sha256'),
            json.dumps(event.get('tags', []), ensure_ascii=False),
            json.dumps(event.get('keywords', []), ensure_ascii=False),
            json.dumps(event.get('sources', []), ensure_ascii=False),
            artifact_path,
            json.dumps(event, ensure_ascii=False),
        ],
    )


def main() -> int:
    p = argparse.ArgumentParser(description='Ingest P6 exemplar artifacts into unified DuckDB.')
    p.add_argument('--db', default='hfo_gen_88_cb_v2/hfo_unified_v88.duckdb')
    p.add_argument('--glob', dest='glob_pattern', default='artifacts/kraken_keeper/exemplars/*.json')
    p.add_argument('--receipt-out', default='artifacts/exemplar_ingest')
    p.add_argument('--dry-run', action='store_true')

    args = p.parse_args()

    paths = sorted(glob.glob(args.glob_pattern))
    errors: list[dict[str, Any]] = []

    if not paths:
        print(json.dumps({'ts': utc_z(), 'result': 'no_files', 'glob': args.glob_pattern}, ensure_ascii=False))
        return 0

    con = duckdb.connect(str(args.db))
    ensure_schema(con)

    processed = 0
    succeeded = 0

    for pth in paths:
        processed += 1
        try:
            raw = Path(pth).read_bytes()
            event = json.loads(raw.decode('utf-8'))
            if not isinstance(event, dict):
                raise ValueError('exemplar JSON must be an object')

            if event.get('type') != 'hfo_exemplar_event':
                raise ValueError('type != hfo_exemplar_event')

            _require_str(event, 'ts')
            _require_str(event, 'scope')
            _require_str(event, 'preflight_receipt_id')
            _require_str(event, 'postflight_receipt_id')
            _require_str(event, 'outcome')
            _require_str(event, 'prompt_sha256')
            _require_str(event, 'answer_sha256')

            artifact_path = pth

            if not args.dry_run:
                upsert_exemplar(con, event, artifact_path)

            succeeded += 1

        except Exception as e:
            errors.append({'path': pth, 'error': f'{type(e).__name__}: {e}'})

    con.close()

    receipt_dir = Path(args.receipt_out)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / f"p6_exemplar_ingest_{utc_z().replace(':','').replace('-','')}.receipt.json"

    receipt = {
        'type': 'p6_exemplar_ingest_receipt',
        'ts': utc_z(),
        'db': str(args.db),
        'glob': args.glob_pattern,
        'dry_run': bool(args.dry_run),
        'counts': {
            'processed': processed,
            'succeeded': succeeded,
            'failed': len(errors),
        },
        'inputs': [{'path': p, 'sha256': sha256_bytes(Path(p).read_bytes())} for p in paths[:200]],
        'errors': errors[:50],
    }

    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'ts': utc_z(), 'receipt_path': str(receipt_path), **receipt['counts']}, ensure_ascii=False))

    return 0 if not errors else 2


if __name__ == '__main__':
    raise SystemExit(main())
