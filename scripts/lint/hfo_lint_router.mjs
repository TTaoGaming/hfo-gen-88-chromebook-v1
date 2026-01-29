#!/usr/bin/env node
/** Medallion: Bronze | Mutation: 0% | HIVE: V
 *
 * Flag-driven staged-file lint router.
 *
 * Designed to be called by lint-staged with a list of file paths.
 *
 * Flags (OpenFeature keys):
 * - lint.enabled (default true)
 * - lint.mermaid (default true)
 * - lint.jsonl (default true)
 * - lint.prettier_check (default false)  (format gating can be high-friction)
 * - lint.markdownlint (default false)
 * - lint.tripwire.slow_ms (default 2500)
 * - lint.tripwire.strict (default false)
 */

import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { performance } from 'node:perf_hooks';

import { loadHfoEnv } from '../flags/hfo_load_env.mjs';
import { installHfoOpenFeatureEnvProvider } from '../flags/hfo_openfeature_env_provider.mjs';

import YAML from 'yaml';
import { parse as parseJsonc, printParseErrorCode } from 'jsonc-parser';

function normalizeArgs(argv) {
    return argv.filter((a) => a && !a.startsWith('-'));
}

function uniq(arr) {
    return Array.from(new Set(arr));
}

function exists(file) {
    try {
        return fs.existsSync(file);
    } catch {
        return false;
    }
}

function extOf(file) {
    return path.extname(file).toLowerCase();
}

function run(cmd, args, { label } = {}) {
    const res = spawnSync(cmd, args, { stdio: 'inherit' });
    if (res.error) {
        console.error(`\n[hfo-lint] ${label ?? cmd} failed to start: ${res.error.message}`);
        return 2;
    }
    return res.status ?? 0;
}

function shouldLintFiles(files) {
    const any = files.some((f) => exists(f));
    return any;
}

async function main(argv) {
    loadHfoEnv({ cwd: process.cwd() });
    const of = installHfoOpenFeatureEnvProvider();

    const lintEnabled = await of.getBooleanValue('lint.enabled', true);
    if (!lintEnabled) return 0;

    const files = uniq(normalizeArgs(argv));
    if (!shouldLintFiles(files)) return 0;

    const mdFiles = files.filter((f) => ['.md', '.mdx'].includes(extOf(f)));
    const jsonlFiles = files.filter((f) => extOf(f) === '.jsonl');
    const jsonFiles = files.filter((f) => extOf(f) === '.json');
    const jsoncFiles = files.filter((f) => extOf(f) === '.jsonc');
    const yamlFiles = files.filter((f) => ['.yml', '.yaml'].includes(extOf(f)));
    const pyFiles = files.filter((f) => extOf(f) === '.py');
    const jsTsHtmlFiles = files.filter((f) => {
        const ext = extOf(f);
        return ['.js', '.mjs', '.cjs', '.ts', '.tsx', '.html'].includes(ext);
    });
    const mermaidFiles = files.filter((f) => ['.mmd', '.mermaid'].includes(extOf(f)));

    const prettierFiles = files.filter((f) => {
        const ext = extOf(f);
        return ['.md', '.mdx', '.yaml', '.yml', '.json', '.jsonc'].includes(ext);
    });

    const t0 = performance.now();

    let exitCode = 0;

    // Mermaid lint (handles fenced blocks in md + raw .mmd/.mermaid)
    if (await of.getBooleanValue('lint.mermaid', true)) {
        const targets = uniq([...mdFiles, ...mermaidFiles]);
        if (targets.length > 0) {
            const rc = run('node', ['scripts/mermaid_lint.mjs', ...targets], { label: 'mermaid' });
            exitCode = Math.max(exitCode, rc);
        }
    }

    // JSONL sanity: parse each non-empty line as JSON
    if (await of.getBooleanValue('lint.jsonl', true)) {
        if (jsonlFiles.length > 0) {
            const rc = lintJsonl(jsonlFiles);
            exitCode = Math.max(exitCode, rc);
        }
    }

    // JSON syntax (fast fail)
    if (await of.getBooleanValue('lint.json_syntax', true)) {
        if (jsonFiles.length > 0) {
            const rc = lintJson(jsonFiles);
            exitCode = Math.max(exitCode, rc);
        }
    }

    // JSONC syntax (fast fail)
    if (await of.getBooleanValue('lint.jsonc_syntax', true)) {
        if (jsoncFiles.length > 0) {
            const rc = lintJsonc(jsoncFiles);
            exitCode = Math.max(exitCode, rc);
        }
    }

    // YAML syntax (fast fail)
    if (await of.getBooleanValue('lint.yaml_syntax', true)) {
        if (yamlFiles.length > 0) {
            const rc = lintYaml(yamlFiles);
            exitCode = Math.max(exitCode, rc);
        }
    }

    // Prettier check (opt-in; can be high-friction)
    if (await of.getBooleanValue('lint.prettier_check', false)) {
        if (prettierFiles.length > 0) {
            const rc = run('npx', ['prettier', '--check', ...prettierFiles], { label: 'prettier --check' });
            exitCode = Math.max(exitCode, rc);
        }
    }

    // Markdownlint (opt-in)
    if (await of.getBooleanValue('lint.markdownlint', false)) {
        if (mdFiles.length > 0) {
            const rc = run('npx', ['markdownlint-cli2', ...mdFiles], { label: 'markdownlint' });
            exitCode = Math.max(exitCode, rc);
        }
    }

    // ESLint for JS/TS/HTML (opt-in; repo already uses eslint)
    if (await of.getBooleanValue('lint.eslint', false)) {
        if (jsTsHtmlFiles.length > 0) {
            const rc = run('npx', ['eslint', '--max-warnings=0', ...jsTsHtmlFiles], { label: 'eslint' });
            exitCode = Math.max(exitCode, rc);
        }
    }

    // TypeScript typecheck (opt-in; can be slow)
    if (await of.getBooleanValue('lint.tsc', false)) {
        const anyTs = jsTsHtmlFiles.some((f) => ['.ts', '.tsx'].includes(extOf(f)));
        if (anyTs) {
            const rc = run('npx', ['tsc', '-p', 'tsconfig.json', '--noEmit'], { label: 'tsc --noEmit' });
            exitCode = Math.max(exitCode, rc);
        }
    }

    // Python ruff (opt-in locally; recommended in CI)
    if (await of.getBooleanValue('lint.ruff', false)) {
        if (pyFiles.length > 0) {
            const rc = run('bash', ['scripts/mcp_env_wrap.sh', './.venv/bin/python', '-m', 'ruff', 'check', ...pyFiles], { label: 'ruff' });
            exitCode = Math.max(exitCode, rc);
        }
    }

    // yamllint (opt-in; stricter than YAML syntax)
    if (await of.getBooleanValue('lint.yamllint', false)) {
        if (yamlFiles.length > 0) {
            const rc = run('bash', ['scripts/mcp_env_wrap.sh', './.venv/bin/python', '-m', 'yamllint', ...yamlFiles], { label: 'yamllint' });
            exitCode = Math.max(exitCode, rc);
        }
    }

    const elapsedMs = Math.round(performance.now() - t0);
    const slowMs = await of.getNumberValue('lint.tripwire.slow_ms', 2500);
    const strictTripwire = await of.getBooleanValue('lint.tripwire.strict', false);

    if (elapsedMs >= slowMs) {
        const msg = `[hfo-lint] Tripwire: lint took ${elapsedMs}ms (threshold ${slowMs}ms). Consider disabling high-friction checks (lint.prettier_check / lint.markdownlint) or raising lint.tripwire.slow_ms.`;
        if (strictTripwire) {
            console.error(msg);
            exitCode = Math.max(exitCode, 1);
        } else {
            console.warn(msg);
        }
    }

    return exitCode;
}

