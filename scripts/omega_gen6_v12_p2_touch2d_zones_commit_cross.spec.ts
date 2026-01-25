// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';

const GEN6_URL =
  process.env.HFO_GEN6_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v12.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&mode=dev';

const GOLDEN_PATH =
  'hfo_hot_obsidian/bronze/3_resources/fixtures/touch2d/gen6_v12_commit_zone_cross_top_bottom_golden.json';

test('Gen6 v12 (TDD RED): COMMIT fingertip crossing top/bottom touch2d zones emits P2 + P3(Space)', async ({ hfoPage }) => {
  const golden = JSON.parse(fs.readFileSync(GOLDEN_PATH, 'utf-8'));
  expect(Array.isArray(golden?.frames)).toBeTruthy();

  await hfoPage.goto(GEN6_URL, { waitUntil: 'domcontentloaded' });
  await hfoPage.waitForTimeout(200);

  const out = await hfoPage.evaluate((frames) => {
    const w = window as any;

    // These are the required runtime hooks for this test.
    if (!w.systemState) throw new Error('missing systemState');
    if (!w.hfoP2GestureLanguage?.tick) throw new Error('missing hfoP2GestureLanguage.tick');

    // Force-enable P2 gesture language and allow P3 dispatch.
    w.systemState.parameters = w.systemState.parameters || {};
    w.systemState.parameters.p2 = w.systemState.parameters.p2 || {};
    w.systemState.parameters.p2.gestureLanguage = {
      ...(w.systemState.parameters.p2.gestureLanguage || {}),
      enabled: true,
      emitP3: true,
      emitTelemetry: true,
      minReadiness: 0.2,
    };

    const captured = {
      p2: [] as Array<{ port: string; type: string; payload: any }>,
      p3Telemetry: [] as Array<{ port: string; type: string; payload: any }>,
      p3Nematocysts: [] as any[],
      perFrameReports: [] as any[],
    };

    // Capture Port2 emits.
    w.hfoPortsEffects = w.hfoPortsEffects || {};
    const originalEmit = w.hfoPortsEffects.emit;
    w.hfoPortsEffects.emit = (port: string, type: string, payload: any) => {
      if (port === 'p2') captured.p2.push({ port, type, payload });
      if (port === 'p3') captured.p3Telemetry.push({ port, type, payload });
      if (typeof originalEmit === 'function') {
        try {
          return originalEmit(port, type, payload);
        } catch {
          // ignore
        }
      }
      return true;
    };

    // Stub P3 injector so keyboard payloads are observable without needing the iframe.
    w.P3InjectorPort = {
      sendNematocystToDino: (payload: any) => {
        captured.p3Nematocysts.push(payload);
        return true;
      },
    };

    const dataFabric = { cursors: [] as any[], systemTime: 0, frameId: 0 };

    for (const f of frames) {
      dataFabric.frameId++;
      dataFabric.systemTime = Number(f?.now || 0);
      dataFabric.cursors = [
        {
          ...f.cursor,
          normX: f.cursor?.uiNormX,
          normY: f.cursor?.uiNormY,
        },
      ];

      const report = w.hfoP2GestureLanguage.tick({
        now: Number(f?.now || 0),
        dt: Number(f?.dt || 16),
        dataFabric,
      });

      captured.perFrameReports.push(report);
    }

    return captured;
  }, golden.frames);

  const p2Types = out?.p2?.map((e: any) => e.type) || [];

  // Desired behavior (will be RED until v12 zones exist + COMMIT gating is implemented):
  expect(p2Types.includes('zone_enter'), 'Expected P2 zone_enter').toBeTruthy();
  expect(p2Types.includes('zone_exit'), 'Expected P2 zone_exit').toBeTruthy();

  const nematocysts: any[] = out?.p3Nematocysts || [];
  const hasSpace = nematocysts.some((p) => p?.kind === 'keyboard' && (p?.key === ' ' || p?.code === 'Space'));
  expect(hasSpace, 'Expected a P3 keyboard Space nematocyst payload on bottom-zone enter').toBeTruthy();
});
