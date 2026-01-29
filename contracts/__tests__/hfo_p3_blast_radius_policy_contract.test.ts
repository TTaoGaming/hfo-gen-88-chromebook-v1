// Medallion: Bronze | Mutation: 0% | HIVE: V
// @ts-nocheck

import assert from 'node:assert/strict';
import fs from 'node:fs';

import { HfoP3BlastRadiusPolicySchemaV1 } from '../hfo_p3_blast_radius_policy.zod';

describe('HfoP3BlastRadiusPolicySchemaV1', () => {
    it('parses the canonical P3 blast radius policy contract JSON', () => {
        const raw = fs.readFileSync('contracts/hfo_p3_blast_radius_policy.v1.json', 'utf8');
        const parsed = HfoP3BlastRadiusPolicySchemaV1.parse(JSON.parse(raw));

        assert.equal(parsed.schema, 'hfo.p3.blast_radius_policy.v1');
        assert.equal(parsed.version, 'v1');
        assert.ok(parsed.targets_allowlist.length >= 1);
        assert.ok(parsed.max_concurrency >= 1);
        assert.ok(parsed.budget.limit >= 1);
        assert.equal(parsed.rollback_required, true);
        assert.equal(parsed.receipts_required, true);
    });
});
