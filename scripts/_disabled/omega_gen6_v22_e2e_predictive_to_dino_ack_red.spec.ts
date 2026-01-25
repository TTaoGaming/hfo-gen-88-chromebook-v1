// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { P3TripwireInjectV2Schema } from '../contracts/hfo_tripwire_events.zod';

// E2E RED: v22 predictive delivery must reach the Dino wrapper and ack ok:true.
// This stays RED until predictive timing is implemented (keydown must lead crossing) and until
// P2 emits lookahead for P3 to use.

test.describe.configure({ mode: 'serial', retries: 1 });

test.beforeEach(async ({ hfoPage }) => {
  await hfoPage.addInitScript(() => {
    const anyWindow = window as any;
    anyWindow.__hfoDiag = anyWindow.__hfoDiag || { acks: [], messages: [] };

    const pushRing = (arr: any[], v: any, maxLen: number) => {
      try {
        arr.push(v);
        if (arr.length > maxLen) arr.splice(0, arr.length - maxLen);
      } catch {
        // ignore
      }
    };

    window.addEventListener('message', (event) => {
      try {
        const data = (event as any)?.data;
        if (!data || typeof data !== 'object') return;

        pushRing(
          anyWindow.__hfoDiag.messages,
          {
            ts: Date.now(),
            origin: (event as any)?.origin || null,
            type: data.type || null,
            payload: data.payload ?? null,
          },
          250,
        );

        if (data.type === 'hfo:nematocyst:ack') {
          pushRing(
            anyWindow.__hfoDiag.acks,
            { ts: Date.now(), origin: (event as any)?.origin || null, payload: data.payload ?? null },
            250,
          );
        }
      } catch {
        // ignore
      }
    });
  });
});

const GEN6_URL = `${GEN6_V22_TEST_URL_LIGHT}`
  + '&flag-p2-tripwire-knuckle=true'
  + '&flag-p2-tripwire-static=false'
  + '&flag-p3-tripwire-injector-knuckle=true'
  + '&flag-p3-tripwire-injector=false'
  + '&flag-p3-tripwire-injector-static=false'
  + '&flag-ui-knuckle-tripwire-panel=false'
  + '&flag-p2-knuckle-tripwire-ext-a-frac=0.5'
  + '&flag-p2-knuckle-tripwire-ext-b-frac=0.5';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

test('Gen6 v22 E2E RED: predictive keydown → Dino wrapper ack ok:true', async ({ hfoPage }) => {
  const frames = fs
    .readFileSync(GOLDEN_PATH, 'utf-8')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => JSON.parse(l));
  expect(frames.length).toBeGreaterThanOrEqual(4);

  await safeGoto(hfoPage, GEN6_URL);

  // Ensure layout + dino wrapper iframe exist.
  await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });
  await hfoPage.waitForFunction(() => !!document.querySelector('#dino-wrapper-iframe'), null, { timeout: 20_000 });

  // Ensure wrapper document is ready (inner runner may still be loading).
  await hfoPage.waitForFunction(() => {
    const iframe = document.querySelector('#dino-wrapper-iframe') as HTMLIFrameElement | null;
    if (!iframe) return false;
    try {
      return iframe.contentDocument?.readyState === 'complete';
    } catch {
      return false;
    }
  }, null, { timeout: 20_000 });

  await hfoPage.waitForTimeout(250);

  const out = await safeEvaluate(
    hfoPage,
    async (framesIn) => {
      const w = window as any;
      if (!w.systemState) throw new Error('missing systemState');
      if (!w.hfoPortsEffects?.subscribe) throw new Error('missing hfoPortsEffects.subscribe');
      if (!w.hfoP2KnuckleTripwireThread?.tick) throw new Error('missing hfoP2KnuckleTripwireThread.tick');

      // Clear diagnostic rings.
      try {
        w.__hfoDiag.acks = [];
        w.__hfoDiag.messages = [];
      } catch {
        // ignore
      }

      // Make sure dino is the active adapter.
      try {
        w.hfoPorts?.p7?.adapters?.setActiveId?.('dino-v1');
      } catch {
        // ignore
      }

      // Ensure injector started.
      try {
        w.hfoP3PlanckSensorInjector?.start?.();
      } catch {
        // ignore
      }

      const captured: Array<{ port: string; type: string; payload: any }> = [];
      const unsubscribe = w.hfoPortsEffects.subscribe((entry: any) => {
        if (entry?.port !== 'p2' && entry?.port !== 'p3' && entry?.port !== 'p7') return;
        captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      });

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

        try {
          w.hfoP3PlanckSensorInjector?.tick?.({ now: Number(f?.now || 0), dt: Number(f?.dt || 16), dataFabric });
        } catch {
          // ignore
        }
      }

      await new Promise((r) => setTimeout(r, 400));

      if (typeof unsubscribe === 'function') {
        try {
          unsubscribe();
        } catch {
          // ignore
        }
      }

      return { captured, acks: w.__hfoDiag?.acks || [], messages: w.__hfoDiag?.messages || [] };
    },
    frames,
  );

  const beginCross = out.captured.find((e: any) => e?.port === 'p2' && e?.type === 'tripwire_cross' && e?.payload?.sensor?.phase === 'begin');
  expect(beginCross, `Expected >=1 p2 tripwire_cross begin; got=${JSON.stringify(out.captured.filter((e: any) => e?.port === 'p2'))}`).toBeTruthy();

  const injects = out.captured.filter((e: any) => e?.port === 'p3' && e?.type === 'tripwire_inject');
  expect(injects.length, `Expected >=1 p3 tripwire_inject; got=${JSON.stringify(out.captured)}`).toBeGreaterThanOrEqual(1);

  for (const e of injects) {
    const parsed = P3TripwireInjectV2Schema.safeParse(e.payload);
    expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);
  }

  const firstKeydown = injects.find((e: any) => String(e?.payload?.payload?.action) === 'keydown');
  expect(firstKeydown, `Expected at least one keydown; got=${JSON.stringify(injects)}`).toBeTruthy();

  const kdNow = Number(firstKeydown?.payload?.now ?? NaN);
  const crossNow = Number(beginCross?.payload?.now ?? NaN);
  expect(Number.isFinite(kdNow) && Number.isFinite(crossNow)).toBe(true);

  // RED condition: v22 should eventually be predictive (keydown now < cross now).
  // Current behavior is non-predictive => should fail until v22 lookahead + P3 policy exist.
  expect(kdNow, `Expected predictive keydown now < crossing now; kdNow=${kdNow} crossNow=${crossNow}`).toBeLessThan(crossNow);

  const dinoPostOk = out.captured.filter((e: any) => e?.port === 'p7' && e?.type === 'dino_postMessage' && e?.payload?.ok);
  expect(
    dinoPostOk.length,
    `Expected >=1 p7 dino_postMessage ok; got=${JSON.stringify(out.captured.filter((e: any) => e?.port === 'p7'))}`,
  ).toBeGreaterThanOrEqual(1);

  const ackOk = (out.acks || []).filter((a: any) => a?.payload?.ok);
  expect((out.acks || []).length, 'Expected at least one hfo:nematocyst:ack').toBeGreaterThanOrEqual(1);
  expect(ackOk.length, `Expected at least one ok:true ack; got=${JSON.stringify((out.acks || []).slice(-5))}`).toBeGreaterThanOrEqual(1);
});
