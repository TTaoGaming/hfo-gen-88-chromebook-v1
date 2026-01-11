// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

test('V42 Omega Interaction: Hero Button and Gesture Lock', async ({ hfoPage }) => {
    const url = 'http://localhost:8080/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v42.html';
    await hfoPage.goto(url);

    // 1. Verify Hero Button is present
    const heroBtn = hfoPage.locator('#hero-button');
    await expect(heroBtn).toBeVisible({ timeout: 10000 });

    // 2. Click Hero Button to unlock
    await heroBtn.click();
    await expect(heroBtn).not.toBeVisible();

    // 3. Wait for HFO to initialize
    await hfoPage.initHFO();
    await hfoPage.waitForHand(0);

    // 4. Verification: Check if Port 0 is sensing
    const handState = await hfoPage.getHandState(0);
    console.log(`V42 E2E: Hand 0 state after unlock: ${JSON.stringify(handState)}`);
    expect(handState).not.toBeNull();
});
