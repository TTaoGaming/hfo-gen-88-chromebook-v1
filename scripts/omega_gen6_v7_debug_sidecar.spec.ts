// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_V7_URL =
  process.env.HFO_GEN6_V7_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v7.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true';

test('Gen6 v7: dev debug sidecar shows SRP components concurrently', async ({ hfoPage }) => {
  await hfoPage.goto(GEN6_V7_URL);

  await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });

  const out = await hfoPage.evaluate(() => {
    const titles = Array.from(document.querySelectorAll('.lm_title')).map((el) => (el.textContent || '').trim());

    const counts = {
      videoFeed: document.querySelectorAll('#video-feed').length,
      overlayCanvas: document.querySelectorAll('#overlay-canvas').length,
      touch2dCanvas: document.querySelectorAll('#touch2d-hero-canvas').length,
      babylonWrap: document.querySelectorAll('#babylon-juice-overlay').length,
      excalidrawIframe: document.querySelectorAll('#excalidraw-wrapper-iframe').length,
      dinoIframe: document.querySelectorAll('#dino-wrapper-iframe').length,
    };

    return {
      titles,
      counts,
      hasPorts: !!(window as any).hfoPorts,
      hasRegistry: !!(window as any).hfoSubstrateRegistry,
    };
  });

  expect(out.hasPorts).toBe(true);
  expect(out.hasRegistry).toBe(true);

  // Dev sidecar should be SRP-first.
  expect(out.titles).toContain('Video');
  expect(out.titles).toContain('Touch2D');
  expect(out.titles).toContain('Babylon');
  expect(out.titles).toContain('Excalidraw');
  expect(out.titles).toContain('Dino Runner');

  // HERO is reserved for kiosk/essentials; not expected in this dev layout gate.
  expect(out.titles).not.toContain('Hero');

  // All SRP visualizations are singletons and present.
  expect(out.counts.videoFeed).toBe(1);
  expect(out.counts.overlayCanvas).toBe(1);
  expect(out.counts.touch2dCanvas).toBe(1);
  expect(out.counts.babylonWrap).toBe(1);
  expect(out.counts.excalidrawIframe).toBe(1);
  expect(out.counts.dinoIframe).toBe(1);
});
