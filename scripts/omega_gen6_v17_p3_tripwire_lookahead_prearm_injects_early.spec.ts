// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V17_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { P3TripwireInjectV1Schema, TripwireLookaheadV1Schema, TripwireCrossV15Schema } from '../contracts/hfo_tripwire_events.zod';

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6 v17: tripwire lookahead pre-arms P3 and injects earlier than crossing', async ({ hfoPage }) => {
  const lookaheadWindowMs = 200;

  const url = `${GEN6_V17_TEST_URL_LIGHT}`
    + `&flag-p2-tripwire-lookahead=true`
    + `&flag-p3-tripwire-lookahead=true`
    + `&flag-p2-tripwire-lookahead-window-ms=${lookaheadWindowMs}`
    + `&flag-p2-tripwire-contact-only=false`
    + `&flag-p3-injector=false`;

  const frames = fs
    .readFileSync(
      'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v17_tripwire_lookahead_slow_cross_golden.jsonl',
      'utf-8',
    )
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));

  await safeGoto(hfoPage, url);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(
    hfoPage,
    (args) => {
      const w = window as any;
      if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
      if (!w.hfoP2TripwireThread?.tick) throw new Error('missing hfoP2TripwireThread.tick');
      if (!w.hfoP3PlanckSensorInjector?.tick) throw new Error('missing hfoP3PlanckSensorInjector.tick');

      const captured: Array<{ port: string; type: string; payload: any }> = [];
      const unsub = w.hfoPortsEffects.subscribe((entry: any) => {
        if (!entry?.port) return;
        if (entry.port !== 'p2' && entry.port !== 'p3') return;
        if (entry.type !== 'tripwire_lookahead' && entry.type !== 'tripwire_cross' && entry.type !== 'tripwire_inject') return;
        captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      });

      const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };

      for (const f of args.frames) {
        const now = Number(f?.now || 0);
        const dt = Number(f?.dt || 16);
        const c = f?.cursor || {};

        dataFabric.frameId++;
        dataFabric.systemTime = now;
        dataFabric.cursors = [
          {
            ...c,
            seq: f?.seq,
            normX: c?.uiNormX,
            normY: c?.uiNormY,
          },
        ];

        w.hfoP2TripwireThread.tick({ now, dt, dataFabric });
        w.hfoP3PlanckSensorInjector.tick({ now, dt, dataFabric });
      }

      try {
        unsub();
      } catch {
        // ignore
      }

      return { captured };
    },
    { frames },
  );

  const p2Look = out.captured.filter((e: any) => e.port === 'p2' && e.type === 'tripwire_lookahead');
  const p2Cross = out.captured.filter((e: any) => e.port === 'p2' && e.type === 'tripwire_cross');
  const p3Inject = out.captured.filter((e: any) => e.port === 'p3' && e.type === 'tripwire_inject');

  expect(p2Look.length, `expected >=1 lookahead, got ${p2Look.length}`).toBeGreaterThanOrEqual(1);
  expect(p2Cross.length, `expected >=1 cross, got ${p2Cross.length}`).toBeGreaterThanOrEqual(1);
  expect(p3Inject.length, `expected >=1 inject, got ${p3Inject.length}`).toBeGreaterThanOrEqual(1);

  // Validate payload shapes (fail-closed contracts).
  TripwireLookaheadV1Schema.parse(p2Look[0].payload);
  TripwireCrossV15Schema.parse(p2Cross[0].payload);
  P3TripwireInjectV1Schema.parse(p3Inject[0].payload);

  const firstLookNow = Number(p2Look[0].payload?.now);
  const firstCrossNow = Number(p2Cross[0].payload?.now);
  const firstInjectNow = Number(p3Inject[0].payload?.now);

  expect(Number.isFinite(firstLookNow)).toBeTruthy();
  expect(Number.isFinite(firstCrossNow)).toBeTruthy();
  expect(Number.isFinite(firstInjectNow)).toBeTruthy();

  // Key invariant: injection should occur before the actual crossing.
  expect(firstInjectNow).toBeLessThanOrEqual(firstCrossNow);

  // For this fixture + window=200ms, we expect a meaningful lead time.
  const lead = firstCrossNow - firstInjectNow;
  expect(lead).toBeGreaterThanOrEqual(150);
});
