#!/usr/bin/env node
/** Medallion: Bronze | Mutation: 0% | HIVE: V
 *
 * Loads repo-local env files in a predictable order.
 *
 * - `.env` (repo root) is the primary local override (gitignored)
 * - `feature_flags.env` is an optional secondary file (gitignored if you add it)
 * - `feature_flags.env.example` is documentation only
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

import dotenv from 'dotenv';

function loadIfExists(filePath) {
    if (!fs.existsSync(filePath)) return false;
    dotenv.config({ path: filePath, override: false });
    return true;
}

export function loadHfoEnv({ cwd = process.cwd() } = {}) {
    const envPath = path.join(cwd, '.env');
    const featureFlagsPath = path.join(cwd, 'feature_flags.env');

    loadIfExists(envPath);
    loadIfExists(featureFlagsPath);
}

if (import.meta.url === `file://${process.argv[1]}`) {
    loadHfoEnv();
}
