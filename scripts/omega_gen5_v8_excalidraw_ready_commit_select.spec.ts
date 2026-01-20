// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_V8_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v8.html'
    + '?flag-engine-babylon=false'
    + '&flag-engine-canvas=true'
    + '&flag-disable-camera=true'
    + '&flag-ui-excalidraw=true'
    + '&flag-p3-adapter-standard=false'
    + '&flag-p3-legacy-click=true';

test('Gen5 v8: READY hover + COMMIT press selects Excalidraw tool on COMMIT (not release)', async ({ hfoPage }) => {
    await hfoPage.goto(GEN5_V8_URL);
    await hfoPage.initHFO();

    await hfoPage.evaluate(() => {
        // @ts-ignore
        const state = window.hfoState;
        if (!state) return;

        // Ensure Excalidraw is enabled/visible
        // @ts-ignore
        if (state.parameters?.excalidraw) state.parameters.excalidraw.enabled = true;
        // @ts-ignore
        if (state.ui?.excalidrawOverlay) state.ui.excalidrawOverlay.style.display = 'block';

        // Normalize viewport mapping for deterministic coords in tests
        // @ts-ignore
        if (state.ui?.viewBounds) {
            state.ui.viewBounds = {
                width: window.innerWidth,
                height: window.innerHeight,
                offsetX: 0,
                offsetY: 0,
                containerRect: { left: 0, top: 0, width: window.innerWidth, height: window.innerHeight },
            };
        }

        // Prepare parent-side log
        // @ts-ignore
        window.__hfoV8TapLog = { over: 0, down: 0, up: 0, click: 0, errors: [] as string[] };
    });

    await expect(hfoPage.locator('#excalidraw-iframe')).toBeVisible({ timeout: 20000 });

    const frame = hfoPage.frameLocator('#excalidraw-iframe');
    const rectTool = frame.locator('label[title*="Rectangle"]');
    await expect(rectTool).toBeVisible({ timeout: 20000 });

    // Attach event listeners inside the iframe, but store counters on parent for easy retrieval.
    await frame.locator('body').evaluate(() => {
        // @ts-ignore
        const log = window.parent.__hfoV8TapLog;
        const label = document.querySelector('label[title*="Rectangle"]');
        if (!label) {
            log.errors.push('missing_rect_tool');
            return;
        }

        // Avoid double-attachment if the test re-runs in same page.
        if ((label as any).__hfoAttached) return;
        (label as any).__hfoAttached = true;

        label.addEventListener('pointerover', () => { log.over += 1; });
        label.addEventListener('pointerdown', () => { log.down += 1; });
        label.addEventListener('pointerup', () => { log.up += 1; });
        label.addEventListener('click', () => { log.click += 1; });
    });

    const coords = await hfoPage.evaluate(() => {
        const iframe = document.querySelector('#excalidraw-iframe') as HTMLIFrameElement | null;
        if (!iframe || !iframe.contentDocument) return null;
        const el = iframe.contentDocument.querySelector('label[title*="Rectangle"]') as HTMLElement | null;
        if (!el) return null;

        const iframeRect = iframe.getBoundingClientRect();
        const elRect = el.getBoundingClientRect();

        return {
            x: iframeRect.left + elRect.left + elRect.width / 2,
            y: iframeRect.top + elRect.top + elRect.height / 2,
        };
    });
    expect(coords).toBeTruthy();
    if (!coords) return;

    const targetX = coords.x;
    const targetY = coords.y;

    // Phase 1: READY hover over the tool
    await hfoPage.evaluate(({ x, y }) => {
        // @ts-ignore
        const state = window.hfoState;
        if (!state) return;
        const nx = x / window.innerWidth;
        const ny = y / window.innerHeight;

        state.fsm.primaryHandIndex = 0;
        state.dataFabric.cursors = [
            { pointerId: 10, handIndex: 0, fsmState: 'READY', uiNormX: nx, uiNormY: ny, normX: nx, normY: ny },
        ];

        // @ts-ignore
        window.hfoTestHarness?.injectPointers?.();
    }, { x: targetX, y: targetY });

    // Phase 2: COMMIT press (should generate pointerdown immediately)
    await hfoPage.evaluate(() => {
        // @ts-ignore
        const state = window.hfoState;
        if (!state?.dataFabric?.cursors?.length) return;
        state.dataFabric.cursors[0].fsmState = 'COMMIT';
        // @ts-ignore
        window.hfoTestHarness?.injectPointers?.();
    });

    // Assert tool switches on COMMIT (pointerdown), before any release/click synthesis.
    await expect.poll(async () => {
        return await rectTool.evaluate((el) => {
            const input = el.querySelector('input') as HTMLInputElement | null;
            return !!input?.checked;
        });
    }, { timeout: 750 }).toBe(true);

    // Phase 3: Release back to READY (should generate pointerup + synthesized click)
    await hfoPage.evaluate(() => {
        // @ts-ignore
        const state = window.hfoState;
        if (!state?.dataFabric?.cursors?.length) return;
        state.dataFabric.cursors[0].fsmState = 'READY';
        // @ts-ignore
        window.hfoTestHarness?.injectPointers?.();
    });

    const log = await hfoPage.evaluate(() => {
        // @ts-ignore
        return window.__hfoV8TapLog;
    });

    expect(log.errors).toEqual([]);

    // “Not weird”: COMMIT should cause immediate press, not a delayed click-on-release only.
    expect(log.down).toBe(1);
    expect(log.up).toBe(1);

    // With legacy click synthesis enabled, Excalidraw may also receive a click on release.
    // The key requirement is that selection happens on COMMIT; release should not be required.
    const isSelectedAfterRelease = await rectTool.evaluate((el) => {
        const input = el.querySelector('input') as HTMLInputElement | null;
        return !!input?.checked;
    });

    expect(isSelectedAfterRelease).toBe(true);
});
