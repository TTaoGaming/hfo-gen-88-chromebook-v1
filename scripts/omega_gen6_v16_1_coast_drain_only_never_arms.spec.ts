// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V16_1_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

// COAST doctrine:
// - COAST is LOW CONFIDENCE sink.
// - While in COAST, readiness must never fill (drain-only).
// - COAST must never transition into READY/COMMIT (fail-closed).

test('Gen6 v16.1: COAST is drain-only and never arms READY/COMMIT', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_V16_1_TEST_URL_LIGHT);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');
        if (!w.hfoPorts?.p1?.weave) throw new Error('missing hfoPorts.p1.weave');

        const href = String(window.location?.href || '');

        // Make the test deterministic and fast.
        w.systemState.parameters.landmarks.numHands = 1;
        w.systemState.parameters.fsm.hysteresisHigh = 0.88;
        // Keep COAST stable for the test: avoid COAST->IDLE so we can assert drain-only behavior.
        w.systemState.parameters.fsm.hysteresisLow = 0.0;
        w.systemState.parameters.fsm.chargeTimeMs = 50;
        w.systemState.parameters.fsm.releaseTimeMs = 200;
        // Keep COAST from decaying to IDLE during this test window.
        w.systemState.parameters.fsm.coastDrainTimeMs = 5000;
        w.systemState.parameters.readiness.fillMultiplier = 2.0;
        w.systemState.parameters.readiness.drainMultiplier = 1.0;
        w.systemState.parameters.readiness.coastDrainMultiplier = 1.0;

        // Force entry into COAST with some readiness available to drain.
        w.systemState.p1.fsmStates[0] = 'COAST';
        w.systemState.p1.readinessScores[0] = 0.9;

        const initial = {
            href,
            fsm: String(w.systemState.p1.fsmStates[0] || ''),
            readiness: Number(w.systemState.p1.readinessScores[0] || 0),
        };

        const dummyLandmarks = () => Array.from({ length: 21 }, (_, j) => ({
            x: 0.5 + (j % 5) * 0.002,
            y: 0.5 + Math.floor(j / 5) * 0.002,
            z: 0,
        }));

        const buildResults = (nowMs: number) => ({
            landmarks: [dummyLandmarks()],
            gestures: [[{ categoryName: 'Pointing_Up', score: 1.0 }]],
            __hfoReplayHands: [{
                handIndex: 0,
                present: true,
                // Intentionally "best case" signals that would normally charge readiness.
                isFacingCamera: true,
                isCharging: true,
                hasConfidence: true,
                shouldFill: true,
                isPointing: true,
                categoryName: 'Pointing_Up',
                confidence: 1.0,
            }],
        });

        const frames: Array<{ now: number; dt: number; fsm: string; readiness: number }> = [];
        let now = 1000;

        for (let k = 0; k < 12; k++) {
            const dt = 16;
            now += dt;
            w.hfoPorts.p1.weave(buildResults(now), dt, now);
            const fsm = String(w.systemState.p1.fsmStates[0] || '');
            const readiness = Number(w.systemState.p1.readinessScores[0] || 0);

            frames.push({
                now,
                dt,
                fsm,
                readiness,
            });

            // Only assert COAST semantics. If COAST exits, stop the experiment window.
            if (fsm !== 'COAST') break;
        }

        return { initial, frames };
    }, null as any);

    // Sanity: test must be running against v16.1.
    expect(out.initial.href).toContain('omega_gen6_v16_1.html');

    // COAST must never arm.
    for (const f of out.frames) {
        expect(f.fsm, `frames=${JSON.stringify(out.frames)}`).toBe('COAST');
    }

    // Readiness must be monotonic non-increasing while COAST remains active.
    // (If it decays to IDLE, readiness should be ~0 by then; still should not increase.)
    for (let i = 1; i < out.frames.length; i++) {
        expect(out.frames[i].readiness).toBeLessThanOrEqual(out.frames[i - 1].readiness + 1e-9);
    }
});
