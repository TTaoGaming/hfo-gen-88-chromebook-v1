// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';

/**
 * V38: FSM Predict and Confirm Lifecycle
 * Verifies the new NONE-to-CLICK and RELEASING->REGULATORY behaviors.
 */
test('V38: FSM Intent Recognition (NONE -> COMMITTING -> COMMITTED)', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);

  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  // 1. Enter ARMED (Palm Facing)
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('OPEN_PALM', now, 0.9, true);
  });
  
  await hfoPage.waitForTimeout(400); // Wait for arming threshold
  
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('OPEN_PALM', now, 0.9, true); // Second call to process the time delta
  });

  let state = await hfoPage.getHandState(0);
  expect(state.state).toBe('ARMED');

  // 2. Intent Prediction: Detect NONE gesture
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('NONE', now, 0.8, true);
  });

  state = await hfoPage.getHandState(0);
  expect(state.state).toBe('COMMITTING');
  expect(state.event).toBe('pointermove');

  // 3. Confirm: POINTING_UP high confidence
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('POINTING_UP', now, 0.9, true);
  });

  state = await hfoPage.getHandState(0);
  expect(state.state).toBe('COMMITTED');
  expect(state.event).toBe('pointerdown');
  console.log('V38: Intent confirmed (NONE -> COMMITTING -> COMMITTED) (PASS)');
});

test('V38: Direct Commit (ARMED -> COMMITTED)', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);

  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  // 1. Enter ARMED
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('OPEN_PALM', now, 0.9, true);
    hand.fsm.process('OPEN_PALM', now + 400, 0.9, true);
  });

  // 2. High confidence POINTING_UP transitions through COMMITTING
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('POINTING_UP', now + 500, 0.9, true); 
  });

  let state = await hfoPage.getHandState(0);
  expect(state.state).toBe('COMMITTING');

  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('POINTING_UP', now + 700, 0.9, true); // After > 150ms
  });

  state = await hfoPage.getHandState(0);
  expect(state.state).toBe('COMMITTED');
  console.log('V38: Direct commit flow (via COMMITTING) verified (PASS)');
});

test('V38: RELEASING Ambiguity Resolution (Re-grip vs Confirm)', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);

  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  // 1. Manually set to COMMITTED
  await hfoPage.injectHand(0, { active: true, state: 'COMMITTED', event: 'pointerdown' });

  // 2. Gesture moves to NONE -> Enter RELEASING
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('NONE', now, 0.8, true);
  });

  let state = await hfoPage.getHandState(0);
  expect(state.state).toBe('RELEASING');

  // 3. Re-grip check: POINTING_UP should return to COMMITTED
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('POINTING_UP', now, 0.9, true);
  });

  state = await hfoPage.getHandState(0);
  expect(state.state).toBe('COMMITTED');

  // 4. Actual Release check: OPEN_PALM
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('NONE', now, 0.8, true); // Back to RELEASING
  });

  await hfoPage.waitForTimeout(100);

  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('OPEN_PALM', now, 0.9, true);
  });

  state = await hfoPage.getHandState(0);
  expect(state.state).toBe('ARMED');
  expect(state.event).toBe('pointerup');
  console.log('V38: Release resolution verified (PASS)');
});

test('V38: Global Departure Bucket', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);

  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  // 1. Set to ARMED
  await hfoPage.injectHand(0, { active: true, state: 'ARMED', event: 'pointermove' });

  // 2. Palm leaves zone (isPalmFacing = false)
  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('POINTING_UP', now, 0.9, false);
  });

  let state = await hfoPage.getHandState(0);
  expect(state.state).toBe('ARMED'); // Still ARMED due to bucket

  // Wait 900ms (Bucket 800ms)
  await hfoPage.waitForTimeout(900);

  await hfoPage.evaluate(() => {
    // @ts-ignore
    const hand = window.hfoState.hands[0];
    const now = performance.now();
    hand.fsm.process('POINTING_UP', now, 0.9, false);
  });

  state = await hfoPage.getHandState(0);
  expect(state.state).toBe('IDLE');
  console.log('V38: Global departure bucket verified (PASS)');
});
