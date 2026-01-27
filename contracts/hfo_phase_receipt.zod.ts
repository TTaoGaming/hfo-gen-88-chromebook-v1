// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: Phase receipts (TDD/BDD/CDD) + drift firewall breadcrumbs.

import { z } from 'zod';

export const HfoPhaseIdSchema = z.enum([
    'phase0_infra_bootstrap',
    'phase1_alpha_generation_bootstrap',
    'phase2_capsule_compiler',
    'phase3_drift_firewall',
    'phase4_memory_delegation',
]);

export const HfoRoleSchema = z.enum(['p7_strategic_c2', 'p1_tactical_c2', 'port6_kraken_keeper', 'other']);

export const PhaseReceiptSchema = z.object({
    type: z.literal('phase_receipt'),
    ts: z.string().min(10),

    phase_id: HfoPhaseIdSchema,
    role: HfoRoleSchema,

    objective_pointer: z.string().min(1),

    spec_refs: z.array(z.string()).default([]),
    contract_refs: z.array(z.string()).default([]),

    tdd_red_tests: z.array(z.string()).default([]),
    bdd_scenarios: z.array(z.string()).default([]),
    cdd_checks: z.array(z.string()).default([]),

    decisions_locked: z.array(z.string()).default([]),
    uncertainties: z.array(z.string()).default([]),

    sources: z.array(z.string()).min(1),
});

export type HfoPhaseId = z.infer<typeof HfoPhaseIdSchema>;
export type HfoRole = z.infer<typeof HfoRoleSchema>;
export type PhaseReceipt = z.infer<typeof PhaseReceiptSchema>;
