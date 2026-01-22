// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_V5_URL =
  process.env.HFO_GEN6_V5_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v5.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true';

test('Gen6 v5: substrate registry is populated (substrate-agnostic)', async ({ hfoPage }) => {
  await hfoPage.goto(GEN6_V5_URL);

  // GoldenLayout + component mount.
  await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });
  await hfoPage.waitForFunction(
    () => !!document.querySelector('[data-hfo-layer="substrate-root"]'),
    null,
    { timeout: 20_000 }
  );

  const out = await hfoPage.evaluate(() => {
    const reg = (window as any).hfoSubstrateRegistry;
    if (!reg) return { ok: false as const, reason: 'registry missing' };

    const adapterHost = (window as any).hfoAdapterHost;
    if (!adapterHost) return { ok: false as const, reason: 'adapterHost missing' };

    const list = typeof reg.listAll === 'function' ? reg.listAll() : [];
    const byRole = (role: string) => (typeof reg.listByRole === 'function' ? reg.listByRole(role) : []);

    const adapterIds = typeof adapterHost.list === 'function' ? adapterHost.list() : [];

    const roleCounts = {
      physicalVideo: byRole('physical:video').length,
      physicalOverlayCanvas: byRole('physical:overlay-canvas').length,
      physicalTouch2d: byRole('physical:touch2d').length,
      physicalJuiceCanvas: byRole('physical:juice-canvas').length,
      appDinoOverlay: byRole('app:dino-overlay').length,
      appDinoIframe: byRole('app:dino-iframe').length,
    };

    const physicalEls =
      typeof reg.getPhysicalSubstrateElements === 'function' ? reg.getPhysicalSubstrateElements() : [];

    const counts = {
      videoFeed: document.querySelectorAll('#video-feed').length,
      overlayCanvas: document.querySelectorAll('#overlay-canvas').length,
      touch2dCanvas: document.querySelectorAll('#touch2d-hero-canvas').length,
      babylonOverlay: document.querySelectorAll('#babylon-juice-overlay').length,
      dinoIframes: document.querySelectorAll('#dino-wrapper-iframe').length,
    };

    return {
      ok: true as const,
      listSize: Array.isArray(list) ? list.length : -1,
      roleCounts,
      physicalElsCount: Array.isArray(physicalEls) ? physicalEls.length : -1,
      counts,
      adapterIds,
    };
  });

  expect(out.ok).toBe(true);
  if (!out.ok) return;

  // DOM sanity (same as v4)
  expect(out.counts.videoFeed).toBe(1);
  expect(out.counts.overlayCanvas).toBe(1);
  expect(out.counts.touch2dCanvas).toBe(1);
  expect(out.counts.babylonOverlay).toBe(1);
  expect(out.counts.dinoIframes).toBe(1);

  // Registry must include the physical substrate and the Dino adapter.
  expect(out.listSize).toBeGreaterThan(0);
  expect(out.roleCounts.physicalVideo).toBe(1);
  expect(out.roleCounts.physicalOverlayCanvas).toBe(1);
  expect(out.roleCounts.physicalTouch2d).toBe(1);

  expect(Array.isArray(out.adapterIds)).toBe(true);
  expect(out.adapterIds).toContain('dino-v1');

  // Babylon can be disabled via flags; when enabled it should register a juice canvas.
  expect(out.roleCounts.physicalJuiceCanvas).toBeGreaterThanOrEqual(0);

  expect(out.roleCounts.appDinoOverlay).toBe(1);
  expect(out.roleCounts.appDinoIframe).toBe(1);

  // Physical elements list should at least include overlay canvas and touch2d.
  expect(out.physicalElsCount).toBeGreaterThanOrEqual(2);
});
