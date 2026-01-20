// Medallion: Bronze | Mutation: 0% | HIVE: V
import 'dotenv/config';
import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.HFO_BASE_URL || 'http://localhost:8889';
const chromePath = process.env.CHROME_PATH;
const chromeChannel = process.env.PLAYWRIGHT_CHROME_CHANNEL || 'chrome';

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
    {
      name: 'chrome',
      use: projectUse,
    },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], browserName: 'chromium' },
    },
  ],
});