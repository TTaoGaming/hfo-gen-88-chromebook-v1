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

test('Gen5 v12: AppHost activates Pointer Lab; target router resolves inside active iframe', async ({ hfoPage }) => {
    const target = '/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html';

    const url = withTarget(ENTRYPOINT_URL, target);

    await hfoPage.goto(
        withFlag(
            withFlag(
                withFlag(
                    withFlag(withFlag(url, 'ui-multiapp', 'true'), 'ui-intent', 'true'),
                    'p3-target-active-app',
                    'true'
                ),
                'ui-games',
                'true'
            ),
            'p5-defend-strict-v11_1',
            'true'
        )
    );

    await hfoPage.waitForURL(/omega_gen5_v12\.html/i, { timeout: 20000 });
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
        if (!apps) throw new Error('P7.apps facade missing');

        apps.activate('pointer-lab');

        const overlay = document.querySelector('#pointer-lab-overlay') as HTMLDivElement | null;
        const iframe = document.querySelector('#pointer-lab-iframe') as HTMLIFrameElement | null;
        if (!overlay) throw new Error('pointer-lab overlay missing');
        if (!iframe) throw new Error('pointer-lab iframe missing');

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
            resolveTag: resolved?.target?.tagName || null,
        };
    });

    expect(out.activeId).toBe('pointer-lab');
    expect(out.overlayDisplay).toBe('block');
    expect(out.resolveOk).toBe(true);
    expect(['CANVAS', 'DIV', 'BODY']).toContain(out.resolveTag);
});

test('Gen5 v12: GoldenLayout tab activates Pointer Lab + intent can be injected', async ({ hfoPage }) => {
    const target = '/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html';

    const url = withTarget(ENTRYPOINT_URL, target);

    await hfoPage.goto(
        withFlag(
            withFlag(
                withFlag(
                    withFlag(withFlag(url, 'ui-multiapp', 'true'), 'ui-intent', 'true'),
                    'p3-target-active-app',
                    'true'
                ),
                'ui-games',
                'true'
            ),
            'p5-defend-strict-v11_1',
            'true'
        )
    );

    await hfoPage.waitForURL(/omega_gen5_v12\.html/i, { timeout: 20000 });
    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return !!(window.hfoTokens && window.hfoRegistry);
    }, null, { timeout: 20000 });
    await hfoPage.initHFO();

    const labTab = hfoPage.locator('.lm_tab .lm_title', { hasText: 'App: Pointer Lab' }).first();
    await labTab.waitFor({ state: 'visible', timeout: 20000 });
    await labTab.click();

    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return window.hfoPorts?.p7?.apps?.getActiveId?.() === 'pointer-lab';
    }, null, { timeout: 20000 });

    const out = await hfoPage.evaluate(() => {
        // @ts-ignore
        const ports = window.hfoPorts;
        const nav = ports?.p7?.navigate;
        const apps = ports?.p7?.apps;
        if (!nav) throw new Error('P7.navigate facade missing');
        if (!apps) throw new Error('P7.apps facade missing');

        const applied = nav.setIntent({ goal: 'unit-test', app: 'pointer-lab' });

        // Optional stigmergy emission should be present and safe.
        // @ts-ignore
        const stig = window.hfoStigmergy;
        const emitted = stig?.emit?.('intent.set', { intent: { goal: 'unit-test' } }) || null;

        return {
            activeId: apps.getActiveId(),
            intentTs: applied?.ts || null,
            intentGoal: applied?.intent?.goal || null,
            emittedType: emitted?.type || null,
        };
    });

    expect(out.activeId).toBe('pointer-lab');
    expect(typeof out.intentTs).toBe('string');
    expect(out.intentGoal).toBe('unit-test');
    expect(out.emittedType).toBe('intent.set');
});

test('Gen5 v12: App dropdown switches to Breakout (MDN) with active-app routing', async ({ hfoPage }) => {
    const target = '/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v12.html';

    const url = withTarget(ENTRYPOINT_URL, target);

    await hfoPage.goto(
        withFlag(
            withFlag(withFlag(withFlag(url, 'ui-multiapp', 'true'), 'ui-intent', 'true'), 'p3-target-active-app', 'true'),
            'p5-defend-strict-v11_1',
            'true'
        )
    );

    await hfoPage.waitForURL(/omega_gen5_v12\.html/i, { timeout: 20000 });
    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return !!(window.hfoTokens && window.hfoRegistry);
    }, null, { timeout: 20000 });
    await hfoPage.initHFO();

    const dropdown = hfoPage.locator('#hfo-app-dropdown').first();
    await dropdown.waitFor({ state: 'visible', timeout: 20000 });
    await dropdown.selectOption('breakout-mdn');

    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return window.hfoPorts?.p7?.apps?.getActiveId?.() === 'breakout-mdn';
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

        const overlay = document.querySelector('#breakout-overlay') as HTMLDivElement | null;
        const iframe = document.querySelector('#breakout-iframe') as HTMLIFrameElement | null;
        if (!overlay) throw new Error('breakout overlay missing');
        if (!iframe) throw new Error('breakout iframe missing');

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
            resolveTag: resolved?.target?.tagName || null,
        };
    });

    expect(out.activeId).toBe('breakout-mdn');
    expect(out.overlayDisplay).toBe('block');
    expect(out.resolveOk).toBe(true);
    expect(typeof out.resolveTag).toBe('string');
});
