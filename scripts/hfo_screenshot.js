/* Medallion: Bronze | HIVE: V */
/* HFO Dual-Sighted Screenshot utility */

const { chromium } = require('playwright');
const path = require('path');

async function capture(mode = 'headless') {
  console.log(`📸 HFO: Initiating [${mode.toUpperCase()}] Capture...`);
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = path.join(__dirname, `../reports/screenshot_${mode}_${timestamp}.png`);

  let browser;
  try {
    if (mode === 'host') {
      // Connect to existing ChromeOS Host
      browser = await chromium.connectOverCDP('http://localhost:9222');
      const pages = await browser.contexts()[0].pages();
      const page = pages[0] || await browser.newPage();
      await page.goto('http://localhost:8888/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/piano_genie_official/index.html');
      await page.screenshot({ path: filename, fullPage: true });
    } else {
      // Launch headless internal Chromium
      browser = await chromium.launch({ headless: true });
      const page = await browser.newPage();
      await page.goto('http://localhost:8888/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/piano_genie_official/index.html');
      // Wait for Piano Genie to settle
      await page.waitForTimeout(5000);
      await page.screenshot({ path: filename, fullPage: true });
    }
    console.log(`✅ HFO: Screenshot saved to: ${filename}`);
  } catch (err) {
    console.error(`❌ HFO: Capture Failed [${mode}]: ${err.message}`);
  } finally {
    if (browser) await browser.close();
  }
}

const targetMode = process.argv[2] || 'headless';
capture(targetMode);
