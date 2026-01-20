// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import path from 'node:path';

const GEN5_URL =
    process.env.HFO_GEN5_URL ||
    'http://localhost:8889/hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/omega_gen5_v4.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true&flag-ui-excalidraw=true';

const REPLAY_PATH =
    process.env.HFO_REPLAY_PATH ||
    path.resolve(
        process.cwd(),
        'hfo_hot_obsidian/bronze/1_projects/omega_gen5_current/replay/right-hand-idle-ready-commit-move-right-release-idle.mirrored.jsonl',
    );

const MAX_MEAN_DELTA_PX = 30;

test('Gen5 excalidraw replay: pointer injection + coord alignment', async ({ hfoPage }) => {
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
    });

    await expect(hfoPage.locator('#excalidraw-iframe')).toBeVisible({ timeout: 20000 });

    const frame = hfoPage.frameLocator('#excalidraw-iframe');
    const canvas = frame.locator('canvas.interactive, canvas.excalidraw__canvas.interactive');
    await expect(canvas).toBeVisible({ timeout: 20000 });

    await hfoPage.evaluate(() => {
        // @ts-ignore
        window.__hfoPointerEvents = [];
        // @ts-ignore
        window.__hfoPointerErrors = [];
    });

    await frame.locator('body').evaluate(() => {
        // @ts-ignore
        const events = window.parent.__hfoPointerEvents;
        // @ts-ignore
        const errors = window.parent.__hfoPointerErrors;

        const canvasEl = document.querySelector('canvas.interactive, canvas.excalidraw__canvas.interactive');
        if (!canvasEl) {
            errors.push({ type: 'missing_canvas' });
            return;
        }

        const getExpected = () => {
            // @ts-ignore
            const parentState = window.parent.hfoState;
            const cursor = parentState?.dataFabric?.cursors?.[0];
            if (!cursor || !parentState?.p1) return null;
            const viewX = parentState.p1.toViewportX(cursor.uiNormX ?? cursor.normX);
            const viewY = parentState.p1.toViewportY(cursor.uiNormY ?? cursor.normY);
            const frameRect = window.frameElement?.getBoundingClientRect();
            if (!frameRect) return null;
            return { x: viewX - frameRect.left, y: viewY - frameRect.top };
        };

        ['pointerdown', 'pointermove', 'pointerup'].forEach((type) => {
            canvasEl.addEventListener(type, (e) => {
                const expected = getExpected();
                const dx = expected ? Math.abs(e.clientX - expected.x) : null;
                const dy = expected ? Math.abs(e.clientY - expected.y) : null;
                events.push({
                    type,
                    clientX: e.clientX,
                    clientY: e.clientY,
                    dx,
                    dy,
                });
            });
        });
    });

    const jsonlText = fs.readFileSync(REPLAY_PATH, 'utf-8');
    const metaLine = jsonlText.split('\n')[0];
    let replayDurationMs = 4000;
    try {
        const meta = JSON.parse(metaLine);
        if (meta?.type === 'meta' && meta.fps && meta.frame_count) {
            replayDurationMs = Math.ceil((meta.frame_count / meta.fps) * 1000);
        }
    } catch {
        // Fallback to default wait
    }
    const waitMs = Math.min(15000, replayDurationMs + 1000);
    const count = await hfoPage.evaluate((text) => {
        // @ts-ignore
        return window.hfoMockPlayer ? window.hfoMockPlayer.loadFromText(text) : 0;
    }, jsonlText);

    expect(count).toBeGreaterThan(0);

    await hfoPage.evaluate(() => {
        // @ts-ignore
        if (window.hfoMockPlayer) window.hfoMockPlayer.start();
        // @ts-ignore
        if (window.hfoStartMockReplay) window.hfoStartMockReplay();
    });

    await hfoPage.waitForTimeout(waitMs);

    const results = await hfoPage.evaluate(() => {
        // @ts-ignore
        return {
            events: window.__hfoPointerEvents || [],
            errors: window.__hfoPointerErrors || [],
        };
    });

    expect(results.errors).toEqual([]);

    const events = results.events as Array<{ type: string; dx: number | null; dy: number | null }>;
    expect(events.length).toBeGreaterThan(0);
    expect(events.some((e) => e.type === 'pointerdown')).toBe(true);
    expect(events.some((e) => e.type === 'pointerup')).toBe(true);

    const deltas = events.filter((e) => e.dx !== null && e.dy !== null);
    const meanDx = deltas.reduce((sum, e) => sum + (e.dx || 0), 0) / Math.max(1, deltas.length);
    const meanDy = deltas.reduce((sum, e) => sum + (e.dy || 0), 0) / Math.max(1, deltas.length);

    expect(meanDx).toBeLessThanOrEqual(MAX_MEAN_DELTA_PX);
    expect(meanDy).toBeLessThanOrEqual(MAX_MEAN_DELTA_PX);
});
