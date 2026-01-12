# Medallion: Bronze | Mutation: 0% | HIVE: I
# 🎯 PORT-3-INJECT: Interaction Finite State Machine (Pointer)

from enum import Enum, auto

class InteractionState(Enum):
    IDLE = auto()
    ARMING = auto()
    ACQUIRING = auto()
    COMMITTED = auto()
    CANCELLED = auto()

class InteractionFSM:
    def __init__(self):
        self.state = InteractionState.IDLE

    def transition(self, event):
        """
        Logic from Cold Bronze:
        IDLE -> ARMING (gesture detected)
        ARMING -> ACQUIRING (target locked)
        ACQUIRING -> COMMITTED (pointer UP / click)
        ARMING/ACQUIRING -> CANCELLED (palm away)
        """
        if self.state == InteractionState.IDLE:
            if event == "GESTURE_DETECTED":
                self.state = InteractionState.ARMING

        elif self.state == InteractionState.ARMING:
            if event == "TARGET_LOCKED":
                self.state = InteractionState.ACQUIRING
            elif event == "PALM_AWAY":
                self.state = InteractionState.CANCELLED

        elif self.state == InteractionState.ACQUIRING:
            if event == "COMMIT":
                self.state = InteractionState.COMMITTED
            elif event == "PALM_AWAY":
                self.state = InteractionState.CANCELLED

        elif self.state == InteractionState.COMMITTED or self.state == InteractionState.CANCELLED:
            self.state = InteractionState.IDLE

        return self.state

# P3_VALIDATOR_ID: OMEGA_FSM_V10
