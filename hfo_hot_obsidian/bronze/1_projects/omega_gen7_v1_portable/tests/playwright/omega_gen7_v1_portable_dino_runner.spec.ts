// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import { GEN7_V1_PORTABLE_DINO_WRAPPER_URL_BASE, safeGoto } from './_support';

test.describe.configure({ mode: 'serial', retries: 1 });

test('Gen7 portable: Dino runner wrapper loads and nematocyst can inject Space (fail-closed)', async ({ page }) => {
  const url = `${GEN7_V1_PORTABLE_DINO_WRAPPER_URL_BASE}?__cb=${Date.now()}`;
  await safeGoto(page, url);

  // Fail-closed: wrapper must contain the runner iframe.
  await expect(page.locator('#frame')).toHaveCount(1);

  const frameLoc = page.frameLocator('#frame');

  // Fail-closed: vendored runner must be present (a prior regression was a 404 iframe).
  await frameLoc.locator('#messageBox').waitFor({ state: 'visible', timeout: 10_000 });
  await expect(frameLoc.locator('#messageBox')).toContainText('Press Space');

  // Send a nematocyst keypress and require an ack.
  const ack = await page.evaluate(async () => {
    const traceId = `pw_${Date.now()}_${Math.random().toString(16).slice(2)}`;

    const waitForAck = new Promise<any>((resolve, reject) => {
      const timeout = setTimeout(() => {
        window.removeEventListener('message', onMsg);
        reject(new Error('timed out waiting for hfo:nematocyst:ack'));
      }, 2500);

      const onMsg = (ev: MessageEvent) => {
        const d: any = ev?.data;
        if (!d || typeof d !== 'object') return;
        if (d.type !== 'hfo:nematocyst:ack') return;
        if (d.traceId !== traceId) return;
        clearTimeout(timeout);
        window.removeEventListener('message', onMsg);
        resolve(d);
      };

      window.addEventListener('message', onMsg);
    });

    // Same-window postMessage so adapter acks back to us.
    window.postMessage(
      {
        type: 'hfo:nematocyst',
        traceId,
        payload: {
          traceId,
          kind: 'keyboard',
          action: 'keypress',
          key: ' ',
          code: 'Space',
        },
      },
      window.location.origin,
    );

    return await waitForAck;
  });

  expect(ack?.payload?.ok).toBe(true);

  // Fail-closed: the runner should have reacted to Space (message box hidden).
  const boxHidden = await frameLoc.locator('#messageBox').evaluate((el) => {
    const style = (el as HTMLElement).style?.visibility;
    return style === 'hidden';
  });

  expect(boxHidden).toBe(true);
});
