"""Health check functionality for ecosystem components."""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from enum import StrEnum

from bodai.core.config import load_ecosystem
from bodai.models.ecosystem import Component


class HealthStatus(StrEnum):
    """Health status of a component."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


def check_port(
    port: int, host: str = "localhost", timeout: float = 1.0
) -> HealthStatus:
    """Check if a port is accepting connections.

    Args:
        port: Port number to check.
        host: Hostname to connect to.
        timeout: Connection timeout in seconds.

    Returns:
        HealthStatus indicating if the port is accepting connections.

    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return HealthStatus.HEALTHY if result == 0 else HealthStatus.UNHEALTHY
    except OSError:
        return HealthStatus.UNHEALTHY


def check_component(component: Component) -> dict:
    """Check health of a single component.

    Args:
        component: Component to check.

    Returns:
        Dictionary with component health information.

    """
    status = check_port(component.port)
    return {
        "name": component.name,
        "port": component.port,
        "status": status,
        "role": component.role_display,
        "description": component.description,
    }


def check_all() -> dict[str, dict]:
    """Check health of all ecosystem components in parallel.

    Returns:
        Dictionary mapping component names to their health information.

    """
    ecosystem = load_ecosystem()
    results = {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(check_component, comp): name
            for name, comp in ecosystem.components.items()
        }

        for future in as_completed(futures):
            name = futures[future]
            results[name] = future.result()

    return results
