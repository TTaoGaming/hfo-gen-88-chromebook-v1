// Medallion: Bronze | Mutation: 0% | HIVE: I
// 🎯 PORT-0-SENSE: Zod Schema Validator

import { z } from 'zod';
import { P0SensingSchema } from '../contracts/omega_contracts.zod.ts';

/**
 * P0 Validator
 * Validates P0 output against P0SensingSchema contract
 * Ensures Port 0 maintains schema compliance
 */

export class P0Validator {
    constructor() {
        this.schema = P0SensingSchema;
        this.validationErrors = [];
        this.validationCount = 0;
        this.errorCount = 0;
    }

    /**
     * Validate sensing data against P0SensingSchema
     * Returns { valid: boolean, data: any, errors: array }
     */
    validate(sensingData) {
        this.validationCount++;

        try {
            // Create CloudEvent envelope
            const cloudEvent = {
                id: crypto.randomUUID(),
                source: 'hfo.omega.p0',
                specversion: '1.0',
                type: 'hfo.omega.p0.sensing',
                datacontenttype: 'application/json',
                time: new Date().toISOString(),
                data: sensingData
            };

            // Validate against schema
            const validatedData = this.schema.parse(cloudEvent);

            return {
                valid: true,
                data: validatedData,
                errors: []
            };
        } catch (error) {
            this.errorCount++;
            
            const errors = error instanceof z.ZodError 
                ? error.errors 
                : [{ message: error.message }];
            
            this.validationErrors.push({
                timestamp: Date.now(),
                input: sensingData,
                errors
            });

            console.error('[P0-VALIDATOR] ❌ Validation failed:', errors);

            return {
                valid: false,
                data: null,
                errors
            };
        }
    }

    /**
     * Get validation statistics
     */
    getStats() {
        return {
            totalValidations: this.validationCount,
            errorCount: this.errorCount,
            successRate: this.validationCount > 0 
                ? ((this.validationCount - this.errorCount) / this.validationCount * 100).toFixed(2) + '%'
                : '0%',
            recentErrors: this.validationErrors.slice(-5)
        };
    }

    /**
     * Reset statistics
     */
    reset() {
        this.validationErrors = [];
        this.validationCount = 0;
        this.errorCount = 0;
    }
}

// P0_VALIDATOR_ID: ZOD_VALIDATOR_V20
