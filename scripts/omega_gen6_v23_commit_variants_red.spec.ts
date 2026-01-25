// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V23_TEST_URL_LIGHT, safeEvaluate, safeGoto } from './omega_gen6_test_guards';
import { buildStepsFromFrames } from './gen6_v23_red_helpers';

// RED TDD: v23 commit variants (COMMIT_POINTER_UP / COMMIT_THUMBS_UP / COMMIT_THUMBS_DOWN)
// These tests intentionally fail until v23 P2 ports are implemented.

type SynthFrame = {
  t: number;
  fsmState: 'IDLE' | 'READY' | 'COMMIT' | 'COAST';
  gesture: 'Pointing_Up' | 'Thumb_Up' | 'Thumb_Down' | 'Open_Palm' | 'None';
  confidence: number;
  isPalmFacing: boolean;
};

test('v23 RED: commitVariantByHand exists + defaults fail-closed', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const hasPort = await safeEvaluate(hfoPage, () => {
    const w = window as any;
    return {
      hasThread: !!w.hfoP2CommitVariantsThread?.tick,
      hasState: !!w.systemState?.p2?.commitVariantByHand,
    };
  }, null as any);

  // RED: both are expected to be false until implemented.
  expect(hasPort.hasThread).toBe(true);
  expect(hasPort.hasState).toBe(true);
});

test('v23 RED: Pointing_Up maps to COMMIT_POINTER_UP (READY gating)', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const frames: SynthFrame[] = [
    { t: 0, fsmState: 'READY', gesture: 'Pointing_Up', confidence: 0.99, isPalmFacing: true },
  ];

  const steps = buildStepsFromFrames(
    frames.map((f, i) => ({ ...f, now: 1000 + i * 50, dt: 50 })),
  );

  const out = await safeEvaluate(hfoPage, (payload: { steps: Array<{ now: number; dt: number; dataFabric: any }> }) => {
    const w = window as any;
    const tick = w.hfoP2CommitVariantsThread?.tick;
    if (!tick) return { ok: false, reason: 'missing hfoP2CommitVariantsThread.tick' };

    for (const s of payload.steps) {
      try {
        tick({ now: Number(s.now), dt: Number(s.dt), dataFabric: s.dataFabric });
      } catch {
        // ignore (RED-first)
      }
    }

    const cv = w.systemState?.p2?.commitVariantByHand;
    return {
      ok: true,
      v0: cv?.hand0 ?? cv?.['0'] ?? cv?.Right ?? cv?.right ?? null,
    };
  }, { steps });

  expect(out.ok).toBe(true);
  expect(out.v0).toBe('COMMIT_POINTER_UP');
});

test('v23 RED: Thumb_Up and Thumb_Down map to COMMIT_THUMBS_UP / COMMIT_THUMBS_DOWN', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const frames: SynthFrame[] = [
    { t: 0, fsmState: 'READY', gesture: 'Thumb_Up', confidence: 0.99, isPalmFacing: true },
    { t: 1, fsmState: 'READY', gesture: 'Thumb_Down', confidence: 0.99, isPalmFacing: true },
  ];

  const steps = buildStepsFromFrames(
    frames.map((f, i) => ({ ...f, now: 1000 + i * 50, dt: 50 })),
  );

  const out = await safeEvaluate(hfoPage, (payload: { steps: Array<{ now: number; dt: number; dataFabric: any }> }) => {
    const w = window as any;
    const tick = w.hfoP2CommitVariantsThread?.tick;
    if (!tick) return { ok: false, reason: 'missing hfoP2CommitVariantsThread.tick' };

    // Tick once per step and capture after each tick.
    const seen: any[] = [];
    for (const s of payload.steps) {
      try {
        tick({ now: Number(s.now), dt: Number(s.dt), dataFabric: s.dataFabric });
      } catch {
        // ignore (RED-first)
      }
      const cv = w.systemState?.p2?.commitVariantByHand;
      seen.push(cv?.hand0 ?? cv?.['0'] ?? cv?.Right ?? cv?.right ?? null);
    }

    return { ok: true, seen };
  }, { steps });

  expect(out.ok).toBe(true);
  expect(out.seen?.[0]).toBe('COMMIT_THUMBS_UP');
  expect(out.seen?.[1]).toBe('COMMIT_THUMBS_DOWN');
});
