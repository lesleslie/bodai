"""Tests for config loading."""

from bodai.core.config import load_ecosystem, load_portmap, load_storage_map
from bodai.models.ecosystem import Ecosystem


def test_load_ecosystem():
    """Test loading ecosystem from YAML."""
    ecosystem = load_ecosystem()
    assert isinstance(ecosystem, Ecosystem)
    assert len(ecosystem.components) > 0
    assert "mahavishnu" in ecosystem.components


def test_load_portmap():
    """Test loading portmap from YAML."""
    portmap = load_portmap()
    assert portmap.mcp_range == (8676, 8699)
    assert 8681 in portmap.reserved


def test_load_storage_map():
    """Test loading storage map from YAML."""
    storage = load_storage_map()
    assert "session_buddy" in storage.databases
    assert "redis" in storage.caches
