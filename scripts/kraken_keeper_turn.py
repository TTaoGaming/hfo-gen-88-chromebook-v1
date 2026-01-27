#!/usr/bin/env python3

# Medallion: Bronze | Mutation: 0% | HIVE: V
# Kraken Keeper Turn Driver
# - Vendor-agnostic behavior via:
#   - Always preflight (P6) before answer
#   - Always postflight after answer (audit)
#   - Fail-closed if grounding or auditing cannot be completed

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, List, Optional, Tuple


@dataclass
class FlightResult:
    receipt_id: str
    payload: dict


def utc_z() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def sha256_text(text: str) -> str:
    return hashlib.sha256((text or '').encode('utf-8')).hexdigest()


def run_cmd(args: list[str], timeout_sec: int = 30) -> dict:
    try:
        proc = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout_sec,
        )
        out = (proc.stdout or '').strip()
        if len(out) > 20000:
            out = out[:19900] + '\n…[truncated]'
        return {'ok': proc.returncode == 0, 'code': proc.returncode, 'out': out}
    except Exception as e:
        return {'ok': False, 'code': None, 'out': f'{type(e).__name__}: {e}'}


def build_day_snapshot(
    *,
    day: str,
    scope: str,
    preflight_receipt_id: str,
    artifacts_dir: Path,
    db_path: str,
) -> Path:
    # Interpret day as UTC window [dayT00:00:00Z, next_dayT00:00:00Z)
    dt0 = datetime.strptime(day, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    dt1 = dt0 + timedelta(days=1)
    since = dt0.strftime('%Y-%m-%d 00:00:00')
    until = dt1.strftime('%Y-%m-%d 00:00:00')

    snap_dir = artifacts_dir / 'day_snapshots'
    snap_dir.mkdir(parents=True, exist_ok=True)
    snap_path = snap_dir / f'{scope}_{day.replace("-", "")}_{preflight_receipt_id}_day_snapshot.json'

    git_summary = run_cmd(
        [
            'git',
            '--no-pager',
            'log',
            f'--since={since}',
            f'--until={until}',
            '--pretty=format:%H|%ad|%an|%s',
            '--date=iso-strict',
            '--max-count=200',
        ],
        timeout_sec=45,
    )

    git_stats = run_cmd(
        [
            'git',
            '--no-pager',
            'log',
            f'--since={since}',
            f'--until={until}',
            '--shortstat',
            '--pretty=format:',
            '--max-count=200',
        ],
        timeout_sec=45,
    )

    duckdb_section: dict[str, Any] = {'db_path': db_path, 'queries': {}, 'errors': []}
    try:
        import duckdb  # local import to avoid hard dependency in non-SSOT contexts

        con = duckdb.connect(db_path, read_only=True)
        try:
            q = (
                "SELECT timestamp, actor_id, event_type, payload "
                "FROM mission_journal "
                "WHERE timestamp >= ? AND timestamp < ? "
                "ORDER BY timestamp ASC "
                "LIMIT 200"
            )
            rows = con.execute(q, [dt0, dt1]).fetchall()
            duckdb_section['queries']['mission_journal'] = {
                'count': len(rows),
                'sample': rows[:25],
            }
        except Exception as e:
            duckdb_section['errors'].append(f'mission_journal: {type(e).__name__}: {e}')
        finally:
            con.close()
    except Exception as e:
        duckdb_section['errors'].append(f'duckdb_import_or_connect: {type(e).__name__}: {e}')

    snapshot = {
        'type': 'p6_day_snapshot',
        'ts': utc_z(),
        'scope': scope,
        'day': day,
        'window': {
            'start_z': dt0.replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
            'end_z': dt1.replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        },
        'preflight_receipt_id': preflight_receipt_id,
        'git': {
            'summary': git_summary,
            'shortstat': git_stats,
        },
        'duckdb': duckdb_section,
    }

    snap_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return snap_path


def parse_multi_json(text: str) -> List[Any]:
    decoder = json.JSONDecoder()
    idx = 0
    objs: List[Any] = []
    length = len(text)
    while idx < length:
        while idx < length and text[idx].isspace():
            idx += 1
        if idx >= length:
            break
        obj, next_idx = decoder.raw_decode(text, idx)
        objs.append(obj)
        idx = next_idx
    return objs


def extract_json_from_model_text(text: str) -> dict:
    text = (text or '').strip()
    if not text:
        raise ValueError('empty model output')

    # Prefer direct JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try code-fence JSON
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if m:
        return json.loads(m.group(1))

    # Try first {...} block
    m2 = re.search(r"(\{.*\})", text, flags=re.DOTALL)
    if m2:
        return json.loads(m2.group(1))

    raise ValueError('model output is not valid JSON')


def prune(obj: Any, depth: int = 4, max_list: int = 12, max_str: int = 2000) -> Any:
    if depth <= 0:
        return '[pruned]'
    if obj is None:
        return None
    if isinstance(obj, (bool, int, float)):
        return obj
    if isinstance(obj, str):
        if len(obj) > max_str:
            return obj[: max_str - 20] + '…[truncated]'
        return obj
    if isinstance(obj, list):
        out = [prune(x, depth - 1, max_list, max_str) for x in obj[:max_list]]
        if len(obj) > max_list:
            out.append(f'…[{len(obj) - max_list} more]')
        return out
    if isinstance(obj, dict):
        out: dict = {}
        for k, v in list(obj.items())[:50]:
            out[str(k)] = prune(v, depth - 1, max_list, max_str)
        if len(obj) > 50:
            out['…'] = f'[{len(obj) - 50} more keys]'
        return out
    return str(obj)


def write_operator_markdown(
    path: Path,
    title: str,
    body_lines: List[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = '\n'.join([f'# {title}', '', *body_lines, ''])
    path.write_text(content, encoding='utf-8')


def bronze_turn_reports_dir() -> Path:
    return Path('hfo_hot_obsidian/bronze/3_resources/reports/kraken_keeper_turns')


def summarize_capsule_for_markdown(capsule: dict) -> List[str]:
    if not isinstance(capsule, dict):
        return ['- Capsule: **missing**']

    lines: List[str] = []
    scope = str(capsule.get('scope', '')).strip() or '**unknown**'
    port = str(capsule.get('port', '')).strip() or '**unknown**'
    role = str(capsule.get('role', '')).strip() or '**unknown**'
    lines.append(f'- Capsule scope: {scope}')
    lines.append(f'- Capsule port: {port}')
    lines.append(f'- Capsule role: {role}')

    pointers = capsule.get('pointers') or {}
    if isinstance(pointers, dict):
        lines.append(f"- Pointers keys (sample): {', '.join(list(map(str, list(pointers.keys())[:8])))}")

    silver = capsule.get('silver_reports_recent')
    if isinstance(silver, list):
        lines.append(f'- Recent Silver reports (count): {len(silver)}')

    wm = capsule.get('working_memory_mcp')
    if isinstance(wm, dict):
        tail = wm.get('tail')
        lines.append(f'- MCP memory tail: {tail!r}')

    bb = capsule.get('short_term_blackboard')
    if isinstance(bb, dict):
        tail = bb.get('tail')
        lines.append(f'- Blackboard tail: {tail!r}')

    return lines


def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')


def blackboard_path() -> Path:
    return Path('hfo_hot_obsidian/hot_obsidian_blackboard.jsonl')


def emit_blackboard_event(event: dict) -> None:
    append_jsonl(blackboard_path(), event)


def emit_artifact_linkage_event(
    *,
    scope: str,
    preflight_receipt_id: str,
    postflight_receipt_id: str,
    outcome: str,
    preflight_md_path: Path,
    postflight_md_path: Path,
    packet_path: Path,
    preflight_raw_path: Path,
    postflight_raw_path: Path,
    turn_receipt_path: Optional[Path],
    exemplar_path: Optional[Path],
    day_snapshot_path: Optional[Path],
) -> None:
    emit_blackboard_event(
        {
            'phase': scope,
            'action': 'artifact_linkage',
            'preflight_receipt_id': preflight_receipt_id,
            'postflight_receipt_id': postflight_receipt_id,
            'outcome': outcome,
            'artifacts': {
                'operator_preflight_markdown_path': str(preflight_md_path),
                'operator_postflight_markdown_path': str(postflight_md_path),
                'packet_path': str(packet_path),
                'preflight_raw_path': str(preflight_raw_path),
                'postflight_raw_path': str(postflight_raw_path),
                'turn_receipt_path': str(turn_receipt_path) if turn_receipt_path else None,
                'exemplar_path': str(exemplar_path) if exemplar_path else None,
                'day_snapshot_path': str(day_snapshot_path) if day_snapshot_path else None,
            },
            'timestamp': utc_z(),
        }
    )


def run_flight(args: List[str]) -> Tuple[str, str]:
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.stdout, str(proc.returncode)


def run_preflight(scope: str, note: str, write_memory: bool, artifacts_dir: Path) -> Tuple[FlightResult, Path]:
    ts = utc_z().replace(':', '').replace('-', '')
    out_path = artifacts_dir / f'preflight_{scope}_{ts}.json'
    cmd = [
        'bash',
        'scripts/hfo_flight.sh',
        'preflight',
        '--scope',
        scope,
        '--note',
        note,
        '--write-memory',
        'true' if write_memory else 'false',
        '--out',
        str(out_path),
    ]
    stdout, code = run_flight(cmd)
    if code != '0':
        raise RuntimeError(f'preflight failed (exit={code}):\n{stdout}')

    objs = parse_multi_json(stdout)
    candidates = [o for o in objs if isinstance(o, dict) and 'receipt_id' in o]
    if not candidates:
        raise RuntimeError(f'preflight produced no receipt_id JSON object:\n{stdout}')
    payload = candidates[-1]
    receipt_id = str(payload.get('receipt_id', '')).strip()
    if len(receipt_id) < 6:
        raise RuntimeError(f'preflight receipt_id invalid: {receipt_id!r}')

    return FlightResult(receipt_id=receipt_id, payload=payload), out_path


def run_postflight(
    scope: str,
    preflight_receipt_id: str,
    summary: str,
    outcome: str,
    sources: List[str],
    changes: List[str],
    write_memory: bool,
    artifacts_dir: Path,
) -> Tuple[FlightResult, Path]:
    ts = utc_z().replace(':', '').replace('-', '')
    out_path = artifacts_dir / f'postflight_{scope}_{ts}.json'

    cmd = [
        'bash',
        'scripts/hfo_flight.sh',
        'postflight',
        '--scope',
        scope,
        '--preflight-receipt-id',
        preflight_receipt_id,
        '--summary',
        summary,
        '--outcome',
        outcome,
        '--sources',
        ','.join(sources),
        '--changes',
        ','.join(changes),
        '--write-memory',
        'true' if write_memory else 'false',
        '--out',
        str(out_path),
    ]
    stdout, code = run_flight(cmd)
    if code != '0':
        raise RuntimeError(f'postflight failed (exit={code}):\n{stdout}')

    objs = parse_multi_json(stdout)
    candidates = [o for o in objs if isinstance(o, dict) and 'receipt_id' in o]
    if not candidates:
        raise RuntimeError(f'postflight produced no receipt_id JSON object:\n{stdout}')
    payload = candidates[-1]
    receipt_id = str(payload.get('receipt_id', '')).strip()
    if len(receipt_id) < 6:
        raise RuntimeError(f'postflight receipt_id invalid: {receipt_id!r}')

    return FlightResult(receipt_id=receipt_id, payload=payload), out_path


def openrouter_chat(model: str, system: str, user: str) -> str:
    api_key = os.environ.get('OPENROUTER_API_KEY', '').strip()
    if not api_key:
        raise RuntimeError('OPENROUTER_API_KEY missing')

    import urllib.request

    req_body = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': user},
        ],
        'temperature': 0.2,
    }

    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=json.dumps(req_body).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read().decode('utf-8')
    data = json.loads(raw)
    return data['choices'][0]['message']['content']


def main() -> int:
    p = argparse.ArgumentParser(description='Kraken Keeper turn driver (fail-closed).')
    p.add_argument('--scope', default='P6')
    p.add_argument('--mode', choices=['chat', 'json'], default='chat')
    p.add_argument('--provider', choices=['manual', 'openrouter'], default='manual')
    p.add_argument('--model', default='')
    p.add_argument('--prompt', default='')
    p.add_argument('--note', default='kraken keeper turn')
    p.add_argument('--write-memory', default='true')
    p.add_argument('--write-exemplar', default='true')
    p.add_argument('--day', default='', help='Optional: YYYY-MM-DD (UTC) for day reconstruction evidence')
    p.add_argument('--db', default='hfo_gen_88_cb_v2/hfo_unified_v88.duckdb', help='DuckDB path for day snapshot')
    p.add_argument('--artifacts-dir', default='artifacts/kraken_keeper')
    p.add_argument('--print-packet', action='store_true', help='Manual mode: print the full turn packet to stdout')

    args = p.parse_args()

    scope = args.scope
    mode = args.mode
    provider = args.provider
    model = args.model.strip() or ('manual' if provider == 'manual' else 'openrouter/unspecified')
    user_prompt = (args.prompt or '').strip()
    if not user_prompt:
        print('FAIL-CLOSED: --prompt is required', file=sys.stderr)
        return 2

    write_memory = str(args.write_memory).lower() not in ('0', 'false', 'no')
    write_exemplar = str(args.write_exemplar).lower() not in ('0', 'false', 'no')

    artifacts_dir = Path(args.artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # 1) PRE-FLIGHT (must succeed)
    pre, pre_path = run_preflight(scope=scope, note=args.note, write_memory=write_memory, artifacts_dir=artifacts_dir)

    capsule = pre.payload.get('capsule', {}) if isinstance(pre.payload, dict) else {}
    capsule_pruned = prune(capsule)

    # Operator-facing report paths (Hot/Bronze, 1-page Markdown)
    preflight_md_path = bronze_turn_reports_dir() / f'{scope}_{pre.receipt_id}_preflight.md'
    postflight_md_path = bronze_turn_reports_dir() / f'{scope}_{pre.receipt_id}_postflight.md'

    agent_mode_path = Path('.github/agents/hfo-port6-kraken-keeper.agent.md')
    agent_mode_text = agent_mode_path.read_text(encoding='utf-8') if agent_mode_path.exists() else ''

    system_prompt = (
        'You are HFO Kraken Keeper (Port 6). Follow the mode spec exactly.\n'
        'Return ONLY valid JSON (no markdown).\n\n'
        + agent_mode_text
    )

    if mode == 'chat':
        # Chat mode: conversational advisor output to stdout; driver handles audit JSON + receipts.
        # We intentionally do not require the model to return JSON in this mode.
        system_prompt = (
            'You are HFO Kraken Keeper (Port 6): a calm advisor.\n'
            'Reply in plain English only (no JSON).\n'
            'Be concise but helpful. If evidence is missing, say so.\n'
            'Format constraints: 4–8 short paragraphs; include bullet points and cognitive scaffolding (headings, checklists, next-step bullets).\n\n'
            + agent_mode_text
        )

    user_packet = {
        'preflight_receipt_id': pre.receipt_id,
        'preflight_scope': scope,
        'capsule': capsule_pruned,
        'user_prompt': user_prompt,
        'operator_reports': {
            'preflight_markdown_path': str(preflight_md_path),
            'postflight_markdown_path': str(postflight_md_path),
        },
        'response_format': {
            'shape': '4–8 short paragraphs total',
            'must_include': [
                'At least one bulleted checklist',
                'A short Sources section (workspace paths/URLs) or explicitly say "unproven"',
                'A Next steps section with 2–5 bullets',
            ],
            'tone': 'human-legible, operator-first',
        },
        'required_json_response': {
            'answer': 'string (plain language)',
            'sources': ['workspace paths or URLs; if none, include "unproven"'],
            'postflight_summary': 'string (1-2 sentences)',
            'outcome': 'ok|partial|error',
            'changes': ['optional short change bullets'],
        },
        'mode': mode,
    }

    day_snapshot_path: Optional[Path] = None
    if str(args.day).strip():
        try:
            day_snapshot_path = build_day_snapshot(
                day=str(args.day).strip(),
                scope=scope,
                preflight_receipt_id=pre.receipt_id,
                artifacts_dir=artifacts_dir,
                db_path=str(args.db),
            )
            user_packet['day_reconstruction'] = {
                'day': str(args.day).strip(),
                'day_snapshot_path': str(day_snapshot_path),
                'db_path': str(args.db),
            }
        except Exception as e:
            user_packet['day_reconstruction'] = {
                'day': str(args.day).strip(),
                'error': f'{type(e).__name__}: {e}',
                'db_path': str(args.db),
            }

    packet_ts = utc_z().replace(':', '').replace('-', '')
    packet_path = artifacts_dir / f'packet_{scope}_{packet_ts}_{pre.receipt_id}.json'
    packet_path.write_text(json.dumps(user_packet, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Write operator preflight markdown (compact)
    pre_lines: List[str] = [
        f'- ts_z: {utc_z()}',
        f'- scope: {scope}',
        f'- preflight_receipt_id: {pre.receipt_id}',
        f'- note: {args.note}',
        '',
        '## Objective',
        f'- {user_prompt}',
        '',
        '## Hydration (from capsule)',
        *summarize_capsule_for_markdown(capsule if isinstance(capsule, dict) else {}),
        '',
        '## Proof sources',
        f'- {pre_path}',
        f'- {packet_path}',
        f'- {day_snapshot_path}' if day_snapshot_path else '- day_snapshot: (not requested)',
        f'- .github/agents/hfo-port6-kraken-keeper.agent.md',
    ]
    write_operator_markdown(preflight_md_path, f'Kraken Keeper Preflight ({scope})', pre_lines)

    model_text = ''
    model_json: Optional[dict] = None

    try:
        if provider == 'openrouter':
            model_text = openrouter_chat(model=model, system=system_prompt, user=json.dumps(user_packet, ensure_ascii=False))
        else:
            print(json.dumps({'packet_path': str(packet_path)}, ensure_ascii=False))
            if args.print_packet:
                print(json.dumps(user_packet, ensure_ascii=False, indent=2))
            if mode == 'chat':
                print('Manual chat mode: open the packet file above, paste it into any model, then paste the model plain-text answer here (4–8 paragraphs, include bullets/checklists), and press Ctrl-D:')
            else:
                print('Manual JSON mode: open the packet file above, paste it into any model, then paste the model JSON response here and press Ctrl-D:')
            model_text = sys.stdin.read()

        if mode == 'chat':
            answer = (model_text or '').strip()
            if not answer:
                raise ValueError('missing chat answer')
            # In chat mode, we keep the receipt auditable but don't force the model to emit structured metadata.
            sources = [
                'hfo_pointers.json',
                'hfo_hot_obsidian/bronze/3_resources/memory/mcp_memory.jsonl',
                'hfo_hot_obsidian/hot_obsidian_blackboard.jsonl',
                str(pre_path),
                str(packet_path),
                str(preflight_md_path),
            ]
            postflight_summary = 'Chat answer delivered; operator reports written (see Hot/Bronze markdown).'
            outcome = 'ok'
            changes = ['operator_markdown_reports_written', 'chat_mode_conversational_stdout']
            model_json = None
        else:
            model_json = extract_json_from_model_text(model_text)

            answer = str(model_json.get('answer', '')).strip()
            sources = model_json.get('sources', [])
            postflight_summary = str(model_json.get('postflight_summary', '')).strip()
            outcome = str(model_json.get('outcome', 'ok')).strip() or 'ok'
            changes = model_json.get('changes', [])

            if not answer:
                raise ValueError('missing answer')
            if not isinstance(sources, list) or len(sources) < 1:
                raise ValueError('sources must be a non-empty array')
            if not postflight_summary:
                raise ValueError('missing postflight_summary')
            if outcome not in ('ok', 'partial', 'error'):
                raise ValueError('outcome must be ok|partial|error')
            if not isinstance(changes, list):
                raise ValueError('changes must be an array if present')

        # 2) POST-FLIGHT (always after answer)
        post, post_path = run_postflight(
            scope=scope,
            preflight_receipt_id=pre.receipt_id,
            summary=postflight_summary,
            outcome=outcome,
            sources=[
                *sources,
                str(pre_path),
                str(agent_mode_path),
                str(preflight_md_path),
            ],
            changes=[
                *[str(x) for x in changes if str(x).strip()],
                'operator_markdown_reports_written',
            ],
            write_memory=write_memory,
            artifacts_dir=artifacts_dir,
        )

        # Write operator postflight markdown (compact 1-page AAR)
        post_lines: List[str] = [
            f'- ts_z: {utc_z()}',
            f'- scope: {scope}',
            f'- preflight_receipt_id: {pre.receipt_id}',
            f'- postflight_receipt_id: {post.receipt_id}',
            '',
            '## Objective',
            f'- {user_prompt}',
            '',
            '## AAR',
            f'- Outcome: **{outcome}**',
            f'- Summary: {postflight_summary}',
            '',
            '## Answer (operator-facing)',
            answer,
            '',
            '## Proof sources',
            *[f'- {s}' for s in sources],
            f'- {pre_path}',
            f'- {post_path}',
            f'- {preflight_md_path}',
        ]
        write_operator_markdown(postflight_md_path, f'Kraken Keeper Postflight ({scope})', post_lines)

        turn_ts = utc_z()

        exemplar_path: Optional[Path] = None
        if write_exemplar:
            exemplar_dir = artifacts_dir / 'exemplars'
            exemplar_dir.mkdir(parents=True, exist_ok=True)
            exemplar_path = exemplar_dir / f'{scope}_{pre.receipt_id}_exemplar.json'
            exemplar_event = {
                'type': 'hfo_exemplar_event',
                'ts': turn_ts,
                'scope': scope,
                'preflight_receipt_id': pre.receipt_id,
                'postflight_receipt_id': post.receipt_id,
                'outcome': outcome,
                'prompt_sha256': sha256_text(user_prompt),
                'answer_sha256': sha256_text(answer),
                'user_prompt': user_prompt,
                'answer': answer,
                'tags': [],
                'keywords': [],
                'sources': [str(s) for s in sources],
                'artifacts': {
                    'exemplar_path': str(exemplar_path),
                    'packet_path': str(packet_path),
                    'turn_receipt_path': None,
                    'operator_preflight_markdown_path': str(preflight_md_path),
                    'operator_postflight_markdown_path': str(postflight_md_path),
                },
            }
            exemplar_path.write_text(json.dumps(exemplar_event, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        turn_receipt = {
            'type': 'kraken_keeper_turn_receipt',
            'ts': turn_ts,
            'scope': scope,
            'preflight_receipt_id': pre.receipt_id,
            'postflight_receipt_id': post.receipt_id,
            'provider': provider,
            'model': model,
            'user_prompt': user_prompt,
            'answer': answer,
            'outcome': outcome,
            'postflight_summary': postflight_summary,
            'changes': [str(x) for x in changes if str(x).strip()],
            'sources': [*sources, str(agent_mode_path)],
            'artifacts': {
                'preflight_raw_path': str(pre_path),
                'postflight_raw_path': str(post_path),
                'operator_preflight_markdown_path': str(preflight_md_path),
                'operator_postflight_markdown_path': str(postflight_md_path),
                'packet_path': str(packet_path),
                'turn_receipt_path': None,
                'exemplar_path': str(exemplar_path) if exemplar_path else None,
                'day_snapshot_path': str(day_snapshot_path) if day_snapshot_path else None,
            },
        }

        receipt_path = artifacts_dir / f'turn_{scope}_{turn_ts.replace(":", "").replace("-", "")}_{pre.receipt_id}.json'
        receipt_path.write_text(json.dumps(turn_receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        # Backfill paths now that the receipt exists
        if isinstance(turn_receipt.get('artifacts'), dict):
            turn_receipt['artifacts']['turn_receipt_path'] = str(receipt_path)
            receipt_path.write_text(json.dumps(turn_receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        if exemplar_path:
            try:
                exemplar_obj = json.loads(exemplar_path.read_text(encoding='utf-8'))
                if isinstance(exemplar_obj, dict) and isinstance(exemplar_obj.get('artifacts'), dict):
                    exemplar_obj['artifacts']['turn_receipt_path'] = str(receipt_path)
                    exemplar_path.write_text(json.dumps(exemplar_obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            except Exception:
                pass

        # Single linkage event per turn (blackboard already has preflight + postflight events)
        emit_artifact_linkage_event(
            scope=scope,
            preflight_receipt_id=pre.receipt_id,
            postflight_receipt_id=post.receipt_id,
            outcome=outcome,
            preflight_md_path=preflight_md_path,
            postflight_md_path=postflight_md_path,
            packet_path=packet_path,
            preflight_raw_path=pre_path,
            postflight_raw_path=post_path,
            turn_receipt_path=receipt_path,
            exemplar_path=exemplar_path,
            day_snapshot_path=day_snapshot_path,
        )

        if mode == 'chat':
            # Conversational stdout for operator; footer keeps it auditable.
            print(answer)
            print('\n---')
            print(f'preflight_receipt_id: {pre.receipt_id}')
            print(f'postflight_receipt_id: {post.receipt_id}')
            print(f'preflight_report: {preflight_md_path}')
            print(f'postflight_report: {postflight_md_path}')
            print(f'raw_preflight: {pre_path}')
            print(f'raw_postflight: {post_path}')
        else:
            # Final stdout envelope (auditable)
            print(json.dumps(turn_receipt, ensure_ascii=False, indent=2))
        return 0

    except Exception as e:
        # Fail-closed but still try to leave a postflight for audit.
        failure_summary = f'FAIL-CLOSED: {type(e).__name__}: {e}'
        try:
            post, post_path = run_postflight(
                scope=scope,
                preflight_receipt_id=pre.receipt_id,
                summary=failure_summary,
                outcome='error',
                sources=[str(pre_path), '.github/agents/hfo-port6-kraken-keeper.agent.md'],
                changes=['fail_closed'],
                write_memory=write_memory,
                artifacts_dir=artifacts_dir,
            )

            # Operator postflight markdown for failure (still 1 page)
            fail_lines: List[str] = [
                f'- ts_z: {utc_z()}',
                f'- scope: {scope}',
                f'- preflight_receipt_id: {pre.receipt_id}',
                f'- postflight_receipt_id: {post.receipt_id}',
                '',
                '## Objective',
                f'- {user_prompt}',
                '',
                '## AAR',
                '- Outcome: **error**',
                f'- Summary: {failure_summary}',
                '',
                '## Proof sources',
                f'- {pre_path}',
                f'- {post_path}',
                f'- .github/agents/hfo-port6-kraken-keeper.agent.md',
                f'- {preflight_md_path}',
            ]
            write_operator_markdown(postflight_md_path, f'Kraken Keeper Postflight ({scope})', fail_lines)

            # Single linkage event per turn (even for fail-closed)
            emit_artifact_linkage_event(
                scope=scope,
                preflight_receipt_id=pre.receipt_id,
                postflight_receipt_id=post.receipt_id,
                outcome='error',
                preflight_md_path=preflight_md_path,
                postflight_md_path=postflight_md_path,
                packet_path=packet_path,
                preflight_raw_path=pre_path,
                postflight_raw_path=post_path,
                turn_receipt_path=None,
                exemplar_path=None,
                day_snapshot_path=day_snapshot_path,
            )

            print(
                json.dumps(
                    {
                        'type': 'kraken_keeper_fail_closed',
                        'ts': utc_z(),
                        'preflight_receipt_id': pre.receipt_id,
                        'postflight_receipt_id': post.receipt_id,
                        'error': failure_summary,
                        'sources': [str(pre_path), str(post_path), str(preflight_md_path), str(postflight_md_path)],
                        'operator_reports': {
                            'preflight_markdown_path': str(preflight_md_path),
                            'postflight_markdown_path': str(postflight_md_path),
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 3
        except Exception as e2:
            print(
                json.dumps(
                    {
                        'type': 'kraken_keeper_fail_closed',
                        'ts': utc_z(),
                        'preflight_receipt_id': pre.receipt_id,
                        'error': failure_summary,
                        'postflight_error': f'{type(e2).__name__}: {e2}',
                        'sources': [str(pre_path)],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 4


if __name__ == '__main__':
    raise SystemExit(main())
