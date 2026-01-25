// Medallion: Bronze | Mutation: 0% | HIVE: V
import { z } from 'zod';

export const ReplayHandSchema = z.object({
  handIndex: z.number().int().min(0).max(3),
  present: z.boolean().optional(),
  isFacingCamera: z.boolean().optional(),
  isCharging: z.boolean().optional(),
  shouldFill: z.boolean().optional(),
  hasConfidence: z.boolean().optional(),
  isPointing: z.boolean().optional(),
  categoryName: z.string().optional(),
  confidence: z.number().min(0).max(1).optional(),
});

export const ReplayStepSchema = z.object({
  ms: z.number().min(1),
  hands: z.array(ReplayHandSchema).optional(),
});

export const ReplaySequenceSchema = z.object({
  id: z.string().min(1),
  description: z.string().optional(),
  config: z
    .object({
      numHands: z.number().int().min(1).max(4).optional(),
      hysteresisHigh: z.number().min(0).max(1).optional(),
      hysteresisLow: z.number().min(0).max(1).optional(),
      chargeTimeMs: z.number().min(1).optional(),
      releaseTimeMs: z.number().min(1).optional(),
      coastDrainTimeMs: z.number().min(1).optional(),
      tensionMs: z.number().min(0).optional(),
      readyTriggerCooldownMs: z.number().min(0).optional(),
    })
    .optional(),
  expect: z
    .object({
      minNematocyst: z.number().int().min(0).optional(),
      maxNematocyst: z.number().int().min(0).optional(),
      minPostMessageOk: z.number().int().min(0).optional(),
    })
    .optional(),
  steps: z.array(ReplayStepSchema).min(1),
});

export const ReplayManifestSchema = z.object({
  version: z.string().optional(),
  sequences: z.array(ReplaySequenceSchema).min(1),
});

export type ReplayHand = z.infer<typeof ReplayHandSchema>;
export type ReplayStep = z.infer<typeof ReplayStepSchema>;
export type ReplaySequence = z.infer<typeof ReplaySequenceSchema>;
export type ReplayManifest = z.infer<typeof ReplayManifestSchema>;
