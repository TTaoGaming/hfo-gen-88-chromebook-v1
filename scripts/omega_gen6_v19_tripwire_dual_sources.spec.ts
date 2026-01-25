// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V19_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V19_TEST_URL_LIGHT}`
    + '&flag-p3-tripwire-injector=false'
    + '&flag-p3-tripwire-injector-static=true'
    + '&flag-p3-tripwire-injector-knuckle=false'
    + '&flag-p2-tripwire-static=true'
    + '&flag-p2-tripwire-knuckle=true';

test('Gen6 v19: P3 routes tripwire injection by sensorId', async ({ hfoPage }) => {
    await safeGoto(hfoPage, GEN6_URL);
    await hfoPage.waitForTimeout(250);

    const out = await safeEvaluate(hfoPage, () => {
        const w = window as any;
        if (!w.systemState) throw new Error('missing systemState');
        if (!w.hfoPortsEffects?.emit) throw new Error('missing hfoPortsEffects.emit');
        if (!w.hfoP3PlanckSensorInjector?.start) throw new Error('missing hfoP3PlanckSensorInjector');

        const p3Events: Array<{ port: string; type: string; payload: any }> = [];
        const deliverCalls: Array<{ adapterId: string; payload: any }> = [];

        // Capture p3 bus events deterministically.
        const unsubscribe = w.hfoPortsEffects?.subscribe
            ? w.hfoPortsEffects.subscribe((entry: any) => {
                if (entry?.port === 'p3') p3Events.push({ port: entry.port, type: entry.type, payload: entry.payload });
            })
            : null;

        // Stub effect delivery so we don't depend on Dino iframe state.
        w.hfoAdapterHost = {
            deliverEffect: (adapterId: string, payload: any) => {
                deliverCalls.push({ adapterId, payload });
                return true;
            },
        };
        w.P3InjectorPort = {
            sendNematocystToDino: (payload: any) => {
                deliverCalls.push({ adapterId: 'P3InjectorPort', payload });
                return true;
            },
        };

        // Ensure subscription is active after stubbing.
        try {
            w.hfoP3PlanckSensorInjector.start();
        } catch {
            // ignore
        }

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

        // Static source should inject (enabled by p3-tripwire-injector-static).
        w.hfoPortsEffects.emit('p2', 'tripwire_cross', {
            sensorId: 'static',
            handIndex: 0,
            pointerId: 77,
            fsmState: 'COMMIT',
            readiness: 0.95,
            now: 1000,
            direction: 'down',
            sensor: { phase: 'begin' },
        });

        // Knuckle source should NOT inject (disabled by p3-tripwire-injector-knuckle=false).
        w.hfoPortsEffects.emit('p2', 'tripwire_cross', {
            sensorId: 'knuckle',
            handIndex: 0,
            pointerId: 77,
            fsmState: 'COMMIT',
            readiness: 0.95,
            now: 1100,
            direction: 'cross',
            sensor: { phase: 'begin' },
        });

        if (typeof unsubscribe === 'function') {
            try {
                unsubscribe();
            } catch {
                // ignore
            }
        }

        const tripwireInjects = p3Events.filter((e) => e?.port === 'p3' && e?.type === 'tripwire_inject');
        return {
            deliverCalls,
            tripwireInjects,
        };
    }, null);

    expect(out.deliverCalls.length, `Expected exactly 1 delivered effect, got=${JSON.stringify(out.deliverCalls)}`).toBe(1);
    expect(out.deliverCalls[0]?.adapterId).toBe('dino-v1');

    const injects = out.tripwireInjects || [];
    expect(injects.length, `Expected at least one p3/tripwire_inject event, got=${JSON.stringify(out.tripwireInjects)}`).toBeGreaterThanOrEqual(1);
    expect(String(injects[0]?.payload?.sensorId || '')).toBe('static');
});
