// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V23_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { buildStepsFromFrames, tickThreadCapture } from './gen6_v23_red_helpers';
import { SwordBabylonMarkerV23Schema, SwordTouch2dMarkerV23Schema } from '../contracts/hfo_ui_markers.zod';

// RED TDD/BDD: v23 adds specialized COMMIT gestures (Thumbs Up / Thumbs Down) to control a sticky
// Flaming Sword state-machine that persists across base FSM states.
//
// Requirements under test (RED-first):
// - In READY, holding a high-confidence Thumb_Up fills a leaky bucket meter (dwell+hysteresis).
// - When meter reaches full, sword becomes LOCKED and remains active even across IDLE/READY/COMMIT/COAST.
// - Sword only deactivates via a separate READY+Thumb_Down dwell (drain leaky bucket) until empty.
// - Parameters (fill/drain ms, thresholds) are user-tunable.
// - Visualization: when locked, a sword (Touch2D + Babylon) renders as an asymmetric knuckle triplane “blade”.

test.describe.configure({ mode: 'serial', retries: 0 });

const GEN6_URL = `${GEN6_V23_TEST_URL_LIGHT}`
  + '&flag-p2-tripwire-knuckle=true'
  + '&flag-p2-tripwire-static=false'
  + '&flag-ui-knuckle-tripwire-panel=false'
  // v23 feature flags (expected to be missing until implemented)
  + '&flag-p2-sword-meter=true'
  + '&flag-ui-knuckle-sword-touch2d=true'
  + '&flag-ui-knuckle-sword-babylon=true'
  + '&flag-ui-knuckle-sword-flames=true';

type Frame = {
  now: number;
  dt: number;
  fsmState: 'IDLE' | 'READY' | 'COMMIT' | 'COAST';
  gesture: string;
  confidence: number;
  isPalmFacing: boolean;
  uiNormX?: number;
  uiNormY?: number;
};

function makeFrames(opts: {
  startNow: number;
  dt: number;
  count: number;
  fsmState: Frame['fsmState'];
  gesture: string;
  confidence: number;
  isPalmFacing: boolean;
}): Frame[] {
  const out: Frame[] = [];
  for (let i = 0; i < opts.count; i++) {
    out.push({
      now: opts.startNow + i * opts.dt,
      dt: opts.dt,
      fsmState: opts.fsmState,
      gesture: opts.gesture,
      confidence: opts.confidence,
      isPalmFacing: opts.isPalmFacing,
      uiNormX: 0.55,
      uiNormY: 0.55,
    });
  }
  return out;
}

test('Gen6 v23 RED: READY + Thumb_Up dwell fills meter and locks sword (sticky across states)', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_URL);
  await hfoPage.waitForTimeout(250);

  const frames: Frame[] = [
    // Ensure we start in READY.
    ...makeFrames({ startNow: 1000, dt: 50, count: 4, fsmState: 'READY', gesture: 'None', confidence: 0.99, isPalmFacing: true }),
    // Thumbs-up dwell should fill the sword meter.
    ...makeFrames({ startNow: 1200, dt: 50, count: 16, fsmState: 'READY', gesture: 'Thumb_Up', confidence: 0.99, isPalmFacing: true }),
    // After lock, even IDLE should keep sword active.
    ...makeFrames({ startNow: 2000, dt: 50, count: 6, fsmState: 'IDLE', gesture: 'None', confidence: 0.99, isPalmFacing: true }),
  ];

  const steps = buildStepsFromFrames(frames);
  const out = await tickThreadCapture<any>(hfoPage, {
    threadName: 'hfoP2SwordMeterThread',
    steps,
    capturePorts: ['p2', 'p3'],
    snapPaths: [
      ['systemState', 'p2', 'swordMeter'],
      ['systemState', 'p2', 'sword'],
    ],
  });

  expect(out.hasThread, 'Expected window.hfoP2SwordMeterThread.tick to exist (v23).').toBe(true);
  expect(out.snap, 'Expected systemState.p2.swordMeter (or p2.sword) snapshot to exist (v23).').toBeTruthy();

  expect(out.snap?.active, 'Expected sword to be active after Thumb_Up dwell.').toBe(true);
  expect(out.snap?.locked, 'Expected sword to be locked (sticky) after filling meter.').toBe(true);
  expect(out.snap?.meter01, 'Expected meter01 to be present and finite.').not.toBeUndefined();
  expect(Number.isFinite(Number(out.snap?.meter01))).toBe(true);
  expect(Number(out.snap?.meter01), 'Expected meter01 >= 1.0 at lock (or clamped to 1).').toBeGreaterThanOrEqual(1);

  // Visual posture: when locked, sword should prefer asymmetric extension (A != B) and expose the values.
  if (out.snap?.extensionFracA !== undefined || out.snap?.extensionFracB !== undefined) {
    expect(out.snap?.extensionFracA).not.toBeUndefined();
    expect(out.snap?.extensionFracB).not.toBeUndefined();
    expect(Number(out.snap?.extensionFracA)).not.toBe(Number(out.snap?.extensionFracB));
  }

  // Expect at least one P2 event indicating sword state changes (contract to be defined in v23).
  const swordEvents = out.captured.filter((e: any) => e?.port === 'p2' && String(e?.type || '').includes('sword'));
  expect(swordEvents.length, `Expected >=1 p2:*sword* event; got=${JSON.stringify(out.captured)}`).toBeGreaterThanOrEqual(1);
});

