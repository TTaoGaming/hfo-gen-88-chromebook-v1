// Medallion: Bronze | Mutation: 0% | HIVE: P
// PORT 1: FUSE | OMEGA STATE CONTRACT (Zod 6.0 Target)

import { z } from "https://cdn.jsdelivr.net/npm/zod@3.22.4/+esm";

/**
 * P0 -> P1 Relay Schema
 * High-fidelity landmark and gesture data wrapper
 */
export const Vec2Schema = z.object({
  x: z.number().min(0).max(1),
  y: z.number().min(0).max(1)
});

export const CursorStateSchema = z.object({
  raw: Vec2Schema,
  smooth: Vec2Schema,
  snappy: Vec2Schema,
  spring: Vec2Schema,
  predictive: Vec2Schema
});

export const HandStateSchema = z.object({
  id: z.number(),
  active: z.boolean(),
  lastSeen: z.number(),
  cursors: CursorStateSchema,
  gestures: z.object({
    active: z.string(),
    score: z.number(),
    isDown: z.boolean()
  })
});

/**
 * CloudEvent Wrapper for HFO Port 1 Communication
 */
export const HfoCloudEventSchema = z.object({
  specversion: z.literal("1.0"),
  type: z.string(), // e.g. "hfo.omega.v20.hand_update"
  source: z.literal("hfo.port.0.sense"),
  id: z.string().uuid(),
  time: z.string().datetime(),
  datacontenttype: z.literal("application/json"),
  data: z.record(HandStateSchema) // Map of HandId -> HandState
});

export type HfoHandState = z.infer<typeof HandStateSchema>;
export type HfoCloudEvent = z.infer<typeof HfoCloudEventSchema>;
