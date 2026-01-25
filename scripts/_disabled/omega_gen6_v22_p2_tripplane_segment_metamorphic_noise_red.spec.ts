// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// RED TDD (metamorphic): segment/extent semantics must be robust to small, deterministic noise.
//
// We take a minimal fixture where the fingertip x is outside the original segment (ext=0)
// and add small y-jitter. Under correct segment semantics, NO crossings should be emitted for
// ANY of these perturbed variants. Current v22 uses infinite-line distance so it will emit => RED.

test.describe.configure({ retries: 0 });

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v22_knuckle_tripplane_extension_only_cross_min_golden.jsonl';

function loadFrames() {
  return fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));
}

async function runReplay(hfoPage: any, url: string, frames: any[]) {
  await safeGoto(hfoPage, url);
  await hfoPage.waitForTimeout(250);

  return await safeEvaluate(
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
}

test('Gen6 v22 RED (metamorphic): ext=0 outside-segment remains non-triggering under small y-jitter', async ({ hfoPage }) => {
  const baseFrames = loadFrames();

  const url = `${GEN6_V22_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-ui-knuckle-tripwire-panel=false'
    + '&flag-p2-knuckle-tripwire-ext-a-frac=0'
    + '&flag-p2-knuckle-tripwire-ext-b-frac=0';

  const jitters = [0, 0.002, -0.002, 0.004, -0.004];

  for (const j of jitters) {
    const frames = baseFrames.map((f: any) => {
      const cursor = { ...(f.cursor || {}) };
      cursor.uiNormY = Number(cursor.uiNormY ?? 0) + j;

      const lm = Array.isArray(cursor.landmarks) ? cursor.landmarks.map((p: any) => ({ ...p })) : [];
      // index_tip is landmark 8 in our fixtures.
      if (lm[8]) lm[8].y = Number(lm[8].y ?? 0) + j;
      cursor.landmarks = lm;

      return { ...f, cursor };
    });

    const out = await runReplay(hfoPage, url, frames);

    // Correct behavior (future): 0 crosses for all jitter variants when x is outside segment.
    // Current behavior (now): emits due to infinite-line distance => RED.
    expect(out.captured.length, `Expected 0 crosses for jitter=${j}; got=${JSON.stringify(out.captured)}`).toBe(0);
  }
});

test('Gen6 v22 (metamorphic): gating check — if not COMMIT, should emit nothing', async ({ hfoPage }) => {
  const baseFrames = loadFrames();

  const url = `${GEN6_V22_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-ui-knuckle-tripwire-panel=false'
    + '&flag-p2-knuckle-tripwire-ext-a-frac=0'
    + '&flag-p2-knuckle-tripwire-ext-b-frac=0';

  const frames = baseFrames.map((f: any) => ({
    ...f,
    cursor: {
      ...(f.cursor || {}),
      fsmState: 'IDLE',
    },
  }));

  const out = await runReplay(hfoPage, url, frames);
  expect(out.captured.length).toBe(0);
});
