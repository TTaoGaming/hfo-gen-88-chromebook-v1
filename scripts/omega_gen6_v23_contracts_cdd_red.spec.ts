// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { safeEvaluate, safeGoto, GEN6_V23_TEST_URL_LIGHT } from './omega_gen6_test_guards';
import {
  CommitVariantByHandV23Schema,
  SwordMeterSnapshotV23Schema,
  P2CommitVariantEventV23Schema,
  P2SwordMeterEventV23Schema,
} from '../contracts/hfo_tripwire_events.zod';
import { buildStepsFromFrames } from './gen6_v23_red_helpers';

// CDD/RED: v23 should expose schema-valid P2 snapshots + events.
// These are expected to FAIL until v23 P2 ports are implemented.

test('v23 CDD RED: systemState.p2.commitVariantByHand conforms to schema', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const snap = await safeEvaluate(hfoPage, () => {
    const w = window as any;
    return w.systemState?.p2?.commitVariantByHand ?? null;
  }, null as any);

  expect(snap, 'Expected systemState.p2.commitVariantByHand to exist (v23).').toBeTruthy();
  CommitVariantByHandV23Schema.parse(snap);
});

test('v23 CDD RED: systemState.p2.swordMeter conforms to schema', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const snap = await safeEvaluate(hfoPage, () => {
    const w = window as any;
    return (w.systemState?.p2?.swordMeter || w.systemState?.p2?.sword) ?? null;
  }, null as any);

  expect(snap, 'Expected systemState.p2.swordMeter (or p2.sword) to exist (v23).').toBeTruthy();
  SwordMeterSnapshotV23Schema.parse(snap);
});

test('v23 CDD RED: emitted p2 events validate against v23 schemas', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const frames = Array.from({ length: 6 }).map((_, i) => ({
    now: 1000 + i * 50,
    dt: 50,
    fsmState: 'READY' as const,
    gesture: i < 3 ? 'Thumb_Up' : 'Thumb_Down',
    confidence: 0.99,
    isPalmFacing: true,
    uiNormX: 0.55,
    uiNormY: 0.55,
  }));
  const steps = buildStepsFromFrames(frames);

  const out = await safeEvaluate(hfoPage, (payload: { steps: Array<{ now: number; dt: number; dataFabric: any }> }) => {
    const w = window as any;

    const captured: Array<{ port: string; type: string; payload: any }> = [];
    const unsub = w.hfoPortsEffects?.subscribe?.((entry: any) => {
      if (!entry?.port) return;
      if (entry.port !== 'p2') return;
      captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
    });

    // Best-effort: if v23 threads exist, drive a few ticks to provoke emissions.
    const meter = w.hfoP2SwordMeterThread;
    const commit = w.hfoP2CommitVariantsThread;

    for (const s of payload.steps) {
      try { commit?.tick?.({ now: Number(s.now), dt: Number(s.dt), dataFabric: s.dataFabric }); } catch { }
      try { meter?.tick?.({ now: Number(s.now), dt: Number(s.dt), dataFabric: s.dataFabric }); } catch { }
    }

    try { unsub?.(); } catch { }

    return {
      hasCommit: !!commit?.tick,
      hasMeter: !!meter?.tick,
      captured,
    };
  }, { steps });

  expect(out.hasCommit, 'Expected window.hfoP2CommitVariantsThread.tick to exist (v23).').toBe(true);
  expect(out.hasMeter, 'Expected window.hfoP2SwordMeterThread.tick to exist (v23).').toBe(true);

  const p2CommitEvents = out.captured.filter((e: any) => String(e?.type || '').includes('commit'));
  const p2SwordEvents = out.captured.filter((e: any) => String(e?.type || '').includes('sword'));

  expect(p2CommitEvents.length + p2SwordEvents.length, 'Expected at least one v23 p2 commit/sword event.').toBeGreaterThan(0);

  for (const e of p2CommitEvents) P2CommitVariantEventV23Schema.parse(e.payload);
  for (const e of p2SwordEvents) P2SwordMeterEventV23Schema.parse(e.payload);
});
