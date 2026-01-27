// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { P3TripwireInjectV1Schema, P3TripwireInjectV2Schema, TripwireLookaheadV1Schema } from '../contracts/hfo_tripwire_events.zod';

test.describe.configure({ mode: 'serial', retries: 1 });

const FIXTURE_PATH =
    'hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/tests/fixtures/touch2d/gen6_v17_tripwire_lookahead_slow_cross_golden.jsonl';

const GEN7_V1_PORTABLE_V23_10_URL_BASE =
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/app/omega_gen6_v23_10.html';

test('Gen7 portable v23.10: raising lookahead window increases inject lead time', async ({ hfoPage }) => {
    const frames = fs
        .readFileSync(FIXTURE_PATH, 'utf-8')
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
        .map((l) => JSON.parse(l));

    const measureLead = async (lookaheadWindowMs: number) => {
        const url = `${GEN7_V1_PORTABLE_V23_10_URL_BASE}`
            + `?__cb=${Date.now()}`
            + '&flag-disable-camera=true'
            + '&flag-engine-babylon=false'
            + '&flag-engine-canvas=false'
            + '&flag-ui-golden-layout=false'
            + '&flag-ui-excalidraw=false'
            + '&flag-ui-lil-gui=false'
            + '&flag-ui-microkernel=false'
            // P3 injector enablement in v23.10 is flag-gated.
            + '&flag-p3-tripwire-injector=true'
            + '&flag-p3-tripwire-injector-static=true'
            + '&kiosk=0&hero=0&mode=dev'
            + `&test-run=${encodeURIComponent(String(lookaheadWindowMs))}`;

        await safeGoto(hfoPage, url);
        await hfoPage.waitForTimeout(150);

        return safeEvaluate(
            hfoPage,
            (args) => {
                const w = window as any;

                if (!w.hfoPortsEffects?.getRecent) throw new Error('missing hfoPortsEffects.getRecent');
                if (!w.hfoPortsEffects?.clear) throw new Error('missing hfoPortsEffects.clear');
                if (!w.hfoP2TripwireThread?.tick) throw new Error('missing hfoP2TripwireThread.tick');
                if (!w.hfoP3PlanckSensorInjector?.tick) throw new Error('missing hfoP3PlanckSensorInjector.tick');
                if (!w.hfoState?.parameters) throw new Error('missing hfoState.parameters');

                // Port7-backed knobs: GUI is a view onto these.
                w.hfoState.parameters.p2 = w.hfoState.parameters.p2 || {};
                w.hfoState.parameters.p2.tripwireThread = w.hfoState.parameters.p2.tripwireThread || {};
                w.hfoState.parameters.p2.tripwireThread.lookaheadEnabled = true;
                w.hfoState.parameters.p2.tripwireThread.lookaheadWindowMs = args.lookaheadWindowMs;

                w.hfoState.parameters.p3 = w.hfoState.parameters.p3 || {};
                w.hfoState.parameters.p3.tripwireInjector = w.hfoState.parameters.p3.tripwireInjector || {};
                w.hfoState.parameters.p3.tripwireInjector.lookaheadEnabled = true;

                try { w.hfoPortsEffects.clear(); } catch { }

                const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };

                for (const f of args.frames) {
                    const now = Number(f?.now || 0);
                    const dt = Number(f?.dt || 16);
                    const c = f?.cursor || {};

                    dataFabric.frameId++;
                    dataFabric.systemTime = now;
                    dataFabric.cursors = [
                        {
                            ...c,
                            seq: f?.seq,
                            // Provide both legacy and modern names to be robust across gens.
                            uiNormX: c?.uiNormX,
                            uiNormY: c?.uiNormY,
                            normX: c?.uiNormX,
                            normY: c?.uiNormY,
                        },
                    ];

                    w.hfoP2TripwireThread.tick({ now, dt, dataFabric });
                    w.hfoP3PlanckSensorInjector.tick({ now, dt, dataFabric });
                }

                const recent = w.hfoPortsEffects.getRecent(350) || [];
                const relevant = recent
                    .filter((e: any) =>
                        (e?.port === 'p2' || e?.port === 'p3')
                        && (e?.type === 'tripwire_lookahead' || e?.type === 'tripwire_cross' || e?.type === 'tripwire_inject'))
                    .map((e: any) => ({ port: e.port, type: e.type, payload: e.payload }));

                const p2Look = relevant.filter((e: any) => e.port === 'p2' && e.type === 'tripwire_lookahead');
                const p2Cross = relevant.filter((e: any) => e.port === 'p2' && e.type === 'tripwire_cross');
                const p3Inject = relevant.filter((e: any) => e.port === 'p3' && e.type === 'tripwire_inject');

                const firstCross = p2Cross[0]?.payload ?? null;
                const firstInject = p3Inject[0]?.payload ?? null;

                const crossNow = Number(firstCross?.now);
                const injectNow = Number(firstInject?.now);
                const leadMs = (Number.isFinite(crossNow) && Number.isFinite(injectNow)) ? (crossNow - injectNow) : NaN;

                return {
                    lookaheadWindowMs: Number(args.lookaheadWindowMs),
                    crossNow,
                    injectNow,
                    leadMs,
                    counts: { lookahead: p2Look.length, cross: p2Cross.length, inject: p3Inject.length },
                    samples: {
                        firstLookahead: p2Look[0]?.payload ?? null,
                        firstCross: firstCross ?? null,
                        firstInject: firstInject ?? null,
                    },
                };
            },
            { frames, lookaheadWindowMs },
        );
    };

    const low = await measureLead(0);
    const high = await measureLead(200);

    if (low.samples.firstLookahead) TripwireLookaheadV1Schema.parse(low.samples.firstLookahead);
    if (high.samples.firstLookahead) TripwireLookaheadV1Schema.parse(high.samples.firstLookahead);

    // v23.10 emits a `sensorId` field on `tripwire_cross` (e.g. "static"), which is richer than
    // `TripwireCrossV15Schema`. For this portable regression check, validate shape minimally.
    expect(low.samples.firstCross?.sensor?.engine).toBe('planck');
    expect(high.samples.firstCross?.sensor?.engine).toBe('planck');
    expect(typeof low.samples.firstCross?.now).toBe('number');
    expect(typeof high.samples.firstCross?.now).toBe('number');

    // Inject payload has evolved across gens (V1 vs V2 adds sensorId + action variants).
    try {
        P3TripwireInjectV1Schema.parse(low.samples.firstInject);
        P3TripwireInjectV1Schema.parse(high.samples.firstInject);
    } catch {
        P3TripwireInjectV2Schema.parse(low.samples.firstInject);
        P3TripwireInjectV2Schema.parse(high.samples.firstInject);
    }

    expect(low.counts.cross, 'expected >=1 p2/tripwire_cross @ window=0ms').toBeGreaterThanOrEqual(1);
    expect(low.counts.inject, 'expected >=1 p3/tripwire_inject @ window=0ms').toBeGreaterThanOrEqual(1);
    expect(low.counts.lookahead, 'expected 0 lookahead @ window=0ms').toBe(0);

    expect(high.counts.cross, 'expected >=1 p2/tripwire_cross @ window=200ms').toBeGreaterThanOrEqual(1);
    expect(high.counts.inject, 'expected >=1 p3/tripwire_inject @ window=200ms').toBeGreaterThanOrEqual(1);
    expect(high.counts.lookahead, 'expected >=1 lookahead @ window=200ms').toBeGreaterThanOrEqual(1);

    expect(low.leadMs).toBeGreaterThanOrEqual(0);
    expect(high.leadMs).toBeGreaterThanOrEqual(0);

    expect(high.leadMs).toBeGreaterThan(low.leadMs + 100);
    expect(high.leadMs).toBeGreaterThanOrEqual(150);
    expect(low.leadMs).toBeLessThanOrEqual(30);
});
