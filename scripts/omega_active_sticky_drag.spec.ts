// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';

/**
 * V33 Sticky Drag: 1s Coastal Persistence Verification
 * Verifies that the FSM stays in COMMITTED during tracking loss for up to 1000ms.
 */
test('V33: 1s Persistence (Sticky Drag) during Tracking Loss', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);

  // 1. Initialize
  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  // 2. Start a drag (COMMITTED)
  await hfoPage.injectHand(0, {
    active: true,
    state: 'COMMITTED',
    event: 'pointerdown'
  });

  // Verify it's committed
  let state = await hfoPage.getHandState(0);
  expect(state.state).toBe('COMMITTED');

  // 3. Simulate "LOST" tracking
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('LOST', now, 0);
  });

  // Wait 500ms (Halfway through persistence)
  await hfoPage.waitForTimeout(500);

  // Process 'LOST' again at +500ms
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('LOST', now, 0);
  });

  state = await hfoPage.getHandState(0);
  expect(state.state).toBe('COMMITTED');
  console.log('V33: State is still COMMITTED after 500ms tracking loss (PASS)');

  // 4. Wait another 600ms (Total 1100ms loss)
  await hfoPage.waitForTimeout(600);

  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('LOST', now, 0);
  });

  state = await hfoPage.getHandState(0);
  expect(state.state).toBe('IDLE');
  console.log('V33: State timed out to IDLE after 1100ms tracking loss (PASS)');
});
