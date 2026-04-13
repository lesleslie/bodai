# Repository Guidelines

## Project Structure & Module Organization

- `bodai/` contains the meta-project package for ecosystem operations, including config loading, health checks, CLI commands, and dashboard or shell orchestration.
- Shared configuration lives under `config/`; treat component definitions, monitoring thresholds, and automation rules as source-controlled operational inputs rather than ad hoc local state.
- Tests live in `tests/`; mirror package structure when adding coverage and keep generated artifacts such as `htmlcov/` and temporary health snapshots out of review.
- Repository-level documentation belongs in `README.md`, `CLAUDE.md`, and focused docs under `docs/` when behavior or operator workflows become non-trivial.

## Build, Test, and Development Commands

- `uv sync --group dev` installs the development environment.
- `uv run pytest` runs the full test suite; use `uv run pytest tests/test_health.py` for focused iteration.
- `uv run pytest --cov=bodai --cov-report=html` generates local coverage output in `htmlcov/`.
- `uv run crackerjack lint`, `uv run crackerjack typecheck`, and `uv run crackerjack security` cover the main quality gates.
- `uv run python -m bodai.cli health`, `uv run python -m bodai.cli dashboard`, and `uv run python -m bodai.cli shell` are the primary local smoke-test commands.

## Coding Style & Naming Conventions

- Use explicit type hints, Pydantic models for structured data, and small composable functions for health checks, config transforms, and CLI operations.
- Keep module names snake_case and isolate concerns cleanly: configuration, models, and operations should not bleed into one another.
- Favor extending existing Typer, Rich, and Textual patterns already present in the repo instead of adding parallel CLI or UI frameworks.

## Testing Guidelines

- Add tests with every substantive behavior change, especially around health checks, topology modeling, and cross-component orchestration.
- Prefer deterministic fixtures and mocked component responses over brittle live-network tests unless the scenario explicitly needs end-to-end verification.
- Review `htmlcov/index.html` after larger changes to catch gaps in operational branches and failure-path handling.

## Commit & Pull Request Guidelines

- Use focused commits with clear scope, such as `fix(health): handle partial component failures`.
- PRs should describe the operational behavior change, commands run for validation, and any ecosystem components affected.
- Include screenshots or terminal captures when changing dashboard, shell, or health-report output.

## Ecosystem Notes

- Bodai is the top-level operations repo for the ecosystem; changes here should preserve clean integration with Mahavishnu, Akosha, Dhara, Session-Buddy, Crackerjack, and related MCP services.
- Keep ports, URLs, credentials, and deployment assumptions in configuration rather than embedding them in code paths.

## Security & Configuration Tips

- Never commit secrets, local machine paths, or environment-specific credentials.
- Treat health-check and dashboard code as operator-facing surfaces: validate external inputs and degrade gracefully when components are unavailable.
