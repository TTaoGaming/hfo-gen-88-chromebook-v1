// Medallion: Bronze | Mutation: 0% | HIVE: I
import { z } from 'zod';

export const GestureStateSchema = z.enum([
    'IDLE',
    'ARMING',
    'ARMED',
    'COMMITTING',
    'COMMITTED'
]);

export const HandGestureSchema = z.enum([
    'NONE',
    'OPEN_PALM',
    'POINTING_UP',
    'VICTORY',
    'THUMBS_UP',
    'THUMBS_DOWN'
]);

export const V23GestureFSMContract = z.object({
    currentState: GestureStateSchema,
    lastGesture: HandGestureSchema,
    dwellStartTime: z.number().optional(),
    recoveryStartTime: z.number().optional(),
    pointerEvent: z.enum(['pointerdown', 'pointerup', 'pointermove', 'pointercancel', 'none'])
});

export type V23GestureFSMState = z.infer<typeof V23GestureFSMContract>;
