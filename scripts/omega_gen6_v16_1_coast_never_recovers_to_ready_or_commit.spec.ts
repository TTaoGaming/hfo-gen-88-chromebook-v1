// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V16_1_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

// This test asserts a strict fail-closed posture:
// Even under best-case signals (facing camera, confident, pointing), COAST must never recover to READY/COMMIT.
// (It may remain COAST until readiness drains and it decays to IDLE.)

test('Gen6 v16.1: COAST never recovers to READY/COMMIT (fail-closed)', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_V16_1_TEST_URL_LIGHT);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');
        if (!w.hfoPorts?.p1?.weave) throw new Error('missing hfoPorts.p1.weave');

        w.systemState.parameters.landmarks.numHands = 1;

        // Make it easier to stay in COAST (avoid immediate COAST->IDLE).
        w.systemState.parameters.fsm.hysteresisLow = 0.1;
        w.systemState.parameters.fsm.coastDrainTimeMs = 5000;
        w.systemState.parameters.readiness.drainMultiplier = 1.0;
        w.systemState.parameters.readiness.coastDrainMultiplier = 1.0;

        // Start in COAST.
        w.systemState.p1.fsmStates[0] = 'COAST';
        w.systemState.p1.readinessScores[0] = 0.9;

        const dummyLandmarks = () =>
            Array.from({ length: 21 }, (_, j) => ({
                x: 0.5 + (j % 5) * 0.002,
                y: 0.5 + Math.floor(j / 5) * 0.002,
                z: 0,
            }));

        const buildResults = () => ({
            landmarks: [dummyLandmarks()],
            gestures: [[{ categoryName: 'Pointing_Up', score: 1.0 }]],
            __hfoReplayHands: [
                {
                    handIndex: 0,
                    present: true,
                    isFacingCamera: true,
                    isCharging: true,
                    hasConfidence: true,
                    shouldFill: true,
                    isPointing: true,
                    categoryName: 'Pointing_Up',
                    confidence: 1.0,
                },
            ],
        });

        const frames: Array<{ fsm: string; readiness: number }> = [];
        for (let k = 0; k < 20; k++) {
            w.hfoPorts.p1.weave(buildResults(), 16, 1000 + k * 16);
            frames.push({
                fsm: String(w.systemState.p1.fsmStates[0] || ''),
                readiness: Number(w.systemState.p1.readinessScores[0] || 0),
            });
        }

        return { frames };
    }, null as any);

    const bad = out.frames.filter((f) => f.fsm === 'READY' || f.fsm === 'COMMIT');
    expect(bad, `frames=${JSON.stringify(out.frames)}`).toHaveLength(0);
});
