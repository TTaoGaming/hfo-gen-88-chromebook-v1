// Medallion: Bronze | Mutation: 0% | HIVE: V
// @ts-nocheck

import assert from "node:assert/strict";

import { HfoBookOfBloodGrudgesSchema } from "../hfo_book_of_blood_grudges.zod";

describe("HfoBookOfBloodGrudgesSchema", () => {
  it("accepts a minimal v1 book", () => {
    const parsed = HfoBookOfBloodGrudgesSchema.parse({
      version: "v1",
      medallion: "Gold",
      status: "RED_TRUTH",
      mutation_score: 0,
      source_markdown: ["hfo_cold_obsidian/BOOK_OF_BLOOD_GRUDGES.md"],
      entries: [
        {
          id: "BREACH_001",
          title: "THE LOBOTOMY OF COLD OBSIDIAN",
          date: "2026-01-11",
          aggressor: { agent_id: "3c272ed3df04", model: "Gemini 3 Flash" },
          session: "f40708bd5682",
          commit: "98b9fc169ecf8d9a82e8157336d86dcc7d4c8b14",
          violations: ["TYPE-1 MEDALLION FAILURE: ..."],
          anchoring: {
            breach_sha256:
              "fc4f9818a3e9d9ca308cee5795a5f6cd5d78ffe1069ff1c8ffe70bc0e28df9a7",
            forensic_report:
              "hfo_cold_obsidian/reports/FORENSIC_BEHAVIORAL_TRIAL_98B9FC1.md",
          },
          status: "CONDEMNED",
        },
      ],
      critical_signals: [
        {
          id: "CS-1",
          name: "IMMUTABLE_COLD",
          description:
            "Unauthorized writes to hfo_cold_obsidian are strictly forbidden.",
        },
      ],
    });

    assert.equal(parsed.medallion, "Gold");
    assert.equal(parsed.version, "v1");
    assert.equal(parsed.entries[0].id, "BREACH_001");
  });

  it("rejects invalid entry id", () => {
    assert.throws(() =>
      HfoBookOfBloodGrudgesSchema.parse({
        version: "v1",
        medallion: "Gold",
        status: "RED_TRUTH",
        mutation_score: 0,
        source_markdown: ["hfo_cold_obsidian/BOOK_OF_BLOOD_GRUDGES.md"],
        entries: [
          {
            id: "BREACH 001",
            title: "x",
            date: "2026-01-11",
            aggressor: { agent_id: "a" },
            violations: ["x"],
          },
        ],
        critical_signals: [{ id: "CS-1", name: "n", description: "d" }],
      }),
    );
  });
});
