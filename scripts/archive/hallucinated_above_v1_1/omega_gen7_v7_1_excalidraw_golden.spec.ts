// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';
import fs from 'node:fs';
import path from 'node:path';

const ENTRYPOINT_URL =
    process.env.HFO_ENTRYPOINT_URL ||
    'http://localhost:8889/active_hfo_omega_entrypoint.html?flag-engine-babylon=false&flag-engine-canvas=true&flag-disable-camera=true';

const TARGET =
  "/hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/app/omega_gen7_v7_1.html";

const FIXTURES_DIR = path.resolve(
  process.cwd(),
  "hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/tests/fixtures/excalidraw",
);

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

function round(n: unknown, places = 0) {
    const x = Number(n);
    if (!Number.isFinite(x)) return null;
    const p = Math.pow(10, places);
    return Math.round(x * p) / p;
}

async function setupGen7Excalidraw(hfoPage: any) {
    await hfoPage.setViewportSize({ width: 1280, height: 720 });

    const url = withTarget(ENTRYPOINT_URL, TARGET);
    await hfoPage.goto(withFlag(withFlag(url, 'p3-target-active-app', 'true'), 'p3-injector', 'true'));
    await hfoPage.waitForURL(/omega_gen7_v7_1\.html/i, { timeout: 60000 });
    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return !!(window.hfoTokens && window.hfoRegistry);
    }, null, { timeout: 60000 });

    await hfoPage.initHFO();

    await hfoPage.evaluate(() => {
        // Ensure the loop runs in test mode (no camera required).
        // @ts-ignore
        window.hfoStartMockReplay?.();

        // Force P3 to behave like the Excalidraw adapter regardless of manifest.
        // @ts-ignore
        if (window.hfoState?.parameters) {
            // @ts-ignore
            window.hfoState.parameters.p3 = {
                ...(window.hfoState.parameters.p3 || {}),
                adapter: 'excalidraw',
                enableClickSynthesis: true,
                clickSynthesisPhase: 'down',
            };
        }

        // Ensure P3 layer is visible.
        // @ts-ignore
        const ports = window.hfoPorts;
        if (ports?.p7?.navigate?.patchParameters) {
            ports.p7.navigate.patchParameters({ ui: { heroLayers: { p3ExcalidrawVisible: true } } });
        }
        // @ts-ignore
        window.hfoHeroApplyLayers?.();
    });

    await expect(hfoPage.locator('#excalidraw-hero-iframe')).toBeVisible({ timeout: 20000 });

    const frame = hfoPage.frameLocator('#excalidraw-hero-iframe');
    const canvas = frame.locator('canvas.excalidraw__canvas');
    await expect(canvas.first()).toBeVisible({ timeout: 20000 });

    const apiReady = await frame.locator('body').evaluate(() => {
        // @ts-ignore
        return !!window.excalidrawAPI;
    });
    expect(apiReady).toBe(true);

    return { frame };
}

async function readGoldenOrUpdate(filePath: string, value: any) {
    const shouldUpdate = process.env.HFO_UPDATE_GOLDEN === '1';

    if (shouldUpdate) {
        fs.writeFileSync(filePath, JSON.stringify(value, null, 2) + '\n', 'utf-8');
        return value;
    }

    if (!fs.existsSync(filePath)) {
        throw new Error(`Missing golden file: ${filePath}. Re-run with HFO_UPDATE_GOLDEN=1 to generate.`);
    }

    const expected = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    return expected;
}

async function getExcalidrawSnapshot(frame: any) {
    return frame.locator('body').evaluate(() => {
        // @ts-ignore
        const api = window.excalidrawAPI;
        if (!api) return { ok: false, reason: 'missing_excalidraw_api' };

        const appState = api.getAppState?.() || null;
        const activeTool = appState?.activeTool?.type || null;

        const elements = (api.getSceneElements?.() || []) as any[];

        const counts: Record<string, number> = {};
        for (const el of elements) {
            const t = String(el?.type || 'unknown');
            counts[t] = (counts[t] || 0) + 1;
        }

        const last = elements.length ? elements[elements.length - 1] : null;

        const freedraw = elements.filter((e) => String(e?.type) === 'freedraw');
        const freedrawLast = freedraw.length ? freedraw[freedraw.length - 1] : null;

        const snapshot = {
            ok: true,
            activeTool,
            elementCount: elements.length,
            counts,
            lastElement: last
                ? {
                      type: String(last.type || 'unknown'),
                      x: last.x,
                      y: last.y,
                      width: last.width,
                      height: last.height,
                  }
                : null,
            freedraw: freedrawLast
                ? {
                      x: freedrawLast.x,
                      y: freedrawLast.y,
                      width: freedrawLast.width,
                      height: freedrawLast.height,
                      pointsLen: Array.isArray(freedrawLast.points) ? freedrawLast.points.length : null,
                  }
                : null,
        };

        return snapshot;
    });
}

