// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V23_TEST_URL_LIGHT, safeEvaluate, safeGoto } from './omega_gen6_test_guards';
import { DataFabricSchema, FabricEnvelopeSchema } from '../contracts/hfo_data_fabric.zod';

// Architecture-first RED TDD (v23): Port 1 is the single authority for the shared DataFabric seam.
// These tests intentionally fail until v23 hardens P1 envelope identity + contract breach signaling.

type WeaveEvalOut =
  | { ok: false; reason: string }
  | {
    ok: true;
    res: { dataFabric: any; envelope: any };
    state: { dataFabric: any; envelope: any };
  };

type WeaveBreachEvalOut =
  | { ok: false; reason: string }
  | {
    ok: true;
    threw: boolean;
    beforeHasFabric: boolean;
    beforeFrameId: number | null;
    afterFrameId: number | null;
    captured: Array<{ port: string; type: string; payload: any }>;
  };

test('v23 RED: P1 weave returns a v23-identified FabricEnvelope and updates systemState', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const out = await safeEvaluate<WeaveEvalOut, { dt: number; nowMs: number; results: any }>(
    hfoPage,
    (payload: { dt: number; nowMs: number; results: any }) => {
      const w = window as any;
      const weave = w.hfoPorts?.p1?.weave;
      if (typeof weave !== 'function') {
        return { ok: false, reason: 'missing window.hfoPorts.p1.weave' };
      }

      const res = weave(payload.results, payload.dt, payload.nowMs);
      return {
        ok: true,
        res: {
          dataFabric: res?.dataFabric ?? null,
          envelope: res?.envelope ?? null,
        },
        state: {
          dataFabric: w.systemState?.dataFabric ?? null,
          envelope: w.systemState?.dataFabricEnvelope ?? null,
        },
      };
    },
    { dt: 16, nowMs: 1234, results: {} },
  );

  if (!out.ok) throw new Error(String((out as any).reason || 'unknown'));

  // Contract-valid fabric is a hard requirement for the P1 seam.
  expect(out.state.dataFabric, 'Expected window.systemState.dataFabric to exist.').toBeTruthy();
  DataFabricSchema.parse(out.state.dataFabric);

  // RED: v23 requires a canonical envelope (not null) and v23-specific identity.
  expect(out.state.envelope, 'Expected window.systemState.dataFabricEnvelope to exist (v23).').toBeTruthy();
  const env = FabricEnvelopeSchema.parse(out.state.envelope);

  // RED: enforce v23 identity for envelope type/id to avoid cross-version ambiguity.
  expect(env.type).toBe('hfo.gen6.p1.fuse.v23');
  expect(env.id.startsWith('hfo-gen6-')).toBe(true);
});

test('v23 RED: P1 contract breach is fail-closed and emits a p1 contract_breach effect', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const out = await safeEvaluate<WeaveBreachEvalOut, { dt: number; goodNowMs: number; badNowMs: number; results: any }>(
    hfoPage,
    (payload: { dt: number; goodNowMs: number; badNowMs: number; results: any }) => {
      const w = window as any;
      const weave = w.hfoPorts?.p1?.weave;
      if (typeof weave !== 'function') {
        return { ok: false, reason: 'missing window.hfoPorts.p1.weave' };
      }

      const captured: Array<{ port: string; type: string; payload: any }> = [];
      const unsub = w.hfoPortsEffects?.subscribe?.((entry: any) => {
        if (!entry?.port) return;
        if (entry.port !== 'p1') return;
        captured.push({ port: entry.port, type: entry.type, payload: entry.payload });
      });

      // Establish a known-good baseline.
      const before = weave(payload.results, payload.dt, payload.goodNowMs);
      const beforeFrameId = w.systemState?.dataFabric?.frameId ?? null;

      // Force a P1 contract breach by providing an invalid (non-finite) systemTime.
      // P1 must be fail-closed: no throws, no state mutation.
      let threw = false;
      try {
        weave(payload.results, payload.dt, payload.badNowMs);
      } catch {
        threw = true;
      }

      const afterFrameId = w.systemState?.dataFabric?.frameId ?? null;

      try {
        unsub?.();
      } catch {
        // ignore
      }

      return {
        ok: true,
        threw,
        beforeHasFabric: !!before?.dataFabric,
        beforeFrameId,
        afterFrameId,
        captured,
      };
    },
    { dt: 16, goodNowMs: 2000, badNowMs: Number.NaN, results: {} },
  );

  if (!out.ok) throw new Error(String((out as any).reason || 'unknown'));
  expect(out.threw, 'P1 weave must not throw on contract breach (fail-closed).').toBe(false);
  expect(out.beforeHasFabric, 'Expected baseline weave to produce a fabric.').toBe(true);
  expect(out.beforeFrameId).toBeTruthy();

  // Fail-closed state mutation rule.
  expect(out.afterFrameId).toBe(out.beforeFrameId);

  // RED: require contract breach signaling through the standard ports effects bus.
  const breach = (out.captured || []).filter((e: any) => String(e?.type || '').includes('contract_breach'));
  expect(breach.length, 'Expected a p1 contract_breach effect on invalid weave input (v23).').toBeGreaterThan(0);
});