function lintJson(files) {
    let ok = true;
    for (const file of files) {
        if (!exists(file)) continue;
        try {
            JSON.parse(fs.readFileSync(file, 'utf-8'));
        } catch (e) {
            ok = false;
            const msg = e?.message ? String(e.message) : String(e);
            console.error(`[hfo-lint][json] ${file} invalid JSON: ${msg}`);
        }
    }
    return ok ? 0 : 1;
}

function lintJsonc(files) {
    let ok = true;
    for (const file of files) {
        if (!exists(file)) continue;
        const text = fs.readFileSync(file, 'utf-8');
        const errors = [];
        const data = parseJsonc(text, errors, { allowTrailingComma: true });
        if (errors.length > 0 || data === undefined) {
            ok = false;
            for (const err of errors) {
                console.error(`[hfo-lint][jsonc] ${file}@${err.offset}: ${printParseErrorCode(err.error)}`);
            }
        }
    }
    return ok ? 0 : 1;
}

function lintYaml(files) {
    let ok = true;
    for (const file of files) {
        if (!exists(file)) continue;
        try {
            YAML.parse(fs.readFileSync(file, 'utf-8'));
        } catch (e) {
            ok = false;
            const msg = e?.message ? String(e.message) : String(e);
            console.error(`[hfo-lint][yaml] ${file} invalid YAML: ${msg}`);
        }
    }
    return ok ? 0 : 1;
}

function lintJsonl(files) {
    let ok = true;

    for (const file of files) {
        if (!exists(file)) continue;

        const text = fs.readFileSync(file, 'utf-8');
        const lines = text.split(/\r?\n/);

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;

            try {
                JSON.parse(line);
            } catch (e) {
                ok = false;
                const msg = e?.message ? String(e.message) : String(e);
                console.error(`[hfo-lint][jsonl] ${file}:${i + 1} invalid JSON: ${msg}`);
            }
        }
    }

    return ok ? 0 : 1;
}

process.exitCode = await main(process.argv.slice(2));
