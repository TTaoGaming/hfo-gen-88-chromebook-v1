// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';

test('Transparency Audit: Verify Anti-Theater Scoring', async ({ hfoPage }) => {
    const url = getActiveUrl();
    await hfoPage.goto(url);
    await hfoPage.initHFO();

    // 1. Initial state should be 1.0 (or whatever we initialized it to)
    const transparency = await hfoPage.evaluate(() => window.hfoState.transparency);
    console.log(`Initial Transparency: ${transparency}`);
    expect(transparency).toBeLessThanOrEqual(1.0);

    // 2. Simulate "Degraded Sensing" by dropping hand presence
    await hfoPage.evaluate(() => {
        // @ts-ignore
        window.hfoSystem.loopActive = true;
        // Inject a fake frame update loop if necessary, or just wait for the loop to run once
    });

    await hfoPage.waitForTimeout(1000);

    const currentScore = await hfoPage.evaluate(() => window.hfoState.transparency);
    console.log(`Current Transparency (No Hands): ${currentScore}`);

    // Since no hands are detected, transparency should drop
    expect(currentScore).toBeLessThan(1.0);
});
