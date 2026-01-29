// Medallion: Bronze | Mutation: 0% | HIVE: V

import { z } from 'zod';

export const HfoEventEnvelopeSchemaV1 = z
    .object({
        schema: z.literal('hfo.event.envelope.v1'),
        version: z.literal('v1'),
        created_utc: z.string().min(1),
        purpose: z.string().min(1),
        invariants: z.array(z.string().min(1)).min(1),
        fields: z
            .array(
                z
                    .object({
                        name: z.string().min(1),
                        required: z.boolean(),
                        type: z.string().min(1),
                        description: z.string().min(1),
                        shape: z.record(z.string(), z.string()).optional(),
                    })
                    .strict(),
            )
            .min(1),
    })
    .strict();

export type HfoEventEnvelopeContractV1 = z.infer<typeof HfoEventEnvelopeSchemaV1>;
