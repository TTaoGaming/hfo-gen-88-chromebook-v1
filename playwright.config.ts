// Medallion: Bronze | Mutation: 0% | HIVE: V
import 'dotenv/config';
import { defineConfig, devices } from '@playwright/test';
import fs from 'node:fs';

const baseURL = process.env.HFO_BASE_URL || 'http://localhost:8889';
const chromePath = process.env.CHROME_PATH;
const chromeChannel = process.env.PLAYWRIGHT_CHROME_CHANNEL || 'chrome';
const enableBundledChromium =
  process.env.PLAYWRIGHT_ENABLE_BUNDLED_CHROMIUM === "1";

function firstExistingPath(candidates: string[]): string | undefined {
  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  return undefined;
}

const detectedSystemBrowserPath = firstExistingPath([
  "/opt/google/chrome/chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser",
]);

const hasChromeChannel = (() => {
  if (chromePath) return fs.existsSync(chromePath);
  // Common Chrome install locations in Linux environments.
  return Boolean(detectedSystemBrowserPath);
})();

const projectUse = {
  ...devices["Desktop Chrome"],
  ...(chromePath
    ? { launchOptions: { executablePath: chromePath } }
    : detectedSystemBrowserPath
      ? { launchOptions: { executablePath: detectedSystemBrowserPath } }
      : { channel: chromeChannel }),
};

export default defineConfig({
  testDir: ".",
  testMatch: [
    "scripts/**/*.spec.ts",
    "tests/**/*.spec.ts",
    "hfo_hot_obsidian_forge/1_silver/0_projects/omega_gen7_unified/tests/playwright/**/*.spec.ts",
  ],
  testIgnore: ["**/scripts/_disabled/**"],
  fullyParallel: true,
  reporter: "list",
  timeout: 60_000,
  expect: { timeout: 10_000 },
  use: {
    baseURL,
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    video: "off",
    trace: "retain-on-failure",
  },
  projects: [
    ...(hasChromeChannel
      ? [
          {
            name: "chrome",
            use: projectUse,
          },
        ]
      : []),
    ...(enableBundledChromium
      ? [
          {
            name: "chromium",
            use: { ...devices["Desktop Chrome"], browserName: "chromium" },
          },
        ]
      : []),
  ],
});

if (!hasChromeChannel && !enableBundledChromium) {
  throw new Error(
    [
      "Playwright config: no system Chrome detected and bundled Chromium is disabled.",
      "Set CHROME_PATH to a Chrome/Chromium executable, or (if acceptable) set PLAYWRIGHT_ENABLE_BUNDLED_CHROMIUM=1 and install Playwright browsers.",
      "This repo defaults to NOT downloading browsers to avoid Chromebook instability.",
    ].join(" "),
  );
}
