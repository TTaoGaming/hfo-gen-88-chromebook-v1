// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED TDD (metamorphic): small landmark noise should not create false positives for
// outside-segment crossings when extension=0.
//
// This intentionally fails today because v22 uses infinite-line distance rather than segment/extent
// intersection semantics.

test.describe.configure({ retries: 0 });

// This file is intentionally RED-first but should remain fast and stable.
test.use({ trace: 'off' });

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v22_knuckle_tripplane_slow_cross_outside_segment_golden.jsonl';

test('Gen6 v22 RED: ext=0 outside-segment stays non-triggering under small deterministic jitter', async ({ hfoPage }) => {
  const frames = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));

  const url = `${GEN6_V22_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-ui-knuckle-tripwire-panel=false'
    + '&flag-p2-knuckle-tripwire-ext-a-frac=0'
    + '&flag-p2-knuckle-tripwire-ext-b-frac=0';

  await safeGoto(hfoPage, url);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(
    hfoPage,
    (framesIn) => {
      const w = window as any;
      if (!w.systemState) throw new Error('missing systemState');
      if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
      if (!w.hfoP2KnuckleTripwireThread?.tick) throw new Error('missing hfoP2KnuckleTripwireThread.tick');

      const captured: Array<{ port: string; type: string; payload: any }> = [];
      const unsub = w.hfoPortsEffects.subscribe((entry: any) => {
        if (entry?.port !== 'p2') return;
        if (entry?.type !== 'tripwire_cross') return;
        captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      }, 'p2');

      // Deterministic LCG for tiny jitter
      let seed = 1337;
      const rand = () => {
        seed = (seed * 1664525 + 1013904223) >>> 0;
        return seed / 0xffffffff;
      };
      const jitter = (v: number, eps: number) => v + (rand() * 2 - 1) * eps;

      const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };
      for (const f of framesIn) {
        dataFabric.frameId++;
        dataFabric.systemTime = Number(f?.now || 0);

        const cursor = { ...f.cursor };
        cursor.uiNormX = jitter(Number(cursor.uiNormX), 0.002);
        cursor.uiNormY = jitter(Number(cursor.uiNormY), 0.002);

        const lm = Array.isArray(cursor.landmarks) ? cursor.landmarks.map((p: any) => ({ ...p })) : [];
        // Jitter the fingertip landmark (index_tip=8) only; keep MCP bar anchors stable.
        if (lm[8]) {
          lm[8].x = jitter(Number(lm[8].x), 0.002);
          lm[8].y = jitter(Number(lm[8].y), 0.002);
        }
        cursor.landmarks = lm;

        dataFabric.cursors = [
          {
            ...cursor,
            seq: f?.seq,
            normX: cursor.uiNormX,
            normY: cursor.uiNormY,
          },
        ];

        w.hfoP2KnuckleTripwireThread.tick({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
      }

      try {
        unsub?.();
      } catch {
        // ignore
      }

      return { captured };
    },
    frames,
  );

  expect(out.captured.length, `Expected 0 knuckle tripwire_cross under jitter; got=${JSON.stringify(out.captured)}`).toBe(0);
});

test('Gen6 v22: gating smoke — if fsmState != COMMIT, emits nothing', async ({ hfoPage }) => {
  const frames = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));

  const url = `${GEN6_V22_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-ui-knuckle-tripwire-panel=false'
    + '&flag-p2-knuckle-tripwire-ext-a-frac=0'
    + '&flag-p2-knuckle-tripwire-ext-b-frac=0';

  await safeGoto(hfoPage, url);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(
    hfoPage,
    (framesIn) => {
      const w = window as any;
      if (!w.systemState) throw new Error('missing systemState');
      if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
      if (!w.hfoP2KnuckleTripwireThread?.tick) throw new Error('missing hfoP2KnuckleTripwireThread.tick');

      try {
        // v22 uses per-hand FSM state (systemState.p1.fsmStates[i]) and the per-cursor fsmState.
        if (Array.isArray(w.systemState?.p1?.fsmStates)) w.systemState.p1.fsmStates[0] = 'IDLE';
        if (w.systemState?.fsm?.currentState) w.systemState.fsm.currentState = 'IDLE';
      } catch {
        // ignore
      }

      const captured: Array<{ port: string; type: string; payload: any }> = [];
      const unsub = w.hfoPortsEffects.subscribe((entry: any) => {
        if (entry?.port !== 'p2') return;
        if (entry?.type !== 'tripwire_cross') return;
        captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      }, 'p2');

      const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };
      for (const f of framesIn) {
        dataFabric.frameId++;
        dataFabric.systemTime = Number(f?.now || 0);
        dataFabric.cursors = [
          {
            ...f.cursor,
            seq: f?.seq,
            normX: f.cursor?.uiNormX,
            normY: f.cursor?.uiNormY,
            fsmState: 'IDLE',
          },
        ];

        w.hfoP2KnuckleTripwireThread.tick({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
      }

      try {
        unsub?.();
      } catch {
        // ignore
      }

      return { captured };
    },
    frames,
  );

  expect(out.captured.length, `Expected 0 p2 tripwire_cross when fsmState!=COMMIT; got=${JSON.stringify(out.captured)}`).toBe(0);
});
