// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { GEN6_V23_TEST_URL_LIGHT, safeEvaluate, safeGoto } from './omega_gen6_test_guards';
import { SwordTouch2dMarkerV23Schema } from '../contracts/hfo_ui_markers.zod';

// RED TDD: Touch2D geometry for the v23 knuckle sword overlay.
// Contract: window.__hfoSwordTouch2dMarker provides deterministic endpoints & axis.

test('v23 RED: Touch2D sword marker exists with endpoint semantics (pinky→index)', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const marker = await safeEvaluate(hfoPage, () => {
    const w = window as any;
    return w.__hfoSwordTouch2dMarker ?? null;
  }, null as any);

  // RED: marker is required by spec; should be null until implemented.
  expect(marker).not.toBeNull();
  SwordTouch2dMarkerV23Schema.parse(marker);
});

test('v23 RED: marker exposes endpointPinkyUiNorm + endpointIndexUiNorm + axisUiNorm', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const out = await safeEvaluate(hfoPage, () => {
    const m = (window as any).__hfoSwordTouch2dMarker;
    if (!m) return { ok: false, reason: 'missing __hfoSwordTouch2dMarker' };

    const hasPoint = (p: any) => p && typeof p.x === 'number' && typeof p.y === 'number';

    return {
      ok: true,
      hasEndpointPinky: hasPoint(m.endpointPinkyUiNorm),
      hasEndpointIndex: hasPoint(m.endpointIndexUiNorm),
      hasEndpointA: hasPoint(m.endpointAUiNorm),
      hasEndpointB: hasPoint(m.endpointBUiNorm),
      hasAxis: hasPoint(m.axisUiNorm),
      thickness: m.thicknessUiNorm,
    };
  }, null as any);

  expect(out.ok).toBe(true);
  expect(out.hasEndpointPinky).toBe(true);
  expect(out.hasEndpointIndex).toBe(true);
  expect(out.hasEndpointA).toBe(true);
  expect(out.hasEndpointB).toBe(true);
  expect(out.hasAxis).toBe(true);
  expect(typeof out.thickness).toBe('number');
});

// Asymmetric extension is a primary affordance: one side longer.
// RED contract: endpointA/endpointB reflect current extensionFracA/B and should be measurably different.

test('v23 RED: asymmetric extension yields measurably different endpoint distances', async ({ hfoPage }) => {
  await safeGoto(hfoPage, GEN6_V23_TEST_URL_LIGHT);

  const out = await safeEvaluate(hfoPage, () => {
    const m = (window as any).__hfoSwordTouch2dMarker;
    if (!m) return { ok: false, reason: 'missing __hfoSwordTouch2dMarker' };

    const a = m.endpointAUiNorm;
    const b = m.endpointBUiNorm;
    const baseA = m.baseEndpointAUiNorm ?? null;
    const baseB = m.baseEndpointBUiNorm ?? null;

    const dist = (p: any, q: any) => Math.hypot((p?.x ?? 0) - (q?.x ?? 0), (p?.y ?? 0) - (q?.y ?? 0));

    // If base endpoints are exposed, assert extension distances differ. Otherwise, fail with reason.
    if (!baseA || !baseB) return { ok: false, reason: 'missing baseEndpointAUiNorm/baseEndpointBUiNorm for extension measurement' };

    return { ok: true, extA: dist(a, baseA), extB: dist(b, baseB) };
  }, null as any);

  expect(out.ok).toBe(true);
  // extA/extB are only present when ok==true.
  expect(Math.abs(Number(out.extA) - Number(out.extB))).toBeGreaterThan(0.02);
});
