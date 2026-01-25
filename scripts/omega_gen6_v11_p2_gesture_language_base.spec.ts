// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_URL =
    process.env.HFO_GEN6_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v11.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&mode=dev';

test('Gen6 v11: P2 gesture language base composes zone + contact adapters', async ({ hfoPage }) => {
    await hfoPage.goto(GEN6_URL, { waitUntil: 'domcontentloaded' });
    await hfoPage.waitForTimeout(200);

    const out = await hfoPage.evaluate(() => {
        const w = window as any;
        if (!w.hfoP2GestureLanguage?.debugEvaluate) throw new Error('missing hfoP2GestureLanguage.debugEvaluate');

        const mkLandmarks = () => {
            const lms = Array.from({ length: 21 }, () => ({ x: 0.5, y: 0.5, z: 0 }));
            // Thumb tip (4) and index tip (8) close enough to trigger contact.
            lms[4] = { x: 0.5, y: 0.5, z: 0 };
            lms[8] = { x: 0.515, y: 0.5, z: 0 };
            // Knuckle line points (5, 17) in a stable pose.
            lms[5] = { x: 0.45, y: 0.55, z: 0 };
            lms[17] = { x: 0.55, y: 0.55, z: 0 };
            return lms;
        };

        return w.hfoP2GestureLanguage.debugEvaluate({
            handIndex: 0,
            fsmState: 'READY',
            readinessScore: 0.95,
            // Center zone: should trigger zone_enter.
            uiNormX: 0.5,
            uiNormY: 0.5,
            landmarks: mkLandmarks(),
            now: performance.now(),
            dt: 16,
        });
    });

    const p2Events: Array<{ type: string; payload: any }> = out?.p2Events || [];
    const eventTypes = new Set(p2Events.map((e) => e.type));

    expect(eventTypes.has('zone_enter'), 'Expected SpatialZonesAdapter zone_enter').toBeTruthy();
    expect(eventTypes.has('contact_down'), 'Expected ContactSubstrateAdapter contact_down').toBeTruthy();

    const p3Payloads: any[] = out?.p3Payloads || [];
    expect(p3Payloads.length, 'Expected at least one P3 payload candidate').toBeGreaterThan(0);
});
