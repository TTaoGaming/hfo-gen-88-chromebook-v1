// Medallion: Bronze | Mutation: 0% | HIVE: V
// @ts-nocheck

import assert from 'node:assert/strict';
import fs from 'node:fs';

import { HfoLegendaryCommandersInvariantsDocV1Schema } from '../hfo_legendary_commanders_invariants.zod';

describe('HfoLegendaryCommandersInvariantsDocV1Schema', () => {
    it('parses the canonical invariants JSON and enforces uniqueness/bit-consistency', () => {
        const raw = fs.readFileSync('contracts/hfo_legendary_commanders_invariants.v1.json', 'utf-8');
        const parsed = HfoLegendaryCommandersInvariantsDocV1Schema.parse(JSON.parse(raw));

        assert.equal(parsed.schema, 'hfo.legendary_commanders.invariants.v1');
        assert.equal(parsed.version, 'v1');
        assert.equal(parsed.ports.length, 8);

        const byIndex = new Map(parsed.ports.map((p) => [p.port_index, p]));
        assert.equal(byIndex.get(2)?.commander_name, 'THE MIRROR MAGUS');
        assert.equal(byIndex.get(2)?.port_label, 'SHAPE');
        assert.equal(byIndex.get(2)?.binary, '010');

        // Guard: P2 owns SHAPE-domain formats (touch2d + W3C pointer event shapes).
        assert.ok(Array.isArray(byIndex.get(2)?.formats?.touch2d?.example_fields));
        assert.ok(Array.isArray(byIndex.get(2)?.formats?.w3c_pointer?.example_fields));
    });
});
