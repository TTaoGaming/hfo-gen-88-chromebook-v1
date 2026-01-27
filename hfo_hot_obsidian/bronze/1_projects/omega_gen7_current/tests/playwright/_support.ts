// Medallion: Bronze | Mutation: 0% | HIVE: V
import type { Page } from '@playwright/test';

export const GEN7_V1_PORTABLE_APP_BASE =
  'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen7_current/app';

export const GEN7_V1_PORTABLE_V23_10_URL_BASE = `${GEN7_V1_PORTABLE_APP_BASE}/omega_gen6_v23_10.html`;
export const GEN7_V1_PORTABLE_DINO_WRAPPER_URL_BASE = `${GEN7_V1_PORTABLE_APP_BASE}/dino_v1_wrapper.html`;

export function buildLightUrl(base: string, extraQuery: string): string {
  const cb = Date.now();
  // Keep these flags aligned with Chromebook low-RAM stability.
  const flags =
    'flag-disable-camera=true'
    + '&flag-engine-babylon=false'
    + '&flag-engine-canvas=false'
    + '&flag-ui-golden-layout=false'
    + '&flag-ui-excalidraw=false'
    + '&flag-ui-lil-gui=false'
    + '&flag-ui-microkernel=false'
    + '&kiosk=0&hero=0&mode=dev';

  const sep = base.includes('?') ? '&' : '?';
  return `${base}${sep}__cb=${cb}&${flags}${extraQuery ? `&${extraQuery}` : ''}`;
}

export async function safeGoto(page: Page, url: string, attempts = 2): Promise<void> {
  let lastErr: unknown;
  for (let i = 0; i < attempts; i++) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded' });
      return;
    } catch (e) {
      lastErr = e;
      try {
        await page.waitForTimeout(250);
      } catch {
        // ignore
      }
    }
  }
  throw lastErr;
}

export async function safeEvaluate<T, A>(page: Page, fn: (arg: A) => T | Promise<T>, arg: A, attempts = 2): Promise<T> {
  let lastErr: unknown;
  for (let i = 0; i < attempts; i++) {
    try {
      return await page.evaluate(fn as any, arg as any);
    } catch (e) {
      lastErr = e;
      try {
        await page.waitForTimeout(250);
      } catch {
        // ignore
      }
    }
  }
  throw lastErr;
}
