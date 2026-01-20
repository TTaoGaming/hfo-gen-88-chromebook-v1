// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

const BASE_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v4_1.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true&flag-ui-excalidraw=true';

async function setupExcalidraw(hfoPage: any) {
    await hfoPage.goto(BASE_URL);
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

    const box = await rectTool.boundingBox();
    if (!box) throw new Error('Rectangle tool bounding box missing');

    return { frame, rectTool, box };
}

test('Gen5 v4.1 excalidraw: pointer-only (legacy off) does NOT select tool', async ({ hfoPage }) => {
    await hfoPage.goto(`${BASE_URL}&flag-p3-legacy-click=false`);
    await hfoPage.initHFO();

    const frame = hfoPage.frameLocator('#excalidraw-iframe');
    const rectTool = frame.locator('label[title*="Rectangle"]');
    await expect(rectTool).toBeVisible({ timeout: 20000 });

    const box = await rectTool.boundingBox();
    if (!box) throw new Error('Rectangle tool bounding box missing');

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
            { pointerId: 10, handIndex: 0, fsmState: 'COMMIT', uiNormX: nx, uiNormY: ny, normX: nx, normY: ny },
        ];
        // @ts-ignore
        if (window.hfoTestHarness?.injectPointers) window.hfoTestHarness.injectPointers();
        state.dataFabric.cursors[0].fsmState = 'READY';
        // @ts-ignore
        if (window.hfoTestHarness?.injectPointers) window.hfoTestHarness.injectPointers();
    }, { x: targetX, y: targetY });

    const isSelected = await rectTool.evaluate((el) => {
        const input = el.querySelector('input') as HTMLInputElement | null;
        return input ? input.checked : el.classList.contains('active');
    });

    expect(isSelected).toBe(false);
});

test('Gen5 v4.1 excalidraw: legacy click enabled selects tool', async ({ hfoPage }) => {
    const { rectTool, box } = await setupExcalidraw(hfoPage);

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
            { pointerId: 10, handIndex: 0, fsmState: 'COMMIT', uiNormX: nx, uiNormY: ny, normX: nx, normY: ny },
        ];
        // @ts-ignore
        if (window.hfoTestHarness?.injectPointers) window.hfoTestHarness.injectPointers();
        state.dataFabric.cursors[0].fsmState = 'READY';
        // @ts-ignore
        if (window.hfoTestHarness?.injectPointers) window.hfoTestHarness.injectPointers();
    }, { x: targetX, y: targetY });

    const isSelected = await rectTool.evaluate((el) => {
        const input = el.querySelector('input') as HTMLInputElement | null;
        return input ? input.checked : el.classList.contains('active');
    });

    expect(isSelected).toBe(true);
});
