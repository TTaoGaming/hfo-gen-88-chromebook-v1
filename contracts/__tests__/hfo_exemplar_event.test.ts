// Medallion: Bronze | Mutation: 0% | HIVE: V
// @ts-nocheck

import assert from 'node:assert/strict';

import { ExemplarEventSchema } from '../hfo_exemplar_event.zod';

describe('ExemplarEventSchema', () => {
    it('accepts a minimal exemplar event', () => {
        const parsed = ExemplarEventSchema.parse({
            type: 'hfo_exemplar_event',
            ts: '2026-01-25T00:00:00Z',
            scope: 'P6',
            preflight_receipt_id: 'abcdef123456',
            postflight_receipt_id: 'fedcba654321',
            outcome: 'ok',
            prompt_sha256: '0'.repeat(64),
            answer_sha256: '1'.repeat(64),
            artifacts: {
                exemplar_path: 'artifacts/kraken_keeper/exemplars/P6_abcdef123456_exemplar.json',
            },
        });

        assert.equal(parsed.scope, 'P6');
        assert.equal(parsed.outcome, 'ok');
        assert.equal(parsed.tags.length, 0);
        assert.equal(parsed.keywords.length, 0);
    });

    it('rejects invalid sha256', () => {
        assert.throws(() =>
            ExemplarEventSchema.parse({
                type: 'hfo_exemplar_event',
                ts: '2026-01-25T00:00:00Z',
                scope: 'P6',
                preflight_receipt_id: 'abcdef123456',
                postflight_receipt_id: 'fedcba654321',
                outcome: 'ok',
                prompt_sha256: 'not-a-hash',
                answer_sha256: '1'.repeat(64),
                artifacts: { exemplar_path: 'x' },
            })
        );
    });
});
