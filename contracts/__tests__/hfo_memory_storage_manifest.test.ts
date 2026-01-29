// Medallion: Bronze | Mutation: 0% | HIVE: V

// @ts-nocheck

import { strict as assert } from "node:assert";
import { MemoryStorageManifestSchema } from "../hfo_memory_storage_manifest.zod";

describe("MemoryStorageManifestSchema", () => {
  it("accepts a minimal valid manifest shape", () => {
    const parsed = MemoryStorageManifestSchema.parse({
      manifest_version: "hfo.memory_storage_manifest.v1",
      generated_at_utc: "2026-01-28T00:00:00Z",
      repo_root: "/tmp/repo",
      policy: {
        blessed_write_path: "doobidoo_sqlite_vec_ssot",
        shodh_mirror: {
          mode: "on_demand",
          derived_from: "doobidoo_sqlite_vec_ssot",
          service: {},
        },
        deprecated_write_paths: [],
      },
      stores: [
        {
          id: "doobidoo_sqlite_vec_ssot",
          kind: "memory_ssot",
          engine: "sqlite_vec",
          authoritative: true,
          write_policy: "blessed_write_path",
          status: { exists: true, size_bytes: 123 },
        },
      ],
      discovery: {
        jsonl: { count: 0, sample_paths: [] },
      },
    });

    assert.equal(parsed.manifest_version, "hfo.memory_storage_manifest.v1");
    assert.equal(parsed.policy.shodh_mirror.mode, "on_demand");
  });
});
