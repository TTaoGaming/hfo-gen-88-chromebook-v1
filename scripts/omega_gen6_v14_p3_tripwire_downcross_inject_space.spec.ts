// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';

const GEN6_URL =
  process.env.HFO_GEN6_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v14.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&flag-p3-tripwire-injector=true&flag-p3-dino-ready-edge=false&mode=dev';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v12_tripwire_sensor_band_commit_only_golden.jsonl';

test('Gen6 v14: Tripwire down-cross injects Space via P3 (tripwire_inject)', async ({ hfoPage }) => {
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
        if (entry?.port === 'p2' || entry?.port === 'p3') {
          captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
        }
      })
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

    return {
      captured,
      debug: w.hfoP2TripwireThread?.getDebugState?.() || null,
      lastInject: w.hfoP3PlanckSensorInjector?.getLastInject?.() || null,
    };
  }, frames);

  const p2TripwireCross = out.captured.filter((e: any) => e?.port === 'p2' && e?.type === 'tripwire_cross');
  const p3TripwireInject = out.captured.filter((e: any) => e?.port === 'p3' && e?.type === 'tripwire_inject');

  // We expect the golden frames to include a COMMIT down-cross (y 0.45 → 0.55).
  // TripwireThread is still COMMIT-only by default, so only COMMIT should emit.
  expect(p2TripwireCross.length).toBeGreaterThanOrEqual(1);

  const crossDirections = new Set(p2TripwireCross.map((e: any) => String(e?.payload?.direction || '')));
  expect(crossDirections.has('down')).toBe(true);

  // Port3 injector should translate the P2 down-cross into an attempted Space keypress.
  expect(p3TripwireInject.length, `Expected p3/tripwire_inject (debug=${JSON.stringify(out.debug)})`).toBeGreaterThanOrEqual(
    1,
  );

  const inject = p3TripwireInject[0]?.payload || {};
  expect(String(inject.direction || ''), 'Injector should be down-cross only').toBe('down');
  expect(String(inject.adapterId || ''), 'Injector should target dino-v1').toBe('dino-v1');

  const payload = inject.payload || {};
  expect(String(payload.kind || '')).toBe('keyboard');
  expect(String(payload.action || '')).toBe('keypress');
  expect(String(payload.key || '')).toBe(' ');
  expect(String(payload.code || '')).toBe('Space');

  // Extra sanity: injector writes a lastInject snapshot.
  if (out.lastInject) {
    expect(String(out.lastInject.direction || '')).toBe('down');
  }
});
