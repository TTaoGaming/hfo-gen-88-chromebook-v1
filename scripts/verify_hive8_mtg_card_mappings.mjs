#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const WORKSPACE_ROOT = process.cwd();

const CONTRACT_PATH = path.join(
  WORKSPACE_ROOT,
  "contracts",
  "hfo_mtg_port_card_mappings.v5.json",
);

const DOC_PATHS = [
  path.join(
    WORKSPACE_ROOT,
    "hfo_hot_obsidian_forge",
    "2_gold",
    "2_resources",
    "reports",
    "hive8_cards",
    "HFO_HIVE8_LEGENDARY_COMMANDERS_3_PLUS_1_MTG_JADC2_FRONT_DOOR_V1_2026_01_29.md",
  ),
  path.join(
    WORKSPACE_ROOT,
    "hfo_hot_obsidian_forge",
    "2_gold",
    "2_resources",
    "reports",
    "hive8_doctrine",
    "HFO_HIVE8_GEN88_V5_LEGENDARY_COMMANDERS_3_PLUS_1_COMPENDIUM_BLUF_PLUS_8x8_PLUS_META_V4_2026_01_29.md",
  ),
  path.join(
    WORKSPACE_ROOT,
    "hfo_hot_obsidian_forge",
    "2_gold",
    "2_resources",
    "reports",
    "hive8_cards",
    "HFO_CARD_SET_HIVE8_LEGENDARY_COMMANDERS_V1_2026_01_27.md",
  ),
  path.join(
    WORKSPACE_ROOT,
    "hfo_hot_obsidian_forge",
    "2_gold",
    "2_resources",
    "reports",
    "hive8_cards",
    "HFO_HIVE8_3_PLUS_1_CARD_SCHEMA_AND_TILE_NARRATIVES_V1_2026_01_27.md",
  ),
];

const EXPECTED_HEADERS = [
  "Port",
  "Commander",
  "Mosaic Domain",
  "Sliver (Static)",
  "Sliver (Trigger)",
  "Sliver (Activated)",
  "Equipment (Non-creature)",
];

function die(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function normalizeCell(value) {
  return String(value ?? "")
    .trim()
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/\s+/g, " ");
}

function readText(filePath) {
  if (!fs.existsSync(filePath)) {
    die(`Missing file: ${path.relative(WORKSPACE_ROOT, filePath)}`);
  }
  return fs.readFileSync(filePath, "utf8");
}

function parseJsonStrict(filePath) {
  const raw = readText(filePath);
  try {
    return JSON.parse(raw);
  } catch (error) {
    die(`Invalid JSON in ${path.relative(WORKSPACE_ROOT, filePath)}: ${error}`);
  }
}

function splitMarkdownRow(line) {
  // Trim edges then split, dropping the empty cells caused by leading/trailing pipes.
  const parts = line
    .trim()
    .split("|")
    .map((p) => normalizeCell(p))
    .filter((p) => p.length > 0);
  return parts;
}

function extractTableRowsByHeaders(markdown, headers) {
  const lines = markdown.split(/\r?\n/);

  for (let i = 0; i < lines.length; i += 1) {
    const line = lines[i];
    if (!line.trim().startsWith("|")) continue;

    const candidateHeaders = splitMarkdownRow(line);
    const matchesAll = headers.every((h) => candidateHeaders.includes(h));
    if (!matchesAll) continue;

    const separator = lines[i + 1] ?? "";
    if (!separator.includes("|") || !separator.includes("-")) continue;

    const rows = [];
    for (let j = i + 2; j < lines.length; j += 1) {
      const rowLine = lines[j];
      if (!rowLine.trim().startsWith("|")) break;

      const cells = splitMarkdownRow(rowLine);
      if (cells.length === 0) continue;
      rows.push(cells);
    }

    return { header: candidateHeaders, rows };
  }

  die(
    `Could not find a mapping table with required headers: ${headers.join(", ")}`,
  );
}

