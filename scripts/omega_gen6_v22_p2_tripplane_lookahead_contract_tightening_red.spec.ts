// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { TripplaneLookaheadV22Schema } from '../contracts/hfo_tripwire_events.zod';

// RED TDD: tighten the lookahead contract expectations beyond mere presence.
//
// When tripplane_lookahead exists, it must:
// - validate against TripplaneLookaheadV22Schema
// - include extension metadata consistent with microkernel flags (A/B)
// - be emitted before the begin crossing event
//
// Expected to FAIL until v22 emits tripplane_lookahead.

test.describe.configure({ retries: 0 });

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

test('Gen6 v22 RED: lookahead contract includes extension A/B and orders before crossing', async ({ hfoPage }) => {
  const frames = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));

  const url = `${GEN6_V22_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-ui-knuckle-tripwire-panel=false'
    + '&flag-p2-knuckle-tripwire-ext-a-frac=0.25'
    + '&flag-p2-knuckle-tripwire-ext-b-frac=0.75';

  await safeGoto(hfoPage, url);
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

  const beginCross = out.captured.find((e: any) => e?.type === 'tripwire_cross' && e?.payload?.sensor?.phase === 'begin');
  const crossNow = Number(beginCross?.payload?.now ?? NaN);

  for (const e of lookaheads) {
    const parsed = TripplaneLookaheadV22Schema.safeParse(e.payload);
    expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);

    const laNow = Number((e as any)?.payload?.now ?? NaN);
    expect(Number.isFinite(laNow) && Number.isFinite(crossNow)).toBe(true);
    expect(laNow, `Expected lookahead before crossing; laNow=${laNow} crossNow=${crossNow}`).toBeLessThan(crossNow);

    // Extension fields should be present once lookahead is implemented.
    const a = (e as any)?.payload?.barExtensionUiNormA;
    const b = (e as any)?.payload?.barExtensionUiNormB;
    expect(Number.isFinite(Number(a)) && Number.isFinite(Number(b))).toBe(true);
  }
});
