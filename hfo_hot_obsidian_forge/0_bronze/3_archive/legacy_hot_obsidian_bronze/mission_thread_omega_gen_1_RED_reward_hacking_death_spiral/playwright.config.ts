// Medallion: Bronze | Mutation: 0% | HIVE: LEGACY
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
            name: 'hfo-host',
            use: {
                // Connect to the ChromeOS host if available
                connectOptions: {
                    wsEndpoint: 'ws://localhost:9222/devtools/browser'
                }
            },
        },
        {
            name: 'hfo-headless',
            use: {
                ...devices['Desktop Chrome'],
                headless: true, // Always headless in Linux to avoid X11 issues
            },
        },
    ],
});
