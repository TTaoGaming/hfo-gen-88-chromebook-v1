// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v4.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

test('Gen5 readiness drain: COAST drains leaky bucket', async ({ hfoPage }) => {
    await hfoPage.goto(GEN5_URL);
    await hfoPage.initHFO();

    const readiness = await hfoPage.evaluate(() => {
        // @ts-ignore
        if (!window.hfoEval) throw new Error('hfoEval not available');
        // Seed readiness
        // @ts-ignore
        window.hfoEval.setReadinessScore(0, 0.8);
        // Drain using coast rate over 200ms
        // @ts-ignore
        return window.hfoEval.drainReadiness(0, 200, true);
    });

    expect(readiness).toBeLessThan(0.8);

    const drained = await hfoPage.evaluate(() => {
        // @ts-ignore
        window.hfoEval.setReadinessScore(0, 0.1);
        // @ts-ignore
        return window.hfoEval.drainReadiness(0, 1000, true);
    });

    expect(drained).toBe(0);
});
