// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect, getActiveUrl } from './hfo_fixtures';

test('V40: FSM Intent Recognition (Direct FSM Test)', async ({ hfoPage }) => {
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
    const r1 = h.fsm.process('Open_Palm', now, 0.9, true); // IDLE -> TRANSITION
    const r2 = h.fsm.process('Open_Palm', now + 300, 0.9, true); // TRANSITION -> ARMED
    const r3 = h.fsm.process('Pointing_Up', now + 400, 0.9, true); // ARMED -> COMMITTED
    return { r1, r2, r3 };
  });

  expect(results.r1.state).toBe('TRANSITION');
  expect(results.r2.state).toBe('ARMED');
  expect(results.r3.state).toBe('COMMITTED');
  expect(results.r3.pointerEvent).toBe('pointerdown');
});

test('V40: Release Logic (Direct FSM Test)', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);
  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  const results = await hfoPage.evaluate(() => {
    // @ts-ignore
    const h = window.hfoState.hands[0];
    const now = performance.now();
    h.fsm.state = 'COMMITTED';
    const r1 = h.fsm.process('Open_Palm', now, 0.9, true); // COMMITTED -> ARMED
    return { r1 };
  });

  expect(results.r1.state).toBe('ARMED');
  expect(results.r1.pointerEvent).toBe('pointerup');
});

test('V40: Global Departure (Direct FSM Test)', async ({ hfoPage }) => {
  const url = getActiveUrl();
  await hfoPage.goto(url);
  await hfoPage.initHFO();
  await hfoPage.waitForHand(0);

  const results = await hfoPage.evaluate(() => {
    // @ts-ignore
    const h = window.hfoState.hands[0];
    const now = performance.now();
    h.fsm.state = 'COMMITTED';
    const r1 = h.fsm.process('Pointing_Up', now, 0.9, false); // Departure Start
    const r2 = h.fsm.process('Pointing_Up', now + 1000, 0.9, false); // Departure Complete -> IDLE
    return { r1, r2 };
  });

  expect(results.r1.state).toBe('COMMITTED');
  expect(results.r2.state).toBe('IDLE');
  expect(results.r2.pointerEvent).toBe('pointercancel');
});
