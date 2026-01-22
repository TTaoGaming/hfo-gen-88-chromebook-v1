// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v10_1.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

function withFlag(urlStr: string, key: string, value: string) {
    const url = new URL(urlStr);
    url.searchParams.set(`flag-${key}`, value);
    return url.toString();
}

test('Gen5 v10.1 P1 ports: weave produces fabric + envelope', async ({ hfoPage }) => {
    await hfoPage.goto(withFlag(GEN5_URL, 'p1-ports', 'true'));
    await hfoPage.initHFO();

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        if (!window.hfoEval) throw new Error('hfoEval not available');
        // @ts-ignore
        if (!window.hfoPorts?.p1?.weave) throw new Error('Ports.p1.weave not available');

        const landmarks = Array.from({ length: 21 }, (_, i) => ({
            x: 0.4 + i * 0.001,
            y: 0.5 + i * 0.001,
            z: 0
        }));

        const results = {
            landmarks: [landmarks],
            gestures: [[]]
        };

        // @ts-ignore
        return window.hfoPorts.p1.weave(results, 16, performance.now());
    });

    expect(out?.dataFabric?.frameId).toBeGreaterThan(0);

    // Envelope is optional but should exist when P1 succeeds.
    expect(out?.envelope).toBeTruthy();
    expect(out?.envelope?.specversion).toBeTruthy();
    expect(out?.envelope?.id).toBeTruthy();
    expect(out?.envelope?.type).toBe('hfo.gen5.p1.fuse');
    expect(out?.envelope?.source).toBeTruthy();
    expect(out?.envelope?.time).toBeTruthy();

    // Ensure data is the canonical DataFabric.
    expect(out?.envelope?.data?.frameId).toBe(out?.dataFabric?.frameId);
});
