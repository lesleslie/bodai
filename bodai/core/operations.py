"""Ecosystem operations for managing Bodai components.

This module provides the EcosystemOperations class for lifecycle management
of all ecosystem components (start, stop, restart, health aggregation).

Example:
    >>> ops = EcosystemOperations()
    >>> await ops.start_all()
    {'mahavishnu': True, 'session-buddy': True, ...}
    >>> health = await ops.health_aggregate()
    >>> print(f"Ecosystem health: {health.health_percentage:.0f}%")
"""

from __future__ import annotations

import asyncio
import os
import signal
import time
from dataclasses import dataclass, field
from datetime import datetime
import shlex
from pathlib import Path
from typing import Any

import httpx

from bodai.core.config import load_ecosystem
from bodai.core.health import HealthStatus, check_port
from bodai.models.ecosystem import Component, ComponentStatus


@dataclass
class ProcessInfo:
    """Information about a managed process."""

    pid: int
    name: str
    started_at: datetime = field(default_factory=datetime.now)
    port: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pid": self.pid,
            "name": self.name,
            "started_at": self.started_at.isoformat(),
            "port": self.port,
        }


@dataclass
class ComponentHealth:
    """Health status of a single component."""

    name: str
    port: int
    status: HealthStatus
    response_time_ms: float = 0.0
    error: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def is_healthy(self) -> bool:
        """Check if component is healthy."""
        return self.status == HealthStatus.HEALTHY

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "port": self.port,
            "status": self.status.value,
            "is_healthy": self.is_healthy,
            "response_time_ms": self.response_time_ms,
            "error": self.error,
            "details": self.details,
        }


@dataclass
class EcosystemHealth:
    """Aggregated health status of the ecosystem."""

    components: list[ComponentHealth] = field(default_factory=list)
    checked_at: datetime = field(default_factory=datetime.now)

    @property
    def total_count(self) -> int:
        """Total number of components."""
        return len(self.components)

    @property
    def healthy_count(self) -> int:
        """Number of healthy components."""
        return sum(1 for c in self.components if c.is_healthy)

    @property
    def unhealthy_count(self) -> int:
        """Number of unhealthy components."""
        return self.total_count - self.healthy_count

    @property
    def health_percentage(self) -> float:
        """Percentage of healthy components."""
        if self.total_count == 0:
            return 0.0
        return (self.healthy_count / self.total_count) * 100

    @property
    def is_healthy(self) -> bool:
        """Check if ecosystem is healthy (all components healthy)."""
        return self.unhealthy_count == 0 and self.total_count > 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "total_count": self.total_count,
            "healthy_count": self.healthy_count,
            "unhealthy_count": self.unhealthy_count,
            "health_percentage": round(self.health_percentage, 1),
            "is_healthy": self.is_healthy,
            "checked_at": self.checked_at.isoformat(),
            "components": [c.to_dict() for c in self.components],
        }


