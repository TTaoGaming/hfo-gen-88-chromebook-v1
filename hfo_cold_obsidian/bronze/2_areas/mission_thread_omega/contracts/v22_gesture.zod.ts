// Medallion: Bronze | Mutation: 0% | HIVE: I
import { z } from 'zod';

export const GestureStateSchema = z.enum([
    'IDLE',
    'ARMING',
    'ARMED',
    'SEQ_PALM',
    'SEQ_GAP',
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

export const V22GestureFSMContract = z.object({
    currentState: GestureStateSchema,
    lastGesture: HandGestureSchema,
    dwellStartTime: z.number().optional(),
    commitSequenceStartTime: z.number().optional(),
    pointerEvent: z.enum(['pointerdown', 'pointerup', 'pointermove', 'pointercancel', 'none'])
});

export type V22GestureFSMState = z.infer<typeof V22GestureFSMContract>;
