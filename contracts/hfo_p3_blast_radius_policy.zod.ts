// Medallion: Bronze | Mutation: 0% | HIVE: V

import { z } from 'zod';

export const HfoP3BlastRadiusPolicySchemaV1 = z
    .object({
        schema: z.literal('hfo.p3.blast_radius_policy.v1'),
        version: z.literal('v1'),
        created_utc: z.string().min(1),
        purpose: z.string().min(1),
        required: z
            .object({
                targets_allowlist: z.literal(true),
                max_concurrency: z.literal(true),
                budget: z.literal(true),
                rollback_required: z.literal(true),
                receipts_required: z.literal(true),
            })
            .strict(),
        targets_allowlist: z.array(z.string().min(1)).min(1),
        max_concurrency: z.number().int().min(1),
        budget: z
            .object({
                unit: z.string().min(1),
                limit: z.number().int().min(1),
            })
            .strict(),
        rollback_required: z.literal(true),
        receipts_required: z.literal(true),
        notes: z.array(z.string().min(1)).optional(),
    })
    .strict();

export type HfoP3BlastRadiusPolicyContractV1 = z.infer<typeof HfoP3BlastRadiusPolicySchemaV1>;
