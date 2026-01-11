// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test as base, Page, expect } from '@playwright/test';
import config from './hfo_config.json';

export interface HFOPage extends Page {
    initHFO(): Promise<void>;
    injectHand(id: number, props: any): Promise<void>;
    getHandState(id: number): Promise<any>;
    waitForHand(id: number): Promise<void>;
}

export const getActiveUrl = (version?: string) => {
    const v = version || config.activeVersion;
    return `${config.baseUrl}${v}${config.suffix}`;
};

export const test = base.extend<{ hfoPage: HFOPage }>({
    hfoPage: async ({ page }, use) => {
        const hfoPage = page as HFOPage;

        hfoPage.initHFO = async () => {
            // Unlock Hero Button if present
            const heroBtn = page.locator('#hero-button');
            if (await heroBtn.isVisible()) {
                await heroBtn.click();
                await expect(heroBtn).not.toBeVisible();
            }

            await page.evaluate(() => {
                // @ts-ignore
                if (window.initPhysics) window.initPhysics();
            });
        };

        hfoPage.waitForHand = async (id: number) => {
            await page.waitForFunction((handId) => {
                // @ts-ignore
                return window.hfoState && window.hfoState.hands && window.hfoState.hands[handId];
            }, id, { timeout: 10000 });
        };

        hfoPage.injectHand = async (id, props) => {
            await page.evaluate(({ handId, handProps }) => {
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
            return await page.evaluate((handId) => {
                // @ts-ignore
                const hand = window.hfoState.hands[handId];
                return hand ? { state: hand.fsm.state, active: hand.active, event: hand.fsm.pointerEvent } : null;
            }, id);
        };

        await use(hfoPage);
    },
});

export { expect } from '@playwright/test';
