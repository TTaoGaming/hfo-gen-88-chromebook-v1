// Medallion: Bronze | Mutation: 0% | HIVE: V

import fs from "node:fs";
import path from "node:path";

import YAML from "yaml";

import { HfoBookOfBloodGrudgesSchema } from "../contracts/hfo_book_of_blood_grudges.zod";

function getArgValue(flag: string): string | undefined {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return undefined;
  return process.argv[idx + 1];
}

function requireArgValue(flag: string): string {
  const v = getArgValue(flag);
  if (!v) throw new Error(`Missing required arg ${flag} <value>`);
  return v;
}

const repoRoot = path.resolve(__dirname, "..");
const defaultYamlPath = path.join(
  repoRoot,
  "hfo_hot_obsidian_forge/2_gold/0_projects/book_of_blood_grudges/book_of_blood_grudges.gen88_v4.v1.yaml",
);

const yamlPath = getArgValue("--file") ?? defaultYamlPath;
const jsonOutPath = getArgValue("--json-out");

const raw = fs.readFileSync(yamlPath, "utf8");
const obj = YAML.parse(raw);
const parsed = HfoBookOfBloodGrudgesSchema.parse(obj);

if (jsonOutPath) {
  fs.mkdirSync(path.dirname(jsonOutPath), { recursive: true });
  fs.writeFileSync(jsonOutPath, JSON.stringify(parsed, null, 2) + "\n", "utf8");
}

// Minimal, stable output for scripting.
process.stdout.write(
  [
    "[ok] blood_grudges_yaml_valid",
    `file=${path.relative(repoRoot, yamlPath)}`,
    `entries=${parsed.entries.length}`,
    `critical_signals=${parsed.critical_signals.length}`,
  ].join(" ") + "\n",
);
