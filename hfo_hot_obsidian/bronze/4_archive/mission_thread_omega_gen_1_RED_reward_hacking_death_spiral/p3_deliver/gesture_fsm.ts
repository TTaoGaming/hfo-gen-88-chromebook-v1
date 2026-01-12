// Medallion: Bronze | Mutation: 0% | HIVE: I
// 🛠️ Abstraction Layer: Proxies to the active versioned FSM.

import { GestureFSMV25 } from './gesture_fsm_v25';
import { V25GestureFSMState } from '../contracts/v25_gesture.zod';

export class GestureFSM extends GestureFSMV25 { }
export type GestureFSMState = V25GestureFSMState;