test('Gen6 v23 RED: sword only deactivates via READY + Thumb_Down dwell drain (not by leaving COMMIT)', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_URL);
  await hfoPage.waitForTimeout(250);

  const frames: Frame[] = [
    // Fill/lock via Thumb_Up
    ...makeFrames({ startNow: 1000, dt: 50, count: 16, fsmState: 'READY', gesture: 'Thumb_Up', confidence: 0.99, isPalmFacing: true }),
    // Wander through other states; lock should persist.
    ...makeFrames({ startNow: 1800, dt: 50, count: 4, fsmState: 'COMMIT', gesture: 'Pointing_Up', confidence: 0.99, isPalmFacing: true }),
    ...makeFrames({ startNow: 2000, dt: 50, count: 6, fsmState: 'COAST', gesture: 'None', confidence: 0.1, isPalmFacing: false }),
    ...makeFrames({ startNow: 2300, dt: 50, count: 6, fsmState: 'IDLE', gesture: 'None', confidence: 0.99, isPalmFacing: true }),
    // Drain via Thumb_Down dwell
    ...makeFrames({ startNow: 2800, dt: 50, count: 20, fsmState: 'READY', gesture: 'Thumb_Down', confidence: 0.99, isPalmFacing: true }),
  ];

  const steps = buildStepsFromFrames(frames.map((f) => ({ ...f, uiNormX: 0.5, uiNormY: 0.5 })));
  const out = await tickThreadCapture<any>(hfoPage, {
    threadName: 'hfoP2SwordMeterThread',
    steps,
    snapPaths: [
      ['systemState', 'p2', 'swordMeter'],
      ['systemState', 'p2', 'sword'],
    ],
  });

  expect(out.hasThread, 'Expected window.hfoP2SwordMeterThread.tick to exist (v23).').toBe(true);
  expect(out.snap, 'Expected systemState.p2.swordMeter (or p2.sword) snapshot to exist (v23).').toBeTruthy();

  // After drain, sword should be inactive.
  expect(out.snap?.active, 'Expected sword inactive after Thumb_Down dwell drain.').toBe(false);
  expect(out.snap?.locked, 'Expected sword unlocked after drain.').toBe(false);
});

test('Gen6 v23 RED: when sword locked, Touch2D/Babylon expose a visible "flaming sword" marker', async ({ hfoPage }) => {
  const urlWithEngines = `${GEN6_URL}`
    .replace('flag-engine-babylon=false', 'flag-engine-babylon=true')
    .replace('flag-engine-canvas=false', 'flag-engine-canvas=true');

  await safeGoto(hfoPage, urlWithEngines);
  await hfoPage.waitForTimeout(500);

  const lockFrames: Frame[] = makeFrames({
    startNow: 1000,
    dt: 50,
    count: 40,
    fsmState: 'READY',
    gesture: 'Thumb_Up',
    confidence: 0.99,
    isPalmFacing: true,
  });
  const lockSteps = buildStepsFromFrames(lockFrames);

  const out = await safeEvaluate(hfoPage, (payload: { lockSteps: Array<{ now: number; dt: number; dataFabric: any }> }) => {
    const w = window as any;
    const state = w.systemState;

    // v23 contract: lock the sword (READY+Thumb_Up dwell) before checking visual markers.
    const meter = w.hfoP2SwordMeterThread;
    const hasThread = !!meter?.tick;
    if (hasThread) {
      for (const s of payload.lockSteps) {
        try { meter.tick({ now: Number(s.now), dt: Number(s.dt), dataFabric: s.dataFabric }); } catch { }
      }
    }

    const snap = state?.p2?.swordMeter || state?.p2?.sword || null;
    // v23 visual contract (proposed): these markers exist when the sword is active/locked.
    // The exact implementation can differ (DOM, Babylon mesh, debug registry), but it must be inspectable.
    return {
      hasThread,
      locked: !!snap?.locked,
      touch2dMarker: w.__hfoSwordTouch2dMarker ?? null,
      babylonMarker: w.__hfoSwordBabylonMarker ?? null,
      swordMeshName: w.__hfoSwordMeshName ?? null,
    };
  }, { lockSteps });

  expect(out.hasThread, 'Expected window.hfoP2SwordMeterThread.tick to exist (v23).').toBe(true);
  expect(out.locked, 'Expected sword to be locked before validating visual markers (v23).').toBe(true);
  expect(!!out.touch2dMarker, 'Expected Touch2D flaming sword marker to be present when enabled (v23).').toBe(true);
  SwordTouch2dMarkerV23Schema.parse(out.touch2dMarker);
  expect(
    !!out.babylonMarker || !!out.swordMeshName,
    'Expected Babylon flaming sword marker/mesh to be present when enabled (v23).',
  ).toBe(true);

  if (out.babylonMarker) {
    SwordBabylonMarkerV23Schema.parse(out.babylonMarker);
  }
});
