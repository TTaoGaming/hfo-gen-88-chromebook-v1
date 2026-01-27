// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';

/**
 * UI Conformance Contract (guardrail, not a full spec prover)
 *
 * Scope: heuristic checks for
 * - W3C: Pointer Events availability + non-crash dispatch
 * - Material 3: presence of core M3 CSS tokens
 * - GoldenLayout: layout container + GL content exists and remains visible after resize
 * - lil-gui: GUI root visible when enabled
 * - Apple HIG: minimal touch-target heuristic when buttons exist
 *
 * Default behavior: SKIPPED unless explicitly enabled.
 * Enable with: HFO_UI_CONFORMANCE=1
 */

test.describe('Omega UI conformance contract (opt-in)', () => {
    test.beforeEach(() => {
        test.skip(process.env.HFO_UI_CONFORMANCE !== '1', 'Set HFO_UI_CONFORMANCE=1 to enable this guardrail.');
    });

    test('Active Omega satisfies baseline UI contracts (HIG/W3C/M3/GoldenLayout/lil-gui)', async ({ page }) => {
        // Use active entrypoint so the “current Omega” target must satisfy the contract.
        const base = 'http://localhost:8889/active_omega.html';
        const url = base + '?flag-ui-lil-gui=true';

        await page.goto(url, { waitUntil: 'networkidle' });

        // GoldenLayout must exist as layout engine.
        const layoutContainer = page.locator('#layout-container');
        await expect(layoutContainer).toBeVisible();
        await expect(page.locator('.lm_content').first()).toBeVisible({ timeout: 20000 });

        // Material 3: core tokens present (heuristic: computed style returns a non-empty value).
        const m3 = await page.evaluate(() => {
            const cs = getComputedStyle(document.documentElement);
            const keys = [
                '--md-sys-color-primary',
                '--md-sys-color-on-primary',
                '--md-sys-color-surface',
                '--md-sys-color-on-surface',
            ];
            const values = Object.fromEntries(keys.map(k => [k, (cs.getPropertyValue(k) || '').trim()]));
            const ok = keys.every(k => values[k] && values[k].length > 0);
            return { ok, values };
        });
        expect(m3.ok).toBe(true);

        // W3C: PointerEvent exists and dispatch does not throw.
        const pointer = await page.evaluate(() => {
            const hasPointerEvent = typeof (window as any).PointerEvent === 'function';
            let dispatchOk = false;
            try {
                if (hasPointerEvent) {
                    const ev = new PointerEvent('pointerdown', {
                        pointerId: 1,
                        pointerType: 'mouse',
                        clientX: 10,
                        clientY: 10,
                        bubbles: true,
                        cancelable: true,
                    });
                    dispatchOk = document.body.dispatchEvent(ev);
                }
            } catch {
                dispatchOk = false;
            }
            return { hasPointerEvent, dispatchOk };
        });
        expect(pointer.hasPointerEvent).toBe(true);
        expect(pointer.dispatchOk).toBe(true);

        // lil-gui: if enabled, a root should be present (heuristic selector).
        const gui = page.locator('.lil-gui, .lil-gui.root').first();
        await expect(gui).toBeVisible({ timeout: 20000 });

        // Responsiveness: after resize, layout container still has non-zero size.
        await page.setViewportSize({ width: 900, height: 600 });
        const a = await layoutContainer.boundingBox();
        expect(a && a.width > 100 && a.height > 100).toBeTruthy();

        await page.setViewportSize({ width: 1400, height: 900 });
        const b = await layoutContainer.boundingBox();
        expect(b && b.width > 100 && b.height > 100).toBeTruthy();

        // Apple HIG (heuristic): if any visible button exists, its tap target should be >= 44px height.
        const btn = page.locator('button:visible').first();
        if (await btn.count()) {
            const bb = await btn.boundingBox();
            if (bb) expect(bb.height).toBeGreaterThanOrEqual(44);
        }

        // Meta viewport should exist.
        const viewportMeta = page.locator('meta[name="viewport"]').first();
        await expect(viewportMeta).toHaveCount(1);
    });
});
