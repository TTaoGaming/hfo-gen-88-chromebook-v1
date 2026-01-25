// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';

// FUZZ scaffold (intentionally skipped for now):
// - Perturb cursor + landmark noise / dt jitter
// - Assert P2 tick never throws and stays COMMIT-gated
// This is infrastructure-only; enable when we want brittleness metrics.

test.describe.configure({ mode: 'serial', retries: 0 });

test.skip('Gen6 v22: P2 knuckle tripplane fuzz scaffold (skipped)', async ({ hfoPage }) => {
  const GOLDEN_PATH =
    'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

  const baseFrames = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));

  const url = `${GEN6_V22_TEST_URL_LIGHT}`
    + '&flag-p2-tripwire-knuckle=true'
    + '&flag-p2-tripwire-static=false'
    + '&flag-p3-tripwire-injector=false'
    + '&flag-ui-knuckle-tripwire-panel=false';

  await safeGoto(hfoPage, url);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(
    hfoPage,
    (framesIn) => {
      const w = window as any;
      if (!w.systemState) throw new Error('missing systemState');
      if (!w.hfoP2KnuckleTripwireThread?.tick) throw new Error('missing hfoP2KnuckleTripwireThread.tick');

      // simple deterministic PRNG
      let seed = 1337;
      const rand = () => {
        seed = (seed * 1103515245 + 12345) & 0x7fffffff;
        return seed / 0x7fffffff;
      };

      const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };
      for (const f of framesIn) {
        dataFabric.frameId++;
        dataFabric.systemTime = Number(f?.now || 0);

        const jitter = (amp: number) => (rand() * 2 - 1) * amp;

        const cursor = {
          ...f.cursor,
          seq: f?.seq,
          normX: Number(f.cursor?.uiNormX ?? 0) + jitter(0.005),
          normY: Number(f.cursor?.uiNormY ?? 0) + jitter(0.005),
        };

        // NOTE: landmarks (if present) are 3D uiNorm coords
        const landmarks = Array.isArray(f.landmarks)
          ? f.landmarks.map((p: any) => ({
              ...p,
              uiNormX: Number(p?.uiNormX ?? 0) + jitter(0.003),
              uiNormY: Number(p?.uiNormY ?? 0) + jitter(0.003),
              uiNormZ: Number(p?.uiNormZ ?? 0) + jitter(0.003),
            }))
          : f.landmarks;

        dataFabric.cursors = [
          {
            ...cursor,
            landmarks,
          },
        ];

        const dtBase = Number(f?.dt || 16);
        const dt = Math.max(1, dtBase + jitter(2));

        w.hfoP2KnuckleTripwireThread.tick({ now: Number(f?.now || 0), dt, dataFabric });
      }

      return { ok: true };
    },
    baseFrames,
  );

  expect(out.ok).toBe(true);
});
