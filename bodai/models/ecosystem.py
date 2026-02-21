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


class ComponentStatus(StrEnum):
    """Status of a component."""

    PRODUCTION = "production"
    DEVELOPMENT = "development"
    DISABLED = "disabled"


class Component(BaseModel):
    """A component in the Bodai ecosystem."""

    name: str
    role: ComponentRole
    port: int = Field(ge=1, le=65535)
    repo: str
    status: ComponentStatus = ComponentStatus.PRODUCTION
    description: str = ""

    @property
    def role_display(self) -> str:
        """Return display name for role."""
        return self.role.value.title()


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
