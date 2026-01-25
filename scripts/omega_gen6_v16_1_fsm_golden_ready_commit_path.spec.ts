// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V16_1_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

const GOLDEN_PATH =
    'hfo_hot_obsidian/bronze/3_resources/fixtures/fsm/gen6_v16_1_fsm_ready_commit_drain_golden.jsonl';

test('Gen6 v16.1 FSM golden: COMMIT only reachable from READY; readiness fill/drain works', async ({ hfoPage }) => {
    const frames = fs
        .readFileSync(GOLDEN_PATH, 'utf-8')
        .split('\n')
        .map((l) => l.trim())
        .filter(Boolean)
        .map((l) => JSON.parse(l));
    expect(frames.length).toBeGreaterThanOrEqual(4);

    await safeGoto(hfoPage, GEN6_V16_1_TEST_URL_LIGHT);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(
        hfoPage,
        (framesIn) => {
            const w = window as any;
            if (!w.systemState) throw new Error('missing systemState');
            if (!w.hfoPorts?.p1?.weave) throw new Error('missing hfoPorts.p1.weave');

            // Deterministic timebase: P1 uses performance.now internally.
            let fakeNow = 1000;
            try {
                (performance as any).now = () => fakeNow;
            } catch {
                // ignore
            }

            // Deterministic config for exact readiness math.
            w.systemState.parameters.landmarks.numHands = 1;
            w.systemState.parameters.fsm.hysteresisHigh = 0.8;
            w.systemState.parameters.fsm.hysteresisLow = 0.2;
            w.systemState.parameters.fsm.chargeTimeMs = 200;
            w.systemState.parameters.fsm.releaseTimeMs = 200;
            w.systemState.parameters.fsm.coastDrainTimeMs = 200;
            w.systemState.parameters.readiness.fillMultiplier = 1.0;
            w.systemState.parameters.readiness.drainMultiplier = 1.0;
            w.systemState.parameters.readiness.coastDrainMultiplier = 1.0;

            // Clean start.
            w.systemState.p1.fsmStates[0] = 'IDLE';
            w.systemState.p1.readinessScores[0] = 0;
            w.systemState.p1.lastPalmFacingTimes[0] = 0;
            w.systemState.p1.lastTrackingTimes[0] = 0;

            const dummyLandmarks = () =>
                Array.from({ length: 21 }, (_, j) => ({
                    x: 0.5 + (j % 5) * 0.002,
                    y: 0.5 + Math.floor(j / 5) * 0.002,
                    z: 0,
                }));

            const observed: Array<{ step: number; dt: number; fsm: string; readiness: number }> = [];

            for (const fr of framesIn as any[]) {
                const dt = Number(fr?.dt ?? 16);
                fakeNow += dt;

                const h = fr?.hand || {};
                const present = h.present !== false;

                const results = {
                    landmarks: [present ? dummyLandmarks() : null],
                    gestures: [[{ categoryName: 'Pointing_Up', score: 1.0 }]],
                    __hfoReplayHands: [
                        {
                            handIndex: 0,
                            present,
                            isFacingCamera: Boolean(h.isFacingCamera),
                            isCharging: Boolean(h.isCharging),
                            hasConfidence: Boolean(h.hasConfidence),
                            shouldFill: Boolean(h.shouldFill),
                            isPointing: Boolean(h.isPointing),
                            categoryName: 'Pointing_Up',
                            confidence: 1.0,
                        },
                    ],
                };

                w.hfoPorts.p1.weave(results, dt, fakeNow);

                observed.push({
                    step: Number(fr?.step ?? 0),
                    dt,
                    fsm: String(w.systemState.p1.fsmStates[0] || ''),
                    readiness: Number(w.systemState.p1.readinessScores[0] || 0),
                });
            }

            return { href: String(window.location?.href || ''), observed };
        },
        frames,
    );

    expect(out.href).toContain('omega_gen6_v16_1.html');

    // Golden: check exact expected fsm + readiness.
    for (let i = 0; i < frames.length; i++) {
        const exp = frames[i].expect;
        const obs = out.observed[i];
        expect(obs.fsm, `step=${frames[i].step} observed=${JSON.stringify(out.observed)}`).toBe(String(exp.fsm));
        expect(obs.readiness, `step=${frames[i].step} observed=${JSON.stringify(out.observed)}`).toBeCloseTo(
            Number(exp.readiness),
            8,
        );
    }

    // Invariant: the only way into COMMIT is from READY.
    for (let i = 1; i < out.observed.length; i++) {
        const prev = out.observed[i - 1].fsm;
        const curr = out.observed[i].fsm;
        if (curr === 'COMMIT' && prev !== 'COMMIT') {
            expect(prev, `observed=${JSON.stringify(out.observed)}`).toBe('READY');
        }
    }
});
