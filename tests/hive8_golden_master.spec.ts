import { test, expect } from "@playwright/test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { execFileSync } from "node:child_process";

function runPython(
  args: string[],
  cwd: string,
): { stdout: string; stderr: string } {
  const res = execFileSync("python3", args, {
    cwd,
    stdio: ["ignore", "pipe", "pipe"],
    encoding: "utf-8",
  });
  // execFileSync returns stdout; stderr captured only on throw. We keep a uniform shape.
  return { stdout: res, stderr: "" };
}

function runPythonAllowFail(
  args: string[],
  cwd: string,
): { code: number; stdout: string; stderr: string } {
  try {
    const stdout = execFileSync("python3", args, {
      cwd,
      stdio: ["ignore", "pipe", "pipe"],
      encoding: "utf-8",
    });
    return { code: 0, stdout, stderr: "" };
  } catch (e: any) {
    return {
      code: typeof e?.status === "number" ? e.status : 1,
      stdout: e?.stdout?.toString?.() ?? "",
      stderr: e?.stderr?.toString?.() ?? "",
    };
  }
}

test("HIVE8 golden master: strict format + known-answer tables", async () => {
  const repoRoot = process.cwd();
  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), "hive8-gm-"));
  const outRoot = path.join(tmpRoot, "turns");
  const blackboard = path.join(tmpRoot, "blackboard.jsonl");

  const turnId = "20260127T000000Z__gm_jadc2_known_answers";
  const createdUtc = "2026-01-27T00:00:00Z";
  const finalizedUtc = "2026-01-27T00:01:00Z";

  const mtgMapPath = path.join(
    repoRoot,
    "contracts",
    "hfo_mtg_port_card_mappings.v2.json",
  );
  const mtgMap = JSON.parse(fs.readFileSync(mtgMapPath, "utf-8"));
  const p0 = mtgMap?.ports?.P0 ?? {};
  const p0Slivers = Array.isArray(p0?.slivers) ? p0.slivers : [];
  const p0SlotToCard = new Map<string, string>();
  for (const s of p0Slivers) {
    const slot = String(s?.slot ?? "")
      .trim()
      .toLowerCase();
    const card = String(s?.card ?? "").trim();
    if (slot && card) p0SlotToCard.set(slot, card);
  }
  const p0SliverStatic = String(p0SlotToCard.get("static") ?? "").trim();
  const p0SliverTrigger = String(p0SlotToCard.get("trigger") ?? "").trim();
  const p0SliverActivated = String(p0SlotToCard.get("activated") ?? "").trim();
  const p0Equipment = String(p0?.equipment?.card ?? "").trim();

  const gen = runPython(
    [
      "scripts/hfo_make_hive8_turn_artifacts.py",
      "--slug",
      "gm_jadc2_known_answers",
      "--prompt",
      "what is the jadc2 mapping? (golden)",
      "--mission-thread",
      "omega",
      "--strict",
      "--out-root",
      outRoot,
      "--blackboard",
      blackboard,
      "--no-stigmergy",
      "--turn-id",
      turnId,
      "--created-utc",
      createdUtc,
    ],
    repoRoot,
  );

  const envelopeDir = gen.stdout.trim();
  const manifestPath = path.join(envelopeDir, "turn_manifest.json");
  const metaPath = path.join(envelopeDir, "HIVE8__meta_synthesis.md");

  const fin = runPythonAllowFail(
    [
      "scripts/hfo_hive8_finalize_turn.py",
      "--manifest",
      manifestPath,
      "--blackboard",
      blackboard,
      "--no-stigmergy",
      "--finalized-utc",
      finalizedUtc,
    ],
    repoRoot,
  );
  expect(fin.code).toBe(0);

  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf-8"));
  expect(manifest.turn_id).toBe(turnId);
  expect(manifest.finalize.strict).toBe(true);
  expect(manifest.finalize.cardinality_validation_passed).toBe(true);
  expect(Array.isArray(manifest.finalize.cardinality_errors)).toBe(true);
  expect(manifest.finalize.cardinality_errors.length).toBe(0);

  const meta = fs.readFileSync(metaPath, "utf-8");

  // Known-answer: OBSIDIAN ↔ JADC2 mapping is deterministic.
  expect(meta).toContain("### OBSIDIAN Powerwords (Ports ↔ JADC2 Domains)");
  expect(meta).toContain("| O | P0 | OBSERVE | ISR |");
  expect(meta).toContain("| B | P1 | BRIDGE | Data Fabric |");

  // Known-answer: MTG mapping is deterministic from contracts/hfo_mtg_port_card_mappings.v2.json.
  expect(meta).toContain("### 3×Sliver + 1×Equipment Mapping (per Port)");
  if (p0SliverStatic) expect(meta).toContain(p0SliverStatic);
  if (p0SliverTrigger) expect(meta).toContain(p0SliverTrigger);
  if (p0SliverActivated) expect(meta).toContain(p0SliverActivated);
  if (p0Equipment) expect(meta).toContain(p0Equipment);

  // No-theater: strict schema summary exists in manifest.
  expect(manifest.finalize.ports.P0.expected_meta_promoted_count).toBe(2);
  expect(manifest.finalize.ports.P4.expected_meta_promoted_count).toBe(1);

  // New requirement: stage flow + final debate sections exist.
  expect(meta).toContain("## Stage Flow (4 stages, paired ports) (auto)");
  expect(meta).toContain("## Final Debate + Map-Elites Matrix (auto)");
});

