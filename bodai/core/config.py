"""Configuration loading for Bodai."""

from pathlib import Path

import yaml

from bodai.models.config import PortmapConfig, StorageMapConfig
from bodai.models.ecosystem import Component, Ecosystem

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"


def load_ecosystem() -> Ecosystem:
    """Load ecosystem configuration from YAML."""
    config_path = CONFIG_DIR / "ecosystem.yaml"
    with config_path.open() as f:
        data = yaml.safe_load(f)

    components = {}
    for name, comp_data in data.get("components", {}).items():
        components[name] = Component(**comp_data)

    return Ecosystem(components=components)


def load_portmap() -> PortmapConfig:
    """Load portmap configuration from YAML."""
    config_path = CONFIG_DIR / "portmap.yaml"
    with config_path.open() as f:
        data = yaml.safe_load(f)

    core_range = data.get("mcp_core_range", {})
    legacy_range = data.get("mcp_range", {})
    mcp_range = (
        core_range.get("start", legacy_range.get("start", 8676)),
        core_range.get("end", legacy_range.get("end", 8699)),
    )

    reserved = {}

    # Load allocations first (these are assigned ports)
    for port, desc in data.get("allocations", {}).items():
        if isinstance(port, int):
            reserved[port] = desc

    # Then load reserved ranges
    for port, desc in data.get("reserved", {}).items():
        if isinstance(port, int):
            reserved[port] = desc
        elif "-" in str(port):
            # Handle ranges like "8684-8699"
            start, end = map(int, str(port).split("-"))
            for p in range(start, end + 1):
                reserved[p] = desc

    return PortmapConfig(mcp_range=mcp_range, reserved=reserved)


def load_storage_map() -> StorageMapConfig:
    """Load storage map configuration from YAML."""
    config_path = CONFIG_DIR / "storage-map.yaml"
    with config_path.open() as f:
        data = yaml.safe_load(f)

    databases = {
        name: info.get("path", "") for name, info in data.get("databases", {}).items()
    }

    caches = {
        name: f"{info.get('host', 'localhost')}:{info.get('port', 6379)}"
        for name, info in data.get("caches", {}).items()
    }

    storage = {
        name: info.get("bucket", "") for name, info in data.get("storage", {}).items()
    }

    return StorageMapConfig(databases=databases, caches=caches, storage=storage)
