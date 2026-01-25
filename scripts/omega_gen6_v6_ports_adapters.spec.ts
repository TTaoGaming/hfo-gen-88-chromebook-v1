// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN6_V6_URL =
  process.env.HFO_GEN6_V6_URL ||
  'http://localhost:8889/hfo_hot_obsidian/bronze/3_resources/para/omega_gen6_current/omega_gen6_v6.html?flag-disable-camera=true&flag-engine-babylon=true&flag-engine-canvas=true';

test('Gen6 v6: adapters are swappable via ports facade', async ({ hfoPage }) => {
  await hfoPage.goto(GEN6_V6_URL);

  // GoldenLayout + component mount.
  await hfoPage.waitForFunction(() => !!document.querySelector('#layout-container'), null, { timeout: 20_000 });
  await hfoPage.waitForFunction(
    () => !!document.querySelector('[data-hfo-layer="substrate-root"]'),
    null,
    { timeout: 20_000 }
  );

  const out = await hfoPage.evaluate(() => {
    const ports = (window as any).hfoPorts;
    if (!ports?.p7?.adapters) return { ok: false as const, reason: 'p7.adapters missing' };

    const adapters = ports.p7.adapters;

    const initialList = typeof adapters.list === 'function' ? adapters.list() : [];
    const initialActive = typeof adapters.getActiveId === 'function' ? adapters.getActiveId() : null;

    const registerOk = typeof adapters.register === 'function'
      ? adapters.register({
        id: 'test-noop-v1',
        kind: 'test',
        capabilities: ['effect:test'],
        deliverEffect: (effect: any) => {
          return effect?.kind === 'test';
        },
      })
      : false;

    const setOk = typeof adapters.setActiveId === 'function' ? adapters.setActiveId('test-noop-v1') : false;
    const activeAfter = typeof adapters.getActiveId === 'function' ? adapters.getActiveId() : null;

    const deliverOk = typeof adapters.deliverEffect === 'function'
      ? adapters.deliverEffect('test-noop-v1', { kind: 'test' })
      : false;

    const listAfter = typeof adapters.list === 'function' ? adapters.list() : [];

    return {
      ok: true as const,
      initialList,
      initialActive,
      registerOk,
      setOk,
      activeAfter,
      deliverOk,
      listAfter,
    };
  });

  expect(out.ok).toBe(true);
  if (!out.ok) return;

  // Must expose built-in adapter and allow swapping.
  expect(Array.isArray(out.initialList)).toBe(true);
  expect(out.initialList).toContain('dino-v1');

  expect(out.registerOk).toBe(true);
  expect(out.setOk).toBe(true);
  expect(out.activeAfter).toBe('test-noop-v1');
  expect(out.deliverOk).toBe(true);

  expect(Array.isArray(out.listAfter)).toBe(true);
  expect(out.listAfter).toContain('test-noop-v1');
});
