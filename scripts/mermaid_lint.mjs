#!/usr/bin/env node
/** Medallion: Bronze | Mutation: 0% | HIVE: V
 *
 * Mermaid linter (fail-closed).
 *
 * - Validates fenced ```mermaid blocks inside Markdown/MDX files
 * - Validates entire .mmd files
 * - Uses @mermaid-js/parser (fast, no browser) to catch parse errors early
 *
 * Intended to run via lint-staged so only changed files are checked.
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

import { JSDOM } from 'jsdom';

/** @type {import('mermaid').default | null} */
let mermaidSingleton = null;

async function getMermaid() {
    if (mermaidSingleton) return mermaidSingleton;

    // Mermaid expects a browser-ish environment for its sanitizer (DOMPurify) in some
    // diagram types (notably flowcharts with subgraphs). Provide a minimal DOM.
    const dom = new JSDOM('<!doctype html><html><body></body></html>');
    globalThis.window = dom.window;
    globalThis.document = dom.window.document;
    globalThis.navigator = dom.window.navigator;

    mermaidSingleton = (await import('mermaid')).default;
    return mermaidSingleton;
}

function isMarkdown(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    return ext === '.md' || ext === '.mdx';
}

function isMermaidFile(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    return ext === '.mmd' || ext === '.mermaid';
}

function extractMermaidBlocksFromMarkdown(markdown) {
  /** @type {string[]} */
  const blocks = [];

  // Support both backtick and tilde fences (```mermaid and ~~~mermaid).
  // We intentionally keep this scanner simple and deterministic.
  const lines = markdown.split(/\r?\n/);
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // Start fence: ```mermaid or ~~~mermaid (any amount of extra whitespace)
    const fenceMatch = /^(?<fence>`{3,}|~{3,})\s*mermaid\s*$/i.exec(trimmed);
    if (!fenceMatch) {
      i += 1;
      continue;
    }

    const fence = fenceMatch.groups?.fence ?? "```";
    const closeRe = new RegExp(
      `^${fence.replace(/([\\^$.*+?()[\]{}|])/g, "\\$1")}\\s*$`,
    );

    i += 1;
    const start = i;
    while (i < lines.length && !closeRe.test(lines[i].trim())) {
      i += 1;
    }

    // If we never found a close fence, treat the rest as a block; a separate
    // heuristic below will flag unterminated fences.
    const end = i;
    blocks.push(lines.slice(start, end).join("\n"));

    // Move past the closing fence if present.
    if (i < lines.length && closeRe.test(lines[i].trim())) {
      i += 1;
    }
  }

  return blocks;
}

async function validateDiagram(diagramText, ctx) {
    const trimmed = (diagramText ?? '').trim();
    if (!trimmed) return;

    // mermaid.parse() throws on invalid syntax and supports the full set of Mermaid diagrams.
    const mermaid = await getMermaid();
    await mermaid.parse(trimmed);
}

async function main(argv) {
    const files = argv.filter((a) => !a.startsWith('-'));
    const wantsHelp = argv.includes('--help') || argv.includes('-h');

    if (wantsHelp) {
        console.error('Usage: node scripts/mermaid_lint.mjs <file...>');
        console.error('  Intended for lint-staged: checks only passed files.');
        return 0;
    }

    if (files.length === 0) {
        // Allow running as a general-purpose gate even when no files are passed.
        // In lint-staged, files are always provided.
        console.log('OK: mermaid lint skipped (no files provided)');
        return 0;
    }

    /** @type {{file:string, blockIndex?:number, message:string}[]} */
    const errors = [];

    for (const file of files) {
      if (!fs.existsSync(file)) continue;

      const ext = path.extname(file).toLowerCase();
      if (!(isMarkdown(file) || isMermaidFile(file))) continue;

      const text = fs.readFileSync(file, "utf-8");

      if (isMermaidFile(file)) {
        try {
          await validateDiagram(text, { file });
        } catch (err) {
          errors.push({
            file,
            message: err?.message ? String(err.message) : String(err),
          });
        }
        continue;
      }

      // Markdown
      const blocks = extractMermaidBlocksFromMarkdown(text);
      for (let i = 0; i < blocks.length; i++) {
        try {
          await validateDiagram(blocks[i], { file, blockIndex: i });
        } catch (err) {
          errors.push({
            file,
            blockIndex: i,
            message: err?.message ? String(err.message) : String(err),
          });
        }
      }

      // Heuristic: flag unterminated fences early (supports ```mermaid and ~~~mermaid).
      const fenceCount = (
        text.match(/(^|\n)\s*(`{3,}|~{3,})\s*mermaid\s*(\n|\r\n)/gi) || []
      ).length;
      if (fenceCount !== blocks.length) {
        errors.push({
          file,
          message: `Found ${fenceCount} mermaid fence starts but ${blocks.length} complete blocks. Possible missing closing fence.`,
        });
      }
    }

    if (errors.length > 0) {
        console.error('\n[mermaid-lint] Parse errors detected:');
        for (const e of errors) {
            const where = typeof e.blockIndex === 'number' ? `${e.file} (block #${e.blockIndex + 1})` : e.file;
            console.error(`- ${where}: ${e.message}`);
        }
        console.error('\nFix Mermaid parse errors before committing.');
        return 1;
    }

    return 0;
}

process.exitCode = await main(process.argv.slice(2));
