// Medallion: Bronze | Mutation: 0% | HIVE: V

import { z } from "zod";

const IsoDateSchema = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);
const IsoTimestampSchema = z
  .string()
  .regex(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/);
const Sha256Schema = z.string().regex(/^[0-9a-f]{64}$/i);
const GitShaSchema = z.string().regex(/^[0-9a-f]{7,40}$/i);

export const HfoBloodGrudgeAggressorSchema = z
  .object({
    agent_id: z.string().min(1),
    model: z.string().min(1).optional(),
  })
  .strict();

export const HfoBloodGrudgeAnchoringSchema = z
  .object({
    breach_sha256: Sha256Schema,
    forensic_report: z.string().min(1).optional(),
  })
  .strict();

export const HfoBloodGrudgeEntrySchema = z
  .object({
    id: z.string().regex(/^BREACH_\d{3}$/),
    title: z.string().min(1),
    date: IsoDateSchema,
    aggressor: HfoBloodGrudgeAggressorSchema,
    session: z.string().min(1).optional(),
    commit: GitShaSchema.optional(),
    violations: z.array(z.string().min(1)).min(1),
    anchoring: HfoBloodGrudgeAnchoringSchema.optional(),
    status: z.string().min(1).optional(),
  })
  .strict();

export const HfoBloodGrudgeCriticalSignalSchema = z
  .object({
    id: z.string().regex(/^CS-\d+$/),
    name: z.string().min(1),
    description: z.string().min(1),
  })
  .strict();

export const HfoBookOfBloodGrudgesSchema = z
  .object({
    version: z.literal("v1"),
    medallion: z.literal("Gold"),
    status: z.string().min(1),
    mutation_score: z.number().min(0).max(100),
    source_markdown: z.array(z.string().min(1)).min(1),
    entries: z.array(HfoBloodGrudgeEntrySchema),
    critical_signals: z.array(HfoBloodGrudgeCriticalSignalSchema).min(1),
  })
  .strict();

export type HfoBookOfBloodGrudges = z.infer<typeof HfoBookOfBloodGrudgesSchema>;
