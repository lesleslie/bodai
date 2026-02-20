"""Tests for ecosystem models."""

import pytest
from pydantic import ValidationError

from bodai.models.ecosystem import Component, ComponentRole, ComponentStatus, Ecosystem


def test_component_creation():
    """Test creating a component."""
    component = Component(
        name="mahavishnu",
        role=ComponentRole.ORCHESTRATOR,
        port=8680,
        repo="~/Projects/mahavishnu",
        status=ComponentStatus.PRODUCTION,
        description="Multi-engine workflow orchestration",
    )
    assert component.name == "mahavishnu"
    assert component.port == 8680
    assert component.role == ComponentRole.ORCHESTRATOR


def test_ecosystem_creation():
    """Test creating an ecosystem with components."""
    ecosystem = Ecosystem(
        components={
            "mahavishnu": Component(
                name="mahavishnu",
                role=ComponentRole.ORCHESTRATOR,
                port=8680,
                repo="~/Projects/mahavishnu",
                status=ComponentStatus.PRODUCTION,
                description="Orchestrator",
            ),
            "akosha": Component(
                name="akosha",
                role=ComponentRole.SEER,
                port=8682,
                repo="~/Projects/akosha",
                status=ComponentStatus.PRODUCTION,
                description="Seer",
            ),
        }
    )
    assert len(ecosystem.components) == 2
    assert "mahavishnu" in ecosystem.components


def test_component_role_display():
    """Test role display name."""
    component = Component(
        name="test",
        role=ComponentRole.ORCHESTRATOR,
        port=8000,
        repo="~/test",
        status=ComponentStatus.PRODUCTION,
        description="Test",
    )
    assert component.role_display == "Orchestrator"


def test_component_default_status():
    """Test component defaults to PRODUCTION status."""
    component = Component(
        name="test",
        role=ComponentRole.BUILDER,
        port=8000,
        repo="~/test",
        description="Test",
    )
    assert component.status == ComponentStatus.PRODUCTION


def test_component_port_validation():
    """Test port validation (1-65535)."""
    # Valid port
    component = Component(
        name="test",
        role=ComponentRole.BUILDER,
        port=8080,
        repo="~/test",
    )
    assert component.port == 8080

    # Invalid port - too low
    with pytest.raises(ValidationError):
        Component(
            name="test",
            role=ComponentRole.BUILDER,
            port=0,
            repo="~/test",
        )

    # Invalid port - too high
    with pytest.raises(ValidationError):
        Component(
            name="test",
            role=ComponentRole.BUILDER,
            port=70000,
            repo="~/test",
        )


def test_ecosystem_empty():
    """Test creating an empty ecosystem."""
    ecosystem = Ecosystem()
    assert len(ecosystem.components) == 0


def test_ecosystem_get_by_port():
    """Test getting component by port."""
    ecosystem = Ecosystem(
        components={
            "mahavishnu": Component(
                name="mahavishnu",
                role=ComponentRole.ORCHESTRATOR,
                port=8680,
                repo="~/Projects/mahavishnu",
            ),
            "akosha": Component(
                name="akosha",
                role=ComponentRole.SEER,
                port=8682,
                repo="~/Projects/akosha",
            ),
        }
    )

    found = ecosystem.get_by_port(8680)
    assert found is not None
    assert found.name == "mahavishnu"

    not_found = ecosystem.get_by_port(9999)
    assert not_found is None


def test_ecosystem_get_by_role():
    """Test getting component by role."""
    ecosystem = Ecosystem(
        components={
            "mahavishnu": Component(
                name="mahavishnu",
                role=ComponentRole.ORCHESTRATOR,
                port=8680,
                repo="~/Projects/mahavishnu",
            ),
            "akosha": Component(
                name="akosha",
                role=ComponentRole.SEER,
                port=8682,
                repo="~/Projects/akosha",
            ),
        }
    )

    found = ecosystem.get_by_role(ComponentRole.SEER)
    assert found is not None
    assert found.name == "akosha"

    not_found = ecosystem.get_by_role(ComponentRole.CURATOR)
    assert not_found is None


def test_component_role_values():
    """Test all component role enum values."""
    assert ComponentRole.ORCHESTRATOR.value == "orchestrator"
    assert ComponentRole.SEER.value == "seer"
    assert ComponentRole.RESOLVER.value == "resolver"
    assert ComponentRole.CURATOR.value == "curator"
    assert ComponentRole.BUILDER.value == "builder"
    assert ComponentRole.INSPECTOR.value == "inspector"


def test_component_status_values():
    """Test all component status enum values."""
    assert ComponentStatus.PRODUCTION.value == "production"
    assert ComponentStatus.DEVELOPMENT.value == "development"
    assert ComponentStatus.DISABLED.value == "disabled"


# Config model tests

from bodai.models.config import PortmapConfig, StorageMapConfig


def test_portmap_config():
    """Test portmap configuration."""
    portmap = PortmapConfig(
        mcp_range=(8676, 8699),
        reserved={8681: "available"},
    )
    assert portmap.mcp_range == (8676, 8699)
    assert 8681 in portmap.reserved


def test_storage_map_config():
    """Test storage map configuration."""
    storage = StorageMapConfig(
        databases={
            "session_buddy": "~/data/session-buddy/session_buddy.db",
            "akosha_hot": "~/data/akosha/hot.db",
        },
        caches={
            "redis": "localhost:6379",
        },
    )
    assert "session_buddy" in storage.databases
    assert "redis" in storage.caches
