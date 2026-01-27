// Medallion: Bronze | Mutation: 0% | HIVE: V
// @ts-nocheck

import assert from 'node:assert/strict';

import { HfoBlackboardCloudEventSchema } from '../hfo_blackboard_cloudevent.zod';

describe('HfoBlackboardCloudEventSchema', () => {
    it('accepts a minimal cloudevent blackboard line', () => {
        const parsed = HfoBlackboardCloudEventSchema.parse({
            phase: 'CLOUDEVENT',
            specversion: '1.0',
            id: 'abc123',
            source: 'hfo://scripts/hfo_structure_validator',
            type: 'hfo.structure_validator.report',
            time: '2026-01-26T00:00:00Z',
            timestamp: '2026-01-26T00:00:00Z',
            datacontenttype: 'application/json',
            traceparent: '00-' + '0'.repeat(32) + '-' + '1'.repeat(16) + '-01',
            trace_id: '0'.repeat(32),
            span_id: '1'.repeat(16),
            parent_span_id: null,
            data: { ok: true },
        });

        assert.equal(parsed.phase, 'CLOUDEVENT');
        assert.equal(parsed.specversion, '1.0');
        assert.equal(parsed.type, 'hfo.structure_validator.report');
    });

    it('rejects invalid traceparent', () => {
        assert.throws(() =>
            HfoBlackboardCloudEventSchema.parse({
                phase: 'CLOUDEVENT',
                specversion: '1.0',
                id: 'abc123',
                source: 'hfo://scripts/hfo_structure_validator',
                type: 'hfo.structure_validator.report',
                time: '2026-01-26T00:00:00Z',
                timestamp: '2026-01-26T00:00:00Z',
                datacontenttype: 'application/json',
                traceparent: 'not-a-traceparent',
                trace_id: '0'.repeat(32),
                span_id: '1'.repeat(16),
                data: { ok: true },
            })
        );
    });
});
