// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const repoRoot = process.cwd();
const mcpConfigPath = path.join(repoRoot, '.vscode', 'mcp.json');
const receiptsPath = path.join(repoRoot, 'hfo_hot_obsidian', 'bronze', '3_resources', 'receipts', 'hfo_mcp_gateway_receipts.jsonl');
const hfoConfigPath = path.join(repoRoot, 'scripts', 'hfo_config.json');

test.describe('HFO MCP Gateway Hub hardgates (red tests)', () => {
    test('MCP config includes gateway server entry', async () => {
        const raw = fs.readFileSync(mcpConfigPath, 'utf-8');
        const config = JSON.parse(raw);
        const servers = config?.servers || {};
        expect(servers['hfo_mcp_gateway_hub'], 'Missing hfo_mcp_gateway_hub server entry in .vscode/mcp.json').toBeTruthy();
    });

    test('activeVersion target exists on disk', async () => {
        const raw = fs.readFileSync(hfoConfigPath, 'utf-8');
        const cfg = JSON.parse(raw);
        const baseUrl: string = cfg.baseUrl;
        const suffix: string = cfg.suffix;
        const version: string = cfg.activeVersion;

        const relativePath = baseUrl.replace(/^https?:\/\/[^/]+\//, '') + version + suffix;
        const absolutePath = path.join(repoRoot, relativePath);

        const exists = fs.existsSync(absolutePath);
        expect(exists, `Active version file missing: ${relativePath}`).toBeTruthy();
    });

    test('gateway receipts file exists', async () => {
        const exists = fs.existsSync(receiptsPath);
        expect(exists, 'Missing gateway receipts file (hfo_mcp_gateway_receipts.jsonl)').toBeTruthy();
    });
});
