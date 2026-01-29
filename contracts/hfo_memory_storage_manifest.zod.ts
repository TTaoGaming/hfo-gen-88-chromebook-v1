// Medallion: Bronze | Mutation: 0% | HIVE: V
// Contract-first: unified manifest of memory/datastore surfaces for consolidation.

import { z } from "zod";

export const StoreStatusSchema = z
  .object({
    exists: z.boolean(),
    size_bytes: z.number().int().nonnegative().nullable().optional(),
    mtime_utc: z.string().optional(),
    is_dir: z.boolean().optional(),
  })
  .passthrough();

export const StoreSchema = z
  .object({
    id: z.string().min(1),
    kind: z.string().min(1),
    engine: z.string().min(1),
    path: z.string().min(1).optional(),
    authoritative: z.boolean().default(false),
    write_policy: z.string().min(1),
    status: StoreStatusSchema,
    tags: z.array(z.string()).optional(),
    notes: z.string().optional(),
  })
  .passthrough();

export const MemoryStorageManifestSchema = z
  .object({
    manifest_version: z.literal("hfo.memory_storage_manifest.v1"),
    generated_at_utc: z.string().min(1),
    repo_root: z.string().min(1),

    policy: z
      .object({
        blessed_write_path: z.string().min(1),
        shodh_mirror: z
          .object({
            mode: z.enum(["on_demand", "always_on"]).default("on_demand"),
            derived_from: z.string().min(1),
            service: z.record(z.any()).default({}),
          })
          .passthrough(),
        deprecated_write_paths: z.array(z.string()).default([]),
      })
      .passthrough(),

    stores: z.array(StoreSchema),

    discovery: z
      .object({
        jsonl: z
          .object({
            count: z.number().int().nonnegative(),
            sample_paths: z.array(z.string()).default([]),
          })
          .passthrough(),
        notes: z.string().optional(),
      })
      .passthrough(),
  })
  .passthrough();

export type MemoryStorageManifest = z.infer<typeof MemoryStorageManifestSchema>;
