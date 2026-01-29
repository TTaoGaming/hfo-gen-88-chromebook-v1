#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

import { loadCompendiumManifest, resolveFamily, resolveCanonicalEntry } from './hive8_compendium_manifest.mjs';

const WORKSPACE_ROOT = process.cwd();

function die(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function assert(cond, message) {
  if (!cond) die(message);
}

const manifest = loadCompendiumManifest();

assert(manifest.defaults && typeof manifest.defaults === 'object', 'manifest.defaults must exist');
assert(
  typeof manifest.defaults.canonical_family_id === 'string' && manifest.defaults.canonical_family_id,
  'manifest.defaults.canonical_family_id must be a non-empty string',
);

const family = resolveFamily(manifest, manifest.defaults.canonical_family_id);
const canonical = resolveCanonicalEntry(family);

for (const entry of family.entries) {
  assert(typeof entry.version === 'string' && entry.version, `Entry missing version in family ${family.family_id}`);
  assert(
    entry.status === 'canonical' || entry.status === 'superseded' || entry.status === 'archived',
    `Invalid entry.status for ${entry.version} (must be canonical|superseded|archived)`,
  );
  assert(typeof entry.path === 'string' && entry.path, `Entry missing path for ${entry.version}`);

  const absolutePath = path.isAbsolute(entry.path) ? entry.path : path.join(WORKSPACE_ROOT, entry.path);
  assert(fs.existsSync(absolutePath), `Missing compendium file: ${path.relative(WORKSPACE_ROOT, absolutePath)}`);
}

if (canonical.status !== 'canonical') {
  die('Canonical entry status must be canonical');
}

process.stdout.write(
  `OK: compendium manifest validated (canonical=${path.relative(WORKSPACE_ROOT, path.join(WORKSPACE_ROOT, canonical.path))})\n`,
);
