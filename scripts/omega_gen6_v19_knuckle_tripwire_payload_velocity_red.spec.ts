// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V19_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// TDD (was RED): lock in knuckle tripwire payload semantics (sensorId + cursor-style velocities).

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V19_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-p3-tripwire-injector-static=false'
    + '&flag-p3-tripwire-injector-knuckle=false'
    + '&flag-ui-knuckle-tripwire-panel=false';

test('Gen6 v19 (TDD): knuckle tripwire emits p2/tripwire_cross with sensorId=knuckle and nonzero vy', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');
        if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
        if (!w.hfoP2KnuckleTripwireThread?.debugEvaluate) throw new Error('missing hfoP2KnuckleTripwireThread.debugEvaluate');

        const mkLandmarks = (tipY: number) => {
            // Minimal deterministic geometry for signedLineFeature2D:
            // a=(0,0), b=(1,0) => feature = tip.y.
            const pts = Array.from({ length: 21 }, () => ({ x: 0, y: 0, z: 0 }));
            pts[5] = { x: 0, y: 0, z: 0 }; // index_mcp
            pts[17] = { x: 1, y: 0, z: 0 }; // pinky_mcp
            pts[8] = { x: 0.5, y: tipY, z: 0 }; // index_tip
            return pts;
        };

        const captured: any[] = [];
        const unsub = w.hfoPortsEffects.subscribe((entry: any) => {
            if (entry?.port !== 'p2') return;
            if (entry?.type !== 'tripwire_cross') return;
            if (String(entry?.payload?.sensorId || '') !== 'knuckle') return;
            captured.push(entry.payload);
        }, 'p2');

        const handIndex = 0;
        const pointerId = 77;

        // First tick: establish previous cursor position/time and keep pressed=false (tipY=0 => below on threshold).
        w.hfoP2KnuckleTripwireThread.debugEvaluate({
            now: 1000,
            dt: 16,
            handIndex,
            pointerId,
            readinessScore: 0.9,
            fsmState: 'COMMIT',
            uiNormX: 0.5,
            uiNormY: 0.2,
            landmarks: mkLandmarks(0.0),
        });

        // Second tick: move cursor downward in uiNormY and cross the feature threshold (tipY=0.02) => begin event.
        w.hfoP2KnuckleTripwireThread.debugEvaluate({
            now: 1100,
            dt: 16,
            handIndex,
            pointerId,
            readinessScore: 0.9,
            fsmState: 'COMMIT',
            uiNormX: 0.5,
            uiNormY: 0.8,
            landmarks: mkLandmarks(0.02),
        });

        try {
            if (typeof unsub === 'function') unsub();
        } catch {
            // ignore
        }

        const last = captured[captured.length - 1] || null;
        return { captured, last };
    }, null);

    expect(out.captured.length, `Expected at least one knuckle tripwire_cross, got=${JSON.stringify(out.captured)}`).toBeGreaterThanOrEqual(1);

    const last = out.last as any;
    expect(String(last.sensorId || '')).toBe('knuckle');
    expect(String(last.fsmState || '')).toBe('COMMIT');

    // uiNormY moved from 0.2 -> 0.8 over 100ms => vy ~= +6.0 uiNorm/s.
    expect(Number.isFinite(last.vyUiNormPerS)).toBe(true);
    expect(Math.abs(Number(last.vyUiNormPerS) - 6.0)).toBeLessThanOrEqual(0.25);
    expect(Number(last.speedUiNormPerS)).toBeGreaterThan(0);
});
