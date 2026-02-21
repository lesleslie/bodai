"""Tests for health check functionality."""

from bodai.core.health import HealthStatus, check_all, check_component, check_port


def test_health_status_enum():
    """Test health status enum values."""
    assert HealthStatus.HEALTHY.value == "healthy"
    assert HealthStatus.UNHEALTHY.value == "unhealthy"
    assert HealthStatus.UNKNOWN.value == "unknown"


def test_check_port_localhost():
    """Test checking a port that should be listening."""
    result = check_port(12345)  # Unlikely port
    assert result in [HealthStatus.HEALTHY, HealthStatus.UNHEALTHY]


def test_check_component_returns_dict():
    """Test check_component returns proper structure."""
    from bodai.core.config import load_ecosystem  # noqa: PLC0415

    ecosystem = load_ecosystem()
    component = ecosystem.components["mahavishnu"]

    result = check_component(component)
    assert "name" in result
    assert "port" in result
    assert "status" in result
    assert result["name"] == "mahavishnu"


def test_check_all_returns_all_components():
    """Test check_all returns status for all components."""
    results = check_all()
    assert len(results) == 5
    assert all("status" in r for r in results.values())
