// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_1_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// v22.1 smoke: when tracer venom battery is enabled, the pipeline should emit stage breadcrumbs.
// Goal: make hidden latency measurable (schedule decision, injection, delivery attempts, ack if present).

test.describe.configure({ retries: 0 });

const GEN6_URL = `${GEN6_V22_1_TEST_URL_LIGHT}`
  + '&flag-p2-tripwire-knuckle=true'
  + '&flag-p2-tripwire-static=false'
  + '&flag-p3-tripwire-injector-knuckle=true'
  + '&flag-p3-tripwire-injector=false'
  + '&flag-p3-tripwire-injector-static=false'
  + '&flag-ui-knuckle-tripwire-panel=false'
  + '&flag-p3-tracer-venom-battery=true';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

test('Gen6 v22.1: tracer venom battery emits stage breadcrumbs (smoke)', async ({ hfoPage }) => {
  const frames = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));

  await safeGoto(hfoPage, GEN6_URL);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(
    hfoPage,
    async (framesIn) => {
      const w = window as any;
      if (!w.systemState) throw new Error('missing systemState');
      if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
      if (!w.hfoP2KnuckleTripwireThread?.tick) throw new Error('missing hfoP2KnuckleTripwireThread.tick');

      try {
        w.__hfoTracerVenomBatteryEvents = [];
      } catch {
        // ignore
      }

      try {
        w.hfoP3PlanckSensorInjector?.start?.();
      } catch {
        // ignore
      }

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

        const now = Number(f?.now || 0);
        const dt = Number(f?.dt || 16);
        w.hfoP2KnuckleTripwireThread.tick({ now, dt, dataFabric });

        try {
          w.hfoP3PlanckSensorInjector?.tick?.({ now, dt, dataFabric });
        } catch {
          // ignore
        }
      }

      // Allow scheduled injections / postMessage attempts to flush.
      await new Promise((r) => setTimeout(r, 350));

      const events = Array.isArray(w.__hfoTracerVenomBatteryEvents) ? w.__hfoTracerVenomBatteryEvents : [];
      return { count: events.length, stages: events.map((e: any) => e?.stage).filter(Boolean), tail: events.slice(-25) };
    },
    frames,
  );

  expect(out.count, `Expected tracer venom battery events > 0; tail=${JSON.stringify(out.tail)}`).toBeGreaterThan(0);

  // Minimal required breadcrumbs: P3 should at least observe P2 traffic.
  expect(out.stages).toContain('p3.rx.tripwire_cross');

  // Stronger signal (optional): lookahead scheduling often present in this fixture.
  // If missing, we still accept as long as we saw P2→P3 receipt and at least one inject payload stage.
  if (!out.stages.includes('p3.rx.tripplane_lookahead')) {
    expect(out.stages, `Expected either tripplane lookahead or inject payload stage; tail=${JSON.stringify(out.tail)}`).toContain('p3.inject.payload');
  }
});
