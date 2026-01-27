// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: Exemplar events for medallion assimilation (Bronze→Silver→Gold).
// These records are intended to be created per Port 6 turn and ingested into DuckDB.

import { z } from 'zod';

export const ExemplarOutcomeSchema = z.enum(['ok', 'partial', 'error']);

export const ExemplarEventSchema = z.object({
    type: z.literal('hfo_exemplar_event'),
    ts: z.string().min(10),

    scope: z.string().min(2),

    preflight_receipt_id: z.string().min(6),
    postflight_receipt_id: z.string().min(6),

    outcome: ExemplarOutcomeSchema,

    // Content hashes are required so the exemplar can be deduplicated/verified
    prompt_sha256: z.string().regex(/^[a-f0-9]{64}$/),
    answer_sha256: z.string().regex(/^[a-f0-9]{64}$/),

    // Optional raw text (can be large/sensitive); ingestion can choose to drop or store it.
    user_prompt: z.string().min(1).optional(),
    answer: z.string().min(1).optional(),

    tags: z.array(z.string().min(1)).default([]),
    keywords: z.array(z.string().min(1)).default([]),

    sources: z.array(z.string().min(1)).default([]),

    artifacts: z
        .object({
            exemplar_path: z.string().min(1),
            packet_path: z.string().min(1).optional(),
            turn_receipt_path: z.string().min(1).optional(),
            operator_preflight_markdown_path: z.string().min(1).optional(),
            operator_postflight_markdown_path: z.string().min(1).optional(),
        })
        .optional(),
});

export type ExemplarOutcome = z.infer<typeof ExemplarOutcomeSchema>;
export type ExemplarEvent = z.infer<typeof ExemplarEventSchema>;
