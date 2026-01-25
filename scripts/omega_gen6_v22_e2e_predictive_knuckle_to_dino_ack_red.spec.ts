// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import { GEN6_V22_TEST_URL_LIGHT, safeGoto, safeEvaluate } from './omega_gen6_test_guards';
import { P3TripwireInjectV2Schema } from '../contracts/hfo_tripwire_events.zod';

// RED TDD (E2E): v22 predictive policy should cause Space keydown to lead the knuckle crossing,
// and that injected action must successfully reach the Dino wrapper (ack ok:true).
//
// This is expected to FAIL until (a) P2 emits tripplane_lookahead and (b) P3 uses it for predictive keydown.

// Safety: E2E is opt-in to reduce crash/resource pressure during RED-only work.
// Enable with: HFO_ENABLE_E2E=1
const ENABLE_E2E = process.env.HFO_ENABLE_E2E === '1';

test.describe.configure({ retries: 0 });

const GEN6_URL = `${GEN6_V22_TEST_URL_LIGHT}`
  + '&flag-p2-tripwire-knuckle=true'
  + '&flag-p2-tripwire-static=false'
  + '&flag-p3-tripwire-injector-knuckle=true'
  + '&flag-p3-tripwire-injector=false'
  + '&flag-p3-tripwire-injector-static=false'
  + '&flag-ui-knuckle-tripwire-panel=false';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v20_knuckle_tripwire_press_release_space_golden.jsonl';

test.describe('Gen6 v22 RED E2E (opt-in)', () => {
  test.skip(!ENABLE_E2E, 'E2E disabled by default; set HFO_ENABLE_E2E=1');

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

  test('Gen6 v22 RED E2E: predictive keydown leads crossing and reaches Dino ack ok:true', async ({ hfoPage }) => {
    const frames = fs
      .readFileSync(GOLDEN_PATH, 'utf-8')
      .split('\n')
      .map((l) => l.trim())
      .filter(Boolean)
      .map((l) => JSON.parse(l));

    await safeGoto(hfoPage, GEN6_URL);

    await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });
    await hfoPage.waitForFunction(() => !!document.querySelector('#dino-wrapper-iframe'), null, { timeout: 20_000 });

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

        try {
          w.__hfoDiag.acks = [];
          w.__hfoDiag.messages = [];
        } catch {
          // ignore
        }

        try {
          w.hfoPorts?.p7?.adapters?.setActiveId?.('dino-v1');
        } catch {
          // ignore
        }

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

          const now = Number(f?.now || 0);
          const dt = Number(f?.dt || 16);

          w.hfoP2KnuckleTripwireThread.tick({ now, dt, dataFabric });

          try {
            w.hfoP3PlanckSensorInjector?.tick?.({ now, dt, dataFabric });
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
    expect(beginCross, `Expected at least one p2 tripwire_cross begin; got=${JSON.stringify(out.captured.filter((e: any) => e?.port === 'p2'))}`).toBeTruthy();
    const crossNow = Number(beginCross?.payload?.now ?? NaN);

    const injects = out.captured.filter((e: any) => e?.port === 'p3' && e?.type === 'tripwire_inject');
    expect(injects.length, `Expected >=1 p3 tripwire_inject; got=${JSON.stringify(out.captured.filter((e: any) => e?.port === 'p3'))}`).toBeGreaterThanOrEqual(1);

    for (const e of injects) {
      const parsed = P3TripwireInjectV2Schema.safeParse(e.payload);
      expect(parsed.success, `Contract invalid: ${JSON.stringify(parsed.error?.issues || parsed.error)}`).toBe(true);
    }

    const keydowns = injects.filter((e: any) => String(e?.payload?.payload?.action || '') === 'keydown');
    expect(keydowns.length, `Expected >=1 keydown inject; got=${JSON.stringify(injects)}`).toBeGreaterThanOrEqual(1);
    const kdNow = Math.min(...keydowns.map((e: any) => Number(e?.payload?.now ?? NaN)).filter((n: any) => Number.isFinite(n)));

    const dinoPostOk = out.captured.filter((e: any) => e?.port === 'p7' && e?.type === 'dino_postMessage' && e?.payload?.ok);
    expect(dinoPostOk.length, `Expected >=1 p7 dino_postMessage ok; got=${JSON.stringify(out.captured.filter((e: any) => e?.port === 'p7'))}`).toBeGreaterThanOrEqual(1);

    const acksAll = out.acks || [];
    const ackOk = acksAll.filter((a: any) => a?.payload?.ok);
    expect(acksAll.length, 'Expected at least one hfo:nematocyst:ack').toBeGreaterThanOrEqual(1);
    expect(ackOk.length, `Expected at least one ok:true ack; got=${JSON.stringify(acksAll.slice(-5))}`).toBeGreaterThanOrEqual(1);

    // RED: predictive requirement. This is expected to FAIL until v22 lookahead + predictive P3 are implemented.
    expect(Number.isFinite(kdNow) && Number.isFinite(crossNow)).toBe(true);
    expect(kdNow, `Expected predictive keydown now < crossing now; kdNow=${kdNow} crossNow=${crossNow}`).toBeLessThan(crossNow);
  });
});
