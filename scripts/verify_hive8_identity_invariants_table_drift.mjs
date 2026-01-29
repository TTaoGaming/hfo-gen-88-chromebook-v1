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

  const headerIdx = lines.findIndex(
    (l) => l.startsWith("|") && l.endsWith("|"),
  );
  if (headerIdx < 0) {
    return null;
  }

  const headerLine = lines[headerIdx];
  const sepLine = lines[headerIdx + 1];
  if (!sepLine || !/^\|\s*-/.test(sepLine)) {
    return null;
  }

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
      die(
        `Invalid markdown table row column count (expected ${headers.length}, got ${cols.length}): ${line}`,
      );
    }
    const obj = {};
    for (let j = 0; j < headers.length; j += 1) {
      obj[headers[j]] = cols[j];
    }
    rows.push(obj);
  }

  return { headers, rows };
}

function normalizeWhitespace(s) {
  return String(s).replace(/\s+/g, " ").trim();
}

function parseTrigramCell(cell) {
  const normalized = normalizeWhitespace(cell);
  const match = normalized.match(/^(.+?)\s*\(([^)]+)\)\s*(.+?)$/);
  if (!match) {
    die(`Unparseable trigram cell (expected "Name (Symbol) Element"): ${cell}`);
  }
  return {
    name: normalizeWhitespace(match[1]),
    symbol: normalizeWhitespace(match[2]),
    element: normalizeWhitespace(match[3]),
  };
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

const section = sliceSection(
  portableBody,
  "Canonical identity invariants (binary)",
);
if (!section) {
  die("Missing required section: '## Canonical identity invariants (binary)'");
}

const table = parseMarkdownTable(section);
if (!table) {
  die("Failed to parse identity invariants markdown table");
}

const requiredHeaders = ["Port", "Powerword", "Commander", "Trigram", "Binary"];
for (const h of requiredHeaders) {
  if (!table.headers.includes(h)) {
    die(`Identity invariants table missing required column: ${h}`);
  }
}

const invariantsPath = path.join(
  WORKSPACE_ROOT,
  "contracts/hfo_legendary_commanders_invariants.v1.json",
);
const invariants = JSON.parse(readText(invariantsPath));
const ports = Array.isArray(invariants?.ports) ? invariants.ports : null;
if (!ports || ports.length !== 8) {
  die(
    "contracts/hfo_legendary_commanders_invariants.v1.json must contain ports[8]",
  );
}

const expectedByPortId = new Map();
for (const p of ports) {
  expectedByPortId.set(String(p.port_id), p);
}

const seen = new Set();
for (const row of table.rows) {
  const port = normalizeWhitespace(row.Port);
  if (!/^P[0-7]$/.test(port)) {
    die(`Invalid Port value in identity table: ${row.Port}`);
  }
  if (seen.has(port)) {
    die(`Duplicate Port row in identity table: ${port}`);
  }
  seen.add(port);

  const expected = expectedByPortId.get(port);
  if (!expected) {
    die(`Port in identity table not found in invariants contract: ${port}`);
  }

  const powerword = normalizeWhitespace(row.Powerword);
  const commander = normalizeWhitespace(row.Commander);
  const binary = normalizeWhitespace(row.Binary);
  const trigram = parseTrigramCell(row.Trigram);

  if (powerword !== String(expected.powerword)) {
    die(
      `Powerword mismatch for ${port}: table=${powerword} contract=${expected.powerword}`,
    );
  }
  if (commander !== String(expected.commander_name)) {
    die(
      `Commander mismatch for ${port}: table=${commander} contract=${expected.commander_name}`,
    );
  }
  if (binary !== String(expected.binary)) {
    die(
      `Binary mismatch for ${port}: table=${binary} contract=${expected.binary}`,
    );
  }

  if (trigram.name !== String(expected.trigram?.name)) {
    die(
      `Trigram name mismatch for ${port}: table=${trigram.name} contract=${expected.trigram?.name}`,
    );
  }
  if (trigram.symbol !== String(expected.trigram?.symbol)) {
    die(
      `Trigram symbol mismatch for ${port}: table=${trigram.symbol} contract=${expected.trigram?.symbol}`,
    );
  }
  if (trigram.element !== String(expected.trigram?.element)) {
    die(
      `Trigram element mismatch for ${port}: table=${trigram.element} contract=${expected.trigram?.element}`,
    );
  }
}

if (seen.size !== 8) {
  die(
    `Identity invariants table must include exactly 8 ports (found ${seen.size})`,
  );
}

process.stdout.write(
  `OK: identity invariants table matches SSOT (${path.relative(WORKSPACE_ROOT, docPath)})\n`,
);
