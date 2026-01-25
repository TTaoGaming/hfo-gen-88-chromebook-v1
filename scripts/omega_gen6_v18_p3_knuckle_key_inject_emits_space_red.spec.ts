// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V18_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED until v18 exists:
// P3 should listen for p2/knuckle_keypress begin (COMMIT-only) and emit p3/knuckle_key_inject for Dino (Space).

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V18_TEST_URL_LIGHT}`
    + '&flag-p3-knuckle-key-injector=true'
    + '&flag-p2-knuckle-keybar=false'
    + '&flag-ui-knuckle-keybar-overlay=false';

test('Gen6 v18 (TDD RED): P3 emits p3/knuckle_key_inject on COMMIT p2/knuckle_keypress begin', async ({ hfoPage }) => {
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

        // Establish a fabric cursor in COMMIT (injector policy is COMMIT-only).
        w.systemState.dataFabric = {
            cursors: [
                {
                    handIndex: 0,
                    pointerId: 77,
                    fsmState: 'COMMIT',
                    readinessScore: 0.95,
                    isPalmFacing: true,
                    uiNormX: 0.5,
                    uiNormY: 0.6,
                },
            ],
            systemTime: 1000,
            frameId: 1,
        };

        w.hfoPortsEffects.emit('p2', 'knuckle_keypress', {
            handIndex: 0,
            pointerId: 77,
            finger: 'index',
            fsmState: 'COMMIT',
            readinessScore: 0.95,
            isPalmFacing: true,
            curl: 0.9,
            knuckleAngleDeg: 10,
            timestampMs: 1000,
            phase: 'begin',
        });

        if (typeof unsubscribe === 'function') {
            try {
                unsubscribe();
            } catch {
                // ignore
            }
        }

        return { captured };
    }, null);

    const injects = out.captured.filter((e: any) => e?.port === 'p3' && e?.type === 'knuckle_key_inject');

    // RED until v18 injector exists.
    expect(injects.length, `Expected at least one p3/knuckle_key_inject, got=${JSON.stringify(out.captured)}`).toBeGreaterThanOrEqual(1);

    const payload = injects[0]?.payload || {};
    expect(String(payload.adapterId || '')).toBe('dino-v1');
    expect(String(payload.payload?.code || '')).toBe('Space');
});
