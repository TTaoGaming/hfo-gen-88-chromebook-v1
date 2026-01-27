// @ts-nocheck
import assert from 'node:assert/strict';

import { FlightReceiptSchema } from '../hfo_flight_receipt.zod';

describe('FlightReceiptSchema', () => {
    it('accepts a minimal valid preflight receipt', () => {
        const receipt = {
            type: 'flight_receipt',
            ts: '2026-01-25T20:40:00Z',
            run_id: 'run_001',
            flight_phase: 'preflight',
            scope: { level: 'hub' },
            objective_pointer: 'pointers:objective_current',
            sources: ['hfo_pointers.json'],
        };

        const parsed = FlightReceiptSchema.safeParse(receipt);
        assert.equal(parsed.success, true);
    });

    it('rejects missing run_id', () => {
        const receipt = {
            type: 'flight_receipt',
            ts: '2026-01-25T20:40:00Z',
            flight_phase: 'preflight',
            scope: { level: 'hub' },
            objective_pointer: 'pointers:objective_current',
            sources: ['hfo_pointers.json'],
        };

        const parsed = FlightReceiptSchema.safeParse(receipt);
        assert.equal(parsed.success, false);
    });

    it('rejects missing objective_pointer', () => {
        const receipt = {
            type: 'flight_receipt',
            ts: '2026-01-25T20:40:00Z',
            run_id: 'run_001',
            flight_phase: 'postflight',
            scope: { level: 'port', port: 'p7' },
            status: 'PASS',
            sources: ['hfo_pointers.json'],
        };

        const parsed = FlightReceiptSchema.safeParse(receipt);
        assert.equal(parsed.success, false);
    });
});
