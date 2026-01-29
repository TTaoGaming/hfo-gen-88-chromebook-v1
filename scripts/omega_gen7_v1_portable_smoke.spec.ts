// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import { safeGoto } from './omega_gen6_test_guards';

test.describe.configure({ mode: 'serial', retries: 0 });

const GEN7_V1_URL =
  "http://localhost:8889/hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/app/omega_gen7_v1.html" +
  "?__cb=";

test("Gen7 v1: loads and exports core globals", async ({ hfoPage }) => {
  const url =
    GEN7_V1_URL +
    String(Date.now()) +
    "&flag-disable-camera=true" +
    "&flag-engine-babylon=false" +
    "&flag-engine-canvas=false" +
    "&flag-ui-golden-layout=false" +
    "&flag-ui-excalidraw=false" +
    "&flag-ui-lil-gui=false" +
    "&flag-ui-microkernel=false" +
    "&kiosk=0&hero=0&mode=dev";

  await safeGoto(hfoPage, url);
  await hfoPage.waitForTimeout(250);

  const ok = await hfoPage.evaluate(() => {
    const w = window as any;
    return {
      hasSystemState: Boolean(w.systemState),
      hasHfoStateAlias: Boolean(w.hfoState),
      hasPortsEffects: Boolean(
        w.hfoPortsEffects?.emit && w.hfoPortsEffects?.getRecent,
      ),
      hasP2Tripwire: Boolean(w.hfoP2TripwireThread?.tick),
      hasP3Injector: Boolean(w.hfoP3PlanckSensorInjector?.tick),
    };
  });

  expect(ok.hasSystemState).toBe(true);
  expect(ok.hasHfoStateAlias).toBe(true);
  expect(ok.hasPortsEffects).toBe(true);
  expect(ok.hasP2Tripwire).toBe(true);
  expect(ok.hasP3Injector).toBe(true);
});
