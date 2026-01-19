# Medallion: Bronze | Mutation: 0% | HIVE: I
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class PersistencePort(ABC):
    """Driven port for state persistence (Blackboard/DuckDB)."""
    @abstractmethod
    def log_event(self, entry: Dict[str, Any]):
        ...

    @abstractmethod
    def read_last_event(self, phase: str) -> Dict[str, Any]:
        ...

class LLMPort(ABC):
    """Driven port for LLM interactions (OpenRouter)."""
    @abstractmethod
    async def request_shards(self, query: str, shards: List[str]) -> Dict[str, Any]:
        ...

    @abstractmethod
    async def synthesize_baton(self, shards_output: Dict[str, Any]) -> Dict[str, Any]:
        ...
