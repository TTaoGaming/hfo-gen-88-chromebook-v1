// @ts-nocheck
import assert from 'node:assert/strict';

import { KrakenKeeperTurnReceiptSchema } from '../hfo_kraken_keeper_turn_receipt.zod';

describe('KrakenKeeperTurnReceiptSchema', () => {
    it('accepts a minimal valid turn receipt', () => {
        const receipt = {
            type: 'kraken_keeper_turn_receipt',
            ts: '2026-01-25T21:50:00Z',
            scope: 'P6',
            preflight_receipt_id: 'abc123',
            postflight_receipt_id: 'def456',
            provider: 'manual',
            model: 'claude-or-gpt-or-grok',
            user_prompt: 'What should I do next?',
            answer: 'Run the preflight and then do X.',
            outcome: 'ok',
            postflight_summary: 'Answered next step; left audit receipts.',
            sources: ['hfo_pointers.json'],
        };

        const parsed = KrakenKeeperTurnReceiptSchema.safeParse(receipt);
        assert.equal(parsed.success, true);
        if (parsed.success === false) throw new Error(parsed.error.message);
    });

    it('rejects missing preflight_receipt_id', () => {
        const receipt = {
            type: 'kraken_keeper_turn_receipt',
            ts: '2026-01-25T21:50:00Z',
            scope: 'P6',
            postflight_receipt_id: 'def456',
            provider: 'manual',
            model: 'x',
            user_prompt: 'q',
            answer: 'a',
            outcome: 'ok',
            postflight_summary: 's',
            sources: ['hfo_pointers.json'],
        };

        const parsed = KrakenKeeperTurnReceiptSchema.safeParse(receipt);
        assert.equal(parsed.success, false);
    });
});
