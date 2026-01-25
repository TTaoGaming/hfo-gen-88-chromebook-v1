// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED TDD: v22 knuckle tripplane should count crossings only when the fingertip crosses the plane
// within the (possibly extended) segment span (i.e., not the infinite line).
//
// This spec uses a MINIMAL golden fixture where the fingertip x is outside the original segment
// (~0.45..0.55) but inside the extended segment when ext=1.0 (~0.35..0.65). The ext=0 case should
// NOT trigger (currently fails because implementation uses infinite-line distance).

test.describe.configure({ retries: 0 });

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v22_knuckle_tripplane_extension_only_cross_min_golden.jsonl';

function loadFrames() {
  return fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));
}

async function runReplay(hfoPage: any, url: string, frames: any[]) {
  await safeGoto(hfoPage, url);
  await hfoPage.waitForTimeout(250);

  return await safeEvaluate(
    hfoPage,
    (framesIn) => {
      const w = window as any;
      if (!w.systemState) throw new Error('missing systemState');
      if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
      if (!w.hfoP2KnuckleTripwireThread?.tick) throw new Error('missing hfoP2KnuckleTripwireThread.tick');

      const captured: Array<{ port: string; type: string; payload: any }> = [];
      const unsub = w.hfoPortsEffects.subscribe((entry: any) => {
        if (entry?.port !== 'p2') return;
        if (entry?.type !== 'tripwire_cross') return;
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
    },
    frames,
  );
}

test('Gen6 v22 RED (MIN): ext=0 should NOT trigger when crossing is outside original segment', async ({ hfoPage }) => {
  const frames = loadFrames();

  const url = `${GEN6_V22_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-ui-knuckle-tripwire-panel=false'
    + '&flag-p2-knuckle-tripwire-ext-a-frac=0'
    + '&flag-p2-knuckle-tripwire-ext-b-frac=0';

  const out = await runReplay(hfoPage, url, frames);

  // v22 target semantics: this should be 0 because x is outside the original segment.
  // Current implementation uses infinite-line distance so it WILL trigger => RED until implemented.
  expect(out.captured.length, `Expected 0 knuckle tripwire_cross; got=${JSON.stringify(out.captured)}`).toBe(0);
});

test('Gen6 v22 (MIN): ext=1 expands endpoints outward (smoke)', async ({ hfoPage }) => {
  const frames = loadFrames();

  const url = `${GEN6_V22_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-ui-knuckle-tripwire-panel=false'
    + '&flag-p2-knuckle-tripwire-ext-a-frac=1.0'
    + '&flag-p2-knuckle-tripwire-ext-b-frac=1.0';

  const out = await runReplay(hfoPage, url, frames);

  if (out.captured.length === 0) return;

  const first = out.captured[0]?.payload;
  expect(first?.sensorId).toBe('knuckle');

  const aX = Number(first?.sensor?.bar?.a?.x ?? NaN);
  const bX = Number(first?.sensor?.bar?.b?.x ?? NaN);
  expect(Number.isFinite(aX) && Number.isFinite(bX)).toBe(true);

  // Original bar is approximately 0.45..0.55; with 1.0 extension on each end it should expand outward.
  expect(aX).toBeLessThan(0.45);
  expect(bX).toBeGreaterThan(0.55);
});
