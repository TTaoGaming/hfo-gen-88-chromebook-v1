#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import YAML from 'yaml';

import {
  loadCompendiumManifest,
  resolveDefaultDocPath,
} from './hive8_compendium_manifest.mjs';

const WORKSPACE_ROOT = process.cwd();

function die(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function readText(filePath) {
  if (!fs.existsSync(filePath)) {
    die(`Missing file: ${path.relative(WORKSPACE_ROOT, filePath)}`);
  }
  return fs.readFileSync(filePath, 'utf8');
}

function extractFrontMatter(markdown) {
  const lines = markdown.split(/\r?\n/);
  if (lines[0]?.trim() !== '---') return null;

  for (let i = 1; i < lines.length; i += 1) {
    if (lines[i]?.trim() === '---') {
      return lines.slice(1, i).join('\n');
    }
  }

  return null;
}

function assertKey(obj, keyPath) {
  const parts = keyPath.split('.');
  let cur = obj;
  for (const part of parts) {
    if (!cur || typeof cur !== 'object' || !(part in cur)) {
      die(`Missing required front matter key: ${keyPath}`);
    }
    cur = cur[part];
  }
}

let docPath;
let expectedVersion;

if (process.argv[2]) {
  docPath = path.isAbsolute(process.argv[2])
    ? process.argv[2]
    : path.join(WORKSPACE_ROOT, process.argv[2]);
} else {
  const manifest = loadCompendiumManifest();
  const familyId = manifest?.defaults?.frontmatter_verify_family_id ?? manifest?.defaults?.canonical_family_id;
  if (!familyId) {
    die('manifest.defaults.frontmatter_verify_family_id missing');
  }
  const resolved = resolveDefaultDocPath({ manifest, familyId });
  docPath = resolved.absolutePath;
  expectedVersion = resolved.entry.version;
}

const markdown = readText(docPath);
const fm = extractFrontMatter(markdown);
if (!fm) {
  die(`Missing YAML front matter in ${path.relative(WORKSPACE_ROOT, docPath)}`);
}

let parsed;
try {
  parsed = YAML.parse(fm);
} catch (error) {
  die(`Invalid YAML front matter: ${String(error)}`);
}

assertKey(parsed, 'schema_id');
assertKey(parsed, 'schema_version');
assertKey(parsed, 'version');
assertKey(parsed, 'doc_id');
assertKey(parsed, 'ssot.identity_invariants');
assertKey(parsed, 'ssot.mapping_contract');
assertKey(parsed, 'gates');

if (parsed.schema_id !== 'hfo.hive8.compendium') {
  die(`schema_id must be hfo.hive8.compendium (found: ${String(parsed.schema_id)})`);
}

if (expectedVersion && parsed.version !== expectedVersion) {
  die(`version must be ${expectedVersion} (found: ${String(parsed.version)})`);
}

if (!Array.isArray(parsed.gates) || parsed.gates.length < 3) {
  die('gates must be an array of at least 3 gate entries');
}

process.stdout.write(
  `OK: compendium front matter parsed (${path.relative(WORKSPACE_ROOT, docPath)})\n`,
);
