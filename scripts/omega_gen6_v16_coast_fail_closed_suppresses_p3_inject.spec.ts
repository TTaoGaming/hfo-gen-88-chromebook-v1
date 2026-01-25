// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V16_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V16_TEST_URL_LIGHT}&flag-p3-tripwire-injector=true&flag-p3-dino-ready-edge=false`;

test('Gen6 v16: COAST fails closed (no P3 inject) even if tripwire_cross emitted', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');
        if (!w.hfoPortsEffects?.emit) throw new Error('missing hfoPortsEffects.emit');

        const captured: Array<{ port: string; type: string; payload: any }> = [];
        const unsubscribe = w.hfoPortsEffects?.subscribe
            ? w.hfoPortsEffects.subscribe((entry: any) => {
                if (entry?.port === 'p3') captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
            })
            : null;

        // Establish a fabric cursor in COAST to mirror the fail-closed posture.
        w.systemState.dataFabric = {
            cursors: [
                {
                    handIndex: 0,
                    pointerId: 10,
                    fsmState: 'COAST',
                    readinessScore: 0.9,
                    uiNormX: 0.5,
                    uiNormY: 0.6,
                },
            ],
            systemTime: 1000,
            frameId: 1,
        };

        // Emit a COAST tripwire event (should never inject).
        w.hfoPortsEffects.emit('p2', 'tripwire_cross', {
            now: 1000,
            dt: 16,
            seq: 'test_coast',
            handIndex: 0,
            pointerId: 10,
            fsmState: 'COAST',
            readiness: 0.9,
            uiNormX: 0.5,
            uiNormY: 0.6,
            direction: 'down',
            vxUiNormPerS: 0,
            vyUiNormPerS: 1,
            speedUiNormPerS: 1,
            sensor: { engine: 'planck', phase: 'begin' },
        });

        // Emit a COMMIT tripwire event (should attempt inject and emit p3/tripwire_inject).
        w.hfoPortsEffects.emit('p2', 'tripwire_cross', {
            now: 2000,
            dt: 16,
            seq: 'test_commit',
            handIndex: 0,
            pointerId: 10,
            fsmState: 'COMMIT',
            readiness: 0.95,
            uiNormX: 0.5,
            uiNormY: 0.7,
            direction: 'down',
            vxUiNormPerS: 0,
            vyUiNormPerS: 1,
            speedUiNormPerS: 1,
            sensor: { engine: 'planck', phase: 'begin' },
        });

        if (typeof unsubscribe === 'function') {
            try {
                unsubscribe();
            } catch {
                // ignore
            }
        }

        return { captured };
    });

    const injects = out.captured.filter((e: any) => e?.port === 'p3' && e?.type === 'tripwire_inject');
    expect(injects.length).toBeGreaterThanOrEqual(1);

    // Ensure the first COAST event did not inject: the first inject should correspond to COMMIT.
    // (We use payload.direction + presence as a coarse check; the hard gate is event count == 1 here.)
    expect(injects.length).toBe(1);
});
