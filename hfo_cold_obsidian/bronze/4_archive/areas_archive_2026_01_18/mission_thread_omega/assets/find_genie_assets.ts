import { chromium } from 'playwright';

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    page.on('request', request => {
        if (request.url().includes('piano_genie')) {
            console.log('GENIE_REQUEST:', request.url());
        }
    });
    await page.goto('https://magenta.github.io/magenta-js/music/demos/piano_genie.html');
    await page.waitForTimeout(5000);
    await browser.close();
})();
