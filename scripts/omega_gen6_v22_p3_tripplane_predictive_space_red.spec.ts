// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { P3TripwireInjectV2Schema } from '../contracts/hfo_tripwire_events.zod';

// RED BDD: v22 should feel snappy.
// In COMMIT, a predictive lookahead should allow Space keydown to occur before the actual crossing.
// This is expected to FAIL until v22 implementation exists.

test.describe.configure({ mode: 'serial', retries: 0 });

const GEN6_URL = `${GEN6_V22_TEST_URL_LIGHT}`
  + '&flag-p2-tripwire-knuckle=true'
  + '&flag-p2-tripwire-static=false'
  + '&flag-p3-tripwire-injector-knuckle=true'
  + '&flag-p3-tripwire-injector=false'
  + '&flag-p3-tripwire-injector-static=false'
  + '&flag-ui-knuckle-tripwire-panel=false';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

test('Gen6 v22 RED: predictive Space keydown leads the crossing (COMMIT)', async ({ hfoPage }) => {
  const frames = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));

  await safeGoto(hfoPage, GEN6_URL);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(hfoPage, (framesIn) => {
    const w = window as any;
    if (!w.systemState) throw new Error('missing systemState');
    if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
    if (!w.hfoP2KnuckleTripwireThread?.tick) throw new Error('missing hfoP2KnuckleTripwireThread.tick');

    try {
      w.hfoP3PlanckSensorInjector?.start?.();
    } catch {
      // ignore
    }

    const captured: Array<{ port: string; type: string; payload: any }> = [];
    const unsub = w.hfoPortsEffects.subscribe((entry: any) => {
      if (entry?.port !== 'p2' && entry?.port !== 'p3') return;
      captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
    });

    const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };
    for (const f of framesIn) {
      dataFabric.frameId++;
      dataFabric.systemTime = Number(f?.now || 0);
      dataFabric.cursors = [
        {
          ...f.cursor,
          seq: f?.seq,
          normX: f.cursor?.uiNormX,
          normY: f.cursor?.uiNormY,
        },
      ];

      w.hfoP2KnuckleTripwireThread.tick({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });

      try {
        w.hfoP3PlanckSensorInjector?.tick?.({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
      } catch {
        // ignore
      }
    }

    try {
      unsub?.();
    } catch {
      // ignore
    }

    return { captured };
  }, frames);

  const crossings = out.captured.filter((e: any) => e?.port === 'p2' && e?.type === 'tripwire_cross');
  const beginCross = crossings.find((e: any) => e?.payload?.sensorId === 'knuckle' && e?.payload?.sensor?.phase === 'begin');
  expect(beginCross, `Expected a knuckle begin crossing; got=${JSON.stringify(crossings)}`).toBeTruthy();

  const injects = out.captured.filter((e: any) => e?.port === 'p3' && e?.type === 'tripwire_inject');
  expect(injects.length, `Expected >=1 tripwire_inject; got=${JSON.stringify(out.captured)}`).toBeGreaterThanOrEqual(1);

  for (const e of injects) {
    const parsed = P3TripwireInjectV2Schema.safeParse(e.payload);
    expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);
  }

  const keydowns = injects.filter((e: any) => String(e?.payload?.payload?.action) === 'keydown');
  expect(keydowns.length, `Expected >=1 keydown inject; got=${JSON.stringify(injects)}`).toBeGreaterThanOrEqual(1);

  // v22 expectation: first keydown should occur BEFORE the begin crossing now (predictive lookahead).
  // (This will be RED until lookahead is implemented.)
  const kdNow = Number(keydowns[0]?.payload?.now ?? NaN);
  const crossNow = Number(beginCross?.payload?.now ?? NaN);
  expect(Number.isFinite(kdNow) && Number.isFinite(crossNow)).toBe(true);
  expect(kdNow, `Expected predictive keydown now < crossing now; kdNow=${kdNow} crossNow=${crossNow}`).toBeLessThan(crossNow);
});
