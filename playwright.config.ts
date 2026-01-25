// Medallion: Bronze | Mutation: 0% | HIVE: V
import 'dotenv/config';
import { defineConfig, devices } from '@playwright/test';
import fs from 'node:fs';

const baseURL = process.env.HFO_BASE_URL || 'http://localhost:8889';
const chromePath = process.env.CHROME_PATH;
const chromeChannel = process.env.PLAYWRIGHT_CHROME_CHANNEL || 'chrome';

const hasChromeChannel = (() => {
  if (chromePath) return fs.existsSync(chromePath);
  // Common Chrome install locations in Linux environments.
  return (
    fs.existsSync('/opt/google/chrome/chrome') ||
    fs.existsSync('/usr/bin/google-chrome') ||
    fs.existsSync('/usr/bin/google-chrome-stable')
  );
})();

const projectUse = {
  ...devices['Desktop Chrome'],
  ...(chromePath
    ? { launchOptions: { executablePath: chromePath } }
    : { channel: chromeChannel }),
};

export default defineConfig({
  testDir: './scripts',
  fullyParallel: true,
  reporter: 'list',
  timeout: 60_000,
  expect: { timeout: 10_000 },
  use: {
    baseURL,
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    video: 'off',
    trace: 'retain-on-failure',
  },
  projects: [
    ...(hasChromeChannel
      ? [
        {
          name: 'chrome',
          use: projectUse,
        },
      ]
      : []),
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], browserName: 'chromium' },
    },
  ],
});
