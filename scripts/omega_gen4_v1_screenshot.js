/* Medallion: Bronze | HIVE: V */
const { chromium } = require('playwright');
const path = require('path');
const config = require('./hfo_config.json');

async function capture() {
    console.log(`📸 HFO: Initiating Omega Gen 4 V1 Capture...`);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = path.join(__dirname, `../reports/omega_gen4_v1_${timestamp}.png`);
    const url = `${config.baseUrl}${config.activeVersion}${config.suffix}`;

    let browser;
    try {
        browser = await chromium.launch({ headless: true });
        const page = await browser.newPage();

        // Log console messages
        page.on('console', msg => {
            console.log(`BROWSER [${msg.type()}]: ${msg.text()}`);
        });

        page.on('pageerror', err => {
            console.error(`BROWSER ERROR: ${err.message}`);
        });

        console.log(`Navigating to: ${url}`);
        await page.goto(url);

        // Wait for layout
        await page.waitForSelector('#btn-start-p0', { timeout: 10000 });

        // Click Initialize
        console.log("Clicking Initialize...");
        await page.click('#btn-start-p0');

        // Wait for MediaPipe (checking logs)
        console.log("Waiting for MediaPipe Initialization...");
        await page.waitForFunction(() => {
            const logs = document.getElementById('mission-logs-content');
            return logs && logs.innerText.includes('✅ P0: MediaPipe Shard Online');
        }, { timeout: 20000 });

        // Wait for some frames
        await page.waitForTimeout(5000);

        await page.screenshot({ path: filename, fullPage: true });
        console.log(`✅ HFO: Screenshot saved to: ${filename}`);
    } catch (err) {
        console.error(`❌ HFO: Capture Failed: ${err.message}`);
    } finally {
        if (browser) await browser.close();
    }
}

capture();
