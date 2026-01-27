// @ts-nocheck
import assert from 'node:assert/strict';

import { PhaseReceiptSchema } from '../hfo_phase_receipt.zod';

describe('PhaseReceiptSchema', () => {
    it('accepts a minimal valid receipt', () => {
        const receipt = {
            type: 'phase_receipt',
            ts: '2026-01-25T20:30:00Z',
            phase_id: 'phase0_infra_bootstrap',
            role: 'p7_strategic_c2',
            objective_pointer: 'pointers:objective_current',
            sources: ['hfo_pointers.json'],
        };

        const parsed = PhaseReceiptSchema.safeParse(receipt);
        assert.equal(parsed.success, true);
        if (parsed.success === false) throw new Error(parsed.error.message);
    });

    it('rejects missing objective_pointer', () => {
        const receipt = {
            type: 'phase_receipt',
            ts: '2026-01-25T20:30:00Z',
            phase_id: 'phase0_infra_bootstrap',
            role: 'p7_strategic_c2',
            sources: ['hfo_pointers.json'],
        };

        const parsed = PhaseReceiptSchema.safeParse(receipt);
        assert.equal(parsed.success, false);
    });
});
