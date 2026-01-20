// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v4.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true&flag-ui-excalidraw=true';

test('Gen5 injector: COMMIT hold then release over Excalidraw tool', async ({ hfoPage }) => {
    await hfoPage.goto(GEN5_URL);
    await hfoPage.initHFO();

    await hfoPage.evaluate(() => {
        // @ts-ignore
        if (window.hfoState?.parameters?.excalidraw) {
            // @ts-ignore
            window.hfoState.parameters.excalidraw.enabled = true;
        }
        // @ts-ignore
        if (window.hfoState?.ui?.excalidrawOverlay) {
            // @ts-ignore
            window.hfoState.ui.excalidrawOverlay.style.display = 'block';
        }
        // Normalize viewport mapping for deterministic coords in tests
        // @ts-ignore
        if (window.hfoState?.ui?.viewBounds) {
            // @ts-ignore
            window.hfoState.ui.viewBounds = {
                width: window.innerWidth,
                height: window.innerHeight,
                offsetX: 0,
                offsetY: 0,
                containerRect: { left: 0, top: 0, width: window.innerWidth, height: window.innerHeight },
            };
        }
    });

    await expect(hfoPage.locator('#excalidraw-iframe')).toBeVisible({ timeout: 20000 });

    const frame = hfoPage.frameLocator('#excalidraw-iframe');
    const rectTool = frame.locator('label[title*="Rectangle"]');
    await expect(rectTool).toBeVisible({ timeout: 20000 });

    await hfoPage.evaluate(() => {
        // @ts-ignore
        window.__hfoInjectorLog = { down: 0, up: 0, moves: 0, mouse: 0, click: 0, errors: [] };
    });

    await frame.locator('body').evaluate(() => {
        // @ts-ignore
        const log = window.parent.__hfoInjectorLog;
        const label = document.querySelector('label[title*="Rectangle"]');
        if (!label) {
            log.errors.push('missing_rect_tool');
            return;
        }
        label.addEventListener('pointerdown', () => { log.down += 1; });
        label.addEventListener('pointerup', () => { log.up += 1; });
        label.addEventListener('pointermove', () => { log.moves += 1; });
        label.addEventListener('mousedown', () => { log.mouse += 1; });
        label.addEventListener('mouseup', () => { log.mouse += 1; });
        label.addEventListener('click', () => { log.click += 1; });
    });

    const box = await rectTool.boundingBox();
    expect(box).toBeTruthy();
    if (!box) return;

    const targetX = box.x + box.width / 2;
    const targetY = box.y + box.height / 2;

    await hfoPage.evaluate(({ x, y }) => {
        // @ts-ignore
        const state = window.hfoState;
        if (!state) return;

        const nx = x / window.innerWidth;
        const ny = y / window.innerHeight;

        state.fsm.primaryHandIndex = 0;
        state.dataFabric.cursors = [
            {
                pointerId: 10,
                handIndex: 0,
                fsmState: 'COMMIT',
                uiNormX: nx,
                uiNormY: ny,
                normX: nx,
                normY: ny,
            },
        ];

        // @ts-ignore
        if (window.hfoTestHarness?.injectPointers) window.hfoTestHarness.injectPointers();
        // Hold commit (pointermove only, no extra down)
        // @ts-ignore
        if (window.hfoTestHarness?.injectPointers) window.hfoTestHarness.injectPointers();

        state.dataFabric.cursors[0].fsmState = 'READY';
        // @ts-ignore
        if (window.hfoTestHarness?.injectPointers) window.hfoTestHarness.injectPointers();

        state.dataFabric.cursors[0].fsmState = 'IDLE';
        // @ts-ignore
        if (window.hfoTestHarness?.injectPointers) window.hfoTestHarness.injectPointers();
    }, { x: targetX, y: targetY });

    const results = await hfoPage.evaluate(() => {
        // @ts-ignore
        return window.__hfoInjectorLog;
    });

    expect(results.errors).toEqual([]);
    expect(results.down).toBe(1);
    expect(results.up).toBe(1);
    expect(results.mouse).toBe(0);
    expect(results.click).toBe(0);
});
