
const fs = require('fs');
const path = require('path');

// Mock a minimal P1Bridger-like environment to check the math
const systemState = {
    parameters: {
        fsm: {
            hysteresisHigh: 88,
            hysteresisLow: 64,
            chargeTimeMs: 200,
            releaseTimeMs: 200,
            tensionMs: 100
        }
    },
    p1: {
        readinessScores: [0, 0, 0, 0],
        fsmStates: ['IDLE', 'IDLE', 'IDLE', 'IDLE'],
        lastPalmFacingTimes: [0, 0, 0, 0]
    }
};

function simulateFuse(isPalmFacing, dt, now) {
    const i = 0;
    const fsmState = systemState.p1.fsmStates[i];

    if (isPalmFacing) systemState.p1.lastPalmFacingTimes[i] = now;
    const isCharging = isPalmFacing || (now - systemState.p1.lastPalmFacingTimes[i] < systemState.parameters.fsm.tensionMs);

    if (isCharging) {
        const fillAmount = (100 / systemState.parameters.fsm.chargeTimeMs) * dt;
        systemState.p1.readinessScores[i] = Math.min(100, systemState.p1.readinessScores[i] + fillAmount);
    } else {
        const drainAmount = (100 / systemState.parameters.fsm.releaseTimeMs) * dt;
        systemState.p1.readinessScores[i] = Math.max(0, systemState.p1.readinessScores[i] - drainAmount);
    }

    let fsmStateNew = fsmState;
    const readiness = systemState.p1.readinessScores[i];

    if (fsmState === 'IDLE') {
        if (readiness >= systemState.parameters.fsm.hysteresisHigh && (isPalmFacing || isCharging)) fsmStateNew = 'READY';
    } else if (fsmState === 'READY') {
        if (readiness <= systemState.parameters.fsm.hysteresisLow) fsmStateNew = 'IDLE';
    }

    systemState.p1.fsmStates[i] = fsmStateNew;
    return { fsmStateNew, readiness };
}

console.log("Starting IDLE State Check:");
let now = 1000;
let dt = 16.6;
let result = simulateFuse(true, dt, now);
console.log(`Frame 0 (dt=16.6, isPalm=true): State=${result.fsmStateNew}, Readiness=${result.readiness.toFixed(2)}`);

for (let f = 1; f < 20; f++) {
    now += dt;
    result = simulateFuse(true, dt, now);
    if (result.fsmStateNew === 'READY') {
        console.log(`Frame ${f} (t=${(f * dt).toFixed(1)}ms): TRANSITION TO READY! Readiness=${result.readiness.toFixed(2)}`);
        break;
    }
}
