// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V16_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { TripwireCrossV15Schema } from '../contracts/hfo_tripwire_events.zod';

// Desired v16 behavior: in contact-only mode, a cursor that enters the sensor band emits contact begin/end phases.
test.describe.configure({ mode: 'serial', retries: 1 });

const GEN6_URL = `${GEN6_V16_TEST_URL_LIGHT}&flag-p2-tripwire-contact-only=true`;

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v16_tripwire_planck_contact_inband_enter_exit_golden.jsonl';

test('Gen6 v16 (TDD RED): contact-only tripwire emits begin+end with contract-valid payload', async ({ hfoPage }) => {
  const lines = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean);
  const frames = lines.map((l) => JSON.parse(l));
  expect(frames.length).toBeGreaterThanOrEqual(4);

  await safeGoto(hfoPage, GEN6_URL);
  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(hfoPage, (framesIn) => {
    const w = window as any;
    if (!w.systemState) throw new Error('missing systemState');
    if (!w.hfoP2TripwireThread?.tick) throw new Error('missing hfoP2TripwireThread.tick');

    const captured: Array<{ port: string; type: string; payload: any }> = [];
    const unsubscribe = w.hfoPortsEffects?.subscribe
      ? w.hfoPortsEffects.subscribe((entry: any) => {
        if (entry?.port === 'p2') captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      }, 'p2')
      : null;

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
      w.hfoP2TripwireThread.tick({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
    }

    if (typeof unsubscribe === 'function') {
      try {
        unsubscribe();
      } catch {
        // ignore
      }
    }

    return { captured, debug: w.hfoP2TripwireThread?.getDebugState?.() || null };
  }, frames);

  const tripwire = out.captured.filter((e: any) => e?.type === 'tripwire_cross');

  // In contact-only mode we want at least a begin and an end phase.
  const phases = tripwire.map((e: any) => e?.payload?.sensor?.phase).filter(Boolean);

  // Validate every event against the existing contract (v15 schema already enforces sensor metadata).
  for (const e of tripwire) {
    const parsed = TripwireCrossV15Schema.safeParse(e.payload);
    expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);
  }

  // RED until v16 implements real contact begin/end emission.
  expect(phases, `Expected begin+end; debug=${JSON.stringify(out.debug)}`).toEqual(['begin', 'end']);
});
