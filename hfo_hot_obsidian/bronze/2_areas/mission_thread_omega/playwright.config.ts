import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './tests',
    fullyParallel: true,
    forbidOnly: !!process.env.CI,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: 'list',
    use: {
        trace: 'on-first-retry',
    },
    webServer: {
        command: 'python3 p0_server.py',
        port: 8094,
        reuseExistingServer: !process.env.CI,
        cwd: './',
        timeout: 120000
    },
    projects: [
        {
            name: 'chromium',
            use: {
                ...devices['Desktop Chrome'],
                channel: 'chrome', // Use system Chrome to avoid heavy downloads on Chromebook
            },
        },
    ],
});
