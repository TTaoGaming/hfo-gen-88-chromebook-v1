const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    page.on('request', request => {
        if (request.url().includes('piano_genie') || request.url().includes('checkpoint')) {
            console.log('GENIE_REQUEST:', request.url());
        }
    });
    console.log('Navigating to demo...');
    await page.goto('https://magenta.github.io/magenta-js/music/demos/piano_genie.html');
    await page.waitForTimeout(5000);
    await browser.close();
})();
