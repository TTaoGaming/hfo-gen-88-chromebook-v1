// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { TripwireCrossV15Schema } from '../contracts/hfo_tripwire_events.zod';

const GEN6_URL =
  process.env.HFO_GEN6_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v15.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&flag-p3-tripwire-injector=true&flag-p3-dino-ready-edge=false&mode=dev';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v12_tripwire_sensor_band_commit_only_golden.jsonl';

test('Gen6 v15 (TDD RED): Tripwire emits Planck contact metadata (sensor begin/end, fixture ids)', async ({ hfoPage }) => {
  const lines = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean);
  const frames = lines.map((l) => JSON.parse(l));
  expect(frames.length).toBeGreaterThanOrEqual(6);

  await hfoPage.goto(GEN6_URL, { waitUntil: 'domcontentloaded' });
  await hfoPage.waitForTimeout(250);

  const out = await hfoPage.evaluate((framesIn) => {
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

      w.hfoP2TripwireThread.tick({
        now: Number(f?.now || 0),
        dt: Number(f?.dt || 16),
        dataFabric,
      });
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
  expect(tripwire.length).toBeGreaterThanOrEqual(1);

  // v15 contract: tripwire_cross payload includes Planck sensor metadata.
  // This is intentionally RED until v15 refactor emits sensor fields.
  const parsed = TripwireCrossV15Schema.safeParse(tripwire[0]?.payload);
  expect(parsed.success, `Expected TripwireCrossV15Schema; debug=${JSON.stringify(out.debug)}`).toBe(true);
});