test('Gen7 v7.1 excalidraw: golden draw (telemetry replay → freedraw element)', async ({ hfoPage }) => {
    const { frame } = await setupGen7Excalidraw(hfoPage);

    // Ensure tool is deterministic before replay.
    await frame.locator('body').evaluate(() => {
        // @ts-ignore
        const api = window.excalidrawAPI;
        if (!api) return;
        if (typeof api.setActiveTool === 'function') {
            api.setActiveTool({ type: 'freedraw' });
            return;
        }
        if (typeof api.updateScene === 'function') {
            api.updateScene({ appState: { activeTool: { type: 'freedraw' } } });
        }
    });

    const replayPath = path.join(FIXTURES_DIR, 'gen7_v7_1_draw_freedraw.telemetry.jsonl');
    const jsonlText = fs.readFileSync(replayPath, 'utf-8');

    const loaded = await hfoPage.evaluate((text) => {
        // @ts-ignore
        return window.hfoLoadReplayFromText ? window.hfoLoadReplayFromText(text) : 0;
    }, jsonlText);

    expect(loaded).toBeGreaterThan(0);

    await hfoPage.evaluate(() => {
        // @ts-ignore
        window.hfoPlayer.loop = false;
        // @ts-ignore
        window.hfoPlayer.start();
        // @ts-ignore
        window.hfoStartMockReplay?.();
    });

    await hfoPage.waitForFunction(() => {
        // @ts-ignore
        return !window.hfoPlayer?.isPlaying;
    }, null, { timeout: 20000 });

    const raw = await getExcalidrawSnapshot(frame);
    if (!raw.ok) throw new Error(`Snapshot failed: ${JSON.stringify(raw)}`);

    // Hard assertion: the replay must actually create a freedraw element.
    expect(raw.elementCount).toBeGreaterThan(0);
    expect(raw.freedraw).not.toBeNull();

    const normalized = {
        ok: true,
        activeTool: raw.activeTool,
        elementCount: raw.elementCount,
        counts: raw.counts,
        freedraw: raw.freedraw
            ? {
                  x: round(raw.freedraw.x, 0),
                  y: round(raw.freedraw.y, 0),
                  width: round(raw.freedraw.width, 0),
                  height: round(raw.freedraw.height, 0),
                  pointsLen: raw.freedraw.pointsLen,
              }
            : null,
    };

    const goldenPath = path.join(FIXTURES_DIR, 'gen7_v7_1_draw_freedraw.expected.json');
    const expected = await readGoldenOrUpdate(goldenPath, normalized);

    expect(normalized).toEqual(expected);
});

