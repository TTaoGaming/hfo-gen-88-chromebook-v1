# Medallion: Bronze | Mutation: 0% | HIVE: V
import pytest
import sys
import os

# Add path for imports
sys.path.append("/home/tommytai3/active/hfo_gen_88_chromebook_v_1/hfo_hot_obsidian/bronze/2_areas/mission_thread_alpha/p0_observe")

from port_0_tools import port_0_sense, scream

def test_port_0_sense_basic():
    """Basic functional test."""
    receipt = port_0_sense("Phoenix Project")
    assert receipt.startswith("P0_SENSE_")

def test_scream_execution():
    """Verify scream doesn't crash."""
    scream("TEST", "Validation")
    assert True

def test_stigmergy_sensing():
    """Verify stigmergy pillar doesn't crash even if missing."""
    from port_0_tools import sense_stigmergy
    results = sense_stigmergy()
    assert "hot" in results
    assert "cold" in results
