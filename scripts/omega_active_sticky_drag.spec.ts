// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';

test('V41: FSM Intent Recognition (Direct FSM Test)', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);
  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  // 1. Initial State: IDLE
  let state = await hfoPage.getHandState(0);
  expect(state.state).toBe('IDLE');

  // 2. Mock FSM Process
  const results = await hfoPage.evaluate(() => {
    // @ts-ignore
    const h = window.hfoState.hands[0];
    const now = performance.now();
    const r1 = h.fsm.process('None', now, 0.9, true); // Still IDLE (Dwell starts)
    const r1_2 = h.fsm.process('None', now + 1000, 0.9, true); // Pass 800ms -> PORT_0_POINTER_READY
    const r2 = h.fsm.process('Pointing_Up', now + 1010, 0.9, true); // PORT_0_POINTER_READY -> PORT_7_POINTER_COMMITTED (High Confidence)
    const r3 = h.fsm.process('Pointing_Up', now + 1020, 0.9, true); // Stay PORT_7_POINTER_COMMITTED
    return { r1, r1_2, r2, r3 };
  });

  expect(results.r1.state).toBe('IDLE');
  expect(results.r1_2.state).toBe('PORT_0_POINTER_READY');
  expect(results.r2.state).toBe('PORT_7_POINTER_COMMITTED');
  expect(results.r2.pointerEvent).toBe('pointerdown');
  expect(results.r3.state).toBe('PORT_7_POINTER_COMMITTED');
});

test('V41: Release Logic (Direct FSM Test)', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);
  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  const results = await hfoPage.evaluate(() => {
    // @ts-ignore
    const h = window.hfoState.hands[0];
    const now = performance.now();
    h.fsm.state = 'PORT_7_POINTER_COMMITTED';
    h.fsm.dwellAccumulator = 1000;
    const r1 = h.fsm.process('Open_Palm', now, 0.9, true); // PORT_7_POINTER_COMMITTED -> PORT_0_POINTER_READY (Facing)
    return { r1 };
  });

  expect(results.r1.state).toBe('PORT_0_POINTER_READY');
  expect(results.r1.pointerEvent).toBe('pointerup');
});

test('V41: Stickiness through NONE and Frame Drops', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);
  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  const results = await hfoPage.evaluate(() => {
    // @ts-ignore
    const h = window.hfoState.hands[0];
    const now = performance.now();
    h.fsm.state = 'PORT_7_POINTER_COMMITTED';
    h.fsm.dwellAccumulator = 1000;

    // 1. Pointing stays Pointing
    const r1 = h.fsm.process('Pointing_Up', now + 10, 0.9, true);

    // 2. 'None' gesture stays committed (Sticky)
    const r2 = h.fsm.process('None', now + 20, 0.9, true);

    // 3. 'LOST' frame stays committed (Sticky)
    const r3 = h.fsm.process('LOST', now + 30, 0, false);

    // 4. Turning palm away (isPalmFacing=false) stays committed TEMPORARILY (Leaky Bucket)
    const r4 = h.fsm.process('Pointing_Up', now + 40, 0.9, false);

    // 5. Sustained lack of palm leads to exit
    const r5 = h.fsm.process('Pointing_Up', now + 1000, 0.9, false);

    return { r1, r2, r3, r4, r5 };
  });

  expect(results.r1.state).toBe('PORT_7_POINTER_COMMITTED');
  expect(results.r2.state).toBe('PORT_7_POINTER_COMMITTED');
  expect(results.r3.state).toBe('PORT_7_POINTER_COMMITTED');
  expect(results.r4.state).toBe('PORT_7_POINTER_COMMITTED');
  expect(results.r5.state).toBe('IDLE');
  expect(results.r5.pointerEvent).toBe('pointercancel');
});

test('V41: Return to READY on Any Other Gesture', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);
  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  const results = await hfoPage.evaluate(() => {
    // @ts-ignore
    const h = window.hfoState.hands[0];
    const now = performance.now();
    h.fsm.state = 'PORT_7_POINTER_COMMITTED';
    h.fsm.dwellAccumulator = 1000;

    // Changing to 'Open_Palm' (a high-confidence non-pointing gesture)
    const r1 = h.fsm.process('Open_Palm', now, 0.9, true);
    return { r1 };
  });

  expect(results.r1.state).toBe('PORT_0_POINTER_READY');
  expect(results.r1.pointerEvent).toBe('pointerup');
});
