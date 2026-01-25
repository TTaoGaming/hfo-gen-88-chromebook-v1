// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_V8_URL =
  process.env.HFO_GEN6_V8_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v8.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true';

test('Gen6 v8: Ports Effects panel mounts and receives events', async ({ hfoPage }) => {
  const pageErrors: string[] = [];
  const consoleErrors: string[] = [];

  hfoPage.on('pageerror', (err) => {
    pageErrors.push(String((err as any)?.message || err));
  });

  hfoPage.on('console', (msg) => {
    if (msg.type() !== 'error') return;
    consoleErrors.push(msg.text());
  });

  await hfoPage.goto(GEN6_V8_URL);

  await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });

  const out = await hfoPage.evaluate(() => {
    const titles = Array.from(document.querySelectorAll('.lm_title')).map((el) => (el.textContent || '').trim());

    return {
      titles,
      hasPortsEffectsBus: !!(window as any).hfoPortsEffects,
      hasPortsFacade: !!(window as any).hfoPorts,
      hasP7EffectsFacade: !!(window as any).hfoPorts?.p7?.effects,
      hasEffectsPanel: !!document.querySelector('[data-testid="ports-effects-panel"]'),
    };
  });

  expect(out.hasPortsFacade).toBe(true);
  expect(out.hasPortsEffectsBus).toBe(true);
  expect(out.hasP7EffectsFacade).toBe(true);
  expect(out.hasEffectsPanel).toBe(true);
  expect(out.titles).toContain('Ports Effects');

  await hfoPage.evaluate(() => {
    // Write a deterministic test event.
    (window as any).hfoPortsEffects?.emit?.('p3', 'test_event', { hello: 'world' });
  });

  await hfoPage.waitForFunction(() => {
    const el = document.querySelector('#ports-effects-log');
    const t = el?.textContent || '';
    return t.includes('test_event') && t.includes('hello') && t.includes('world');
  }, null, { timeout: 10_000 });

  // Exercise the Babylon projection path without requiring camera/MediaPipe.
  await hfoPage.evaluate(() => {
    const anyWindow = window as any;
    const systemState = anyWindow.systemState;
    const juice =
      systemState?.ui?.juiceLayers?.find((j: any) => j?.name === 'babylon-juice') || systemState?.ui?.juiceLayers?.[0];

    if (!juice) throw new Error('No juice layer found');

    if (juice?.canvas?.style) {
      juice.canvas.style.display = 'block';
      juice.canvas.style.width = '640px';
      juice.canvas.style.height = '360px';
    }
    if (juice?.engine?.resize) juice.engine.resize();

    const landmarks = Array.from({ length: 21 }, (_, i) => ({
      x: 0.4 + (i % 5) * 0.01,
      y: 0.4 + Math.floor(i / 5) * 0.01,
      z: 0,
    }));

    juice.update?.([
      {
        handIndex: 0,
        fsmState: 'READY',
        uiNormX: 0.5,
        uiNormY: 0.5,
        normZ: 0,
        skeletonAlpha: 1,
        landmarks,
      },
    ]);
  });

  // Give any async render loops a moment to surface issues.
  await hfoPage.waitForTimeout(250);

  const allowlisted = (msg: string) => {
    // Keep allowlist small and explicit: only benign/known noisy cases.
    const allow = [/ResizeObserver loop limit exceeded/i, /Permissions-Policy/i, /The AudioContext was not allowed to start/i];
    return allow.some((re) => re.test(msg));
  };

  const unexpectedPageErrors = pageErrors.filter((e) => !allowlisted(e));
  const unexpectedConsoleErrors = consoleErrors.filter((e) => !allowlisted(e));

  expect(unexpectedPageErrors, `Unexpected page errors:\n${unexpectedPageErrors.join('\n')}`).toEqual([]);
  expect(unexpectedConsoleErrors, `Unexpected console errors:\n${unexpectedConsoleErrors.join('\n')}`).toEqual([]);
});
