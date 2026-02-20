"""Configuration models for Bodai."""

from pydantic import BaseModel, Field


class PortmapConfig(BaseModel):
    """Port allocation configuration."""

    mcp_range: tuple[int, int] = Field(default=(8676, 8699))
    reserved: dict[int, str] = Field(default_factory=dict)


class StorageMapConfig(BaseModel):
    """Storage and cache allocation configuration."""

    databases: dict[str, str] = Field(default_factory=dict)
    caches: dict[str, str] = Field(default_factory=dict)
    storage: dict[str, str] = Field(default_factory=dict)
