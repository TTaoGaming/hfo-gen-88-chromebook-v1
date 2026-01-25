// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V16_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// Desired v16 behavior: when contact-only is enabled, tripwire events are driven by Planck sensor contacts.
// Sparse frames that never enter the band thickness must NOT emit.
test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V16_TEST_URL_LIGHT}&flag-p2-tripwire-contact-only=true`;

// Existing sparse fixture (0.45 -> 0.55) crosses center but has no in-band sample.
const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v12_tripwire_sensor_band_commit_only_golden.jsonl';

test('Gen6 v16 (TDD RED): contact-only tripwire suppresses geometric emit on sparse frames', async ({ hfoPage }) => {
  const lines = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean);
  const frames = lines.map((l) => JSON.parse(l));
  expect(frames.length).toBeGreaterThanOrEqual(6);

  await safeGoto(hfoPage, GEN6_URL);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(hfoPage, (framesIn) => {
    const w = window as any;
    if (!w.systemState) throw new Error('missing systemState');
    if (!w.hfoP2TripwireThread?.tick) throw new Error('missing hfoP2TripwireThread.tick');

    const captured: Array<{ port: string; type: string; payload: any }> = [];
    const unsubscribe = w.hfoPortsEffects?.subscribe
      ? w.hfoPortsEffects.subscribe((entry: any) => {
        if (entry?.port === 'p2') captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      }, 'p2')
      : null;

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
      w.hfoP2TripwireThread.tick({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
    }

    if (typeof unsubscribe === 'function') {
      try {
        unsubscribe();
      } catch {
        // ignore
      }
    }

    return { captured, debug: w.hfoP2TripwireThread?.getDebugState?.() || null };
  }, frames);

  const tripwire = out.captured.filter((e: any) => e?.type === 'tripwire_cross');

  // RED until v16 implements contact-only mode.
  expect(tripwire.length, `Expected 0 in contact-only mode; debug=${JSON.stringify(out.debug)}`).toBe(0);
});
