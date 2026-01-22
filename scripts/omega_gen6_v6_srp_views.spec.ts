// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_V6_URL =
  process.env.HFO_GEN6_V6_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v6.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true&flag-ui-excalidraw=true';

test('Gen6 v6: SRP views mount concurrently (no Hero)', async ({ hfoPage }) => {
  await hfoPage.goto(GEN6_V6_URL);

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

  // No monolithic Hero tab.
  expect(out.titles).not.toContain('Hero');

  // All SRP visualizations are singletons and present.
  expect(out.counts.videoFeed).toBe(1);
  expect(out.counts.overlayCanvas).toBe(1);
  expect(out.counts.touch2dCanvas).toBe(1);
  expect(out.counts.babylonWrap).toBe(1);
  expect(out.counts.excalidrawIframe).toBe(1);
  expect(out.counts.dinoIframe).toBe(1);
});
