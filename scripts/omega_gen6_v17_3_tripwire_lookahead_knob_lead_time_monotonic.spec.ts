// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V17_3_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { P3TripwireInjectV1Schema, TripwireLookaheadV1Schema, TripwireCrossV15Schema } from '../contracts/hfo_tripwire_events.zod';

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen6 v17.3: raising lookahead window increases inject lead time', async ({ hfoPage }) => {
    const frames = fs
        .readFileSync(
            'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v17_tripwire_lookahead_slow_cross_golden.jsonl',
            'utf-8',
        )
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
        .map((l) => JSON.parse(l));

    const measureLead = async (lookaheadWindowMs: number) => {
        // NOTE: include a per-run nonce in the URL to force a fresh document.
        // This prevents state bleed across repeated runs inside the same Playwright test.
        const url = `${GEN6_V17_3_TEST_URL_LIGHT}`
            + '&flag-p2-tripwire-contact-only=false'
            + '&flag-p3-injector=false'
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

                // Set the Port7-backed knobs directly (GUI is just a view onto these).
                w.hfoState.parameters.p2 = w.hfoState.parameters.p2 || {};
                w.hfoState.parameters.p2.tripwireThread = w.hfoState.parameters.p2.tripwireThread || {};
                w.hfoState.parameters.p2.tripwireThread.lookaheadEnabled = true;
                w.hfoState.parameters.p2.tripwireThread.lookaheadWindowMs = args.lookaheadWindowMs;

                w.hfoState.parameters.p3 = w.hfoState.parameters.p3 || {};
                w.hfoState.parameters.p3.tripwireInjector = w.hfoState.parameters.p3.tripwireInjector || {};
                w.hfoState.parameters.p3.tripwireInjector.lookaheadEnabled = true;

                try {
                    w.hfoPortsEffects.clear();
                } catch {
                    // ignore
                }

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
                            normX: c?.uiNormX,
                            normY: c?.uiNormY,
                        },
                    ];

                    w.hfoP2TripwireThread.tick({ now, dt, dataFabric });
                    w.hfoP3PlanckSensorInjector.tick({ now, dt, dataFabric });
                }

                const recent = w.hfoPortsEffects.getRecent(250) || [];
                const relevant = recent.filter((e: any) =>
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
                    debug: { sampleCount: relevant.length, recentCount: recent.length },
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

    // Validate payload shapes (fail-closed contracts) in Node context.
    if (low.samples.firstLookahead) TripwireLookaheadV1Schema.parse(low.samples.firstLookahead);
    if (high.samples.firstLookahead) TripwireLookaheadV1Schema.parse(high.samples.firstLookahead);
    TripwireCrossV15Schema.parse(low.samples.firstCross);
    TripwireCrossV15Schema.parse(high.samples.firstCross);
    P3TripwireInjectV1Schema.parse(low.samples.firstInject);
    P3TripwireInjectV1Schema.parse(high.samples.firstInject);

    // Sanity: with window=0ms, we should not be emitting lookahead events.
    expect(low.counts.cross, 'expected >=1 p2/tripwire_cross @ window=0ms').toBeGreaterThanOrEqual(1);
    expect(low.counts.inject, 'expected >=1 p3/tripwire_inject @ window=0ms').toBeGreaterThanOrEqual(1);
    expect(low.counts.lookahead, 'expected 0 lookahead @ window=0ms').toBe(0);

    // With window=200ms, we expect at least one lookahead emission.
    expect(high.counts.cross, 'expected >=1 p2/tripwire_cross @ window=200ms').toBeGreaterThanOrEqual(1);
    expect(high.counts.inject, 'expected >=1 p3/tripwire_inject @ window=200ms').toBeGreaterThanOrEqual(1);
    expect(high.counts.lookahead, 'expected >=1 lookahead @ window=200ms').toBeGreaterThanOrEqual(1);

    // Both modes should inject on/around crossing.
    expect(low.leadMs).toBeGreaterThanOrEqual(0);
    expect(high.leadMs).toBeGreaterThanOrEqual(0);

    // Monotonic: raising window should strictly increase lead time.
    expect(high.leadMs).toBeGreaterThan(low.leadMs + 100);

    // For this fixture, window=200ms should produce a meaningful lead.
    expect(high.leadMs).toBeGreaterThanOrEqual(150);

    // In the zero-window case, lead should be near-zero (inject driven by crossing subscription).
    expect(low.leadMs).toBeLessThanOrEqual(30);
});
