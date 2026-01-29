#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const WORKSPACE_ROOT = process.cwd();

export const MANIFEST_PATH = path.join(
  WORKSPACE_ROOT,
  'contracts',
  'hfo_hive8_compendium_manifest.v1.json',
);

function die(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function readJson(filePath) {
  if (!fs.existsSync(filePath)) {
    die(`Missing file: ${path.relative(WORKSPACE_ROOT, filePath)}`);
  }
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    die(`Invalid JSON in ${path.relative(WORKSPACE_ROOT, filePath)}: ${String(error)}`);
  }
}

export function loadCompendiumManifest() {
  const manifest = readJson(MANIFEST_PATH);

  if (manifest?.schema_id !== 'hfo.hive8.compendium_manifest') {
    die(`manifest schema_id must be hfo.hive8.compendium_manifest (found: ${String(manifest?.schema_id)})`);
  }
  if (manifest?.schema_version !== 1) {
    die(`manifest schema_version must be 1 (found: ${String(manifest?.schema_version)})`);
  }
  if (!Array.isArray(manifest?.families) || manifest.families.length < 1) {
    die('manifest.families must be a non-empty array');
  }

  return manifest;
}

export function resolveFamily(manifest, familyId) {
  const family = manifest.families.find((f) => f.family_id === familyId);
  if (!family) {
    die(`Missing family_id in manifest: ${familyId}`);
  }
  if (!Array.isArray(family.entries) || family.entries.length < 1) {
    die(`Family ${familyId} entries must be a non-empty array`);
  }
  if (typeof family.canonical_version !== 'string' || !family.canonical_version) {
    die(`Family ${familyId} canonical_version must be a non-empty string`);
  }
  return family;
}

export function resolveCanonicalEntry(family) {
  const entry = family.entries.find(
    (e) => e.version === family.canonical_version && e.status === 'canonical',
  );
  if (!entry) {
    die(
      `No canonical entry found for canonical_version=${family.canonical_version} in family ${family.family_id}`,
    );
  }
  if (typeof entry.path !== 'string' || !entry.path) {
    die(`Canonical entry path missing for family ${family.family_id}`);
  }
  return entry;
}

export function resolveDefaultDocPath({
  manifest,
  familyId,
}) {
  const family = resolveFamily(manifest, familyId);
  const entry = resolveCanonicalEntry(family);

  const absolutePath = path.isAbsolute(entry.path)
    ? entry.path
    : path.join(WORKSPACE_ROOT, entry.path);

  if (!fs.existsSync(absolutePath)) {
    die(`Missing canonical doc: ${path.relative(WORKSPACE_ROOT, absolutePath)}`);
  }

  return {
    family,
    entry,
    absolutePath,
  };
}

const THIS_FILE = fileURLToPath(import.meta.url);

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(THIS_FILE)) {
  // Manual CLI helper: prints the canonical path.
  const manifest = loadCompendiumManifest();
  const familyId = manifest?.defaults?.canonical_family_id;
  if (!familyId) {
    die('manifest.defaults.canonical_family_id missing');
  }
  const resolved = resolveDefaultDocPath({ manifest, familyId });
  process.stdout.write(`${path.relative(WORKSPACE_ROOT, resolved.absolutePath)}\n`);
}
