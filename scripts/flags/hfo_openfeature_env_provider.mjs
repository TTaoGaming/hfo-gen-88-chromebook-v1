#!/usr/bin/env node
/** Medallion: Bronze | Mutation: 0% | HIVE: V
 *
 * OpenFeature provider backed by .env values.
 *
 * Inputs:
 * - HFO_OPENFEATURE_FLAGS_JSON='{"lint.enabled":true, "lint.mermaid":true}'
 * - Convenience overrides like HFO_FLAG_LINT_MERMAID=0 (maps to lint.mermaid)
 */

import process from 'node:process';

import { OpenFeature } from '@openfeature/server-sdk';

function coerceScalar(value) {
    if (value === undefined || value === null) return undefined;
    const v = String(value).trim();
    if (!v) return undefined;

    if (/^(true|1|yes|on)$/i.test(v)) return true;
    if (/^(false|0|no|off)$/i.test(v)) return false;

    // number
    if (/^-?\d+(\.\d+)?$/.test(v)) return Number(v);

    return v;
}

function safeParseJson(text) {
    try {
        return JSON.parse(text);
    } catch {
        return null;
    }
}

function getFlagMap() {
    const out = {};

    const jsonText = process.env.HFO_OPENFEATURE_FLAGS_JSON;
    if (jsonText) {
        const parsed = safeParseJson(jsonText);
        if (parsed && typeof parsed === 'object') {
            for (const [k, v] of Object.entries(parsed)) {
                out[String(k)] = v;
            }
        }
    }

    // Convenience env vars: HFO_FLAG_FOO_BAR -> foo.bar
    for (const [k, v] of Object.entries(process.env)) {
        if (!k.startsWith('HFO_FLAG_')) continue;
        const suffix = k.slice('HFO_FLAG_'.length);
        const flagKey = suffix
            .toLowerCase()
            .split('_')
            .filter(Boolean)
            .join('.');

        out[flagKey] = coerceScalar(v);
    }

    return out;
}

export function createHfoEnvFlagResolver() {
    const flagMap = getFlagMap();

    return {
        resolveBoolean(flagKey, defaultValue) {
            const v = flagMap[flagKey];
            if (typeof v === 'boolean') return v;
            return defaultValue;
        },
        resolveString(flagKey, defaultValue) {
            const v = flagMap[flagKey];
            if (typeof v === 'string') return v;
            return defaultValue;
        },
        resolveNumber(flagKey, defaultValue) {
            const v = flagMap[flagKey];
            if (typeof v === 'number' && Number.isFinite(v)) return v;
            return defaultValue;
        },
        _debugSnapshot() {
            return { ...flagMap };
        },
    };
}

class HfoEnvOpenFeatureProvider {
    metadata = { name: 'hfo-env-provider' };

    constructor() {
        this._resolver = createHfoEnvFlagResolver();
    }

    resolveBooleanEvaluation(flagKey, defaultValue) {
        return { value: this._resolver.resolveBoolean(flagKey, defaultValue), variant: 'env' };
    }

    resolveStringEvaluation(flagKey, defaultValue) {
        return { value: this._resolver.resolveString(flagKey, defaultValue), variant: 'env' };
    }

    resolveNumberEvaluation(flagKey, defaultValue) {
        return { value: this._resolver.resolveNumber(flagKey, defaultValue), variant: 'env' };
    }

    resolveObjectEvaluation(flagKey, defaultValue) {
        return { value: defaultValue, variant: 'default' };
    }
}

export function installHfoOpenFeatureEnvProvider() {
    OpenFeature.setProvider(new HfoEnvOpenFeatureProvider());
    return OpenFeature.getClient();
}
