#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import YAML from "yaml";

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

function extractFrontMatter(markdown) {
  const lines = markdown.split(/\r?\n/);
  if (lines[0]?.trim() !== "---") return null;

  for (let i = 1; i < lines.length; i += 1) {
    if (lines[i]?.trim() === "---") {
      return lines.slice(1, i).join("\n");
    }
  }

  return null;
}

function normalizeCommand(value) {
  if (typeof value !== "string") return "";

  // Remove inline code markers and normalize whitespace.
  return value.replace(/`/g, "").replace(/\s+/g, " ").trim();
}

function parseExecutableGatesIndexCommands(markdown) {
  // Find the specific table by anchoring on the heading.
  const heading = "## Executable Gates Index (DevOps/TDD)";
  const headingIndex = markdown.indexOf(heading);
  if (headingIndex < 0) {
    die('Missing section: "## Executable Gates Index (DevOps/TDD)"');
  }

  const afterHeading = markdown.slice(headingIndex + heading.length);
  const lines = afterHeading.split(/\r?\n/);

  // Find the first markdown table header row.
  const headerRowIndex = lines.findIndex((l) =>
    l.trim().startsWith("| Gate |"),
  );
  if (headerRowIndex < 0) {
    die('Missing gates index table header row: "| Gate |"');
  }

  // Expect the next row to be the separator row.
  const separatorRowIndex = headerRowIndex + 1;
  if (
    !lines[separatorRowIndex] ||
    !lines[separatorRowIndex].trim().startsWith("| ----")
  ) {
    die("Malformed gates index table: missing separator row");
  }

  const commands = [];
  for (let i = separatorRowIndex + 1; i < lines.length; i += 1) {
    const line = lines[i];
    if (!line) break;
    const trimmed = line.trim();

    // End of table.
    if (!trimmed.startsWith("|")) break;

    // Split into cells; markdown tables have leading and trailing pipes.
    const rawCells = trimmed.split("|").map((c) => c.trim());
    // rawCells[0] and rawCells[last] are empty due to leading/trailing '|'
    const cells = rawCells.slice(1, rawCells.length - 1);

    // Expect: Gate | What it protects | Command | Pass condition
    if (cells.length < 4) {
      die(`Malformed gates index table row (expected >=4 cells): ${trimmed}`);
    }

    const commandCell = normalizeCommand(cells[2]);
    if (commandCell) commands.push(commandCell);
  }

  if (commands.length < 3) {
    die("Gates index table must contain at least 3 command rows");
  }

  return commands;
}

function loadFrontMatterCommands(markdown) {
  const fm = extractFrontMatter(markdown);
  if (!fm) {
    die("Missing YAML front matter");
  }

  let parsed;
  try {
    parsed = YAML.parse(fm);
  } catch (error) {
    die(`Invalid YAML front matter: ${String(error)}`);
  }

  if (!Array.isArray(parsed?.gates) || parsed.gates.length < 3) {
    die("frontmatter.gates must be an array of at least 3 gate entries");
  }

  const commands = parsed.gates
    .map((g) => normalizeCommand(g?.command))
    .filter(Boolean);

  if (commands.length < 3) {
    die("frontmatter.gates must include at least 3 non-empty command strings");
  }

  return commands;
}

function diffSets({ expected, actual }) {
  const expectedSet = new Set(expected);
  const actualSet = new Set(actual);

  const missing = [...expectedSet].filter((x) => !actualSet.has(x));
  const extra = [...actualSet].filter((x) => !expectedSet.has(x));

  return { missing, extra };
}

let docPath;

if (process.argv[2]) {
  docPath = path.isAbsolute(process.argv[2])
    ? process.argv[2]
    : path.join(WORKSPACE_ROOT, process.argv[2]);
} else {
  const manifest = loadCompendiumManifest();
  const familyId = manifest?.defaults?.canonical_family_id;
  if (!familyId) {
    die("manifest.defaults.canonical_family_id missing");
  }
  const resolved = resolveDefaultDocPath({ manifest, familyId });
  docPath = resolved.absolutePath;
}

const markdown = readText(docPath);

const frontmatterCommands = loadFrontMatterCommands(markdown);
const tableCommands = parseExecutableGatesIndexCommands(markdown);

const { missing, extra } = diffSets({
  expected: frontmatterCommands,
  actual: tableCommands,
});

if (missing.length || extra.length) {
  if (missing.length) {
    process.stderr.write("Missing commands in Executable Gates Index table:\n");
    for (const cmd of missing) process.stderr.write(`- ${cmd}\n`);
  }
  if (extra.length) {
    process.stderr.write(
      "Extra commands in Executable Gates Index table (not in frontmatter.gates):\n",
    );
    for (const cmd of extra) process.stderr.write(`- ${cmd}\n`);
  }
  die(`Gate index parity failed for ${path.relative(WORKSPACE_ROOT, docPath)}`);
}

process.stdout.write(
  `OK: gates index parity satisfied (${path.relative(WORKSPACE_ROOT, docPath)})\n`,
);
