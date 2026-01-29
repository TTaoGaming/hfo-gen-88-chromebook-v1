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

const sectionHeading = "Canonical event envelope (P1↔P6 spine)";
const section = sliceSection(portableBody, sectionHeading);
if (!section) {
  die(`Missing required section: '## ${sectionHeading}'`);
}

const table = parseMarkdownTable(section);
if (!table) {
  die("Failed to parse event envelope markdown table");
}

const requiredHeaders = ["Field", "Required", "Meaning"];
for (const h of requiredHeaders) {
  if (!table.headers.includes(h)) {
    die(`Event envelope table missing required column: ${h}`);
  }
}

const contractPath = path.join(WORKSPACE_ROOT, "contracts/hfo_event_envelope.v1.json");
const contract = JSON.parse(readText(contractPath));

const contractFields = Array.isArray(contract?.fields) ? contract.fields : null;
if (!contractFields || contractFields.length < 5) {
  die("contracts/hfo_event_envelope.v1.json must contain fields[]");
}

const expected = new Set(contractFields.map((f) => String(f.name)));
const actual = new Set(table.rows.map((r) => normalizeWhitespace(r.Field)));

const missing = [...expected].filter((x) => !actual.has(x));
const extra = [...actual].filter((x) => !expected.has(x));

if (missing.length || extra.length) {
  if (missing.length) {
    process.stderr.write("Missing fields in event envelope table (present in contract):\n");
    for (const f of missing) process.stderr.write(`- ${f}\n`);
  }
  if (extra.length) {
    process.stderr.write("Extra fields in event envelope table (not in contract):\n");
    for (const f of extra) process.stderr.write(`- ${f}\n`);
  }
  die(`Event envelope table drift detected in ${path.relative(WORKSPACE_ROOT, docPath)}`);
}

process.stdout.write(
  `OK: event envelope table matches SSOT (${path.relative(WORKSPACE_ROOT, docPath)})\n`,
);
