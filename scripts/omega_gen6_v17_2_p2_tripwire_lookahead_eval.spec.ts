// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V17_2_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V17_2_TEST_URL_LIGHT}`
  + '&flag-p2-tripwire-contact-only=false'
  + '&flag-p3-injector=false';

const SLOW_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v17_2_tripwire_slow_cross_golden.jsonl';

const FAST_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v17_2_tripwire_fast_cross_golden.jsonl';

function readFrames(path: string): any[] {
  return fs
    .readFileSync(path, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));
}

test('Gen6 v17.2: evaluate tripwire lookahead lead time (slow vs fast)', async ({ hfoPage }) => {
  const slowFrames = readFrames(SLOW_PATH);
  const fastFrames = readFrames(FAST_PATH);

  expect(slowFrames.length).toBeGreaterThanOrEqual(6);
  expect(fastFrames.length).toBeGreaterThanOrEqual(3);

  await safeGoto(hfoPage, GEN6_URL);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(
    hfoPage,
    (args) => {
      const w = window as any;
      if (!w.systemState) throw new Error('missing systemState');
      if (!w.hfoP2TripwireThread?.tick) throw new Error('missing hfoP2TripwireThread.tick');

      const lookaheads: number[] = [0, 50, 100, 200];

      function evalFixture(framesIn: any[]) {
        const captured: Array<{ port: string; type: string; payload: any }> = [];
        const unsubscribe = w.hfoPortsEffects?.subscribe
          ? w.hfoPortsEffects.subscribe((entry: any) => {
            if (entry?.port === 'p2') captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
          })
          : null;

        const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };

        // Warm debug state so we can read bandY.
        const dbg0 = w.hfoP2TripwireThread?.getDebugState?.() || null;
        const band = dbg0?.band || { centerUiNormY: 0.5 };
        const bandY = Number(band.centerUiNormY ?? 0.5);

        const predictedAtByLookahead: Record<string, number | null> = {};
        for (const ms of lookaheads) predictedAtByLookahead[String(ms)] = null;

        let prevNow: number | null = null;
        let prevY: number | null = null;

        for (const f of framesIn) {
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

          // Prediction (measurement-only): estimate vy from deltas.
          if (prevNow != null && prevY != null) {
            const y = Number(c?.uiNormY);
            const dtS = Math.max(1e-6, (now - prevNow) / 1000);
            const vy = (y - prevY) / dtS;

            // Downcross only for this eval: y increasing toward band.
            if (Number.isFinite(vy) && vy > 0 && Number.isFinite(y) && y < bandY) {
              const ttcMs = ((bandY - y) / vy) * 1000;
              if (Number.isFinite(ttcMs) && ttcMs > 0) {
                for (const ms of lookaheads) {
                  const k = String(ms);
                  if (predictedAtByLookahead[k] == null && ttcMs <= ms) {
                    predictedAtByLookahead[k] = now;
                  }
                }
              }
            }
          }

          prevNow = now;
          prevY = Number(c?.uiNormY);

          // Feed into the real TripwireThread to capture the actual crossing event.
          w.hfoP2TripwireThread.tick({ now, dt, dataFabric });
        }

        if (typeof unsubscribe === 'function') {
          try {
            unsubscribe();
          } catch {
            // ignore
          }
        }

        const crosses = captured.filter((e) => e?.type === 'tripwire_cross');
        const first = crosses[0]?.payload || null;
        const actualAt = first && typeof first.now === 'number' ? Number(first.now) : null;

        return { bandY, predictedAtByLookahead, actualAt, firstCross: first, crossCount: crosses.length };
      }

      return {
        slow: evalFixture(args.slowFrames),
        fast: evalFixture(args.fastFrames),
      };
    },
    { slowFrames, fastFrames },
  );

  // Coarse invariants: we should see a crossing for both fixtures.
  expect(out.slow.actualAt, `slow missing crossing; debug=${JSON.stringify(out.slow)}`).not.toBeNull();
  expect(out.fast.actualAt, `fast missing crossing; debug=${JSON.stringify(out.fast)}`).not.toBeNull();

  const slowActualAt = out.slow.actualAt;
  const fastActualAt = out.fast.actualAt;
  if (slowActualAt == null || fastActualAt == null) {
    throw new Error('missing crossing timestamp (unexpected after assertions)');
  }

  // Prediction sanity: for nonzero lookahead, predictedAt should be <= actualAt when it exists.
  for (const ms of [50, 100, 200]) {
    const k = String(ms);
    const pSlow = out.slow.predictedAtByLookahead[k];
    if (pSlow != null) expect(pSlow).toBeLessThanOrEqual(slowActualAt);

    const pFast = out.fast.predictedAtByLookahead[k];
    if (pFast != null) expect(pFast).toBeLessThanOrEqual(fastActualAt);
  }

  // Expectation shaped by fixtures:
  // - Slow: lookahead=200 should trigger at least 100ms before actual.
  {
    const p = out.slow.predictedAtByLookahead['200'];
    expect(p, `slow should predict at 200ms; debug=${JSON.stringify(out.slow)}`).not.toBeNull();
    expect(slowActualAt - (p as number)).toBeGreaterThanOrEqual(100);
  }

  // - Fast: lookahead=50 should trigger before crossing frame (given 3 frames).
  {
    const p = out.fast.predictedAtByLookahead['50'];
    expect(p, `fast should predict at 50ms; debug=${JSON.stringify(out.fast)}`).not.toBeNull();
    expect(fastActualAt - (p as number)).toBeGreaterThanOrEqual(1);
  }
});
