// Medallion: Bronze | Mutation: 0% | HIVE: I
import { z } from 'zod';
import { CloudEventEnvelopeSchema } from './omega_contracts.zod';

export const GestureStateSchema = z.enum([
    'IDLE',
    'PENDING',
    'ARMING',
    'COMMITTING'
]);

export const HandGestureSchema = z.enum([
    'NONE',
    'OPEN_PALM',
    'POINTING_UP'
]);

export const V21GestureFSMContract = CloudEventEnvelopeSchema.extend({
    type: z.literal('hfo.omega.v21.gesture_fsm'),
    data: z.object({
        currentState: GestureStateSchema,
        lastGesture: HandGestureSchema,
        dwellStartTime: z.number().optional(),
        commitWindowStartTime: z.number().optional(),
        pointerEvent: z.enum(['pointerdown', 'pointerup', 'pointermove', 'pointercancel', 'none'])
    })
});

export type V21GestureFSMState = z.infer<typeof V21GestureFSMContract>;
