// Medallion: Bronze | Mutation: 0% | HIVE: I
import { z } from 'zod';
import { CloudEventEnvelopeSchema } from './omega_contracts.zod';

export const GestureStateSchema = z.enum([
    'IDLE',
    'ARMING',
    'ARMED',
    'COMMITTING',
    'COMMITTED',
    'RELEASING'
]);

export const HandGestureSchema = z.enum([
    'NONE',
    'OPEN_PALM',
    'POINTING_UP',
    'VICTORY',
    'THUMBS_UP',
    'THUMBS_DOWN'
]);

export const V24GestureFSMContract = CloudEventEnvelopeSchema.extend({
    type: z.literal('hfo.omega.v24.gesture_fsm'),
    data: z.object({
        currentState: GestureStateSchema,
        lastGesture: HandGestureSchema,
        progress: z.number().default(0), // For leaking bucket (0-1000)
        recoveryStartTime: z.number().optional(),
        dwellStartTime: z.number().optional(),
        pointerEvent: z.enum(['pointerdown', 'pointerup', 'pointermove', 'pointercancel', 'none'])
    })
});

export type V24GestureFSMState = z.infer<typeof V24GestureFSMContract>;
