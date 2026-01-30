// Medallion: Bronze | Mutation: 0% | HIVE: V
// Medallion: Bronze | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import fs from 'fs';
import path from 'path';

const repoRoot = process.cwd();
const gatewayPath = path.join(repoRoot, 'hfo_mcp_gateway_hub.py');

function readGateway(): string {
    return fs.readFileSync(gatewayPath, 'utf-8');
}

test.describe('HFO MCP Gateway Hub (red tests)', () => {
    test('gateway file exists at repo root', async () => {
        const exists = fs.existsSync(gatewayPath);
        expect(exists, 'Missing hfo_mcp_gateway_hub.py at repo root').toBeTruthy();
    });

    test('gateway exposes required tool surface', async () => {
        const source = readGateway();
        expect(source.includes('observe_navigate'), 'Gateway must expose observe_navigate tool').toBeTruthy();
        expect(source.includes('bridge_assimilate'), 'Gateway must expose bridge_assimilate tool').toBeTruthy();
        expect(source.includes('shape_immunize'), 'Gateway must expose shape_immunize tool').toBeTruthy();
        expect(source.includes('deliver_disrupt'), 'Gateway must expose deliver_disrupt tool').toBeTruthy();
        expect(source.includes('query_journal'), 'Gateway must expose query_journal tool').toBeTruthy();
    });

    test('gateway enforces receipt chain', async () => {
        const source = readGateway();
        expect(source.includes('phase1_receipt'), 'Gateway must reference phase1_receipt').toBeTruthy();
        expect(source.includes('phase2_receipt'), 'Gateway must reference phase2_receipt').toBeTruthy();
        expect(source.includes('phase3_receipt'), 'Gateway must reference phase3_receipt').toBeTruthy();
        expect(source.includes('phase4_receipt'), 'Gateway must reference phase4_receipt').toBeTruthy();
        expect(source.includes('commit_receipt'), 'Gateway must reference commit_receipt').toBeTruthy();
    });

    test('gateway logs to blackboard and DuckDB', async () => {
        const source = readGateway();
        expect(source.includes('hot_obsidian_blackboard.jsonl'), 'Gateway must log to blackboard').toBeTruthy();
        expect(source.includes('duckdb'), 'Gateway must persist to DuckDB').toBeTruthy();
    });
});
