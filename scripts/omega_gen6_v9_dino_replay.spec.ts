// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_V9_URL =
  process.env.HFO_GEN6_V9_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v9.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true&mode=dev';

const GOLDEN_MANIFEST_URL =
  process.env.HFO_GEN6_V9_REPLAY_MANIFEST_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/fixtures/replay/gen6_v9_dino_readiness_golden.json';

test('Gen6 v9: Dino readiness golden replay (8 sequences)', async ({ hfoPage }) => {
  const pageErrors: string[] = [];
  const consoleErrors: string[] = [];

  hfoPage.on('pageerror', (err) => {
    pageErrors.push(String((err as any)?.message || err));
  });

  hfoPage.on('console', (msg) => {
    if (msg.type() !== 'error') return;
    consoleErrors.push(msg.text());
  });

  await hfoPage.goto(GEN6_V9_URL);
  await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });
  await hfoPage.waitForFunction(() => !!(window as any).hfoReplay, null, { timeout: 20_000 });

  const run = await hfoPage.evaluate(async (manifestUrl) => {
    const anyWindow = window as any;
    const loaded = await anyWindow.hfoReplay.loadManifestUrl(manifestUrl);
    const manifest = anyWindow.hfoReplay.getManifest();
    const out = await anyWindow.hfoReplay.runAll();
    return { loaded, manifestVersion: manifest?.version || 'unknown', manifestCount: manifest?.sequences?.length || 0, out };
  }, GOLDEN_MANIFEST_URL);

  expect(run.manifestCount).toBe(8);
  expect(run.out?.reports?.length).toBe(8);

  for (const rep of run.out.reports) {
    const exp = rep.expect || {};

    if (typeof exp.minNematocyst === 'number') {
      expect(rep.counts.nematocyst, `${rep.sequenceId}: nematocyst < min`).toBeGreaterThanOrEqual(exp.minNematocyst);
    }
    if (typeof exp.maxNematocyst === 'number') {
      expect(rep.counts.nematocyst, `${rep.sequenceId}: nematocyst > max`).toBeLessThanOrEqual(exp.maxNematocyst);
    }
    if (typeof exp.minPostMessageOk === 'number') {
      expect(rep.counts.dinoPostMessageOk, `${rep.sequenceId}: dino_postMessage ok < min`).toBeGreaterThanOrEqual(exp.minPostMessageOk);
    }

    expect(rep.counts.dinoPostMessageErr, `${rep.sequenceId}: dino_postMessage errors`).toBe(0);
  }

  const allowlisted = (msg: string) => {
    const allow = [/ResizeObserver loop limit exceeded/i, /Permissions-Policy/i, /The AudioContext was not allowed to start/i];
    return allow.some((re) => re.test(msg));
  };

  const unexpectedPageErrors = pageErrors.filter((e) => !allowlisted(e));
  const unexpectedConsoleErrors = consoleErrors.filter((e) => !allowlisted(e));

  expect(unexpectedPageErrors, `Unexpected page errors:\n${unexpectedPageErrors.join('\n')}`).toEqual([]);
  expect(unexpectedConsoleErrors, `Unexpected console errors:\n${unexpectedConsoleErrors.join('\n')}`).toEqual([]);
});
