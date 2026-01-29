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
    const blocks = [];
    const re = /```mermaid\s*\n([\s\S]*?)\n```/g;
    let match;
    while ((match = re.exec(markdown)) !== null) {
        blocks.push(match[1]);
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

    if (wantsHelp || files.length === 0) {
        console.error('Usage: node scripts/mermaid_lint.mjs <file...>');
        console.error('  Intended for lint-staged: checks only passed files.');
        return wantsHelp ? 0 : 2;
    }

    /** @type {{file:string, blockIndex?:number, message:string}[]} */
    const errors = [];

    for (const file of files) {
        if (!fs.existsSync(file)) continue;

        const ext = path.extname(file).toLowerCase();
        if (!(isMarkdown(file) || isMermaidFile(file))) continue;

        const text = fs.readFileSync(file, 'utf-8');

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

        // Heuristic: flag unterminated fences early.
        const fenceCount = (text.match(/```mermaid/g) || []).length;
        if (fenceCount !== blocks.length) {
            errors.push({
                file,
                message: `Found ${fenceCount} mermaid fence starts but ${blocks.length} complete blocks. Possible missing closing \`\`\`.`,
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