class EcosystemOperations:
    """Manage ecosystem component lifecycle.

    Provides methods to start, stop, restart, and monitor
    all components in the Bodai ecosystem.

    Example:
        >>> ops = EcosystemOperations()
        >>> # Start all components
        >>> results = await ops.start_all()
        >>> # Check health
        >>> health = await ops.health_aggregate()
        >>> print(f"Health: {health.health_percentage:.0f}%")
    """

    def __init__(
        self,
        health_timeout: float = 5.0,
        shutdown_timeout: float = 30.0,
    ) -> None:
        """Initialize ecosystem operations.

        Args:
            health_timeout: Timeout for health check requests in seconds.
            shutdown_timeout: Default timeout for graceful shutdown in seconds.
        """
        self._ecosystem = load_ecosystem()
        self._health_timeout = health_timeout
        self._shutdown_timeout = shutdown_timeout
        self._managed_processes: dict[str, ProcessInfo] = {}

    @property
    def components(self) -> dict[str, Component]:
        """Get all ecosystem components."""
        return self._ecosystem.components

    def _get_component(self, name: str) -> Component | None:
        """Get a component by name.

        Args:
            name: Component name.

        Returns:
            Component if found, None otherwise.
        """
        return self._ecosystem.get_component(name)

    def _component_to_start_command(self, component: Component) -> list[str] | None:
        """Convert component to start command.

        Args:
            component: Component to convert.

        Returns:
            Command list or None if cannot determine.
        """
        repo_path = Path(component.repo).expanduser()
        if not repo_path.exists():
            return None

        # Prefer explicit component-level launch command when provided.
        if component.start_command:
            return [os.path.expandvars(part) for part in component.start_command]

        # Determine start command based on repo structure
        # Check for pyproject.toml (Python project)
        pyproject = repo_path / "pyproject.toml"
        if pyproject.exists():
            # Extract package name from pyproject.toml
            package_name = repo_path.name.replace("-", "_")
            return [
                "python",
                "-m",
                f"{package_name}.mcp.server",
            ]

        return None

    async def _find_process_on_port(self, port: int) -> int | None:
        """Find process ID listening on a port.

        Args:
            port: Port number to check.

        Returns:
            PID if found, None otherwise.
        """
        try:
            proc = await asyncio.create_subprocess_exec(
                "lsof",
                "-i",
                f":{port}",
                "-t",
                "-sTCP:LISTEN",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
            )
            stdout, _ = await proc.communicate()
            if stdout:
                pids = stdout.decode().strip().split("\n")
                if pids and pids[0]:
                    return int(pids[0])
        except (OSError, ValueError):
            pass
        return None

    async def _wait_for_port(
        self,
        port: int,
        timeout: float = 30.0,
        interval: float = 0.5,
    ) -> bool:
        """Wait for a port to become available.

        Args:
            port: Port number to wait for.
            timeout: Maximum time to wait in seconds.
            interval: Time between checks in seconds.

        Returns:
            True if port became available, False if timeout.
        """
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            if check_port(port) == HealthStatus.HEALTHY:
                return True
            await asyncio.sleep(interval)
        return False

    async def start_component(self, name: str) -> bool:
        """Start a single ecosystem component.

        Args:
            name: Component name to start.

        Returns:
            True if started successfully, False otherwise.
        """
        component = self._get_component(name)
        if not component:
            return False

        # Skip disabled components
        if component.status == ComponentStatus.DISABLED:
            return False

        # Non-network components are not lifecycle-managed here.
        if component.port is None:
            return False

        # Check if already running
        if check_port(component.port, host=component.host) == HealthStatus.HEALTHY:
            return True

        # Get start command
        cmd = self._component_to_start_command(component)
        if not cmd:
            return False

        repo_path = Path(component.repo).expanduser()

        try:
            # Backward compatibility: if start_command is provided as a single
            # tokenized string item, normalize it here.
            if len(cmd) == 1 and " " in cmd[0]:
                cmd = shlex.split(cmd[0])

            child_env = {**os.environ, **component.env}

            # Start the process
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=repo_path,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
                start_new_session=True,
                env=child_env,
            )

            # Track the process
            self._managed_processes[name] = ProcessInfo(
                pid=proc.pid,
                name=name,
                port=component.port,
            )

            # Wait for port to become available
            started = await self._wait_for_port(component.port, timeout=30.0)
            return started

        except OSError:
            return False

    async def stop_component(
        self,
        name: str,
        timeout: float | None = None,
    ) -> bool:
        """Stop a single ecosystem component.

        Args:
            name: Component name to stop.
            timeout: Timeout for graceful shutdown in seconds.

        Returns:
            True if stopped successfully, False otherwise.
        """
        component = self._get_component(name)
        if not component:
            return False

        timeout = timeout or self._shutdown_timeout

        # Find process on port
        pid = await self._find_process_on_port(component.port)
        if not pid:
            # Already stopped
            self._managed_processes.pop(name, None)
            return True

        try:
            # Send SIGTERM for graceful shutdown
            os.kill(pid, signal.SIGTERM)

            # Wait for process to stop
            start = time.monotonic()
            while time.monotonic() - start < timeout:
                if check_port(component.port, host=component.host) == HealthStatus.UNHEALTHY:
                    self._managed_processes.pop(name, None)
                    return True
                await asyncio.sleep(0.5)

            # Force kill if still running
            try:
                os.kill(pid, signal.SIGKILL)
                await asyncio.sleep(1)
            except ProcessLookupError:
                pass

            self._managed_processes.pop(name, None)
            return check_port(component.port) == HealthStatus.UNHEALTHY

        except ProcessLookupError:
            # Process already gone
            self._managed_processes.pop(name, None)
            return True
        except OSError:
            return False

    async def restart_component(
        self,
        name: str,
        timeout: float | None = None,
    ) -> bool:
        """Restart a single ecosystem component.

        Args:
            name: Component name to restart.
            timeout: Timeout for graceful shutdown in seconds.

        Returns:
            True if restarted successfully, False otherwise.
        """
        # Stop first
        stopped = await self.stop_component(name, timeout=timeout)
        if not stopped:
            return False

        # Brief pause
        await asyncio.sleep(1)

        # Start again
        return await self.start_component(name)

    async def start_all(self) -> dict[str, bool]:
        """Start all ecosystem components concurrently.

        Returns:
            Dictionary mapping component names to start success status.
        """
        # Get all production components
        components = [
            name
            for name, comp in self.components.items()
            if comp.status != ComponentStatus.DISABLED
        ]

        # Start all concurrently
        tasks = {name: asyncio.create_task(self.start_component(name)) for name in components}

        results = {}
        for name, task in tasks.items():
            try:
                results[name] = await task
            except Exception:
                results[name] = False

        return results

    async def stop_all(self, timeout: float | None = None) -> dict[str, bool]:
        """Stop all ecosystem components concurrently.

        Args:
            timeout: Timeout for graceful shutdown per component in seconds.

        Returns:
            Dictionary mapping component names to stop success status.
        """
        # Get all running components
        components = [
            name
            for name, comp in self.components.items()
            if check_port(comp.port, host=comp.host) == HealthStatus.HEALTHY
        ]

        # Stop all concurrently
        tasks = {
            name: asyncio.create_task(self.stop_component(name, timeout=timeout))
            for name in components
        }

        results = {}
        for name, task in tasks.items():
            try:
                results[name] = await task
            except Exception:
                results[name] = False

        return results

    async def _check_component_health(
        self,
        component: Component,
    ) -> ComponentHealth:
        """Check health of a single component via HTTP.

        Args:
            component: Component to check.

        Returns:
            ComponentHealth with check results.
        """
        path = component.health_path if component.health_path.startswith("/") else f"/{component.health_path}"
        scheme = component.health_scheme
        host = component.host
        url = f"{scheme}://{host}:{component.port}{path}"
        start_time = time.monotonic()

        try:
            async with httpx.AsyncClient(timeout=self._health_timeout) as client:
                response = await client.get(url)
                elapsed_ms = (time.monotonic() - start_time) * 1000

                if response.status_code == 200:
                    try:
                        details = response.json()
                    except Exception:
                        details = {}

                    return ComponentHealth(
                        name=component.name,
                        port=component.port,
                        status=HealthStatus.HEALTHY,
                        response_time_ms=round(elapsed_ms, 2),
                        details=details,
                    )
                else:
                    return ComponentHealth(
                        name=component.name,
                        port=component.port,
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=round(elapsed_ms, 2),
                        error=f"HTTP {response.status_code}",
                    )

        except httpx.TimeoutException:
            return ComponentHealth(
                name=component.name,
                port=component.port,
                status=HealthStatus.UNHEALTHY,
                details={"url": url},
                error="Timeout",
            )
        except httpx.ConnectError:
            return ComponentHealth(
                name=component.name,
                port=component.port,
                status=HealthStatus.UNHEALTHY,
                details={"url": url},
                error="Connection refused",
            )
        except Exception as e:
            return ComponentHealth(
                name=component.name,
                port=component.port,
                status=HealthStatus.UNKNOWN,
                details={"url": url},
                error=str(e),
            )

    async def health_aggregate(self) -> EcosystemHealth:
        """Aggregate health status across all ecosystem components.

        Performs HTTP health checks on all components concurrently.

        Returns:
            EcosystemHealth with aggregated status.
        """
        # Check all components concurrently
        tasks = {
            name: asyncio.create_task(self._check_component_health(comp))
            for name, comp in self.components.items()
            if comp.status != ComponentStatus.DISABLED
        }

        components = []
        for name, task in tasks.items():
            try:
                health = await task
                components.append(health)
            except Exception as e:
                comp = self.components[name]
                components.append(
                    ComponentHealth(
                        name=name,
                        port=comp.port,
                        status=HealthStatus.UNKNOWN,
                details={"url": url},
                error=str(e),
                    )
                )

        return EcosystemHealth(components=components)

    def get_managed_processes(self) -> dict[str, ProcessInfo]:
        """Get information about processes managed by this instance.

        Returns:
            Dictionary mapping component names to ProcessInfo.
        """
        return self._managed_processes.copy()


# Convenience functions for CLI usage
async def start_ecosystem() -> dict[str, bool]:
    """Start all ecosystem components."""
    ops = EcosystemOperations()
    return await ops.start_all()


async def stop_ecosystem(timeout: float = 30.0) -> dict[str, bool]:
    """Stop all ecosystem components."""
    ops = EcosystemOperations()
    return await ops.stop_all(timeout=timeout)


async def check_ecosystem_health() -> EcosystemHealth:
    """Check health of all ecosystem components."""
    ops = EcosystemOperations()
    return await ops.health_aggregate()
