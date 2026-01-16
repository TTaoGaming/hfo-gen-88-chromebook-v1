# Medallion: Bronze | Mutation: 0% | HIVE: I
from base_actor import HardenedBaseActor
from typing import Dict, Any

class NavigatorActor(HardenedBaseActor):
    """
    Navigator Actor (Port 7) for HFO Mission Thread Alpha.
    Manages the Galois Lattice [8x8] state and high-level mission goals.
    """
    def __init__(self, actor_id: str = "P7_NAVIGATOR"):
        super().__init__(actor_id=actor_id, mission_thread="ALPHA")
        if "galois_lattice" not in self.state:
            self.state["galois_lattice"] = self._initialize_lattice()
            self.persist_state()

    def _initialize_lattice(self) -> Dict[str, Any]:
        """Initializes an empty 8x8 Galois Lattice."""
        lattice = {}
        for x in range(8):
            for y in range(8):
                lattice[f"{x},{y}"] = {"status": "UNINITIALIZED", "data": None}
        return lattice

    def update_tile(self, x: int, y: int, status: str, data: Any = None):
        """Updates a specific tile in the Galois Lattice."""
        coord = f"{x},{y}"
        if coord in self.state["galois_lattice"]:
            self.state["galois_lattice"][coord] = {
                "status": status,
                "data": data,
                "last_update": self._get_timestamp()
            }
            self.update_state("galois_lattice", self.state["galois_lattice"])
            self.log_event("LATTICE_UPDATE", {"coord": coord, "status": status})

    def _get_timestamp(self) -> str:
        import datetime
        return datetime.datetime.now(datetime.timezone.utc).isoformat()

    def get_mission_summary(self) -> str:
        initialized = sum(1 for tile in self.state["galois_lattice"].values() if tile["status"] != "UNINITIALIZED")
        return f"Galois Lattice Coverage: {initialized}/64 tiles."
