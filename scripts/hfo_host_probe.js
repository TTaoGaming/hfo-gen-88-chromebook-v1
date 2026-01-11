/* Medallion: Bronze | HIVE: I */
/* HFO Stability Probe: Auto-detects Chromebook Host Browser */

const { chromium } = require('playwright');

async function probe() {
  console.log('🔍 HFO: Probing for Chromebook Host Browser (localhost:9222)...');
  try {
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    console.log('✅ HFO: Successfully bridged to ChromeOS Host!');
    const contexts = browser.contexts();
    console.log(`📡 Active Contexts: ${contexts.length}`);
    await browser.close();
    process.exit(0);
  } catch (err) {
    console.error('❌ HFO: Host Bridge Failed. Is --remote-debugging-port=9222 active?');
    console.error(`Reason: ${err.message}`);
    process.exit(1);
  }
}

probe();
