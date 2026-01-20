// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v4.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

test('Gen5 readiness energy multipliers apply (v4)', async ({ hfoPage }) => {
    await hfoPage.goto(GEN5_URL);
    await hfoPage.initHFO();

    const baseline = await hfoPage.evaluate(() => {
        // @ts-ignore
        window.hfoEval.setReadinessScore(0, 0.5);
        // @ts-ignore
        return window.hfoEval.drainReadiness(0, 200, true);
    });

    const boosted = await hfoPage.evaluate(() => {
        // @ts-ignore
        window.hfoEval.setReadinessScore(0, 0.5);
        // @ts-ignore
        window.hfoEval.setReadinessParams({ drainMultiplier: 2.0, coastDrainMultiplier: 2.0 });
        // @ts-ignore
        return window.hfoEval.drainReadiness(0, 200, true);
    });

    expect(boosted).toBeLessThan(baseline);

    const filled = await hfoPage.evaluate(() => {
        // @ts-ignore
        window.hfoEval.setReadinessScore(0, 0);
        // @ts-ignore
        window.hfoEval.setReadinessParams({ fillMultiplier: 2.0 });
        // @ts-ignore
        return window.hfoEval.fillReadiness(0, 200);
    });

    expect(filled).toBeGreaterThan(0);
});
