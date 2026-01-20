// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test as base, Page, expect, chromium } from '@playwright/test';
import config from './hfo_config.json';

export interface HFOPage extends Page {
    initHFO(): Promise<void>;
    injectHand(id: number, props: any): Promise<void>;
    getHandState(id: number): Promise<any>;
    waitForHand(id: number): Promise<void>;
}

export const getActiveUrl = (version?: string) => {
    const v = version || process.env.HFO_ACTIVE_VERSION || config.activeVersion;
    const base = process.env.HFO_BASE_URL || config.baseUrl;
    return `${base}${v}${config.suffix}`;
};

export const test = base.extend<{ hfoPage: HFOPage }>({
    hfoPage: async ({ page }, use) => {
        const cdpUrl = process.env.HFO_CDP_URL;
        let activePage = page as HFOPage;
        let browser: Awaited<ReturnType<typeof chromium.connectOverCDP>> | null = null;
        let context: ReturnType<typeof activePage.context> | null = null;

        if (cdpUrl) {
            browser = await chromium.connectOverCDP(cdpUrl);
            context = browser.contexts()[0] || await browser.newContext();
            activePage = (context.pages()[0] || await context.newPage()) as HFOPage;
        }

        const hfoPage = activePage as HFOPage;

        activePage.on('console', (msg) => {
            if (msg.type() === 'error' || msg.type() === 'warning') {
                console.log(`[browser:${msg.type()}] ${msg.text()}`);
            }
        });

        activePage.on('pageerror', (err) => {
            console.log(`[browser:pageerror] ${err.message}`);
        });

        hfoPage.initHFO = async () => {
            // Support both old and new (Gen 4) buttons
            const heroBtn = activePage.locator('#hero-button, #btn-ignite');
            if (await heroBtn.isVisible()) {
                await heroBtn.click();
                await expect(heroBtn).not.toBeVisible();
            }

            await activePage.evaluate(() => {
                // @ts-ignore
                if (window.initPhysics) window.initPhysics();
            });
        };

        hfoPage.waitForHand = async (id: number) => {
            await activePage.waitForFunction((handId) => {
                // @ts-ignore
                return window.hfoState && window.hfoState.hands && window.hfoState.hands[handId];
            }, id, { timeout: 10000 });
        };

        hfoPage.injectHand = async (id, props) => {
            await activePage.evaluate(({ handId, handProps }) => {
                // @ts-ignore
                const hand = window.hfoState.hands[handId];
                if (!hand) return;

                if (handProps.cursors) {
                    for (const key in handProps.cursors) {
                        Object.assign(hand.cursors[key], handProps.cursors[key]);
                    }
                    delete handProps.cursors;
                }

                Object.assign(hand, handProps);
                if (handProps.state) hand.fsm.state = handProps.state;
                if (handProps.event) hand.fsm.pointerEvent = handProps.event;

                // @ts-ignore
                if (window.port3Inject) window.port3Inject(hand);
            }, { handId: id, handProps: props });
        };

        hfoPage.getHandState = async (id) => {
            return await activePage.evaluate((handId) => {
                // @ts-ignore
                const hand = window.hfoState.hands[handId];
                return hand ? { state: hand.fsm.state, active: hand.active, event: hand.fsm.pointerEvent } : null;
            }, id);
        };

        await use(hfoPage);

        if (browser && context) {
            try { await activePage.close(); } catch {}
            try { await context.close(); } catch {}
            try { await browser.close(); } catch {}
        }
    },
});

export { expect } from '@playwright/test';
