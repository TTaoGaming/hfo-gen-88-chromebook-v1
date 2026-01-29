#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

import {
  loadCompendiumManifest,
  resolveDefaultDocPath,
} from "./hive8_compendium_manifest.mjs";

const WORKSPACE_ROOT = process.cwd();

function die(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function readText(filePath) {
  if (!fs.existsSync(filePath)) {
    die(`Missing file: ${path.relative(WORKSPACE_ROOT, filePath)}`);
  }
  return fs.readFileSync(filePath, "utf8");
}

function indexOfSection(markdown, heading) {
  const needle = `\n## ${heading}\n`;
  const idx = markdown.indexOf(needle);
  if (idx >= 0) return idx;
  if (markdown.startsWith(`## ${heading}\n`)) return 0;
  return -1;
}

function sliceSection(markdown, heading) {
  const startIdx = indexOfSection(markdown, heading);
  if (startIdx < 0) return null;

  const afterStart = markdown.slice(startIdx);
  const nextHeaderIdx = afterStart.indexOf("\n## ", 4);
  if (nextHeaderIdx < 0) return afterStart;
  return afterStart.slice(0, nextHeaderIdx);
}

function parseMarkdownTable(tableText) {
  const lines = tableText
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.length > 0);

  const headerIdx = lines.findIndex((l) => l.startsWith("|") && l.endsWith("|"));
  if (headerIdx < 0) return null;

  const headerLine = lines[headerIdx];
  const sepLine = lines[headerIdx + 1];
  if (!sepLine || !/^\|\s*-/.test(sepLine)) return null;

  const headers = headerLine
    .slice(1, -1)
    .split("|")
    .map((h) => h.trim());

  const rows = [];
  for (let i = headerIdx + 2; i < lines.length; i += 1) {
    const line = lines[i];
    if (!line.startsWith("|") || !line.endsWith("|")) break;

    const cols = line
      .slice(1, -1)
      .split("|")
      .map((c) => c.trim());

    if (cols.length !== headers.length) {
      die(`Invalid markdown table row column count (expected ${headers.length}, got ${cols.length}): ${line}`);
    }

    const obj = {};
    for (let j = 0; j < headers.length; j += 1) obj[headers[j]] = cols[j];
    rows.push(obj);
  }

  return { headers, rows };
}

function normalizeWhitespace(s) {
  return String(s).replace(/\s+/g, " ").trim();
}

const docPath = (() => {
  if (process.argv[2]) {
    return path.isAbsolute(process.argv[2])
      ? process.argv[2]
      : path.join(WORKSPACE_ROOT, process.argv[2]);
  }

  const manifest = loadCompendiumManifest();
  const familyId = manifest?.defaults?.canonical_family_id;
  if (!familyId) {
    die("manifest.defaults.canonical_family_id missing");
  }
  const resolved = resolveDefaultDocPath({ manifest, familyId });
  return resolved.absolutePath;
})();

const markdown = readText(docPath);
const extraIdx = indexOfSection(markdown, "Extra References (non-portable)");
const portableBody = extraIdx >= 0 ? markdown.slice(0, extraIdx) : markdown;

const sectionHeading = "P3 bounded cascade policy (blast radius, enforceable)";
const section = sliceSection(portableBody, sectionHeading);
if (!section) {
  die(`Missing required section: '## ${sectionHeading}'`);
}

const table = parseMarkdownTable(section);
if (!table) {
  die("Failed to parse P3 blast radius policy markdown table");
}

const requiredHeaders = ["Control", "Required", "Meaning"];
for (const h of requiredHeaders) {
  if (!table.headers.includes(h)) {
    die(`P3 blast radius table missing required column: ${h}`);
  }
}

const contractPath = path.join(
  WORKSPACE_ROOT,
  "contracts/hfo_p3_blast_radius_policy.v1.json",
);
const contract = JSON.parse(readText(contractPath));

if (contract?.schema !== "hfo.p3.blast_radius_policy.v1") {
  die(`Blast radius policy schema mismatch (found ${String(contract?.schema)})`);
}

const required = contract?.required;
if (!required || typeof required !== "object") {
  die("Blast radius policy missing required object: required");
}

const mustHave = [
  "targets_allowlist",
  "max_concurrency",
  "budget",
  "rollback_required",
  "receipts_required",
];
for (const k of mustHave) {
  if (required[k] !== true) {
    die(`Blast radius policy required.${k} must be true`);
  }
}

if (!Array.isArray(contract?.targets_allowlist) || contract.targets_allowlist.length < 1) {
  die("Blast radius policy targets_allowlist must be a non-empty array");
}

if (!Number.isInteger(contract?.max_concurrency) || contract.max_concurrency < 1) {
  die("Blast radius policy max_concurrency must be an integer >= 1");
}

if (!contract?.budget || typeof contract.budget !== "object") {
  die("Blast radius policy missing budget object");
}

if (!Number.isInteger(contract.budget.limit) || contract.budget.limit < 1) {
  die("Blast radius policy budget.limit must be an integer >= 1");
}

if (contract.rollback_required !== true) {
  die("Blast radius policy rollback_required must be true");
}

if (contract.receipts_required !== true) {
  die("Blast radius policy receipts_required must be true");
}

const expectedControls = new Set(mustHave);
const actualControls = new Set(table.rows.map((r) => normalizeWhitespace(r.Control)));

const missing = [...expectedControls].filter((x) => !actualControls.has(x));
const extra = [...actualControls].filter((x) => !expectedControls.has(x));

if (missing.length || extra.length) {
  if (missing.length) {
    process.stderr.write("Missing controls in P3 blast radius table (required by policy):\n");
    for (const c of missing) process.stderr.write(`- ${c}\n`);
  }
  if (extra.length) {
    process.stderr.write("Extra controls in P3 blast radius table (not required by policy):\n");
    for (const c of extra) process.stderr.write(`- ${c}\n`);
  }
  die(`Blast radius policy drift detected in ${path.relative(WORKSPACE_ROOT, docPath)}`);
}

process.stdout.write(
  `OK: P3 blast radius policy matches SSOT (${path.relative(WORKSPACE_ROOT, docPath)})\n`,
);
