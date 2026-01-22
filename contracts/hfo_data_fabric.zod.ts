// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: common fabric payload shared across ports.
// NOTE: This is a portable TS contract mirror of the in-HTML runtime schemas.

import { z } from 'zod';

export const FsmStateSchema = z.enum(['IDLE', 'READY', 'COMMIT', 'COAST']);

export const FabricCursorSchema = z.object({
  handIndex: z.number().int().min(0),
  x: z.number(),
  y: z.number(),
  z: z.number().optional(),
  confidence: z.number().min(0).max(1).optional(),
  fsmState: FsmStateSchema,
  timestamp: z.number(),
});

export const DataFabricSchema = z.object({
  cursors: z.array(FabricCursorSchema),
  systemTime: z.number(),
  frameId: z.number().int(),
});

export type FsmState = z.infer<typeof FsmStateSchema>;
export type FabricCursor = z.infer<typeof FabricCursorSchema>;
export type DataFabric = z.infer<typeof DataFabricSchema>;