function buildExpectedRowsFromContract(contract) {
  if (contract?.gen !== 88) {
    die(`Contract gen must be 88 (found: ${String(contract?.gen)})`);
  }
  if (contract?.version !== "v5") {
    die(`Contract version must be v5 (found: ${String(contract?.version)})`);
  }
  if (!contract?.ports || typeof contract.ports !== "object") {
    die("Contract missing required object: ports");
  }

  const expected = new Map();

  for (let portIndex = 0; portIndex < 8; portIndex += 1) {
    const port = `P${portIndex}`;
    const entry = contract.ports[port];
    if (!entry) {
      die(`Contract missing port entry: ${port}`);
    }

    const commander = normalizeCell(entry.commander);
    const mosaicDomain = normalizeCell(entry.mosaic_domain);

    if (!commander) die(`Contract ${port} missing commander`);
    if (!mosaicDomain) die(`Contract ${port} missing mosaic_domain`);

    const slivers = Array.isArray(entry.slivers) ? entry.slivers : [];
    if (slivers.length !== 3) {
      die(
        `Contract ${port} slivers must have length 3 (found: ${slivers.length})`,
      );
    }

    const bySlot = new Map(
      slivers.map((s) => [normalizeCell(s.slot), normalizeCell(s.card)]),
    );

    const staticSliver = bySlot.get("static");
    const triggerSliver = bySlot.get("trigger");
    const activatedSliver = bySlot.get("activated");

    if (!staticSliver) die(`Contract ${port} missing sliver slot: static`);
    if (!triggerSliver) die(`Contract ${port} missing sliver slot: trigger`);
    if (!activatedSliver)
      die(`Contract ${port} missing sliver slot: activated`);

    const equipment = normalizeCell(entry?.equipment?.card);
    if (!equipment) die(`Contract ${port} missing equipment.card`);

    expected.set(port, [
      port,
      commander,
      mosaicDomain,
      staticSliver,
      triggerSliver,
      activatedSliver,
      equipment,
    ]);
  }

  return expected;
}

function assertDocMatchesExpected({ docPath, expectedRows }) {
  const markdown = readText(docPath);
  const { rows } = extractTableRowsByHeaders(markdown, EXPECTED_HEADERS);

  const rowByPort = new Map();
  for (const row of rows) {
    if (row.length < 7) continue;
    const port = normalizeCell(row[0]);
    if (port.startsWith("P"))
      rowByPort.set(port, row.slice(0, 7).map(normalizeCell));
  }

  for (let portIndex = 0; portIndex < 8; portIndex += 1) {
    const port = `P${portIndex}`;
    const expected = expectedRows.get(port);
    const actual = rowByPort.get(port);

    if (!expected) die(`Internal error: missing expected row for ${port}`);
    if (!actual) {
      die(
        `Doc missing row for ${port}: ${path.relative(WORKSPACE_ROOT, docPath)}`,
      );
    }

    const diffs = [];
    for (let col = 0; col < 7; col += 1) {
      if (normalizeCell(actual[col]) !== normalizeCell(expected[col])) {
        diffs.push({ col, expected: expected[col], actual: actual[col] });
      }
    }

    if (diffs.length > 0) {
      const header = `${path.relative(WORKSPACE_ROOT, docPath)}: ${port} mapping mismatch`;
      const details = diffs
        .map(
          (d) =>
            `  - col ${d.col} expected="${d.expected}" actual="${d.actual}"`,
        )
        .join("\n");
      die(`${header}\n${details}`);
    }
  }
}

function main() {
  const contract = parseJsonStrict(CONTRACT_PATH);
  const expectedRows = buildExpectedRowsFromContract(contract);

  for (const docPath of DOC_PATHS) {
    assertDocMatchesExpected({ docPath, expectedRows });
  }

  process.stdout.write(
    `OK: HIVE8 3+1 mappings match ${path.relative(WORKSPACE_ROOT, CONTRACT_PATH)} across ${DOC_PATHS.length} docs.\n`,
  );
}

main();
