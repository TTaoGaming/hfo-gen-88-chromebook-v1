// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: Vendor-agnostic Kraken Keeper turn receipts.

import { z } from 'zod';

export const KrakenOutcomeSchema = z.enum(['ok', 'partial', 'error']);

export const KrakenProviderSchema = z.enum(['manual', 'openrouter']);

export const KrakenKeeperTurnReceiptSchema = z.object({
    type: z.literal('kraken_keeper_turn_receipt'),
    ts: z.string().min(10),

    scope: z.string().min(2),

    preflight_receipt_id: z.string().min(6),
    postflight_receipt_id: z.string().min(6),

    provider: KrakenProviderSchema,
    model: z.string().min(1),

    user_prompt: z.string().min(1),

    answer: z.string().min(1),

    outcome: KrakenOutcomeSchema,
    postflight_summary: z.string().min(1),

    changes: z.array(z.string()).default([]),

    sources: z.array(z.string()).min(1),

    artifacts: z
        .object({
            preflight_raw_path: z.string().min(1),
            postflight_raw_path: z.string().min(1),
            operator_preflight_markdown_path: z.string().min(1).optional(),
            operator_postflight_markdown_path: z.string().min(1).optional(),
            packet_path: z.string().min(1).optional(),
            turn_receipt_path: z.string().min(1).optional(),
            exemplar_path: z.string().min(1).optional(),
            day_snapshot_path: z.string().min(1).optional(),
        })
        .optional(),
});

export type KrakenOutcome = z.infer<typeof KrakenOutcomeSchema>;
export type KrakenProvider = z.infer<typeof KrakenProviderSchema>;
export type KrakenKeeperTurnReceipt = z.infer<typeof KrakenKeeperTurnReceiptSchema>;
