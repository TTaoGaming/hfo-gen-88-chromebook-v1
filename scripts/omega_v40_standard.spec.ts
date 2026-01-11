// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from './hfo_fixtures';

test('V40 Standard: Pure W3C PointerEvent Validation (Red Test)', async ({ hfoPage }) => {
    const url = 'http://localhost:8080/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v40.html';
    await hfoPage.goto(url);
    await hfoPage.initHFO();
    await hfoPage.waitForHand(0);

    // Setup event spy
    await hfoPage.evaluate(() => {
        (window as any).hfoEventLog = [];
        const logEvent = (e: Event) => {
            if (!e.isTrusted) {
                (window as any).hfoEventLog.push({
                    type: e.type,
                    pointerId: (e as any).pointerId,
                    isPrimary: (e as any).isPrimary,
                    target: (e.target as any).tagName || 'UNKNOWN'
                });
            }
        };

        const attach = (win: Window) => {
            ['mousedown', 'mouseup', 'click', 'pointerdown', 'pointerup'].forEach(type => {
                win.addEventListener(type, logEvent, true);
            });
        };

        attach(window);
        // Also attach to iframes
        document.querySelectorAll('iframe').forEach(ifr => {
            try {
                if (ifr.contentWindow) attach(ifr.contentWindow);
            } catch (e) { }
        });
    });

    // Inject interaction for Hand 0
    await hfoPage.injectHand(0, {
        active: true,
        state: 'COMMITTED',
        event: 'pointerdown',
        cursors: { predictive: { x: 0.5, y: 0.5 } }
    });

    await hfoPage.injectHand(0, {
        state: 'ARMED',
        event: 'pointerup'
    });

    // Collect logs
    const logs = await hfoPage.evaluate(() => (window as any).hfoEventLog);
    console.log('Detected Events:', logs);

    // Assertions:
    // 1. Should have PointerEvents
    const pointerEvents = logs.filter((l: any) => l.type.startsWith('pointer'));
    expect(pointerEvents.length).toBeGreaterThan(0);

    // 2. Should NOT have MouseEvents (This is the "Red" part if V40 still has them)
    const mouseEvents = logs.filter((l: any) => ['mousedown', 'mouseup', 'click'].includes(l.type));

    // FAIL CONDITION: If we still have legacy dispatches
    expect(mouseEvents.length, 'Legacy MouseEvents detected! Expected Pure PointerEvents (V40 Standard).').toBe(0);
});
