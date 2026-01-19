# Medallion: Bronze | Mutation: 0% | HIVE: I
from openfeature import api
from openfeature.provider.in_memory_provider import InMemoryProvider, InMemoryFlag
import os

# Define initial flags for the Strangler Fig refactor
# Using InMemoryFlag from the specific provider
FLAGS = {
    "hex_hub_enabled": InMemoryFlag(
        state=InMemoryFlag.State.ENABLED,
        default_variant="on",
        variants={"on": True, "off": False}
    ),
    "bft_quorum_v2": InMemoryFlag(
        state=InMemoryFlag.State.ENABLED,
        default_variant="off",
        variants={"on": True, "off": False}
    ),
    "persistent_actors_enabled": InMemoryFlag(
        state=InMemoryFlag.State.ENABLED,
        default_variant="on",
        variants={"on": True, "off": False}
    )
}

def setup_feature_flags():
    """Initializes OpenFeature with an In-Memory provider."""
    provider = InMemoryProvider(flags=FLAGS)
    api.set_provider(provider)
    return api.get_client()

# Singleton-like accessor
client = setup_feature_flags()

def is_enabled(flag_name: str, default: bool = False) -> bool:
    """Helper to check if a feature flag is enabled."""
    return client.get_boolean_value(flag_name, default)
