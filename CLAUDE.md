# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bodai (The Orb) is a meta-project for the Bodai ecosystem. It provides configuration, documentation, and operational tooling for managing interconnected components. The project serves as a central hub for ecosystem-wide operations, health monitoring, and configuration management.

## Ecosystem Components

| Component | Role | Port |
|-----------|------|------|
| Mahavishnu | Orchestrator | 8680 |
| Akosha | Seer | 8682 |
| Dhruva | Curator | 8683 |
| Session-Buddy | Builder | 8678 |
| Crackerjack | Inspector | 8676 |

## Development Commands

### Installation

```bash
uv sync --group dev
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_health.py

# Run tests with coverage
pytest --cov=bodai
```

### Code Quality

```bash
# Linting
crackerjack lint

# Type checking
crackerjack typecheck

# Security scanning
crackerjack security
```

### Running CLI

```bash
# Health check command
python -m bodai.cli health

# Dashboard command
python -m bodai.cli dashboard

# Interactive shell
python -m bodai.cli shell
```

## Architecture

The Bodai project is organized into three primary layers:

### 1. Config Layer

- Configuration management for ecosystem components
- YAML-based configuration files for each component
- Environment-specific settings management

### 2. Models Layer

- Pydantic models for data validation and serialization
- Component status and health check models
- Ecosystem topology representations

### 3. Operations Layer

- CLI commands using Typer framework
- Interactive TUI using Textual
- Concurrent operations using ThreadPoolExecutor

## Key Patterns

### Pydantic Models

All data models use Pydantic v2 for validation, serialization, and settings management. Models are defined with strict type hints and comprehensive validation rules.

### Typer CLI Framework

The CLI is built using Typer for intuitive command-line interfaces with automatic help generation and rich formatting via Rich integration.

### Textual TUI

Interactive dashboards and shells use Textual for terminal-based user interfaces with reactive components and event-driven architecture.

### ThreadPoolExecutor

Concurrent health checks and operations across ecosystem components use ThreadPoolExecutor for parallel execution with configurable thread pools.

## Configuration Files

The ecosystem configuration is managed through three YAML files:

1. `config/components.yaml` - Component definitions and connection settings
1. `config/monitoring.yaml` - Health check intervals and thresholds
1. `config/operations.yaml` - Operational procedures and automation rules
