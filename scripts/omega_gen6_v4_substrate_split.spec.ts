// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_V4_URL =
  process.env.HFO_GEN6_V4_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v4.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true';

test('Gen6 v4: substrate pieces are SRP-separated (DOM ownership)', async ({ hfoPage }) => {
  await hfoPage.goto(GEN6_V4_URL);

  // GoldenLayout + component mount.
  await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });
  await hfoPage.waitForFunction(
    () => !!document.querySelector('[data-hfo-layer="substrate-root"]'),
    null,
    { timeout: 20_000 }
  );

  const out = await hfoPage.evaluate(() => {
    const root = document.querySelector('[data-hfo-layer="substrate-root"]');
    if (!root) return { ok: false as const, reason: 'substrate root missing' };

    const q = (sel: string) => root.querySelector(sel);

    const counts = {
      videoFeed: document.querySelectorAll('#video-feed').length,
      overlayCanvas: document.querySelectorAll('#overlay-canvas').length,
      touch2dCanvas: document.querySelectorAll('#touch2d-hero-canvas').length,
      babylonOverlay: document.querySelectorAll('#babylon-juice-overlay').length,
      dinoIframes: document.querySelectorAll('#dino-wrapper-iframe').length,
    };

    const layers = {
      video: !!q('[data-hfo-layer="video"]'),
      overlayCanvas: !!q('[data-hfo-layer="overlay-canvas"]'),
      touch2dCursor: !!q('[data-hfo-layer="touch2d-cursor"]'),
      babylon: !!q('[data-hfo-layer="babylon"]'),
      dinoOverlay: !!q('[data-hfo-layer="dino-overlay"]'),
      dinoIframe: !!q('[data-hfo-layer="dino-iframe"]'),
    };

    const dinoOverlay = q('[data-hfo-layer="dino-overlay"]') as HTMLElement | null;
    const dinoDisplay = dinoOverlay ? window.getComputedStyle(dinoOverlay).display : null;

    return { ok: true as const, layers, counts, dinoDisplay };
  });

  expect(out.ok).toBe(true);
  if (!out.ok) return;

  expect(out.counts.videoFeed).toBe(1);
  expect(out.counts.overlayCanvas).toBe(1);
  expect(out.counts.touch2dCanvas).toBe(1);
  expect(out.counts.babylonOverlay).toBe(1);
  expect(out.counts.dinoIframes).toBe(1);

  expect(out.layers.video).toBe(true);
  expect(out.layers.overlayCanvas).toBe(true);
  expect(out.layers.touch2dCursor).toBe(true);
  expect(out.layers.babylon).toBe(true);
  expect(out.layers.dinoOverlay).toBe(true);
  expect(out.layers.dinoIframe).toBe(true);

  // Default mode should hide Dino until explicitly toggled.
  expect(out.dinoDisplay).toBe('none');

  await hfoPage.click('#btn-hero-mode-dino');
  await hfoPage.waitForFunction(() => {
    const el = document.querySelector('[data-hfo-layer="dino-overlay"]') as HTMLElement | null;
    return !!el && window.getComputedStyle(el).display !== 'none';
  });
});
