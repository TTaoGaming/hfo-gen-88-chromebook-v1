// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';

const GEN6_URL =
  process.env.HFO_GEN6_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v12.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&mode=dev';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v12_tripwire_sensor_band_commit_only_golden.jsonl';

test('Gen6 v12 (TDD RED): Tripwire sensor band emits only in COMMIT (IDLE/READY crossing is silent)', async ({ hfoPage }) => {
  const lines = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean);
  const frames = lines.map((l) => JSON.parse(l));
  expect(frames.length).toBeGreaterThanOrEqual(6);

  await hfoPage.goto(GEN6_URL, { waitUntil: 'domcontentloaded' });
  await hfoPage.waitForTimeout(200);

  const out = await hfoPage.evaluate((framesIn) => {
    const w = window as any;

    if (!w.systemState) throw new Error('missing systemState');

    // The tripwire module will be introduced by the v12 evolution.
    // RED until it exists.
    if (!w.hfoP2TripwireThread?.tick) throw new Error('missing hfoP2TripwireThread.tick');

    // Capture Port2 emits.
    // NOTE: hfoPortsEffects is Object.freeze()'d in the runtime, so monkey-patching emit is unreliable.
    const captured: Array<{ port: string; type: string; payload: any }> = [];
    const unsubscribe = w.hfoPortsEffects?.subscribe
      ? w.hfoPortsEffects.subscribe((entry: any) => {
        if (entry?.port === 'p2') captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      }, 'p2')
      : null;

    // Replay frames through a minimal DataFabric envelope.
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
    };
  }, frames);

  const tripwireEvents = out.captured.filter(
    (e: any) => String(e.type || '').startsWith('tripwire_') || String(e.type || '').includes('tripwire'),
  );

  // Expected outcome after implementation:
  // - no tripwire cross events for IDLE crossing
  // - no tripwire cross events for READY crossing
  // - exactly 1 tripwire cross event for COMMIT crossing
  const bySeq: Record<string, number> = { idle_cross: 0, ready_cross: 0, commit_cross: 0 };
  for (const ev of tripwireEvents) {
    const seq = ev?.payload?.seq;
    if (seq && typeof bySeq[seq] === 'number') bySeq[seq]++;
  }

  expect(bySeq.idle_cross, 'IDLE crossing should be silent').toBe(0);
  expect(bySeq.ready_cross, 'READY crossing should be silent').toBe(0);
  expect(bySeq.commit_cross, `COMMIT crossing should emit (debug=${JSON.stringify(out.debug)})`).toBeGreaterThanOrEqual(1);
});
