"""Pydantic models for ecosystem configuration."""

from enum import StrEnum

from pydantic import BaseModel, Field


class ComponentRole(StrEnum):
    """Role of a component in the ecosystem."""

    ORCHESTRATOR = "orchestrator"
    SEER = "seer"
    RESOLVER = "resolver"
    CURATOR = "curator"
    BUILDER = "builder"
    INSPECTOR = "inspector"
    COMPOSER = "composer"
    PRESENTER = "presenter"
    DOCTOR = "doctor"
    TOOL = "tool"


class ComponentStatus(StrEnum):
    """Status of a component."""

    PRODUCTION = "production"
    DEVELOPMENT = "development"
    DISABLED = "disabled"


class Component(BaseModel):
    """A component in the Bodai ecosystem."""

    name: str
    role: ComponentRole
    port: int | None = Field(default=None, ge=1, le=65535)
    repo: str
    nicknames: list[str] = Field(default_factory=list)
    status: ComponentStatus = ComponentStatus.PRODUCTION
    description: str = ""
    host: str = "localhost"
    health_path: str = "/health"
    health_scheme: str = "http"
    start_command: list[str] | None = None
    env: dict[str, str] = Field(default_factory=dict)

    @property
    def role_display(self) -> str:
        """Return display name for role."""
        return self.role.value.title()

    def matches_identifier(self, identifier: str) -> bool:
        """Return True when identifier matches the name or any nickname alias."""
        return identifier == self.name or identifier in self.nicknames


class Ecosystem(BaseModel):
    """The complete Bodai ecosystem."""

    components: dict[str, Component] = Field(default_factory=dict)

    def get_by_port(self, port: int) -> Component | None:
        """Get component by port number."""
        for component in self.components.values():
            if component.port == port:
                return component
        return None

    def get_by_role(self, role: ComponentRole) -> Component | None:
        """Get component by role."""
        for component in self.components.values():
            if component.role == role:
                return component
        return None

    def get_component(self, identifier: str) -> Component | None:
        """Get component by registry key, canonical name, or nickname alias."""
        if component := self.components.get(identifier):
            return component

        for component in self.components.values():
            if component.matches_identifier(identifier):
                return component

        return None
