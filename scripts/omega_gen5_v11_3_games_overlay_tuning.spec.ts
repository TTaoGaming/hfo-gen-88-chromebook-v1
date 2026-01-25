// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const ENTRYPOINT_URL =
    process.env.HFO_ENTRYPOINT_URL ||
    'http://localhost:8889/active_hfo_omega_entrypoint.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

function withFlag(urlStr: string, key: string, value: string) {
    const url = new URL(urlStr);
    url.searchParams.set(`flag-${key}`, value);
    return url.toString();
}

function withTarget(urlStr: string, targetPath: string) {
    const url = new URL(urlStr);
    url.searchParams.set('target', targetPath);
    return url.toString();
}

test('Gen5 v11.3: AppHost activates sandbox; overlay tuning applies; target router resolves inside active iframe', async ({ hfoPage }) => {
    const target = '/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v11_3.html';

    const url = withTarget(ENTRYPOINT_URL, target);

    await hfoPage.goto(
        withFlag(
            withFlag(withFlag(url, 'ui-multiapp', 'true'), 'p3-target-active-app', 'true'),
            'p5-defend-strict-v11_1',
            'true'
        )
    );

    await hfoPage.waitForURL(/omega_gen5_v11_3\.html/i, { timeout: 20000 });
    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return !!(window.hfoTokens && window.hfoRegistry);
    }, null, { timeout: 20000 });
    await hfoPage.initHFO();

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        const ports = window.hfoPorts;
        // @ts-ignore
        const tokens = window.hfoTokens;
        // @ts-ignore
        const registry = window.hfoRegistry;

        const apps = ports?.p7?.apps;
        const nav = ports?.p7?.navigate;
        if (!apps) throw new Error('P7.apps facade missing');
        if (!nav) throw new Error('P7.navigate facade missing');

        apps.activate('sandbox');

        const overlay = document.querySelector('#sandbox-hero-overlay') as HTMLDivElement | null;
        const iframe = document.querySelector('#sandbox-iframe') as HTMLIFrameElement | null;
        const hero = document.querySelector('.hero-view-container') as HTMLDivElement | null;
        if (!overlay) throw new Error('sandbox overlay missing');
        if (!iframe) throw new Error('sandbox iframe missing');
        if (!hero) throw new Error('hero container missing');

        // Apply global overlay tuning (non-GUI path)
        nav.patchParameters({
            apps: {
                overlay: { opacity: 0.5, zoom: 1.25, rememberPerApp: false }
            }
        });
        apps.applyActiveOverlayTuning();

        const heroRect = hero.getBoundingClientRect();
        const overlayRect = overlay.getBoundingClientRect();

        const router = registry.resolve(tokens.P3_TARGET_ROUTER);
        const viewX = heroRect.left + heroRect.width / 2;
        const viewY = heroRect.top + heroRect.height / 2;
        const resolved = router.resolveTargetAt?.(viewX, viewY);

        const ok =
            !!resolved &&
            !!resolved.target &&
            !!iframe.contentDocument &&
            resolved.target.ownerDocument === iframe.contentDocument;

        return {
            activeId: apps.getActiveId(),
            overlayDisplay: overlay.style.display,
            overlayOpacity: overlay.style.opacity,
            heroW: heroRect.width,
            overlayW: overlayRect.width,
            overlayH: overlayRect.height,
            resolveOk: ok,
            resolveTag: resolved?.target?.tagName || null
        };
    });

    expect(out.activeId).toBe('sandbox');
    expect(out.overlayDisplay).toBe('block');
    expect(out.overlayOpacity).toBe('0.5');

    // zoom>1 expands overlay box (cropped by hero)
    expect(out.overlayW).toBeGreaterThan(out.heroW);
    expect(out.overlayH).toBeGreaterThan(0);

    expect(out.resolveOk).toBe(true);
    expect(['CANVAS', 'DIV', 'BODY']).toContain(out.resolveTag);
});

test('Gen5 v11.3 games: GoldenLayout tab selection activates AppHost (brick breaker)', async ({ hfoPage }) => {
    const target = '/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v11_3.html';

    const url = withTarget(ENTRYPOINT_URL, target);

    await hfoPage.goto(
        withFlag(
            withFlag(withFlag(url, 'ui-multiapp', 'true'), 'p3-target-active-app', 'true'),
            'p5-defend-strict-v11_1',
            'true'
        )
    );

    await hfoPage.waitForURL(/omega_gen5_v11_3\.html/i, { timeout: 20000 });
    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return !!(window.hfoTokens && window.hfoRegistry);
    }, null, { timeout: 20000 });
    await hfoPage.initHFO();

    const sandboxTab = hfoPage.locator('.lm_tab .lm_title', { hasText: 'App: Sandbox' }).first();
    await sandboxTab.waitFor({ state: 'visible', timeout: 20000 });
    await sandboxTab.click();

    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return window.hfoPorts?.p7?.apps?.getActiveId?.() === 'sandbox';
    }, null, { timeout: 20000 });

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        const ports = window.hfoPorts;
        // @ts-ignore
        const tokens = window.hfoTokens;
        // @ts-ignore
        const registry = window.hfoRegistry;

        const apps = ports?.p7?.apps;
        if (!apps) throw new Error('P7.apps facade missing');

        const overlay = document.querySelector('#sandbox-hero-overlay') as HTMLDivElement | null;
        const iframe = document.querySelector('#sandbox-iframe') as HTMLIFrameElement | null;
        if (!overlay) throw new Error('sandbox overlay missing');
        if (!iframe) throw new Error('sandbox iframe missing');

        const router = registry.resolve(tokens.P3_TARGET_ROUTER);
        const r = overlay.getBoundingClientRect();
        const x = r.left + r.width / 2;
        const y = r.top + r.height / 2;
        const resolved = router.resolveTargetAt?.(x, y);

        const ok =
            !!resolved &&
            !!resolved.target &&
            !!iframe.contentDocument &&
            resolved.target.ownerDocument === iframe.contentDocument;

        return {
            activeId: apps.getActiveId(),
            overlayDisplay: overlay.style.display,
            resolveOk: ok,
            resolveTag: resolved?.target?.tagName || null
        };
    });

    expect(out.activeId).toBe('sandbox');
    expect(out.overlayDisplay).toBe('block');
    expect(out.resolveOk).toBe(true);
    expect(['CANVAS', 'DIV', 'BODY']).toContain(out.resolveTag);
});
