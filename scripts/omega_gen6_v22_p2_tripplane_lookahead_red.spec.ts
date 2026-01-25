// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { TripplaneLookaheadV22Schema } from '../contracts/hfo_tripwire_events.zod';

// RED TDD: v22 must emit COMMIT-gated predictive lookahead events for the knuckle trip-plane.
// This is expected to FAIL until v22 implementation exists.

test.describe.configure({ mode: 'serial', retries: 0 });

const GEN6_URL = `${GEN6_V22_TEST_URL_LIGHT}`
  + '&flag-p2-tripwire-knuckle=true'
  + '&flag-p2-tripwire-static=false'
  + '&flag-p3-tripwire-injector=false'
  + '&flag-p3-tripwire-injector-static=false'
  + '&flag-p3-tripwire-injector-knuckle=false'
  + '&flag-ui-knuckle-tripwire-panel=false';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

test('Gen6 v22 RED: emits p2 tripplane_lookahead before knuckle crossing (COMMIT)', async ({ hfoPage }) => {
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

    const captured: Array<{ port: string; type: string; payload: any }> = [];
    const unsub = w.hfoPortsEffects.subscribe((entry: any) => {
      if (entry?.port !== 'p2') return;
      captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
    }, 'p2');

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
    }

    try {
      unsub?.();
    } catch {
      // ignore
    }

    return { captured };
  }, frames);

  const lookaheads = out.captured.filter((e: any) => e?.type === 'tripplane_lookahead');
  expect(lookaheads.length, `Expected >=1 tripplane_lookahead; got=${JSON.stringify(out.captured.slice(-20))}`).toBeGreaterThanOrEqual(1);

  for (const e of lookaheads) {
    const parsed = TripplaneLookaheadV22Schema.safeParse(e.payload);
    expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);
  }
});
