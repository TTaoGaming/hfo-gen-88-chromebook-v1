// Medallion: Silver | Mutation: 0% | HIVE: V
import { test, expect } from '@playwright/test';
import { P1_FUSE, P1_HandLandmarksContract, P1_PhysicsInputContract, P0_SENSE, P2_SHAPE } from './omega_core';

test.describe('Omega Silver Core Mutation Tests', () => {

    test('P1_HandLandmarksContract should validate correct data', () => {
        const validData = {
            id: 1,
            landmarks: Array(21).fill({ x: 0.1, y: 0.2, z: 0.3 }),
            handedness: 'Left'
        };
        const result = P1_HandLandmarksContract.parse(validData);
        expect(result.id).toBe(1);
        expect(result.landmarks).toHaveLength(21);
        expect(result.handedness).toBe('Left');
    });

    test('P1_HandLandmarksContract should use Right as default handedness', () => {
        const data = {
            landmarks: Array(21).fill({ x: 0, y: 0, z: 0 })
        };
        const result = P1_HandLandmarksContract.parse(data);
        expect(result.handedness).toBe('Right');
    });

    test('P1_PhysicsInputContract should validate velocity structure', () => {
        const data = {
            x: 10,
            y: 20,
            velocity: { x: 1, y: 2 }
        };
        const result = P1_PhysicsInputContract.parse(data);
        expect(result.velocity).toEqual({ x: 1, y: 2 });

        // Negative test for velocity schema
        const invalidVelocity = {
            x: 10,
            y: 20,
            velocity: { x: "high" }
        };
        expect(() => P1_PhysicsInputContract.parse(invalidVelocity)).toThrow();
    });

    test('P1_FUSE should transform landmarks to screen coordinates', () => {
        const rawData = {
            id: 0,
            landmarks: Array(21).fill({ x: 0.5, y: 0.5, z: 0 }),
            handedness: 'Right'
        };
        const config = { width: 1000, height: 1000 };
        const result = P1_FUSE.validateAndFuse(rawData, config);

        expect(result).not.toBeNull();
        if (result) {
            expect(result.x).toBe(500);
            expect(result.y).toBe(500);
            expect(result.intent).toBe('POINTER_READY');
        }
    });

    test('P1_FUSE should return null for invalid data', () => {
        const invalidData = { landmarks: [] };
        const config = { width: 1000, height: 1000 };
        const result = P1_FUSE.validateAndFuse(invalidData, config);
        expect(result).toBeNull();
    });

    test('P1_PhysicsInputContract should support all intents', () => {
        const intents: Array<'IDLE' | 'POINTER_READY' | 'POINTER_COMMIT'> = ['IDLE', 'POINTER_READY', 'POINTER_COMMIT'];
        intents.forEach(intent => {
            const result = P1_PhysicsInputContract.parse({ x: 0, y: 0, intent });
            expect(result.intent).toBe(intent);
        });
    });

    test('P0_SENSE should return default landmarks and handedness', () => {
        const result = P0_SENSE.read();
        expect(result.landmarks).toHaveLength(21);
        expect(result.landmarks[0]).toEqual({ x: 0.5, y: 0.5, z: 0 });
        expect(result.handedness).toBe('Right');
        expect(result.id).toBe(0);
    });

    test('P1_HandLandmarksContract should reject wrong landmark count', () => {
        const data = {
            id: 1,
            landmarks: Array(20).fill({ x: 0, y: 0, z: 0 }),
            handedness: 'Left'
        };
        expect(() => P1_HandLandmarksContract.parse(data)).toThrow();
    });

    test('P2_SHAPE should calculate proportional forces', () => {
        const cursor = { x: 100, y: 100 };
        const target = { x: 200, y: 200 };
        const force = P2_SHAPE.calculateForce(cursor, target);

        // (200 - 100) * 0.005 = 0.5
        expect(force.x).toBeCloseTo(0.5);
        expect(force.y).toBeCloseTo(0.5);
    });

});
