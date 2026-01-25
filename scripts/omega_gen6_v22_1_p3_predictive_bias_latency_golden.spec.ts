// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import {
    GEN6_V22_1_TEST_URL_LIGHT,
    safeGoto,
    safeEvaluate,
} from './omega_gen6_test_guards';

test.describe.configure({ retries: 0 });

const FRAME_FIXTURE_PATH =
    'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v17_tripwire_lookahead_slow_cross_golden.jsonl';

const EXPECT_GOLDEN_PATH =
    'hfo_hot_obsidian/bronze/3_resources/fixtures/latency/gen6_v22_1_p3_predictive_bias_latency_golden.json';

function loadFrames() {
    return fs
        .readFileSync(FRAME_FIXTURE_PATH, 'utf-8')
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
        .map((l) => JSON.parse(l));
}

function loadExpected() {
    return JSON.parse(fs.readFileSync(EXPECT_GOLDEN_PATH, 'utf-8'));
}

type VenomEvent = {
    ts?: number;
    stage: string;
    [k: string]: any;
};

function pickFirst(events: VenomEvent[], stage: string, predicate?: (e: VenomEvent) => boolean): VenomEvent | null {
    const filtered = events.filter((e) => e?.stage === stage && (!predicate || predicate(e)));
    if (filtered.length === 0) return null;
    filtered.sort((a, b) => Number(a?.now ?? 0) - Number(b?.now ?? 0));
    return filtered[0] || null;
}

function projectSchedule(e: VenomEvent | null) {
    if (!e) return null;
    return {
        now: Number(e.now ?? 0),
        ttcMs: Number(e.ttcMs ?? 0),
        windowMs: Number(e.windowMs ?? 0),
        biasMs: Number(e.biasMs ?? 0),
        delayMsUnbiased: Number(e.delayMsUnbiased ?? 0),
        delayMs: Number(e.delayMs ?? 0),
        injectAtNow: Number(e.injectAtNow ?? 0),
    };
}

function projectFire(e: VenomEvent | null) {
    if (!e) return null;
    return {
        now: Number(e.now ?? 0),
        injectAtNow: Number(e.injectAtNow ?? 0),
        driftMs: Number(e.driftMs ?? 0),
    };
}

function projectInject(e: VenomEvent | null) {
    if (!e) return null;
    return {
        now: Number(e.now ?? 0),
        sensorId: String(e.sensorId ?? ''),
        phase: String(e.phase ?? ''),
        action: String(e.action ?? ''),
    };
}

function projectCross(e: VenomEvent | null) {
    if (!e) return null;
    return {
        now: Number(e.now ?? 0),
        sensorId: String(e.sensorId ?? ''),
        phase: String(e.phase ?? ''),
    };
}

