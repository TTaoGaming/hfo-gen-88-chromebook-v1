# Medallion: Bronze | Mutation: 0% | HIVE: I
try:
    from .base_actor import HardenedBaseActor
except (ImportError, ValueError):
    from base_actor import HardenedBaseActor
from typing import Dict, Any

class LidlessLegion(HardenedBaseActor):
    """P0: Sense | Observe | ISR"""
    def __init__(self):
        super().__init__(actor_id="P0_LIDLESS", mission_thread="ALPHA")

class MirrorMagus(HardenedBaseActor):
    """P2: Shape | Digital Twin"""
    def __init__(self):
        super().__init__(actor_id="P2_MAGUS", mission_thread="ALPHA")

class HarmonicHydra(HardenedBaseActor):
    """P3: Deliver | Injector"""
    def __init__(self):
        super().__init__(actor_id="P3_HYDRA", mission_thread="ALPHA")

class RedRegnant(HardenedBaseActor):
    """P4: Disrupt | MDO"""
    def __init__(self):
        super().__init__(actor_id="P4_REGNANT", mission_thread="ALPHA")

class PyrePraetorian(HardenedBaseActor):
    """P5: Defend | Immunize"""
    def __init__(self):
        super().__init__(actor_id="P5_PRAETORIAN", mission_thread="ALPHA")

class KrakenKeeper(HardenedBaseActor):
    """P6: Store | Assimilate"""
    def __init__(self):
        super().__init__(actor_id="P6_KRAKEN", mission_thread="ALPHA")
