// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import { execFileSync } from 'node:child_process';

// This test is intentionally non-flaky and does not require the local server.
// It validates that healthcheck output is machine-readable and stable.

test('P5 healthcheck emits valid JSON (soft mode)', () => {
  const out = execFileSync('python3', ['scripts/hfo_healthcheck.py', '--mode=soft', '--format=json'], {
    encoding: 'utf-8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });

  const report = JSON.parse(out);

  expect(report).toHaveProperty('summary');
  expect(report).toHaveProperty('signals');
  expect(report).toHaveProperty('deps');

  expect(report.summary).toHaveProperty('fail');
  expect(report.summary).toHaveProperty('warn');

  // Counters should exist and be non-negative.
  const bb = report.signals.blackboard.counters;
  for (const key of ['jsonl_parse_errors', 'pending_signatures', 'tripwire_fails', 'timestamp_ambiguities']) {
    expect(typeof bb[key]).toBe('number');
    expect(bb[key]).toBeGreaterThanOrEqual(0);
  }
});
