// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: Preflight/Postflight receipts for hub/ports/subshards/tools.

import { z } from 'zod';

export const FlightPhaseSchema = z.enum(['preflight', 'postflight']);

export const FlightScopeLevelSchema = z.enum(['hub', 'port', 'subshard', 'tool']);

export const PortIdSchema = z.enum(['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']);

export const FlightScopeSchema = z.object({
    level: FlightScopeLevelSchema,
    port: PortIdSchema.optional(),
    shard_id: z.string().min(1).optional(),
    tool_id: z.string().min(1).optional(),
});

export const FlightReceiptSchema = z.object({
    type: z.literal('flight_receipt'),
    ts: z.string().min(10),

    run_id: z.string().min(6),
    flight_phase: FlightPhaseSchema,

    scope: FlightScopeSchema,

    objective_pointer: z.string().min(1),

    capsule_refs: z.array(z.string()).default([]),
    spec_refs: z.array(z.string()).default([]),
    contract_refs: z.array(z.string()).default([]),

    checks: z.array(z.string()).default([]),
    results: z.array(z.string()).default([]),

    status: z.enum(['PASS', 'FAIL']).optional(),
    errors: z.array(z.string()).default([]),
    duration_ms: z.number().int().min(0).optional(),

    sources: z.array(z.string()).min(1),
});

export type FlightPhase = z.infer<typeof FlightPhaseSchema>;
export type FlightScopeLevel = z.infer<typeof FlightScopeLevelSchema>;
export type PortId = z.infer<typeof PortIdSchema>;
export type FlightScope = z.infer<typeof FlightScopeSchema>;
export type FlightReceipt = z.infer<typeof FlightReceiptSchema>;
