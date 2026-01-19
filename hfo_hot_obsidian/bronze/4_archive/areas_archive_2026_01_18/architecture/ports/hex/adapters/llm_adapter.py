# Medallion: Bronze | Mutation: 0% | HIVE: I
from ..ports.driven import LLMPort
from typing import Dict, Any, List

class OpenRouterMockAdapter(LLMPort):
    """Temporary Mock Adapter for LLM services."""
    async def request_shards(self, query: str, shards: List[str]) -> Dict[str, Any]:
        return {"status": "MOCK_SUCCESS", "msg": f"Mock sensing for {len(shards)} shards."}

    async def synthesize_baton(self, shards_output: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "MOCK_SUCCESS", "baton": "Mock BATON synthesized."}