test("HIVE8 golden master: strict validator fails closed + no stigmergy on failure", async () => {
  const repoRoot = process.cwd();
  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), "hive8-gm-fail-"));
  const outRoot = path.join(tmpRoot, "turns");
  const blackboard = path.join(tmpRoot, "blackboard.jsonl");

  const turnId = "20260127T000000Z__gm_strict_failure";
  const createdUtc = "2026-01-27T00:00:00Z";
  const finalizedUtc = "2026-01-27T00:01:00Z";

  const gen = runPython(
    [
      "scripts/hfo_make_hive8_turn_artifacts.py",
      "--slug",
      "gm_strict_failure",
      "--prompt",
      "golden: induce failure",
      "--mission-thread",
      "omega",
      "--strict",
      "--out-root",
      outRoot,
      "--blackboard",
      blackboard,
      "--no-stigmergy",
      "--turn-id",
      turnId,
      "--created-utc",
      createdUtc,
    ],
    repoRoot,
  );

  const envelopeDir = gen.stdout.trim();
  const manifestPath = path.join(envelopeDir, "turn_manifest.json");
  const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf-8"));
  const p0Path: string = String(manifest?.artifacts?.P0 ?? "");
  expect(p0Path).not.toBe("");

  // Break P0 meta-promoted count: remove one promoted bullet.
  let p0 = fs.readFileSync(p0Path, "utf-8");
  p0 = p0.replace(
    /<!-- HIVE8_META_PROMOTED_START -->[\s\S]*?<!-- HIVE8_META_PROMOTED_END -->/m,
    (block) => {
      return block.replace(/- 2[\s\S]*?\n/, "").replace(/\n\n+/g, "\n\n");
    },
  );
  fs.writeFileSync(p0Path, p0, "utf-8");

  const fin = runPythonAllowFail(
    [
      "scripts/hfo_hive8_finalize_turn.py",
      "--manifest",
      manifestPath,
      "--blackboard",
      blackboard,
      "--finalized-utc",
      finalizedUtc,
      // NOTE: do NOT pass --no-stigmergy; we want to prove it doesn't emit on failure.
    ],
    repoRoot,
  );
  expect(fin.code).toBe(2);

  const manifest2 = JSON.parse(fs.readFileSync(manifestPath, "utf-8"));
  expect(manifest2.finalize.strict).toBe(true);
  expect(manifest2.finalize.cardinality_validation_passed).toBe(false);

  const errors: Array<{ port: string; check: string }> =
    manifest2.finalize.cardinality_errors;
  expect(
    errors.some((e) => e.port === "P0" && e.check === "meta_promoted_count"),
  ).toBe(true);

  // Ensure no stigmergy was emitted on failure.
  const exists = fs.existsSync(blackboard);
  if (exists) {
    const size = fs.statSync(blackboard).size;
    expect(size).toBe(0);
  }
});
