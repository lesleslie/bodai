# Bodai - The Orb

Central meta-project for the Bodai ecosystem, providing configuration, documentation, and operations for all components.

## Ecosystem Components

| Component | Role | Port | Description |
|-----------|------|------|-------------|
| Mahavishnu | The Orchestrator | 8680 | Multi-engine workflow orchestration |
| Akosha | The Seer | 8682 | Cross-system intelligence |
| Dhruva | The Curator | 8683 | Persistent object storage |
| Session-Buddy | The Builder | 8678 | Session management |
| Crackerjack | The Inspector | 8676 | Quality gates and CI/CD |

## Installation

```bash
uv sync
```

## Commands

Bodai provides a unified CLI for managing the ecosystem:

| Command | Description |
|---------|-------------|
| `bodai health` | Check health status of all ecosystem components |
| `bodai start` | Start all ecosystem services |
| `bodai stop` | Stop all ecosystem services |
| `bodai restart` | Restart all ecosystem services |
| `bodai dashboard` | Launch the interactive monitoring dashboard |
| `bodai shell` | Open an interactive management shell |
| `bodai config show` | Display current configuration |
| `bodai config validate` | Validate configuration files |

## Architecture

For detailed architecture documentation, see [docs/architecture.md](docs/architecture.md).

## The Orb Metaphor

Bodai (meaning "The Orb" in Sanskrit) serves as the central hub that connects and illuminates all components of the ecosystem:

- **Configuration**: Central registry of all components, their ports, and interdependencies
- **Documentation**: Comprehensive guides explaining how the ecosystem works together
- **Operations**: Tools to manage ecosystem health, start/stop services, and monitor status

Like an orb that reflects and contains everything around it, Bodai provides the meta-layer that makes the ecosystem greater than the sum of its parts.

## Development

### Running Tests

```bash
pytest
```

### Quality Checks

```bash
crackerjack run
```
