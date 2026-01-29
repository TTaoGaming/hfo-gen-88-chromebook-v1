/* Medallion: Bronze | Mutation: 0% | HIVE: V */
/* Gen7 v1 CDP Smoke: attach to an existing Chrome via CDP (no local browser install/download). */

const { chromium } = require("@playwright/test");

function buildLightUrl(base, extraQuery) {
  const cb = Date.now();
  const flags =
    "flag-disable-camera=true" +
    "&flag-engine-babylon=false" +
    "&flag-engine-canvas=false" +
    "&flag-ui-golden-layout=false" +
    "&flag-ui-excalidraw=false" +
    "&flag-ui-lil-gui=false" +
    "&flag-ui-microkernel=false" +
    "&kiosk=0&hero=0&mode=dev";

  const sep = base.includes("?") ? "&" : "?";
  return `${base}${sep}__cb=${cb}&${flags}${extraQuery ? `&${extraQuery}` : ""}`;
}

async function main() {
  const cdpUrl = process.env.HFO_CDP_URL || "http://localhost:9222";
  const baseUrl = process.env.HFO_BASE_URL || "http://localhost:8889";

  const targetBase = `${baseUrl}/hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/app/omega_gen7_v1.html`;
  const url = buildLightUrl(targetBase, "test-run=cdp-smoke");

  let browser;
  try {
    browser = await chromium.connectOverCDP(cdpUrl);

    const context = browser.contexts()[0] || (await browser.newContext());
    const page = context.pages()[0] || (await context.newPage());

    await page.goto(url, { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(250);

    const ok = await page.evaluate(() => {
      const w = globalThis;
      return {
        hasSystemState: Boolean(w.systemState),
        hasHfoStateAlias: Boolean(w.hfoState),
        hasPortsEffects: Boolean(
          w.hfoPortsEffects?.emit && w.hfoPortsEffects?.getRecent,
        ),
        hasP2Tripwire: Boolean(w.hfoP2TripwireThread?.tick),
        hasP3Injector: Boolean(w.hfoP3PlanckSensorInjector?.tick),
      };
    });

    const failures = Object.entries(ok)
      .filter(([, v]) => !v)
      .map(([k]) => k);

    console.log("[gen7][cdp] url=", url);
    console.log("[gen7][cdp] ok=", ok);

    if (failures.length) {
      console.error("[gen7][cdp] FAIL missing:", failures.join(", "));
      process.exitCode = 1;
      return;
    }

    console.log("[gen7][cdp] PASS");
  } finally {
    if (browser) {
      try {
        await browser.close();
      } catch {}
    }
  }
}

main().catch((err) => {
  console.error("[gen7][cdp] ERROR", err?.stack || String(err));
  process.exit(2);
});
