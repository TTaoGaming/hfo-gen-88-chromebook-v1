#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

import { loadCompendiumManifest, resolveDefaultDocPath } from './hive8_compendium_manifest.mjs';

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

function indexOfSection(markdown, heading) {
  const needle = `\n## ${heading}\n`;
  const idx = markdown.indexOf(needle);
  if (idx >= 0) return idx;

  // Also allow the heading to be the first thing after front matter.
  if (markdown.startsWith(`## ${heading}\n`)) return 0;
  return -1;
}

const docPath = (() => {
  if (process.argv[2]) {
    return path.isAbsolute(process.argv[2])
      ? process.argv[2]
      : path.join(WORKSPACE_ROOT, process.argv[2]);
  }

  const manifest = loadCompendiumManifest();
  const familyId = manifest?.defaults?.portable_links_verify_family_id ?? manifest?.defaults?.canonical_family_id;
  if (!familyId) {
    die('manifest.defaults.portable_links_verify_family_id missing');
  }
  const resolved = resolveDefaultDocPath({ manifest, familyId });
  return resolved.absolutePath;
})();

const markdown = readText(docPath);

// Hard-ban web URLs anywhere.
if (/https?:\/\//i.test(markdown)) {
  die('Found http(s) URL in document; portable docs must not contain web URLs');
}

const extraIdx = indexOfSection(markdown, 'Extra References (non-portable)');
if (extraIdx < 0) {
  die("Missing required section: '## Extra References (non-portable)'");
}

const body = markdown.slice(0, extraIdx);

// Disallow Markdown links in the portable body.
// This matches common inline link syntax: [text](target)
const linkMatch = body.match(/\[[^\]]+\]\([^\)]+\)/);
if (linkMatch) {
  die(`Found Markdown link in portable body: ${linkMatch[0]}`);
}

process.stdout.write(
  `OK: portable link policy satisfied (${path.relative(WORKSPACE_ROOT, docPath)})\n`,
);