async function runReplayAndGetVenomEvents(hfoPage: any, url: string, frames: any[]) {
    await safeGoto(hfoPage, url);
    await hfoPage.waitForTimeout(200);

    return await safeEvaluate(
        hfoPage,
        (framesIn) => {
            const w = window as any;
            if (!w.systemState) throw new Error('missing systemState');
            if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
            if (!w.hfoP3PlanckSensorInjector?.tick) throw new Error('missing hfoP3PlanckSensorInjector.tick');
            if (!w.hfoTracerVenomBattery?.getEvents) throw new Error('missing hfoTracerVenomBattery.getEvents');

            try { w.__hfoTracerVenomBatteryEvents = []; } catch (_) { }
            try { w.hfoPortsEffects?.clear?.(); } catch (_) { }

            const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };

            // Deterministic synthetic Port-2 events:
            // - Emit lookahead early (ttcMs=500 at now=100) so P3 schedules an injectAtNow=300.
            //   (300ms clears the hard-coded P3 cooldown gate.)
            // - Emit the real crossing at now=600 so we can compute leadMs.
            const pointerId = 10;
            const handIndex = 0;
            const readinessScore = 0.95;
            const bandY = 0.5;
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

                // Emit a single lookahead at now=100ms.
                if (now === 100) {
                    try {
                        w.hfoPortsEffects.emit('p2', 'tripwire_lookahead', {
                            ts: new Date().toISOString(),
                            sensorId: 'static',
                            now,
                            dt,
                            seq: 1,
                            handIndex,
                            pointerId,
                            fsmState: 'COMMIT',
                            readiness: readinessScore,
                            uiNormX: Number(f?.cursor?.uiNormX ?? 0.5),
                            uiNormY: Number(f?.cursor?.uiNormY ?? 0.3),
                            direction: 'down',
                            vxUiNormPerS: 0,
                            vyUiNormPerS: 0.5,
                            speedUiNormPerS: 0.5,
                            bandY,
                            ttcMs: 500,
                            lookaheadWindowMs: 500,
                        });
                    } catch (_) {
                        // ignore
                    }
                }

                // Emit the real crossing at now=600ms.
                if (now === 600) {
                    try {
                        w.hfoPortsEffects.emit('p2', 'tripwire_cross', {
                            ts: new Date().toISOString(),
                            sensorId: 'static',
                            now,
                            dt,
                            seq: 2,
                            handIndex,
                            pointerId,
                            fsmState: 'COMMIT',
                            readiness: readinessScore,
                            uiNormX: Number(f?.cursor?.uiNormX ?? 0.5),
                            uiNormY: Number(f?.cursor?.uiNormY ?? 0.55),
                            direction: 'down',
                            vxUiNormPerS: 0,
                            vyUiNormPerS: 0.5,
                            speedUiNormPerS: 0.5,
                            sensor: { phase: 'begin' },
                        });
                    } catch (_) {
                        // ignore
                    }
                }

                // Tick P3 after Port-2 emissions so it can schedule and fire.
                w.hfoP3PlanckSensorInjector.tick({ now, dt, dataFabric });
            }

            const events = w.hfoTracerVenomBattery.getEvents();
            return { events };
        },
        frames,
    );
}

test('Gen6 v22.1: default -100ms bias is observable as earlier scheduled inject (golden)', async ({ hfoPage }) => {
    const frames = loadFrames();
    const golden = loadExpected();

    const url = `${GEN6_V22_1_TEST_URL_LIGHT}`
        + '&flag-p2-tripwire-static=true'
        + '&flag-p2-tripwire-knuckle=false'
        + '&flag-p2-tripwire-lookahead=true'
        + '&flag-p2-tripwire-lookahead-window-ms=400'
        + '&flag-p3-tripwire-injector-static=true'
        + '&flag-p3-tripwire-injector-knuckle=false'
        + '&flag-p3-tripwire-lookahead=true'
        + '&flag-p3-tripwire-lookahead-window-ms=200'
        + '&flag-p3-tracer-venom-battery=true'
        + '&flag-p3-tracer-venom-battery-verbose=false';

    const out = await runReplayAndGetVenomEvents(hfoPage, url, frames);
    const events: VenomEvent[] = Array.isArray(out?.events) ? out.events : [];

    const schedule = projectSchedule(
        pickFirst(events, 'p3.lookahead.schedule', (e) => String(e?.sensorId || '') === 'static'),
    );
    const fire = projectFire(
        pickFirst(events, 'p3.lookahead.fire', (e) => String(e?.sensorId || '') === 'static'),
    );
    const inject = projectInject(
        pickFirst(events, 'p3.inject.payload', (e) => String(e?.sensorId || '') === 'static'),
    );
    const cross = projectCross(
        pickFirst(events, 'p3.rx.tripwire_cross', (e) => String(e?.sensorId || '') === 'static'),
    );

    const derived = {
        leadMs: (cross && inject) ? (Number(cross.now) - Number(inject.now)) : null,
    };

    const summary = { schedule, fire, inject, cross, derived };

    // Guardrails: if these go missing, we are no longer observing the pipeline.
    expect(schedule, 'missing p3.lookahead.schedule').toBeTruthy();
    expect(fire, 'missing p3.lookahead.fire').toBeTruthy();
    expect(inject, 'missing p3.inject.payload').toBeTruthy();
    expect(cross, 'missing p3.rx.tripwire_cross').toBeTruthy();

    expect(summary).toEqual(golden.expect);
});
