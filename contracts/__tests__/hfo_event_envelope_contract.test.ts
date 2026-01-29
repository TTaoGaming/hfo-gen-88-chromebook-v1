// Medallion: Bronze | Mutation: 0% | HIVE: V
// @ts-nocheck

import assert from 'node:assert/strict';
import fs from 'node:fs';

import { HfoEventEnvelopeSchemaV1 } from '../hfo_event_envelope.zod';

describe('HfoEventEnvelopeSchemaV1', () => {
    it('parses the canonical event envelope contract JSON', () => {
        const raw = fs.readFileSync('contracts/hfo_event_envelope.v1.json', 'utf8');
        const parsed = HfoEventEnvelopeSchemaV1.parse(JSON.parse(raw));

        assert.equal(parsed.schema, 'hfo.event.envelope.v1');
        assert.equal(parsed.version, 'v1');
        assert.ok(parsed.fields.length >= 7);

        const fieldNames = new Set(parsed.fields.map((f) => f.name));
        assert.ok(fieldNames.has('event_id'));
        assert.ok(fieldNames.has('trace'));
        assert.ok(fieldNames.has('provenance'));
        assert.ok(fieldNames.has('budget'));
        assert.ok(fieldNames.has('payload'));
    });
});