test('Gen7 v7.1 excalidraw: COMMIT_POINTER_UP can switch Rectangle tool; thumbs-up cannot', async ({ hfoPage }) => {
    const { frame } = await setupGen7Excalidraw(hfoPage);

    const rectTool = frame.locator('label[title*="Rectangle"]');
    await expect(rectTool).toBeVisible({ timeout: 20000 });

    const box = await rectTool.boundingBox();
    if (!box) throw new Error('Rectangle tool bounding box missing');

    const targetX = box.x + box.width / 2;
    const targetY = box.y + box.height / 2;

    const runClickReplay = async (gesture: 'Pointing_Up' | 'Thumb_Up') => {
        const viewBounds = await hfoPage.evaluate(() => {
            // @ts-ignore
            return window.hfoState?.ui?.viewBounds || null;
        });

        if (!viewBounds || !viewBounds.width || !viewBounds.height) {
            throw new Error(`Projected viewBounds missing (needed for uiNorm mapping): ${JSON.stringify(viewBounds)}`);
        }

        const left = (viewBounds.containerRect?.left || 0) + (viewBounds.offsetX || 0);
        const top = (viewBounds.containerRect?.top || 0) + (viewBounds.offsetY || 0);

        const nx = (targetX - left) / viewBounds.width;
        const ny = (targetY - top) / viewBounds.height;

        // Re-force adapter settings right before replay (app activation can overwrite these).
        await hfoPage.evaluate(() => {
            // @ts-ignore
            if (window.hfoState?.parameters) {
                // @ts-ignore
                window.hfoState.parameters.p3 = {
                    ...(window.hfoState.parameters.p3 || {}),
                    adapter: 'excalidraw',
                    enableClickSynthesis: true,
                    clickSynthesisPhase: 'down',
                };
            }
        });

        const makeCursor = (opts: {
            frameId: number;
            systemTime: number;
            fsmState: 'COMMIT' | 'READY' | 'IDLE' | 'COAST';
            gesture: string;
            readinessScore: number;
        }) => {
            const screenX = nx * 1280;
            const screenY = ny * 720;
            return {
                pointerId: 10,
                handIndex: 0,
                fsmState: opts.fsmState,
                uiNormX: nx,
                uiNormY: ny,
                normX: nx,
                normY: ny,
                normZ: 0,
                screenX,
                screenY,
                rawX: screenX,
                rawY: screenY,
                isPalmFacing: true,
                normalZ: 1,
                palmConeAngle: 0,
                palmNormal: { x: 0, y: 0, z: -1 },
                curls: { index: 0, middle: 0, ring: 0, pinky: 0 },
                readinessScore: opts.readinessScore,
                gesture: opts.gesture,
                confidence: 1,
            };
        };

        const frames = [
            {
                phase: 'P1_FUSE',
                data: {
                    frameId: 1,
                    systemTime: 0,
                    cursors: [
                        makeCursor({
                            frameId: 1,
                            systemTime: 0,
                            fsmState: 'READY',
                            gesture: 'None',
                            readinessScore: 0.7,
                        }),
                    ],
                },
            },
            {
                phase: 'P1_FUSE',
                data: {
                    frameId: 2,
                    systemTime: 50,
                    cursors: [
                        makeCursor({
                            frameId: 2,
                            systemTime: 50,
                            fsmState: 'COMMIT',
                            gesture,
                            readinessScore: 0.95,
                        }),
                    ],
                },
            },
            {
                phase: 'P1_FUSE',
                data: {
                    frameId: 3,
                    systemTime: 100,
                    cursors: [
                        makeCursor({
                            frameId: 3,
                            systemTime: 100,
                            fsmState: 'COMMIT',
                            gesture,
                            readinessScore: 0.95,
                        }),
                    ],
                },
            },
            {
                phase: 'P1_FUSE',
                data: {
                    frameId: 4,
                    systemTime: 150,
                    cursors: [
                        makeCursor({
                            frameId: 4,
                            systemTime: 150,
                            fsmState: 'READY',
                            gesture: 'None',
                            readinessScore: 0.7,
                        }),
                    ],
                },
            },
            {
                phase: 'P1_FUSE',
                data: {
                    frameId: 5,
                    systemTime: 200,
                    cursors: [
                        makeCursor({
                            frameId: 5,
                            systemTime: 200,
                            fsmState: 'IDLE',
                            gesture: 'None',
                            readinessScore: 0.2,
                        }),
                    ],
                },
            },
        ];

        const jsonlText = frames.map((f) => JSON.stringify(f)).join('\n') + '\n';

        const loaded = await hfoPage.evaluate((text) => {
            // @ts-ignore
            return window.hfoLoadReplayFromText ? window.hfoLoadReplayFromText(text) : 0;
        }, jsonlText);

        expect(loaded).toBeGreaterThan(0);

        await hfoPage.evaluate(() => {
            // @ts-ignore
            window.hfoPlayer.loop = false;
            // @ts-ignore
            window.hfoPlayer.start();
            // @ts-ignore
            window.hfoStartMockReplay?.();
        });

        await hfoPage.waitForFunction(() => {
            // @ts-ignore
            return !window.hfoPlayer?.isPlaying;
        }, null, { timeout: 20000 });

        // Give Excalidraw a moment to apply state changes from synthetic events.
        await hfoPage.waitForTimeout(150);
    };

    // Reset to selection tool first.
    await frame.locator('body').evaluate(() => {
        // @ts-ignore
        const api = window.excalidrawAPI;
        if (api?.setActiveTool) api.setActiveTool({ type: 'selection' });
    });

    await runClickReplay('Pointing_Up');

    const afterPointerUp = await frame.locator('body').evaluate(() => {
        // @ts-ignore
        const api = window.excalidrawAPI;
        const appState = api?.getAppState?.();
        return { activeTool: appState?.activeTool?.type || null };
    });

    // Hard assertion: COMMIT_POINTER_UP must be able to switch the tool.
    expect(afterPointerUp.activeTool).toBe('rectangle');

    // Reset again.
    await frame.locator('body').evaluate(() => {
        // @ts-ignore
        const api = window.excalidrawAPI;
        if (api?.setActiveTool) api.setActiveTool({ type: 'selection' });
    });

    await runClickReplay('Thumb_Up');

    const afterThumbUp = await frame.locator('body').evaluate(() => {
        // @ts-ignore
        const api = window.excalidrawAPI;
        const appState = api?.getAppState?.();
        return { activeTool: appState?.activeTool?.type || null };
    });

    const normalized = {
        activeToolAfterCommitPointerUp: afterPointerUp.activeTool,
        activeToolAfterThumbsUp: afterThumbUp.activeTool,
    };

    const goldenPath = path.join(FIXTURES_DIR, 'gen7_v7_1_toolbar_rectangle.expected.json');
    const expected = await readGoldenOrUpdate(goldenPath, normalized);

    expect(normalized).toEqual(expected);

    // Explicit invariant assertion: thumbs-up must NOT select Rectangle.
    expect(afterThumbUp.activeTool).not.toBe('rectangle');
});
